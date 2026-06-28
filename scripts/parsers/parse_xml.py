"""Parser for IOF-XML / Eventor ResultList files.

Covers three XML flavours seen in results/raw/:
  A) Eventor's native ResultList (2019, 2021-2024 sprint/long): Result/Time as "MM:SS",
     country via Organisation/Country/Alpha3, class via EventClass/ClassShortName.
  B) Plain IOF XML 3.0 from WinSplits (2025 sprint/long/relay): Result/Time as integer
     seconds already, class via Class/Name (full name, e.g. "Men 18").
  C) IOF XML 3.0 exported from Oribos (2026 sprint/long/relay): like B but richer
     (BibNumber, Country code attribute, relay TeamMemberResult/Result/OverallResult).

Run directly: `python parse_xml.py` parses every *-eventor.xml / Long.xml / Sprint.xml /
Relay.xml under results/raw/<year>/ for years where this format applies.
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

INDIVIDUAL_FILES = {
    2019: [("Sprint-eventor.xml", "sprint"), ("Long-eventor.xml", "long")],
    2021: [("Sprint-eventor.xml", "sprint"), ("Long-eventor.xml", "long")],
    2022: [("Sprint-eventor.xml", "sprint"), ("Long-eventor.xml", "long")],
    2023: [("Sprint-eventor.xml", "sprint"), ("Long-eventor.xml", "long")],
    2024: [("Sprint-eventor.xml", "sprint"), ("Long-eventor.xml", "long")],
    2025: [("Sprint.xml", "sprint"), ("Long.xml", "long")],
    2026: [("01-sprint-results-eventor.xml", "sprint"), ("02-long-results-eventor.xml", "long")],
}
RELAY_FILES = {
    2025: "Relay.xml",
    2026: "03-relay-results-eventor.xml",
}


def strip_ns(elem):
    for e in elem.iter():
        if "}" in e.tag:
            e.tag = e.tag.split("}", 1)[1]
    return elem


def text_of(elem, path, default=None):
    found = elem.find(path)
    return found.text if found is not None and found.text else default


def country_for_person(person_el, org_el):
    """Try every known place a country code/name can live, in order of reliability."""
    nat = person_el.find("Nationality")
    if nat is not None:
        code_attr = nat.get("code")
        if code_attr:
            res = common.normalize_country(code_attr)
            if res:
                return res
        alpha3 = nat.find("Country/Alpha3")
        if alpha3 is not None and alpha3.get("value"):
            res = common.normalize_country(alpha3.get("value"))
            if res:
                return res
        if nat.text:
            res = common.normalize_country(nat.text)
            if res:
                return res
    if org_el is not None:
        country_el = org_el.find("Country")
        if country_el is not None and country_el.get("code"):
            res = common.normalize_country(country_el.get("code"))
            if res:
                return res
        alpha3 = org_el.find("Country/Alpha3")
        if alpha3 is not None and alpha3.get("value"):
            res = common.normalize_country(alpha3.get("value"))
            if res:
                return res
        name_el = org_el.find("Name")
        if name_el is not None and name_el.text:
            res = common.normalize_country(name_el.text)
            if res:
                return res
    return None


def parse_time(time_text):
    if time_text is None:
        return None
    time_text = time_text.strip()
    if not time_text:
        return None
    if time_text.isdigit():
        return int(time_text)
    return common.time_to_seconds(time_text)


def class_short_name(class_result_el):
    ec = class_result_el.find("EventClass")
    if ec is not None:
        short = text_of(ec, "ClassShortName")
        if short:
            norm = common.normalize_class(short)
            if norm:
                return norm
        name = text_of(ec, "Name")
        if name:
            norm = common.normalize_class(name)
            if norm:
                return norm
    cls = class_result_el.find("Class")
    if cls is not None:
        name = text_of(cls, "Name")
        if name:
            return common.normalize_class(name)
    return None


def parse_individual_file(path, source_rel):
    root = strip_ns(ET.parse(path).getroot())
    rows = []
    total_seen = 0
    for cr in root.findall(".//ClassResult"):
        klass = class_short_name(cr)
        if not klass:
            continue
        for pr in cr.findall("PersonResult"):
            total_seen += 1
            person = pr.find("Person")
            org = pr.find("Organisation")
            result = pr.find("Result")
            if person is None or result is None:
                continue
            country = country_for_person(person, org)
            if not country:
                continue
            code, _name = country
            family = text_of(person, "PersonName/Family") or text_of(person, "Name/Family") or ""
            given = text_of(person, "PersonName/Given") or text_of(person, "Name/Given") or ""
            name = f"{given} {family}".strip()
            bib = text_of(result, "BibNumber")
            time_s = parse_time(text_of(result, "Time"))
            rank_text = text_of(result, "ResultPosition") or text_of(result, "Position")
            rank = int(rank_text) if rank_text and rank_text.isdigit() else None
            status_el = result.find("CompetitorStatus")
            status_text = status_el.get("value") if status_el is not None else text_of(result, "Status")
            status = common.normalize_status(status_text, time_s is not None)
            rows.append(common.individual_row(klass, rank, status, bib, code, name, time_s, "high", source_rel))
    return rows, total_seen


def parse_relay_file(path, source_rel):
    root = strip_ns(ET.parse(path).getroot())
    rows = []
    total_seen = 0
    for cr in root.findall(".//ClassResult"):
        klass = class_short_name(cr)
        if not klass:
            continue
        for rank_idx, tr in enumerate(cr.findall("TeamResult"), start=1):
            total_seen += 1
            org = tr.find("Organisation")
            team_name_el = tr.find("Name")
            team_name_alt = tr.find("TeamName")
            team_label = (team_name_el.text if team_name_el is not None and team_name_el.text else None) or \
                         (team_name_alt.text if team_name_alt is not None and team_name_alt.text else None) or ""
            country = None
            if org is not None:
                country_el = org.find("Country")
                if country_el is not None and country_el.get("code"):
                    country = common.normalize_country(country_el.get("code"))
                if not country:
                    name_el = org.find("Name")
                    if name_el is not None and name_el.text:
                        country = common.normalize_country(name_el.text)
            if not country and team_label:
                country = common.normalize_country(team_label)
            if not country:
                continue
            code, _name = country

            # leg members, sorted by Leg number; pull per-leg time/name; total time/rank
            # come either from a flat TeamResult/Time (flavour B) or from the last leg's
            # OverallResult (flavour C, richer Oribos export).
            members = []
            for tmr in tr.findall("TeamMemberResult"):
                leg_no_text = text_of(tmr, "Leg") or text_of(tmr, "Result/Leg")
                leg_no = int(leg_no_text) if leg_no_text and leg_no_text.isdigit() else None
                p = tmr.find("Person")
                family = text_of(p, "Name/Family") if p is not None else None
                given = text_of(p, "Name/Given") if p is not None else None
                if family or given:
                    runner_name = f"{given or ''} {family or ''}".strip()
                else:
                    runner_name = text_of(p, "Name") if p is not None else ""
                result = tmr.find("Result")
                leg_time = parse_time(text_of(result, "Time")) if result is not None else None
                members.append((leg_no or len(members) + 1, runner_name, leg_time))
            members.sort(key=lambda m: m[0])
            legs = [(m[1], m[2]) for m in members]

            total_time = parse_time(text_of(tr, "Time"))
            rank = None
            overall = None
            if total_time is None:
                # flavour C: derive from the last leg's cumulative OverallResult
                last_tmr = None
                last_leg = -1
                for tmr in tr.findall("TeamMemberResult"):
                    leg_no_text = text_of(tmr, "Leg") or text_of(tmr, "Result/Leg")
                    leg_no = int(leg_no_text) if leg_no_text and leg_no_text.isdigit() else -1
                    if leg_no > last_leg:
                        last_leg = leg_no
                        last_tmr = tmr
                if last_tmr is not None:
                    overall = last_tmr.find("Result/OverallResult")
                    if overall is not None:
                        total_time = parse_time(text_of(overall, "Time"))
                        rtxt = text_of(overall, "Position")
                        rank = int(rtxt) if rtxt and rtxt.isdigit() else None
            if rank is None:
                rank = rank_idx

            status_el = tr.find("TeamStatus")
            status_text = status_el.get("value") if status_el is not None else text_of(tr, "Status")
            if not status_text and overall is not None:
                status_text = text_of(overall, "Status")
            status = common.normalize_status(status_text, total_time is not None)
            rows.append(common.relay_row(klass, rank, status, code, code, team_label or code, total_time, legs, "high", source_rel))
    return rows, total_seen


def main():
    for year, files in INDIVIDUAL_FILES.items():
        for fname, discipline in files:
            path = common.RAW / str(year) / fname
            if not path.exists():
                continue
            common.reset_dropped_report()
            rows, total_seen = parse_individual_file(path, f"{year}/{fname}")
            out = common.write_csv(year, discipline, rows, common.SPRINT_COLUMNS)
            dropped_n = total_seen - len(rows)
            print(f"{year} {discipline}: kept {len(rows)}/{total_seen} -> {out}" + (f"  (dropped non-European: {dropped_n})" if dropped_n else ""))

    for year, fname in RELAY_FILES.items():
        path = common.RAW / str(year) / fname
        if not path.exists():
            continue
        common.reset_dropped_report()
        rows, total_seen = parse_relay_file(path, f"{year}/{fname}")
        out = common.write_csv(year, "relay", rows, common.RELAY_COLUMNS)
        dropped_n = total_seen - len(rows)
        print(f"{year} relay: kept {len(rows)}/{total_seen} -> {out}" + (f"  (dropped non-European: {dropped_n})" if dropped_n else ""))


if __name__ == "__main__":
    main()
