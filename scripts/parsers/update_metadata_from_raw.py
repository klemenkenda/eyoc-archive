#!/usr/bin/env python3
"""Update EYOC metadata.json files from a local eyoc-archive clone.

Usage:
  python scripts/update_metadata_from_raw.py --repo /path/to/eyoc-archive --metadata /path/to/metadata-root

What it extracts from IOF XML when present:
  - Class/category name (M16, M18, W16, W18)
  - Course name / map-like course label if present
  - Length -> distance_km (metres converted to km when >100)
  - Climb -> elevation_m
  - NumberOfControls / Controls -> control_points

It is namespace-agnostic and conservative: if a field is missing or ambiguous, it leaves the existing value unchanged.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import xml.etree.ElementTree as ET

DISCIPLINE_ALIASES = {
    'long': ['Long.xml','long.xml','Long','long'],
    'sprint': ['Sprint.xml','sprint.xml','Sprint','sprint'],
    'relay': ['Relay.xml','relay.xml','Relay','relay'],
}
CLASSES = {'M16','M18','W16','W18'}

def local(tag: str) -> str:
    return tag.split('}',1)[-1] if '}' in tag else tag

def text_child(el, name):
    for ch in list(el):
        if local(ch.tag).lower() == name.lower() and ch.text:
            return ch.text.strip()
    return None

def num(v):
    if v is None: return None
    m = re.search(r'-?\d+(?:[.,]\d+)?', str(v))
    if not m: return None
    x = float(m.group(0).replace(',','.'))
    return int(x) if abs(x - int(x)) < 1e-9 else x

def as_km(length):
    x = num(length)
    if x is None: return None
    # IOF XML usually stores length in metres; human text may already be km.
    return round(x/1000.0, 3) if x > 100 else x

def find_class_course_xml(path: Path):
    out = {}
    try:
        root = ET.parse(path).getroot()
    except Exception:
        return out

    # IOF XML commonly uses ClassResult -> Class + Course, but we also scan
    # every element that contains a Class child and Course descendant.
    for el in root.iter():
        lname = local(el.tag)
        if lname not in {'ClassResult','ClassCourseAssignment','ClassCourse','CourseClass'}:
            continue
        cls = None
        course_el = None
        for ch in el.iter():
            if local(ch.tag) == 'Class':
                n = text_child(ch, 'Name') or (ch.text.strip() if ch.text else None)
                if n in CLASSES:
                    cls = n
            if local(ch.tag) == 'Course':
                course_el = ch
        if cls and course_el is not None:
            vals = extract_course(course_el)
            if vals:
                out.setdefault(cls, {}).update(vals)

    # Some XML files put Course inside each PersonResult/TeamResult.
    # Use first usable course per class.
    for el in root.iter():
        if local(el.tag) not in {'PersonResult','TeamResult'}:
            continue
        cls = None
        course_el = None
        for ch in el.iter():
            if local(ch.tag) == 'Class':
                n = text_child(ch, 'Name') or (ch.text.strip() if ch.text else None)
                if n in CLASSES:
                    cls = n
            if local(ch.tag) == 'Course':
                course_el = ch
        if cls and course_el is not None and cls not in out:
            vals = extract_course(course_el)
            if vals:
                out[cls] = vals
    return out

def extract_course(course_el):
    data = {}
    mapping = {
        'Name': 'map_name',
        'Length': 'distance_km',
        'Climb': 'elevation_m',
        'NumberOfControls': 'control_points',
        'Controls': 'control_points',
    }
    for ch in list(course_el):
        key = mapping.get(local(ch.tag))
        if not key or ch.text is None:
            continue
        val = ch.text.strip()
        if key == 'distance_km': val = as_km(val)
        elif key in {'elevation_m','control_points'}: val = num(val)
        if val not in (None, ''):
            data[key] = val
    return data

def update_one(meta_path: Path, repo: Path):
    meta = json.loads(meta_path.read_text(encoding='utf-8'))
    year = str(meta.get('year') or meta_path.parent.name)
    changed = False
    for disc in ['long','sprint','relay']:
        d = meta.get(disc, {})
        srcs = (d.get('source') or {}).get('raw_source_files') or []
        extracted = {}
        for rel in srcs:
            p = repo / rel
            if p.suffix.lower() == '.xml' and p.exists():
                vals = find_class_course_xml(p)
                for cls, fields in vals.items():
                    extracted.setdefault(cls, {}).update(fields)
        for cls, fields in extracted.items():
            cat = d.get('categories', {}).get(cls)
            if not cat: continue
            for k, v in fields.items():
                if k in cat and v is not None:
                    cat[k] = v
                    changed = True
            cat['extraction_status'] = 'course metadata extracted from raw XML'
            cat.setdefault('course_metadata_source', []).extend(srcs)
        if extracted:
            d['course_metadata_status'] = 'partially/fully extracted from raw XML'
    if changed:
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return changed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True, type=Path)
    ap.add_argument('--metadata', required=True, type=Path)
    args = ap.parse_args()
    changed = 0
    for meta_path in sorted(args.metadata.glob('20[0-9][0-9]/metadata.json')):
        if update_one(meta_path, args.repo):
            changed += 1
    print(f'Updated {changed} metadata files')

if __name__ == '__main__':
    main()
