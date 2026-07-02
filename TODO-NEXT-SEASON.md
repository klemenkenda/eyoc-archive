# TODO: Adding Next Season to the Archive

Step-by-step checklist for onboarding a new EYOC edition after the event.

---

## 1. Download raw results

**Preferred source: IOF Eventor (IOF web page)**

All results are published on the IOF Eventor platform. Download the XML result files for each discipline:

- Sprint individual results → `results/raw/<year>/`
- Long individual results → `results/raw/<year>/`
- Relay results → `results/raw/<year>/`

Eventor exports IOF-XML 3.0. The naming convention used so far:
- `<NN>-sprint-results-eventor.xml` / `<NN>-long-results-eventor.xml` / `<NN>-relay-results-eventor.xml` (2026 style), or
- `Sprint-eventor.xml` / `Long-eventor.xml` (2019–2024 style), or
- `Sprint.xml` / `Long.xml` / `Relay.xml` (2025 WinSplits style).

Pick any consistent naming; what matters is registering the actual filenames in `scripts/parsers/parse_xml.py`.

> If Eventor is not available, fall back to OE2010/OS2010 SportSoftware PDFs (handled by `parse_oe_pdf.py`) or, for relay only, an Eventor "print view" PDF (`parse_eventor_relay_pdf.py`). Check `scripts/parsers/PARSERS.md` for which parser covers which format.

---

## 2. Register the new files in the parser

Open `scripts/parsers/parse_xml.py` and add the new year's filenames to the two dicts near the top of the file:

```python
INDIVIDUAL_FILES = {
    ...
    <year>: [("<sprint-filename>.xml", "sprint"), ("<long-filename>.xml", "long")],
}
RELAY_FILES = {
    ...
    <year>: "<relay-filename>.xml",
}
```

If Eventor XML was not available and you are using a different format, add the year to the relevant parser instead (see `scripts/parsers/PARSERS.md` for the full list).

---

## 3. Run the parsers

```sh
python scripts/parsers/run_all.py
```

This regenerates every `results/<year>/*.csv` from `results/raw/`. Check the output for unexpected `dropped:` counts — those usually mean guest nations being filtered out, which is expected, but a high drop count could indicate a country-code mapping issue.

Cross-check field sizes against the official start list to catch any silent parse failures, and update `results/raw/QUALITY-CHECK.md` with the new year's row counts and any caveats.

---

## 4. Update the IOF ranking lists

The name-cleanup tool compares EYOC names against the IOF world ranking files in `results/iof/`. Refresh them before running the cleanup so the new season's athletes are covered:

1. Download the current IOF world ranking CSVs (men's footO and women's footO) from the IOF web page.
2. Replace the files in `results/iof/`:
   - `iof_ranking_MEN_F_<DD-MM-YYYY>.csv`
   - `iof_ranking_WOMEN_F_<DD-MM-YYYY>.csv`
3. Delete (or archive) the old ranking files so the tool does not pick up stale entries.

---

## 5. Name cleanup — apply existing corrections

An already-reviewed batch of corrections is archived at `scripts/name_cleanup/name_corrections.20260701-1630.csv`. Apply it first (before running detection on new data, so detect starts from a clean baseline):

```sh
python scripts/name_cleanup/find_name_corrections.py apply --dry-run \
    --in scripts/name_cleanup/name_corrections.20260701-1630.csv
python scripts/name_cleanup/find_name_corrections.py apply \
    --in scripts/name_cleanup/name_corrections.20260701-1630.csv
git diff results/
```

---

## 6. Name cleanup — detect and apply corrections for the new season

Now run detection to find misspellings in the new season's data (and any that prior rounds missed):

```sh
python scripts/name_cleanup/find_name_corrections.py detect
```

Review `scripts/name_cleanup/name_corrections.csv`:
- Set `status` to `approved` for rows you agree with (edit `to_name` first if the suggestion is wrong).
- Delete or leave blank rows that are false positives (e.g. siblings, two distinct athletes with similar names).
- Pay extra attention to rows marked `conflict-multiple-iof-matches` or `conflict-ambiguous-iof-match`.

Apply and archive:
```sh
python scripts/name_cleanup/find_name_corrections.py apply --dry-run
python scripts/name_cleanup/find_name_corrections.py apply
git diff results/
mv scripts/name_cleanup/name_corrections.csv \
   scripts/name_cleanup/name_corrections.<YYYYMMDD-HHMM>.csv
```

Repeat detect → review → apply until the detect run produces no new suggestions (or only rows you intentionally skip).

---

## 7. Build the www dataset

```sh
python scripts/build_www_data.py
```

This reads `results/` (post-cleanup) and writes the static JSON files consumed by the web app:
- `www/data/individual.json`
- `www/data/relay.json`
- `www/data/events.json`
- `www/data/manifest.json`
- `www/assets/logos/*.png`

Also add the event logo to `logos/png/eyoc-<year>.png` before this step if available.

---

## 8. Commit and deploy

```sh
git add results/raw/<year>/ results/<year>/ results/raw/QUALITY-CHECK.md \
        scripts/parsers/parse_xml.py \
        scripts/name_cleanup/ \
        results/iof/ \
        www/data/ www/assets/logos/
git commit -m "Add <year> EYOC results"
```

Deploy the updated `www/` directory to the hosting environment (eyoc.spletne-resitve.eu).

---

## Summary order

```
1. Download raw XMLs from IOF Eventor  →  results/raw/<year>/
2. Register filenames in parse_xml.py
3. python scripts/parsers/run_all.py
4. Refresh results/iof/ ranking CSVs
5. find_name_corrections.py apply --in name_corrections.20260701-1630.csv
6. find_name_corrections.py detect  →  review  →  apply  →  archive  (repeat until clean)
7. python scripts/build_www_data.py
8. git commit + deploy
```
