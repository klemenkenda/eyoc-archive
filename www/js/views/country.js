window.Eyoc = window.Eyoc || {};
Eyoc.views = Eyoc.views || {};

// Generalizes ../../analysis/eyoc_slo_progression.md and eyoc_slo_percentile_progression.md
// (originally one-off Slovenia reports) to any country, computed live from the in-memory
// dataset instead of being a static report.
Eyoc.views.country = function (code) {
  return {
    code,
    sexFilter: "all", // 'all' | 'M' | 'W'
    chart: null,

    init() {
      this.renderChart();
      // Same in-place-update concern as the year view: route.params.code can change
      // without route.name changing (jumping country -> country via links).
      this.$watch("route.params.code", (code) => {
        this.code = code;
        this.sexFilter = "all";
        this.$nextTick(() => this.renderChart());
      });
    },

    get name() {
      return Eyoc.store.countryName(this.code);
    },

    get individualRows() {
      return Eyoc.store.individual.filter((r) => r.country === this.code);
    },

    get relayRows() {
      return Eyoc.store.relay.filter((r) => r.country === this.code);
    },

    get yearsParticipated() {
      const years = new Set();
      this.individualRows.forEach((r) => years.add(r.year));
      this.relayRows.forEach((r) => years.add(r.year));
      return [...years].sort((a, b) => a - b);
    },

    get rankedRows() {
      let rows = this.individualRows.filter((r) => r.rank !== null && r.status === "OK");
      if (this.sexFilter !== "all") rows = rows.filter((r) => r.class.startsWith(this.sexFilter));
      return rows;
    },

    get fieldSizes() {
      return Eyoc.lib.fieldSizes(Eyoc.store.individual);
    },

    get bestChain() {
      return Eyoc.lib.bestPlaceProgression(this.rankedRows, this.fieldSizes);
    },

    get percentileChain() {
      return Eyoc.lib.percentileProgression(this.rankedRows, this.fieldSizes);
    },

    setSexFilter(filter) {
      this.sexFilter = filter;
      this.$nextTick(() => this.renderChart());
    },

    renderChart() {
      const canvas = this.$refs.chart;
      const steps = this.percentileChain.map((s) => ({
        year: s.row.year,
        percentile: Math.round(s.percentile * 10) / 10,
        label: `${s.row.name} — ${s.row.year} ${s.row.discipline} ${s.row.class} (${s.row.rank}/${s.field})`,
      }));
      this.chart = Eyoc.lib.renderPercentileChart(canvas, steps, this.chart);
    },

    formatTime(seconds) {
      return Eyoc.lib.formatTime(seconds);
    },
  };
};
