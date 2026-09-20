#!/usr/bin/env python3
"""Mark register rows as read off the plate, in one call per plate.

Written 21 September 2026, while walking the list that tools/transcript-only.py
produces. Doing this by hand meant a bespoke edit script per plate, and the third
one introduced a ragged row. This does the same edit the same way every time:

  * appends the film and image to the SOURCE field, with the words IMAGE READ,
    which is the marker transcript-only.py looks for;
  * appends one shared sentence to the NOTE of every row on that plate, and
    optionally a per-person sentence;
  * refuses to write anything if a name is not found, or if the edit would leave
    a row ragged or with an odd number of emphasis markers.

Usage:
    python3 tools/plate-read.py --film 007713686 --image 02847 \\
        --shared "What the plate confirmed, in one sentence." \\
        --row "Don Juan TRAIBEL::extra sentence for this person" \\
        --row "Dona Ysabel CENTENO"
"""
import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "lerena-register.tsv"
T = "\t"
SRC, NOTE = 6, 8


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--film", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--date", default="21 September 2026")
    ap.add_argument("--shared", default="")
    ap.add_argument("--row", action="append", default=[],
                    help='"Exact register name" or "Exact register name::extra sentence"')
    a = ap.parse_args()

    lines = REG.read_text(encoding="utf-8").split("\n")
    ncol = len(lines[0].split(T))
    index = {}
    for i, l in enumerate(lines):
        if l.strip() and not l.startswith("#"):
            index[l.split(T)[0]] = i

    # Resolve every name BEFORE touching anything - a half-applied plate is worse
    # than an unapplied one, because the marker then lies about which rows were read.
    targets = []
    missing = []
    for spec in a.row:
        name, _, extra = spec.partition("::")
        if name not in index:
            missing.append(name)
        else:
            targets.append((index[name], name, extra))
    if missing:
        print("REFUSING TO WRITE - these names are not in the register, exactly:")
        for m in missing:
            print("   ", repr(m))
        return 1

    cite = f" - IMAGE READ {a.date}; film {a.film} image {a.image}"
    for i, name, extra in targets:
        f = lines[i].split(T)
        while len(f) < ncol:
            f.append("")
        f[SRC] = f[SRC] + cite
        add = (" " + a.shared if a.shared else "") + (" " + extra if extra else "")
        f[NOTE] = (f[NOTE] + " " + add.strip()).strip()
        lines[i] = T.join(f)

    bad = 0
    for i, l in enumerate(lines, 1):
        if not l.strip() or l.startswith("#"):
            continue
        f = l.split(T)
        if len(f) != ncol:
            print(f"RAGGED line {i}: {len(f)} fields"); bad += 1
        for x in f:
            if x.count("***") % 2:
                print(f"ODD MARKERS line {i}: {x[:60]!r}"); bad += 1
    if bad:
        print("REFUSING TO WRITE - the edit would break the file.")
        return 1

    REG.write_text("\n".join(lines), encoding="utf-8")
    print(f"film {a.film} image {a.image}: {len(targets)} row(s) marked IMAGE READ")
    for _, name, _ in targets:
        print("   ·", name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
