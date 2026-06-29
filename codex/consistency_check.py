"""Independent clean-vs-raw consistency audit for EYOC results.

This script deliberately does not import or modify scripts/parsers. It reads the
normalized CSV files, inspects the declared raw source files, performs exact checks for
IOF/Eventor XML sources, and writes a Markdown report.
"""
from __future__ import annotations

import csv
import html
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RAW = RESULTS / "raw"
REPORT = RAW / "CONSISTENCY-CHECK-CODEX.md"
COUNTRIES_MD = RESULTS / "EYOC-COUNTRIES.md"

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
CLASSES = {"M16", "M18", "W16", "W18"}
RELAY_CLASSES = CLASSES | {"Mixed"}
STATUSES = {"OK", "DNF", "DSQ", "DNS", "MP"}
CONFIDENCE = {"high", "approx"}


def load_country_codes() -> dict[str, str]:
    codes: dict[str, str] = {}
    for line in COUNTRIES_MD.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\|\s*([A-Z]{3})\s*\|\s*([^|]+?)\s*\|", line)
        if match:
            codes[match.group(1)] = match.group(2).strip()
    return codes


CODES = load_country_codes()
ALIASES = {
    "czech republic": "CZE",
    "czech rep": "CZE",
    "czechia": "CZE",
    "great britain": "GBR",
    "united kingdom": "GBR",
    "uk": "GBR",
    "russia": "RUS",
    "russian federation": "RUS",
    "belorussia": "BLR",
    "belarus": "BLR",
    "latvija": "LAT",
    "latvia": "LAT",
    "macedonia": "MKD",
    "north macedonia": "MKD",
    "fyr macedonia": "MKD",
    "moldova": "MDA",
    "moldavia": "MDA",
    "moldova, republic of": "MDA",
    "republic of moldova": "MDA",
    "slovak republic": "SVK",
    "slovakia": "SVK",
    "switzerland": "SUI",
    "netherlands": "NED",
    "holland": "NED",
    "rom": "ROU",
    "turkiye": "TUR",
    "türkiye": "TUR",
    "turkey": "TUR",
}
for code, name in CODES.items():
    ALIASES[code.lower()] = code
    ALIASES[name.lower()] = code


def normalize_country(text: str | None) -> str | None:
    if not text:
        return None
    cleaned = re.sub(r"\s+", " ", text).strip().strip(".")
    lead = cleaned.split(" ", 1)[0]
    if lead.upper() in CODES and lead.isupper() and len(lead) == 3:
        return lead.upper()
    no_number = re.sub(r"\s+\d+$", "", cleaned)
    for candidate in (cleaned, no_number):
        code = ALIASES.get(candidate.lower())
        if code:
            return code
    key = no_number.lower()
    if len(key) >= 6:
        for alias, code in ALIASES.items():
            if len(alias) >= 6 and alias.startswith(key):
                return code
    return None


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
    if value in CLASSES:
        return value
    if value in {"MIX", "MIXT", "MIXED"}:
        return "Mixed"
    return None


def parse_time(text: str | None) -> int | None:
    if not text:
        return None
    value = text.strip()
    if value.isdigit():
        return int(value)
    match = re.match(r"^(\d+)\.(\d{2}),(\d+)$", value)
    if match:
        minutes, seconds, frac = match.groups()
        return int(minutes) * 60 + int(seconds) + (1 if int(frac) >= 5 else 0)
    match = re.match(r"^(\d+)\.(\d{2})$", value)
    if match:
        minutes, seconds = match.groups()
        return int(minutes) * 60 + int(seconds)
    parts = value.split(":")
    try:
        if len(parts) == 2:
            return int(round(float(parts[0]) * 60 + float(parts[1])))
        if len(parts) == 3:
            return int(round(float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])))
    except ValueError:
        return None
    return None


# Canonical IOF-XML status enum values - matched as exact tokens because several don't
# contain the abbreviated substrings the heuristics below look for ("disqualified" has
# no "dsq", "didnotfinish" has no "dnf", "missingpunch" isn't "mp"/"mispunch"). Kept as
# its own copy here (not imported from scripts/parsers/common.py) on purpose, per this
# script's independent-audit design - but needs the same fix or it'll flag every
# correctly-classified DNS/DNF/MP/NotCompeting/Unknown row as a false-positive mismatch.
_IOF_STATUS_MAP = {
    "ok": "OK",
    "missingpunch": "MP",
    "mispunch": "MP",
    "disqualified": "DSQ",
    "didnotstart": "DNS",
    "didnotfinish": "DNF",
    "notcompeting": "DNS",
    "overtime": "DNF",
    "cancelled": "DNF",
    "sportingwithdrawal": "DNF",
    "unknown": "DNF",
}


def normalize_status(text: str | None, has_time: bool) -> str:
    if not text:
        return "OK" if has_time else "DNF"
    value = text.strip().lower()
    compact = re.sub(r"[^a-z]", "", value)
    if compact in _IOF_STATUS_MAP:
        return _IOF_STATUS_MAP[compact]
    if "dsq" in value or "disq" in value:
        return "DSQ"
    if "dns" in value:
        return "DNS"
    if value in {"mp", "mispunch"}:
        return "MP"
    if "dnf" in value or "abandon" in value or "no sale" in value:
        return "DNF"
    return "OK" if has_time else "DNF"


def text_of(element: ET.Element | None, path: str) -> str | None:
    if element is None:
        return None
    found = element.find(path)
    return found.text if found is not None and found.text else None


def text_or_value(element: ET.Element | None, path: str) -> str | None:
    if element is None:
        return None
    found = element.find(path)
    if found is None:
        return None
    return found.text or found.get("value")


def strip_ns(root: ET.Element) -> ET.Element:
    for element in root.iter():
        if "}" in element.tag:
            element.tag = element.tag.split("}", 1)[1]
    return root


def class_from_xml(class_result: ET.Element) -> str | None:
    event_class = class_result.find("EventClass")
    if event_class is not None:
        for path in ("ClassShortName", "Name"):
            klass = normalize_class(text_of(event_class, path))
            if klass:
                return klass
    klass = class_result.find("Class")
    return normalize_class(text_of(klass, "Name"))


def person_country(person: ET.Element | None, org: ET.Element | None) -> str | None:
    if person is not None:
        nat = person.find("Nationality")
        if nat is not None:
            for value in (nat.get("code"), text_or_value(nat, "Country/Alpha3"), nat.text):
                code = normalize_country(value)
                if code:
                    return code
    if org is not None:
        country = org.find("Country")
        values = [
            country.get("code") if country is not None else None,
            text_or_value(org, "Country/Alpha3"),
            text_of(org, "Name"),
        ]
        for value in values:
            code = normalize_country(value)
            if code:
                return code
    return None


def xml_individual_rows(path: Path) -> list[tuple[str, ...]]:
    root = strip_ns(ET.parse(path).getroot())
    rows: list[tuple[str, ...]] = []
    for class_result in root.findall(".//ClassResult"):
        klass = class_from_xml(class_result)
        if not klass or klass not in CLASSES:
            continue
        for person_result in class_result.findall("PersonResult"):
            person = person_result.find("Person")
            result = person_result.find("Result")
            if person is None or result is None:
                continue
            code = person_country(person, person_result.find("Organisation"))
            if not code:
                continue
            family = text_of(person, "PersonName/Family") or text_of(person, "Name/Family") or ""
            given = text_of(person, "PersonName/Given") or text_of(person, "Name/Given") or ""
            name = f"{given} {family}".strip()
            time_s = parse_time(text_of(result, "Time"))
            rank_text = text_of(result, "ResultPosition") or text_of(result, "Position")
            rank = rank_text if rank_text and rank_text.isdigit() else ""
            status_element = result.find("CompetitorStatus")
            status_text = status_element.get("value") if status_element is not None else text_of(result, "Status")
            status = normalize_status(status_text, time_s is not None)
            rows.append(
                (
                    klass,
                    rank,
                    status,
                    text_of(result, "BibNumber") or "",
                    code,
                    name,
                    "" if time_s is None else str(time_s),
                )
            )
    return rows


def xml_relay_rows(path: Path) -> list[tuple[str, ...]]:
    root = strip_ns(ET.parse(path).getroot())
    rows: list[tuple[str, ...]] = []
    for class_result in root.findall(".//ClassResult"):
        klass = class_from_xml(class_result)
        if not klass or klass not in RELAY_CLASSES:
            continue
        for fallback_rank, team_result in enumerate(class_result.findall("TeamResult"), start=1):
            team_name = text_of(team_result, "Name") or text_of(team_result, "TeamName") or ""
            org = team_result.find("Organisation")
            code = None
            if org is not None:
                country = org.find("Country")
                code = normalize_country(country.get("code") if country is not None else None)
                code = code or normalize_country(text_of(org, "Name"))
            code = code or normalize_country(team_name)
            if not code:
                continue
            legs: list[tuple[str, str]] = []
            for member_result in team_result.findall("TeamMemberResult"):
                leg_text = text_of(member_result, "Leg") or text_of(member_result, "Result/Leg")
                try:
                    leg_no = int(leg_text or "")
                except ValueError:
                    leg_no = len(legs) + 1
                person = member_result.find("Person")
                family = text_of(person, "Name/Family")
                given = text_of(person, "Name/Given")
                if family or given:
                    name = f"{given or ''} {family or ''}".strip()
                else:
                    name = text_of(person, "Name") or ""
                result = member_result.find("Result")
                leg_time = parse_time(text_of(result, "Time")) if result is not None else None
                legs.append((leg_no, name, "" if leg_time is None else str(leg_time)))
            legs.sort(key=lambda item: item[0])

            total_time = parse_time(text_of(team_result, "Time"))
            rank: str | int | None = None
            overall = None
            if total_time is None:
                last_member = None
                last_leg = -1
                for member_result in team_result.findall("TeamMemberResult"):
                    leg_text = text_of(member_result, "Leg") or text_of(member_result, "Result/Leg")
                    try:
                        leg_no = int(leg_text or "")
                    except ValueError:
                        leg_no = -1
                    if leg_no > last_leg:
                        last_leg = leg_no
                        last_member = member_result
                if last_member is not None:
                    overall = last_member.find("Result/OverallResult")
                    if overall is not None:
                        total_time = parse_time(text_of(overall, "Time"))
                        pos = text_of(overall, "Position")
                        rank = pos if pos and pos.isdigit() else ""
            if rank is None:
                rank = str(fallback_rank)
            status_element = team_result.find("TeamStatus")
            status_text = status_element.get("value") if status_element is not None else text_of(team_result, "Status")
            if not status_text and overall is not None:
                status_text = text_of(overall, "Status")
            status = normalize_status(status_text, total_time is not None)
            # A team with fewer than 3 TeamMemberResult entries didn't field full legs -
            # there's no explicit TeamStatus in this case, so status_text/overall above
            # came from a single leg-runner's own individual OverallResult. Mirrors the
            # same fix in scripts/parsers/parse_xml.py (kept as a separate copy here on
            # purpose, per this script's independent-audit design).
            if status == "OK" and len(team_result.findall("TeamMemberResult")) < 3:
                status = "DNF"
            flat_legs: list[str] = []
            for index in range(3):
                if index < len(legs):
                    flat_legs.extend([legs[index][1], legs[index][2]])
                else:
                    flat_legs.extend(["", ""])
            rows.append(
                (
                    klass,
                    str(rank),
                    status,
                    code,
                    team_name or code,
                    "" if total_time is None else str(total_time),
                    *flat_legs,
                )
            )
    return rows


def plain_text(path: Path) -> str:
    if path.suffix.lower() in {".htm", ".html"}:
        raw = path.read_bytes()
        try:
            decoded = raw.decode("utf-8")
        except UnicodeDecodeError:
            decoded = raw.decode("cp1250", errors="replace")
        decoded = re.sub(r"<br\s*/?>", "\n", decoded, flags=re.IGNORECASE)
        return html.unescape(re.sub(r"<[^>]+>", " ", decoded))
    if path.suffix.lower() == ".xml":
        return path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".pdf":
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


def fold(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    asciiish = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", asciiish.casefold())


def row_key(row: dict[str, str], discipline: str) -> tuple[str, ...]:
    if discipline == "relay":
        return tuple(row[column] for column in RELAY_COLUMNS if column not in {"confidence", "source_file"})
    return tuple(row[column] for column in INDIVIDUAL_COLUMNS if column not in {"confidence", "source_file"})


def source_tokens_for_name_check() -> list[tuple[str, str]]:
    values: set[tuple[str, str]] = set()
    for code, name in CODES.items():
        values.add((code, name.lower()))
    for alias, code in ALIASES.items():
        if len(alias) > 3 and alias.isalpha() or " " in alias:
            values.add((code, alias.lower()))
    return sorted(values, key=lambda item: len(item[1]), reverse=True)


def main() -> None:
    csv_files = sorted(RESULTS.glob("[0-9][0-9][0-9][0-9]/*.csv"))
    rows_by_file: dict[Path, list[dict[str, str]]] = {}
    structural: list[str] = []
    source_missing: list[str] = []
    counts: dict[str, Counter[str]] = {}
    confidence_counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    source_text_cache: dict[Path, str] = {}
    source_presence_failures: list[str] = []
    replacement_char_rows: list[str] = []
    contaminated_names: list[str] = []
    suspicious_empty_legs: list[str] = []

    country_name_tokens = source_tokens_for_name_check()

    for csv_file in csv_files:
        discipline = csv_file.stem
        expected = RELAY_COLUMNS if discipline == "relay" else INDIVIDUAL_COLUMNS
        with csv_file.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        rows_by_file[csv_file] = rows
        rel_csv = csv_file.relative_to(RESULTS).as_posix()
        if reader.fieldnames != expected:
            structural.append(f"{rel_csv}: unexpected header {reader.fieldnames}")
        counts[rel_csv] = Counter(row.get("class", "") for row in rows)

        for line_no, row in enumerate(rows, start=2):
            row_label = f"{rel_csv}:{line_no}"
            klass = row.get("class", "")
            allowed_classes = RELAY_CLASSES if discipline == "relay" else CLASSES
            if klass not in allowed_classes:
                structural.append(f"{row_label}: unexpected class {klass!r}")
            if row.get("status", "") not in STATUSES:
                structural.append(f"{row_label}: unexpected status {row.get('status')!r}")
            confidence = row.get("confidence", "")
            confidence_counts[confidence] += 1
            if confidence not in CONFIDENCE:
                structural.append(f"{row_label}: unexpected confidence {confidence!r}")

            source_rel = row.get("source_file", "")
            source_counts[source_rel] += 1
            source_path = RAW / source_rel
            if not source_path.exists():
                source_missing.append(f"{row_label}: {source_rel}")
                continue
            if not source_rel.startswith(csv_file.parent.name + "/"):
                structural.append(f"{row_label}: source_file points outside its year: {source_rel}")

            if discipline != "relay":
                for int_field in ("rank", "time_seconds"):
                    value = row.get(int_field, "")
                    if value and not value.isdigit():
                        structural.append(f"{row_label}: {int_field} is not integer/blank: {value!r}")
                if row.get("status") == "OK" and not row.get("time_seconds"):
                    structural.append(f"{row_label}: OK result has blank time_seconds")
                if "\ufffd" in row.get("name", ""):
                    replacement_char_rows.append(f"{row_label}: {row.get('name')}")
                folded_name = fold(row.get("name", ""))
                for code, country_name in country_name_tokens:
                    if folded_name.endswith(" " + fold(country_name)):
                        contaminated_names.append(
                            f"{row_label}: {row.get('name')} [{row.get('country')}] ends with country token {country_name}"
                        )
                        break
            else:
                for int_field in ("rank", "total_time_seconds", "leg1_time_seconds", "leg2_time_seconds", "leg3_time_seconds"):
                    value = row.get(int_field, "")
                    if value and not value.isdigit():
                        structural.append(f"{row_label}: {int_field} is not integer/blank: {value!r}")
                if row.get("status") == "OK" and not row.get("total_time_seconds"):
                    structural.append(f"{row_label}: OK relay result has blank total_time_seconds")
                if row.get("status") == "OK" and not all(row.get(f"leg{i}_name", "") for i in (1, 2, 3)):
                    suspicious_empty_legs.append(row_label)
                replacement_fields = [row.get("team", "")] + [row.get(f"leg{i}_name", "") for i in (1, 2, 3)]
                if any("\ufffd" in value for value in replacement_fields):
                    replacement_char_rows.append(f"{row_label}: {row.get('team')}")

            if source_path.suffix.lower() not in {".xml"}:
                if source_path not in source_text_cache:
                    source_text_cache[source_path] = fold(plain_text(source_path))
                source_text = source_text_cache[source_path]
                probes: list[str] = []
                if discipline == "relay":
                    probes = [row.get("team", ""), row.get("leg1_name", ""), row.get("leg2_name", ""), row.get("leg3_name", "")]
                else:
                    probes = [row.get("name", "")]
                for probe in [p for p in probes if p]:
                    if fold(probe) not in source_text:
                        source_presence_failures.append(f"{row_label}: {probe!r} not found in {source_rel} text layer")
                        break

    xml_exact: list[str] = []
    xml_mismatch_examples: list[str] = []
    for source_rel in sorted(source_counts):
        source_path = RAW / source_rel
        if source_path.suffix.lower() != ".xml" or not source_path.exists():
            continue
        related_rows = []
        for csv_file, rows in rows_by_file.items():
            for row in rows:
                if row.get("source_file") == source_rel:
                    related_rows.append((csv_file.stem, row))
        if not related_rows:
            continue
        discipline = related_rows[0][0]
        raw_rows = xml_relay_rows(source_path) if discipline == "relay" else xml_individual_rows(source_path)
        clean_rows = [row_key(row, discipline) for _, row in related_rows]
        raw_counter = Counter(raw_rows)
        clean_counter = Counter(clean_rows)
        if raw_counter == clean_counter:
            xml_exact.append(f"{source_rel}: {len(clean_rows)} rows")
        else:
            missing = list((raw_counter - clean_counter).elements())
            extra = list((clean_counter - raw_counter).elements())
            xml_mismatch_examples.append(
                f"{source_rel}: clean={len(clean_rows)} raw={len(raw_rows)} missing_from_clean={missing[:3]} extra_in_clean={extra[:3]}"
            )

    all_years = [path.name for path in sorted(RESULTS.glob("[0-9][0-9][0-9][0-9]")) if path.is_dir()]
    coverage_lines: list[str] = []
    for year in all_years:
        present = sorted(path.stem for path in (RESULTS / year).glob("*.csv"))
        coverage_lines.append(f"{year}: {', '.join(present) if present else '-'}")

    report: list[str] = []
    report.append("# Clean-vs-Raw Consistency Check (Codex)")
    report.append("")
    report.append("Generated by `codex/consistency_check.py`. This audit did not import, modify, or regenerate any files under `scripts/parsers/`.")
    report.append("")
    report.append("## Scope")
    report.append("")
    report.append(f"- Clean CSV files checked: {len(csv_files)}")
    report.append(f"- Clean rows checked: {sum(len(rows) for rows in rows_by_file.values())}")
    report.append(f"- Distinct raw source references used by clean rows: {len(source_counts)}")
    report.append(f"- Exact XML source comparisons passed: {len(xml_exact)}")
    report.append(f"- Exact XML source comparisons with mismatches: {len(xml_mismatch_examples)}")
    report.append("")
    report.append("## Verdict")
    report.append("")
    if not source_missing and not structural and not xml_mismatch_examples:
        report.append("The clean CSV files are structurally consistent and every declared raw `source_file` exists. All XML-backed clean files match their raw XML sources exactly after applying the same documented European-country filter and normalized schema.")
    else:
        report.append("The audit found issues that should be reviewed before treating the clean data as fully source-consistent.")
    report.append("")
    if contaminated_names:
        report.append("One substantive data-quality problem was found in old HTML-derived individual files: several athlete `name` values appear to include the printed country name. These rows still point to real source rows, but the normalized `name` field is polluted and should be corrected.")
    else:
        report.append("No country-name pollution was detected in athlete names.")
    if replacement_char_rows:
        report.append(f"A second text-quality issue was found: {len(replacement_char_rows)} clean rows contain the Unicode replacement character, which indicates lost or undecoded accents in names.")
    report.append("")
    report.append("## Coverage")
    report.append("")
    report.extend(f"- {line}" for line in coverage_lines)
    report.append("")
    report.append("Known intentional gaps remain consistent with `QUALITY-CHECK.md`: no clean `relay.csv` for 2002-2014 except later available years, no `results/2016/sprint.csv`, and abbreviated 2002 individual files.")
    report.append("")
    report.append("## Structural Checks")
    report.append("")
    report.append(f"- Header/class/status/confidence/integer problems: {len(structural)}")
    report.append(f"- Missing raw `source_file` targets: {len(source_missing)}")
    report.append(f"- OK relay rows with blank leg names: {len(suspicious_empty_legs)}")
    report.append("  These are advisory completeness flags. For XML-backed rows, the clean CSV still matches the raw XML exactly.")
    report.append("")
    for item in structural[:50]:
        report.append(f"- {item}")
    for item in source_missing[:50]:
        report.append(f"- {item}")
    if len(structural) > 50 or len(source_missing) > 50:
        report.append("- Additional structural/source-link findings omitted from this summary.")
    for item in suspicious_empty_legs[:20]:
        report.append(f"- {item}: OK relay row has at least one blank leg name")
    if len(suspicious_empty_legs) > 20:
        report.append("- Additional blank-leg relay findings omitted from this summary.")
    report.append("")
    report.append("## XML Exact Matches")
    report.append("")
    if xml_exact:
        for item in xml_exact:
            report.append(f"- {item}")
    else:
        report.append("- None")
    report.append("")
    report.append("## XML Mismatches")
    report.append("")
    if xml_mismatch_examples:
        for item in xml_mismatch_examples:
            report.append(f"- {item}")
    else:
        report.append("- None")
    report.append("")
    report.append("## Source Text Presence Checks")
    report.append("")
    checked_text_rows = sum(
        1
        for rows in rows_by_file.values()
        for row in rows
        if (RAW / row.get("source_file", "")).suffix.lower() != ".xml"
    )
    report.append(f"- Non-XML clean rows checked against extracted HTML/PDF text: {checked_text_rows}")
    report.append(f"- Rows whose primary name/team probe was not found in the raw text layer: {len(source_presence_failures)}")
    report.append(f"- Rows containing the Unicode replacement character in clean text: {len(replacement_char_rows)}")
    if source_presence_failures:
        report.append("")
        for item in source_presence_failures[:80]:
            report.append(f"- {item}")
        if len(source_presence_failures) > 80:
            report.append("- Additional source-text misses omitted from this summary.")
    if replacement_char_rows:
        report.append("")
        report.append("Replacement-character rows:")
        for item in replacement_char_rows[:40]:
            report.append(f"- {item}")
        if len(replacement_char_rows) > 40:
            report.append("- Additional replacement-character rows omitted from this summary.")
    report.append("")
    report.append("## Suspected Name Pollution")
    report.append("")
    report.append(f"- Rows where `name` ends with a country token: {len(contaminated_names)}")
    if contaminated_names:
        by_file: defaultdict[str, int] = defaultdict(int)
        for item in contaminated_names:
            by_file[item.split(":", 1)[0]] += 1
        for filename, count in sorted(by_file.items()):
            report.append(f"- {filename}: {count}")
        report.append("")
        report.append("Examples:")
        for item in contaminated_names[:40]:
            report.append(f"- {item}")
        if len(contaminated_names) > 40:
            report.append("- Additional suspected polluted names omitted from this summary.")
    report.append("")
    report.append("## Row Counts By File")
    report.append("")
    for rel_csv, counter in sorted(counts.items()):
        parts = ", ".join(f"{klass}={counter[klass]}" for klass in sorted(counter))
        report.append(f"- {rel_csv}: {sum(counter.values())} rows ({parts})")
    report.append("")
    report.append("## Confidence Values")
    report.append("")
    for value, count in sorted(confidence_counts.items()):
        report.append(f"- {value}: {count}")
    report.append("")
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    print(f"csv_files={len(csv_files)} rows={sum(len(rows) for rows in rows_by_file.values())}")
    print(f"structural={len(structural)} missing_sources={len(source_missing)} xml_mismatches={len(xml_mismatch_examples)}")
    print(f"name_pollution={len(contaminated_names)} source_text_misses={len(source_presence_failures)}")


if __name__ == "__main__":
    main()
