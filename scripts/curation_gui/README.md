# Data Curation GUI

A local-only tool for reviewing and hand-fixing results, separate from the public `www/`
app. For a given year/discipline it shows the original raw source file next to the
generated CSV, lets you edit the CSV directly, edit that year's `metadata.json`
(distance/climb/controls/place/etc.), and lock the CSV once you're happy with it.

Locking a `<year>/<discipline>.csv` means `python scripts/parsers/run_all.py` (and
`scripts/name_cleanup/find_name_corrections.py apply`) will skip it from then on - see
`scripts/locks.py` and `results/locks.json`. Unlock it from this GUI to let the pipeline
regenerate it again.

## Run

```sh
pip install -r requirements.txt
python scripts/curation_gui/app.py
```

Then open http://127.0.0.1:5151. Nothing here is deployed; it's dev tooling in the same
spirit as `docker-compose.yml`.

## Layout

- **Top bar** - pick a year and discipline (Sprint/Long/Relay), lock/unlock the current
  CSV, and trigger a full rebuild (`run_all.py`) without leaving the browser.
- **Left pane** - the original raw source file(s) for the selected discipline
  (PDF/HTML/XML/TXT under `results/raw/<year>/`), identified from the CSV's
  `source_file` column (starred in the dropdown) with the rest of that year's raw
  files also selectable for cross-reference.
- **Right pane** - the CSV as an editable table. Add/delete rows, edit any cell, then
  "Save CSV" to write it back in the schema from `results/FORMAT-RESULTS.md`. A banner
  warns when the file isn't locked, since a rebuild would discard your edits.
- **Bottom panel** - a form for `results/<year>/metadata.json`
  (`results/METADATA.md`): title/city/country/dates, and per-discipline
  place/map name/distance/climb/controls/field size for each of M16/M18/W16/W18.
  Metadata isn't touched by the parser pipeline, so it doesn't need locking.

## Notes

- "Rebuild from raw" runs the full `scripts/parsers/run_all.py` pipeline (can take a
  while - a couple of years use OCR). It only affects unlocked `<year>/<discipline>.csv`
  files; metadata and locked CSVs are untouched.
- This tool intentionally stops at the parser step. `name_cleanup`'s detect/review/apply
  flow and `build_www_data.py` remain separate manual steps (see the root `README.md`) -
  run them yourself once you're done curating.
