"""Shared lock registry for hand-curated results CSVs.

results/locks.json records which <year>/<discipline>.csv files a human has reviewed and
fixed by hand. Locked files are source of truth from that point on: scripts/parsers/common.py's
write_csv() and scripts/name_cleanup/find_name_corrections.py's apply step both skip a file
while it's locked, so `python scripts/parsers/run_all.py` (and name-correction apply runs)
are still safe to re-run at any time without clobbering curated data.

Locks are normally toggled through the curation GUI (scripts/curation_gui/), not edited by
hand, but the file is plain JSON if you ever need to.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCKS_PATH = ROOT / "results" / "locks.json"

DISCIPLINES = ("sprint", "long", "relay")


def load() -> dict:
    """{year_str: [discipline, ...]}, e.g. {"2018": ["sprint", "relay"]}."""
    if not LOCKS_PATH.exists():
        return {}
    return json.loads(LOCKS_PATH.read_text(encoding="utf-8"))


def save(locks: dict) -> None:
    cleaned = {year: sorted(set(disciplines)) for year, disciplines in locks.items() if disciplines}
    LOCKS_PATH.write_text(json.dumps(cleaned, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def is_locked(year, discipline: str) -> bool:
    return discipline in load().get(str(year), [])


def set_locked(year, discipline: str, locked: bool) -> None:
    locks = load()
    key = str(year)
    disciplines = set(locks.get(key, []))
    if locked:
        disciplines.add(discipline)
    else:
        disciplines.discard(discipline)
    locks[key] = sorted(disciplines)
    save(locks)
