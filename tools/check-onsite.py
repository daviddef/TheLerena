#!/usr/bin/env python3
"""Refuse the build when a data file reaches no page and has not been declared a notebook.

WHY THIS EXISTS. On 17 September 2026 David said: "make sure anything you find is always
referenced and available on our site." He was right to press it. An audit that morning had
found that 129 of 168 TSVs were read by no build script at all - the research lived in
data/ and the reader never saw it. Findings written that same day landed straight into
that hole: the UK National Archives search, the 1999 deaths, the Devon addresses.

The fault is not that research files exist. It is that a file could go BOTH ways by
accident - neither rendered nor consciously set aside - and nobody found out.

So every data/*.tsv must now be one of exactly two things, and must SAY which:

  1. ON THE SITE. Listed in build-pages.py's export list AND imported by an .astro page,
     so a reader can actually reach it. Being in the export list alone is not enough -
     that only writes a JSON file, and a JSON nothing imports is the same silence in a
     different directory.

  2. A DECLARED NOTEBOOK. Named in data/_not-on-site.txt, which is a working log the
     archive has deliberately chosen not to publish.

Anything in neither fails the build, and the message names the file. A new finding
therefore cannot become invisible by omission - somebody has to choose.

The 129 already in the hole were grandfathered into _not-on-site.txt rather than quietly
deleted or hurriedly published. They are genuine working logs. The count sits at the top
of that file so the debt stays visible instead of dissolving into a passed gate.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
BUILD = ROOT / "tools" / "build-pages.py"
DECLARED = DATA / "_not-on-site.txt"
PAGES = ROOT / "site" / "src"


def exported():
    """The names build-pages.py turns into JSON."""
    t = BUILD.read_text(encoding="utf-8")
    m = re.search(r"for name in \((.*?)\):", t, re.S)
    return set(re.findall(r'"([^"]+)"', m.group(1))) if m else set()


def imported():
    """The JSONs an .astro file actually pulls in."""
    out = set()
    for f in PAGES.rglob("*.astro"):
        for n in re.findall(r'from\s+"[^"]*?/data/([A-Za-z0-9_.-]+)\.json"',
                            f.read_text(encoding="utf-8")):
            out.add(n)
    return out


def declared():
    if not DECLARED.exists():
        return set()
    return {l.strip() for l in DECLARED.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")}


def main():
    exp, imp, dec = exported(), imported(), declared()
    onsite, notebooks, orphans = [], [], []
    for f in sorted(DATA.glob("*.tsv")):
        n = f.stem
        if n in exp and n in imp:
            onsite.append(n)
        elif n in dec:
            notebooks.append(n)
        else:
            why = ("it is exported to JSON but no page imports it"
                   if n in exp else "no build script reads it")
            orphans.append(f"data/{n}.tsv reaches no reader - {why}")

    if orphans:
        print("  FAIL  onsite     %d data file(s) reach no reader:" % len(orphans))
        for o in orphans:
            print("          - " + o)
        print("          Either render it (add to build-pages.py AND import it in a page),")
        print("          or declare it a working log by adding its name to data/_not-on-site.txt.")
        return 1

    print(f"  ok    onsite     {len(onsite)} data file(s) on the site, "
          f"{len(notebooks)} declared working logs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
