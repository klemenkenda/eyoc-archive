window.Eyoc = window.Eyoc || {};
Eyoc.views = Eyoc.views || {};

Eyoc.views.home = function () {
  return {
    query: "",
    suggestionsOpen: false,
    countryCode: "",
    countryQuery: "",
    countryOpen: false,

    get years() {
      return Eyoc.store
        .yearsSorted()
        .slice()
        .reverse()
        .map((year) => ({ year, meta: Eyoc.store.events[String(year)] }));
    },

    get countries() {
      return Eyoc.store.countriesWithResults();
    },

    get filteredCountries() {
      const q = this.countryQuery.trim().toLowerCase();
      if (!q) return this.countries;
      return this.countries.filter(
        (c) => this.countryName(c).toLowerCase().includes(q) || c.toLowerCase().includes(q)
      );
    },

    get totalYears() {
      return Eyoc.store.yearsSorted().length;
    },

    get totalResults() {
      return Eyoc.store.individual.length + Eyoc.store.relay.length;
    },

    get totalCountries() {
      return Eyoc.store.countriesWithResults().length;
    },

    get suggestions() {
      const q = this.query.trim().toLowerCase();
      if (!q) return [];
      return Eyoc.lib.athleteNameSuggestions(q, 8);
    },

    countryName(code) {
      return Eyoc.store.countryName(code);
    },

    logoUrl(meta) {
      return meta && meta.has_logo ? `assets/logos/eyoc-${meta.year}.png` : null;
    },

    yearsLabel(entry) {
      return Eyoc.lib.athleteYearsLabel(entry);
    },

    openSuggestions() {
      this.suggestionsOpen = true;
    },

    closeSuggestions() {
      this.suggestionsOpen = false;
    },

    selectSuggestion(entry) {
      this.query = entry.name;
      this.suggestionsOpen = false;
      location.hash = `#/athlete?q=${encodeURIComponent(entry.name)}`;
    },

    submitSearch() {
      const q = this.query.trim();
      this.suggestionsOpen = false;
      if (q) location.hash = `#/athlete?q=${encodeURIComponent(q)}`;
    },

    goToCountry() {
      if (this.countryCode) location.hash = `#/country/${this.countryCode}`;
    },

    countryLabel(code) {
      return `${this.countryName(code)} (${code})`;
    },

    openCountryDropdown() {
      this.countryOpen = true;
      this.countryQuery = "";
    },

    closeCountryDropdown() {
      this.countryOpen = false;
      this.countryQuery = this.countryCode ? this.countryLabel(this.countryCode) : "";
    },

    selectCountry(code) {
      this.countryCode = code;
      this.countryQuery = this.countryLabel(code);
      this.countryOpen = false;
      this.goToCountry();
    },
  };
};
