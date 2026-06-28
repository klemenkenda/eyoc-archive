# EYOC Results Archive

An archive of results from the European Youth Orienteering Championships (EYOC),
2002–2026: Sprint, Long (Middle), and Relay, for classes M16/M18/W16/W18 (plus the odd
bonus Mixed Sprint Relay where a year ran one).

The repository has two layers:

- **`results/raw/<year>/`** — the original files as found/downloaded for each year:
  whatever that year's organizers happened to publish (IOF-XML, OE2010/OS2010 PDF result
  sheets, scanned PDFs, or — for 2002–2013 — a single combined-year HTML page archived at
  [lazarus.elte.hu](http://lazarus.elte.hu)). Nothing in this layer is rewritten; it's
  the source of truth.
- **`results/<year>/{sprint,long,relay}.csv`** — a normalized CSV per discipline per
  year, generated *from* the raw layer by the parsers in `scripts/parsers/`. This is
  what you want if you're analyzing results rather than archaeology.

## Quick start

```sh
python scripts/parsers/run_all.py
```

Regenerates every `results/<year>/*.csv` from `results/raw/`. Safe to re-run any time —
it's a pure function of the raw files and the parser code, nothing is hand-edited
downstream. See [`scripts/parsers/PARSERS.md`](scripts/parsers/PARSERS.md) for what each
parser covers, its dependencies, and how to run pieces of the pipeline individually.

## Layout

```
results/
  raw/<year>/             original source files (read-only source of truth)
  raw/QUALITY-CHECK.md    per-year coverage/confidence audit
  <year>/sprint.csv        normalized, one row per competitor
  <year>/long.csv          normalized, one row per competitor
  <year>/relay.csv         normalized, one row per team (3 legs wide)
  FORMAT-RESULTS.md        the CSV schema, column by column
  EYOC-COUNTRIES.md        the European-federation whitelist used to filter rows
scripts/parsers/
  common.py               shared helpers (country/name/time normalization, CSV I/O, OCR)
  parse_*.py              one parser per raw source *format* (not per year)
  run_all.py              regenerates every results/<year>/*.csv
  PARSERS.md              parser-by-parser documentation, with run examples
codex/
  consistency_check.py    independent clean-vs-raw audit, doesn't import scripts/parsers
```

## The CSV format

`sprint.csv`/`long.csv` are one row per competitor; `relay.csv` is one row per team with
all three leg runners inline. Full column-by-column schema:
[`results/FORMAT-RESULTS.md`](results/FORMAT-RESULTS.md).

Every row's `country` is restricted to the federations listed in
[`results/EYOC-COUNTRIES.md`](results/EYOC-COUNTRIES.md) — recent years' guest nations
(Australia, New Zealand, USA, Canada, ...) appear in the raw files but are filtered out
of the clean CSVs.

Every row also carries a `confidence` column (`high` or `approx`) — `approx` means the
data came from OCR rather than extracted text, see
[`results/raw/QUALITY-CHECK.md`](results/raw/QUALITY-CHECK.md) for exactly which years.

## Data quality

[`results/raw/QUALITY-CHECK.md`](results/raw/QUALITY-CHECK.md) tracks, per year and
discipline, the field-size counts and any known gaps or caveats (abbreviated sources,
missing files, OCR-derived confidence, unresolved name-order ambiguities). Read this
before trusting an unusual-looking number.

[`codex/consistency_check.py`](codex/consistency_check.py) is an independent audit: it
re-derives facts straight from the raw files (without importing the parser code) and
cross-checks them against the clean CSVs, to catch parser bugs the parsers' own author
wouldn't think to check for.

## Adding or fixing a parser

Each parser in `scripts/parsers/` handles one raw source *format*, not one year — e.g.
all OE2010/OS2010 PDF sheets share one parser regardless of which years used that
software. When a source's exact markup drifts year to year (this happens a lot in the
2002–2013 hand-coded HTML archive), the convention is one small per-year function inside
that format's parser module rather than a single regex stretched to fit every year. See
[`scripts/parsers/PARSERS.md`](scripts/parsers/PARSERS.md) for the current list and
each one's quirks.

After changing a parser, re-run `python scripts/parsers/run_all.py` and check
`results/raw/QUALITY-CHECK.md`'s per-year counts haven't regressed.
