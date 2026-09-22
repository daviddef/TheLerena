#!/usr/bin/env python3
"""Every edge of the tree must join two people this archive actually holds.

WHY THIS EXISTS. On 23 September 2026 the question "is the TREE keeping up with the
research?" was asked for the first time, and the answer was found by comparing
data/relations.tsv against data/lerena-register.tsv rather than by looking at either.

*** FOURTEEN EDGES NAMED SOMEBODY THE REGISTER DID NOT HOLD, and they failed in two
different ways that look identical from inside either file. ***

  1. THE SAME WOMAN, WRITTEN TWO WAYS. Six edges said "Sofia CLAVIJO",
     "Celedonia VILLADEMOROS" and "Dona Juliana GONZALEZ" while the register rows read
     "Sofia CLAVIJO (wife of Pedro LLERENA)", "Celedonia VILLADEMOROS (wife of Avelino
     Eduardo)" and "Dona Juliana Joaquina GONZALEZ". Those edges JOINED NOTHING. Half of
     each woman's family hung off a row that did not exist, and every page drawing the
     tree drew it that way, silently, for as long as the rows had carried their
     qualifiers.

  2. A PERSON WHO WAS SIMPLY MISSING. *** JULIA SALVANACH *** - wife of Gilberto Lerena
     and mother of seven Lerena Salvanach - had no register row at all, while BOTH HER
     PARENTS did, entered from the act that names them as her child's grandparents. The
     archive held her parents, and her children, and not her.

WHAT IT CHECKS. Both ends of every edge resolve to a register row - except names declared
in data/_tree-offsite.txt, which are people this estate keeps in another file (the Taylor,
Brayley and Booyzen side) or another archive. A declaration there is a claim that somebody
looked, and it carries where the person is held.

WHAT IT DOES NOT CHECK, on purpose. Whether an edge is TRUE. A tree that joins real rows
can still join the wrong ones, and no gate can see that - see data/_person-pairs.txt, which
is where this archive keeps the men it refuses to merge. This only refuses an edge that
joins a name to nothing at all.

It is a GATE. It exits 1.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "lerena-register.tsv"
REL = ROOT / "data" / "relations.tsv"
OFF = ROOT / "data" / "_tree-offsite.txt"


def main():
    reg = {l.split("\t")[0] for l in REG.read_text(encoding="utf-8").split("\n")
           if l.strip() and not l.startswith("#")}

    offsite = {}
    if OFF.exists():
        for line in OFF.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or ":" not in s:
                continue
            who, _, why = s.partition(":")
            offsite[who.strip()] = why.strip()

    rows = [l.split("\t") for l in REL.read_text(encoding="utf-8").split("\n")
            if l.strip() and not l.startswith("#")][1:]

    bad, undeclared = [], {}
    for i, r in enumerate(rows, 2):
        for end, label in ((r[0], "person"), (r[2] if len(r) > 2 else "", "other")):
            if not end or end in reg or end in offsite:
                continue
            bad.append(f'relations.tsv: "{end}" ({label} of a {r[1] if len(r)>1 else "?"} edge) '
                       f'is not a register row')
            undeclared[end] = undeclared.get(end, 0) + 1

    if bad:
        print(f"  FAIL  tree       {len(bad)} edge end(s) join a name to nothing:")
        for b in sorted(set(bad)):
            print(f"          - {b}")
        print("\n          Either add the person to data/lerena-register.tsv, or - if this estate")
        print("          holds them in another file or another archive - declare them in")
        print("          data/_tree-offsite.txt as \"Name: where they are held\".")
        return 1

    joined = len({r[0] for r in rows} | {r[2] for r in rows if len(r) > 2 and r[2]})
    print(f"  ok    tree       {len(rows)} edge(s) join {joined} named people; "
          f"{len(offsite)} declared off-site")
    return 0


if __name__ == "__main__":
    sys.exit(main())
