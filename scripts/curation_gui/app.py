"""Local-only data-curation GUI for the EYOC results archive.

Lets a curator, per year/discipline, see the original raw source file next to the
generated CSV, hand-edit the CSV, edit results/<year>/metadata.json, and lock a CSV so
`python scripts/parsers/run_all.py` (and name_cleanup's apply step) never overwrite it
again - see scripts/locks.py for how the lock is enforced.

Not part of www/ and never deployed - same "dev-only tooling" spirit as docker-compose.yml.

Run (from the repo root):
    python scripts/curation_gui/app.py
Then open http://127.0.0.1:5151
"""
import csv
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from flask import Flask, jsonify, request, render_template, send_from_directory, abort

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
RAW = RESULTS / "raw"

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "parsers"))
import locks  # noqa: E402
import common  # noqa: E402
import parse_xml  # noqa: E402
import parse_lazarus_html  # noqa: E402

DISCIPLINES = ("sprint", "long", "relay")
COLUMNS = {
    "sprint": common.SPRINT_COLUMNS,
    "long": common.SPRINT_COLUMNS,
    "relay": common.RELAY_COLUMNS,
}

app = Flask(__name__)


def _years():
    return sorted(int(p.name) for p in RESULTS.iterdir() if p.is_dir() and p.name.isdigit())


def _csv_path(year, discipline):
    return RESULTS / str(year) / f"{discipline}.csv"


def _read_csv(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _metadata_path(year):
    return RESULTS / str(year) / "metadata.json"


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/years")
def api_years():
    all_locks = locks.load()
    out = []
    for year in _years():
        disciplines = {}
        for d in DISCIPLINES:
            rows = _read_csv(_csv_path(year, d))
            disciplines[d] = {
                "hasCsv": _csv_path(year, d).exists(),
                "rowCount": len(rows),
                "locked": d in all_locks.get(str(year), []),
            }
        out.append({
            "year": year,
            "hasMetadata": _metadata_path(year).exists(),
            "disciplines": disciplines,
        })
    return jsonify(out)


@app.get("/api/year/<int:year>")
def api_year(year):
    if year not in _years():
        abort(404)

    meta_path = _metadata_path(year)
    metadata = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else None

    year_raw_dir = RAW / str(year)
    all_raw_files = sorted(
        str(p.relative_to(RAW).as_posix()) for p in year_raw_dir.rglob("*") if p.is_file()
    ) if year_raw_dir.is_dir() else []

    all_locks = locks.load()
    disciplines = {}
    for d in DISCIPLINES:
        rows = _read_csv(_csv_path(year, d))
        referenced = sorted({r["source_file"] for r in rows if r.get("source_file")})
        disciplines[d] = {
            "columns": COLUMNS[d],
            "rows": rows,
            "locked": d in all_locks.get(str(year), []),
            "referencedRawFiles": referenced,
        }

    return jsonify({
        "year": year,
        "metadata": metadata,
        "rawFiles": all_raw_files,
        "disciplines": disciplines,
    })


@app.get("/api/raw/<path:relpath>")
def api_raw(relpath):
    return send_from_directory(RAW, relpath)


RAW_INDIVIDUAL_COLUMNS = ["class", "rank", "status", "bib", "country", "name", "time"]
RAW_RELAY_COLUMNS = [
    "class", "rank", "status", "country", "team", "total_time",
    "leg1_name", "leg1_time", "leg2_name", "leg2_time", "leg3_name", "leg3_time",
]


def _raw_class_name(class_result_el):
    """Whatever class label the source itself uses - not run through common.normalize_class."""
    ec = class_result_el.find("EventClass")
    if ec is not None:
        return parse_xml.text_of(ec, "ClassShortName") or parse_xml.text_of(ec, "Name") or ""
    cls = class_result_el.find("Class")
    if cls is not None:
        return parse_xml.text_of(cls, "Name") or ""
    return ""


def _raw_status(result_el):
    status_el = result_el.find("CompetitorStatus") if result_el is not None else None
    if status_el is None and result_el is not None:
        status_el = result_el.find("TeamStatus")
    if status_el is not None:
        return status_el.get("value") or (status_el.text or "").strip()
    return (parse_xml.text_of(result_el, "Status") if result_el is not None else None) or ""


def _raw_country(person_el, org_el):
    """First country code/name found in the source, verbatim - no alias resolution."""
    nat = person_el.find("Nationality") if person_el is not None else None
    if nat is not None:
        if nat.get("code"):
            return nat.get("code")
        alpha3 = nat.find("Country/Alpha3")
        if alpha3 is not None and alpha3.get("value"):
            return alpha3.get("value")
        if nat.text and nat.text.strip():
            return nat.text.strip()
    if org_el is not None:
        country_el = org_el.find("Country")
        if country_el is not None:
            if country_el.get("code"):
                return country_el.get("code")
            alpha3 = country_el.find("Alpha3")
            if alpha3 is not None and alpha3.get("value"):
                return alpha3.get("value")
            if country_el.text and country_el.text.strip():
                return country_el.text.strip()
        name_el = org_el.find("Name")
        if name_el is not None and name_el.text:
            return name_el.text.strip()
    return ""


def raw_individual_rows(root):
    rows = []
    for cr in root.findall(".//ClassResult"):
        klass = _raw_class_name(cr)
        for pr in cr.findall("PersonResult"):
            person = pr.find("Person")
            org = pr.find("Organisation")
            result = pr.find("Result")
            if result is None:
                continue
            family = (parse_xml.text_of(person, "PersonName/Family") or parse_xml.text_of(person, "Name/Family")) if person is not None else None
            given = (parse_xml.text_of(person, "PersonName/Given") or parse_xml.text_of(person, "Name/Given")) if person is not None else None
            name = f"{given or ''} {family or ''}".strip()
            rows.append({
                "class": klass,
                "rank": parse_xml.text_of(result, "ResultPosition") or parse_xml.text_of(result, "Position") or "",
                "status": _raw_status(result),
                "bib": parse_xml.text_of(result, "BibNumber") or "",
                "country": _raw_country(person, org),
                "name": name,
                "time": parse_xml.text_of(result, "Time") or "",
            })
    return rows


def raw_relay_rows(root):
    rows = []
    for cr in root.findall(".//ClassResult"):
        klass = _raw_class_name(cr)
        for tr in cr.findall("TeamResult"):
            org = tr.find("Organisation")
            team_name_el = tr.find("Name")
            team_name_alt = tr.find("TeamName")
            team_label = (team_name_el.text if team_name_el is not None and team_name_el.text else None) or \
                         (team_name_alt.text if team_name_alt is not None and team_name_alt.text else None) or ""
            country = _raw_country(None, org)

            members = []
            for tmr in tr.findall("TeamMemberResult"):
                leg_no_text = parse_xml.text_of(tmr, "Leg") or parse_xml.text_of(tmr, "Result/Leg")
                leg_no = int(leg_no_text) if leg_no_text and leg_no_text.isdigit() else len(members) + 1
                p = tmr.find("Person")
                family = parse_xml.text_of(p, "Name/Family") if p is not None else None
                given = parse_xml.text_of(p, "Name/Given") if p is not None else None
                runner_name = f"{given or ''} {family or ''}".strip()
                if not runner_name and p is not None:
                    runner_name = parse_xml.text_of(p, "Name") or ""
                result = tmr.find("Result")
                leg_time = (parse_xml.text_of(result, "Time") or "") if result is not None else ""
                members.append((leg_no, runner_name, leg_time))
            members.sort(key=lambda m: m[0])

            total_time = parse_xml.text_of(tr, "Time")
            rank = ""
            status_text = _raw_status(tr)

            if total_time is None:
                # flavour C: the source itself only records the team total on the last
                # leg's cumulative OverallResult - same place, just following the pointer.
                last_tmr, last_leg = None, -1
                for tmr in tr.findall("TeamMemberResult"):
                    leg_no_text = parse_xml.text_of(tmr, "Leg") or parse_xml.text_of(tmr, "Result/Leg")
                    leg_no = int(leg_no_text) if leg_no_text and leg_no_text.isdigit() else -1
                    if leg_no > last_leg:
                        last_leg, last_tmr = leg_no, tmr
                if last_tmr is not None:
                    overall = last_tmr.find("Result/OverallResult")
                    if overall is not None:
                        total_time = parse_xml.text_of(overall, "Time")
                        rank = parse_xml.text_of(overall, "Position") or ""
                        if not status_text:
                            status_text = parse_xml.text_of(overall, "Status") or ""

            row = {
                "class": klass, "rank": rank, "status": status_text,
                "country": country, "team": team_label, "total_time": total_time or "",
            }
            for i in range(3):
                leg = members[i] if i < len(members) else (None, "", "")
                row[f"leg{i+1}_name"] = leg[1]
                row[f"leg{i+1}_time"] = leg[2]
            rows.append(row)
    return rows


@app.get("/api/raw-xml/<path:relpath>")
def api_raw_xml(relpath):
    """Show an IOF-XML/Eventor raw source as a table - literal field values as they
    appear in the source (no country/class/status normalization, no dropping of
    non-European entries, no synthesized fields), just laid out instead of as a wall
    of angle brackets."""
    path = (RAW / relpath).resolve()
    if RAW.resolve() not in path.parents or path.suffix.lower() != ".xml" or not path.exists():
        abort(404)
    try:
        root = parse_xml.strip_ns(ET.parse(path).getroot())
    except ET.ParseError as e:
        return jsonify({"error": f"Could not parse this file as XML: {e}"}), 400

    is_relay = root.find(".//TeamResult") is not None
    if is_relay:
        rows = raw_relay_rows(root)
        columns = RAW_RELAY_COLUMNS
    else:
        rows = raw_individual_rows(root)
        columns = RAW_INDIVIDUAL_COLUMNS

    if not rows:
        return jsonify({"error": "No ClassResult/PersonResult/TeamResult rows recognised in this file."}), 400

    return jsonify({"columns": columns, "rows": rows})


RAW_LAZARUS_COLUMNS = ["discipline", "class", "rank", "status", "country", "name", "time"]


def raw_lazarus_rows(path, year):
    """Same line-parsing heuristics as parse_lazarus_html.parse_year() - unavoidable
    for this free-text format, since there's no tag boundary between name/country/time
    to key off of - but literal country/status/class text instead of the normalized
    CSV values, and nothing dropped for being unrecognised. Bib is never present in
    this source; `discipline` is included because one page covers both sprint and long."""
    doc = parse_lazarus_html.read_html(path)
    sections = [
        (m.start(), parse_lazarus_html.strip_tags_and_unescape(m.group(1)).strip())
        for m in parse_lazarus_html.SECTION_RE.finditer(doc)
    ]
    headers = [(m.start(), m.end(), m.group(1)) for m in parse_lazarus_html.HEADER_RE.finditer(doc)]

    rows = []
    for i, (h_start, h_end, raw_class) in enumerate(headers):
        if not common.normalize_class(raw_class):
            continue  # not actually a class header (structural check, same as the pipeline)
        section_name = "?"
        for s_idx, s_name in sections:
            if s_idx < h_start:
                section_name = s_name
        discipline = parse_lazarus_html.discipline_for_section(section_name)
        if not discipline:
            continue
        chunk_end = headers[i + 1][0] if i + 1 < len(headers) else len(doc)
        chunk = parse_lazarus_html.strip_tags_and_unescape(doc[h_end:chunk_end])
        for line in chunk.splitlines():
            parsed = parse_lazarus_html.parse_row(line)
            if not parsed:
                continue
            rank, name, country_text, time_text, status_word = parsed
            if year in parse_lazarus_html.FORCE_SURNAME_FIRST_YEARS:
                words = name.split(" ")
                if len(words) >= 2:
                    name = " ".join([words[-1]] + words[:-1])
            rows.append({
                "discipline": discipline,
                "class": raw_class,
                "rank": rank if rank is not None else "",
                "status": status_word or "",
                "country": country_text or "",
                "name": name,
                "time": time_text or "",
            })
    return rows


@app.get("/api/raw-lazarus/<path:relpath>")
def api_raw_lazarus(relpath):
    """Show a lazarus.elte.hu combined results page (2002-2013, see PARSERS.md) as a
    table - literal values as segmented by the source's own line-parsing heuristics,
    not normalized and nothing dropped for being unresolved."""
    path = (RAW / relpath).resolve()
    if RAW.resolve() not in path.parents or not path.exists():
        abort(404)
    try:
        year = int(path.parent.name)
    except ValueError:
        abort(404)

    try:
        rows = raw_lazarus_rows(path, year)
    except Exception as e:  # noqa: BLE001 - surfaced to the curator, not a crash
        return jsonify({"error": f"Could not parse this file: {e}"}), 400

    if not rows:
        return jsonify({"error": "No class/result rows recognised in this file."}), 400

    return jsonify({"columns": RAW_LAZARUS_COLUMNS, "rows": rows})


@app.get("/api/country-codes")
def api_country_codes():
    return jsonify(sorted(common.CODES.items()))


@app.get("/api/country-aliases")
def api_country_aliases():
    """Lowercase name/code -> canonical EYOC code, so the GUI can flag non-EYOC
    countries client-side the same way common.normalize_country resolves them."""
    return jsonify(common.ALIASES)


@app.post("/api/year/<int:year>/<discipline>/csv")
def api_save_csv(year, discipline):
    if discipline not in DISCIPLINES:
        abort(404)
    body = request.get_json(force=True)
    rows = body.get("rows", [])
    columns = COLUMNS[discipline]

    path = _csv_path(year, discipline)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        for r in rows:
            w.writerow({c: (r.get(c) or "") for c in columns})

    return jsonify({"ok": True, "rowCount": len(rows)})


@app.post("/api/year/<int:year>/<discipline>/lock")
def api_set_lock(year, discipline):
    if discipline not in DISCIPLINES:
        abort(404)
    body = request.get_json(force=True)
    locked = bool(body.get("locked"))
    locks.set_locked(year, discipline, locked)
    return jsonify({"ok": True, "locked": locked})


@app.post("/api/year/<int:year>/metadata")
def api_save_metadata(year):
    body = request.get_json(force=True)
    path = _metadata_path(year)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, indent=2, ensure_ascii=False), encoding="utf-8")
    return jsonify({"ok": True})


@app.post("/api/rebuild")
def api_rebuild():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "parsers" / "run_all.py")],
        cwd=ROOT, capture_output=True, text=True, timeout=900,
    )
    return jsonify({
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5151, debug=True)
