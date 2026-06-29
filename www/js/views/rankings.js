window.Eyoc = window.Eyoc || {};
Eyoc.views = Eyoc.views || {};

// Each country's single best-ever placing for the selected discipline/category - "best"
// is by percentile (rank/field*100) so fields of different sizes across 2002-2026 are
// comparable, but the table itself is listed alphabetically by country code (then by
// rank), like a reference table rather than a leaderboard. A country has more than one
// row only if it has an exact tie for its own best percentile (e.g. two different
// years/athletes at the identical placing).
//
// "All" on either filter removes that restriction rather than picking one value: All
// discipline compares a country's best sprint/long/relay result against each other;
// All category compares M16/M18/W16/W18 against each other (Men/Women narrow to one sex).
Eyoc.views.rankings = function () {
  return {
    disciplineFilter: "long",
    categoryFilter: "M18",
    page: 1,
    pageSize: 20,
    disciplines: ["all", "sprint", "long", "relay"],
    categories: ["all", "M", "W", "M16", "M18", "W16", "W18"],

    init() {
      this.$watch("disciplineFilter", () => (this.page = 1));
      this.$watch("categoryFilter", () => (this.page = 1));
    },

    disciplineLabel(key) {
      return key === "all" ? "All" : key.charAt(0).toUpperCase() + key.slice(1);
    },

    categoryLabel(key) {
      if (key === "all") return "All";
      if (key === "M") return "Men";
      if (key === "W") return "Women";
      return key;
    },

    matchesCategory(row) {
      if (this.categoryFilter === "all") return true;
      if (this.categoryFilter === "M" || this.categoryFilter === "W") return row.class.startsWith(this.categoryFilter);
      return row.class === this.categoryFilter;
    },

    // Sprint/long rows and relay rows have different shapes but share year/discipline/
    // class, so one combined field-size map (keyed by year|discipline|class) covers both.
    get fieldSizes() {
      return Eyoc.lib.fieldSizes([...Eyoc.store.individual, ...Eyoc.store.relay]);
    },

    get candidateRows() {
      let pool;
      if (this.disciplineFilter === "all") pool = [...Eyoc.store.individual, ...Eyoc.store.relay];
      else if (this.disciplineFilter === "relay") pool = Eyoc.store.relay;
      else pool = Eyoc.store.individual.filter((r) => r.discipline === this.disciplineFilter);
      return pool.filter((r) => r.status === "OK" && r.rank !== null && this.matchesCategory(r));
    },

    // One entry per country: its best percentile for the current filters, plus every
    // row that ties that best (usually just one). Relay rows get displayName/timeSeconds
    // aliases so the template doesn't need to branch between individual and relay shapes.
    get countryBestRows() {
      const withPercentile = this.candidateRows
        .map((r) => {
          const field = Eyoc.lib.fieldSizeFor(this.fieldSizes, r);
          if (!field) return null;
          const isRelay = r.discipline === "relay";
          return {
            ...r,
            field,
            percentile: (r.rank / field) * 100,
            isRelay,
            displayName: isRelay ? r.team : r.name,
            timeSeconds: isRelay ? r.total_time_seconds : r.time_seconds,
          };
        })
        .filter(Boolean);

      const bestByCountry = new Map();
      for (const row of withPercentile) {
        const best = bestByCountry.get(row.country);
        if (best === undefined || row.percentile < best) bestByCountry.set(row.country, row.percentile);
      }

      const result = withPercentile.filter((row) => Math.abs(row.percentile - bestByCountry.get(row.country)) < 1e-9);
      result.sort((a, b) => a.country.localeCompare(b.country) || a.rank - b.rank);
      return result;
    },

    get totalPages() {
      return Math.max(1, Math.ceil(this.countryBestRows.length / this.pageSize));
    },

    get rows() {
      const start = (this.page - 1) * this.pageSize;
      return this.countryBestRows.slice(start, start + this.pageSize);
    },

    rowNumber(indexOnPage) {
      return (this.page - 1) * this.pageSize + indexOnPage + 1;
    },

    goToPage(p) {
      this.page = Math.min(Math.max(1, p), this.totalPages);
    },

    formatTime(seconds) {
      return Eyoc.lib.formatTime(seconds);
    },
  };
};
