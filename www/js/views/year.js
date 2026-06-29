window.Eyoc = window.Eyoc || {};
Eyoc.views = Eyoc.views || {};

// disciplines/classes are validated against the known lists rather than trusted
// outright - params comes straight from the URL query string (e.g. a "Class" link from
// the athlete search page linking to #/year/2024?discipline=long&class=W16 to land
// directly on that result table), so a stale or hand-edited URL shouldn't be able to
// leave the view in a state selectClass()/the discipline tabs could never produce.
Eyoc.views.year = function (yearParam, params = {}) {
  const disciplines = ["sprint", "long", "relay"];
  const classes = ["M16", "M18", "W16", "W18"];
  return {
    year: Number(yearParam),
    discipline: disciplines.includes(params.discipline) ? params.discipline : "long",
    classes,
    ...Eyoc.lib.tableState("rank"),
    classFilter: classes.includes(params.class) ? params.class : "",
    // Set when arriving via a "Class" link from the athlete search page - highlights
    // that specific competitor/leg runner's row so it's easy to spot in a long table.
    highlightName: params.name || "",

    init() {
      // The wrapping x-if only swaps this component out when route.name changes, not
      // when route.params.year changes (e.g. navigating year 2024 -> 2025 directly) -
      // watch the param explicitly so the view updates in place.
      this.$watch("route.params.year", (year) => {
        this.year = Number(year);
      });
    },

    get meta() {
      return Eyoc.store.events[String(this.year)] || {};
    },

    get logoUrl() {
      return this.meta.has_logo ? `assets/logos/eyoc-${this.year}.png` : null;
    },

    get hasAnyResults() {
      return (
        Eyoc.store.individual.some((r) => r.year === this.year) ||
        Eyoc.store.relay.some((r) => r.year === this.year)
      );
    },

    get categoryMeta() {
      const disc = this.meta[this.discipline];
      return disc && disc.categories ? disc.categories : {};
    },

    // No class selected yet -> show no results table at all; the user picks a category
    // box first (see selectClass below).
    get rows() {
      if (!this.classFilter) return [];
      const source = this.discipline === "relay" ? Eyoc.store.relay : Eyoc.store.individual;
      const rows = source.filter(
        (r) => r.year === this.year && r.discipline === this.discipline && r.class === this.classFilter
      );
      return Eyoc.lib.sortRows(rows, this.sortKey, this.sortDir);
    },

    // Clicking the already-selected category box deselects it (back to no results).
    selectClass(cls) {
      this.classFilter = this.classFilter === cls ? "" : cls;
    },


    // "4.8km, 410m, 11 controls" - skips any null/missing field instead of leaving a
    // stray separator, and deliberately omits field_size (shown elsewhere already).
    courseSummary(cls) {
      const meta = this.categoryMeta[cls];
      if (!meta) return "";
      const parts = [];
      if (meta.distance_km != null) parts.push(`${meta.distance_km}km`);
      if (meta.elevation_m != null) parts.push(`${meta.elevation_m}m`);
      if (meta.control_points != null) parts.push(`${meta.control_points} controls`);
      return parts.join(", ");
    },
  };
};
