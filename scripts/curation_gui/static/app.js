const DISCIPLINES = ["sprint", "long", "relay"];
const CLASSES = ["M16", "M18", "W16", "W18"];
const CATEGORY_FIELDS = [
  { key: "distance_km", label: "Distance (km)", type: "number", step: "0.1" },
  { key: "elevation_m", label: "Climb (m)", type: "number", step: "1" },
  { key: "control_points", label: "Controls", type: "number", step: "1" },
  { key: "field_size", label: "Field size", type: "number", step: "1" },
];
const COLUMN_LABELS = {
  class: "Class", rank: "Rank", status: "Status", bib: "Bib", country: "Country",
  name: "Name", time_seconds: "Time", time: "Time", confidence: "Conf.", source_file: "Source",
  discipline: "Discipline",
  team: "Team", total_time_seconds: "Total", total_time: "Total",
  leg1_name: "Leg 1", leg1_time_seconds: "Leg 1", leg1_time: "Leg 1",
  leg2_name: "Leg 2", leg2_time_seconds: "Leg 2", leg2_time: "Leg 2",
  leg3_name: "Leg 3", leg3_time_seconds: "Leg 3", leg3_time: "Leg 3",
};
// CSV pane: these columns aren't shown at all (still round-tripped on save).
const HIDDEN_CSV_COLUMNS = ["source_file"];
// CSV pane: columns rendered narrower than the default (short text/codes).
const NARROW_CSV_COLUMNS = ["bib", "confidence"];
// CSV pane: columns rendered narrower still - fixed-format codes with almost no
// variation in length (rank is 1-3 digits, status/country are short enums/codes) -
// so name/team get the space they actually need.
const XNARROW_CSV_COLUMNS = ["class", "rank", "status", "country"];
const TIME_COLUMNS = [
  "time_seconds", "total_time_seconds",
  "leg1_time_seconds", "leg2_time_seconds", "leg3_time_seconds",
];
// CSV pane: display column order per discipline (independent of the CSV's on-disk
// column order, which write_csv/COLUMNS controls and is unaffected by this).
const CSV_DISPLAY_ORDER = {
  sprint: ["class", "rank", "name", "country", "time_seconds", "status", "bib", "confidence"],
  long: ["class", "rank", "name", "country", "time_seconds", "status", "bib", "confidence"],
  relay: [
    "class", "rank", "team", "country", "total_time_seconds", "status",
    "leg1_name", "leg1_time_seconds", "leg2_name", "leg2_time_seconds", "leg3_name", "leg3_time_seconds",
    "confidence",
  ],
};

function orderedCsvColumns(discipline, columns) {
  const visible = columns.filter((c) => !HIDDEN_CSV_COLUMNS.includes(c));
  const order = (CSV_DISPLAY_ORDER[discipline] || visible).filter((c) => visible.includes(c));
  const extra = visible.filter((c) => !order.includes(c));
  return [...order, ...extra];
}

// seconds (int, or float with 1 decimal = tenths, see common.time_to_seconds) ->
// "(H:)MM:SS(.T)" - the hour and tenths parts are only shown when non-zero.
function secondsToHms(val) {
  if (val === "" || val === null || val === undefined) return "";
  const num = typeof val === "number" ? val : parseFloat(val);
  if (Number.isNaN(num)) return val.toString();
  const sign = num < 0 ? "-" : "";
  const totalTenths = Math.round(Math.abs(num) * 10);
  const tenths = totalTenths % 10;
  const totalSeconds = Math.floor(totalTenths / 10);
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = totalSeconds % 60;
  const pad = (n) => n.toString().padStart(2, "0");
  const hPart = h > 0 ? `${h}:` : "";
  const tPart = tenths > 0 ? `.${tenths}` : "";
  return `${sign}${hPart}${pad(m)}:${pad(s)}${tPart}`;
}

// "(H:)MM:SS(.T)" (also tolerates plain "SS") -> seconds, for editing round-trip.
// Also parses the raw lazarus.elte.hu (2002-2013) "MM.SS,d" / "MM.SS" convention -
// the dot there separates minutes/seconds, not tenths - mirrors
// common.time_to_seconds() so raw-source times from that era compare correctly
// instead of every row misreading as a tenths-of-a-second value. Unambiguous vs. our
// own "(H:)MM:SS(.T)" display format because that one always has a colon; this one
// never does.
function hmsToSeconds(text) {
  if (text === null || text === undefined) return "";
  const t = text.toString().trim();
  if (t === "") return "";
  if (!t.includes(":")) {
    let m = t.match(/^(\d+)\.(\d{2}),(\d+)$/);
    if (m) {
      const [, mins, secs, frac] = m;
      const base = Number(mins) * 60 + Number(secs);
      const fracVal = Number(frac) / 10 ** frac.length;
      return fracVal ? Math.round((base + fracVal) * 10) / 10 : base;
    }
    m = t.match(/^(\d+)\.(\d{2})$/);
    if (m) return Number(m[1]) * 60 + Number(m[2]);
  }
  const dotIdx = t.lastIndexOf(".");
  let mainPart = t;
  let tenths = 0;
  if (dotIdx !== -1) {
    mainPart = t.slice(0, dotIdx);
    const frac = t.slice(dotIdx + 1);
    if (frac === "" || Number.isNaN(Number(frac))) return text;
    tenths = Math.round(Number(`0.${frac}`) * 10) / 10;
  }
  const parts = mainPart.split(":").map((p) => p.trim());
  if (parts.some((p) => p !== "" && Number.isNaN(Number(p)))) return text;
  let h = 0, m = 0, s = 0;
  if (parts.length === 3) [h, m, s] = parts.map(Number);
  else if (parts.length === 2) [m, s] = parts.map(Number);
  else if (parts.length === 1) [s] = parts.map(Number);
  else return text;
  const total = h * 3600 + m * 60 + s + tenths;
  return Math.round(total * 10) / 10;
}

function escapeHtml(s) {
  return (s ?? "").toString()
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

// Same resolution common.normalize_country uses (bare code, or a known alias/name),
// plus its two "leading mention, junk trails after" shortcuts - lazarus-era HTML
// (2002-2013) glues a redundant bib/heat/seed-group suffix onto the country, e.g.
// "POL 1 D" or "Switzerland SUI13 D" (see resolve_name_and_country in
// parse_lazarus_html.py) - without these, every row in years that do this fails to
// resolve as EYOC-eligible and the CSV-vs-source check misfires on the entire file.
// Still missing common.normalize_country()'s PDF-OCR truncation heuristics - good
// enough to flag for review, not a byte-for-byte port.
function resolveEyocCode(text) {
  if (!text) return null;
  const t = text.toString().trim();
  if (!t) return null;
  if (state.countryCodes.has(t.toUpperCase())) return t.toUpperCase();
  const alias = state.countryAliases[t.toLowerCase()];
  if (alias) return alias;

  // "POL 1 D" - a bare 3-letter code (written upper-case, same as the source) as the
  // first word, with anything trailing after it.
  const lead = t.split(/\s+/)[0];
  if (lead.length === 3 && lead === lead.toUpperCase() && state.countryCodes.has(lead)) {
    return lead;
  }
  // "Switzerland SUI13 D" - a known country name as a leading prefix, then junk.
  const lower = t.toLowerCase();
  for (const aliasKey of state.countryAliasKeysByLengthDesc) {
    if (aliasKey.length >= 4 && lower.startsWith(aliasKey + " ")) {
      return state.countryAliases[aliasKey];
    }
  }
  return null;
}

function isEyocCountry(text) {
  return resolveEyocCode(text) !== null;
}

const state = {
  year: null,
  discipline: "sprint",
  yearData: null,   // full /api/year/<year> response
  rows: [],         // working copy of rows for the active discipline
  countryCodes: new Set(),   // EYOC-eligible 3-letter codes
  countryAliases: {},        // lowercase name/code -> canonical EYOC code
  countryAliasKeysByLengthDesc: [],  // Object.keys(countryAliases), longest first
  timeColMode: {},           // time column key -> "hms" (default) | "seconds"
  rawSourceData: null,       // last successfully parsed /api/raw-xml or /api/raw-lazarus response, or null
  rawViewMode: "table",      // "table" (parsed) | "original" (iframe) - only relevant when rawSourceData is set
  xmlCheckIssues: [],        // last checkCsvAgainstSource() result
};

const $ = (sel) => document.querySelector(sel);

async function api(path, opts) {
  const res = await fetch(path, opts);
  if (!res.ok) throw new Error(`${path}: HTTP ${res.status}`);
  return res.json();
}

function toast(message, isError) {
  const el = $("#toast");
  el.textContent = message;
  el.classList.toggle("error", !!isError);
  el.classList.remove("hidden");
  clearTimeout(toast._t);
  toast._t = setTimeout(() => el.classList.add("hidden"), 3500);
}

// ---------- Year / discipline selection ----------

async function init() {
  const [years, codes, aliases] = await Promise.all([
    api("/api/years"),
    api("/api/country-codes"),
    api("/api/country-aliases"),
  ]);
  state.countryCodes = new Set(codes.map(([code]) => code));
  state.countryAliases = aliases;
  state.countryAliasKeysByLengthDesc = Object.keys(aliases).sort((a, b) => b.length - a.length);

  const codeList = $("#countryCodes");
  codeList.innerHTML = codes.map(([code, name]) => `<option value="${code}">${name}</option>`).join("");

  const sel = $("#yearSelect");
  sel.innerHTML = years.map((y) => `<option value="${y.year}">${y.year}</option>`).join("");
  sel.value = years[years.length - 1].year;
  sel.addEventListener("change", () => loadYear(parseInt(sel.value, 10)));

  document.querySelectorAll("#disciplineTabs .tab").forEach((btn) => {
    btn.addEventListener("click", () => selectDiscipline(btn.dataset.discipline));
  });

  $("#lockToggle").addEventListener("click", toggleLock);
  $("#rawFileSelect").addEventListener("change", updateRawFrame);
  $("#rawViewToggle").addEventListener("click", () => {
    setRawViewMode(state.rawViewMode === "table" ? "original" : "table");
  });
  $("#addRowBtn").addEventListener("click", addRow);
  $("#saveCsvBtn").addEventListener("click", saveCsv);
  $("#saveMetadataBtn").addEventListener("click", saveMetadata);
  $("#rebuildBtn").addEventListener("click", rebuild);
  $("#xmlCheckBtn").addEventListener("click", toggleXmlCheckPanel);
  $("#xmlCheckCloseBtn").addEventListener("click", () => $("#xmlCheckPanel").classList.add("hidden"));

  await loadYear(parseInt(sel.value, 10));
}

async function loadYear(year) {
  state.year = year;
  state.yearData = await api(`/api/year/${year}`);
  renderRawFileOptions();
  selectDiscipline(state.discipline, true);
  renderMetadata();
}

function selectDiscipline(discipline, force) {
  if (state.discipline === discipline && !force) return;
  state.discipline = discipline;
  document.querySelectorAll("#disciplineTabs .tab").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.discipline === discipline);
  });
  const d = state.yearData.disciplines[discipline];
  state.rows = (d.rows || []).map((r) => ({ ...r }));
  renderRawFileOptions();
  renderLockUI();
  renderCsvTable();
}

// ---------- Raw source pane ----------

function renderRawFileOptions() {
  const d = state.yearData.disciplines[state.discipline];
  const referenced = d.referencedRawFiles || [];
  const all = state.yearData.rawFiles || [];
  const ordered = [...referenced, ...all.filter((f) => !referenced.includes(f))];

  const sel = $("#rawFileSelect");
  if (ordered.length === 0) {
    sel.innerHTML = `<option value="">(no raw files found)</option>`;
  } else {
    sel.innerHTML = ordered.map((f) => `<option value="${f}">${f}${referenced.includes(f) ? "  ★" : ""}</option>`).join("");
  }
  updateRawFrame();
}

// Which /api/raw-* endpoint (if any) can turn this raw file into a structured table -
// XML sources are parsed exactly (one format); .htm/.html is tried as a lazarus
// combined-year page (the only HTML source format with a table parser), and simply
// fails gracefully (falls back to the iframe) for the other, differently-shaped HTML
// files in results/raw/ (2006 ozs_*/eyoc2006com_*, 2024's Eventor export copies).
function rawTableEndpoint(file) {
  const lower = file.toLowerCase();
  if (lower.endsWith(".xml")) return "raw-xml";
  if (lower.endsWith(".htm") || lower.endsWith(".html")) return "raw-lazarus";
  return null;
}

// Shows either the parsed table or the original raw file in an iframe, without
// re-fetching - the table's already-rendered HTML (including check highlighting)
// just gets hidden/shown, so toggling back and forth is instant.
function setRawViewMode(mode) {
  state.rawViewMode = mode;
  const frame = $("#rawFrame");
  const wrap = $("#rawXmlWrap");
  const toggle = $("#rawViewToggle");
  const file = $("#rawFileSelect").value;
  if (mode === "original") {
    wrap.classList.add("hidden");
    frame.classList.remove("hidden");
    frame.src = file ? `/api/raw/${file}` : "about:blank";
    toggle.textContent = "Show table";
  } else {
    frame.classList.add("hidden");
    wrap.classList.remove("hidden");
    toggle.textContent = "Show original";
  }
}

async function updateRawFrame() {
  const sel = $("#rawFileSelect");
  const wrap = $("#rawXmlWrap");
  const toggle = $("#rawViewToggle");
  const file = sel.value;
  state.rawSourceData = null;
  toggle.classList.add("hidden");

  const endpoint = file ? rawTableEndpoint(file) : null;
  if (endpoint) {
    wrap.innerHTML = `<p class="raw-loading">Parsing...</p>`;
    setRawViewMode("table");
    try {
      const data = await api(`/api/${endpoint}/${file}`);
      renderRawSourceTable(data, file);
      state.rawSourceData = data;
      toggle.classList.remove("hidden");
    } catch (e) {
      wrap.innerHTML = `<p class="raw-loading">Could not render as a table (${e.message}). ` +
        `<a href="/api/raw/${file}" target="_blank">Open raw file instead</a>.</p>`;
    }
    updateXmlCheckBadge();
    return;
  }

  setRawViewMode("original");
  updateXmlCheckBadge();
}

function renderRawSourceTable(data, file) {
  const wrap = $("#rawXmlWrap");
  if (data.error) {
    wrap.innerHTML = `<p class="raw-loading">${escapeHtml(data.error)} ` +
      `<a href="/api/raw/${file}" target="_blank">Open raw file instead</a>.</p>`;
    return;
  }
  const columns = data.columns;
  const nonEyoc = data.rows.filter((r) => !isEyocCountry(r.country)).length;
  const meta = `${data.rows.length} rows (raw values, unedited)` +
    (nonEyoc > 0 ? ` - <span class="raw-xml-meta-flag">${nonEyoc} highlighted as non-EYOC country</span>` : "");

  const thead = `<tr>${columns.map((c) => `<th>${COLUMN_LABELS[c] || c}</th>`).join("")}</tr>`;
  const tbody = data.rows.map((r) => {
    const rowClass = isEyocCountry(r.country) ? "" : " class=\"row-non-eyoc\"";
    return `<tr${rowClass}>${columns.map((c) => `<td>${escapeHtml(r[c])}</td>`).join("")}</tr>`;
  }).join("");

  wrap.innerHTML = `<div class="raw-xml-meta">${meta}</div>` +
    `<table id="rawXmlTable"><thead>${thead}</thead><tbody>${tbody}</tbody></table>`;
}

// ---------- Lock ----------

function renderLockUI() {
  const locked = state.yearData.disciplines[state.discipline].locked;
  $("#lockControl").classList.toggle("locked", locked);
  $("#lockToggle").textContent = locked ? "Unlock" : "Lock";
  $("#lockStatus").textContent = locked
    ? "Locked - rebuild will skip this file"
    : "Not locked";
  $("#unlockedWarning").classList.toggle("hidden", locked);
}

async function toggleLock() {
  const d = state.yearData.disciplines[state.discipline];
  const next = !d.locked;
  await api(`/api/year/${state.year}/${state.discipline}/lock`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ locked: next }),
  });
  d.locked = next;
  renderLockUI();
  toast(next ? "Locked. Rebuild will no longer touch this file." : "Unlocked.");
}

// ---------- CSV table ----------

function csvColClass(c) {
  if (XNARROW_CSV_COLUMNS.includes(c)) return "col-xnarrow";
  if (NARROW_CSV_COLUMNS.includes(c)) return "col-narrow";
  if (TIME_COLUMNS.includes(c)) return "col-time";
  return "";
}

function timeColMode(c) {
  return state.timeColMode[c] || "hms";
}

function toggleTimeColMode(c) {
  state.timeColMode[c] = timeColMode(c) === "hms" ? "seconds" : "hms";
  renderCsvTable();
}

function displayTimeValue(c, val) {
  return timeColMode(c) === "seconds" ? (val ?? "").toString() : secondsToHms(val);
}

function renderCsvTable() {
  const d = state.yearData.disciplines[state.discipline];
  const columns = orderedCsvColumns(state.discipline, d.columns);

  $("#rowCount").textContent = state.rows.length;

  const thead = $("#csvTable thead");
  thead.innerHTML = `<tr>${columns.map((c) => {
    const isTime = TIME_COLUMNS.includes(c);
    const label = COLUMN_LABELS[c] || c;
    if (!isTime) return `<th class="${csvColClass(c)}">${label}</th>`;
    const modeTag = timeColMode(c) === "seconds" ? " (s)" : "";
    return `<th class="${csvColClass(c)} col-time-header" data-col="${c}" ` +
      `title="Click to toggle seconds / (H:)MM:SS(.T)">${label}${modeTag}</th>`;
  }).join("")}<th></th></tr>`;
  thead.querySelectorAll("th.col-time-header").forEach((th) => {
    th.addEventListener("click", () => toggleTimeColMode(th.dataset.col));
  });

  const tbody = $("#csvTable tbody");
  tbody.innerHTML = "";
  state.rows.forEach((row, i) => {
    const tr = document.createElement("tr");
    tr.classList.toggle("row-non-eyoc", !isEyocCountry(row.country));
    tr.innerHTML = columns.map((c) => {
      const list = c === "country" ? ' list="countryCodes"' : "";
      const isTime = TIME_COLUMNS.includes(c);
      const display = isTime ? displayTimeValue(c, row[c]) : (row[c] ?? "").toString();
      const val = display.replace(/"/g, "&quot;");
      const title = isTime ? ' title="(H:)MM:SS(.T) - click the column header to show seconds instead"' : "";
      return `<td class="${csvColClass(c)}"><input data-row="${i}" data-col="${c}" value="${val}"${list}${title}></td>`;
    }).join("") + `<td><button class="btn btn-small btn-danger" data-del="${i}">✕</button></td>`;
    tbody.appendChild(tr);
  });

  tbody.querySelectorAll("input").forEach((input) => {
    const rowIdx = input.dataset.row;
    const col = input.dataset.col;
    const isTime = TIME_COLUMNS.includes(col);
    input.addEventListener("input", () => {
      if (isTime) {
        state.rows[rowIdx][col] = timeColMode(col) === "seconds" ? input.value : hmsToSeconds(input.value);
      } else {
        state.rows[rowIdx][col] = input.value;
      }
      if (col === "country") {
        input.closest("tr").classList.toggle("row-non-eyoc", !isEyocCountry(input.value));
      }
    });
    if (isTime) {
      input.addEventListener("blur", () => {
        input.value = displayTimeValue(col, state.rows[rowIdx][col]);
      });
    }
    input.addEventListener("blur", () => updateXmlCheckBadge());
  });
  tbody.querySelectorAll("[data-del]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.rows.splice(parseInt(btn.dataset.del, 10), 1);
      renderCsvTable();
    });
  });

  updateXmlCheckBadge();
}

// ---------- CSV vs XML check ----------

const KNOWN_CLASSES = ["M16", "M18", "W16", "W18"];

// Mirrors common.normalize_class closely enough to build a matching key between the
// CSV's normalized class and the XML source's raw class label - returns "" (unrecognised,
// same as Python's None) for anything that isn't one of the four EYOC classes or "Mixed".
function normalizeClassForCompare(raw) {
  if (!raw) return "";
  let t = raw.toString().trim().toUpperCase();
  if (t.startsWith("WOMEN") || t.startsWith("WOMAN")) t = "W" + t.slice(5);
  else if (t.startsWith("MEN")) t = "M" + t.slice(3);
  t = t.replace(/E+$/, "").replace(/\s+/g, "");
  if (KNOWN_CLASSES.includes(t)) return t;
  if (["MIX", "MIXT", "MIXED"].includes(t)) return "Mixed";
  return "";
}

// Buckets a raw IOF-XML status string into the same enum common.normalize_status
// produces, for comparison against the CSV's already-normalized status column.
function statusBucket(text) {
  if (!text) return "";
  const t = text.toString().trim().toLowerCase().replace(/[^a-z]/g, "");
  if (t === "ok") return "OK";
  if (t.includes("dsq") || t.includes("disq") || t.includes("disk")) return "DSQ";
  if (t.includes("dns") || t.includes("notcompeting")) return "DNS";
  if (t === "mp" || t.includes("missingpunch") || t.includes("mispunch")) return "MP";
  if (t.includes("dnf") || t.includes("overtime") || t.includes("cancelled") || t.includes("unknown")) return "DNF";
  return "";
}

// Mirrors common.to_latin() (strip accents so e.g. "Beneš"/"Benes" key the same) -
// needed because sources with no bib (lazarus HTML) can only be matched by name, and
// the CSV's name has already been through common.format_name()'s to_latin() step.
function foldAccents(text) {
  return (text ?? "").toString().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function individualKey(cls, row) {
  const bib = (row.bib ?? "").toString().trim();
  if (bib) return `${cls}|bib:${bib}`;
  return `${cls}|name:${foldAccents(row.name).trim().toLowerCase()}`;
}

function relayKey(cls, row) {
  const team = foldAccents(row.team).trim().toLowerCase();
  if (team) return `${cls}|team:${team}`;
  return `${cls}|country:${(row.country ?? "").toString().trim().toUpperCase()}`;
}

// Compares the curator's working CSV rows against the raw source (XML or lazarus
// HTML) and returns a list of {severity, class, subject, message, row|rows}
// discrepancies - `row` (or `rows`, for the rare ambiguous-match case) references the
// actual object(s) from `csvRows` so the CSV table can highlight exactly the affected
// line(s); an issue with neither (the "missing from CSV entirely" case) has no CSV
// row to point at. "error" = an EYOC-eligible source entry is missing from the CSV,
// or a matched runner's time disagrees - things that would make the published results
// wrong. "warning" = everything softer (CSV-only rows, status/country drift, ambiguous
// matches).
function checkCsvAgainstSource(discipline, csvRows, sourceData) {
  if (!sourceData || !sourceData.rows) return [];

  const isRelay = discipline === "relay";
  const xmlIsRelay = sourceData.columns.includes("team");
  if (xmlIsRelay !== isRelay) {
    return [{
      severity: "warning", class: "", subject: "",
      message: `Selected raw file looks like a ${xmlIsRelay ? "relay" : "individual"} results file - ` +
        `pick the matching source for the "${discipline}" tab to check against it.`,
    }];
  }

  const keyFor = (row) => {
    const cls = normalizeClassForCompare(row.class);
    if (!cls) return null;
    return isRelay ? relayKey(cls, row) : individualKey(cls, row);
  };
  const subjectFor = (row) => isRelay
    ? (row.team || row.country || "?")
    : `${row.name || "?"} (bib ${row.bib || "?"})`;

  // Only source rows that would actually survive run_all.py (EYOC country + a
  // recognised class) are expected to have a CSV counterpart.
  const xmlEligible = sourceData.rows
    .map((r) => ({ row: r, key: isEyocCountry(r.country) ? keyFor(r) : null }))
    .filter((e) => e.key);

  const xmlByKey = new Map();
  xmlEligible.forEach(({ row, key }) => {
    if (!xmlByKey.has(key)) xmlByKey.set(key, []);
    xmlByKey.get(key).push(row);
  });

  const csvByKey = new Map();
  const csvKeyed = csvRows.map((r) => ({ row: r, key: keyFor(r) })).filter((e) => e.key);
  csvKeyed.forEach(({ row, key }) => {
    if (!csvByKey.has(key)) csvByKey.set(key, []);
    csvByKey.get(key).push(row);
  });

  const issues = [];

  csvKeyed.forEach(({ row, key }) => {
    if (!xmlByKey.has(key)) {
      issues.push({
        severity: "warning", class: row.class, subject: subjectFor(row), row,
        message: "In CSV but no matching entry found in the raw source.",
      });
    }
  });

  xmlByKey.forEach((rows, key) => {
    if (!csvByKey.has(key)) {
      const row = rows[0];
      issues.push({
        severity: "error", class: normalizeClassForCompare(row.class), subject: subjectFor(row), sourceRow: row,
        message: "In the raw source (EYOC-eligible) but missing from the CSV.",
      });
    }
  });

  xmlByKey.forEach((xmlRows, key) => {
    const csvRows2 = csvByKey.get(key);
    if (!csvRows2) return;
    if (xmlRows.length > 1 || csvRows2.length > 1) {
      issues.push({
        severity: "warning", class: normalizeClassForCompare(xmlRows[0].class), subject: key,
        rows: csvRows2, sourceRows: xmlRows,
        message: "Multiple rows share the same match key (class + bib/team) - comparison skipped for these.",
      });
      return;
    }
    const xmlRow = xmlRows[0];
    const csvRow = csvRows2[0];
    const subject = subjectFor(csvRow);
    const cls = normalizeClassForCompare(csvRow.class);

    const csvTimeField = isRelay ? "total_time_seconds" : "time_seconds";
    const xmlTimeField = isRelay ? "total_time" : "time";
    const csvSeconds = csvRow[csvTimeField] === "" || csvRow[csvTimeField] == null ? null : Number(csvRow[csvTimeField]);
    const xmlParsed = hmsToSeconds(xmlRow[xmlTimeField]);
    const xmlSeconds = xmlParsed === "" ? null : Number(xmlParsed);
    if (csvSeconds !== null && xmlSeconds !== null) {
      if (Math.abs(csvSeconds - xmlSeconds) > 0.05) {
        issues.push({
          severity: "error", class: cls, subject, row: csvRow, sourceRow: xmlRow,
          message: `Time mismatch: CSV ${secondsToHms(csvSeconds)} vs source ${secondsToHms(xmlSeconds)}.`,
        });
      }
    } else if ((csvSeconds !== null) !== (xmlSeconds !== null)) {
      issues.push({
        severity: "warning", class: cls, subject, row: csvRow, sourceRow: xmlRow,
        message: `Time present in only one source (CSV: ${csvSeconds !== null ? secondsToHms(csvSeconds) : "-"}, ` +
          `XML: ${xmlSeconds !== null ? secondsToHms(xmlSeconds) : "-"}).`,
      });
    }

    const csvStatus = (csvRow.status || "").toString().trim().toUpperCase();
    const xmlStatus = statusBucket(xmlRow.status);
    if (csvStatus && xmlStatus && csvStatus !== xmlStatus) {
      issues.push({
        severity: "warning", class: cls, subject, row: csvRow, sourceRow: xmlRow,
        message: `Status mismatch: CSV "${csvStatus}" vs source "${xmlRow.status}" (~${xmlStatus}).`,
      });
    }

    if (!isRelay) {
      const csvCountry = (csvRow.country || "").toString().trim().toUpperCase();
      const xmlCountry = resolveEyocCode(xmlRow.country);
      if (csvCountry && xmlCountry && csvCountry !== xmlCountry) {
        issues.push({
          severity: "warning", class: cls, subject, row: csvRow, sourceRow: xmlRow,
          message: `Country mismatch: CSV "${csvCountry}" vs source "${xmlRow.country}" (resolves to ${xmlCountry}).`,
        });
      }
    }
  });

  return issues;
}

// The rows an issue points at, whether it recorded one (`row`) or several (`rows`).
function issueRows(issue) {
  return issue.rows || (issue.row ? [issue.row] : []);
}

// Same, but for the raw-source-side row(s) an issue points at (`sourceRow`/`sourceRows`).
function issueSourceRows(issue) {
  return issue.sourceRows || (issue.sourceRow ? [issue.sourceRow] : []);
}

function buildSeverityMap(issues, getRows) {
  const map = new Map();
  issues.forEach((issue) => {
    getRows(issue).forEach((row) => {
      if (map.get(row) === "error") return;
      if (issue.severity === "error") map.set(row, "error");
      else if (!map.has(row)) map.set(row, "warning");
    });
  });
  return map;
}

// Recomputes state.xmlCheckIssues plus row -> "error"|"warning" severity maps (the
// worst severity of any issue touching that row) for both the CSV and raw-source
// tables, so both can be highlighted.
function computeXmlCheck() {
  let sourceData = state.rawSourceData;
  if (sourceData && sourceData.rows.some((r) => r.discipline)) {
    // A lazarus HTML page covers both sprint and long in one file - only compare
    // against the slice that actually corresponds to the currently open CSV tab.
    sourceData = { ...sourceData, rows: sourceData.rows.filter((r) => r.discipline === state.discipline) };
  }
  state.xmlCheckIssues = checkCsvAgainstSource(state.discipline, state.rows, sourceData);
  state.xmlCheckRowSeverity = buildSeverityMap(state.xmlCheckIssues, issueRows);
  state.xmlCheckSourceRowSeverity = buildSeverityMap(state.xmlCheckIssues, issueSourceRows);
}

// Applies row-check-error/warning classes + a tooltip to the *existing* table <tr>
// elements (matched to `rows` by position) - no table rebuild needed, so this is
// cheap enough to call after every edit without disturbing input focus.
function applyRowHighlighting(tableSelector, rows, severityMap, getIssueRows) {
  const tbody = $(`${tableSelector} tbody`);
  if (!tbody) return;
  Array.from(tbody.children).forEach((tr, i) => {
    const row = rows[i];
    if (!row) return;
    const sev = severityMap.get(row);
    tr.classList.toggle("row-check-error", sev === "error");
    tr.classList.toggle("row-check-warning", sev === "warning");
    const messages = state.xmlCheckIssues.filter((iss) => getIssueRows(iss).includes(row)).map((iss) => iss.message);
    if (messages.length) tr.title = messages.join("\n");
    else tr.removeAttribute("title");
  });
}

function applyXmlCheckRowHighlighting() {
  applyRowHighlighting("#csvTable", state.rows, state.xmlCheckRowSeverity, issueRows);
  if (state.rawSourceData) {
    applyRowHighlighting("#rawXmlTable", state.rawSourceData.rows, state.xmlCheckSourceRowSeverity, issueSourceRows);
  }
}

function updateXmlCheckBadge() {
  computeXmlCheck();
  const btn = $("#xmlCheckBtn");
  if (btn) {
    const errors = state.xmlCheckIssues.filter((i) => i.severity === "error").length;
    const warnings = state.xmlCheckIssues.filter((i) => i.severity === "warning").length;
    const total = errors + warnings;
    if (!state.rawSourceData) {
      // Nothing to compare against yet - stay neutral rather than falsely reading "all clear".
      btn.classList.remove("has-errors", "all-clear");
      btn.textContent = "⚠ –";
      btn.title = "Select an XML or lazarus-HTML raw source file (left pane) to check the CSV against it";
    } else {
      btn.classList.toggle("has-errors", errors > 0);
      btn.classList.toggle("all-clear", errors === 0);
      btn.textContent = `⚠ ${total}`;
      btn.title = `${errors} error(s), ${warnings} warning(s) vs the raw source - click for details`;
    }
  }

  applyXmlCheckRowHighlighting();
  if (!$("#xmlCheckPanel").classList.contains("hidden")) renderXmlCheckPanel();
}

function renderXmlCheckPanel() {
  const listEl = $("#xmlCheckList");
  const summaryEl = $("#xmlCheckSummary");
  const issues = state.xmlCheckIssues;

  if (!state.rawSourceData) {
    summaryEl.textContent = "Select an XML or lazarus-HTML raw source file (left pane) to check the CSV against it.";
    listEl.innerHTML = "";
    return;
  }
  const errors = issues.filter((i) => i.severity === "error").length;
  const warnings = issues.filter((i) => i.severity === "warning").length;
  summaryEl.textContent = issues.length === 0
    ? "No discrepancies found between the CSV and the raw source."
    : `${errors} error(s), ${warnings} warning(s)`;

  listEl.innerHTML = issues.map((i, idx) =>
    `<div class="xml-check-row sev-${i.severity}"${issueRows(i).length ? ` data-issue="${idx}"` : ""}>` +
    `<span class="xml-check-class">${escapeHtml(i.class || "")}</span>` +
    `<span class="xml-check-subject">${escapeHtml(i.subject || "")}</span>` +
    `<span>${escapeHtml(i.message)}</span></div>`
  ).join("");

  listEl.querySelectorAll("[data-issue]").forEach((el) => {
    el.addEventListener("click", () => scrollToCsvRow(issues[parseInt(el.dataset.issue, 10)]));
  });
}

// Jumps the CSV pane to the first row an issue points at and briefly flashes it,
// so clicking an entry in the check panel is a fast way to find the row to fix.
function scrollToCsvRow(issue) {
  const rows = issueRows(issue);
  if (!rows.length) return;
  const idx = state.rows.indexOf(rows[0]);
  if (idx === -1) return;
  const tr = $("#csvTable tbody").children[idx];
  if (!tr) return;
  tr.scrollIntoView({ block: "center" });
  tr.classList.add("row-flash");
  setTimeout(() => tr.classList.remove("row-flash"), 1200);
}

function toggleXmlCheckPanel() {
  const panel = $("#xmlCheckPanel");
  panel.classList.toggle("hidden");
  if (!panel.classList.contains("hidden")) renderXmlCheckPanel();
}

function addRow() {
  const columns = state.yearData.disciplines[state.discipline].columns;
  const blank = {};
  columns.forEach((c) => (blank[c] = ""));
  state.rows.push(blank);
  renderCsvTable();
}

async function saveCsv() {
  try {
    const res = await api(`/api/year/${state.year}/${state.discipline}/csv`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rows: state.rows }),
    });
    state.yearData.disciplines[state.discipline].rows = state.rows.map((r) => ({ ...r }));
    toast(`Saved ${res.rowCount} rows.`);
  } catch (e) {
    toast(`Save failed: ${e.message}`, true);
  }
}

// ---------- Metadata ----------

function getPath(obj, path) {
  return path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), obj);
}

function setPath(obj, path, value) {
  const keys = path.split(".");
  let o = obj;
  for (let i = 0; i < keys.length - 1; i++) o = o[keys[i]];
  o[keys[keys.length - 1]] = value;
}

function sanitizeMetadata(meta) {
  if (!meta || typeof meta !== "object") return meta;
  for (const discipline of DISCIPLINES) {
    const block = meta[discipline];
    if (!block || typeof block !== "object" || !block.categories) continue;
    for (const cls of Object.keys(block.categories)) {
      const cat = block.categories[cls];
      if (!cat || typeof cat !== "object") continue;
      delete cat.place;
      delete cat.map_name;
    }
  }
  return meta;
}

function blankMetadata(year) {
  const disciplineBlock = () => ({
    place: null,
    map_name: null,
    categories: Object.fromEntries(CLASSES.map((cls) => [cls, {
      distance_km: null, elevation_m: null, control_points: null, field_size: null,
    }])),
  });
  return {
    schema_version: "2.0-simple",
    year,
    title: "",
    city: "",
    country: "",
    date: "",
    start_date: null,
    end_date: null,
    long: disciplineBlock(),
    sprint: disciplineBlock(),
    relay: disciplineBlock(),
  };
}

function renderMetadata() {
  const form = $("#metadataForm");
  let meta = state.yearData.metadata;
  if (!meta) {
    form.innerHTML = `<p>No metadata.json for this year yet.</p><button id="createMetaBtn" class="btn btn-primary">Create metadata.json</button>`;
    $("#createMetaBtn").addEventListener("click", () => {
      state.yearData.metadata = blankMetadata(state.year);
      renderMetadata();
    });
    return;
  }

  meta = sanitizeMetadata(meta);
  state.yearData.metadata = meta;

  const topField = (path, label) =>
    `<label>${label}<input data-path="${path}" value="${(getPath(meta, path) ?? "").toString().replace(/"/g, "&quot;")}"></label>`;

  let html = `<div class="meta-top">
    ${topField("title", "Title")}
    ${topField("city", "City")}
    ${topField("country", "Country")}
    ${topField("date", "Date (display text)")}
    ${topField("start_date", "Start date (YYYY-MM-DD)")}
    ${topField("end_date", "End date (YYYY-MM-DD)")}
  </div>`;

  for (const discipline of DISCIPLINES) {
    const block = meta[discipline] || {};
    html += `<div class="meta-discipline">
      <h3>${discipline[0].toUpperCase()}${discipline.slice(1)}</h3>
      <div class="meta-discipline-place">
        ${topField(`${discipline}.place`, "Overall place")}
        ${topField(`${discipline}.map_name`, "Overall map name")}
      </div>
      <div class="meta-categories">`;
    for (const cls of CLASSES) {
      html += `<div class="meta-category"><h4>${cls}</h4>`;
      for (const f of CATEGORY_FIELDS) {
        const path = `${discipline}.categories.${cls}.${f.key}`;
        const raw = getPath(meta, path);
        const val = raw === null || raw === undefined ? "" : raw;
        html += `<div class="meta-field"><label>${f.label}</label><input data-path="${path}" type="${f.type}" ${f.step ? `step="${f.step}"` : ""} value="${val}"></div>`;
      }
      html += `</div>`;
    }
    html += `</div></div>`;
  }

  form.innerHTML = html;
}

async function saveMetadata() {
  const meta = state.yearData.metadata;
  if (!meta) return;

  sanitizeMetadata(meta);

  document.querySelectorAll("#metadataForm [data-path]").forEach((input) => {
    let value = input.value;
    if (input.type === "number") {
      value = value === "" ? null : parseFloat(value);
    } else if (value === "" && input.dataset.path.endsWith("_date")) {
      value = null;
    }
    setPath(meta, input.dataset.path, value);
  });

  try {
    await api(`/api/year/${state.year}/metadata`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(meta),
    });
    toast("Metadata saved.");
  } catch (e) {
    toast(`Save failed: ${e.message}`, true);
  }
}

// ---------- Rebuild ----------

async function rebuild() {
  if (!confirm("Rebuild all results/<year>/*.csv from raw sources? Locked files are skipped; everything else is regenerated.")) return;
  const btn = $("#rebuildBtn");
  const log = $("#rebuildLog");
  btn.disabled = true;
  btn.textContent = "Rebuilding...";
  log.classList.remove("hidden");
  log.textContent = "Running scripts/parsers/run_all.py ...\n";
  try {
    const res = await api("/api/rebuild", { method: "POST" });
    log.textContent = res.stdout + (res.stderr ? `\n--- stderr ---\n${res.stderr}` : "");
    toast(res.ok ? "Rebuild complete." : "Rebuild finished with errors - see log.", !res.ok);
    await loadYear(state.year);
  } catch (e) {
    log.textContent += `\nRequest failed: ${e.message}`;
    toast("Rebuild request failed.", true);
  } finally {
    btn.disabled = false;
    btn.textContent = "Rebuild from raw";
  }
}

init().catch((e) => toast(`Init failed: ${e.message}`, true));
