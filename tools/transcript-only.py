#!/usr/bin/env python3
"""Which people in this register have never been seen on a plate.

WHY THIS EXISTS, and it is one day old. On 21 September 2026 three register rows -
HERMENEGILDA CAROLINA GAVARRO and her parents GERONIMO GAVARRO and CAROLINA JUAREZ -
turned out to carry surnames no human had ever read. The 1892 marriage act was recorded
as "FULL-TEXT TRANSCRIPT READ", which means A MACHINE READ IT, and the image was never
opened. It is GAVAZZO and SUAREZ, on the plate, corroborated by a second image
forty-eight years later.

THE POINT IS NOT THAT THE TRANSCRIPT WAS BAD. It had the dates right, the ages right,
the dispensation right, and the relationships right. It was wrong about exactly the
thing a machine is worst at and a reader is best at: an unfamiliar proper noun. And
this archive's own standing rule already says so - "never exclude on an index alone;
open the image" - which is a rule it had not kept on more than half the rows here. The count below is live.

WHAT THIS RANKS BY, and it is not row count. It is ARKS. One image can carry six
people, so opening one plate can move six rows at once. A page with a single dependent
row is a smaller purchase than a page with eight.

WHAT IT IS NOT. Not a gate, and it exits 0. A transcript-only row is not an error - it
is a row whose proper nouns have never been checked, which is a different and quieter
thing. Rows with no source citation at all are reported separately, because those are
not transcript-only, they are unsourced.

Usage:  python3 tools/transcript-only.py [--all] [--names]
"""
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "lerena-register.tsv"

SHOW_ALL = "--all" in sys.argv
NAMES = "--names" in sys.argv

ARK = re.compile(r"3:1:[A-Z0-9-]{8,}")
FILM = re.compile(r"film\s*(\d{6,9})\s*,?\s*image\s*(\d{4,5})", re.I)
TRANSCRIPT = re.compile(r"FULL-?TEXT TRANSCRIPT READ", re.I)
# THE MARKER IS "IMAGE READ", and this tool can only see the words the register uses.
# Its first run reported ALFREDO JUSTINIANO LERENA TRAIBEL as never seen on a plate. His
# row says "Re-read off the image 20 September: film 007713686 image 2847". The row was
# right and the tool was wrong, so the alternatives are matched here - and the real fix
# is that the register should write IMAGE READ every time, because a checker cannot know
# every way a sentence can mean it. If a row is listed below that you know was read, the
# fault is in the row's wording, and the row is the thing to fix.
IMAGE = re.compile(r"\bIMAGE READ\b|read off the (?:image|plate)|image was opened", re.I)


def rows():
    lines = [l.rstrip("\n") for l in REG.open(encoding="utf-8")
             if l.strip() and not l.startswith("#")]
    hdr = lines[0].split("\t")
    for l in lines[1:]:
        c = (l.split("\t") + [""] * len(hdr))[:len(hdr)]
        yield dict(zip(hdr, c))


def main():
    seen_on_plate, transcript_only, unsourced = [], [], []
    by_ark = collections.defaultdict(list)

    for r in rows():
        name = r.get("name", "")
        blob = " ".join([r.get("source", ""), r.get("note", "")])
        if IMAGE.search(blob):
            seen_on_plate.append(name)
            continue
        if TRANSCRIPT.search(blob):
            transcript_only.append(name)
            # Attribute the row to every plate it names, so the ranking below counts
            # how many rows ONE image would settle.
            keys = set(ARK.findall(r.get("source", "")))
            keys |= {f"film {f} image {i}" for f, i in FILM.findall(r.get("source", ""))}
            for k in (keys or {"(no ark or film cited)"}):
                by_ark[k].append(name)
            continue
        if not r.get("source", "").strip() or r.get("source", "").strip() == "-":
            unsourced.append(name)

    total = len(seen_on_plate) + len(transcript_only) + len(unsourced)
    print(f"TRANSCRIPT-ONLY PEOPLE — {len(transcript_only)} of {total} classified row(s) rest on a")
    print(f"machine transcript that no reader has checked against the plate. "
          f"{len(seen_on_plate)} have been seen on one.\n")

    ranked = sorted(by_ark.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    shown = ranked if SHOW_ALL else ranked[:12]
    print("  Ranked by what ONE image would settle:\n")
    for key, people in shown:
        print(f"  {len(people):3}  {key}")
        if NAMES or len(people) <= 3:
            for p in people:
                print(f"         · {p}")
    if not SHOW_ALL and len(ranked) > 12:
        print(f"\n  ... and {len(ranked) - 12} more plate(s). Pass --all to see them, --names for who.")

    if unsourced:
        print(f"\n  ?  {len(unsourced)} row(s) cite no source at all, which is a different problem:")
        for p in unsourced[:8]:
            print(f"         · {p}")

    print("\n" + "-" * 74)
    print("A transcript-only row is NOT an error. It is a row whose PROPER NOUNS have never")
    print("been read by a human, and a machine is worst at exactly those. Three surnames in")
    print("this register were wrong for a week for that reason, and the dates beside them")
    print("were right the whole time.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
