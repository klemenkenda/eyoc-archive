"""LLM-based independent audit of EYOC normalized CSVs via OpenRouter.

The script groups normalized rows by raw `source_file`, sends the raw source text plus
the matching CSV rows to an OpenRouter model, and writes one combined Markdown report.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Any
from urllib import error, request
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
RAW = RESULTS / "raw"
SCRIPT_DIR = Path(__file__).resolve().parent
PROMPT_FILE = SCRIPT_DIR / "openrouter_audit_prompt.txt"
DEFAULT_REPORT = RAW / "OPENROUTER-DATA-AUDIT.md"
CACHE_DIR = SCRIPT_DIR / "cache"
ENV_FILE = ROOT / ".env"

INDIVIDUAL_COLUMNS = [
    "class",
    "rank",
    "status",
    "bib",
    "country",
    "name",
    "time_seconds",
    "confidence",
    "source_file",
]
RELAY_COLUMNS = [
    "class",
    "rank",
    "status",
    "country",
    "team",
    "total_time_seconds",
    "leg1_name",
    "leg1_time_seconds",
    "leg2_name",
    "leg2_time_seconds",
    "leg3_name",
    "leg3_time_seconds",
    "confidence",
    "source_file",
]


@dataclass
class SourceBundle:
    source_rel: str
    csv_rows: dict[str, list[dict[str, str]]]


@dataclass
class AuditTask:
    source_rel: str
    csv_rows: dict[str, list[dict[str, str]]]
    label: str
    class_names: tuple[str, ...] = ()


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
            value = value[1:-1]
        os.environ.setdefault(key, value)


def plain_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".htm", ".html"}:
        raw = path.read_bytes()
        try:
            decoded = raw.decode("utf-8")
        except UnicodeDecodeError:
            decoded = raw.decode("cp1250", errors="replace")
        decoded = re.sub(r"<br\s*/?>", "\n", decoded, flags=re.IGNORECASE)
        return html.unescape(re.sub(r"<[^>]+>", " ", decoded))
    if suffix in {".xml", ".csv", ".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".pdf":
        try:
            import fitz
        except ImportError:
            return ""
        parts: list[str] = []
        with fitz.open(str(path)) as document:
            for page in document:
                parts.append(page.get_text())
        return "\n".join(parts)
    return path.read_text(encoding="utf-8", errors="replace")


def normalize_class(text: str | None) -> str | None:
    if not text:
        return None
    value = text.strip().upper().replace(" ", "")
    if value.startswith("WOMEN"):
        value = "W" + value[5:]
    elif value.startswith("WOMAN"):
        value = "W" + value[5:]
    elif value.startswith("MEN"):
        value = "M" + value[3:]
    value = value.rstrip("E")
    if value in {"M16", "M18", "W16", "W18"}:
        return value
    if value in {"MIX", "MIXT", "MIXED"}:
        return "Mixed"
    return None


def strip_ns(root: ET.Element) -> ET.Element:
    for element in root.iter():
        if "}" in element.tag:
            element.tag = element.tag.split("}", 1)[1]
    return root


def xml_class_name(class_result: ET.Element) -> str | None:
    event_class = class_result.find("EventClass")
    if event_class is not None:
        for tag_name in ("ClassShortName", "Name"):
            found = event_class.find(tag_name)
            if found is not None and found.text:
                klass = normalize_class(found.text)
                if klass:
                    return klass
    klass = class_result.find("Class")
    if klass is not None:
        name = klass.find("Name")
        if name is not None and name.text:
            return normalize_class(name.text)
    return None


def xml_text_for_classes(path: Path, class_names: tuple[str, ...]) -> str:
    try:
        root = strip_ns(ET.parse(path).getroot())
    except ET.ParseError:
        return plain_text(path)

    snippets: list[str] = []
    for class_result in root.findall(".//ClassResult"):
        klass = xml_class_name(class_result)
        if klass in class_names:
            snippets.append(ET.tostring(class_result, encoding="unicode"))
    if not snippets:
        return plain_text(path)
    return "\n\n".join(snippets)


def render_csv_rows(rows: list[dict[str, str]], fieldnames: list[str]) -> str:
    handle = StringIO()
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({name: row.get(name, "") for name in fieldnames})
    return handle.getvalue().strip()


def collect_bundles() -> list[SourceBundle]:
    grouped: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for csv_file in sorted(RESULTS.glob("[0-9][0-9][0-9][0-9]/*.csv")):
        with csv_file.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        rel_csv = csv_file.relative_to(RESULTS).as_posix()
        for row in rows:
            source_rel = row.get("source_file", "").strip()
            if not source_rel:
                continue
            grouped[source_rel][rel_csv].append(row)
    return [SourceBundle(source_rel=source_rel, csv_rows=dict(sorted(csv_rows.items())))
            for source_rel, csv_rows in sorted(grouped.items())]


def classes_in_rows(rows: list[dict[str, str]]) -> tuple[str, ...]:
    return tuple(sorted({row.get("class", "").strip() for row in rows if row.get("class", "").strip()}))


def split_bundle(bundle: SourceBundle) -> list[AuditTask]:
    source_path = RAW / bundle.source_rel
    if source_path.suffix.lower() != ".xml":
        return [AuditTask(source_rel=bundle.source_rel, csv_rows=bundle.csv_rows, label=bundle.source_rel)]

    grouped_by_class: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for rel_csv, rows in bundle.csv_rows.items():
        for row in rows:
            klass = row.get("class", "").strip() or "UNKNOWN"
            grouped_by_class[klass][rel_csv].append(row)

    if len(grouped_by_class) <= 1:
        only_classes = classes_in_rows(next(iter(bundle.csv_rows.values()), []))
        return [AuditTask(source_rel=bundle.source_rel, csv_rows=bundle.csv_rows, label=bundle.source_rel, class_names=only_classes)]

    tasks: list[AuditTask] = []
    for klass, csv_rows in sorted(grouped_by_class.items()):
        tasks.append(
            AuditTask(
                source_rel=bundle.source_rel,
                csv_rows=dict(sorted(csv_rows.items())),
                label=f"{bundle.source_rel} [{klass}]",
                class_names=(klass,),
            )
        )
    return tasks


def build_user_payload(task: AuditTask) -> str:
    source_path = RAW / task.source_rel
    if source_path.suffix.lower() == ".xml" and task.class_names:
        raw_text = xml_text_for_classes(source_path, task.class_names)
    else:
        raw_text = plain_text(source_path)
    raw_warning = ""
    if not raw_text.strip():
        raw_warning = (
            "WARNING: the raw file could not be rendered as useful text in this environment. "
            "Treat conclusions as lower-confidence and avoid overcalling issues."
        )

    csv_blocks: list[str] = []
    for rel_csv, rows in task.csv_rows.items():
        fieldnames = RELAY_COLUMNS if rel_csv.endswith("relay.csv") else INDIVIDUAL_COLUMNS
        csv_blocks.append(f"### {rel_csv}\n```csv\n{render_csv_rows(rows, fieldnames)}\n```")

    return "\n".join(
        [
            f"RAW_SOURCE_FILE: {task.source_rel}",
            f"AUDIT_TASK_LABEL: {task.label}",
            f"AUDIT_CLASSES: {', '.join(task.class_names) if task.class_names else '(all)'}",
            f"RAW_SOURCE_EXTENSION: {source_path.suffix.lower() or '(none)'}",
            f"RELATED_CSV_FILES: {', '.join(task.csv_rows)}",
            raw_warning,
            "",
            "RAW_SOURCE_TEXT:",
            "```text",
            raw_text if raw_text.strip() else "[no raw text extracted]",
            "```",
            "",
            "EXTRACTED_CSV_ROWS:",
            *csv_blocks,
        ]
    )


def cache_key(model: str, prompt_text: str, user_payload: str) -> str:
    digest = hashlib.sha256()
    digest.update(model.encode("utf-8"))
    digest.update(b"\0")
    digest.update(prompt_text.encode("utf-8"))
    digest.update(b"\0")
    digest.update(user_payload.encode("utf-8"))
    return digest.hexdigest()


def extract_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```json\s*(\{[\s\S]*\})\s*```", text, flags=re.IGNORECASE)
    if fenced:
        return json.loads(fenced.group(1))

    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
        return json.loads(text[brace_start:brace_end + 1])
    raise ValueError("Model response did not contain valid JSON")


def call_openrouter(
    api_key: str,
    model: str,
    prompt_text: str,
    user_payload: str,
    timeout: int,
    max_completion_tokens: int,
) -> tuple[dict[str, Any], str]:
    body = {
        "model": model,
        "temperature": 0,
        "max_tokens": max_completion_tokens,
        "messages": [
            {"role": "system", "content": prompt_text},
            {"role": "user", "content": user_payload},
        ],
    }
    req = request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-OpenRouter-Metadata": "enabled",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenRouter HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"OpenRouter request failed: {exc}") from exc

    message = payload["choices"][0]["message"]["content"]
    parsed = extract_json(message)
    return parsed, message


def load_cached(cache_path: Path) -> dict[str, Any] | None:
    if not cache_path.exists():
        return None
    return json.loads(cache_path.read_text(encoding="utf-8"))


def save_cache(cache_path: Path, bundle: SourceBundle, response_json: dict[str, Any], raw_message: str) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps(
            {
                "source_rel": bundle.source_rel,
                "response": response_json,
                "raw_message": raw_message,
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )


def normalize_issue(issue: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "severity": str(issue.get("severity", "low")).lower(),
        "category": str(issue.get("category", "other")),
        "title": str(issue.get("title", "")).strip() or "Untitled issue",
        "evidence_raw": str(issue.get("evidence_raw", "")).strip(),
        "evidence_csv": str(issue.get("evidence_csv", "")).strip(),
        "reason": str(issue.get("reason", "")).strip(),
        "likely_parser_bug": bool(issue.get("likely_parser_bug", False)),
        "likely_source_limitation": bool(issue.get("likely_source_limitation", False)),
        "recommended_action": str(issue.get("recommended_action", "")).strip(),
    }
    if normalized["severity"] not in {"low", "medium", "high"}:
        normalized["severity"] = "low"
    return normalized


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def render_markdown(
    model: str,
    prompt_file: Path,
    evaluations: list[tuple[AuditTask, dict[str, Any]]],
    failures: list[str],
) -> str:
    verdict_counts = Counter(str(result.get("verdict", "review")) for _, result in evaluations)
    severity_counts = Counter()
    for _, result in evaluations:
        for issue in result.get("issues", []):
            severity_counts[issue.get("severity", "low")] += 1

    lines = [
        "# OpenRouter Independent Data Audit",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Model: `{model}`",
        f"Prompt: `{display_path(prompt_file)}`",
        "",
        "## Summary",
        "",
        f"- Raw sources audited: {len(evaluations)}",
        f"- `pass` verdicts: {verdict_counts.get('pass', 0)}",
        f"- `review` verdicts: {verdict_counts.get('review', 0)}",
        f"- `fail` verdicts: {verdict_counts.get('fail', 0)}",
        f"- High-severity issues: {severity_counts.get('high', 0)}",
        f"- Medium-severity issues: {severity_counts.get('medium', 0)}",
        f"- Low-severity issues: {severity_counts.get('low', 0)}",
    ]

    if failures:
        lines.extend(
            [
                "",
                "## Request Failures",
                "",
                *[f"- {item}" for item in failures],
            ]
        )

    for task, result in evaluations:
        verdict = str(result.get("verdict", "review"))
        confidence = str(result.get("confidence", "medium"))
        summary = str(result.get("summary", "")).strip()
        issues = [normalize_issue(issue) for issue in result.get("issues", []) if isinstance(issue, dict)]
        matches = [str(item).strip() for item in result.get("notable_matches", []) if str(item).strip()]

        lines.extend(
            [
                "",
                f"## {task.label}",
                "",
                f"- Verdict: `{verdict}`",
                f"- Confidence: `{confidence}`",
                f"- Related CSVs: {', '.join(f'`{name}`' for name in task.csv_rows)}",
            ]
        )
        if task.class_names:
            lines.append(f"- Classes: {', '.join(f'`{name}`' for name in task.class_names)}")
        if summary:
            lines.append(f"- Summary: {summary}")

        lines.extend(["", "### Issues", ""])
        if not issues:
            lines.append("- None reported.")
        else:
            for issue in issues:
                lines.append(
                    f"- [{issue['severity']}] `{issue['category']}` {issue['title']} "
                    f"(parser_bug={str(issue['likely_parser_bug']).lower()}, "
                    f"source_limitation={str(issue['likely_source_limitation']).lower()})"
                )
                if issue["evidence_csv"]:
                    lines.append(f"  CSV: {issue['evidence_csv']}")
                if issue["evidence_raw"]:
                    lines.append(f"  Raw: {issue['evidence_raw']}")
                if issue["reason"]:
                    lines.append(f"  Why: {issue['reason']}")
                if issue["recommended_action"]:
                    lines.append(f"  Next: {issue['recommended_action']}")

        lines.extend(["", "### Notable Matches", ""])
        if matches:
            lines.extend(f"- {item}" for item in matches)
        else:
            lines.append("- None provided.")

    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an OpenRouter-backed independent data audit.")
    parser.add_argument("--model", help="OpenRouter model ID. Falls back to OPENROUTER_MODEL.")
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT, help="Markdown report path.")
    parser.add_argument("--prompt-file", type=Path, default=PROMPT_FILE, help="System prompt text file.")
    parser.add_argument("--source-filter", help="Only audit raw source paths containing this substring.")
    parser.add_argument("--max-sources", type=int, help="Only audit the first N matching raw sources.")
    parser.add_argument("--timeout", type=int, default=180, help="HTTP timeout in seconds.")
    parser.add_argument("--max-completion-tokens", type=int, default=4000, help="Cap completion size to preserve context room.")
    parser.add_argument("--no-cache", action="store_true", help="Ignore cached model responses.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_dotenv(ENV_FILE)

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Missing OPENROUTER_API_KEY. Put it in .env or export it in the environment.", file=sys.stderr)
        return 2

    model = args.model or os.environ.get("OPENROUTER_MODEL")
    if not model:
        print("Missing model. Pass --model or set OPENROUTER_MODEL in .env.", file=sys.stderr)
        return 2

    prompt_text = args.prompt_file.read_text(encoding="utf-8")
    bundles = collect_bundles()
    if args.source_filter:
        bundles = [bundle for bundle in bundles if args.source_filter in bundle.source_rel]
    if args.max_sources is not None:
        bundles = bundles[: args.max_sources]
    tasks: list[AuditTask] = []
    for bundle in bundles:
        tasks.extend(split_bundle(bundle))
    if not tasks:
        print("No matching raw sources found.", file=sys.stderr)
        return 1

    evaluations: list[tuple[AuditTask, dict[str, Any]]] = []
    failures: list[str] = []

    for index, task in enumerate(tasks, start=1):
        print(f"[{index}/{len(tasks)}] auditing {task.label}")
        user_payload = build_user_payload(task)
        key = cache_key(model, prompt_text, user_payload)
        cache_path = CACHE_DIR / f"{key}.json"

        cached = None if args.no_cache else load_cached(cache_path)
        if cached is not None:
            evaluations.append((task, cached["response"]))
            continue

        try:
            response_json, raw_message = call_openrouter(
                api_key,
                model,
                prompt_text,
                user_payload,
                args.timeout,
                args.max_completion_tokens,
            )
        except Exception as exc:
            failures.append(f"{task.label}: {exc}")
            continue

        save_cache(cache_path, SourceBundle(source_rel=task.source_rel, csv_rows=task.csv_rows), response_json, raw_message)
        evaluations.append((task, response_json))
        time.sleep(0.25)

    report = render_markdown(model, args.prompt_file, evaluations, failures)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote {display_path(args.output)}")
    return 0 if evaluations else 1


if __name__ == "__main__":
    raise SystemExit(main())
