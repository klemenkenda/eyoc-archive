"""Parser for the two relay result PDFs that don't fit the OE2010/OS2010 "(N)" template:

  2016 Relay: one row per team, all 3 legs inline -
    "1 201 France 117.09 HABERKORN Guilhem 38.23 GENNARO Mathis 42.16 80.39 ELIAS Guilhem 36.30 117.09"
  2017 Relay: two rows per team - a header ("18. ROM 1 Romania 128.19") then a legs row
    ("Name1 Time1 (legpl) Name2 Time2 (legpl) Name3 Time3 (legpl)"); some teams are
    DNF/MP and have no rank prefix at all.

Both extract cleanly via PyMuPDF word coordinates (common.pdf_rows) - pdftotext -layout
badly mangles 2017's column spacing (see conversation history / QUALITY-CHECK.md), which
is why 2017 relay was previously flagged "approximate" - this coordinate-based read fixes
that, so confidence is upgraded to "high" here.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

CLASS_BARE_RE = re.compile(r"^([MW]\d{2})$")
CLASS_LABEL_RE = re.compile(r"^Class\s+([MW]\d{2})$", re.IGNORECASE)

ROW_2016_RE = re.compile(
    r"^(\d+)\s+(\d+)\s+(.+?)\s+(\d+\.\d{2})\s+(.+?)\s+(\d+\.\d{2})\s+(.+?)\s+(\d+\.\d{2})\s+"
    r"(\d+\.\d{2})\s+(.+?)\s+(\d+\.\d{2})\s+(\d+\.\d{2})\s*$"
)
TEAM_2017_RANKED_RE = re.compile(r"^(\d+)\.\s+([A-Z]{3})\s+\d+\s+(?:(.+?)\s+)?(\d+\.\d{2}|MP|DNF)\s*$")
TEAM_2017_UNRANKED_RE = re.compile(r"^([A-Z]{3})\s+\d+\s+(?:(.+?)\s+)?(\d+\.\d{2}|MP|DNF)\s*$")
LEGS_2017_RE = re.compile(
    r"^(.+?)\s+(\d+\.\d{2}|MP|DNF)\s*\(\s*\d*\)\s+(.+?)\s+(\d+\.\d{2}|MP|DNF)\s*\(\s*\d*\)\s+"
    r"(.+?)\s+(\d+\.\d{2}|MP|DNF)\s*\(\s*\d*\)\s*$"
)


def t2s(text):
    if text in ("MP", "DNF", None):
        return None
    return common.time_to_seconds(text)


def parse_2016_relay(path, source_rel):
    out_rows, total_seen = [], 0
    current_class = None
    for pdf_row in common.pdf_rows(path):
        text = common.row_text(pdf_row)
        m = CLASS_BARE_RE.match(text.strip())
        if m:
            current_class = common.normalize_class(m.group(1))
            continue
        if not current_class:
            continue
        m = ROW_2016_RE.match(text)
        if not m:
            continue
        total_seen += 1
        rank = int(m.group(1))
        country = common.normalize_country(m.group(3))
        if not country:
            continue
        code, _name = country
        legs = [
            (re.sub(r"\s+", " ", m.group(5)).strip(), t2s(m.group(6))),
            (re.sub(r"\s+", " ", m.group(7)).strip(), t2s(m.group(8))),
            (re.sub(r"\s+", " ", m.group(10)).strip(), t2s(m.group(11))),
        ]
        total_time = t2s(m.group(12))
        status = common.normalize_status(None, total_time is not None)
        out_rows.append(common.relay_row(current_class, rank, status, code, code, m.group(3).strip(), total_time, legs, "high", source_rel))
    return out_rows, total_seen


def parse_2017_relay(path, source_rel):
    out_rows, total_seen = [], 0
    current_class = None
    pending = None  # (klass, rank, code, team_label, total_time)

    def flush(legs):
        nonlocal pending
        if pending is None:
            return
        klass, rank, code, team_label, total_time = pending
        status = common.normalize_status(None, total_time is not None)
        out_rows.append(common.relay_row(klass, rank, status, code, code, team_label, total_time, legs, "high", source_rel))
        pending = None

    for pdf_row in common.pdf_rows(path):
        text = common.row_text(pdf_row)
        m = CLASS_LABEL_RE.match(text.strip())
        if m:
            flush([])
            current_class = common.normalize_class(m.group(1))
            continue
        if not current_class:
            continue

        m = TEAM_2017_RANKED_RE.match(text) or TEAM_2017_UNRANKED_RE.match(text)
        if m:
            flush([])
            total_seen += 1
            if len(m.groups()) == 4:  # ranked: rank, code, name, time
                rank, code_text, team_label, total_time_text = m.groups()
                rank = int(rank)
            else:  # unranked: code, name, time
                code_text, team_label, total_time_text = m.groups()
                rank = None
            country = common.normalize_country(code_text)
            if not country:
                pending = None
                continue
            code, _name = country
            pending = (current_class, rank, code, (team_label or code_text).strip(), t2s(total_time_text))
            continue

        m = LEGS_2017_RE.match(text)
        if m and pending is not None:
            legs = [
                (re.sub(r"\s+", " ", m.group(1)).strip(), t2s(m.group(2))),
                (re.sub(r"\s+", " ", m.group(3)).strip(), t2s(m.group(4))),
                (re.sub(r"\s+", " ", m.group(5)).strip(), t2s(m.group(6))),
            ]
            flush(legs)
    flush([])
    return out_rows, total_seen


def main():
    rows, total_seen = parse_2016_relay(common.RAW / "2016" / "results-relay.pdf", "2016/results-relay.pdf")
    out = common.write_csv(2016, "relay", rows, common.RELAY_COLUMNS)
    print(f"2016 relay: kept {len(rows)}/{total_seen} -> {out}")

    rows, total_seen = parse_2017_relay(common.RAW / "2017" / "results-relay.pdf", "2017/results-relay.pdf")
    out = common.write_csv(2017, "relay", rows, common.RELAY_COLUMNS)
    print(f"2017 relay: kept {len(rows)}/{total_seen} -> {out}")


if __name__ == "__main__":
    main()
