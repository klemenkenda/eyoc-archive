window.Eyoc = window.Eyoc || {};
Eyoc.views = Eyoc.views || {};

// Generalizes ../../analysis/eyoc_slo_progression.md and eyoc_slo_percentile_progression.md
// (originally one-off Slovenia reports) to any country, computed live from the in-memory
// dataset instead of being a static report.
Eyoc.views.country = function (code) {
  // Deliberately not part of the returned x-data object: Alpine recursively wraps any
  // object assigned to a reactive property in a Proxy, and Chart.js instances are full
  // of internal circular references (chart <-> canvas <-> controller back-references) -
  // proxying that graph blows the call stack the moment Chart.js touches its own
  // internals (e.g. on .update()). Keeping it in this closure instead of `this.chart`
  // sidesteps Alpine's reactivity entirely, which is fine since nothing in the template
  // reads it directly.
  let chart = null;

  return {
    code,
    view: "results", // 'results' | 'progression'
    resultsDiscipline: "all",
    resultsCategory: "all",
    resultsPage: 1,
    resultsPageSize: 50,
    disciplines: ["all", "sprint", "long", "relay"],
    categories: ["all", "M", "W", "M16", "M18", "W16", "W18"],

    init() {
      // Deliberately no eager renderChart() call here: the chart's <canvas> lives behind
      // x-if="view === 'progression'" and view starts as 'results', so the canvas doesn't
      // exist yet at init() time. Alpine's $refs proxy is cached on first access per
      // element - touching $refs.chart before the canvas ever mounts permanently caches
      // an empty lookup, so the chart could never render even once the canvas appears
      // later. Only ever access $refs.chart (via renderChart) once the progression tab -
      // and therefore the canvas - is actually in the DOM.
      this.$watch("route.params.code", (code) => {
        this.code = code;
        this.view = "results";
        this.resultsDiscipline = "all";
        this.resultsCategory = "all";
        this.resultsPage = 1;
      });
      this.$watch("resultsDiscipline", () => {
        this.resultsPage = 1;
        if (this.view === "progression") this.$nextTick(() => this.renderChart());
      });
      this.$watch("resultsCategory", () => {
        this.resultsPage = 1;
        if (this.view === "progression") this.$nextTick(() => this.renderChart());
      });
      this.$watch("view", (view) => {
        if (view === "progression") {
          this.$nextTick(() => this.renderChart());
        } else if (chart) {
          // x-if removes the canvas the instant view stops being 'progression', but
          // nothing else would destroy the Chart.js instance until the next
          // renderChart() call - in the meantime its resize observer keeps watching the
          // now-detached canvas and throws asynchronously.
          chart.destroy();
          chart = null;
        }
      });
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

    // Every EYOC edition year (2002-2026), each tagged with this country's attendance,
    // for the timeline strip - a row of dots reads at a glance far better than a
    // "2002-2019, 2021-2026"-style range list, especially once there are several gaps.
    get timeline() {
      const participated = new Set(this.yearsParticipated);
      const editionYears = Eyoc.lib.editionYears();
      return Eyoc.store.yearsSorted().map((year) => ({
        year,
        state: participated.has(year) ? "participated" : editionYears.has(year) ? "absent" : "no-edition",
      }));
    },

    timelineTitle(entry) {
      if (entry.state === "participated") return `${entry.year}: competed`;
      if (entry.state === "no-edition") return `${entry.year}: no edition held`;
      return `${entry.year}: did not compete`;
    },

    highlightName(row) {
      if (row.discipline !== "relay") return row.name || "";
      return [row.leg1_name, row.leg2_name, row.leg3_name].find(Boolean) || "";
    },

    resultsLink(row) {
      return `#/year/${row.year}?discipline=${row.discipline}&class=${row.class}&name=${encodeURIComponent(this.highlightName(row))}`;
    },

    get bestChain() {
      return Eyoc.lib.bestPlaceProgression(this.resultsCandidateRows, this.resultsFieldSizes);
    },

    get percentileChain() {
      return Eyoc.lib.percentileProgression(this.resultsCandidateRows, this.resultsFieldSizes);
    },

    renderChart() {
      const canvas = this.$refs.chart;
      const steps = this.percentileChain.map((s) => {
        const isRelay = s.row.discipline === "relay";
        return {
          year: s.row.year,
          percentile: Math.round(s.percentile * 10) / 10,
          label: `${isRelay ? s.row.team : s.row.name} — ${s.row.year} ${s.row.discipline} ${s.row.class} (${s.row.rank}/${s.field})`,
        };
      });
      chart = Eyoc.lib.renderPercentileChart(canvas, steps, chart);
    },

    matchesResultsCategory(row) {
      if (this.resultsCategory === "all") return true;
      if (this.resultsCategory === "M" || this.resultsCategory === "W") return row.class.startsWith(this.resultsCategory);
      return row.class === this.resultsCategory;
    },

    get resultsCandidateRows() {
      let pool;
      if (this.resultsDiscipline === "all") pool = [...this.individualRows, ...this.relayRows];
      else if (this.resultsDiscipline === "relay") pool = this.relayRows;
      else pool = this.individualRows.filter((r) => r.discipline === this.resultsDiscipline);
      return pool.filter((r) => r.status === "OK" && r.rank !== null && this.matchesResultsCategory(r));
    },

    // Field sizes (rank/field, for percentile) come from the full dataset, not just this
    // country's rows - a field of 100 stays 100 regardless of how many of those 100 are
    // from this country. Cached by Eyoc.lib since the underlying rows never change after
    // the initial fetch.
    get resultsFieldSizes() {
      return Eyoc.lib.allFieldSizes();
    },

    // Every matching result for this country, ordered by percentile ascending (best first).
    get resultsAllRows() {
      const fieldSizes = this.resultsFieldSizes;
      return this.resultsCandidateRows
        .map((r) => {
          const field = Eyoc.lib.fieldSizeFor(fieldSizes, r);
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
        .filter(Boolean)
        .sort((a, b) => a.percentile - b.percentile);
    },

    get resultsTotalPages() {
      return Math.max(1, Math.ceil(this.resultsAllRows.length / this.resultsPageSize));
    },

    get resultsRows() {
      const start = (this.resultsPage - 1) * this.resultsPageSize;
      return this.resultsAllRows.slice(start, start + this.resultsPageSize);
    },

    resultsRowNumber(indexOnPage) {
      return (this.resultsPage - 1) * this.resultsPageSize + indexOnPage + 1;
    },

    goToResultsPage(p) {
      this.resultsPage = Math.min(Math.max(1, p), this.resultsTotalPages);
    },

    formatTime(seconds) {
      return Eyoc.lib.formatTime(seconds);
    },
  };
};
