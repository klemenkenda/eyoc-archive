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
from pathlib import Path

from flask import Flask, jsonify, request, render_template, send_from_directory, abort

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
RAW = RESULTS / "raw"

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "parsers"))
import locks  # noqa: E402
import common  # noqa: E402

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


@app.get("/api/country-codes")
def api_country_codes():
    return jsonify(sorted(common.CODES.items()))


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
