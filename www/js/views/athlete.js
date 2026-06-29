window.Eyoc = window.Eyoc || {};
Eyoc.views = Eyoc.views || {};

// Name-string matching only - there's no athlete ID in the source data, so this can
// both miss and over-match where spelling drifted across years (see
// results/raw/QUALITY-CHECK.md).
Eyoc.views.athlete = function (initialQuery) {
  return {
    query: initialQuery || "",

    init() {
      // Same in-place-update concern as the year view: route.params.q can change
      // without route.name changing (searching again from this same page).
      this.$watch("route.params.q", (q) => {
        this.query = q || "";
      });
    },

    get normalizedQuery() {
      return this.query.trim().toLowerCase();
    },

    get individualMatches() {
      const q = this.normalizedQuery;
      if (!q) return [];
      return Eyoc.store.individual
        .filter((r) => r.name && r.name.toLowerCase().includes(q))
        .sort((a, b) => b.year - a.year);
    },

    get relayMatches() {
      const q = this.normalizedQuery;
      if (!q) return [];
      return Eyoc.store.relay
        .filter((r) =>
          [r.leg1_name, r.leg2_name, r.leg3_name].some(
            (n) => n && n.toLowerCase().includes(q)
          )
        )
        .sort((a, b) => b.year - a.year);
    },

    matchedLegName(row) {
      const q = this.normalizedQuery;
      const legs = [row.leg1_name, row.leg2_name, row.leg3_name];
      return legs.find((n) => n && n.toLowerCase().includes(q)) || "";
    },

    submitSearch() {
      const q = this.query.trim();
      location.hash = q ? `#/athlete?q=${encodeURIComponent(q)}` : "#/athlete";
    },
  };
};
