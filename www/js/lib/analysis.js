// Country-record progression analysis, generalized from the one-off Slovenia reports in
// ../../analysis/eyoc_slo_progression.md and eyoc_slo_percentile_progression.md.
// Shared by the country and rankings views.
window.Eyoc = window.Eyoc || {};
Eyoc.lib = Eyoc.lib || {};

// "Field" for a given year/discipline/class = every row in that group, ranked or not
// (DNF/DSQ/DNS competitors still started). Matches the field_size counts elsewhere in
// the dataset without depending on metadata.json (which is incomplete for some years).
Eyoc.lib.fieldSizes = function (individualRows) {
  const sizes = new Map();
  for (const row of individualRows) {
    const key = `${row.year}|${row.discipline}|${row.class}`;
    sizes.set(key, (sizes.get(key) || 0) + 1);
  }
  return sizes;
};

// Eyoc.store.individual/relay never change after the initial fetch, so the field-size
// map (and the leader lookup below) only need to be built once per page load rather
// than on every call site that needs them.
let _fieldSizesCache = null;
Eyoc.lib.allFieldSizes = function () {
  if (!_fieldSizesCache) {
    _fieldSizesCache = Eyoc.lib.fieldSizes([...Eyoc.store.individual, ...Eyoc.store.relay]);
  }
  return _fieldSizesCache;
};

Eyoc.lib.fieldSizeFor = function (fieldSizes, row) {
  return fieldSizes.get(`${row.year}|${row.discipline}|${row.class}`) || null;
};

// Years with at least one actual result - distinguishes a year nobody from a given
// country attended from a year with no edition at all (2020 was postponed to 2022 and
// has a placeholder entry in events.json but zero result rows), so the country-page
// timeline can tell "didn't attend" apart from "nothing to attend".
let _editionYearsCache = null;
Eyoc.lib.editionYears = function () {
  if (!_editionYearsCache) {
    const years = new Set();
    for (const r of Eyoc.store.individual) years.add(r.year);
    for (const r of Eyoc.store.relay) years.add(r.year);
    _editionYearsCache = years;
  }
  return _editionYearsCache;
};

// One entry per distinct athlete/leg-runner name (individual rows + the three relay leg
// names) - {name, lower, country, minYear, maxYear}. Pre-lowercased once and built
// lazily, cached like allFieldSizes above - this is what makes the athlete-search
// autocomplete fast: without it, every keystroke would re-run .toLowerCase() (a fresh
// string allocation) on every one of the ~18k rows in the dataset, which is the actual
// cost that made typing feel slow, not the substring check itself. country/minYear/
// maxYear feed the suggestion dropdown's flag + "years active" label; a name is assumed
// to belong to one country (the one from its first-seen row) - this can be wrong for the
// rare case of a genuine name collision across countries, same caveat as the substring
// matching itself (see results/raw/QUALITY-CHECK.md).
let _athleteNameIndex = null;
function athleteNameIndex() {
  if (_athleteNameIndex) return _athleteNameIndex;
  const byLower = new Map();
  const add = (name, row) => {
    if (!name) return;
    const lower = name.toLowerCase();
    const entry = byLower.get(lower);
    if (!entry) {
      byLower.set(lower, { name, lower, country: row.country, minYear: row.year, maxYear: row.year });
    } else {
      if (row.year < entry.minYear) entry.minYear = row.year;
      if (row.year > entry.maxYear) entry.maxYear = row.year;
    }
  };
  for (const r of Eyoc.store.individual) add(r.name, r);
  for (const r of Eyoc.store.relay) {
    add(r.leg1_name, r);
    add(r.leg2_name, r);
    add(r.leg3_name, r);
  }
  _athleteNameIndex = [...byLower.values()];
  return _athleteNameIndex;
}

// Up to `limit` entries whose name contains `query` (already lowercased) - stops
// scanning as soon as it has enough, so a query matching early entries doesn't pay for
// the rest of the index.
Eyoc.lib.athleteNameSuggestions = function (query, limit) {
  const out = [];
  for (const entry of athleteNameIndex()) {
    if (entry.lower.includes(query)) {
      out.push(entry);
      if (out.length >= limit) break;
    }
  }
  return out;
};

// "2012" for a one-year career so far, "2012-2015" otherwise.
Eyoc.lib.athleteYearsLabel = function (entry) {
  return entry.minYear === entry.maxYear ? `${entry.minYear}` : `${entry.minYear}-${entry.maxYear}`;
};

// A country can run both Sprint and Long in the same year, so the source rows aren't
// one-per-year. Collapse to a single best-of-year candidate first (matching the
// Slovenia reports' behavior) - otherwise a same-year-but-worse race that happens to
// sort before that year's best would itself show up as a spurious "improvement" the
// instant before being immediately superseded.
function bestOfYear(rows, fieldSizes, metric) {
  const perYear = new Map();
  for (const row of rows) {
    const field = Eyoc.lib.fieldSizeFor(fieldSizes, row);
    if (!field) continue;
    const candidate = { row, field, metric: metric(row, field) };
    const current = perYear.get(row.year);
    if (!current || candidate.metric < current.metric) perYear.set(row.year, candidate);
  }
  return [...perYear.values()].sort((a, b) => a.row.year - b.row.year);
}

// rows: ranked (rank != null) individual results for one country, any order.
// Returns the chain of best-so-far steps in chronological order, one candidate per
// year. A year only enters the chain if its best result improves on the previous best:
// lower rank wins; if rank ties, the result from the larger field is treated as better.
Eyoc.lib.bestPlaceProgression = function (rows, fieldSizes) {
  const candidates = bestOfYear(rows, fieldSizes, (row) => row.rank);
  const chain = [];
  let best = null;
  for (const candidate of candidates) {
    const better =
      !best ||
      candidate.row.rank < best.row.rank ||
      (candidate.row.rank === best.row.rank && candidate.field > best.field);
    if (better) {
      best = candidate;
      chain.push({ row: candidate.row, field: candidate.field, percentile: (candidate.row.rank / candidate.field) * 100 });
    }
  }
  return chain;
};

// Same idea but the metric being improved is percentile (rank/field*100), so a smaller
// field with a proportionally better placing can still count as an improvement, unlike
// the absolute version above.
Eyoc.lib.percentileProgression = function (rows, fieldSizes) {
  const candidates = bestOfYear(rows, fieldSizes, (row, field) => (row.rank / field) * 100);
  const chain = [];
  let bestPercentile = Infinity;
  for (const candidate of candidates) {
    if (candidate.metric < bestPercentile) {
      bestPercentile = candidate.metric;
      chain.push({ row: candidate.row, field: candidate.field, percentile: candidate.metric });
    }
  }
  return chain;
};

// 0 is never a real orienteering time - some sources use it as a sentinel for "this
// runner didn't actually complete this leg/course" (e.g. a relay leg nobody ran because
// the team didn't start), so it's treated the same as missing/null everywhere here.
Eyoc.lib.formatTime = function (seconds) {
  if (!seconds) return "—";
  seconds = Math.round(seconds);
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  const mmss = `${String(m).padStart(h ? 2 : 1, "0")}:${String(s).padStart(2, "0")}`;
  return h ? `${h}:${mmss}` : mmss;
};

// A non-OK runner/team's recorded time (if any - e.g. a mispunch can still have a
// finish time) isn't a real result, so it's never shown - same rule as displayRank.
Eyoc.lib.formatResultTime = function (row, timeField) {
  if (row.status !== "OK") return "—";
  return Eyoc.lib.formatTime(row[timeField]);
};

// Gap to the race leader, as "+MM:SS" - "—" for the leader themselves or where either
// time is missing (DNF/DNS/no time recorded).
Eyoc.lib.formatDiff = function (rowSeconds, leaderSeconds) {
  if (!rowSeconds || !leaderSeconds) return "—"; // 0 is a sentinel for "no time", not a real time
  const diff = Math.round(rowSeconds - leaderSeconds);
  if (diff <= 0) return "—";
  const m = Math.floor(diff / 60);
  const s = diff % 60;
  return `+${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
};

// One-time index of each race's rank-1 row (year|class|discipline, "relay" standing in
// for discipline on relay rows), so diffToLeader is a Map lookup instead of a linear
// scan of the whole dataset per row - it's called once per visible table row.
let _leaderIndex = null;
function leaderIndex() {
  if (_leaderIndex) return _leaderIndex;
  _leaderIndex = new Map();
  for (const r of Eyoc.store.individual) {
    if (Eyoc.lib.effectiveRank(r) === 1) _leaderIndex.set(`${r.year}|${r.class}|${r.discipline}`, r);
  }
  for (const r of Eyoc.store.relay) {
    if (Eyoc.lib.effectiveRank(r) === 1) _leaderIndex.set(`${r.year}|${r.class}|relay`, r);
  }
  return _leaderIndex;
}

// Looks up the winning time of *that row's own race* (same year/discipline/class, or
// year/class for relay) anywhere in the full dataset - lets any table that lists results
// from mixed races (athlete search, rankings, country pages) show a Diff column too,
// not just same-race tables like the year browser.
Eyoc.lib.diffToLeader = function (row, isRelay) {
  if (row.status !== "OK") return "—"; // not a real result - same rule as formatResultTime
  const timeField = isRelay ? "total_time_seconds" : "time_seconds";
  const leader = leaderIndex().get(`${row.year}|${row.class}|${isRelay ? "relay" : row.discipline}`);
  return Eyoc.lib.formatDiff(row[timeField], leader ? leader[timeField] : null);
};

// Fastest leg1/2/3_time_seconds among every OK team in that same year+class - the
// reference point for each leg's own Diff. Only OK teams count, same rule as the leg
// times themselves not being shown for non-OK teams (see formatLegTime) - a team that
// didn't complete the relay isn't a trustworthy "best leg" reference either.
Eyoc.lib.bestLegTime = function (year, klass, legField) {
  let best = null;
  for (const r of Eyoc.store.relay) {
    if (r.year !== year || r.class !== klass || r.status !== "OK") continue;
    const t = r[legField];
    if (t && (best === null || t < best)) best = t; // 0 is "no time", never a real best
  }
  return best;
};

// A non-OK team's leg splits aren't shown even where the source has a recorded time for
// some legs - same rule as the team's overall time/diff (formatResultTime/diffToLeader).
Eyoc.lib.formatLegTime = function (row, legNumber) {
  if (row.status !== "OK") return "—";
  return Eyoc.lib.formatTime(row[`leg${legNumber}_time_seconds`]);
};

Eyoc.lib.legDiff = function (row, legNumber) {
  if (row.status !== "OK") return "—";
  const legField = `leg${legNumber}_time_seconds`;
  return Eyoc.lib.formatDiff(row[legField], Eyoc.lib.bestLegTime(row.year, row.class, legField));
};

// Identifies a team within one year+class for the Map keys below. Can't key by row
// object identity - Alpine/Vue's reactivity wraps array elements accessed through a
// reactive proxy in per-access proxies, so the `row` a template hands in is a different
// object identity than what a plain `Eyoc.store.relay.filter(...)` returns here, even
// though both wrap the same underlying data.
function teamKey(row) {
  return `${row.team}|${row.source_file}`;
}

// Cumulative standings after leg 1/2/3: for every OK team in that year+class with a
// complete run of leg times through legN, rank them by summed time-so-far. Only OK teams
// with a full set of leg times through that point are eligible - same rule as
// bestLegTime, an incomplete or non-OK team isn't a trustworthy position to show or to
// compare anyone else against.
Eyoc.lib.legPositions = function (year, klass) {
  const positions = { 1: new Map(), 2: new Map(), 3: new Map() };
  const teams = Eyoc.store.relay.filter((r) => r.year === year && r.class === klass && r.status === "OK");
  for (let n = 1; n <= 3; n++) {
    const standings = [];
    for (const team of teams) {
      let sum = 0;
      let complete = true;
      for (let i = 1; i <= n; i++) {
        const t = team[`leg${i}_time_seconds`];
        if (!t) {
          complete = false;
          break;
        }
        sum += t;
      }
      if (complete) standings.push({ key: teamKey(team), sum });
    }
    standings.sort((a, b) => a.sum - b.sum);
    standings.forEach((entry, index) => positions[n].set(entry.key, index + 1));
  }
  return positions;
};

// Team's standing immediately after this leg - "(3)" meaning 3rd place at that point.
Eyoc.lib.legPosition = function (row, legNumber) {
  if (row.status !== "OK") return null;
  return Eyoc.lib.legPositions(row.year, row.class)[legNumber].get(teamKey(row)) ?? null;
};

// Places gained (positive) or lost (negative) on this leg vs. the position after the
// previous leg - only meaningful for legs 2 and 3 (leg 1 has no previous leg to compare).
Eyoc.lib.legPositionChange = function (row, legNumber) {
  if (row.status !== "OK" || legNumber < 2) return null;
  const positions = Eyoc.lib.legPositions(row.year, row.class);
  const key = teamKey(row);
  const current = positions[legNumber].get(key);
  const previous = positions[legNumber - 1].get(key);
  if (current == null || previous == null) return null;
  return previous - current;
};

Eyoc.lib.legPositionChangeText = function (row, legNumber) {
  const delta = Eyoc.lib.legPositionChange(row, legNumber);
  if (!delta) return "";
  return delta > 0 ? `-${delta}` : `+${Math.abs(delta)}`;
};

Eyoc.lib.legPositionChangeClass = function (row, legNumber) {
  const delta = Eyoc.lib.legPositionChange(row, legNumber);
  if (!delta) return "";
  return delta > 0 ? "place-gain" : "place-loss";
};
