#!/usr/bin/env python3
"""Refuse the build when a reading this archive has RETRACTED is still asserted in the data.

WHY THIS EXISTS. On 17 September 2026, hunting the Mazza fault, a second shape of the
same disease turned up. The first shape was evidence in a file the build never read, so
a page said nothing was known. This is its mirror image: a correction applied only where
it showed.

David read the enrolment card off the original and reported Serie "E 3555". The page was
corrected. The correction was logged. And in data/ the old wrong number sat on, twice -

    data/enrolment-card-1908.tsv   serie  Serie  3885
    data/direct-line.tsv           '... / Serie 3885 / Seccion I 3322'

the second one inside what reads as a transcription of the card, which is the worst
place for a wrong number to hide, because it looks like the record talking.

Worse was data/racing-dynasty.tsv, which still asserted "Roque Luis Armando Lerena
married Rosalina Wilhelmina CHAPPELL... Frederick Chapell is her kin" - a claim a
SERIOUS correction had withdrawn seven days earlier - and offered it as a
CROSS-CONFIRMATION of the parish register. A retracted fact was doing corroborating work.

THE RULE THIS ENFORCES, and it is the archive's own habit made compulsory:

    A retracted reading may appear in data/ ONLY inside quotation marks.

Quoted, it is history: 'ALBERTO OCTAVIO, not "Alberto Otario" as indexed'. Bare, it is
an assertion, and the assertion is false. That rule separated all six real occurrences
from all six innocent ones on the day it was written, with nothing left over.

Opt-in by design. A correction is enforced only once someone fills its `retired` column,
so this can never go noisy on its own - guessing retired values out of English prose was
tried first and returned "child", "probably" and "Argentine".
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORR = ROOT / "data" / "corrections.tsv"


def cells(path):
    for i, line in enumerate(path.open(encoding="utf-8"), 1):
        if not line.strip() or line.startswith("#"):
            continue
        yield i, line.rstrip("\n").split("\t")


def quoted(field, at):
    """True when the match at `at` sits inside a "..." span: an odd number of quote
    marks opened before it. Cheap, and exactly right while quotes are balanced."""
    return field.count('"', 0, at) % 2 == 1


def main():
    if not CORR.exists():
        print("  ok    corrections no corrections.tsv; nothing to check")
        return 0

    rows = list(cells(CORR))
    if not rows:
        return 0
    head = rows[0][1]
    try:
        col = head.index("retired")
    except ValueError:
        print("  ok    corrections no `retired` column; nothing is enforced yet")
        return 0

    retired = {}
    for _, r in rows[1:]:
        if len(r) > col and r[col].strip():
            retired[r[col].strip()] = (r[2][:70] if len(r) > 2 else "")
    if not retired:
        print("  ok    corrections no retracted readings are being enforced yet")
        return 0

    fails = []
    for f in sorted(ROOT.glob("data/*.tsv")):
        if f.name == "corrections.tsv":
            continue          # the ledger's whole job is to quote what was wrong
        for ln, fields in cells(f):
            for ci, field in enumerate(fields):
                for token in retired:
                    at = field.find(token)
                    while at != -1:
                        if not quoted(field, at):
                            fails.append(
                                f'data/{f.name}:{ln} column {ci + 1} states "{token}" as fact. '
                                f"That reading was RETRACTED (corrections.tsv: {retired[token]}). "
                                f"Quote it or drop it - bare, it asserts what this archive took back")
                            break
                        at = field.find(token, at + 1)

    if fails:
        print("  FAIL  corrections %d retracted reading(s) still asserted:" % len(fails))
        for x in fails:
            print("          - " + x)
        return 1

    print(f"  ok    corrections {len(retired)} retracted reading(s) appear only in quotation marks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
