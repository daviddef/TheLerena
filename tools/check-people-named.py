#!/usr/bin/env python3
"""A person this archive puts on a record must BE a person in this archive.

WHY THIS EXISTS. On 8 October 2026 David asked a simple question: "is all this making
it to our sites, persons, families charts, diagrams?" The honest answer was half no.

That day this archive proved the nine children of William Taylor and Mary Ann Hellen
Brayley from the GRO index, read the whole family's baptism series at Northam, and found
JOHN WALKER BRAILEY's 1845 registration - a man it had previously known only as a guess.
All of it reached /taylor/ and /family-papers/ as prose and tables.

*** NOT ONE OF THOSE PEOPLE WAS A PERSON. *** The register held exactly one Taylor -
Mary Septima - so eight siblings, two parents and five Braileys had no person page, no
place in the bloodline graph, and nothing on the ancestor chart. A reader could read that
Kathleen Georgina was registered at Bideford in the December quarter of 1870 and could not
click on her.

THE EXISTING GATES COULD NOT SEE IT. check:onsite asks whether a DATA FILE reaches a page;
check:tree asks whether an EDGE joins a name to nothing. Nothing asked whether a person
named in a finding had been made a person. The archive could keep discovering people and
keep failing to admit them, and every gate would stay green.

So this walks the record files and insists that every child named in one is in the
register. It is a GATE. It exits 1.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "lerena-register.tsv"

# Files that assert "this named person appears on this record".
FILES = {
    "gro-taylor-brayley-births.tsv": "child",
    "gro-brailey-temple-births.tsv": "child",
    "taylor-baptisms-northam.tsv": "child",
    "roque-infants-civil-deaths.tsv": "child",
    # Added 9 October 2026, after the same gap was found a second time: four people who
    # died on one day in 1999, researched and published on /south-africa/ since September,
    # and not one of them a person. The gate grows by being made to.
    "johannesburg-cemetery-1999.tsv": "person",
    # Added 11 October 2026, after David asked the same question a THIRD time: "are we
    # keeping every finding as a person?" The honest answer was no, and the reason this
    # gate could not see it is that every file it watched was TAYLOR, BRAYLEY or SOUTH
    # AFRICAN. The Uruguayan side - which is most of this archive - had no gate at all.
    # A measurement that day found 39 of 45 people named in one session's work had no
    # row. *** THE GATE WAS BLIND TO THE LARGER HALF OF THE REGISTER. ***
    "trinidad-flores-sweep-2026-09-27.tsv": "child",
}

# *** THE RULE, WRITTEN DOWN 11 OCTOBER 2026 BECAUSE IT HAD NEVER BEEN. ***
#
# A PERSON NAMED ON AN ACT THIS ARCHIVE HAS READ IS A PERSON IN THIS REGISTER,
# WHATEVER THEIR ROLE.
#
# Principal, parent, spouse, child, godparent, witness, declarant, notary, priest,
# physician, judge - and the other family's principals too, when our people appear
# inside their file. No role is furniture.
#
# WHY, and it is not completeness for its own sake. /method/ carries a section called
# "Search for the people standing next to the person", because that is how this archive
# has made most of its progress: Sancho Llerena was found deposing in a stranger's
# marriage investigation, and Ramon Lerena was found inside a probate filed under
# CLEMENTE GARCIA's name. If the people standing next to our people are not people, the
# method has nowhere to put its own results.
#
# WHAT WENT WRONG WITHOUT IT. On 11 October 2026 this archive admitted a Juez de Paz, a
# wedding witness and a godmother about whom nothing is known, and in the same hours left
# out Eduardo Zalduondo's own brother, four officiating clergy, two declarants, a
# certifying physician and the groom Sancho Llerena swore for. Not a policy - an unwritten
# judgement made twenty times and made differently each time.
#
# THE ONE THING THE RULE DOES NOT COVER is the living. That rule is older and it wins:
# living people are named only, with no dates, no places and no photographs, and a record
# that cannot be entered without implying a living person's details is not entered at all.
#
# Cells in those columns that are headings or summary lines, not people. Each is listed
# in full so that adding one is a deliberate act rather than a pattern that quietly grows.
NOT_PEOPLE = {
    "and the two who are not there",
    "the unnamed infant, 1932",
    # Summary lines in the Johannesburg file - they state a finding about the register
    # itself rather than naming anybody.
    "the four arks are consecutive",
    "two confirmations that cost nothing",
    "a trap in this collection, and it would have cost a century",
    # *** NOT A DODGE, AND THE REASON MATTERS. *** This cell reports a search that FAILED -
    # "swept under her own surname at last, and not found". Catherine Tertia Karon is a real
    # person, a daughter named in the 1971 death notice, but her 1999 death rests on one
    # commercial index row that the free cemetery register could not confirm. A register row
    # would have to carry either a death this archive cannot stand behind or a living person's
    # dates, and the living rule forbids the second. She stays out until the death is sourced.
    "catherine tertia karon - swept under her own surname at last, and not found",
}

STOP = {"the", "de", "la", "of", "mr", "mrs", "b", "d", "c", "jr", "snr", "unnamed", "infant",
        # "born" and "nee" join a maiden name to a married one; they are grammar, not name.
        "born", "nee", "née"}


def words(s, keep_parens=False):
    """The significant words of a name.

    *** PARENTHESES ARE DROPPED FOR A RECORD AND KEPT FOR THE REGISTER, deliberately. ***
    A record names a person once; the register row is where this archive carries the
    alternates - nicknames, married surnames, and the SPELLING A DIFFERENT SOURCE USED.
    Margaret Hellen Walker Taylor is HELLEN in the GRO index and HELEN in the Northam
    baptism register, and the place to hold both is her own row.
    """
    s = re.sub(r"\*\*\*", " ", s)
    if not keep_parens:
        s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^A-Za-z\s]", " ", s)
    return [w for w in s.lower().split() if w and w not in STOP and len(w) > 1]


def main():
    reg = []
    for line in REG.read_text(encoding="utf-8").split("\n"):
        if not line.strip() or line.startswith("#"):
            continue
        reg.append(set(words(line.split("\t")[0], keep_parens=True)))

    missing = []
    for fname, col in FILES.items():
        path = ROOT / "data" / fname
        if not path.exists():
            continue
        lines = [l for l in path.read_text(encoding="utf-8").split("\n")
                 if l.strip() and not l.startswith("#")]
        if not lines:
            continue
        hdr = lines[0].split("\t")
        if col not in hdr:
            missing.append(f"{fname}: no '{col}' column - the gate cannot check it")
            continue
        idx = hdr.index(col)
        for l in lines[1:]:
            f = l.split("\t")
            if len(f) <= idx:
                continue
            cell = f[idx].strip()
            flat = re.sub(r"\*\*\*", "", cell).strip().strip(",").lower()
            if not cell or flat in NOT_PEOPLE:
                continue
            w = set(words(cell))
            if not w:
                continue
            if not any(w <= r for r in reg):
                shown = cell.replace("***", "").strip()
                missing.append(f"{fname}: '{shown}'")

    if missing:
        print(f"  FAIL  named      {len(missing)} person(s) put on a record and never made a person:")
        for m in missing:
            print(f"          - {m}")
        print("\n          A reader who can read that someone was registered should be able to")
        print("          click on them. Add the row to data/lerena-register.tsv, wire the")
        print("          parents in data/relations.tsv, or declare the cell in NOT_PEOPLE.")
        return 1

    n = sum(1 for f in FILES if (ROOT / "data" / f).exists())
    print(f"  ok    named      every person named on a record in {n} file(s) is in the register")
    return 0


if __name__ == "__main__":
    sys.exit(main())
