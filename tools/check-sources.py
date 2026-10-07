#!/usr/bin/env python3
"""Every plate the register says was READ must appear on /sources/.

WHY THIS EXISTS. data/sources-consulted.tsv opens with this promise:

    "This file is the source of truth; /sources/ is generated from it, so the page
     cannot fall behind the work again. It did once: the table sat unchanged from
     10 to 13 Sep 2026 while three days of reading went unrecorded, under a heading
     claiming to list everything."

*** ON 22 SEPTEMBER 2026 IT HAD FALLEN BEHIND AGAIN, AND BY MORE THAN THE FIRST TIME. ***
Twenty-one of the twenty-two films the register cited as IMAGE READ were absent from it -
two whole days of plate reading - under a page still headed "Everything consulted so far".

THE SAFEGUARD HAD BEEN AIMED AT THE WRONG GAP. Generating the page from the TSV
guarantees that the PAGE matches the TSV. Nothing guaranteed that the TSV matched the
WORK, and that is the join where it broke, twice. A generated page is not a current one.

So this walks the other way: it reads the REGISTER, collects every film that a row claims
was read off a plate, and insists /sources/ can account for it. A source the archive used
and did not list is a claim the reader cannot check, which is the one thing this site says
it will never do.

It is a GATE. It exits 1.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "lerena-register.tsv"
SRC = ROOT / "data" / "sources-consulted.tsv"

FILM = re.compile(r"film\s*(\d{6,9})", re.I)
READ = re.compile(r"\bIMAGE READ\b|read off the (?:image|plate)|image was opened", re.I)
FILMIMG = re.compile(r"film\s*\d{6,9}\s*,?\s*image\s*\d{4,5}", re.I)
IMGARK = re.compile(r"3:1:[A-Z0-9-]{8,}")

# *** A THIRD LOCATOR, ADDED 8 OCTOBER 2026, AND IT IS NOT AN EXEMPTION. ***
# David sent a photograph of one opening of the Maitland Road Cemetery Record of
# Interments. It was genuinely read off an image, so READ fires - and it has no film
# number and no ark, because it never came through FamilySearch. Under the old rule the
# only ways to pass were to lie about the locator or to delete the word READ, and both
# would have made the register worse than the gate.
#
# WHAT THIS ACCEPTS INSTEAD: the register's own page and entry number, which is what a
# reader needs to order the same opening from the holding archive - plus the explicit
# words IMAGE SUPPLIED, so nobody can fall through this hole by accident. Both halves are
# required. "Supplied by the family" on its own still fails; so does a page number on a
# row that claims a film it does not name.
#
# AND THESE ARE COUNTED OUT LOUD on every passing run. A locator that cannot be resolved
# to a public image is weaker than one that can, and the build should say how many of
# them the archive is carrying rather than let them blend in.
SUPPLIED = re.compile(r"\bIMAGE SUPPLIED\b", re.I)
PAGEENTRY = re.compile(r"page\s*\d{1,5}\s*,?\s*entry\s*\d{1,4}", re.I)


def main():
    src = SRC.read_text(encoding="utf-8")
    listed = set(re.findall(r"\b(\d{6,9})\b", src))

    used = {}
    for line in REG.read_text(encoding="utf-8").split("\n"):
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split("\t")
        blob = " ".join(f[6:9]) if len(f) > 8 else " ".join(f[6:])
        if not READ.search(blob):
            continue
        for film in FILM.findall(blob):
            used.setdefault(film, []).append(f[0])

    # A film may be written 007713686 or 7713686 in either file.
    def seen(film):
        return film in listed or film.lstrip("0") in listed

    missing = {f: who for f, who in used.items() if not seen(f)}

    # *** AND A ROW THAT SAYS AN IMAGE WAS READ MUST SAY WHICH IMAGE. *** Added
    # 23 September 2026, after two rows were found claiming a plate without naming one.
    # One of them was the ENROLMENT CARD - the single most important document this
    # archive holds, whose note says "The image was opened on 10 Sep 2026" while its
    # source field said only "Argentina Military Records 1911-1936 (machine-indexed)".
    # A plate nobody can find again is a plate the reader has to take on trust, which is
    # the one thing this archive says it will never ask.
    #
    # EITHER LOCATOR SATISFIES IT: film+image, or a 3:1 image ark. Some collections give
    # a usable ark and no stable image number - the army drawer's number box and its arks
    # do not stay in step across loads, which data/cajon-985-scan.tsv records - so
    # demanding film+image everywhere would demand a number that is known to drift.
    unlocated = []
    supplied = []
    for line in REG.read_text(encoding="utf-8").split("\n"):
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split("\t")
        if len(f) < 9 or not READ.search(" ".join(f[6:9])):
            continue
        if FILMIMG.search(f[6]) or IMGARK.search(f[6]):
            continue
        if SUPPLIED.search(f[6]) and PAGEENTRY.search(f[6]):
            supplied.append(f[0])
            continue
        unlocated.append(f[0])

    if unlocated:
        print(f"  FAIL  sources    {len(unlocated)} row(s) say an image was read and do not say WHICH:")
        for n in unlocated:
            print(f"          - {n}")
        print("\n          Add film NNNNNNNNN image NNNNN, or a 3:1 image ark, to the SOURCE field.")
        return 1

    if not missing:
        extra = (f"; {len(supplied)} located by supplied page+entry, not by film"
                 if supplied else "")
        print(f"  ok    sources    {len(used)} plate(s) read; every one is on /sources/, "
              f"and every row claiming a plate names one{extra}")
        return 0

    print(f"  FAIL  sources    {len(missing)} film(s) the register says were READ appear nowhere")
    print("                    in data/sources-consulted.tsv:")
    for film, who in sorted(missing.items()):
        print(f"          - film {film}  ({len(who)} register row(s), e.g. {who[0]})")
    print("\n          A plate that was read and not listed is research the reader cannot check.")
    print("          Add a row to data/sources-consulted.tsv: source, used_for, accessed, tier, link.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
