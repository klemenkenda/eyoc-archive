"""Parser for Relay results in the lazarus.elte.hu archive HTML (2002-2013).

Unlike Sprint/Long (handled by parse_lazarus_html.py, which intentionally skips Relay -
see its module docstring), this source's relay section turns out to be reliably
parseable per year: one "team" line (rank, bib, country, total time or status) followed
by up to 3 "leg" lines (runner identifier, name, leg time or status, plus assorted extra
columns - course-variant letters, leg rank, cumulative time - that differ by year and are
ignored here). Team and leg lines are told apart by whether the line starts with a
number (team) or a letter (leg name) - reliable across every year checked so far.

The exact markup, time format (colon "mm:ss" vs decimal-point "mm.ss"), name order
(Given Surname vs Surname Given - sometimes signalled by an ALL-CAPS run, sometimes not
signalled at all and only knowable by cross-checking the same athlete against another
year), and presence/absence of a birth-year suffix on leg names all drift across
2002-2013 (lazarus.elte.hu is a hand-coded archive, not a single export format). So each
year gets its own small parse function below rather than one generic engine being
stretched to cover all of them - some years share enough shape to reuse the same
helpers, but none are assumed to generalize without being checked against the raw HTML
and validated (leg-time sums cross-checked against each team's printed total).

Currently covers: 2002, 2003, 2004, 2005, 2007, 2008, 2009, 2010, 2011, 2012, 2013.
Not covered:
  - 2006: only top-3 placings with no runner names at all in the only source found -
    not enough data to populate relay.csv's per-leg schema.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402
import parse_lazarus_html as lazarus  # noqa: E402 - reuse read_html/HEADER_RE/strip_tags_and_unescape

RELAY_MARKER_RE = re.compile(r"RELAY", re.IGNORECASE)
# Some years (2004, 2005 confirmed) put a stray "<br />" right after the opening <font>
# tag in the relay section's W18E header specifically (not seen in the individual
# Sprint/Long section's headers), which parse_lazarus_html.HEADER_RE doesn't tolerate -
# without this, the W18E header goes undetected and its rows get silently absorbed into
# the preceding class's chunk. A local, more permissive variant avoids touching the
# shared regex (which works fine for the individual-race parser) for a quirk specific to
# this section.
RELAY_HEADER_RE = re.compile(
    r'<font size="?\+1"?[^>]*>\s*(?:<br\s*/?>)?\s*(?:<b>)?\s*(?:<a[^>]*>)?\s*([A-Za-z0-9]+)\s*(?:</a>)?\s*(?:</b>)?\s*</font>',
    re.IGNORECASE,
)
# 2010 prints status in Spanish ("n tarj." = no card/punch, "bandona" = abandoned,
# "No sale" = did not finish) instead of the usual English mp/dnf/dns abbreviations;
# common.normalize_status already recognizes these words, this just needs to be broad
# enough to split them off the country-name text in the first place.
STATUS_RE = re.compile(r"\b(mp|dns|dsq|disq|dnf|abandona|bandona|no\s+sale|n\s*tarj\.?)\b", re.IGNORECASE)
TIME_COLON_RE = re.compile(r"\d{1,2}:\d{2}:\d{2}|\d{1,3}:\d{2}")
TIME_DOT_RE = re.compile(r"\d{1,3}\.\d{2}")

# "<rank> [<bib>] <rest>" - both numbers are plain digits, with rest (country + time/
# status) starting wherever the digits stop. An optional leading "nc " (not classified)
# marks a handful of composite/guest teams (e.g. "nc 23 LAT-HUN-BUL mp") that won't
# resolve to a single EYOC country anyway and are dropped by the country lookup.
TEAM_LINE_RE = re.compile(r"^(?:nc\s+)?(\d+)(?:\s+(\d+))?\s+(\D.*)$")
# "<rank>. <rest>" variant (2005/2011) where rest still starts with a country code/name.
TEAM_LINE_DOT_RE = re.compile(r"^(\d+)\.\s+(\D.*)$")


def strip_byear(text):
    return re.sub(r"\s+\d{2}$", "", text).strip()


def resolve_country(text):
    """Try the text as-is (handles 'CZE Czech Republic' and similar via
    common.normalize_country's own dedup/shortcut logic), then fall back to checking
    each half separately for the 'TRUNCATEDNAME FULLNAME' doubling seen in some years
    (e.g. '2010: SWITZERLAN SWITZERLAND'), which is the reverse of the truncation
    pattern normalize_country already handles."""
    candidates = [text]
    words = text.split()
    if len(words) >= 2 and len(words) % 2 == 0:
        half = len(words) // 2
        candidates.append(" ".join(words[half:]))
        candidates.append(" ".join(words[:half]))
    # last resort: a stray leading/trailing code or word amid otherwise-unparsed noise,
    # e.g. "ROM Romania ROM" (doubled code+name+code, odd word count so the halving
    # above doesn't apply) - try each individual word too.
    candidates.extend(words)
    for candidate in candidates:
        result = common.normalize_country(candidate)
        if result:
            return result
    return None


def extract_trailing(text, time_re):
    """Find the LAST status word or time match in text - used for team rows, where the
    total time/status comes after the country name (and after the country, anything
    else, like a trailing '+ 5.41' time-behind column, may follow)."""
    text = text.strip()
    status_m = None
    for m in STATUS_RE.finditer(text):
        status_m = m
    time_m = None
    for m in time_re.finditer(text):
        time_m = m
    candidates = [m for m in (status_m, time_m) if m]
    if not candidates:
        return text, None, None
    last = max(candidates, key=lambda m: m.start())
    before = text[: last.start()].strip()
    if last is status_m:
        return before, common.normalize_status(last.group(1), False), None
    return before, "OK", common.time_to_seconds(last.group(0))


def extract_leading(text, time_re):
    """Find the FIRST status word or time match in text - used for leg rows, where the
    leg time/status comes right after the name (birth year, course-variant letters, leg
    rank, and cumulative time/rank may all follow and are ignored)."""
    text = text.strip()
    status_m = STATUS_RE.search(text)
    time_m = time_re.search(text)
    candidates = [m for m in (status_m, time_m) if m]
    if not candidates:
        return text, None, None
    first = min(candidates, key=lambda m: m.start())
    before = text[: first.start()].strip()
    if first is status_m:
        return before, common.normalize_status(first.group(1), False), None
    return before, "OK", common.time_to_seconds(first.group(0))


def class_chunks(doc, year, path):
    """Yield (klass, chunk_text) for each class section under the relay marker."""
    marker = RELAY_MARKER_RE.search(doc)
    if not marker:
        return
    chunk_doc = doc[marker.start():]
    headers = [(m.start(), m.end(), m.group(1)) for m in RELAY_HEADER_RE.finditer(chunk_doc)]
    for i, (_h_start, h_end, raw_class) in enumerate(headers):
        klass = common.normalize_class(raw_class)
        if not klass:
            continue
        chunk_end = headers[i + 1][0] if i + 1 < len(headers) else len(chunk_doc)
        yield klass, lazarus.strip_tags_and_unescape(chunk_doc[h_end:chunk_end])


def make_row(klass, rank, status, country_result, total_time, legs, year, path):
    code, name = country_result
    return common.relay_row(klass, rank, status or "DNF", code, code, name, total_time,
                             legs, "high", f"{year}/{path.name}")


# --- 2002: "rank. total_time<TAB>country" then "leg#. SURNAME Given<TAB>leg_time<TAB>cum_time<TAB>(rank)" ---
TEAM_2002_RE = re.compile(r"^(\d+)\.\s+(\d+\.\d{2}|mp|dns|dsq|disq|dnf)\s+(\S.*)$", re.IGNORECASE)
LEG_2002_RE = re.compile(r"^\d+\.\s+(\S.*)$")


def parse_2002(doc, year, path):
    rows, total_seen = [], 0
    for klass, chunk in class_chunks(doc, year, path):
        pending = None

        def flush():
            nonlocal pending
            if pending is None:
                return
            country = resolve_country(pending["country_text"])
            if country:
                rows.append(make_row(klass, pending["rank"], pending["status"], country,
                                      pending["total_time"], pending["legs"], year, path))
            pending = None

        for line in chunk.splitlines():
            line = line.strip()
            if not line:
                continue
            m = TEAM_2002_RE.match(line)
            if m:
                total_seen += 1
                flush()
                rank, time_text, country_text = m.groups()
                total_time = common.time_to_seconds(time_text)
                status = "OK" if total_time is not None else common.normalize_status(time_text, False)
                pending = {"rank": int(rank), "country_text": country_text,
                           "status": status, "total_time": total_time, "legs": []}
                continue
            m = LEG_2002_RE.match(line)
            if m and pending is not None and len(pending["legs"]) < 3:
                name, status, seconds = extract_leading(m.group(1), TIME_DOT_RE)
                if name:
                    pending["legs"].append((name, seconds))
        flush()
    return rows, total_seen


# --- 2004/2007/2008/2009/2010/2012: "rank [bib] country[/code] total_time_or_status",
# leg rows "Name [byear] leg_time_or_status [...ignored extra columns...]" ---
def make_colon_year_parser(strip_year_suffix, force_swap=False):
    def parser(doc, year, path):
        rows, total_seen = [], 0
        for klass, chunk in class_chunks(doc, year, path):
            pending = None

            def flush():
                nonlocal pending
                if pending is None:
                    return
                country = resolve_country(pending["country_text"])
                if country:
                    rows.append(make_row(klass, pending["rank"], pending["status"], country,
                                          pending["total_time"], pending["legs"], year, path))
                pending = None

            for line in chunk.splitlines():
                line = line.strip()
                if not line:
                    continue
                m = TEAM_LINE_RE.match(line)
                if m:
                    total_seen += 1
                    flush()
                    rank_or_bib, bib, rest = m.groups()
                    rank = int(rank_or_bib) if bib is not None else None
                    country_text, status, total_time = extract_trailing(rest, TIME_COLON_RE)
                    pending = {"rank": rank, "country_text": country_text,
                               "status": status, "total_time": total_time, "legs": []}
                    continue
                if pending is None or len(pending["legs"]) >= 3:
                    continue
                name, status, seconds = extract_leading(line, TIME_COLON_RE)
                if strip_year_suffix:
                    name = strip_byear(name)
                if name and force_swap:
                    words = name.split(" ")
                    if len(words) >= 2:
                        name = " ".join([words[-1]] + words[:-1])
                if name:
                    pending["legs"].append((name, seconds))
            flush()
        return rows, total_seen
    return parser


# --- 2005/2011: "rank. CODE country_name total_time[ + behind]", leg rows
# "Surname Given leg_time (leg_rank) [cum_time (cum_rank)]" - decimal-point time,
# name order needs swapping (no case signal; confirmed by cross-checking the same
# athletes' Given-Surname order in other years/sources). ---
TRAILING_DIFF_RE = re.compile(r"\s*\+\s*\d+\.\d{2}\s*$")


def make_dot_year_parser():
    def parser(doc, year, path):
        rows, total_seen = [], 0
        for klass, chunk in class_chunks(doc, year, path):
            pending = None

            def flush():
                nonlocal pending
                if pending is None:
                    return
                country = resolve_country(pending["country_text"])
                if country:
                    rows.append(make_row(klass, pending["rank"], pending["status"], country,
                                          pending["total_time"], pending["legs"], year, path))
                pending = None

            for line in chunk.splitlines():
                line = TRAILING_DIFF_RE.sub("", line.strip())
                if not line:
                    continue
                m = TEAM_LINE_DOT_RE.match(line)
                if m:
                    total_seen += 1
                    flush()
                    rank, rest = m.groups()
                    country_text, status, total_time = extract_trailing(rest, TIME_DOT_RE)
                    pending = {"rank": int(rank), "country_text": country_text,
                               "status": status, "total_time": total_time, "legs": []}
                    continue
                if pending is None or len(pending["legs"]) >= 3:
                    continue
                name, status, seconds = extract_leading(line, TIME_DOT_RE)
                if name:
                    words = name.split(" ")
                    if len(words) >= 2:
                        name = " ".join([words[-1]] + words[:-1])
                    pending["legs"].append((name, seconds))
            flush()
        return rows, total_seen
    return parser


# --- 2003: one fixed-width line per team with all 3 legs inline: "rank bib CODE
# country total_time leg1_name leg1_time/rank leg2_name leg2_time/rank cum_time/rank
# leg3_name leg3_time/rank total_time/rank" (the last 2 fields just repeat the team
# total). Decimal-point time, "Surname Given" order (no case signal, forced swap).
# Unranked/DSQ teams omit the rank number and/or replace the total time with a status
# word (e.g. "DISQ"); composite "MIX" guest teams are dropped naturally since "MIX 1 -
# LAT, LTU, UKR" doesn't resolve to a single EYOC country. ---
TEAM_HEADER_2003_RE = re.compile(
    r"^\s*(\d+)?\s+(\d+)\s+(\S+)\s+(.+?)\s+(\d{1,3}\.\d{2}|DISQ|MP|DNF|DNS)(?=\s|$)",
    re.IGNORECASE,
)
LEG_TIME_2003_RE = re.compile(r"(\d{1,3}\.\d{2})(?:/(\d+))?")


def parse_2003_legs(remainder):
    """Scan the text after the team header for up to 3 leg (name, time) pairs. Each
    real leg has a name immediately before its time; the cumulative-time field after
    leg 2 and the repeated final total after leg 3 have no name before them (the gap is
    pure whitespace/digits), which is how they're told apart from a genuine leg."""
    legs = []
    pos = 0
    for m in LEG_TIME_2003_RE.finditer(remainder):
        gap = remainder[pos:m.start()]
        pos = m.end()
        if len(legs) >= 3:
            break
        if re.search(r"[A-Za-zÀ-ž]", gap):
            name = re.sub(r"\bnC\b", "", gap).strip()
            words = name.split(" ")
            if len(words) >= 2:
                name = " ".join([words[-1]] + words[:-1])
            if name:
                legs.append((name, common.time_to_seconds(m.group(1))))
    return legs


def parse_2003(doc, year, path):
    rows, total_seen = [], 0
    for klass, chunk in class_chunks(doc, year, path):
        for line in chunk.splitlines():
            line = line.strip()
            if not line:
                continue
            m = TEAM_HEADER_2003_RE.match(line)
            if not m:
                continue
            total_seen += 1
            rank, _bib, code, country_text, time_or_status = m.groups()
            country = common.normalize_country(re.sub(r"\bnC\b", "", country_text).strip())
            if not country:
                continue
            total_time = common.time_to_seconds(time_or_status)
            status = "OK" if total_time is not None else common.normalize_status(time_or_status, False)
            legs = parse_2003_legs(line[m.end():])
            rows.append(make_row(klass, int(rank) if rank else None, status, country,
                                  total_time, legs, year, path))
    return rows, total_seen


YEAR_PARSERS = {
    2002: parse_2002,
    2003: parse_2003,
    2004: make_colon_year_parser(strip_year_suffix=True),
    2005: make_dot_year_parser(),
    2007: make_colon_year_parser(strip_year_suffix=False, force_swap=True),
    2008: make_colon_year_parser(strip_year_suffix=True),
    2009: make_colon_year_parser(strip_year_suffix=False),
    2010: make_colon_year_parser(strip_year_suffix=False),
    2011: make_dot_year_parser(),
    2012: make_colon_year_parser(strip_year_suffix=True),
    2013: None,  # handled separately by its own SI-card-based grammar below
}


# --- 2013: "rank bib CODE total_time", leg rows "SI-card name leg_time" - SI-card
# numbers (5+ digits) reliably distinguish leg rows from short rank/bib numbers, so this
# year doesn't need the start-of-line digit-vs-letter rule the other years use. ---
RANKED_TEAM_2013_RE = re.compile(r"^(\d{1,3})\s+(\d{1,4})\s+([A-Z]{3})\s+(\S.*)$")
UNRANKED_TEAM_2013_RE = re.compile(r"^(\d{1,4})\s+([A-Z]{3})\s+(\S.*)$")
LEG_2013_RE = re.compile(r"^(\d{5,})\s+(\S.*)$")
TRAILING_TIME_2013_RE = re.compile(r"(\d{1,2}:\d{2}:\d{2}|\d{1,3}:\d{2})\s*$")


def split_trailing_2013(text):
    text = text.strip()
    m = TRAILING_TIME_2013_RE.search(text)
    if m:
        return text[: m.start()].strip(), m.group(1)
    m = STATUS_RE.search(text)
    if m:
        return text[: m.start()].strip(), m.group(1)
    return text, ""


def parse_2013(doc, year, path):
    rows, total_seen = [], 0
    for klass, chunk in class_chunks(doc, year, path):
        pending = None

        def flush():
            nonlocal pending
            if pending is None:
                return
            country = common.normalize_country(pending["code"])
            if country:
                rows.append(make_row(klass, pending["rank"], pending["status"], country,
                                      pending["total_time"], pending["legs"], year, path))
            pending = None

        for line in chunk.splitlines():
            line = line.strip()
            if not line:
                continue
            m = RANKED_TEAM_2013_RE.match(line)
            if m:
                total_seen += 1
                flush()
                rank, _bib, code, tail = m.groups()
                status, total_time = extract_trailing(tail, TIME_COLON_RE)[1:]
                pending = {"rank": int(rank), "code": code, "status": status,
                           "total_time": total_time, "legs": []}
                continue
            m = UNRANKED_TEAM_2013_RE.match(line)
            if m:
                total_seen += 1
                flush()
                _bib, code, tail = m.groups()
                status, total_time = extract_trailing(tail, TIME_COLON_RE)[1:]
                pending = {"rank": None, "code": code, "status": status,
                           "total_time": total_time, "legs": []}
                continue
            m = LEG_2013_RE.match(line)
            if m and pending is not None and len(pending["legs"]) < 3:
                _si, tail = m.groups()
                name, time_text = split_trailing_2013(tail)
                _status, leg_time = extract_leading(time_text, TIME_COLON_RE)[1:] if time_text else (None, None)
                if name:
                    pending["legs"].append((name, leg_time))
        flush()
    return rows, total_seen


YEAR_PARSERS[2013] = parse_2013

YEARS = sorted(YEAR_PARSERS)


def main():
    for year in YEARS:
        path = common.RAW / str(year) / f"eyoc{year}.htm"
        if not path.exists():
            continue
        doc = lazarus.read_html(path)
        rows, total_seen = YEAR_PARSERS[year](doc, year, path)
        out = common.write_csv(year, "relay", rows, common.RELAY_COLUMNS)
        dropped = total_seen - len(rows)
        print(f"{year} relay: kept {len(rows)}/{total_seen} -> {out}" + (f"  (dropped: {dropped})" if dropped else ""))


if __name__ == "__main__":
    main()
