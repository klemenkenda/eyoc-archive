# Parsers

Each module here handles one raw source *format*, not one year — e.g. every
OE2010/OS2010 PDF result sheet goes through `parse_oe_pdf.py` regardless of which year
used that software. Where a format's exact markup drifts year to year (mainly the
2002–2013 hand-coded HTML archive), the module has one small per-year function rather
than a single regex stretched to fit every year.

All parsers write into `results/<year>/{sprint,long,relay}.csv` per the schema in
[`results/FORMAT-RESULTS.md`](../../results/FORMAT-RESULTS.md), and filter `country` to
the federations listed in
[`results/EYOC-COUNTRIES.md`](../../results/EYOC-COUNTRIES.md). Run any parser directly
from the repository root, or all of them via `run_all.py`.

## Setup

```sh
pip install pymupdf pytesseract
```

- **PyMuPDF (`fitz`)** — used by `common.pdf_rows()` / `common.render_pdf_pages()` for
  every PDF parser. Required.
- **`pdftotext`** (from poppler-utils) — only used by `parse_text_pdf.py` for 2017
  Sprint/Long, via `common.pdf_to_text()`. Needs to be on `PATH`.
- **Tesseract OCR** — only used by the two `*_ocr.py` parsers, via `pytesseract`. Needs
  the `eng` language data; `common.configure_tesseract()` tries to locate a conda-forge
  install (`conda install -c conda-forge tesseract`) automatically, but a system install
  on `PATH` works too.

## Running everything

```sh
python scripts/parsers/run_all.py
```

Regenerates every `results/<year>/*.csv` from `results/raw/`, in this order:
`parse_lazarus_html` → `parse_lazarus_relay` → `parse_text_pdf` → `parse_oe_pdf` →
`parse_relay_text_pdf` → `parse_eventor_relay_pdf` → `parse_xml` →
`parse_2016_sprint_ocr` → `parse_2014_relay_ocr`. Order doesn't matter functionally
(each parser only touches its own years/files) — it's just the order they were added.

## Running one parser

Every module is also runnable standalone — useful after editing just one of them:

```sh
python scripts/parsers/parse_xml.py
python scripts/parsers/parse_lazarus_relay.py
```

Each prints one line per year/discipline it touched, e.g.:

```
2013 relay: kept 91/91 -> results/2013/relay.csv
2014 sprint: kept 376/386  -> results/2014/sprint.csv  (dropped: 11)
```

`kept/total` is rows written vs. rows the parser attempted to read; a `dropped: N`
suffix means N rows didn't survive country resolution (usually a non-European guest
nation or a composite/mixed team, both intentionally excluded — see
`results/raw/QUALITY-CHECK.md` for whether a given year's drops are expected).

## `common.py`

Not a parser itself — shared helpers every parser imports:

- `normalize_country` / `normalize_class` / `normalize_status` / `time_to_seconds` —
  text → normalized value, tolerant of the many spellings/codes/formats seen across 24
  years of sources.
- `format_name` / `reorder_name` — Title-cases names and normalizes "Surname Given" /
  "Given Surname" ordering signals (comma, ALL-CAPS run) to a consistent Given-first
  order. Applied automatically by `individual_row()`/`relay_row()`.
- `pdf_rows()` / `row_text()` / `bucket_row()` — PyMuPDF word-coordinate row
  reconstruction and column-bucketing for PDFs. Used in preference to
  `pdftotext -layout`, which misaligns columns on several of these PDF templates.
  `pdf_to_text()` wraps `pdftotext -layout` itself for the one parser that still needs it.
  `render_pdf_pages()` / `tesseract_ocr()` / `group_ocr_lines()` — OCR pipeline for
  scanned PDFs with no text layer at all.
- `individual_row()` / `relay_row()` / `write_csv()` — build a row dict in the
  `FORMAT-RESULTS.md` schema and write the CSV.

## Parser reference

### `parse_xml.py` — IOF-XML / Eventor

```sh
python scripts/parsers/parse_xml.py
```

2019, 2021–2026 Sprint/Long; 2025–2026 Relay. Handles three XML flavours (Eventor-native,
plain IOF-XML 3.0 from WinSplits, IOF-XML 3.0 from Oribos) via `INDIVIDUAL_FILES`/
`RELAY_FILES` dicts at the top of the module — add a year there if a future event uses
one of these flavours under a new filename.

### `parse_oe_pdf.py` — OE2010/OS2010 SportSoftware PDFs

```sh
python scripts/parsers/parse_oe_pdf.py
```

2014, 2015, 2018 Sprint/Long/Relay; 2019, 2024 Relay. File lists in `INDIVIDUAL_FILES`/
`RELAY_FILES`. Column positions come from each PDF's own header row, so it adapts to
minor per-year column changes automatically.

### `parse_text_pdf.py` — one-off plain-text PDFs

```sh
python scripts/parsers/parse_text_pdf.py
```

2016 Long, 2017 Sprint/Long — two distinct one-off formats sharing a module since
neither fits the `(N)`-header OE2010 template. 2016 Sprint is a scanned image with no
text layer at all — see `parse_2016_sprint_ocr.py` instead.

### `parse_relay_text_pdf.py` — 2016/2017 Relay

```sh
python scripts/parsers/parse_relay_text_pdf.py
```

2016 Relay (one row per team, all 3 legs inline) and 2017 Relay (a team header row then
a separate legs row) — two distinct row grammars in one module.

### `parse_eventor_relay_pdf.py` — Eventor "print view" relay PDFs

```sh
python scripts/parsers/parse_eventor_relay_pdf.py
```

2021–2023 Relay, exported from Eventor's print-view layout rather than SportSoftware.

### `parse_lazarus_html.py` — lazarus.elte.hu archive, individual races

```sh
python scripts/parsers/parse_lazarus_html.py
```

2002–2013 Sprint/Long, from the single combined-year HTML page archived at
lazarus.elte.hu (the only surviving source for these years). Relay is intentionally not
handled here — see `parse_lazarus_relay.py`.

### `parse_lazarus_relay.py` — lazarus.elte.hu archive, relay

```sh
python scripts/parsers/parse_lazarus_relay.py
```

2002–2005, 2007–2013 Relay. `YEAR_PARSERS` at the bottom of the module maps year →
parse function; most years share one of two generic builders
(`make_colon_year_parser`/`make_dot_year_parser`, parameterized per year for time format,
name order, and birth-year suffix), while 2002, 2003, and 2013 have fully bespoke
functions because their line grammar doesn't fit either builder. 2006 has no parser —
the only source found has just top-3 placings with no runner names, not enough data for
the schema. To add a year: read the raw HTML's relay section by hand, pick or write a
matching function, add it to `YEAR_PARSERS`, then verify with the leg-time-sum check
below before trusting the output.

### `parse_2016_sprint_ocr.py` / `parse_2014_relay_ocr.py` — scanned PDFs (OCR)

```sh
python scripts/parsers/parse_2016_sprint_ocr.py
python scripts/parsers/parse_2014_relay_ocr.py
```

2016 Sprint and 2014 Relay are the two source files with no embedded text layer at all
(genuine scans). Each renders every page to PNG and runs Tesseract OCR
(`common.tesseract_ocr`), then reconstructs rows the same way the text-based PDF parsers
do. Both write `confidence=approx` rather than `high`. Requires Tesseract OCR to be
installed (see Setup above) — without it these two will raise rather than silently
produce empty output.

## Verifying a relay parser's output

There's no ground-truth source to diff against, but every relay team's 3 leg times
should sum to its printed total time — this catches most row-splitting bugs even
without one:

```sh
python -c "
import csv
for year in range(2002, 2027):
    try:
        rows = list(csv.DictReader(open(f'results/{year}/relay.csv', encoding='utf-8')))
    except FileNotFoundError:
        continue
    bad = 0
    for row in rows:
        if row['status'] != 'OK':
            continue
        legs = [row['leg1_time_seconds'], row['leg2_time_seconds'], row['leg3_time_seconds']]
        if all(legs) and abs(sum(int(x) for x in legs) - int(row['total_time_seconds'])) > 2:
            bad += 1
            print(year, row['class'], row['country'], 'mismatch')
    print(year, 'rows', len(rows), 'mismatches', bad)
"
```
