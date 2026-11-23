#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The offline gate for /forenames/ (npm run check:forenames).  (23 November 2026)

The page reads site/src/data/given-names.json, which the Archive Kit's tools/atlas_given_names.py fetches from Record Atlas (`npm run given:atlas`,
online, with --seen and --strict). A build must not need the network, so this is the same question asked of the committed files:

  1. site/src/data/given-forms-seen.json is what people.json gives (tools/build-given-forms-seen.py --check): the count of every given-name form this
     archive has met, and nothing else.
  2. Every one of those forms is in the committed catalogue: as a form of a name (a row's `langs`), or as a form the Atlas holds as a DIFFERENT name from
     the family it files near it (a row's `notSame`: Jesus is not Joseph). A form in neither is a form nobody has catalogued: the fix is
     `given_name_variants.py add` from the Record Atlas checkout and `publish`, then `npm run given:atlas`. Never a table here.
  3. The catalogue's `seen` is THIS archive's count (`seenIs`), and agrees with the file of counts for every form it holds: a catalogue fetched without --seen
     would say «attested here» of forms only another archive has met.

Matching is the kit's (accents, case and a trailing «?» are not a difference).
"""
import io
import json
import pathlib
import subprocess
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "src" / "data"


def fold(s):
    t = "".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if not unicodedata.combining(c))
    return t.strip().rstrip("?").strip()


def main():
    bad = 0
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "build-given-forms-seen.py"), "--check"], capture_output=True, text=True)
    print(r.stdout.rstrip() or r.stderr.rstrip())
    if r.returncode:
        bad += 1
    seen = json.load(io.open(DATA / "given-forms-seen.json", encoding="utf-8")).get("observed", {})
    cat = json.load(io.open(DATA / "given-names.json", encoding="utf-8"))
    if not cat.get("seenIs"):
        print("  FAIL  forenames: given-names.json carries no `seenIs`: it was fetched without --seen, so its `seen` is every archive's, not this one's")
        bad += 1
    held, different, here = {}, set(), {}
    for row in cat.get("rows", []):
        for forms in (row.get("langs") or {}).values():
            for f in forms:
                held[fold(f["form"])] = True
                here[fold(f["form"])] = max(here.get(fold(f["form"]), 0), int(f.get("seen") or 0))
        for f in row.get("notSame") or []:
            different.add(fold(f["form"]))
    mine = {}
    for form, n in seen.items():
        mine[fold(form)] = mine.get(fold(form), 0) + int(n)
    missing = sorted(k for k in mine if k not in held and k not in different)
    if missing:
        print("  FAIL  forenames: %d form(s) met in these records are in no row of the committed Atlas catalogue: %s" % (len(missing), ", ".join(missing[:40])))
        print("        fix: python3 \"../Record Atlas/scripts/given_name_variants.py\" add --family ... (with its evidence), publish, then `npm run given:atlas`")
        bad += 1
    wrong = [k for k, n in here.items() if n and n != mine.get(k, 0)]
    if wrong:
        print("  FAIL  forenames: the catalogue's `seen` disagrees with the counts of this archive for %d form(s): %s (run `npm run given:atlas`)" % (len(wrong), ", ".join(sorted(wrong)[:20])))
        bad += 1
    if not bad:
        print("  ok    forenames: %d forms met here; %d held as forms of a name, %d held as a different name; the catalogue's `seen` is this archive's (%d names, %d forms)"
              % (len(mine), sum(1 for k in mine if k in held), sum(1 for k in mine if k not in held and k in different), len(cat["rows"]), cat["totalForms"]))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
