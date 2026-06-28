"""Run every parser in sequence, regenerating all results/<year>/{sprint,long,relay}.csv
files from results/raw/. Safe to re-run any time the raw sources or parsing logic change.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import parse_xml
import parse_oe_pdf
import parse_text_pdf
import parse_relay_text_pdf
import parse_eventor_relay_pdf
import parse_lazarus_html
import parse_2016_sprint_ocr

MODULES = [
    parse_lazarus_html, parse_text_pdf, parse_oe_pdf, parse_relay_text_pdf,
    parse_eventor_relay_pdf, parse_xml, parse_2016_sprint_ocr,
]

if __name__ == "__main__":
    for mod in MODULES:
        print(f"--- {mod.__name__} ---")
        mod.main()
