# Proposed CSV format for normalized EYOC results

`results/raw/<year>/` holds the original files as downloaded (IOF-XML, PDF, HTML —
whatever each year happened to publish). This document proposes a normalized CSV layout
to convert that into, mirrored one level up: `results/<year>/sprint.csv`,
`results/<year>/long.csv`, `results/<year>/relay.csv`. One file per year per discipline.
`year` itself isn't a column — it's already the folder name.

Sprint and Long share the same columns (both are just "ranked individual result, one row
per person"). Relay is its own shape: one row per **team**, with all three leg runners
inline on that row.

## `sprint.csv` / `long.csv`

One row per competitor.

| column | type | meaning |
|---|---|---|
| `class` | text | `M16`, `M18`, `W16`, `W18` |
| `rank` | int, blank if unranked | finishing position within the class |
| `status` | text | `OK`, `DNF`, `DSQ`, `DNS`, `MP` — default `OK` |
| `bib` | text, optional | start/bib number if the source has one |
| `country` | text | country/federation name or IOF 3-letter code, whichever the source gives |
| `name` | text | competitor's full name |
| `time_seconds` | int, blank if no time | total elapsed time, converted to seconds so every year is comparable regardless of source format (`mm:ss`, `h:mm:ss`, ...) |
| `confidence` | text | `high` / `approx` — carries forward the flags from `QUALITY-CHECK.md`; omit or default `high` |
| `source_file` | text | path relative to `results/raw/<year>/`, e.g. `results-sprint.pdf` |

## `relay.csv`

One row per team, three runners wide.

| column | type | meaning |
|---|---|---|
| `class` | text | `M16`, `M18`, `W16`, `W18`, `Mixed` (bonus mixed sprint relay) |
| `rank` | int, blank if unranked | |
| `status` | text | `OK`, `DNF`, `DSQ`, `DNS`, `MP` |
| `country` | text | federation name/code, without any team-number suffix |
| `team` | text | team label exactly as the source prints it, e.g. `Czech Republic 1` (countries sometimes field more than one team) |
| `total_time_seconds` | int | team's overall finish time |
| `leg1_name` | text | runner 1 |
| `leg1_time_seconds` | int, optional | leg 1 split |
| `leg2_name` | text | runner 2 |
| `leg2_time_seconds` | int, optional | leg 2 split |
| `leg3_name` | text | runner 3 |
| `leg3_time_seconds` | int, optional | leg 3 split |
| `confidence` | text | `high` / `approx` |
| `source_file` | text | path relative to `results/raw/<year>/` |

Notes:
- Leg time columns are optional — leave blank where the source doesn't reliably distinguish
  team-rank rows from leg-runner rows (the lazarus.elte.hu years, 2002–2013 — see
  `QUALITY-CHECK.md`). The team's own `rank`/`total_time_seconds` still gets filled in;
  only the three `legN_*` columns are left empty.
- Three leg columns assumes a 3-person relay, which has been the EYOC relay format every
  year checked. If a future year ever runs a different leg count, that year's file would
  need extra `leg4_*` columns — not worth building in up front for a format that's been
  constant for 24 editions.
- Known-abbreviated years (2002) or known-missing files (2006 `relay.csv`) simply don't
  exist / have fewer rows — no special "missing" marker needed.
