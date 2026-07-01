"""Build the static JSON dataset + logo assets consumed by the www/ webapp.

Reads results/<year>/{sprint,long,relay}.csv + metadata.json (the output of
scripts/parsers/run_all.py) and logos/png/eyoc-<year>.png, and writes:

  www/data/individual.json  every sprint/long row, all years, flattened
  www/data/relay.json       every relay row, all years, flattened
  www/data/events.json      per-year event metadata, keyed by year
  www/data/manifest.json    build timestamp + content hash, for cache-busting
  www/assets/logos/*.png    copy of logos/png/*.png

Safe to re-run any time - it's a pure function of results/ and logos/png/, nothing
downstream is hand-edited. Run after scripts/parsers/run_all.py whenever results/ changes,
and after scripts/name_cleanup/find_name_corrections.py apply if there are pending
competitor-name corrections (see scripts/name_cleanup/README.md) - this reads results/
directly, so running it first would ship uncorrected names.
"""
import csv
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
LOGOS_SRC = ROOT / "logos" / "png"
WWW_DATA = ROOT / "www" / "data"
WWW_LOGOS = ROOT / "www" / "assets" / "logos"

INDIVIDUAL_INT_FIELDS = ("rank", "time_seconds")
RELAY_INT_FIELDS = ("rank", "total_time_seconds", "leg1_time_seconds", "leg2_time_seconds", "leg3_time_seconds")


def _to_int(value):
    value = (value or "").strip()
    return int(value) if value else None


def _years():
    return sorted(int(p.name) for p in RESULTS.iterdir() if p.is_dir() and p.name.isdigit())


def _read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_individual_and_relay():
    individual, relay = [], []
    for year in _years():
        year_dir = RESULTS / str(year)
        for discipline in ("sprint", "long"):
            path = year_dir / f"{discipline}.csv"
            if not path.exists():
                continue
            for row in _read_csv(path):
                row["year"] = year
                row["discipline"] = discipline
                for field in INDIVIDUAL_INT_FIELDS:
                    row[field] = _to_int(row.get(field))
                individual.append(row)
        relay_path = year_dir / "relay.csv"
        if relay_path.exists():
            for row in _read_csv(relay_path):
                row["year"] = year
                row["discipline"] = "relay"
                for field in RELAY_INT_FIELDS:
                    row[field] = _to_int(row.get(field))
                relay.append(row)
    return individual, relay


def build_events():
    events = {}
    available_logos = {p.stem for p in LOGOS_SRC.glob("eyoc-*.png")} if LOGOS_SRC.exists() else set()
    for year in _years():
        meta_path = RESULTS / str(year) / "metadata.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {"year": year}
        meta["has_logo"] = f"eyoc-{year}" in available_logos
        events[str(year)] = meta
    return events


def copy_logos():
    WWW_LOGOS.mkdir(parents=True, exist_ok=True)
    if not LOGOS_SRC.exists():
        return 0
    count = 0
    for src in LOGOS_SRC.glob("eyoc-*.png"):
        shutil.copyfile(src, WWW_LOGOS / src.name)
        count += 1
    return count


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def main():
    individual, relay = build_individual_and_relay()
    events = build_events()

    write_json(WWW_DATA / "individual.json", individual)
    write_json(WWW_DATA / "relay.json", relay)
    write_json(WWW_DATA / "events.json", events)

    logo_count = copy_logos()

    content_hash = hashlib.sha256(
        (WWW_DATA / "individual.json").read_bytes()
        + (WWW_DATA / "relay.json").read_bytes()
        + (WWW_DATA / "events.json").read_bytes()
    ).hexdigest()[:12]
    write_json(WWW_DATA / "manifest.json", {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "content_hash": content_hash,
        "individual_rows": len(individual),
        "relay_rows": len(relay),
        "years": len(events),
    })

    print(f"individual.json: {len(individual)} rows")
    print(f"relay.json: {len(relay)} rows")
    print(f"events.json: {len(events)} years")
    print(f"logos copied: {logo_count}")
    print(f"content_hash: {content_hash}")


if __name__ == "__main__":
    main()
