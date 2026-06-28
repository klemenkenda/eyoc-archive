"""Parser for the Eventor "print view" relay result PDFs (2021-2023) - these were
exported from `eventor.orienteering.org/Events/ResultList?layout=print...` rather than
SportSoftware, so they have their own column layout: a team row ("1 Norway 1:42:35")
followed by 3 leg rows ("1. Alfred Bjoerneroed 33:26 3 33:26 3"). pdftotext -layout
misaligns these badly (same family of bug as the OE2010 PDFs); PyMuPDF word coordinates
via common.pdf_rows() read them cleanly.

Class headers appear either as their own row ("Men 18") or combined with the start-list
size on one row ("Men 16 26 starting competitors") depending on the year/file.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

FILES = {
    2021: "results-relay.pdf",
    2022: "result-relay.pdf",
    2023: "results-relay.pdf",
}

CLASS_RE = re.compile(r"^(Men|Women|M|W)\s*0*(\d{2})\b", re.IGNORECASE)
TIME_RE = re.compile(r"\b(\d{1,2}:\d{2}(?::\d{2})?)\b")
STATUS_WORDS_RE = re.compile(r"\b(disqualified|did not start|undefined|active|mispunched)\b", re.IGNORECASE)


def parse_team_line(text):
    m = re.match(r"^(\d+)\s+(.*)$", text)
    if not m:
        return None
    rank = int(m.group(1))
    rest = m.group(2)
    tm = TIME_RE.search(rest)
    if tm:
        return rank, rest[: tm.start()].strip(), common.time_to_seconds(tm.group(1))
    return rank, STATUS_WORDS_RE.sub("", rest).strip(), None


def parse_leg_line(text):
    m = re.match(r"^(\d)\.\s+(.*)$", text)
    if not m:
        return None
    leg_no = int(m.group(1))
    rest = m.group(2)
    tm = TIME_RE.search(rest)
    if tm:
        return leg_no, rest[: tm.start()].strip(), common.time_to_seconds(tm.group(1))
    return leg_no, STATUS_WORDS_RE.sub("", rest).strip(), None


def parse_file(path, source_rel):
    out_rows, total_seen = [], 0
    current_class = None
    pending = None  # dict: class, rank, code, team_label, total_time, legs

    def flush():
        nonlocal pending
        if pending is None:
            return
        status = common.normalize_status(None, pending["total_time"] is not None)
        out_rows.append(common.relay_row(
            pending["class"], pending["rank"], status, pending["code"], pending["code"],
            pending["team_label"], pending["total_time"], pending["legs"], "high", source_rel,
        ))
        pending = None

    for pdf_row in common.pdf_rows(path):
        text = common.row_text(pdf_row).strip()
        m = CLASS_RE.match(text)
        if m:
            flush()
            current_class = common.normalize_class(f"{m.group(1)}{m.group(2)}")
            continue
        if not current_class or "starting competitors" in text:
            continue

        if re.match(r"^\d\.\s", text):
            res = parse_leg_line(text)
            if res and pending is not None and len(pending["legs"]) < 3:
                _leg_no, name, leg_time = res
                pending["legs"].append((name, leg_time))
            continue

        if re.match(r"^\d+\s*/\s*\d+\s", text):
            continue  # page footer, e.g. "1 / 9 2021.08.28."
        if re.match(r"^\d+\s", text):
            res = parse_team_line(text)
            if not res:
                continue
            flush()
            total_seen += 1
            rank, team_text, total_time = res
            country = common.normalize_country(team_text)
            if not country:
                continue
            code, _name = country
            pending = {
                "class": current_class, "rank": rank, "code": code,
                "team_label": team_text, "total_time": total_time, "legs": [],
            }
    flush()
    return out_rows, total_seen


def main():
    for year, fname in FILES.items():
        path = common.RAW / str(year) / fname
        if not path.exists():
            continue
        rows, total_seen = parse_file(path, f"{year}/{fname}")
        out = common.write_csv(year, "relay", rows, common.RELAY_COLUMNS)
        dropped = total_seen - len(rows)
        print(f"{year} relay: kept {len(rows)}/{total_seen} -> {out}" + (f"  (dropped: {dropped})" if dropped else ""))


if __name__ == "__main__":
    main()
