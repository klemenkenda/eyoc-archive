"""Shared helpers for all EYOC result parsers.

Every parser script is responsible for one raw source *format* (not one year) and writes
into results/<year>/{sprint,long,relay}.csv per results/FORMAT-RESULTS.md.
"""
import csv
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "results" / "raw"
CLEAN_ROOT = ROOT / "results"
COUNTRIES_MD = ROOT / "results" / "EYOC-COUNTRIES.md"

SPRINT_COLUMNS = ["class", "rank", "status", "bib", "country", "name", "time_seconds", "confidence", "source_file"]
RELAY_COLUMNS = [
    "class", "rank", "status", "country", "team", "total_time_seconds",
    "leg1_name", "leg1_time_seconds", "leg2_name", "leg2_time_seconds", "leg3_name", "leg3_time_seconds",
    "confidence", "source_file",
]


def load_country_codes():
    """Parse results/EYOC-COUNTRIES.md -> {code: name}."""
    codes = {}
    for line in COUNTRIES_MD.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*([A-Z]{3})\s*\|\s*([^|]+?)\s*\|", line)
        if m:
            codes[m.group(1)] = m.group(2).strip()
    return codes


CODES = load_country_codes()  # code -> canonical name
NAMES_BY_LOWER = {name.lower(): code for code, name in CODES.items()}

# Alternative spellings/codes seen across 24 years of differently-formatted source files,
# mapped to the canonical IOF 3-letter code used in EYOC-COUNTRIES.md.
ALIASES = {
    "czech republic": "CZE", "czech rep": "CZE", "czechia": "CZE", "czech": "CZE",
    "great britain": "GBR", "uk": "GBR", "united kingdom": "GBR",
    "russia": "RUS", "russian federation": "RUS",
    "belorussia": "BLR", "belarus": "BLR",
    "latvija": "LAT", "latvia": "LAT",
    "macedonia": "MKD", "north macedonia": "MKD", "fyr macedonia": "MKD",
    "moldova": "MDA", "moldavia": "MDA", "moldova, republic of": "MDA", "republic of moldova": "MDA",
    "slovak republic": "SVK", "slovakia": "SVK",
    "switzerland": "SUI",
    "netherlands": "NED", "holland": "NED",
    "denmark": "DEN",
    "spain": "ESP",
    "ireland": "IRL",
    "israel": "ISR",
    "italy": "ITA",
    "lithuania": "LTU",
    "luxembourg": "LUX",
    "montenegro": "MNE",
    "norway": "NOR",
    "poland": "POL",
    "portugal": "POR",
    "romania": "ROU",
    "slovenia": "SLO",
    "serbia": "SRB",
    "sweden": "SWE",
    "turkey": "TUR", "turkiye": "TUR", "türkiye": "TUR",
    "ukraine": "UKR",
    "austria": "AUT",
    "azerbaijan": "AZE",
    "belgium": "BEL",
    "bulgaria": "BUL",
    "croatia": "CRO",
    "cyprus": "CYP",
    "estonia": "EST",
    "finland": "FIN",
    "france": "FRA",
    "germany": "GER",
    "hungary": "HUN",
    "liechtenstein": "LIE",
}
# also accept the codes themselves (case-insensitive) and canonical names
for _code in CODES:
    ALIASES[_code.lower()] = _code
ALIASES["rom"] = "ROU"  # old IOC-style code for Romania, still used by some older software
ALIASES["lreland"] = "IRL"  # common OCR misread of "Ireland" (capital I -> lowercase l)
ALIASES["ukraina"] = "UKR"  # Hungarian/Slavic spelling seen in some lazarus.elte.hu years
for _name, _code in NAMES_BY_LOWER.items():
    ALIASES[_name] = _code

_dropped_counter = {}


def normalize_country(raw_text, source_file=""):
    """Return (code, name) if raw_text maps to an EYOC-eligible European country, else None.

    Non-European / composite / unrecognised entries (e.g. "Europa", guest teams) are
    counted in _dropped_counter for later reporting and otherwise silently excluded.
    """
    if not raw_text:
        return None
    text = re.sub(r"\s+", " ", raw_text).strip().strip(".")
    # "CZE Czechia" - leading 3-letter code followed by the (possibly misspelled) name
    lead = text.split(" ", 1)[0]
    if lead.upper() in CODES and lead.isupper() and len(lead) == 3:
        return lead.upper(), CODES[lead.upper()]
    # strip a trailing team-number suffix like "Czech Republic 1" -> "Czech Republic"
    text_no_num = re.sub(r"\s+\d+$", "", text)
    # some PDF templates print the country name twice (sometimes the 2nd copy is
    # truncated by column width), e.g. "Hungary Hungary" or "Czech Republic Czech Repub"
    words = text_no_num.split(" ")
    if len(words) >= 2 and len(words) % 2 == 0:
        n = len(words) // 2
        first_half, second_half = " ".join(words[:n]), " ".join(words[n:])
        if first_half == second_half or (second_half and first_half.startswith(second_half)):
            text_no_num = first_half
    for candidate in (text, text_no_num):
        key = candidate.lower()
        if key in ALIASES:
            code = ALIASES[key]
            return code, CODES[code]
    # last resort: narrow PDF columns sometimes truncate the name, e.g. "Russian Federati"
    # -> match against alias keys it's a prefix of (long enough to avoid false positives)
    key = text_no_num.lower()
    if len(key) >= 6:
        for alias_key, code in ALIASES.items():
            if len(alias_key) >= 6 and alias_key.startswith(key):
                return code, CODES[code]
    # some narrow-column 2014 PDFs truncate the country *code* to 2 letters, e.g.
    # "GB" for GBR, "NO" for NOR - only resolve if exactly one EYOC code matches the
    # prefix (e.g. "PO" -> POL/POR is genuinely ambiguous and stays dropped)
    if len(text_no_num) == 2:
        matches = [c for c in CODES if c.startswith(text_no_num.upper())]
        if len(matches) == 1:
            return matches[0], CODES[matches[0]]
    _dropped_counter[raw_text] = _dropped_counter.get(raw_text, 0) + 1
    return None


def get_dropped_report():
    return dict(sorted(_dropped_counter.items(), key=lambda kv: -kv[1]))


def reset_dropped_report():
    _dropped_counter.clear()


def time_to_seconds(text):
    """Convert mm:ss, h:mm:ss, or 'mm.ss,d' (European decimal-comma) to integer seconds."""
    if not text:
        return None
    text = text.strip()
    if not text or text.lower() in ("dnf", "dsq", "dns", "mp", "no sale", "-", "n/a"):
        return None
    # mm.ss,d or mm.ss (lazarus old-style: "12.01,4" => 12 min 01.4 sec)
    m = re.match(r"^(\d+)\.(\d{2}),(\d+)$", text)
    if m:
        minutes, secs, frac = m.groups()
        return int(minutes) * 60 + int(secs) + (1 if int(frac) >= 5 else 0)
    m = re.match(r"^(\d+)\.(\d{2})$", text)
    if m:
        minutes, secs = m.groups()
        return int(minutes) * 60 + int(secs)
    # h:mm:ss or mm:ss
    parts = text.split(":")
    if len(parts) == 3:
        try:
            h, mn, s = (float(p) for p in parts)
            return int(round(h * 3600 + mn * 60 + s))
        except ValueError:
            return None
    if len(parts) == 2:
        try:
            mn, s = (float(p) for p in parts)
            return int(round(mn * 60 + s))
        except ValueError:
            return None
    return None


def normalize_status(text, has_time):
    if not text:
        return "OK" if has_time else "DNF"
    t = text.strip().lower()
    if "dsq" in t or "disq" in t:
        return "DSQ"
    if "dns" in t:
        return "DNS"
    if t in ("mp", "mispunch") or "mp" == t:
        return "MP"
    if "dnf" in t or "no sale" in t or "abandon" in t or "bandona" in t:
        return "DNF"
    return "OK" if has_time else "DNF"


def pdf_rows(pdf_path, y_tol=2.0):
    """Extract (y, [(x0, text), ...]) rows from a PDF using word coordinates (PyMuPDF),
    which is far more reliable than pdftotext -layout for the multi-column OE2010/OS2010
    result sheets (pdftotext's heuristic row-joiner misaligns rows with offset baselines).
    Rows are merged across consecutive words whose y0 is within y_tol, per page.
    """
    import fitz  # PyMuPDF
    rows = []
    with fitz.open(str(pdf_path)) as doc:
        for page in doc:
            words = page.get_text("words")  # x0,y0,x1,y1,text,block,line,word_no
            words.sort(key=lambda w: (round(w[1] / y_tol) * y_tol, w[0]))
            current_y = None
            current = []
            for w in words:
                y = w[1]
                if current_y is None or abs(y - current_y) <= y_tol:
                    current.append((w[0], w[4]))
                    current_y = y if current_y is None else current_y
                else:
                    rows.append((current_y, sorted(current, key=lambda t: t[0])))
                    current = [(w[0], w[4])]
                    current_y = y
            if current:
                rows.append((current_y, sorted(current, key=lambda t: t[0])))
    return rows


def row_text(row):
    return " ".join(t for _, t in row[1])


def bucket_row(row, columns, slack=8.0):
    """columns: list of (name, x_start) sorted ascending by x_start.
    Returns {name: joined_text} by assigning each word to the last column whose
    x_start <= word's x0 + slack. The slack accounts for right-justified numeric
    columns (time, bib) whose data sits a few px left of the header label's x0.
    """
    starts = [c[1] for c in columns]
    names = [c[0] for c in columns]
    out = {n: [] for n in names}
    for x0, text in row[1]:
        idx = 0
        for i, s in enumerate(starts):
            if x0 + slack >= s:
                idx = i
        out[names[idx]].append(text)
    return {k: " ".join(v) for k, v in out.items()}


def configure_tesseract():
    """Locate the Tesseract binary/tessdata installed via conda-forge, which doesn't
    always end up on PATH and whose tessdata can land in the package cache rather than
    the live env's share dir."""
    import pytesseract

    if not os.environ.get("TESSDATA_PREFIX"):
        candidates = list(Path(sys.prefix).glob("**/tessdata")) + list(Path(sys.prefix).glob("**/pkgs/tesseract-*/share/tessdata"))
        for c in candidates:
            if (c / "eng.traineddata").exists():
                os.environ["TESSDATA_PREFIX"] = str(c)
                break
    try:
        pytesseract.get_tesseract_version()
    except Exception:
        for exe in (Path(sys.prefix) / "Library" / "bin" / "tesseract.exe",):
            if exe.exists():
                pytesseract.pytesseract.tesseract_cmd = str(exe)
                break
    return pytesseract


@dataclass
class OcrWord:
    page: int
    text: str
    x: float
    y: float
    w: float
    h: float

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2


def render_pdf_pages(pdf_path, out_dir, zoom=4.0):
    """Render every page of pdf_path to PNG files in out_dir, for scanned PDFs with no
    text layer. Returns the list of image paths, one per page in order."""
    import fitz

    doc = fitz.open(str(pdf_path))
    paths = []
    matrix = fitz.Matrix(zoom, zoom)
    for index, page in enumerate(doc, start=1):
        out = Path(out_dir) / f"page_{index:02d}.png"
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        pix.save(str(out))
        paths.append(out)
    return paths


def tesseract_ocr(paths, zoom=4.0, psm=6):
    """OCR each rendered page image and return OcrWord list with coordinates normalized
    back to PDF points (i.e. divided by the zoom factor used to render them)."""
    pytesseract = configure_tesseract()
    from pytesseract import Output

    words = []
    for page_num, path in enumerate(paths, start=1):
        data = pytesseract.image_to_data(str(path), config=f"--psm {psm}", output_type=Output.DICT)
        for i, text in enumerate(data["text"]):
            text = text.strip()
            if not text:
                continue
            words.append(OcrWord(
                page=page_num,
                text=text,
                x=data["left"][i] / zoom,
                y=data["top"][i] / zoom,
                w=data["width"][i] / zoom,
                h=data["height"][i] / zoom,
            ))
    return words


def group_ocr_lines(words, y_tol=4.5):
    """Group OcrWord results into table rows by y-coordinate, per page."""
    lines = []
    for page in sorted({word.page for word in words}):
        page_words = sorted((word for word in words if word.page == page), key=lambda w: (w.cy, w.x))
        current = []
        current_y = None
        for word in page_words:
            if current_y is None or abs(word.cy - current_y) <= y_tol:
                current.append(word)
                current_y = word.cy if current_y is None else (current_y * (len(current) - 1) + word.cy) / len(current)
            else:
                lines.append(sorted(current, key=lambda w: w.x))
                current = [word]
                current_y = word.cy
        if current:
            lines.append(sorted(current, key=lambda w: w.x))
    return lines


def ocr_line_text(words):
    return " ".join(word.text for word in sorted(words, key=lambda w: w.x))


def pdf_to_text(pdf_path):
    """Run pdftotext -layout and return stdout text, or None if extraction yields nothing useful."""
    try:
        out = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            capture_output=True, timeout=60,
        )
    except FileNotFoundError:
        raise RuntimeError("pdftotext not found on PATH (poppler/xpdf utils required)")
    text = out.stdout.decode("utf-8", errors="replace")
    if len(text.strip()) < 20:
        return None
    return text


def ensure_year_dir(year):
    d = CLEAN_ROOT / str(year)
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_csv(year, discipline, rows, columns):
    """discipline in {'sprint','long','relay'}. rows: list of dicts. Skips writing if rows empty."""
    if not rows:
        return None
    d = ensure_year_dir(year)
    path = d / f"{discipline}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})
    return path


_NAME_PARTICLES = {
    "von", "van", "de", "der", "den", "des", "du", "la", "le", "di", "da",
    "dos", "das", "del", "della", "av", "af", "ter", "ten", "zu", "y",
    "el", "al", "bin", "ibn", "ov", "vd",
}
_WORD_RE = re.compile(r"^([^A-Za-zÀ-ž]*)([A-Za-zÀ-ž'\-]*)([^A-Za-zÀ-ž]*)$")
_BARE_RE = re.compile(r"[^A-Za-zÀ-ž]")


def _cap_simple(s):
    return s[0].upper() + s[1:].lower() if s else s


def _format_core(core):
    """Capitalize one alphabetic run, respecting O'Brien / McDonald / MacLeod style names."""
    if not core:
        return core
    if "'" in core:
        return "'".join(_cap_simple(seg) for seg in core.split("'"))
    lc = core.lower()
    # Only split "Mc"/"Mac" off as a name prefix when the source text itself already
    # capitalized the following letter (true camel-case, e.g. "McDonald"/"MacLeod") -
    # otherwise this misfires on ordinary surnames that happen to start with those
    # letters, e.g. the Czech surname "Machutova".
    if lc.startswith("mc") and len(core) > 2 and core[2].isupper():
        return "Mc" + _cap_simple(core[2:])
    if lc.startswith("mac") and len(core) > 3 and core[3].isupper():
        return "Mac" + _cap_simple(core[3:])
    return _cap_simple(core)


def _format_token(token):
    """One whitespace-separated chunk, possibly with leading/trailing punctuation
    (e.g. a trailing comma in 'Muller,') and/or internal hyphens ('Anne-Marie')."""
    m = _WORD_RE.match(token)
    if not m:
        return token
    prefix, core, suffix = m.groups()
    if not core:
        return token
    formatted = "-".join(_format_core(part) for part in core.split("-"))
    return prefix + formatted + suffix


def _is_capsword(w):
    letters = [c for c in w if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)


def reorder_name(raw_name):
    """Source PDFs/HTML print names in two different orders depending on the event's
    software/template: some print 'Given Surname' (already what we want), others print
    'Surname Given' or 'Surname, Given'. Detect the latter and swap to Given-first:

      - a comma always marks 'Surname, Given' (e.g. lazarus.elte.hu archive) - split and swap.
      - a leading run of ALL-CAPS word(s) followed by mixed-case word(s) marks the
        SportSoftware-style 'SURNAME Given' convention (e.g. several OE2010/text-PDF
        sources) - move the caps run to the end.

    If neither signal is present, the name is left as-is (already Given-first).
    """
    if not raw_name:
        return raw_name
    if "," in raw_name:
        surname, _, given = raw_name.partition(",")
        return f"{given.strip()} {surname.strip()}".strip()
    words = raw_name.split()
    if len(words) < 2:
        return raw_name
    caps_run = 0
    for w in words:
        if _is_capsword(w):
            caps_run += 1
        else:
            break
    if 0 < caps_run < len(words):
        return " ".join(words[caps_run:] + words[:caps_run])
    return raw_name


def format_name(name):
    """Title-case an extracted name: 'JOHN VON SMITH' / 'mueller, sandrine' ->
    'John von Smith' / 'Mueller, Sandrine'. Lowercase name particles (von, van, de, ...)
    keep their lowercase form; O'Brien/McDonald/MacLeod-style names keep their inner caps.
    """
    if not name:
        return name
    words = name.split(" ")
    out = []
    for w in words:
        bare = _BARE_RE.sub("", w).lower()
        if bare in _NAME_PARTICLES:
            out.append(w.lower())
        else:
            out.append(_format_token(w))
    return " ".join(out)


def relay_row(klass, rank, status, code, name_country, team_label, total_time, legs, confidence, source_file):
    row = {
        "class": klass, "rank": rank if rank is not None else "",
        "status": status, "country": code, "team": team_label,
        "total_time_seconds": total_time if total_time is not None else "",
        "confidence": confidence, "source_file": source_file,
    }
    for i in range(3):
        n, t = (legs[i] if i < len(legs) else (None, None))
        row[f"leg{i+1}_name"] = format_name(reorder_name(n)) if n else ""
        row[f"leg{i+1}_time_seconds"] = t if t is not None else ""
    return row


def individual_row(klass, rank, status, bib, code, name, time_s, confidence, source_file):
    return {
        "class": klass, "rank": rank if rank is not None else "",
        "status": status, "bib": bib or "", "country": code, "name": format_name(reorder_name(name)),
        "time_seconds": time_s if time_s is not None else "",
        "confidence": confidence, "source_file": source_file,
    }


# class-name normalization: source files spell classes inconsistently (Men 16 / M16 / M16E / M)
def normalize_class(raw):
    t = raw.strip().upper()
    if t.startswith("WOMEN") or t.startswith("WOMAN"):
        t = "W" + t[5:] if t.startswith("WOMEN") else "W" + t[5:]
    elif t.startswith("MEN"):
        t = "M" + t[3:]
    t = t.rstrip("E").replace(" ", "")
    if t in ("M16", "M18", "W16", "W18"):
        return t
    if t in ("MIX", "MIXT", "MIXED"):
        return "Mixed"
    return None
