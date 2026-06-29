window.Eyoc = window.Eyoc || {};
Eyoc.views = Eyoc.views || {};

// Name-string matching only - there's no athlete ID in the source data, so this can
// both miss and over-match where spelling drifted across years (see
// results/raw/QUALITY-CHECK.md).
//
// The input is an autocomplete: `query` drives only the lightweight suggestion dropdown
// (cheap - see Eyoc.lib.athleteNameSuggestions), while the actual result tables are
// driven by `chosenName`, which only changes when a suggestion is clicked or the form is
// submitted. That split is what keeps typing fast: individualMatches/relayMatches (full
// substring scans of the dataset) no longer re-run on every keystroke, only once per
// search.
Eyoc.views.athlete = function (initialQuery) {
  return {
    query: initialQuery || "",
    chosenName: initialQuery || "",
    suggestionsOpen: false,

    init() {
      // Same in-place-update concern as the year view: route.params.q can change
      // without route.name changing (searching again from this same page).
      this.$watch("route.params.q", (q) => {
        this.query = q || "";
        this.chosenName = q || "";
        this.suggestionsOpen = false;
      });
    },

    get normalizedChosen() {
      return this.chosenName.trim().toLowerCase();
    },

    get suggestions() {
      const q = this.query.trim().toLowerCase();
      if (!q) return [];
      return Eyoc.lib.athleteNameSuggestions(q, 8);
    },

    // Bound to both the input's focus and input events (see index.html) - not just
    // focus. suggestionsOpen gets set false by several things that don't blur the field
    // (submitSearch, selectSuggestion, Escape), so if it were only reopened on focus, a
    // user who keeps typing the next search right after one of those - without ever
    // clicking away and back - would see the dropdown silently stay closed even though
    // matching suggestions exist.
    openSuggestions() {
      this.suggestionsOpen = true;
    },

    closeSuggestions() {
      this.suggestionsOpen = false;
    },

    selectSuggestion(entry) {
      this.query = entry.name;
      this.chosenName = entry.name;
      this.suggestionsOpen = false;
      location.hash = `#/athlete?q=${encodeURIComponent(entry.name)}`;
    },

    yearsLabel(entry) {
      return Eyoc.lib.athleteYearsLabel(entry);
    },

    // field (the race's full field size) feeds the "1/104"-style rank display, the
    // medal/podium icon and the first-half bolding in the template.
    get individualMatches() {
      const q = this.normalizedChosen;
      if (!q) return [];
      const fieldSizes = Eyoc.lib.allFieldSizes();
      return Eyoc.store.individual
        .filter((r) => r.name && r.name.toLowerCase().includes(q))
        .map((r) => ({ ...r, field: Eyoc.lib.fieldSizeFor(fieldSizes, r) }))
        .sort((a, b) => b.year - a.year);
    },

    // Same field-size attachment as individualMatches above, for the same rank/field
    // display, medal/podium icon and first-half bolding in the relay results table.
    get relayMatches() {
      const q = this.normalizedChosen;
      if (!q) return [];
      const fieldSizes = Eyoc.lib.allFieldSizes();
      return Eyoc.store.relay
        .filter((r) =>
          [r.leg1_name, r.leg2_name, r.leg3_name].some(
            (n) => n && n.toLowerCase().includes(q)
          )
        )
        .map((r) => ({ ...r, field: Eyoc.lib.fieldSizeFor(fieldSizes, r) }))
        .sort((a, b) => b.year - a.year);
    },

    // All three leg runners (skipping any leg with no recorded name), each flagged with
    // whether it's the one that matched the search - feeds the Runners column, which
    // shows the whole team's lineup rather than just the matched name.
    legRunners(row) {
      const q = this.normalizedChosen;
      return [row.leg1_name, row.leg2_name, row.leg3_name]
        .map((name) => (name ? { name, matched: name.toLowerCase().includes(q) } : null))
        .filter(Boolean);
    },

    // The one leg runner that actually matched the search - feeds the Class link's
    // "name" query param, so the year page can highlight that specific runner's row.
    matchedRunnerName(row) {
      const match = this.legRunners(row).find((r) => r.matched);
      return match ? match.name : "";
    },

    submitSearch() {
      const q = this.query.trim();
      this.chosenName = q;
      this.suggestionsOpen = false;
      location.hash = q ? `#/athlete?q=${encodeURIComponent(q)}` : "#/athlete";
    },
  };
};
