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

    if not missing:
        print(f"  ok    sources    {len(used)} plate(s) read; every one is on /sources/")
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
