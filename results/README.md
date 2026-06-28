# EYOC metadata JSON files (2002-2026)

This ZIP contains one folder per year, with `metadata.json` inside.

## Schema

Each metadata file has:

- `title`
- `city`
- `country`
- `long`, `sprint`, `relay`
  - `place`
  - `map_name`
  - `categories` (`M16`, `M18`, `W16`, `W18`)
    - `distance_km`
    - `elevation_m`
    - `controls`
    - `field_size`

## Important limitation

The normalized result CSV files in the repository contain rankings, competitors/teams, times, confidence and source-file references. They do not contain course metadata such as map name, distance, climb/elevation or number of controls. Therefore those requested course fields are set to `null`; `field_size` is populated from the CSV category row counts where available.

2020 is included as a folder because the requested range is 2002-2026, but EYOC 2020 was postponed and the repository has no 2020 result CSVs.
