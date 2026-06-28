"""OCR parser for the scanned 2016 EYOC Sprint PDF.

This is intentionally separate from the text-based PDF parsers. The source file
`results/raw/2016/results-sprint.pdf` has no embedded text layer at all (confirmed: its
single PDF "text block" is just the logo image) - it's a genuine raster scan, so the
parser renders each page to PNG, OCRs it, reconstructs table rows from the OCR word
coordinates, and writes `results/2016/sprint.csv`.

This was originally written against Windows' built-in Windows.Media.Ocr API, which
turned out to have a real, reproducible blind spot: it fails to recognize short,
isolated colon-separated digit runs (e.g. "0:10:19") as text at all - verified with
synthetic test images, at multiple zoom levels, with explicit language selection, with
and without adjacent anchor text. That's exactly the "Netto" (time) column here, so the
Windows engine could read every column except the one that matters most. Switched to
Tesseract (via pytesseract), which reads this page cleanly including the time column.

Requirements:
  - Tesseract OCR installed (e.g. `conda install -c conda-forge tesseract`) with the
    `eng` language data present in its tessdata directory
  - pytesseract (`pip install pytesseract`)
  - PyMuPDF (`fitz`) for rendering the PDF pages

Run directly from the repository root:
  python scripts/parsers/parse_2016_sprint_ocr.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

YEAR = 2016
DISCIPLINE = "sprint"
SOURCE_FILE = "2016/results-sprint.pdf"
PDF = common.RAW / "2016" / "results-sprint.pdf"
ZOOM = 4.0

# OCR coordinates are normalized back to PDF points by dividing by ZOOM. These columns
# are stable across the 2016 sprint pages.
COLUMNS = {
    "rank": (0, 55),
    "bib": (55, 120),
    "name": (120, 345),
    "country": (345, 480),
    "time": (480, 560),
}
LINE_Y_TOL = 4.5


def detect_class(text: str) -> str | None:
    compact = re.sub(r"[^A-Za-z0-9]", "", text).upper()
    match = re.search(r"([MW]1[68])", compact)
    if match and "SPRINT" in compact:
        return common.normalize_class(match.group(1))
    return None


def words_by_column(words: list[common.OcrWord]) -> dict[str, list[str]]:
    cells = {name: [] for name in COLUMNS}
    for word in sorted(words, key=lambda w: w.x):
        for name, (start, end) in COLUMNS.items():
            if start <= word.cx < end:
                cells[name].append(word.text)
                break
    return cells


def clean_cell(parts: list[str]) -> str:
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def parse_rank(text: str) -> int | None:
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None


def parse_bib(text: str) -> str:
    match = re.search(r"\d{2,4}", text)
    return match.group() if match else ""


def normalize_ocr_time(text: str) -> tuple[str, int | None]:
    cleaned = text.upper().replace("O:", "0:").replace("Q:", "0:")
    if "DISQ" in cleaned or "DSQ" in cleaned:
        return "DSQ", None
    if "DNF" in cleaned:
        return "DNF", None
    if "DNS" in cleaned:
        return "DNS", None
    if "MP" in cleaned:
        return "MP", None

    match = re.search(r"(?:0:)?(\d{1,2}):(\d{2})", cleaned)
    if not match:
        return "DNF", None
    minutes = int(match.group(1))
    seconds = int(match.group(2))
    return "OK", minutes * 60 + seconds


def clean_name(text: str) -> str:
    text = re.sub(r"[^A-Za-zÀ-ž'´` -]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    # The scanned page prints the whole name in caps with no case distinction between
    # surname and given name, so common.reorder_name's ALL-CAPS-run heuristic can't tell
    # the order apart here. Cross-checking against the 2016 Long PDF (same event, same
    # competitors, real text layer) confirms this source prints "Surname Given" - move
    # the trailing word to the front.
    words = text.split(" ")
    if len(words) >= 2:
        text = " ".join([words[-1]] + words[:-1])
    return text


def parse_rows(words: list[common.OcrWord]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    current_class: str | None = None
    seen_keys: set[tuple[object, ...]] = set()

    for line in common.group_ocr_lines(words, y_tol=LINE_Y_TOL):
        text = common.ocr_line_text(line)
        klass = detect_class(text)
        if klass:
            current_class = klass
            continue
        if not current_class:
            continue
        if re.search(r"\b(NUMER|NAZWISKO|KLUB|NETTO|WYNIKI|EYOC)\b", text.upper()):
            continue

        cells = words_by_column(line)
        bib = parse_bib(clean_cell(cells["bib"]))
        name = clean_name(clean_cell(cells["name"]))
        country_text = clean_cell(cells["country"])
        time_text = clean_cell(cells["time"])

        if not bib or not name or not country_text:
            continue
        country = common.normalize_country(country_text)
        if not country:
            continue
        code, _country_name = country
        status, time_s = normalize_ocr_time(time_text)
        rank = parse_rank(clean_cell(cells["rank"]))
        if status != "OK":
            rank = None

        key = (current_class, rank, status, bib, code, name, time_s)
        if key in seen_keys:
            continue
        seen_keys.add(key)

        rows.append(
            common.individual_row(
                current_class,
                rank,
                status,
                bib,
                code,
                name,
                time_s,
                "approx",
                SOURCE_FILE,
            )
        )
    return rows


def write_csv(rows: list[dict[str, object]]) -> Path:
    out_dir = common.ensure_year_dir(YEAR)
    out = out_dir / f"{DISCIPLINE}.csv"
    import csv
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=common.SPRINT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in common.SPRINT_COLUMNS})
    return out


def main() -> None:
    if not PDF.exists():
        raise FileNotFoundError(PDF)
    import tempfile
    with tempfile.TemporaryDirectory(prefix="eyoc2016_sprint_ocr_") as tmp:
        image_paths = common.render_pdf_pages(PDF, Path(tmp), zoom=ZOOM)
        words = common.tesseract_ocr(image_paths, zoom=ZOOM)
    rows = parse_rows(words)
    out = write_csv(rows)
    counts: dict[str, int] = {}
    for row in rows:
        counts[str(row["class"])] = counts.get(str(row["class"]), 0) + 1
    count_text = ", ".join(f"{klass}={counts[klass]}" for klass in sorted(counts))
    print(f"{YEAR} {DISCIPLINE}: OCR kept {len(rows)} rows ({count_text}) -> {out}")


if __name__ == "__main__":
    main()
