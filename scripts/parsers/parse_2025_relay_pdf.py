"""Parser for the 2025 EYOC relay results PDF (lazarus.elte.hu archive copy of the
official OResults export, results/raw/2025/results-relay.pdf).

The Eventor-sourced results/raw/2025/Relay.xml lists TeamResult elements in a corrupted
order that does not match ascending finish time (e.g. Men16 lists HUN, the slowest crew
in that block, first), so the rank previously assigned to results/2025/relay.csv by
document position was wrong. This PDF carries the real "Plac" column and is used instead.

Layout (per class, one team block followed by up to 3 leg lines):
    Plac Name Leg time Leg pl Leg diff Time Co plac Diff
    1 FIN 1:28:34
    1. Kasper Ekonoja 29:04 1 ...
    2. Joakim Savinainen 29:04 2 +0:47 58:08 1 0 0:00
    3. Veeti Viippola 30:26 5 +2:13 1:28:34 1 0 0:00
Unranked teams print just "<CODE> mispunched" / "<CODE> disqualified" instead of a rank +
time. One Men 18 row (SVK) carries a "-12" rank and an all-zero total/leg2 time - an
artifact in the source PDF itself rather than a real result - so it's treated as MP with
only its two valid leg times kept.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

CLASS_RE = re.compile(r"^(Men|Women)\s+(\d+)\s+\d+\s+starting competitors$")
TEAM_RANKED_RE = re.compile(r"^(-?\d+)\s+([A-Z]{3})\s+(\d{1,2}:\d{2}(?::\d{2})?)(?:\s+[+-]\d+:\d{2})?$")
TEAM_UNRANKED_RE = re.compile(r"^([A-Z]{3})\s+(mispunched|disqualified)$")
LEG_RE = re.compile(r"^[123]\.\s+(.+?)\s+(\d{1,2}:\d{2}(?::\d{2})?|mispunched|disqualified)\b")

SOURCE_REL = "2025/results-relay.pdf"


def parse(path):
    out_rows, total_seen = [], 0
    current_class = None
    pending = None  # dict: rank, code, total_time, status, legs[]

    def flush():
        nonlocal pending
        if pending is None:
            return
        out_rows.append(common.relay_row(
            pending["class"], pending["rank"], pending["status"],
            pending["code"], pending["code"], pending["code"],
            pending["total_time"], pending["legs"], "high", SOURCE_REL,
        ))
        pending = None

    for pdf_row in common.pdf_rows(path):
        text = common.row_text(pdf_row).strip()

        m = CLASS_RE.match(text)
        if m:
            flush()
            current_class = common.normalize_class(f"{m.group(1)}{m.group(2)}")
            continue
        if not current_class:
            continue

        m = TEAM_RANKED_RE.match(text)
        if m:
            flush()
            total_seen += 1
            rank_text, code, time_text = m.groups()
            rank = int(rank_text)
            total_time = common.time_to_seconds(time_text)
            # the one PDF artifact (Men18 SVK, "-12 ... 0:00"): negative rank and an
            # all-zero total are not a real result - keep the team as MP with no rank.
            if rank < 0 or total_time == 0:
                rank, total_time, status = None, None, "MP"
            else:
                status = "OK"
            pending = {"class": current_class, "rank": rank, "code": code,
                       "total_time": total_time, "status": status, "legs": []}
            continue

        m = TEAM_UNRANKED_RE.match(text)
        if m:
            flush()
            total_seen += 1
            code, status_text = m.groups()
            status = "DSQ" if status_text == "disqualified" else "MP"
            pending = {"class": current_class, "rank": None, "code": code,
                       "total_time": None, "status": status, "legs": []}
            continue

        m = LEG_RE.match(text)
        if m and pending is not None and len(pending["legs"]) < 3:
            name, time_text = m.groups()
            leg_time = common.time_to_seconds(time_text) if time_text not in ("mispunched", "disqualified") else None
            # one runner's leg time prints as the bogus placeholder "0:00" (same PDF
            # artifact as the SVK/MDA team-level "0:00" totals) - not a real zero-second leg.
            if leg_time == 0:
                leg_time = None
            pending["legs"].append((name.strip(), leg_time))
    flush()
    return out_rows, total_seen


def main():
    path = common.RAW / "2025" / "results-relay.pdf"
    rows, total_seen = parse(path)
    out = common.write_csv(2025, "relay", rows, common.RELAY_COLUMNS)
    print(f"2025 relay: kept {len(rows)}/{total_seen} -> {out}")


if __name__ == "__main__":
    main()
