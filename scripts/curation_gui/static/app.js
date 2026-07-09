const DISCIPLINES = ["sprint", "long", "relay"];
const CLASSES = ["M16", "M18", "W16", "W18"];
const CATEGORY_FIELDS = [
  { key: "place", label: "Place", type: "text" },
  { key: "map_name", label: "Map name", type: "text" },
  { key: "distance_km", label: "Distance (km)", type: "number", step: "0.1" },
  { key: "elevation_m", label: "Climb (m)", type: "number", step: "1" },
  { key: "control_points", label: "Controls", type: "number", step: "1" },
  { key: "field_size", label: "Field size", type: "number", step: "1" },
];
const COLUMN_LABELS = {
  class: "Class", rank: "Rank", status: "Status", bib: "Bib", country: "Country",
  name: "Name", time_seconds: "Time (s)", confidence: "Confidence", source_file: "Source",
  team: "Team", total_time_seconds: "Total (s)",
  leg1_name: "Leg 1", leg1_time_seconds: "Leg 1 (s)",
  leg2_name: "Leg 2", leg2_time_seconds: "Leg 2 (s)",
  leg3_name: "Leg 3", leg3_time_seconds: "Leg 3 (s)",
};

const state = {
  year: null,
  discipline: "sprint",
  yearData: null,   // full /api/year/<year> response
  rows: [],         // working copy of rows for the active discipline
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
  const [years, codes] = await Promise.all([
    api("/api/years"),
    api("/api/country-codes"),
  ]);

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
  $("#addRowBtn").addEventListener("click", addRow);
  $("#saveCsvBtn").addEventListener("click", saveCsv);
  $("#saveMetadataBtn").addEventListener("click", saveMetadata);
  $("#rebuildBtn").addEventListener("click", rebuild);

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

function updateRawFrame() {
  const sel = $("#rawFileSelect");
  const frame = $("#rawFrame");
  frame.src = sel.value ? `/api/raw/${sel.value}` : "about:blank";
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

function renderCsvTable() {
  const d = state.yearData.disciplines[state.discipline];
  const columns = d.columns;

  $("#rowCount").textContent = state.rows.length;

  const thead = $("#csvTable thead");
  thead.innerHTML = `<tr>${columns.map((c) => `<th>${COLUMN_LABELS[c] || c}</th>`).join("")}<th></th></tr>`;

  const tbody = $("#csvTable tbody");
  tbody.innerHTML = "";
  state.rows.forEach((row, i) => {
    const tr = document.createElement("tr");
    tr.innerHTML = columns.map((c) => {
      const list = c === "country" ? ' list="countryCodes"' : "";
      const val = (row[c] ?? "").toString().replace(/"/g, "&quot;");
      return `<td><input data-row="${i}" data-col="${c}" value="${val}"${list}></td>`;
    }).join("") + `<td><button class="btn btn-small btn-danger" data-del="${i}">✕</button></td>`;
    tbody.appendChild(tr);
  });

  tbody.querySelectorAll("input").forEach((input) => {
    input.addEventListener("input", () => {
      state.rows[input.dataset.row][input.dataset.col] = input.value;
    });
  });
  tbody.querySelectorAll("[data-del]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.rows.splice(parseInt(btn.dataset.del, 10), 1);
      renderCsvTable();
    });
  });
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

function blankMetadata(year) {
  const disciplineBlock = () => ({
    place: null,
    map_name: null,
    categories: Object.fromEntries(CLASSES.map((cls) => [cls, {
      place: null, map_name: null, distance_km: null, elevation_m: null, control_points: null, field_size: null,
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
