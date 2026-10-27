#!/usr/bin/env python3
"""Make site/src/data/ribbon-flags.json, the mini flags on every ribbon card: the story's (/story/) and every family ribbon's.
(27 October 2026; kit docs/ribbon-flags.md)

    python3 tools/build-ribbon-flags.py                write the file (the build runs this after family:data, as flags:data)
    python3 tools/build-ribbon-flags.py --check        fail, and write nothing, if the committed file is not what the data makes
    python3 tools/build-ribbon-flags.py --gate DIST    --check, then the kit's gate (checkribbonflags.py) on the cards with their
                                                       flags and on the built pages in DIST (the build runs this as check:ribbonflags)
    python3 tools/build-ribbon-flags.py --report       print every place line: the flags it draws, or why none

NOTHING HERE CHOOSES A FLAG. The kit's own generator (kit/tools/ribbonflags.py, imported, its `run`) decides every flag from:
  site/src/data/era-snapshot.json   this archive's era snapshot (the region a place is filed under, its eras)
  site/src/data/flag-countries.json this archive's own country for a place the kit will not place by itself, each entry with its
                                    evidence in the file (HAND-WRITTEN: Córdoba and Córdova la Llana are Spain's; the River Plate none)
  the kit's tables                  data/regime-flags.json, data/place-countries.json, data/flags (the Flags Atlas flags)
applied to the cards of site/src/data/story.json (hand-written) and site/src/data/family-lines.json (tools/build-family-lines.py).

WHY A FILE OF ITS OWN, AND NOT `flags` WRITTEN INTO THE CARDS AS THE KIT'S --write DOES. At kit 1fa6b54 the story's schema
(kit/data/story-schema.json, checkfamilystory S0) and the family ribbon's (family-ribbon-schema.json, checkfamilyribbon F0) do not
know a card's `flags`, so a card that carries them fails both gates; story.json is hand-written (its living card would carry a
generated field the prose gate refuses); and family-lines.json is rewritten whole by its own tool. So the flags live here, by card
position, and the two pages put them on the cards as they draw them (src/pages/story.astro, src/lib/ribbon-flags.js). The kit's
gate is run on copies of the two files with the flags put back, written outside the checkout and removed after.
"""
import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DATA = SITE / "src" / "data"
OUT = DATA / "ribbon-flags.json"
KIT_TOOLS = SITE / "node_modules" / "@daviddef" / "archive-kit" / "kit" / "tools"
NOTE = ("Made by tools/build-ribbon-flags.py with the kit's ribbonflags.py from era-snapshot.json and flag-countries.json, for the "
        "cards of story.json and family-lines.json, by position (null: no flag on that card); do not edit by hand.")


def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def kit():
    if not (KIT_TOOLS / "ribbonflags.py").exists():
        raise SystemExit("build-ribbon-flags: the kit's ribbonflags.py is not installed (npm install in site/; kit pin 1fa6b54 or later)")
    sys.path.insert(0, str(KIT_TOOLS))
    import ribbonflags  # noqa: E402
    return ribbonflags


def countries():
    return {k: v for k, v in load(DATA / "flag-countries.json").items() if not k.startswith("_")}


def make():
    """-> (the file's document, the story with flags, the families with flags, the kit's report)"""
    RF = kit()
    story, fams = load(DATA / "story.json"), load(DATA / "family-lines.json")
    for c in (story.get("ribbon") or {}).get("cards") or []:
        c.pop("flags", None)
    for f in fams.get("families") or []:
        for c in f.get("cards") or []:
            c.pop("flags", None)
    ctx = RF.context(load(DATA / "era-snapshot.json"), {}, None, countries=countries())
    rep = RF.run(ctx, story, fams)
    doc = {"_note": NOTE,
           "story": [c.get("flags") for c in (story.get("ribbon") or {}).get("cards") or []],
           "families": {f["id"]: [c.get("flags") for c in f.get("cards") or []] for f in fams.get("families") or [] if f.get("cards")}}
    return doc, story, fams, rep


def text_of(doc):
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true")
    g.add_argument("--gate", metavar="DIST")
    g.add_argument("--report", action="store_true")
    a = ap.parse_args()
    doc, story, fams, rep = make()
    if a.report:
        kit().print_report(rep)
        return 0
    if a.check or a.gate:
        cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if cur != text_of(doc):
            print("  FAIL  ribbon-flags  site/src/data/ribbon-flags.json is not what the data makes: run python3 tools/build-ribbon-flags.py")
            return 1
        n = sum(len(x or []) for x in doc["story"]) + sum(len(x or []) for v in doc["families"].values() for x in v)
        print("  ok    ribbon-flags  %d flag(s) on the story and %d family ribbon(s); the file is what the data makes"
              % (n, len(doc["families"])))
        if a.check:
            return 0
        tmp = tempfile.mkdtemp(prefix="lerena-ribbon-flags-")
        try:
            for name, d in (("story.json", story), ("family-lines.json", fams)):
                (pathlib.Path(tmp) / name).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            cmd = [sys.executable, str(KIT_TOOLS / "checkribbonflags.py"), "--snapshot", str(DATA / "era-snapshot.json"),
                   "--story", os.path.join(tmp, "story.json"), "--family-lines", os.path.join(tmp, "family-lines.json"),
                   "--countries", str(DATA / "flag-countries.json"), "--dist", str(pathlib.Path(a.gate).resolve())]
            return subprocess.run(cmd).returncode
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    OUT.write_text(text_of(doc), encoding="utf-8")
    print("build-ribbon-flags: %d flag(s) on %d card(s); place lines: %s"
          % (len(rep["cards"]), len({(c["where"], c["card"]) for c in rep["cards"]}),
             ", ".join("%s %d" % kv for kv in sorted(rep["lines"].items()))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
