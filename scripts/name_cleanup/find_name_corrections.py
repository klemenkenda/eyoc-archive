"""Detect and apply likely competitor-name misspellings across the results CSVs.

Workflow:
1. `detect` scans every results/<year>/{long,sprint,relay}.csv for competitor
   names, groups them by country, and compares them:
     - against the current IOF world ranking lists in results/iof/
       (many EYOC juniors go on to elite senior careers and show up there;
       gender is taken from which IOF file - MEN_F/WOMEN_F - a name is in),
     - against each other, to catch spellings that only disagree internally
       (e.g. one source file transliterated a name differently than another).
   Two spellings are only ever treated as the same person if they were seen
   in the same or an adjacent competition year and in a compatible class
   (M16/M18 or W16/W18, not across genders) - a bigger year gap or a gender
   mismatch means it is more likely two different competitors with similar
   names (e.g. Topias Arola, EYOC 2016-2019, vs. Topias Ahola, EYOC 2013-2014
   - two distinct real IOF-ranked Finnish athletes).
   It writes a review CSV of suggested corrections.
2. A person opens scripts/name_cleanup/name_corrections.csv, edits the
   `to_name` column where the suggestion is wrong, deletes rows that are not
   real misspellings (e.g. two different people), and sets `status` to
   `approved` for the rows that should be applied.
3. `apply` reads the reviewed file and rewrites the matching name fields in
   the results CSVs, leaving everything else untouched.

Usage:
    python scripts/name_cleanup/find_name_corrections.py detect
    python scripts/name_cleanup/find_name_corrections.py apply --dry-run
    python scripts/name_cleanup/find_name_corrections.py apply
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
IOF_DIR = RESULTS / "iof"
DEFAULT_CORRECTIONS = Path(__file__).resolve().parent / "name_corrections.csv"

INDIVIDUAL_NAME_COLUMNS = ["name"]
RELAY_NAME_COLUMNS = ["leg1_name", "leg2_name", "leg3_name"]

APPROVED_STATUSES = {"approved", "approve", "yes", "y", "ok"}

CORRECTIONS_FIELDS = [
    "status",
    "country",
    "from_name",
    "to_name",
    "reason",
    "score",
    "occurrences",
    "sample_files",
]


def normalize(name: str) -> str:
    return " ".join(name.strip().casefold().split())


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    previous = list(range(len(b) + 1))
    for i, char_a in enumerate(a, 1):
        current = [i] + [0] * len(b)
        for j, char_b in enumerate(b, 1):
            cost = 0 if char_a == char_b else 1
            current[j] = min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + cost)
        previous = current
    return previous[-1]


def is_close(a: str, b: str) -> tuple[bool, float, int]:
    """Decide whether two *normalized* names are likely the same person misspelled.

    Returns (is_close, similarity_ratio, edit_distance).

    A plain edit-distance/ratio cutoff is fooled by names that share a long
    identical surname but have short, genuinely different first names (e.g.
    "Rune Cederberg" vs. "Line Cederberg" is 2 edits apart with ~0.86 ratio -
    same ballpark as real typos like "Agnes Norgard" vs. "Agnes Noergaard").
    Distance 1 is safe on its own (one dropped/swapped letter almost never
    turns one real name into another); anything looser also needs a high
    ratio to avoid flagging two different people as a misspelling.
    """
    if a == b:
        return False, 1.0, 0
    if abs(len(a) - len(b)) > 4:
        return False, 0.0, 999
    tokens_a, tokens_b = a.split(), b.split()
    if sorted(tokens_a) == sorted(tokens_b):
        return True, 1.0, 0  # same words, different order (e.g. swapped first/last name)
    dist = levenshtein(a, b)
    if dist > 4:
        return False, 0.0, dist
    ratio = SequenceMatcher(None, a, b).ratio()
    close = dist <= 1 or ratio >= 0.93
    return close, ratio, dist


def iof_file_gender(path: Path) -> str | None:
    upper = path.name.upper()
    if "WOMEN" in upper:
        return "W"
    if "MEN" in upper:
        return "M"
    return None


def load_iof_reference() -> dict[str, dict[str, tuple[str, str | None]]]:
    """country -> {normalized_name: (original 'First Last' spelling, gender)}.

    The IOF lists are split into separate MEN/WOMEN files, so gender comes for
    free from the filename and is used to avoid matching a name against the
    wrong gender's ranking list.
    """
    reference: dict[str, dict[str, tuple[str, str | None]]] = defaultdict(dict)
    for path in sorted(IOF_DIR.glob("iof_ranking_*.csv")):
        gender = iof_file_gender(path)
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                country = (row.get("Country") or "").strip()
                first = (row.get("First Name") or "").strip()
                last = (row.get("Last Name") or "").strip()
                if not country or not (first or last):
                    continue
                full = f"{first} {last}".strip()
                reference[country][normalize(full)] = (full, gender)
    return reference


@dataclass
class Occurrence:
    count: int = 0
    files: Counter = field(default_factory=Counter)
    years: set = field(default_factory=set)
    genders: set = field(default_factory=set)


def iter_result_files():
    yield from sorted(RESULTS.glob("[0-9][0-9][0-9][0-9]/*.csv"))


def scan_occurrences() -> dict[str, dict[str, Occurrence]]:
    """country -> {exact_name_as_seen: Occurrence}."""
    occurrences: dict[str, dict[str, Occurrence]] = defaultdict(lambda: defaultdict(Occurrence))
    for path in iter_result_files():
        rel = path.relative_to(RESULTS).as_posix()
        year = int(path.parent.name)
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = reader.fieldnames or []
            columns = INDIVIDUAL_NAME_COLUMNS if "name" in fieldnames else RELAY_NAME_COLUMNS
            for row in reader:
                country = (row.get("country") or "").strip()
                if not country:
                    continue
                class_value = (row.get("class") or "").strip()
                gender = class_value[:1]  # "M16"/"M18" -> "M", "W16"/"W18" -> "W"
                for column in columns:
                    name = (row.get(column) or "").strip()
                    if not name:
                        continue
                    occurrence = occurrences[country][name]
                    occurrence.count += 1
                    occurrence.files[rel] += 1
                    occurrence.years.add(year)
                    if gender:
                        occurrence.genders.add(gender)
    return occurrences


MAX_YEAR_GAP = 1


def years_compatible(years_a: set, years_b: set) -> bool:
    """Two name spellings are only considered the same person if they were seen
    in the same year or in adjacent years. A bigger gap (e.g. one spelling only
    in 2013-2014, the other only in 2016-2019) means they are more likely two
    different competitors who happen to have similar names - see Topias Arola
    vs. Topias Ahola (FIN), two distinct real IOF-ranked athletes."""
    return any(abs(a - b) <= MAX_YEAR_GAP for a in years_a for b in years_b)


def genders_compatible(genders_a: set, genders_b: set) -> bool:
    """Classes are M16/M18/W16/W18 - the leading letter is the gender/category
    family. A junior naturally moves M16 -> M18 (or W16 -> W18), so we don't
    require the exact same class, but a spelling only ever seen racing M* and
    one only ever seen racing W* are not a typo of each other."""
    if not genders_a or not genders_b:
        return True
    return bool(genders_a & genders_b)


class UnionFind:
    def __init__(self, items):
        self.parent = {item: item for item in items}

    def find(self, item):
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, a, b):
        root_a, root_b = self.find(a), self.find(b)
        if root_a != root_b:
            self.parent[root_a] = root_b

    def groups(self) -> dict:
        result: dict = defaultdict(list)
        for item in self.parent:
            result[self.find(item)].append(item)
        return result


@dataclass
class NodeInfo:
    normalized: str
    count: int
    exact_variants: Counter
    variant_files: dict
    years: set
    genders: set
    iof_exact: str | None = None
    iof_fuzzy: tuple[str, float, int] | None = None  # (original, ratio, distance)


def build_nodes(
    country: str, exact_occurrences: dict[str, Occurrence], iof_names: dict[str, tuple[str, str | None]]
) -> dict[str, NodeInfo]:
    nodes: dict[str, NodeInfo] = {}
    for exact_name, occurrence in exact_occurrences.items():
        norm = normalize(exact_name)
        node = nodes.get(norm)
        if node is None:
            node = NodeInfo(
                normalized=norm, count=0, exact_variants=Counter(), variant_files={}, years=set(), genders=set()
            )
            nodes[norm] = node
        node.count += occurrence.count
        node.exact_variants[exact_name] += occurrence.count
        node.variant_files[exact_name] = occurrence.files
        node.years |= occurrence.years
        node.genders |= occurrence.genders

    for norm, node in nodes.items():
        node_genders = node.genders or {"M", "W"}  # unknown class -> don't filter by gender
        exact_match = iof_names.get(norm)
        if exact_match and (exact_match[1] is None or exact_match[1] in node_genders):
            node.iof_exact = exact_match[0]
            continue
        best: tuple[str, float, int] | None = None
        for iof_norm, (iof_original, iof_gender) in iof_names.items():
            if iof_gender is not None and iof_gender not in node_genders:
                continue
            close, ratio, dist = is_close(norm, iof_norm)
            if not close:
                continue
            if best is None or dist < best[2] or (dist == best[2] and ratio > best[1]):
                best = (iof_original, ratio, dist)
        node.iof_fuzzy = best
    return nodes


@dataclass
class Suggestion:
    country: str
    from_name: str
    to_name: str
    reason: str
    score: str
    occurrences: int
    sample_files: str


def cluster_country(country: str, nodes: dict[str, NodeInfo]) -> list[Suggestion]:
    union_find = UnionFind(nodes.keys())
    norms = list(nodes.keys())
    for i in range(len(norms)):
        for j in range(i + 1, len(norms)):
            close, _ratio, _dist = is_close(norms[i], norms[j])
            if not close:
                continue
            node_i, node_j = nodes[norms[i]], nodes[norms[j]]
            if years_compatible(node_i.years, node_j.years) and genders_compatible(node_i.genders, node_j.genders):
                union_find.union(norms[i], norms[j])

    suggestions: list[Suggestion] = []
    for members in union_find.groups().values():
        exact_anchors = sorted({nodes[m].iof_exact for m in members if nodes[m].iof_exact})
        fuzzy_anchors = sorted({nodes[m].iof_fuzzy[0] for m in members if nodes[m].iof_fuzzy})

        if exact_anchors:
            canonical_display = exact_anchors[0]
            reason = "iof-exact" if len(exact_anchors) == 1 else "conflict-multiple-iof-matches"
            score = "exact"
        elif fuzzy_anchors:
            canonical_display = fuzzy_anchors[0]
            reason = "iof-fuzzy" if len(fuzzy_anchors) == 1 else "conflict-ambiguous-iof-match"
            best_dist = min(nodes[m].iof_fuzzy[2] for m in members if nodes[m].iof_fuzzy)
            best_ratio = max(nodes[m].iof_fuzzy[1] for m in members if nodes[m].iof_fuzzy)
            score = f"dist={best_dist} ratio={best_ratio:.2f}"
        else:
            if len(members) < 2:
                continue  # no IOF anchor and nothing to compare against internally
            canonical_member = max(members, key=lambda m: nodes[m].count)
            canonical_display = nodes[canonical_member].exact_variants.most_common(1)[0][0]
            reason = "internal"
            score = "majority-vote"

        for member in members:
            node = nodes[member]
            for exact_variant, count in node.exact_variants.items():
                if exact_variant == canonical_display:
                    continue
                suggestions.append(
                    Suggestion(
                        country=country,
                        from_name=exact_variant,
                        to_name=canonical_display,
                        reason=reason,
                        score=score,
                        occurrences=count,
                        sample_files=", ".join(sorted(node.variant_files.get(exact_variant, {}))[:4]),
                    )
                )
    return suggestions


def detect(output_path: Path) -> None:
    iof_reference = load_iof_reference()
    occurrences = scan_occurrences()

    all_suggestions: list[Suggestion] = []
    for country, exact_occurrences in sorted(occurrences.items()):
        nodes = build_nodes(country, exact_occurrences, iof_reference.get(country, {}))
        all_suggestions.extend(cluster_country(country, nodes))

    reason_order = {
        "conflict-multiple-iof-matches": 0,
        "conflict-ambiguous-iof-match": 1,
        "iof-exact": 2,
        "iof-fuzzy": 3,
        "internal": 4,
    }
    all_suggestions.sort(
        key=lambda s: (reason_order.get(s.reason, 9), s.country, -s.occurrences, s.from_name)
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(CORRECTIONS_FIELDS)
        for suggestion in all_suggestions:
            writer.writerow(
                [
                    "",
                    suggestion.country,
                    suggestion.from_name,
                    suggestion.to_name,
                    suggestion.reason,
                    suggestion.score,
                    suggestion.occurrences,
                    suggestion.sample_files,
                ]
            )

    by_reason = Counter(s.reason for s in all_suggestions)
    print(f"Scanned {sum(len(v) for v in occurrences.values())} name occurrences across "
          f"{len(occurrences)} countries.")
    print(f"Wrote {len(all_suggestions)} suggested corrections to {output_path}")
    for reason, count in by_reason.most_common():
        print(f"  {reason}: {count}")
    if by_reason.get("conflict-multiple-iof-matches") or by_reason.get("conflict-ambiguous-iof-match"):
        print("Note: rows marked 'conflict-*' matched more than one distinct IOF athlete "
              "for that country - check these by hand before approving.")


def load_corrections(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def apply_corrections(corrections_path: Path, dry_run: bool) -> None:
    rows = load_corrections(corrections_path)
    approved = [
        row for row in rows
        if (row.get("status") or "").strip().casefold() in APPROVED_STATUSES
    ]
    if not approved:
        print(f"No approved rows found in {corrections_path} "
              f"(set status to one of {sorted(APPROVED_STATUSES)} to apply a row).")
        return

    mapping: dict[tuple[str, str], str] = {}
    for row in approved:
        country = (row.get("country") or "").strip()
        from_name = (row.get("from_name") or "").strip()
        to_name = (row.get("to_name") or "").strip()
        if not country or not from_name or not to_name:
            continue
        mapping[(country, from_name)] = to_name

    print(f"Applying {len(mapping)} approved name correction(s){' (dry run)' if dry_run else ''}.")

    total_changes = 0
    for path in iter_result_files():
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            rows_in = list(reader)
        if not rows_in:
            continue
        header = rows_in[0]
        columns = INDIVIDUAL_NAME_COLUMNS if "name" in header else RELAY_NAME_COLUMNS
        indices = [header.index(column) for column in columns if column in header]

        file_changes = 0
        for data_row in rows_in[1:]:
            if not data_row:
                continue
            country = data_row[header.index("country")].strip()
            for index in indices:
                current = data_row[index].strip()
                replacement = mapping.get((country, current))
                if replacement and replacement != current:
                    data_row[index] = replacement
                    file_changes += 1

        if file_changes:
            rel = path.relative_to(RESULTS).as_posix()
            print(f"  {rel}: {file_changes} field(s) updated")
            total_changes += file_changes
            if not dry_run:
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.writer(handle, lineterminator="\r\n")
                    writer.writerows(rows_in)

    print(f"Total fields {'that would be' if dry_run else ''} updated: {total_changes}")
    if dry_run:
        print("Dry run only - rerun without --dry-run to write the changes.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)

    detect_parser = subparsers.add_parser("detect", help="Scan results and write a review CSV of suggested corrections.")
    detect_parser.add_argument("--out", type=Path, default=DEFAULT_CORRECTIONS, help="Where to write the review CSV.")

    apply_parser = subparsers.add_parser("apply", help="Apply approved corrections from a reviewed CSV to the results CSVs.")
    apply_parser.add_argument("--in", dest="input", type=Path, default=DEFAULT_CORRECTIONS, help="Reviewed corrections CSV to read.")
    apply_parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing files.")

    args = parser.parse_args()
    if args.command == "detect":
        detect(args.out)
    elif args.command == "apply":
        apply_corrections(args.input, args.dry_run)


if __name__ == "__main__":
    main()
