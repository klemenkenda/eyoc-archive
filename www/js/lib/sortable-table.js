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

// "1/104" (rank/field size) for a ranked OK row, the bare status (DNF/DSQ/DNS/MP)
// otherwise - field is optional so callers without a field-size lookup handy still get
// a plain rank number rather than nothing.
Eyoc.lib.displayRankWithField = function (row, field) {
  if (row.status !== "OK") return row.status;
  if (row.rank === null || row.rank === undefined) return "—";
  return field ? `${row.rank}/${field}` : `${row.rank}`;
};

// CSS class for the small rank icon: gold/silver/bronze medal for the top 3, a podium
// icon for 4th-6th, nothing beyond that or for a non-OK/unranked row.
Eyoc.lib.rankIconClass = function (row) {
  if (row.status !== "OK" || row.rank === null || row.rank === undefined) return "";
  if (row.rank === 1) return "rank-icon-gold";
  if (row.rank === 2) return "rank-icon-silver";
  if (row.rank === 3) return "rank-icon-bronze";
  if (row.rank <= 6) return "rank-icon-podium";
  return "";
};

// True for an OK, ranked result finishing in the top half of its field - used to bold
// such results so a strong placing stands out even in a long results list.
Eyoc.lib.isFirstHalf = function (row, field) {
  return row.status === "OK" && row.rank !== null && row.rank !== undefined && !!field && row.rank <= field / 2;
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
