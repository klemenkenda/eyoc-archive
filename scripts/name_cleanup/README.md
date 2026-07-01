# Competitor Name Cleanup

`find_name_corrections.py` finds likely misspellings of competitor names across
the normalized results CSVs (`results/<year>/{long,sprint,relay}.csv`) and
produces a translation file for you to review before anything is changed.

## Pipeline position

This is a postprocessing step on top of the parser output, run in this order:

```sh
python scripts/parsers/run_all.py                              # 1. regenerate results/ from raw sources
python scripts/name_cleanup/find_name_corrections.py detect     # 2. --- this tool, see Usage below ---
python scripts/build_www_data.py                                # 3. build the www/ dataset
```

Name corrections must be applied **before** `build_www_data.py` runs, since the
www dataset is built directly from `results/`; running the build first would ship
the misspellings and require a rebuild once corrections land.

It compares names in two ways, both scoped by country (the same name can be
common in one country and a typo in another, so country avoids false matches):

- **Against `results/iof/*.csv`** - the official IOF world ranking lists.
  Many EYOC juniors go on to elite senior careers, so a lot of names in this
  archive show up there with a known-correct spelling. Gender is taken from
  which file the name is in (`iof_ranking_MEN_F_*` vs. `iof_ranking_WOMEN_F_*`).
- **Against each other** - if the same person is spelled two different ways
  across different years/files with no IOF match available, the more common
  spelling wins.

In both cases, two spellings are only ever treated as the same person if:
- they were seen in the **same year or adjacent years** (e.g. 2013 and 2014
  is fine; 2013 and 2016 is not), and
- they raced in a **compatible class** - M16/M18 count as the same person
  aging up, as do W16/W18, but M* is never merged with W*.

A bigger year gap or a gender mismatch is treated as two different
competitors with similar names, not a misspelling - e.g. Topias Arola (EYOC
2016-2019) and Topias Ahola (EYOC 2013-2014) are two distinct real
IOF-ranked Finnish athletes, correctly never suggested as a correction of
each other.

## Usage

1. Generate suggestions:

   ```sh
   python scripts/name_cleanup/find_name_corrections.py detect
   ```

   Writes `scripts/name_cleanup/name_corrections.csv` with one row per
   spelling that might need fixing:

   | column | meaning |
   |---|---|
   | `status` | empty by default; set to `approved` to apply this row |
   | `country` | 3-letter country code |
   | `from_name` | the spelling as it currently appears in the CSVs |
   | `to_name` | the suggested correct spelling - edit this if the tool guessed wrong |
   | `reason` | `iof-exact`, `iof-fuzzy`, `internal`, or `conflict-*` (see below) |
   | `score` | `exact`, or `dist=N ratio=R` for fuzzy matches |
   | `occurrences` | how many rows currently use `from_name` |
   | `sample_files` | a few `source_file` values, for context |

2. **Review the CSV by hand.** This is the important step - fuzzy name
   matching *will* occasionally flag two different people as a misspelling
   (e.g. siblings sharing a surname, or a genuine nickname). For each row you
   agree with, set `status` to `approved` (edit `to_name` first if needed).
   Leave `status` blank, or delete the row, to skip it.

   Rows marked `conflict-multiple-iof-matches` or `conflict-ambiguous-iof-match`
   matched more than one distinct real IOF athlete for that country - check
   these especially carefully.

3. Apply the approved rows:

   ```sh
   # preview only, writes nothing
   python scripts/name_cleanup/find_name_corrections.py apply --dry-run

   # actually rewrite the results CSVs
   python scripts/name_cleanup/find_name_corrections.py apply
   ```

   Only exact `(country, from_name)` matches are replaced, so applying is
   safe to re-run - unrelated rows are left untouched. Since the results
   CSVs are git-tracked, `git diff` afterwards to confirm the changes, and
   `git checkout -- results/` to undo if something looks wrong.

4. Archive the reviewed batch under a timestamped name instead of leaving it as
   the plain `name_corrections.csv` (which the next `detect` run overwrites):

   ```sh
   mv scripts/name_cleanup/name_corrections.csv \
      scripts/name_cleanup/name_corrections.<YYYYMMDD-HHMM>.csv
   ```

   using the date/time you did the review, e.g.
   `name_corrections.20260701-1630.csv` for the first reviewed/applied batch.
   This keeps a permanent, auditable record of exactly which corrections were
   approved and when - `git blame`/`git log` on the live `name_corrections.csv`
   alone can't tell you that once it's been regenerated and overwritten by a
   later round. Re-run `detect` afterwards to generate the next round's file.

## Notes

- Matching is heuristic (edit distance + `difflib` similarity ratio, tuned to
  avoid flagging short-first-name differences on a shared surname as a
  misspelling). It will miss some real typos and occasionally suggest a wrong
  fix - that's why review is a required step, not optional.
- Re-running `detect` after `apply` should show a smaller/empty diff for the
  rows you approved; new suggestions may appear as new results get added over
  time.
