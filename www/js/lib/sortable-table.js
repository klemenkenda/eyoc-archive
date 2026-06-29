// Small generic sort/filter helper shared by the year/athlete/country/rankings views.
window.Eyoc = window.Eyoc || {};
Eyoc.lib = Eyoc.lib || {};

// A non-OK row (DNF/DNS/DSQ/MP) is never genuinely ranked, even where the source file
// happened to print a sequential number on it - treat it as unranked everywhere.
Eyoc.lib.effectiveRank = function (row) {
  return row.status === "OK" ? row.rank : null;
};

// Non-OK rows show their status (DNF/DSQ/DNS/MP) in place of a rank, instead of a
// separate Status column - there's no rank to show, but the reason is more useful than
// a bare dash.
Eyoc.lib.displayRank = function (row) {
  if (row.status !== "OK") return row.status;
  return row.rank === null || row.rank === undefined ? "—" : row.rank;
};

Eyoc.lib.sortRows = function (rows, key, dir) {
  const sign = dir === "desc" ? -1 : 1;
  const valueOf = key === "rank" ? Eyoc.lib.effectiveRank : (row) => row[key];
  return [...rows].sort((a, b) => {
    let av = valueOf(a);
    let bv = valueOf(b);
    const aMissing = av === null || av === undefined || av === "";
    const bMissing = bv === null || bv === undefined || bv === "";
    if (aMissing && bMissing) return 0;
    if (aMissing) return 1; // unranked (incl. non-OK) always sorts last regardless of direction
    if (bMissing) return -1;
    if (typeof av === "string" || typeof bv === "string") {
      return sign * String(av).localeCompare(String(bv));
    }
    return sign * (av - bv);
  });
};

// Mixin object: spread into a view's x-data to get class-filter + sort state for one table.
// usage: Object.assign(viewData, Eyoc.lib.tableState('rank'))
Eyoc.lib.tableState = function (defaultSortKey) {
  return {
    classFilter: "",
    sortKey: defaultSortKey,
    sortDir: "asc",
    sortBy(key) {
      if (this.sortKey === key) {
        this.sortDir = this.sortDir === "asc" ? "desc" : "asc";
      } else {
        this.sortKey = key;
        this.sortDir = "asc";
      }
    },
    sortIndicator(key) {
      if (this.sortKey !== key) return "";
      return this.sortDir === "asc" ? "▲" : "▼";
    },
  };
};
