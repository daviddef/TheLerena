#!/usr/bin/env python3
"""Refuse the build when evidence about a named person does not reach that person's page.

WHY THIS EXISTS. The Mazza archive kept evidence in files its person-builder never
read, so people documented several times over had pages saying nothing was known
about them. The same fault was looked for here on 17 September 2026 and found in a
different shape: this archive had no person-keyed evidence file at all, so a whole
session of records lived on topic pages while

    /people/cipriano-lerena/  said  "No relationships are recorded for this person.
                                     The source names them and nothing more."

with his wife, his three children and his parents all sitting in data/.

The data was fine. The build dropped it. Nothing refused. This refuses.

Three checks, and each one exists because the fault it catches has happened:

  1. Every person named in person-evidence.tsv must be a name the register holds.
     (build-people.py also fails on this; belt and braces, and this one names the
     file the reader has to open.)
  2. That person's rendered page must actually CARRY the evidence.
  3. That page must NOT still be asserting that nothing is recorded about them.

Check 3 is the one that matters. A page can carry evidence and still print the
old claim if the template forgets to guard it, and a reader believes the sentence.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EVID = ROOT / "data" / "person-evidence.tsv"
REL = ROOT / "data" / "relations.tsv"
PEOPLE = ROOT / "site" / "src" / "data" / "people.json"
DIST = ROOT / "site" / "dist" / "people"

MARKER = "What has been read about this person"
FALSE_CLAIM = "No relationships are recorded for this person"


def rows(path):
    if not path.exists():
        return []
    out = []
    for line in path.open(encoding="utf-8"):
        if not line.strip() or line.startswith("#"):
            continue
        out.append(line.rstrip("\n").split("\t"))
    return out[1:] if out else []


def main():
    if not EVID.exists():
        print("  ok    evidence   no person-evidence.tsv; nothing to check")
        return 0
    if not PEOPLE.exists() or not DIST.exists():
        print("  FAIL  evidence   people.json or dist/people missing — run the build first")
        return 1

    people = json.loads(PEOPLE.read_text(encoding="utf-8"))
    by_name = {p["name"]: p for p in people}

    named, fails = {}, []
    for r in rows(EVID):
        who = (r + [""])[0].strip()
        if not who:
            continue
        named.setdefault(who, 0)
        named[who] += 1

    for who, n in sorted(named.items()):
        p = by_name.get(who)
        if not p:
            fails.append(f'"{who}" is named in data/person-evidence.tsv but is not a name in '
                         f"data/lerena-register.tsv, so the evidence reaches no page")
            continue
        page = DIST / p["slug"] / "index.html"
        if not page.exists():
            fails.append(f'"{who}" has evidence but no page was built at /people/{p["slug"]}/')
            continue
        html = page.read_text(encoding="utf-8", errors="ignore")
        if MARKER not in html:
            fails.append(f'"{who}" has {n} record(s) in person-evidence.tsv but /people/{p["slug"]}/ '
                         f"does not carry them — the build is dropping the evidence")
        if FALSE_CLAIM in html:
            fails.append(f'/people/{p["slug"]}/ still says "{FALSE_CLAIM}" while {n} record(s) have '
                         f"been read about them — the page is asserting the opposite of what is held")

    # The same class of fault, in the file that had it first: relations.tsv skips
    # silently past a name the register does not hold, so an edge can be written
    # and simply never appear. Report it rather than let it vanish.
    orphan_edges = sorted({(r + [""])[0].strip() for r in rows(REL)
                           if (r + [""])[0].strip() and (r + [""])[0].strip() not in by_name})
    if orphan_edges:
        fails.append("data/relations.tsv names %d person(s) the register does not hold, so their "
                     "edges are silently dropped: %s" % (len(orphan_edges), ", ".join(orphan_edges[:6])))

    if fails:
        print("  FAIL  evidence   %d problem(s):" % len(fails))
        for f in fails:
            print("          - " + f)
        return 1

    total = sum(named.values())
    print(f"  ok    evidence   {total} record(s) about {len(named)} named person(s) reach their pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
