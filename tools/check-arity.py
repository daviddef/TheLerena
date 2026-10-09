#!/usr/bin/env python3
"""Refuse the build when a register row has the wrong number of columns,
or when a data file does not end with a newline.

WHY THIS EXISTS, 9 October 2026. A person was appended to data/lerena-register.tsv
while the file's last line carried NO TRAILING NEWLINE. The new row was glued onto
the end of the previous one, making a single row of NINETEEN fields where the
header declares ten.

*** EVERY GATE IN THIS ARCHIVE PASSED. *** The build was green. The register read
correctly. And VITALINO GREGORIO PELAEZ - the groom of the 1913 dispensation, the
man that day's work was about - was not there at all: no row, no page, no slug, no
entry in people.json. He was found by hand, by checking that each person written
that day had actually been given a page.

That is the worst failure available here because it is SILENT and SUBTRACTIVE.
Every other gate catches something WRONG. Nothing caught something MISSING, because
a short file is perfectly well-formed: it parses, it renders, it passes.

*** AND THE FIRST VERSION OF THIS CHECKER WAS ITSELF WRONG. *** It asserted one
header per file and fired 179 times, because several of this archive's TSVs
deliberately carry TWO TABLES under two different headers - 1812-union-act.tsv
has a 2-column argument and a 3-column test log in one file. That is a real pattern
here and not a defect, so the rule was narrowed rather than the files changed.
A gate that would force the data to be reshaped to suit the gate is the wrong gate.

So this checks only what was actually violated, and nothing it cannot be sure of:
  1. every data TSV ends with a newline - the cause, and universal;
  2. data/lerena-register.tsv, which is one table with a fixed schema, has rows
     that all match its header.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REGISTER = DATA / "lerena-register.tsv"

bad = []

files = sorted(DATA.glob("*.tsv"))
for f in files:
    raw = f.read_bytes()
    if raw and not raw.endswith(b"\n"):
        bad.append("%s does not end with a newline - the next row appended to it "
                   "will be GLUED ONTO THE LAST ONE and the person in it will vanish" % f.name)

rows = 0
if REGISTER.exists():
    body = [(n, l.rstrip("\n")) for n, l in
            enumerate(REGISTER.read_text(encoding="utf-8").splitlines(), 1)
            if l.strip() and not l.startswith("#")]
    if body:
        want = len(body[0][1].split("\t"))
        for n, l in body[1:]:
            rows += 1
            got = len(l.split("\t"))
            if got != want:
                bad.append("lerena-register.tsv line %d has %d fields, header says %d  (%s) "
                           "- a merged row hides a person, a split row invents one"
                           % (n, got, want, l.split("\t")[0][:48]))

if bad:
    print("  FAIL  arity     %d problem(s):" % len(bad))
    for b in bad[:15]:
        print("          - %s" % b)
    sys.exit(1)

print("  ok    arity      %d register row(s) match the header; %d data file(s) end with a newline"
      % (rows, len(files)))
