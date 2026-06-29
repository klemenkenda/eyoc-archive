// Loads + caches the static JSON dataset built by scripts/build_www_data.py.
// Registered as the Alpine.store('eyoc') in app.js. Plain global script (no bundler).
window.Eyoc = window.Eyoc || {};

// Mirrors results/EYOC-COUNTRIES.md - the EYOC-eligible federation whitelist.
Eyoc.COUNTRY_NAMES = {
  AUT: "Austria", AZE: "Azerbaijan", BEL: "Belgium", BLR: "Belarus", BUL: "Bulgaria",
  CRO: "Croatia", CYP: "Cyprus", CZE: "Czechia", DEN: "Denmark", ESP: "Spain",
  EST: "Estonia", FIN: "Finland", FRA: "France", GBR: "UK", GER: "Germany",
  HUN: "Hungary", IRL: "Ireland", ISR: "Israel", ITA: "Italy", LAT: "Latvia",
  LIE: "Liechtenstein", LTU: "Lithuania", LUX: "Luxembourg", MDA: "Moldavia",
  MKD: "Macedonia", MNE: "Montenegro", NED: "Netherlands", NOR: "Norway", POL: "Poland",
  POR: "Portugal", ROU: "Romania", RUS: "Russia", SLO: "Slovenia", SRB: "Serbia",
  SUI: "Switzerland", SVK: "Slovakia", SWE: "Sweden", TUR: "Türkiye", UKR: "Ukraine",
};

Eyoc.store = {
  loaded: false,
  error: null,
  individual: [],
  relay: [],
  events: {},
  manifest: {},
  countries: Eyoc.COUNTRY_NAMES,

  async init() {
    if (this.loaded || this._loading) return;
    this._loading = true;
    try {
      const [individual, relay, events, manifest] = await Promise.all([
        fetch("data/individual.json").then((r) => r.json()),
        fetch("data/relay.json").then((r) => r.json()),
        fetch("data/events.json").then((r) => r.json()),
        fetch("data/manifest.json").then((r) => r.json()),
      ]);
      this.individual = individual;
      this.relay = relay;
      this.events = events;
      this.manifest = manifest;
      this.loaded = true;
    } catch (err) {
      this.error = String(err);
    } finally {
      this._loading = false;
    }
  },

  yearsSorted() {
    return Object.keys(this.events).map(Number).sort((a, b) => a - b);
  },

  countryName(code) {
    return this.countries[code] || code;
  },

  // Country codes that actually appear in the data, sorted by name.
  countriesWithResults() {
    const codes = new Set();
    for (const row of this.individual) codes.add(row.country);
    for (const row of this.relay) codes.add(row.country);
    return [...codes].filter(Boolean).sort((a, b) =>
      this.countryName(a).localeCompare(this.countryName(b))
    );
  },
};
