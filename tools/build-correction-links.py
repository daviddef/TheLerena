#!/usr/bin/env python3
"""The places the Corrections page may link in its prose, with the flag of the state that held each in the year a sentence names.
(17 November 2026; kit docs/corrections.md, "Places and shared names")

    python3 tools/build-correction-links.py            write site/src/data/correction-places.json
    python3 tools/build-correction-links.py --check    fail, and write nothing, if the committed file is not what the data makes

Nothing is chosen by hand. The rows are the place pages this archive already publishes (site/src/data/places.json), cut down to the
ones that name ONE place plainly and carry three or more people: a page called "Montevideo / Canelones", "Montevideo, later Buenos Aires",
"Buenos Aires — arrivals" or "Montevideo, calle San Juan No 60" is a note on a place, not a place a sentence names. A place is matched
by the part of its page name before the first comma ("Trinidad, Flores" -> "Trinidad"). A page whose whole name is that word owns it
("Montevideo" over "Montevideo, San Francisco de Asis"); otherwise a short name that two place pages share (Rosario of Santa Fe and Rosario of
Colonia) is dropped everywhere, so a sentence about the Uruguayan Rosario is never sent to the Argentine one. A word that flag-countries.json says means a place elsewhere (Cordoba, which that file files under Spain)
is not linked either, because the page of that spelling is another place. The flags are the kit's own placeflags.py over this archive's era snapshot and flag-countries.json, exactly
as the ribbon cards' flags are (tools/build-ribbon-flags.py); where the snapshot is silent for a place, the link has no flag.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "src" / "data"
OUT = DATA / "correction-places.json"
KIT_TOOLS = ROOT / "site" / "node_modules" / "@daviddef" / "archive-kit" / "kit" / "tools"
MIN_PEOPLE = 3
NOT_A_PLACE = re.compile(r"( / | or | then | later | and |\d|calle|arrivals|—)", re.I)
NOTE = ("Made by tools/build-correction-links.py from places.json, era-snapshot.json and flag-countries.json with the kit's placeflags.py; "
        "do not edit by hand.")


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).casefold()


def archive_ambiguous():
    """Names this archive's own hand-written flag-countries.json says mean a place elsewhere than the page of that spelling (Cordoba, in Spain here)."""
    d = json.loads((DATA / "flag-countries.json").read_text(encoding="utf-8"))
    return {fold(main_name(k)) for k in d if not k.startswith("_")}


def main_name(full):
    return full.split(",")[0].strip()


def build():
    places = json.loads((DATA / "places.json").read_text(encoding="utf-8"))
    clean = [p for p in places if p.get("name") and p.get("slug") and not NOT_A_PLACE.search(p["name"])]
    owners = {}
    for p in clean:
        owners.setdefault(main_name(p["name"]), set()).add(p["slug"])
    for p in clean:           # the page called exactly "Montevideo" owns the word; "Montevideo, San Francisco de Asis" is a place inside it
        if p["name"] == main_name(p["name"]):
            owners[p["name"]] = {p["slug"]}
    held = archive_ambiguous()
    rows = []
    for p in sorted(clean, key=lambda x: x["slug"]):
        m = main_name(p["name"])
        if p.get("count", 0) < MIN_PEOPLE or len(owners[m]) != 1 or p["slug"] not in owners[m] or len(m) < 3 or fold(m) in held:
            continue
        rows.append({"name": m, "href": f"/places/{p['slug']}/", "flagKey": p["name"]})
    if not (KIT_TOOLS / "placeflags.py").exists():
        raise SystemExit("build-correction-links: the kit's placeflags.py is not installed (npm install in site/; kit pin eb8ce42 or later)")
    with tempfile.TemporaryDirectory(prefix="lerena-place-flags-") as tmp:
        pf, outf = pathlib.Path(tmp) / "places.json", pathlib.Path(tmp) / "flags.json"
        pf.write_text(json.dumps([{"name": r["flagKey"]} for r in rows], ensure_ascii=False), encoding="utf-8")
        cp = subprocess.run([sys.executable, str(KIT_TOOLS / "placeflags.py"), "--snapshot", str(DATA / "era-snapshot.json"),
                             "--places", str(pf), "--countries", str(DATA / "flag-countries.json"), "--out", str(outf)],
                            capture_output=True, text=True)
        if cp.returncode:
            raise SystemExit("build-correction-links: placeflags.py failed: " + (cp.stderr or cp.stdout))
        flags = json.loads(outf.read_text(encoding="utf-8"))
        print("  " + cp.stdout.strip())
    return {"_note": NOTE, "rows": rows, "flags": flags}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    text = json.dumps(build(), indent=1, ensure_ascii=False) + "\n"
    if a.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("  FAIL  correction-places  site/src/data/correction-places.json is not what the data makes: run python3 tools/build-correction-links.py")
            return 1
        print("  ok    correction-places  the file is what the data makes")
        return 0
    OUT.write_text(text, encoding="utf-8")
    d = json.loads(text)
    print(f"build-correction-links: {len(d['rows'])} place(s) may be linked in a correction, {len(d['flags'])} with a flag")
    return 0


if __name__ == "__main__":
    sys.exit(main())
