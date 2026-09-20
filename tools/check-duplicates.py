#!/usr/bin/env python3
"""Refuse the build when two register rows look like the same person.

WHY THIS EXISTS. On 20 September 2026 this archive found a Dominga in the 1836 Montevideo
census, published her as "a candidate, not a finding" and "attached to Sancho by nothing",
and added a new person for her - one hour after declining to add three other children
BECAUSE they might duplicate people already here.

She was already here. DOMINGA JOSEFA LLERENA FERNANDEZ, b. 13 May 1804, proved on
14 September from the Catedral act of 1827, married to the same Carvallo, with the same
daughter Lucinda standing beside her.

Every gate in this archive catches BROKEN data. Nothing caught REDUNDANT data, because a
duplicate person is perfectly well-formed: it renders, it carries evidence, it passes every
check. This is the missing one.

HOW IT DECIDES. Two rows are a suspected pair when they share a first forename AND a
canonical surname, where canonical means the seven spellings this family is known by
(LERENA, LLERENA, SERENA, GERENA, LORENA, LARENA, LERINA) all fold to one. That is
deliberately blunt: the point is to make somebody look, not to be clever.

Because a blunt rule on a register of 290 will fire on real distinct people - two Marias,
two Luises - pairs can be declared distinct in data/_distinct-people.txt, one pair per
line, "name A || name B". Declaring a pair IS A CLAIM THAT SOMEBODY COMPARED THEM, and it
carries the reason.
"""
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
PEOPLE = ROOT / "site" / "src" / "data" / "people.json"
DECLARED = ROOT / "data" / "_person-pairs.txt"

VARIANTS = ("llerena", "serena", "gerena", "lorena", "larena", "lerina")


def norm(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z ]+", " ", s)


def key(name):
    """First forename + canonical surname, or None when the row has no surname to speak of."""
    bare = norm(re.sub(r"\(.*?\)", " ", str(name)))          # drop parenthetical gloss
    words = [w for w in bare.split() if w not in
             ("don", "dona", "dn", "da", "sr", "sra", "the", "of", "and", "y", "de", "del", "la", "el")]
    if len(words) < 2:
        return None
    fore = words[0]
    sur = None
    for w in words[1:]:
        c = "lerena" if w in VARIANTS else w
        if c == "lerena" or sur is None:
            sur = c
            if c == "lerena":
                break
    return (fore, sur) if sur else None


def declared():
    if not DECLARED.exists():
        return set()
    out = set()
    for line in DECLARED.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "||" not in line:
            continue
        a, b = (x.strip() for x in line.split("||", 1))
        out.add(frozenset((a, b)))
    return out


def main():
    if not PEOPLE.exists():
        print("  ok    duplicates people.json missing - run the build first")
        return 0
    people = json.loads(PEOPLE.read_text(encoding="utf-8"))
    ok = declared()
    buckets = {}
    for p in people:
        if p.get("aliasOf"):
            continue
        k = key(p["name"])
        if k:
            buckets.setdefault(k, []).append(p["name"])

    # A shared forename on this surname is not enough - it fires 382 times on a register of
    # 290, because the family reuses Carlos, Luis, Maria and Avelino in every generation.
    # A pair must ALSO share something only the same person would share:
    #   - a spouse or associated surname appearing in both rows' text
    #   - an ark
    #   - birth years within six (a census age is routinely four out)
    # That is what the Dominga pair had: both carried CARVALLO/CARBALLO.
    by_name = {p["name"]: p for p in people}
    TOKENS = re.compile(r"[a-z]{5,}")

    def blob(p):
        return norm(" ".join(str(p.get(k) or "") for k in ("name", "note", "source", "where_found")))

    def arks(p):
        return set(re.findall(r"[0-9]:[0-9]:[A-Z0-9-]{6,}", str(p.get("note") or "") + str(p.get("source") or "")))

    def year(p):
        m = re.search(r"(1[6-9]\d\d)", str(p.get("born") or p.get("born_est") or ""))
        return int(m.group(1)) if m else None

    pairs = []
    for k, names in sorted(buckets.items()):
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = by_name[names[i]], by_name[names[j]]
                if frozenset((names[i], names[j])) in ok:
                    continue
                why = None
                shared_ark = arks(a) & arks(b)
                if shared_ark:
                    why = "the same record: " + sorted(shared_ark)[0]
                else:
                    ta, tb = set(TOKENS.findall(blob(a))), set(TOKENS.findall(blob(b)))
                    # surname-ish tokens both rows carry, ignoring the family's own spellings
                    common = {w for w in (ta & tb) if w not in VARIANTS and w != "lerena"}
                    common -= {"montevideo", "uruguay", "archive", "september", "canelones", "records",
                               "baptism", "census", "register", "daughter", "familysearch", "argentina",
                               "married", "husband", "rosario", "father", "mother", "children", "record",
                               "buenos", "aires", "spelling", "indexed", "sancho", "maria", "santa"}
                    if len(common) >= 3:
                        why = "shared terms: " + ", ".join(sorted(common)[:4])
                if why is None:
                    ya, yb = year(a), year(b)
                    if ya and yb and abs(ya - yb) <= 6:
                        why = f"birth years {ya} and {yb}, within six"
                if why:
                    pairs.append((k, names[i], names[j], why))

    if pairs and "--baseline" in sys.argv:
        hdr = [
            "# SAME-NAME PERSON PAIRS - the backlog, and the baseline this gate fires against.",
            "#",
            "# tools/check-duplicates.py flags two register rows sharing a forename and a canonical",
            "# surname AND something only the same person would share. Every pair it finds must be",
            "# listed here, so a NEW one fails the build and gets looked at while it is still fresh.",
            "#",
            "# %d PAIRS WERE ALREADY PRESENT on 20 September 2026 and are listed UNREVIEWED." % len(pairs),
            "# *** Being in this file does NOT mean a pair has been compared. *** It means the gate has",
            "# seen it. Mark one reviewed by putting the reason after a #, for example:",
            "#   Name A || Name B   # different men: one d.1878 Montevideo, one arr. Buenos Aires 1926",
            "#",
            "# The list exists because this archive added a duplicate of Dominga Josefa Llerena on the",
            "# day this checker was written - one hour after refusing to add duplicates on principle.",
            "# Every other gate here catches BROKEN data. Nothing caught REDUNDANT data, because a",
            "# duplicate person is perfectly well-formed: it renders, it carries evidence, it passes.",
            "",
        ]
        DECLARED.write_text("\n".join(hdr + ["%s || %s" % (a, b) for _, a, b, _ in pairs]) + "\n",
                            encoding="utf-8")
        print("  baselined %d pair(s) into data/_person-pairs.txt" % len(pairs))
        return 0

    if pairs:
        print("  FAIL  duplicates %d register pair(s) share a forename and a canonical surname:" % len(pairs))
        for (f, s), a, b, why in pairs[:12]:
            print(f'          - "{a}"  vs  "{b}"')
            print(f'              {why}')
        print("          NEW pair(s). Compare them, then either merge them or add each to")
        print("          data/_person-pairs.txt as \"name A || name B   # reason they are different\".")
        return 1

    print(f"  ok    duplicates {len(people)} people, no unresolved same-name pairs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
