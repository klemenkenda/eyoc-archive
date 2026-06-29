window.Eyoc = window.Eyoc || {};
Eyoc.views = Eyoc.views || {};

Eyoc.views.home = function () {
  return {
    searchQuery: "",
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

    countryName(code) {
      return Eyoc.store.countryName(code);
    },

    logoUrl(meta) {
      return meta && meta.has_logo ? `assets/logos/eyoc-${meta.year}.png` : null;
    },

    submitSearch() {
      const q = this.searchQuery.trim();
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
