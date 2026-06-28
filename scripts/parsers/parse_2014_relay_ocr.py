"""OCR parser for the scanned 2014 EYOC Relay PDF.

`results/raw/2014/results-relay.pdf` (1.7 MB) has no embedded text layer - it's a raster
scan of an OS2010 sheet (confirmed by the page header: "OS2010 (c) Stephan Kraemer
SportSoftware 2014"), the same software/layout family as the text-based relay PDFs
`parse_oe_pdf.py` already handles for 2015/2018/2019/2024. So this reuses that parser's
row grammar (one "team" row - rank, bib, country, total time - followed by up to 3 "leg"
rows - runner name, leg time), just sourced from OCR'd word coordinates (via
common.render_pdf_pages/tesseract_ocr/group_ocr_lines) instead of a real text layer.

Status words ("mp", "disq", "dnf", "dns") appear in lowercase in both the team-total-time
and leg-time columns; unranked teams (mp/disq/dnf) have a blank Pl (rank) column, not a
dash, so team rows are identified by the Stno (bib) column being numeric rather than by
the rank column like parse_oe_pdf.py's text-based relay parser does.

Run directly from the repository root:
  python scripts/parsers/parse_2014_relay_ocr.py
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

YEAR = 2014
SOURCE_FILE = "2014/results-relay.pdf"
PDF = common.RAW / "2014" / "results-relay.pdf"
ZOOM = 4.0
LINE_Y_TOL = 4.5

# OCR coordinates normalized back to PDF points (divided by ZOOM). Calibrated against
# the header row ("Pl" @120, "Stno" @146, "Team"/"Name" @177, "B" @355, leg "Time" @391,
# total "Time" @451 at zoom=3) and stable across all 10 pages.
COLUMNS = {
    "rank": (100, 145),
    "bib": (145, 176),
    "team": (176, 375),
    "legtime": (375, 420),
    "totaltime": (420, 600),
}

CLASS_RE = re.compile(r"\b(M16|M18|W16|W18)\b.*?\((\d+)\)", re.IGNORECASE)
SKIP_RE = re.compile(r"\b(EYOC|RESULTS|STNO|PAGE)\b", re.IGNORECASE)
STATUS_WORDS = {"mp", "disq", "dsq", "dnf", "dns"}


def detect_class(text: str):
    m = CLASS_RE.search(text)
    return common.normalize_class(m.group(1)) if m else None


def words_by_column(words):
    cells = {name: [] for name in COLUMNS}
    for word in sorted(words, key=lambda w: w.x):
        for name, (start, end) in COLUMNS.items():
            if start <= word.cx < end:
                cells[name].append(word.text)
                break
    return cells


def clean_cell(parts):
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def parse_time_or_status(text: str):
    """Returns (status, seconds). A leg/total time cell is either a clock time, a
    lowercase status word (mp/disq/dnf/dns), or a status word plus a parenthetical
    OCR'd annotation (e.g. "dnf (Exceeded maximum running time)") - only the leading
    status word matters."""
    cleaned = text.strip()
    if not cleaned:
        return None, None
    first_word = re.split(r"[\s(]", cleaned, maxsplit=1)[0].lower()
    if first_word in STATUS_WORDS:
        return common.normalize_status(first_word, False), None
    seconds = common.time_to_seconds(cleaned)
    if seconds is not None:
        return "OK", seconds
    return None, None


def parse_relay(words):
    rows = []
    total_seen = 0
    current_class = None
    pending = None  # dict: rank, bib, country_text, total_time, status, legs[]

    def flush():
        nonlocal pending
        if pending is None:
            return
        country = common.normalize_country(pending["country_text"])
        if country:
            code, _name = country
            rows.append(common.relay_row(
                pending["class"], pending["rank"], pending["status"], code, code,
                pending["country_text"], pending["total_time"], pending["legs"],
                "approx", SOURCE_FILE,
            ))
        pending = None

    for line in common.group_ocr_lines(words, y_tol=LINE_Y_TOL):
        text = common.ocr_line_text(line)
        if not text.strip():
            continue
        klass = detect_class(text)
        if klass:
            flush()
            current_class = klass
            continue
        if not current_class or SKIP_RE.search(text) or text.strip().upper().startswith("NAME"):
            continue

        cells = words_by_column(line)
        bib = clean_cell(cells["bib"])
        is_team_row = bool(re.match(r"^\d{2,4}$", bib))

        if is_team_row:
            total_seen += 1
            flush()
            rank_text = clean_cell(cells["rank"])
            rank = int(rank_text) if rank_text.isdigit() else None
            country_text = clean_cell(cells["team"])
            status, total_time = parse_time_or_status(clean_cell(cells["totaltime"]))
            pending = {
                "class": current_class, "rank": rank, "bib": bib,
                "country_text": country_text,
                "total_time": total_time, "status": status or "DNF", "legs": [],
            }
        else:
            if pending is None or len(pending["legs"]) >= 3:
                continue
            name = clean_cell(cells["team"])
            if not name:
                continue
            _leg_status, leg_time = parse_time_or_status(clean_cell(cells["legtime"]))
            pending["legs"].append((name, leg_time))
    flush()
    return rows, total_seen


def main() -> None:
    if not PDF.exists():
        raise FileNotFoundError(PDF)
    with tempfile.TemporaryDirectory(prefix="eyoc2014_relay_ocr_") as tmp:
        image_paths = common.render_pdf_pages(PDF, Path(tmp), zoom=ZOOM)
        words = common.tesseract_ocr(image_paths, zoom=ZOOM)
    rows, total_seen = parse_relay(words)
    out = common.write_csv(YEAR, "relay", rows, common.RELAY_COLUMNS)
    dropped = total_seen - len(rows)
    print(f"{YEAR} relay: OCR kept {len(rows)}/{total_seen} -> {out}" + (f"  (dropped: {dropped})" if dropped else ""))


if __name__ == "__main__":
    main()
