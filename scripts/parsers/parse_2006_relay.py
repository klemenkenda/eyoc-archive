"""Parser for the 2006 EYOC Relay results recovered from orientacijska-zveza.si.

Source: results/raw/2006/2006_relay_{w16,w18,m16,m18,mix}.txt - plain tab-separated
text extracted (via scripts/fetch_2006_relay.py) from Excel-published HTML sheets whose
embedded legacy IE-compatibility script trips antivirus heuristics; only the stripped
text ever touched disk, so this parser reads that, not HTML.

Each file is one Excel worksheet: a few header lines, one or more class markers
("W 15-16", "mix M 16", ...), then one row per team ("rank  time  bib  Team CODE
Team CODE N") followed by 3 leg rows ("[glyph-or-repeated-total]  legnum  SI-card
name (SI-card)  leg time"). Team and leg rows are told apart by column 3 (0-indexed):
"Team ..." for a team row, a leg number (1/2/3) in column 2 for a leg row - reliable
regardless of rank/time being present. Unranked/non-finishing teams have rank blank and
"---" instead of a time; a mispunched leg has "MisPunch" instead of a time; occasional
extra trailing columns (control-code sequences, free-text notes) are ignored except for
spotting a "disq" keyword to set status.

The "mix" sheet has 4 sub-headers (mix M16/M18, Mix W16/W18 - mixed-nationality teams,
not mixed-gender) - all mapped to class "Mixed", the schema's single bonus-relay bucket,
same convention as other years' bonus Mixed Sprint Relay.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

YEAR = 2006
# The "mix" sheet (mixed-nationality bonus teams) is intentionally excluded - only the
# 4 standard classes go into relay.csv, consistent with how other years' bonus Mixed
# Sprint Relay isn't counted in the main relay table either.
SOURCE_FILES = ["2006_relay_w16.txt", "2006_relay_w18.txt", "2006_relay_m16.txt",
                 "2006_relay_m18.txt"]

CLASS_RE = re.compile(r"^(mix\s+)?([MW])\s*(?:(\d{2})-(\d{2})|(\d{2}))\s*$", re.IGNORECASE)
SI_SUFFIX_RE = re.compile(r"\s*\(\d+\)\s*$")


def detect_class(line):
    m = CLASS_RE.match(line.strip())
    if not m:
        return None
    is_mix, gender, _lo, hi, single = m.groups()
    if is_mix:
        return "Mixed"
    return common.normalize_class(f"{gender.upper()}{hi or single}")


def parse_file(path, source_rel):
    rows = []
    total_seen = 0
    current_class = None
    pending = None

    def flush():
        nonlocal pending
        if pending is None:
            return
        country = common.normalize_country(re.sub(r"^Team\s+", "", pending["club"]))
        if country:
            code, name = country
            rows.append(common.relay_row(
                pending["class"], pending["rank"], pending["status"], code, code,
                pending["team_label"], pending["total_time"], pending["legs"],
                "high", source_rel,
            ))
        pending = None

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        klass = detect_class(line)
        if klass:
            flush()
            current_class = klass
            continue
        if not current_class:
            continue

        cells = line.split("\t")
        cells += [""] * (6 - len(cells))
        col0, col1, col2, col3, col4, col5 = cells[:6]
        rest = cells[6:]

        if col3.strip().startswith("Team "):
            total_seen += 1
            flush()
            rank = int(col0) if col0.strip().isdigit() else None
            total_time = common.time_to_seconds(col1.strip())
            if total_time is not None:
                status = "OK"
            elif any("disq" in c.lower() for c in rest):
                status = "DSQ"
            else:
                status = "MP"
            pending = {
                "class": current_class, "rank": rank, "status": status,
                "club": col3.strip(), "team_label": col4.strip(),
                "total_time": total_time, "legs": [],
            }
            continue

        if pending is None or len(pending["legs"]) >= 3:
            continue
        # Leg rows' leading "time echo" cell (blank on leg 3, the glyph on leg 1, the
        # team total repeated on leg 2) is sometimes omitted from the row entirely
        # rather than emitted as an empty cell, shifting every fixed column index left
        # by one - happens inconsistently even within one file (confirmed: 2006 W18's
        # leg-3 rows). Anchor on the leg-number cell itself (always exactly "1"/"2"/"3")
        # instead of a fixed position.
        leg_idx = next((i for i, c in enumerate(cells) if c.strip() in ("1", "2", "3")), None)
        if leg_idx is None or leg_idx + 2 >= len(cells):
            continue
        name = SI_SUFFIX_RE.sub("", cells[leg_idx + 2].strip())
        leg_time = common.time_to_seconds(cells[leg_idx + 3].strip()) if leg_idx + 3 < len(cells) else None
        if name:
            pending["legs"].append((name, leg_time))
    flush()
    return rows, total_seen


def main():
    all_rows = []
    total_seen_all = 0
    for fname in SOURCE_FILES:
        path = common.RAW / str(YEAR) / fname
        if not path.exists():
            continue
        rows, total_seen = parse_file(path, f"{YEAR}/{fname}")
        all_rows.extend(rows)
        total_seen_all += total_seen
    if all_rows:
        out = common.write_csv(YEAR, "relay", all_rows, common.RELAY_COLUMNS)
        dropped = total_seen_all - len(all_rows)
        print(f"{YEAR} relay: kept {len(all_rows)}/{total_seen_all} -> {out}" + (f"  (dropped: {dropped})" if dropped else ""))


if __name__ == "__main__":
    main()
