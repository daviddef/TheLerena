#!/usr/bin/env python3
"""Check the register against itself.

No external source: only dates and relationships that cannot all be true at once.
The sibling archives (Blazevic, Booyzen) have carried a check like this for a while;
the Lerena archive did not, and on 13 September 2026 it cost three published errors
in one day - Ema Sixta "c.1880" when three records said 1876, Julia "c.1844" when her
baptism says 1842, and two siblings indexed as born in February and July of 1843.

The third is the one this file exists for: nothing external is needed to see it.

Ordered by how badly the archive would be embarrassed to publish it.
"""
import json, re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
people = json.loads((ROOT / "site/src/data/people.json").read_text(encoding="utf-8"))
# An alias row is the SAME person under a spelling a machine produced. It shares its
# subject's dates and parents by design, so it contradicts them by design too.
people = [p for p in people if not p.get("aliasOf")]

def year(s):
    """First 4-digit year in a date string, or None. Handles 1884-09-13, c.1880, 1875."""
    if not s or s == "-":
        return None
    m = re.search(r"\b(1[5-9]\d\d|20\d\d)\b", str(s))
    return int(m.group(1)) if m else None

def full(s):
    """(y, m, d) when the field carries a real date, else None."""
    m = re.match(r"^\s*(1[5-9]\d\d|20\d\d)-(\d\d)-(\d\d)\s*$", str(s or ""))
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None

def months(a, b):
    return abs((a[0] - b[0]) * 12 + (a[1] - b[1]))

hard, soft = [], []
by_name = {p["name"]: p for p in people}

# 1. A parent who is younger than their child, or too young to be one.
for p in people:
    cy = year(p.get("born"))
    for key in ("father", "mother"):
        par = p.get(key)
        if not par:
            continue
        tgt = by_name.get(par["name"] if isinstance(par, dict) else par)
        if not tgt:
            continue
        py = year(tgt.get("born"))
        if cy and py and cy - py < 13:
            hard.append(f"{p['name']} (b.{cy}) is {cy-py} years younger than their {key} "
                        f"{tgt['name']} (b.{py})")

# 2. Full siblings born too close together to both be right.
kids = collections.defaultdict(list)
for p in people:
    for key in ("father", "mother"):
        par = p.get(key)
        if par:
            kids[(key, par["name"] if isinstance(par, dict) else par)].append(p)
seen = set()
for (key, parent), group in kids.items():
    for i, a in enumerate(group):
        for b in group[i + 1:]:
            fa, fb = full(a.get("born")), full(b.get("born"))
            if not (fa and fb):
                continue
            pair = tuple(sorted([a["name"], b["name"]]))
            if pair in seen:
                continue
            gap = months(fa, fb)
            if gap < 9:
                seen.add(pair)
                hard.append(f"{a['name']} (b.{a['born']}) and {b['name']} (b.{b['born']}) share a "
                            f"{key} ({parent}) but are only {gap} months apart - both cannot be right")

# 3. A date field that carries a hedge and a precise date at once.
for p in people:
    b = str(p.get("born") or "")
    if re.match(r"^\s*c\.", b) and re.search(r"-\d\d-\d\d", b):
        soft.append(f"{p['name']} has a hedged AND precise birth: {b!r}")

# 4. A row claiming an image was read but carrying no ark anywhere.
for p in people:
    src = (p.get("source") or "") + " " + (p.get("note") or "")
    if re.search(r"IMAGE READ|image read", src) and "ark" not in src.lower():
        soft.append(f"{p['name']} says an image was read but names no ark")

print(f"{len(people)} people checked")
if hard:
    print(f"\n{len(hard)} CONTRADICTION(S) - these cannot all be true:")
    for h in hard:
        print("   ", h)
if soft:
    print(f"\n{len(soft)} thing(s) to look at:")
    for s in soft:
        print("   ", s)
if not hard and not soft:
    print("nothing contradicts itself")
sys.exit(1 if hard else 0)
