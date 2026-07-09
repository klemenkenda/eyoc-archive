"""Parser for the two one-off plain-text result PDFs that don't use OE2010/OS2010's
tabular "(N)" header style: 2016 Long and 2017 Sprint/Long. Both extract cleanly with
plain `pdftotext` (single column, no coordinate work needed) - just two different
row grammars:

  2016 Long:  "64.NAME                Country                                CC        50.39 +   0.00"
  2017 Sprint/Long: "1. Name            CCCbib C Country              12.42 + 0.24"

(2016 Sprint is a scanned image PDF with no extractable text - see QUALITY-CHECK.md.)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

FILES = {
    2016: [("results-long.pdf", "long", "2016")],
    2017: [("result-sprint.pdf", "sprint", "2017"), ("results-long.pdf", "long", "2017")],
}

CLASS_2016_RE = re.compile(r"Final class results:\s*([MW]\d{2})", re.IGNORECASE)
CLASS_2017_RE = re.compile(r"^Class\s+([MW]\d{2})\s*$", re.IGNORECASE)
# Non-finishers get no leading "N. " rank at all in this PDF - the row is just indented
# straight to the name column - so the rank group is optional here (unlike 2016, this
# source's blank-rank rows still carry a full bib/country, just no rank digit).
ROW_2017_RE = re.compile(r"^(?:(\d+)\.\s+)?(\S.*?)\s+([A-Z]{3})(\d{3,5})\s+[A-Z]\s+(\S.*?)(?:\s+(\d+\.\d{2})(?:\s*\+\s*(\d+\.\d{2}))?)?\s*$")
STATUS_TAIL_RE = re.compile(r"\b(DSQ|DISQ|DNS|DNF|MP|OT)\s*$", re.IGNORECASE)


RANK_NAME_RE = re.compile(r"^(\d+)\.(.*)$")
# pdftotext -layout loses the country column on ~25% of rows in this particular file (a
# row-reconstruction artifact, not missing source data); these columns are at fixed x
# positions throughout the document (verified across all 4 classes), so bucket on that
# directly from PyMuPDF word coordinates instead of relying on pdftotext's line-joiner.
COLUMNS_2016 = [("rank_name", 0.0), ("country", 240.0), ("code", 366.0), ("time", 450.0), ("diff", 492.0)]


def parse_2016_long(path, source_rel):
    rows, total_seen = [], 0
    current_class = None
    for pdf_row in common.pdf_rows(path):
        line = common.row_text(pdf_row)
        m = CLASS_2016_RE.search(line)
        if m:
            current_class = common.normalize_class(m.group(1))
            continue
        if not current_class:
            continue
        cells = common.bucket_row(pdf_row, COLUMNS_2016, slack=0.0)
        rn_m = RANK_NAME_RE.match(cells.get("rank_name", ""))
        # Non-finishers (DISQ/DNF/...) get no "N." rank at all - the row just starts
        # straight at the name, so a failed rank match still means "unranked row", not
        # "not a row" - but keep requiring *some* name text either way.
        if rn_m:
            rank = int(rn_m.group(1))
            name = re.sub(r"\s+", " ", rn_m.group(2)).strip()
        else:
            rank = None
            name = re.sub(r"\s+", " ", cells.get("rank_name", "")).strip()
        if not name:
            continue
        total_seen += 1
        country_text = cells.get("country", "").strip()
        time_text = cells.get("time", "").strip()
        # the status word (DISQ/DNF/...) lands in the "code" column, trailing the
        # 2-letter alpha code this source uses there, e.g. "LT DISQ" / "SE DNF".
        status_hint_m = STATUS_TAIL_RE.search(cells.get("code", ""))
        status_hint = status_hint_m.group(1) if status_hint_m else None
        country = common.normalize_country(country_text) if country_text else None
        if not country:
            continue
        code, _name = country
        time_s = common.time_to_seconds(time_text) if time_text else None
        status = common.normalize_status(status_hint, time_s is not None)
        rows.append(common.individual_row(current_class, rank, status, None, code, name, time_s, "high", source_rel))
    return rows, total_seen


def parse_2017(text, source_rel):
    rows, total_seen = [], 0
    current_class = None
    for line in text.splitlines():
        line = line.rstrip()
        m = CLASS_2017_RE.match(line.strip())
        if m:
            current_class = common.normalize_class(m.group(1))
            continue
        if not current_class:
            continue
        m = ROW_2017_RE.match(line.lstrip())
        if not m:
            continue
        total_seen += 1
        rank = int(m.group(1)) if m.group(1) else None
        name = re.sub(r"\s+", " ", m.group(2)).strip()
        bib_code = m.group(3)
        bib = m.group(4)
        time_text = m.group(6)
        # the status word (DISQ/DNF/...) lands at the tail of the country-name capture
        # when there's no time, e.g. "Portugal       MP" - group(5) isn't otherwise used
        # (country is resolved from the bib's 3-letter prefix instead, which is reliable
        # even when this group is truncated/misaligned by pdftotext's layout mode).
        status_hint_m = STATUS_TAIL_RE.search(m.group(5) or "")
        status_hint = status_hint_m.group(1) if status_hint_m else None
        country = common.normalize_country(bib_code)
        if not country:
            continue
        code, _name = country
        time_s = common.time_to_seconds(time_text) if time_text else None
        status = common.normalize_status(status_hint, time_s is not None)
        rows.append(common.individual_row(current_class, rank, status, bib, code, name, time_s, "high", source_rel))
    return rows, total_seen


def main():
    for year, files in FILES.items():
        for fname, discipline, _ in files:
            path = common.RAW / str(year) / fname
            if not path.exists():
                continue
            if year == 2016:
                rows, total_seen = parse_2016_long(path, f"{year}/{fname}")
            else:
                text = common.pdf_to_text(path)
                if not text:
                    print(f"{year} {discipline}: unreadable PDF, skipped")
                    continue
                rows, total_seen = parse_2017(text, f"{year}/{fname}")
            out = common.write_csv(year, discipline, rows, common.SPRINT_COLUMNS)
            dropped = total_seen - len(rows)
            print(f"{year} {discipline}: kept {len(rows)}/{total_seen} -> {out}" + (f"  (dropped: {dropped})" if dropped else ""))


if __name__ == "__main__":
    main()
