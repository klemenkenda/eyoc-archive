"""Parser for OE2010/OS2010 SportSoftware result PDFs.

These are the "Pl ... Name ... Club/Time/Diff." text-based PDFs from 2014, 2015, 2018
(individual + relay), plus the relay-only PDFs from 2019 and 2024. pdftotext -layout
misaligns rows in some of these files (offset baselines between the name and time text
frames), so this parser reads word coordinates directly via PyMuPDF and reconstructs rows
itself - see common.pdf_rows().

Individual races: column positions come from the header row ("Pl tno Name B Na Time
Diff." or similar) - whichever columns exist that year. Relay: each team occupies one
"team" row (rank, bib, country, total time) followed by up to 3 "leg" rows (name, leg
time) - rows are told apart by whether the first token sits in the rank column.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

TIME_RE = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?$")
TIME_RE_ANYWHERE = re.compile(r"\b\d{1,2}:\d{2}(:\d{2})?\b")
CLASS_HEADER_RE = re.compile(
    r"\b(MEN|WOMEN|M|W|MIXT|MIXED|MIX)\s*0*(\d{2})?\b.*?\((\d+)\)", re.IGNORECASE
)

INDIVIDUAL_FILES = {
    2014: [("results-sprint.pdf", "sprint"), ("results-long.pdf", "long")],
    2015: [("results-sf.pdf", "sprint"), ("results-lf.pdf", "long")],
    2018: [("results-sprint.pdf", "sprint"), ("results-long.pdf", "long")],
}
RELAY_FILES = {
    2015: ["results-relay.pdf", "results-mixed_sprint_relay.pdf"],
    2018: ["results-relay.pdf"],
    2019: ["result-relay.pdf"],
    2024: ["RESULTS-RELAY-WITH-MIX.pdf"],
}

HEADER_LABEL_MAP = {
    "Pl": "rank", "tno": "bib", "Name": "name", "Club": "country",
    "Na": "country", "Nat": "country", "Time": "time",
}


def detect_class(row_text):
    m = CLASS_HEADER_RE.search(row_text)
    if not m:
        return None
    prefix, digits = m.group(1).upper(), m.group(2) or ""
    if prefix in ("MIXT", "MIXED", "MIX"):
        return "Mixed"
    return common.normalize_class(f"{prefix}{digits}")


def parse_individual_oe_pdf(path, source_rel):
    rows = common.pdf_rows(path)
    # locate the column header row
    header_idx = None
    columns = []
    for i, row in enumerate(rows):
        texts = [t for _, t in row[1]]
        if "Pl" in texts and "Name" in texts and "Time" in texts:
            header_idx = i
            for x, t in row[1]:
                key = t.rstrip(".")
                # drop the "time" anchor itself: its column boundary is unreliable for
                # longer (h:mm:ss) times, which sit far enough left to spill into the
                # country column. Instead "country" becomes a catch-all through to the
                # end of the row, and the time is pulled out of it by regex below.
                if key in HEADER_LABEL_MAP and HEADER_LABEL_MAP[key] != "time":
                    columns.append((HEADER_LABEL_MAP[key], x))
            break
    if header_idx is None or not columns:
        return [], 0
    columns.sort(key=lambda c: c[1])

    out_rows = []
    total_seen = 0
    current_class = None
    for row in rows[header_idx + 1:]:
        text = common.row_text(row)
        klass = detect_class(text)
        if klass:
            current_class = klass
            continue
        if not current_class:
            continue
        cells = common.bucket_row(row, columns)
        rank_text = cells.get("rank", "").strip()
        if not rank_text.isdigit():
            continue
        total_seen += 1
        rank = int(rank_text)
        bib = cells.get("bib", "").strip() or None
        name = re.sub(r"\s+", " ", cells.get("name", "")).strip()
        tail = re.sub(r"\s+", " ", cells.get("country", "")).strip()
        time_m = TIME_RE_ANYWHERE.search(tail)
        if time_m:
            country_text = tail[: time_m.start()].strip()
            time_text = time_m.group()
        else:
            country_text = tail
            time_text = ""
        country = common.normalize_country(country_text)
        if not country:
            continue
        code, _name = country
        time_s = common.time_to_seconds(time_text) if TIME_RE.match(time_text) else None
        status = common.normalize_status(time_text if time_s is None else None, time_s is not None)
        out_rows.append(common.individual_row(current_class, rank, status, bib, code, name, time_s, "high", source_rel))
    return out_rows, total_seen


def parse_relay_oe_pdf(path, source_rel):
    rows = common.pdf_rows(path)
    pl_x = None
    for row in rows:
        for x, t in row[1]:
            if t == "Pl":
                pl_x = x
                break
        if pl_x is not None:
            break
    if pl_x is None:
        return [], 0

    out_rows = []
    total_seen = 0
    current_class = None
    pending = None  # dict: rank,bib,country_text,total_time,legs[],status_hint

    def flush():
        nonlocal pending
        if pending is None:
            return
        country = common.normalize_country(pending["country_text"])
        if country:
            code, _name = country
            legs = [(n, t) for n, t in pending["legs"]]
            status = common.normalize_status(pending["status_hint"], pending["total_time"] is not None)
            out_rows.append(common.relay_row(
                pending["class"], pending["rank"], status, code, code,
                pending["country_text"], pending["total_time"], legs, "high", source_rel,
            ))
        pending = None

    for row in rows:
        text = common.row_text(row)
        klass = detect_class(text)
        if klass:
            flush()
            current_class = klass
            continue
        if not current_class:
            continue
        tokens = [t for _, t in row[1]]
        if not tokens:
            continue
        first_x = row[1][0][0]
        is_team_row = tokens[0].isdigit() and abs(first_x - pl_x) <= 15

        time_idx = next((i for i, t in enumerate(tokens) if TIME_RE.match(t)), None)
        if is_team_row:
            total_seen += 1
            flush()
            rank = int(tokens[0])
            rest = tokens[1:]
            bib = None
            if rest and rest[0].isdigit():
                bib = rest[0]
                rest = rest[1:]
            if time_idx is not None:
                # recompute time_idx relative to `rest` slice
                rest_time_idx = next((i for i, t in enumerate(rest) if TIME_RE.match(t)), None)
            else:
                rest_time_idx = None
            if rest_time_idx is not None:
                country_text = " ".join(rest[:rest_time_idx])
                total_time = common.time_to_seconds(rest[rest_time_idx])
                status_hint = None
            else:
                country_text = " ".join(t for t in rest if not t.isdigit())
                total_time = None
                status_hint = next((t for t in rest if t.lower() in ("mp", "dnf", "dsq", "dns")), "DNF")
            pending = {
                "class": current_class, "rank": rank, "country_text": re.sub(r"\s+", " ", country_text).strip(),
                "total_time": total_time, "legs": [], "status_hint": status_hint,
            }
        else:
            if pending is None or len(pending["legs"]) >= 3:
                continue
            if time_idx is not None:
                name = " ".join(tokens[:time_idx])
                leg_time = common.time_to_seconds(tokens[time_idx])
            else:
                name = " ".join(tokens)
                leg_time = None
            name = re.sub(r"\s+", " ", name).strip()
            if name:
                pending["legs"].append((name, leg_time))
    flush()
    return out_rows, total_seen


def main():
    for year, files in INDIVIDUAL_FILES.items():
        for fname, discipline in files:
            path = common.RAW / str(year) / fname
            if not path.exists():
                continue
            rows, total_seen = parse_individual_oe_pdf(path, f"{year}/{fname}")
            out = common.write_csv(year, discipline, rows, common.SPRINT_COLUMNS)
            dropped = total_seen - len(rows)
            print(f"{year} {discipline}: kept {len(rows)}/{total_seen} -> {out}" + (f"  (dropped: {dropped})" if dropped else ""))

    for year, fnames in RELAY_FILES.items():
        all_rows = []
        total_seen_all = 0
        for fname in fnames:
            path = common.RAW / str(year) / fname
            if not path.exists():
                continue
            rows, total_seen = parse_relay_oe_pdf(path, f"{year}/{fname}")
            all_rows.extend(rows)
            total_seen_all += total_seen
        if all_rows:
            out = common.write_csv(year, "relay", all_rows, common.RELAY_COLUMNS)
            dropped = total_seen_all - len(all_rows)
            print(f"{year} relay: kept {len(all_rows)}/{total_seen_all} -> {out}" + (f"  (dropped: {dropped})" if dropped else ""))


if __name__ == "__main__":
    main()
