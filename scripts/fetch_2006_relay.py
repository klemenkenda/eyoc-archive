"""One-off fetch for the 2006 EYOC relay results (found at orientacijska-zveza.si).

The source files are Excel-published HTML with embedded legacy IE/VBScript-style
compatibility script, which trips antivirus heuristics (the host itself renamed 3 of
the 5 sheet files to "*.html-virus" years ago, and a local Sophos install deletes the
other 2 on write). To avoid ever writing that markup to disk, this fetches each sheet
into memory only, strips it down to plain text via BeautifulSoup (no script/style
tags survive), and writes just the resulting text.
"""
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

BASE = "https://orientacijska-zveza.si/datoteke/rezultati"
DEST = Path(__file__).resolve().parents[1] / "results" / "raw" / "2006"

SHEETS = {
    "W16": "2006_07_EYOC_relay_sheet001.html",
    "W18": "2006_07_EYOC_relay_sheet002.html-virus",
    "M16": "2006_07_EYOC_relay_sheet003.html-virus",
    "M18": "2006_07_EYOC_relay_sheet004.html",
    "Mix": "2006_07_EYOC_relay_sheet005.html-virus",
}


def fetch_text(url: str) -> str:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    resp.encoding = "windows-1250"
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    lines = []
    table = soup.find("table")
    rows = table.find_all("tr") if table else soup.find_all("tr")
    for tr in rows:
        cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
        if any(cells):
            lines.append("\t".join(cells))
    text = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for klass, fname in SHEETS.items():
        url = f"{BASE}/{fname}"
        text = fetch_text(url)
        out = DEST / f"2006_relay_{klass.lower()}.txt"
        out.write_text(text, encoding="utf-8")
        print(f"{klass}: {len(text.splitlines())} lines -> {out}")


if __name__ == "__main__":
    main()
