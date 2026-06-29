window.Eyoc = window.Eyoc || {};
Eyoc.views = Eyoc.views || {};

// All-time medal table: gold/silver/bronze counts per country across individual and
// relay events combined (each row is one event result, so a relay medal counts once for
// the team, same as one individual result counts once for that athlete - no double
// counting either way). Ranked the standard medal-table way: most gold first, silver and
// bronze only as tiebreakers, not folded into a single "total" sort.
Eyoc.views.medals = function () {
  const editionYears = [...Eyoc.lib.editionYears()].sort((a, b) => a - b);

  return {
    years: editionYears,
    fromYear: editionYears[0],
    toYear: editionYears[editionYears.length - 1],
    fromOpen: false,
    toOpen: false,

    init() {
      // Keep the range from inverting if the user picks a "from" after the current "to"
      // (or vice versa) - clamp the other end to match instead of silently no-op'ing.
      this.$watch("fromYear", (year) => {
        if (year > this.toYear) this.toYear = year;
      });
      this.$watch("toYear", (year) => {
        if (year < this.fromYear) this.fromYear = year;
      });
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
