# EYOC metadata JSON, enriched through 2017-2019 and 2021

This package contains simple `<year>/metadata.json` files for EYOC 2002-2026.

This build preserves the previous enrichment and adds verified values for 2017, 2018 and 2021 where available.

## Added in this pass

- 2017: Long M18 distance, climb and controls. Other 2017 course metrics remain null where not directly verified.
- 2018: Sprint and Long course metadata for W16, W18, M16 and M18, including place/map name, distance, climb and controls.
- 2019: Raw XML/PDF sources exist in the repository, but course metrics were not directly recoverable in this run, so JSON values remain null rather than guessed.
- 2021: Sprint place/map name set to Vilnius Old Town; course metrics remain null where not directly verified.

Relay metrics for 2017, 2018, 2019 and 2021 remain null unless already enriched elsewhere, because the exposed relay result sources did not show reliable course distance/climb/control rows in this run.
