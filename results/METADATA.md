# EYOC metadata JSON with raw-source provenance (2002-2026)

This package contains `metadata.json` in each year folder.

## What is filled now

- `title`, `city`, `country`
- `field_size` per discipline/category from normalized CSV rows
- `source.raw_source_files` and `source.raw_source_formats` from the CSV `source_file` column

## What is deliberately left as `null`

Course fields remain `null` in this generated package where the current runtime could not save/parse the raw XML/PDF/HTML files directly:

- `place`
- `map_name`
- `distance_km`
- `elevation_m`
- `control_points`

## Fill from raw XML locally

Clone the repository, unzip this package, then run:

```bash
python scripts/update_metadata_from_raw.py --repo /path/to/eyoc-archive --metadata /path/to/unzipped-metadata-root
```

The script parses IOF XML files in `results/raw/<year>/` and fills course metadata when the XML contains it.
