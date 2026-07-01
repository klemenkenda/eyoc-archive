"""Shared helpers for all EYOC result parsers.

Every parser script is responsible for one raw source *format* (not one year) and writes
into results/<year>/{sprint,long,relay}.csv per results/FORMAT-RESULTS.md.
"""
import csv
import os
import re
import subprocess
import sys
import unicodedata
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
    "belorussia": "BLR", "belarus": "BLR", "belarusia": "BLR",
    "latvija": "LAT", "latvia": "LAT",
    "macedonia": "MKD", "north macedonia": "MKD", "fyr macedonia": "MKD", "mecedonia": "MKD",
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
    "romania": "ROU", "romenia": "ROU",
    "slovenia": "SLO", "slovenija": "SLO",
    "serbia": "SRB", "scg": "SRB", "serbia and montenegro": "SRB",
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
    "hungary": "HUN", "hunegarv": "HUN",
    "liechtenstein": "LIE",
}
# also accept the codes themselves (case-insensitive) and canonical names
BARE_CODE_ALIASES = {_code.lower() for _code in CODES}
for _code in CODES:
    ALIASES[_code.lower()] = _code
ALIASES["rom"] = "ROU"  # old IOC-style code for Romania, still used by some older software
ALIASES["lreland"] = "IRL"  # common OCR misread of "Ireland" (capital I -> lowercase l)
ALIASES["ukraina"] = "UKR"  # Hungarian/Slavic spelling seen in some lazarus.elte.hu years
for _name, _code in NAMES_BY_LOWER.items():
    ALIASES[_name] = _code

_dropped_counter = {}


def normalize_country(raw_text, source_file="", allow_bare_code_alias=True):
    """Return (code, name) if raw_text maps to an EYOC-eligible European country, else None.

    Non-European / composite / unrecognised entries (e.g. "Europa", guest teams) are
    counted in _dropped_counter for later reporting and otherwise silently excluded.

    `allow_bare_code_alias=False` disables the case-insensitive bare-3-letter-code match
    (e.g. "ita" -> ITA, "pol" -> POL) while still allowing real country names/aliases.
    Use this when matching against text that could plausibly be a person's name instead
    of a country mention - e.g. the given names "Ita" (Klingenberg, DEN) and "Pol"
    (Rafols, ESP) are indistinguishable from the bare codes for Italy/Poland otherwise.
    """
    if not raw_text:
        return None
    text = re.sub(r"\s+", " ", raw_text).strip().strip(".")
    # "CZE Czechia" - leading 3-letter code followed by the (possibly misspelled) name
    lead = text.split(" ", 1)[0]
    if lead.upper() in CODES and lead.isupper() and len(lead) == 3:
        return lead.upper(), CODES[lead.upper()]
    # some 2003 rows glue the bib number straight onto the code with no space at all,
    # e.g. "POL14" - a bare 3-letter code prefix followed only by digits is unambiguous
    glued = re.match(r"^([A-Z]{3})\d+$", lead)
    if glued and glued.group(1) in CODES:
        return glued.group(1), CODES[glued.group(1)]
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
        if key in ALIASES and (allow_bare_code_alias or key not in BARE_CODE_ALIASES):
            code = ALIASES[key]
            return code, CODES[code]
    # last resort: narrow PDF columns sometimes truncate the name, e.g. "Russian Federati"
    # -> match against alias keys it's a prefix of (long enough to avoid false positives)
    key = text_no_num.lower()
    if len(key) >= 6:
        for alias_key, code in ALIASES.items():
            if len(alias_key) >= 6 and alias_key.startswith(key):
                return code, CODES[code]
    # the opposite truncation: some rows print a verbose/annotated country name that's
    # itself cut off mid-parenthetical by column width, e.g. "Switzerland (Confederation
    # o" - here the real country name is a clean PREFIX of the text, with truncated
    # junk trailing after it (require a word boundary so "Polandxyz" can't match "poland")
    if len(key) >= 5:
        for alias_key, code in ALIASES.items():
            if len(alias_key) >= 4 and key.startswith(alias_key + " "):
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


_GLUED_CODE_SUFFIX_RE = re.compile(r"^(.*[a-z])([A-Z]{3})$")


def glued_country_code_suffix(word):
    """If `word` is a name fragment with a bare country code glued directly onto its
    end with no space - e.g. "BjerkreimNOR" - return (name_part, code). The lowercase
    letter required right before the code is what tells this apart from an ordinary
    ALL-CAPS surname that happens to end in 3 letters matching a code (e.g. "BACHMANN"
    isn't lowercase-then-uppercase, so it's correctly left alone); otherwise None."""
    m = _GLUED_CODE_SUFFIX_RE.match(word)
    if m and m.group(2) in CODES:
        return m.group(1), m.group(2)
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


# Canonical IOF-XML status enum values (CompetitorStatus/TeamStatus/Status elements,
# e.g. <Status>MissingPunch</Status> or <CompetitorStatus value="DidNotStart" />) -
# matched as exact tokens because several of them don't contain the abbreviated
# substrings the heuristics below look for ("disqualified" has no "dsq", "didnotfinish"
# has no "dnf", "missingpunch" isn't "mp"/"mispunch"). Checked before the heuristics so a
# DNS/DNF/MP competitor who still has a partial recorded time doesn't fall through to OK.
_IOF_STATUS_MAP = {
    "ok": "OK",
    "missingpunch": "MP",
    "mispunch": "MP",
    "disqualified": "DSQ",
    "didnotstart": "DNS",
    "didnotfinish": "DNF",
    "notcompeting": "DNS",
    "overtime": "DNF",
    "cancelled": "DNF",
    "sportingwithdrawal": "DNF",
    "unknown": "DNF",
}


def normalize_status(text, has_time):
    if not text:
        return "OK" if has_time else "DNF"
    t = text.strip().lower()
    compact = re.sub(r"[^a-z]", "", t)
    if compact in _IOF_STATUS_MAP:
        return _IOF_STATUS_MAP[compact]
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


def renumber_ranks(rows):
    """Re-derive 'rank' within each class so gaps left by entries this pipeline
    excludes (non-European guests, composite/mixed teams, unresolvable rows) collapse
    into a consecutive sequence - while preserving genuine tied-rank skips from the
    source itself (two people tied for 5th means the next rank is 7th, not 6th) and
    leaving rows that were never ranked to begin with (blank rank, e.g. most DNF/DSQ)
    untouched. Mutates and returns `rows`; row order is unchanged, only rank values."""
    by_class = {}
    for r in rows:
        if r.get("rank") not in (None, ""):
            by_class.setdefault(r.get("class"), []).append(r)
    for class_rows in by_class.values():
        class_rows.sort(key=lambda r: int(r["rank"]))
        groups = []  # [(original_rank, [rows_at_that_rank]), ...] in ascending order
        for r in class_rows:
            rv = int(r["rank"])
            if groups and groups[-1][0] == rv:
                groups[-1][1].append(r)
            else:
                groups.append((rv, [r]))
        prev_rank, prev_count, shift = 0, 1, 0
        for rv, grp in groups:
            expected = prev_rank + prev_count if prev_rank else 1
            shift += rv - expected
            for r in grp:
                r["rank"] = rv - shift
            prev_rank, prev_count = rv, len(grp)
    return rows


def write_csv(year, discipline, rows, columns):
    """discipline in {'sprint','long','relay'}. rows: list of dicts. Skips writing if rows empty."""
    if not rows:
        return None
    renumber_ranks(rows)
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


# Letters with no Unicode decomposition (NFKD won't separate them into base + combining
# mark), so unicodedata can't strip their diacritic - map them to a plain-Latin spelling
# by hand. Curly quotes are included so apostrophe-name forms (e.g. "O’Brien") come
# out as a plain ASCII apostrophe.
_EXTRA_LATIN_MAP = str.maketrans({
    "æ": "ae", "Æ": "AE", "ø": "o", "Ø": "O", "ß": "ss", "đ": "d", "Đ": "D",
    "ł": "l", "Ł": "L", "þ": "th", "Þ": "Th", "ı": "i", "İ": "I",
    "‘": "'", "’": "'",
})


def to_latin(text):
    """Strip accents/diacritics so names render in plain Latin (ASCII) characters,
    e.g. 'Beneš' -> 'Benes', 'Müller' -> 'Muller'."""
    if not text:
        return text
    text = text.translate(_EXTRA_LATIN_MAP)
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))


# The 2005/2006/2017 raw sources already had this exact damage baked in before this
# project ever touched them: many accented letters got replaced with the Unicode
# replacement character (U+FFFD) at some earlier point, and the original letter is gone
# from the byte stream - it can't be recovered by re-reading the source. These are manual
# restorations researched against same-event sources that still have the real diacritics
# (results/raw/2006/2006_relay_*.txt - a different source pipeline for the same event that
# wasn't affected) and cross-year spellings of the same competitor elsewhere in this
# archive. A couple of names had no corroborating evidence anywhere and are left with the
# placeholder simply dropped rather than guessed.
NAME_FIXES = {
    "Ivana Bochenkov�": "Ivana Bochenkova",
    "Michaela Proch�zkov�": "Michaela Prochazkova",
    "Jindra Hlavov�": "Jindra Hlavova",
    "Martina Jir��kov�": "Martina Jiraskova",
    "Marie-Christine B�hm": "Marie-Christine Bohm",
    "Triin Aedm�e": "Triin Aedmae",
    "Jana Kr�iakov�": "Jana Krsiakova",
    "Ivana Korimov�": "Ivana Korimova",
    "Maris Palop��l": "Maris Palopol",
    "Zuzana Bele�ov�": "Zuzana Belesova",
    "d�a Mihalov�": "Dasa Mihalova",
    "Isabel S�": "Isabel Sa",
    "Monika Dole�alov�": "Monika Dolezalova",
    "Lucie Mach�tov�": "Lucie Machutova",
    "��Rka Svobodn�": "Sarka Svobodna",
    "Zuzana Hermanov�": "Zuzana Hermanova",
    "Tetiana Zhy�tsova": "Tetiana Zhytsova",
    "Ren�ta Barc�kov�": "Renata Barcikova",
    "Erika Hlav��ikov�": "Erika Hlavacikova",
    "Patr�cia Casalinho": "Patricia Casalinho",
    "Daniel H�jek": "Daniel Hajek",
    "Mat�j Klus��ek": "Matej Klusacek",
    "Anton�n Bedna��k": "Antonin Bednarik",
    "Rastislav O�hava": "Rastislav Olhava",
    "Martin Majl�th": "Martin Majlath",
    "Tiago Rom�o": "Tiago Romao",
    "Tom� Sokol": "Tomas Sokol",
    "Ruair� Short": "Ruairi Short",
    "Bla� Grah": "Blaz Grah",
    "�t�p�n Kodeda": "Stepan Kodeda",
    "Michal Kraj��k": "Michal Krajcik",
    "�t�p�n Holas": "Stepan Holas",
    "J�rome K�ser": "Jerome Kaser",
    "Rastislav Szab�": "Rastislav Szabo",
    "Philipp M�ller": "Philipp Muller",
    "Martin Maz�r": "Martin Mazur",
    "S�ren L�sch": "Soren Losch",
    "Ale� Mal�": "Ales Maly",
    "Lauri Tammem�e": "Lauri Tammemae",
    "Vojt�ch Kr�l": "Vojtech Kral",
    "Primo� �Ega": "Primoz Sega",
    "G�bor Turcsán": "Gabor Turcsan",
    "M�rton Mets": "Marton Mets",
    "Ad�la Jakobov�": "Adela Jakobova",
    "Vera M�llerov�": "Vera Mullerova",
    "Michaela Chmelarov�": "Michaela Chmelarova",
    "Lucie Mezn�kov�": "Lucie Meznikova",
    "Eva Farkasov�": "Eva Farkasova",
    "Aliz�e Gaillard": "Alizee Gaillard",
    "Piibe Tamem�e": "Piibe Tammemae",
    "Vera M�dlov�": "Vera Madlova",
    "Gabija Ra�aityt?": "Gabija Razaityte",
    "Jana Krsiakov�": "Jana Krsiakova",
    "Laetitia H�chler": "Laetitia Hachler",
    "Di�na Koos": "Diana Koos",
    "C�cile Papillon": "Cecile Papillon",
    "Helena Heinv�li": "Helena Heinvali",
    "Tereza Petrzelov�": "Tereza Petrzelova",
    "l�a Molinier": "Lea Molinier",
    "l�a Vercellotti": "Lea Vercellotti",
    "Th�o Fleurent": "Theo Fleurent",
    "�tip�n Zimmermann": "Stepan Zimmermann",
    "Anton�n Bednar�k": "Antonin Bednarik",
    "Milos Nykod�m": "Milos Nykodym",
    "Jan Kol�rik": "Jan Kolarik",
    "Tom�s Sokol": "Tomas Sokol",
    "Tom�s Boril": "Tomas Boril",
    "Matij Klus�cek": "Matej Klusacek",
    "Max R�hnert": "Max Rohnert",
    "D�sa Mih�lov�": "Dasa Mihalova",
    "Stip�n Zimmermann": "Stepan Zimmermann",
    "Kaspar H�gler": "Kaspar Hagler",
    "Andr�s Szabo": "Andras Szabo",
    "Kilian J�rg": "Kilian Jorg",
    "Morten �Rnhagen Jorgensen": "Morten Ornhagen Jorgensen",
    "Szuromi �Ron": "Szuromi Ron",
    "�Ubka Weissova": "Lubka Weissova",
    # Unrelated to the "�" corruption above, but same fix mechanism: the 2016 sprint
    # scan is OCR'd (see parse_2016_sprint_ocr.py), and Tesseract misread this competitor
    # tied for 8th in W16 as "HAINAI" - the real name, confirmed by other EYOC sources
    # for this athlete, is "Hajnal".
    "Dorottya Hainai": "Dorottya Hajnal",
}


def _fix_key(s):
    """Order/case-insensitive key for NAME_FIXES lookup: the corrupted "�" in a source
    word can confuse both reorder_name's all-caps detection and format_name's casing
    (e.g. relay legs printed "TURCSAN G�BOR" don't get recognised as a caps-run with a
    "�" sitting in them), so a plain string match against the source-order text isn't
    reliable - compare the lowercased, order-independent word set instead."""
    return tuple(sorted(w.lower() for w in s.split(" ") if w))


_NAME_FIXES_BY_KEY = {_fix_key(k): v for k, v in NAME_FIXES.items()}


def format_name(name):
    """Title-case an extracted name: 'JOHN VON SMITH' / 'mueller, sandrine' ->
    'John von Smith' / 'Mueller, Sandrine'. Lowercase name particles (von, van, de, ...)
    keep their lowercase form; O'Brien/McDonald/MacLeod-style names keep their inner caps.
    """
    if not name:
        return name
    fix = _NAME_FIXES_BY_KEY.get(_fix_key(name))
    if fix is not None:
        return to_latin(fix)
    words = name.split(" ")
    out = []
    for w in words:
        bare = _BARE_RE.sub("", w).lower()
        if bare in _NAME_PARTICLES:
            out.append(w.lower())
        else:
            out.append(_format_token(w))
    return to_latin(" ".join(out))


def dedupe_repeated_name(text):
    """Several source PDFs/exports print the country name twice before the team-number
    suffix, e.g. "Norway Norway 1" or "Czech Republic Czech Republic" - collapse the
    duplicated run for display, preserving a trailing team-number suffix if present."""
    if not text:
        return text
    text = re.sub(r"\s+", " ", text).strip()
    m = re.search(r"^(.*?)(\s+\d+)$", text)
    core, suffix = (m.group(1), m.group(2)) if m else (text, "")
    words = core.split(" ")
    n = len(words)
    if n >= 2 and n % 2 == 0:
        half = n // 2
        first_half, second_half = " ".join(words[:half]), " ".join(words[half:])
        if first_half == second_half:
            core = first_half
    return core + suffix


def relay_row(klass, rank, status, code, name_country, team_label, total_time, legs, confidence, source_file):
    row = {
        "class": klass, "rank": rank if rank is not None else "",
        "status": status, "country": code, "team": to_latin(dedupe_repeated_name(team_label)),
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
