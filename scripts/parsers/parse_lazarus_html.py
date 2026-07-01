"""Parser for the lazarus.elte.hu combined-year archive pages (2002-2013), the only
surviving source for these years (see QUALITY-CHECK.md). Each page is one big
hand-coded HTML document with no consistent markup from year to year: some years wrap
results in <pre> blocks, others just use <br>-separated lines; class headers are a
"<font size=+1>...</font>" tag with the class code in some order/nesting that also
varies. Country names are sometimes followed by a 2-3 letter code, sometimes not, and
times appear as mm:ss, mm.ss, or mm.ss,d depending on year.

Only Sprint/Long are extracted here. Relay from this source is intentionally skipped:
investigation during the original QUALITY-CHECK pass found that relay rows interleave
team-rank lines with individually-numbered leg-runner lines (and sometimes SI-card
numbers at the start of a line) in a way that can't be told apart reliably by an
automated parser - publishing a guess would be worse than no data.
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

YEARS = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013]

# Most years here print "Given Surname" (left as-is) or signal "Surname Given" via a
# comma or an ALL-CAPS surname run, both already handled generically by
# common.reorder_name(). These specific years instead print plain "Surname Given" with
# no such marker (verified by hand against the raw HTML, e.g. 2011: "1. Mueller Sandrine
# Switzerland" for a competitor who appears in other years as "Sandrine Mueller") - move
# the trailing word to the front for these years only.
FORCE_SURNAME_FIRST_YEARS = {2003, 2004, 2005, 2011}

SECTION_RE = re.compile(r'<TD[^>]*BGCOLOR="ffffaa"[^>]*>([\s\S]{0,150}?)</TD>', re.IGNORECASE)
HEADER_RE = re.compile(
    r'<font size="?\+1"?[^>]*>\s*(?:<b>)?\s*(?:<a[^>]*>)?\s*([A-Za-z0-9]+)\s*(?:</a>)?\s*(?:</b>)?\s*</font>',
    re.IGNORECASE,
)
TAG_RE = re.compile(r"<[^>]+>")
BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
RANK_RE = re.compile(r"^\s*(\d+)[.\s]\s*")
LEADING_NUM_RE = re.compile(r"^\s*\d{1,4}\s+")
TRAILING_JUNK_RE = re.compile(r"^[A-Z]{1,3}\d{0,2}$|^\d{1,3}$")
TIME_RE = re.compile(r"(\d{1,3}:\d{2}(?::\d{2})?|\d{1,3}\.\d{2}(?:,\d)?)")


def discipline_for_section(section_text):
    t = section_text.upper()
    if "SPRINT" in t or "RÖVIDTÁV" in t or "ROVIDTAV" in t or "SHORT" in t:
        return "sprint"
    if "HOSSZ" in t or "LONG" in t or "KÖZÉPTÁV" in t or "KOZEPTAV" in t or "MIDDLE" in t:
        return "long"
    if "VÁLTÓ" in t or "VALTO" in t or "RELAY" in t:
        return None  # intentionally skipped, see module docstring
    return None


def strip_tags_and_unescape(s):
    s = BR_RE.sub("\n", s)
    s = TAG_RE.sub(" ", s)
    return html.unescape(s)


def parse_row(line):
    """Returns (rank, name, country_text, time_text) or None."""
    line = line.strip()
    if not line:
        return None
    rm = RANK_RE.match(line)
    if not rm:
        return None
    rank = int(rm.group(1))
    rest = line[rm.end():]
    tm = TIME_RE.search(rest)
    if not tm:
        return None
    before = rest[: tm.start()].strip()
    time_text = tm.group(1)
    # drop a leading bib number / birth year, e.g. "717 Müller, Sandrine ... Switzerland"
    before = LEADING_NUM_RE.sub("", before)
    words = before.split()
    # a 2006 row glues the bare country code directly onto the end of the name with no
    # space at all and no other mention of the country anywhere in the row, e.g.
    # "BjerkreimNOR" - split it off up front (the candidate-matching loop below works on
    # whole words, so a glued suffix on the final word would otherwise never be seen).
    country_text = None
    name_words = words
    glued = common.glued_country_code_suffix(words[-1]) if words else None
    if glued:
        name_part, country_text = glued
        name_words = words[:-1] + [name_part]
    else:
        # Country is the longest trailing run of 1-3 words that resolves to a known
        # country. Try matching as-is first (some years print just a bare code, e.g.
        # "CZE", with no full name - that single token IS the country, don't go
        # stripping it away). Only if nothing matches do we strip one trailing junk
        # token - heat letter (D), code+bib glued (SUI13), bare bib (1) - and retry,
        # since other years print redundant junk *after* the real country name, e.g.
        # "Switzerland SUI13 D" or "Romania ROM 1 D".
        attempt = words
        for _ in range(4):
            if not attempt:
                break
            for n in (3, 2, 1):
                if len(attempt) <= n:
                    continue
                candidate = " ".join(attempt[-n:])
                if common.normalize_country(candidate) is not None:
                    country_text = candidate
                    name_words = attempt[:-n]
                    break
            if country_text or not TRAILING_JUNK_RE.match(attempt[-1]):
                break
            attempt = attempt[:-1]
    if country_text is None:
        return None
    # some rows redundantly print the country name AND its code, e.g. "Czech republic
    # CZE 1 A" - the loop above can match just the trailing "CZE 1 A" (via the bare-code
    # shortcut in normalize_country) and leave "Czech republic" stranded in the name.
    # Strip a trailing 1-3 word country-*name* match from what's left, too. Bare 3-letter
    # codes are excluded here (allow_bare_code_alias=False) even though
    # common.normalize_country() normally accepts them case-insensitively: a given name
    # that happens to equal a country code - "Ita" (Klingenberg, DEN) or "Pol" (Rafols,
    # ESP) - would otherwise be misread as a stray redundant country mention and silently
    # dropped from the name. Genuine bare-code leftovers are already handled by the
    # trailing-candidate loop above; this second pass only needs to catch spelled-out
    # names (which are never exactly 3 letters, so excluding bare codes costs nothing).
    for n2 in (3, 2, 1):
        if len(name_words) <= n2:
            continue
        candidate2 = " ".join(name_words[-n2:])
        if common.normalize_country(candidate2, allow_bare_code_alias=False) is not None:
            name_words = name_words[:-n2]
            break
    # a few 2003 rows glue the country name straight onto the given name with no space
    # at all, e.g. "GrzegorzPoland" - split off a known country-name alias if it forms
    # the tail of the last word (min length 5 to avoid matching bare 3-letter codes).
    if name_words:
        last = name_words[-1]
        lower = last.lower()
        for alias_key in sorted(common.ALIASES, key=len, reverse=True):
            if len(alias_key) >= 5 and lower.endswith(alias_key) and len(lower) > len(alias_key):
                name_words[-1] = last[: len(last) - len(alias_key)]
                break
        else:
            # redundant glued bare-code suffix left over from a row that also printed
            # the country separately, e.g. "CARCELESESP" in a row that ALSO has "Spain"
            # right after it - only strip if it's the SAME code already resolved above
            # (an all-caps surname coincidentally ending in some unrelated code, e.g.
            # "...DEN", should be left alone).
            resolved = common.normalize_country(country_text)
            if resolved and name_words[-1].upper().endswith(resolved[0]) and len(name_words[-1]) > 3:
                name_words[-1] = name_words[-1][: -len(resolved[0])]
    name = re.sub(r"\s+", " ", " ".join(name_words)).strip().rstrip(",")
    name = re.sub(r"\s+\d{2}$", "", name)  # trailing 2-digit birth year, e.g. "Sandrine 95"
    return rank, name, country_text, time_text


def _cp1250_char(b):
    try:
        return bytes([b]).decode("cp1250")
    except UnicodeDecodeError:
        return None


_C1_TO_CP1250 = {chr(b): _cp1250_char(b) for b in range(0x80, 0xA0) if _cp1250_char(b) is not None}
_C1_RE = re.compile("[" + "".join(_C1_TO_CP1250) + "]")


def read_html(path):
    raw = path.read_bytes()
    # some years (2002-2007) are genuinely UTF-8; others (2008-2013) are a single-byte
    # codepage that isn't valid UTF-8 at all (decoding raises) - the file's own <meta
    # charset> tag isn't reliable (some UTF-8 files mislabel as something else and vice
    # versa), so just try UTF-8 first and fall back.
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1250")  # Central European codepage - handles Š/Č/Ž etc
    # 2003's file mixes that same cp1250 encoding for a handful of names but had it
    # mis-converted to UTF-8 a byte at a time (treating each cp1250 byte as a Latin-1
    # codepoint), landing as literal C1 control characters U+0080-U+009F, e.g. "Bene\x9a"
    # for "Beneš" - repair those back to the cp1250 character they actually meant.
    return _C1_RE.sub(lambda m: _C1_TO_CP1250[m.group()], text)


def parse_year(path, year):
    doc = read_html(path)
    sections = [(m.start(), strip_tags_and_unescape(m.group(1)).strip()) for m in SECTION_RE.finditer(doc)]
    headers = [(m.start(), m.end(), m.group(1)) for m in HEADER_RE.finditer(doc)]

    by_discipline = {"sprint": [], "long": []}
    total_seen_by_discipline = {"sprint": 0, "long": 0}

    for i, (h_start, h_end, raw_class) in enumerate(headers):
        klass = common.normalize_class(raw_class)
        if not klass:
            continue
        section_name = "?"
        for s_idx, s_name in sections:
            if s_idx < h_start:
                section_name = s_name
        discipline = discipline_for_section(section_name)
        if not discipline:
            continue
        chunk_end = headers[i + 1][0] if i + 1 < len(headers) else len(doc)
        chunk = strip_tags_and_unescape(doc[h_end:chunk_end])
        for line in chunk.splitlines():
            parsed = parse_row(line)
            if not parsed:
                continue
            total_seen_by_discipline[discipline] += 1
            rank, name, country_text, time_text = parsed
            if year in FORCE_SURNAME_FIRST_YEARS:
                words = name.split(" ")
                if len(words) >= 2:
                    name = " ".join([words[-1]] + words[:-1])
            country = common.normalize_country(country_text)
            if not country:
                continue
            code, _name = country
            time_s = common.time_to_seconds(time_text)
            status = common.normalize_status(None, time_s is not None)
            by_discipline[discipline].append(
                common.individual_row(klass, rank, status, None, code, name, time_s, "high", f"{year}/{path.name}")
            )
    return by_discipline, total_seen_by_discipline


def main():
    for year in YEARS:
        path = common.RAW / str(year) / f"eyoc{year}.htm"
        if not path.exists():
            continue
        by_discipline, total_seen = parse_year(path, year)
        for discipline, rows in by_discipline.items():
            out = common.write_csv(year, discipline, rows, common.SPRINT_COLUMNS)
            total = total_seen[discipline]
            dropped = total - len(rows)
            print(f"{year} {discipline}: kept {len(rows)}/{total} -> {out}" + (f"  (dropped: {dropped})" if dropped else ""))


if __name__ == "__main__":
    main()
