window.Eyoc = window.Eyoc || {};
Eyoc.views = Eyoc.views || {};

// All-time medal table: gold/silver/bronze counts per country across individual and
// relay events combined (each row is one event result, so a relay medal counts once for
// the team, same as one individual result counts once for that athlete - no double
// counting either way). Ranked the standard medal-table way: most gold first, silver and
// bronze only as tiebreakers, not folded into a single "total" sort.
Eyoc.views.medals = function (params = {}) {
  const editionYears = [...Eyoc.lib.editionYears()].sort((a, b) => a - b);
  const minYear = editionYears[0];
  const maxYear = editionYears[editionYears.length - 1];
  // ?from=&to= from the URL, same validate-against-the-known-list pattern as year.js's
  // discipline/class params - falls back to the full range if missing or bogus, so a
  // stale/hand-edited URL can't put the view in an impossible state.
  const initialFrom = editionYears.includes(Number(params.from)) ? Number(params.from) : minYear;
  const initialTo = editionYears.includes(Number(params.to)) ? Number(params.to) : maxYear;

  return {
    years: editionYears,
    fromYear: initialFrom,
    toYear: initialTo,
    fromOpen: false,
    toOpen: false,

    init() {
      // Keep the range from inverting if the user picks a "from" after the current "to"
      // (or vice versa) - clamp the other end to match instead of silently no-op'ing.
      // Also keeps the URL in sync with whatever range is selected (replaceState, not
      // location.hash, so this doesn't fire a hashchange/scroll-to-top/pageview-log on
      // every year pick) - that's what makes any chosen range, not just "Last edition",
      // a shareable link.
      this.$watch("fromYear", (year) => {
        if (year > this.toYear) this.toYear = year;
        this.syncUrl();
      });
      this.$watch("toYear", (year) => {
        if (year < this.fromYear) this.fromYear = year;
        this.syncUrl();
      });
    },

    syncUrl() {
      history.replaceState(null, "", `#/medals?from=${this.fromYear}&to=${this.toYear}`);
    },

    // Same dropdown-list pattern as the "Jump to a country" picker on the home page
    // (Eyoc.views.home's countryOpen/openCountryDropdown/selectCountry), just without
    // the text-filtering since there are only ~25 years to choose from.
    selectFromYear(year) {
      this.fromYear = year;
      this.fromOpen = false;
    },

    selectToYear(year) {
      this.toYear = year;
      this.toOpen = false;
    },

    selectLastEdition() {
      this.fromYear = maxYear;
      this.toYear = maxYear;
    },

    // One entry per country with at least one medal or podium finish in range, sorted
    // gold -> silver -> bronze -> podium -> country name (the last only to keep ties
    // deterministic). "Podium" is rank 4-6 - the same range Eyoc.lib.rankIconClass shows
    // the podium icon for elsewhere, just tallied per country instead of per row.
    get countryMedals() {
      const counts = new Map();
      const tally = (row) => {
        if (row.status !== "OK" || row.rank === null || row.rank > 6) return;
        if (row.year < this.fromYear || row.year > this.toYear) return;
        const entry = counts.get(row.country) || { code: row.country, gold: 0, silver: 0, bronze: 0, podium: 0 };
        if (row.rank === 1) entry.gold++;
        else if (row.rank === 2) entry.silver++;
        else if (row.rank === 3) entry.bronze++;
        else entry.podium++;
        counts.set(row.country, entry);
      };
      Eyoc.store.individual.forEach(tally);
      Eyoc.store.relay.forEach(tally);

      return [...counts.values()]
        .map((entry) => ({ ...entry, total: entry.gold + entry.silver + entry.bronze, name: Eyoc.store.countryName(entry.code) }))
        .sort(
          (a, b) =>
            b.gold - a.gold || b.silver - a.silver || b.bronze - a.bronze || b.podium - a.podium || a.name.localeCompare(b.name)
        );
    },
  };
};
