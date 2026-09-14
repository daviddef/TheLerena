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
import unicodedata
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

# 2b. The same check again, for the 87% of the register that carries NO structured parent.
# On 14 September 2026 check 2 printed a clean bill of health over 31 of 246 people while the
# contradiction this file was written for sat in the data. A test that can only see an eighth of
# the register and still says "nothing contradicts itself" manufactures confidence.
#
# Spanish naming gives a second key for free: "LERENA LENGUAS" means a Lerena father and a Lenguas
# mother, so everyone carrying the same pair of surnames is a sibling or a first cousin. Cousins
# make this SOFT rather than hard - it reports, it does not fail the build.
def compound(nm):
    # Two consecutive capitalised surnames, the first the family name. "Alejandro LERENA TRAIBEL".
    m = re.search(r"\b([A-Z]{3,})\s+([A-Z][a-zA-Z]{2,}|[A-Z]{3,})\b", re.sub(r"\(.*?\)", "", nm))
    if not m:
        return None
    a, b = m.group(1), m.group(2).upper()
    return (a, b) if a != b else None

cohorts = collections.defaultdict(list)
for p in people:
    c = compound(p["name"])
    if c and full(p.get("born")):
        cohorts[c].append(p)
for c, group in cohorts.items():
    for i, a in enumerate(group):
        for b in group[i + 1:]:
            pair = tuple(sorted([a["name"], b["name"]]))
            if pair in seen:
                continue
            gap = months(full(a["born"]), full(b["born"]))
            if gap < 9:
                seen.add(pair)
                soft.append(f"{a['name']} (b.{a['born']}) and {b['name']} (b.{b['born']}) both read as "
                            f"{c[0]} {c[1]} but are only {gap} months apart - siblings this close cannot "
                            f"both be right, and first cousins would explain it")

# 2c. And a THIRD key, because 2b only reaches people whose own NAME carries two surnames.
# On 14 September 2026 checks 2 and 2b together saw 31 structured + 56 compound of 265, and the
# register was still mostly invisible to them. But 94 people have a parent NAMED IN PROSE - the acts
# this archive transcribes say "hijo legitimo de X y de Y", and the English rows say "daughter of X".
# Two children who CITE THE SAME PARENT are siblings, and that needs no link to a register row at all,
# which is the point: the cited parent usually is not in the register.
PARTICLE = {"de", "del", "la", "las", "los", "y", "e", "da", "do", "dos"}
TITLE = re.compile(r"^(d|dn|da|don|dona|doa|sr|sra|srta|mr|mrs|miss)\.?$", re.I)

def _fold(t):
    t = unicodedata.normalize("NFD", str(t))
    return "".join(c for c in t if unicodedata.category(c) != "Mn")

def namehead(span):
    """Only the leading run of name-like tokens. The prose that follows a name is not a name -
    without this, one key came out as 'gilberto 1854" with a birth of 1869 - which would have'."""
    out = []
    for raw in _fold(span).replace('"', " ").replace("'", " ").split():
        tok = raw.strip(",;:")
        if not tok:
            break
        if TITLE.match(tok):
            continue
        if re.fullmatch(r"\(?1[6-9]\d\d\)?", tok):        # a disambiguating year, "Gilberto (1854)"
            out.append(tok.strip("()"))
            continue
        if tok.lower() in PARTICLE:
            if not out:
                break
            out.append(tok.lower())
            continue
        if re.fullmatch(r"[A-Z][A-Za-z-]+\.", tok):          # sentence ended: "...Felisa. CEMLA"
            out.append(tok[:-1])
            break
        if re.fullmatch(r"[A-Z][A-Za-z.-]+", tok):
            out.append(tok)
        else:
            break
        if len(out) >= 6:
            break
    while out and out[-1] in PARTICLE:
        out.pop()
    return " ".join(out).lower()

CITES = (r"\bhij[oa]s?\s+(?:leg[i\u00ed]tim[oa]s?\s+)?de\s+(.{4,90})",
         r"\b(?:son|daughter|child)\s+of\s+(.{4,90})")
cited = collections.defaultdict(list)
for p in people:
    blob = " ".join(str(p.get(k) or "") for k in ("note", "source", "where"))
    own = set(_fold(p["name"]).lower().replace("(", " ").replace(")", " ").split())
    for pat in CITES:
        for m in re.finditer(pat, blob, re.I):
            head = namehead(m.group(1))
            if not head:
                continue
            # An act quoted on the PARENT's own row names that parent. Without this, Sancho came
            # out as his own child, in a cohort with his wife.
            if len([t for t in head.split() if t in own and t not in PARTICLE]) >= 2:
                continue
            if len(head.split()) < 2:            # a bare forename needs the child's surname to be a key
                head += " | " + (_fold(p["name"]).lower().split() or ["?"])[-1]
            cited[head].append(p)
for parent, group in cited.items():
    if len(group) < 2:
        continue
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
                soft.append(f"{a['name']} (b.{a['born']}) and {b['name']} (b.{b['born']}) are both "
                            f"recorded as children of '{parent}' but are only {gap} months apart")

# 2d. A FOURTH key: who a person is said to have MARRIED.
# Checks 2, 2b and 2c all ask "are these two people siblings". None of them can see the other
# structural fact the prose carries in quantity: 57 of 268 rows say who somebody married, as
# "m. X", "married X", "c.c. X", "esposa de X" or "viuda de X".
#
# Two DIFFERENT rows naming the SAME spouse is either an ordinary remarriage - Luis Lerena had
# two wives and both are here - or the same man entered twice under two spellings of a surname
# that this archive has documented in seven forms. The second is a real error this archive has
# actually made: "Dona Sixta LENGUAS" and "Dona Sixta LENGUAS Gonzalez" were one woman on two
# rows, written hours apart. So this reports, and does not fail the build.
SPOUSE = (r"\bm\.\s+([A-Z].{3,50})", r"\bmarried\s+(?:to\s+)?([A-Z].{3,50})",
          r"\bc\.c\.\s*([A-Z].{3,50})", r"\besposa de\s+([A-Z].{3,50})",
          r"\bviuda de\s+([A-Z].{3,50})", r"\bwife of\s+([A-Z].{3,50})",
          r"\bwidow of\s+([A-Z].{3,50})")
# A row's prose routinely mentions OTHER people's marriages, and an unrestricted match reports
# them as the subject's own. Measured on 14 September 2026: four findings, of which three were
# that mistake. The subject's own marriage is stated FIRST - the two real ones sat at offset 0,
# the three false ones at 163, 291 and 385 - so only the opening of the NOTE counts.
SPOUSE_WINDOW = 120
spouses = collections.defaultdict(list)
for p in people:
    blob = str(p.get("note") or "")[:SPOUSE_WINDOW]
    own = set(_fold(p["name"]).lower().replace("(", " ").replace(")", " ").split())
    for pat in SPOUSE:
        for m in re.finditer(pat, blob):
            head = namehead(m.group(1))
            if len(head.split()) < 2:
                continue
            # "m. X" on X's OWN row names the other party, not themselves.
            if len([t for t in head.split() if t in own and t not in PARTICLE]) >= 2:
                continue
            spouses[head].append(p["name"])
# Adjudicated cases. A soft warning that fires on every build for a question already answered is
# a warning nobody reads - the same reason drift.py keeps a PUBLISHED list. An entry here is a
# CLAIM THAT SOMEBODY CHECKED, so it carries the answer and the date.
SPOUSE_SETTLED = {
    "carlos lerena": "14 Sep 2026 - two different men, and both rows now say so. Adela Camiglia's "
                     "Carlos is at MENDOZA and fathered Avelino Carlos Lerena; Rosa Maria Eppens's "
                     "is the Uruguayan b.1885 who arrived in 1926 travelling with her.",
}
for spouse, names in spouses.items():
    uniq = sorted(set(names))
    if len(uniq) < 2:
        continue
    if spouse in SPOUSE_SETTLED:
        continue
    soft.append(f"{len(uniq)} rows are each said to have married '{spouse}': "
                + "; ".join(uniq[:4])
                + " - a remarriage, or one person entered twice under two spellings")

# 3. Two rows that are probably one person.
# build-people.py refuses EXACT duplicate names, which is why they never happen. It does not
# see "Dona Sixta LENGUAS (2nd wife of Candido Juanico)" and "Dona Sixta LENGUAS Gonzalez
# (2nd wife of Candido Juanico)" - two rows for one woman, written hours apart on 13 Sep 2026.
# Compare on the first two words plus any parenthetical, which is what actually collides.
def key(nm):
    base = " ".join(re.sub(r"\(.*?\)", "", nm).split()[:2]).lower()
    par = re.search(r"\((.*?)\)", nm)
    return (base, (par.group(1).lower() if par else ""))
# Collisions somebody has looked at. Adding a pair here is a claim that someone checked,
# so it carries the reason. The sibling Blazevic archive keeps its CHECKED_SHARED the same way.
CHECKED_PAIRS = {
    ("Bartolome LLERENA - Cordoba origin", "Bartolome LLERENA"):
        "deliberate: the second row is a cross-reference pointing at the Cordoba Llerena family",
    ("Maria Luisa Lina LERENA Gazo", "Maria Luisa LERENA"):
        "different people: Ysaac's daughter at Trinidad in 1875, and Gilberto's in the 1895 census",
    ("Maria E. LERENA", "Maria E. C. LERENA"):
        "different people in one census household - but see the age note against Maria E. C.",
    ("Dona Juana SUAREZ", "Dona Juana GRANDAL"):
        "different women sharing only the forename Juana: the late wife of Mayor Joaquin Ruiz de "
        "Carvallo, named in 1827, and the Juana Grandal of Las Piedras",
    ("Dona Carolina Amalia de la CONCEPCION", "Dona Carolina JUAREZ"):
        "different women sharing only the forename Carolina: the godmother beside General Maggesi at "
        "the Catedral in 1827, and an unrelated Carolina Juarez",
    ("Maria Carlota LERENA Salvanach", "Maria Carlota MORATORIO Lerena"):
        "different children ten years apart: Gilberto and Julia Salvanach's daughter baptised at "
        "Recoleta in 1890, and Fernando Moratorio and Josefa Lerena Traibel's baptised at Union in "
        "1880. A Lerena naming habit, not one person",
}
CHECKED_PAIRS = {tuple(sorted(k)): v for k, v in CHECKED_PAIRS.items()}
seen_key = {}
for p in people:
    k = key(p["name"])
    if not k[0]:
        continue
    if k in seen_key and seen_key[k] != p["name"]:
        pair = tuple(sorted([p["name"], seen_key[k]]))
        if pair not in CHECKED_PAIRS:
            soft.append(f"{p['name']!r} and {seen_key[k]!r} may be one person entered twice")
    seen_key[k] = p["name"]

# 4. A date field that carries a hedge and a precise date at once.
for p in people:
    b = str(p.get("born") or "")
    if re.match(r"^\s*c\.", b) and re.search(r"-\d\d-\d\d", b):
        soft.append(f"{p['name']} has a hedged AND precise birth: {b!r}")

# 5. A row claiming an image was read but carrying no ark anywhere.
for p in people:
    src = (p.get("source") or "") + " " + (p.get("note") or "")
    if re.search(r"IMAGE READ|image read", src) and "ark" not in src.lower():
        soft.append(f"{p['name']} says an image was read but names no ark")

# Coverage. A checker that does not say what it could not see is not telling the truth.
with_parent = sum(1 for p in people if p.get("father") or p.get("mother"))
with_cohort = sum(1 for p in people if compound(p["name"]))
with_cited = len({p["name"] for g in cited.values() if len(g) > 1 for p in g})
reached = {p["name"] for p in people if p.get("father") or p.get("mother")}
reached |= {p["name"] for p in people if compound(p["name"])}
reached |= {p["name"] for g in cited.values() if len(g) > 1 for p in g}
with_born = sum(1 for p in people if full(p.get("born")))
# 6. An UNPAIRED emphasis marker in the TSVs themselves.
# check-links.py already catches these, but only AFTER a build, by reading rendered HTML - and by then
# the literal *** is on a published page. On 14 September 2026 the same slip was made three times in
# one session, always the same way: writing "*** A *** B ***" while meaning "*** A *** *** B ***".
# Catching it in the data costs nothing and catches it before the page exists.
for tsv in sorted((ROOT / "data").glob("*.tsv")):
    for ln, line in enumerate(tsv.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("#") or "\t" not in line:
            continue
        for col, field in enumerate(line.split("\t")):
            if field.count("***") % 2:
                hard.append(f"{tsv.name}:{ln} field {col} has an ODD number of *** markers - "
                            f"one is unpaired and will render literally")

# 7. A PLACE field holding a CITATION.
# The atlas is built from where_found, so a row saying "SA records" or "GRO + SA records" does two
# things at once: it loses that person from the map, and it invents a phantom location on it. On
# 14 September 2026 five such entries were standing on /places/ as though they were towns.
CITATION_SHAPED = re.compile(r"\brecords?\b|\bGRO\b|\bcrossings?\b|\bindex\b|^\s*-?\s*$", re.I)
for p in people:
    for key in ("where_found", "birthplace"):
        v = str(p.get(key) or "").strip()
        if v and v != "-" and CITATION_SHAPED.search(v):
            soft.append(f"{p['name']} has a {key} that reads like a citation, not a place: {v!r} "
                        f"- it will appear on the atlas as a phantom location")

print(f"{len(people)} people checked")
print(f"   sibling gaps: {with_parent} have a structured parent, {with_cohort} reachable by compound "
      f"surname, {with_cited} by a parent named in prose; {len(reached)} of {len(people)} reached by "
      f"at least one; {with_born} carry a full birth date")
if len(reached) < len(people) // 2:
    print(f"   NOTE: the sibling tests reach {len(reached)}/{len(people)}. A pass here is not a "
          f"pass over the register.")
if hard:
    print(f"\n{len(hard)} CONTRADICTION(S) - these cannot all be true:")
    for h in hard:
        print("   ", h)
if soft:
    print(f"\n{len(soft)} thing(s) to look at:")
    for s in soft:
        print("   ", s)
if not hard and not soft:
    print("nothing contradicts itself - within the coverage printed above")
sys.exit(1 if hard else 0)
