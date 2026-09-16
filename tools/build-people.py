#!/usr/bin/env python3
"""Generate site/src/data/people.json and places.json from data/lerena-register.tsv.

The register is the single source of truth. Run this after every edit to it, so the
pages and the data cannot drift apart.
"""
import json, re, unicodedata, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG  = ROOT / "data" / "lerena-register.tsv"
REL  = ROOT / "data" / "relations.tsv"
EVID = ROOT / "data" / "person-evidence.tsv"
OUT  = ROOT / "site" / "src" / "data"

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-+", "-", s) or "person"

STATUS = {
    "CONNECTED": "connected",
    "EXCLUDED": "excluded",
    "UNPLACED - HIGH INTEREST": "high",
    "UNPLACED - INTEREST": "interest",
    "UNPLACED": "unplaced",
}

SURNAME_FIX = {"ARMAND[O": "LORENA"}

def surname_of(name):
    """The ALL-CAPS token in each register name is the surname, by convention."""
    toks = re.findall(r"\b[A-Z\u00c1\u00c9\u00cd\u00d3\u00da\u00d1][A-Z\u00c1\u00c9\u00cd\u00d3\u00da\u00d1\[\]]{2,}\b", name)
    if not toks:
        return "OTHER"
    s = toks[0].rstrip("[]")
    return SURNAME_FIX.get(toks[0], s)

FS = "https://www.familysearch.org"

def ark_url(a):
    """Store the bare id; build the link. The Defranceski archive's trick, and the reason
    it links thousands of rows where this one linked five."""
    if not a:
        return ""
    if a.startswith("tree:"):
        return f"{FS}/tree/person/details/{a[5:]}"
    return f"{FS}/ark:/61903/{a}"

def no_link_reason(src):
    """Falco convention: every row links to its source, or says here why it cannot."""
    b = src.lower()
    if "cemla" in b:
        return "CEMLA results are not addressable \u2014 search the surname at cemla.com/buscador/"
    if "passport" in b or "estate" in b or "family chart" in b or "death notice" in b:
        return "family papers \u2014 held offline, not on a public site"
    if "gro" in b:
        return "GRO index \u2014 no public per-record link"
    if "census" in b or "familysearch" in b or "catholic church" in b or "civil" in b or "cemetery" in b or "military" in b or "marriage" in b or "baptism" in b:
        return "FamilySearch index \u2014 ark not recorded for this entry"
    if "forebears" in b or "surname distribution" in b:
        return "aggregate statistic \u2014 not a per-person record"
    return "no public link"

def norm_place(w):
    w = w.strip()
    if re.search(r"\barr\.", w, flags=re.I) or "arrival" in w.lower():
        return "Buenos Aires — arrivals"
    w = re.sub(r",\s*Seccion.*$", "", w, flags=re.I)
    return w or "Unrecorded"

rows = [l.rstrip("\n").split("\t") for l in REG.open(encoding="utf-8") if l.strip()]
hdr, rows = rows[0], rows[1:]

people, seen = [], {}
for r in rows:
    r = (r + [""] * 10)[:10]
    name, born, bp, nat, occ, where, src, st, note, ark = r
    base = slugify(name)
    seen[base] = seen.get(base, 0) + 1
    slug = base if seen[base] == 1 else f"{base}-{seen[base]}"
    place = norm_place(where)
    people.append({
        "slug": slug, "name": name, "born": born, "birthplace": bp,
        "nationality": nat, "occupation": occ, "where": where, "source": src,
        "status": STATUS.get(st.strip().upper(), "unplaced"), "statusRaw": st,
        "note": note, "place": place, "placeSlug": slugify(place),
        "surname": surname_of(name),
        "ark": ark,
        "sourceUrl": ark_url(ark),
        "noLink": "" if ark else no_link_reason(src),
    })

places = {}
for p in people:
    places.setdefault(p["placeSlug"], {"slug": p["placeSlug"], "name": p["place"], "people": []})
    places[p["placeSlug"]]["people"].append(p["slug"])
places = sorted(places.values(), key=lambda x: -len(x["people"]))
for pl in places:
    pl["count"] = len(pl["people"])

# ---- relationships -------------------------------------------------------
# A name that appears twice in the register would silently collapse here - the later row winning -
# so an edge or a chart node written for that name would attach to the wrong person, and the other
# row would be unreachable by name entirely. Slugs are disambiguated; names were not. Fail loudly.
_dupes = {}
for _p in people:
    _dupes.setdefault(_p["name"], []).append(_p["slug"])
_bad = {k: v for k, v in _dupes.items() if len(v) > 1}
if _bad:
    print("*** DUPLICATE REGISTER NAMES - relations and chart links will attach to the wrong row ***")
    for k, v in _bad.items():
        print(f"    {len(v)}x  {k}   -> {', '.join(v)}")
    raise SystemExit("Give each register row a unique name, then rebuild.")
by_name = {p["name"]: p for p in people}
GEN = {"pablo-armando-lerena": 1, "mary-septima-taylor": 1, "juan-carlos-lerena": 0,
       "maria-lerena": 0, "roque-luis-armando-lerena": 2, "ricardo-juan-carlos-lerena": 2,
       "nuno-fernando-lerena": 2, "anton-lerena": 3, "rieta-maria-lerena": 3,
       "antoinette-septima-lynette-lerena": 3, "doreen-may-chappell-m-lerena": 2,
       "roseline-wilhelmina-forbes-m-1-chappell-m-2-lerena": 2, "rhena-may-lerena": 2}
LINE = {"juan-carlos-lerena", "maria-lerena", "pablo-armando-lerena", "mary-septima-taylor",
        "nuno-fernando-lerena"}

def node(name, dates, via):
    """A chart node: links to a person page when the register holds that name."""
    tgt = by_name.get(name)
    return {"name": name, "dates": (dates or "").replace("-", "\u2013") if dates and dates != "-" else "",
            "slug": tgt["slug"] if tgt else "", "via": via}

for p in people:
    p["gen"] = GEN.get(p["slug"])
    p["father"] = None; p["mother"] = None
    p["spouses"] = []; p["children"] = []; p["siblings"] = []
    p["isLine"] = p["slug"] in LINE

if REL.exists():
    edges = [l.rstrip("\n").split("\t") for l in REL.open(encoding="utf-8")
             if l.strip() and not l.startswith("#")][1:]
    for e in edges:
        e = (e + [""] * 6)[:6]
        who, rel, other, dates, via, note = e
        subj = by_name.get(who)
        if not subj:
            continue
        n = node(other, dates, via); n["note"] = note
        if rel == "father":  subj["father"] = n
        elif rel == "mother": subj["mother"] = n
        elif rel == "spouse": subj["spouses"].append(n)
        elif rel == "child":  subj["children"].append(n)

    # ALIASES. This register deliberately keeps a row for a mangled machine-index reading of a person
    # it has already resolved, written "WRONG NAME (as machine-indexed) = Right Name". Those rows carry
    # their own parent edges, which is correct for the alias but would make the parent appear to have
    # two children where there is one. An alias is anything whose name ends "= <a name in the register>".
    def alias_target(nm):
        if " = " not in nm:
            return None
        cand = nm.rsplit(" = ", 1)[1].strip()
        if cand in by_name:
            return cand
        # the canonical row often carries a parenthetical - "Pablo Armando LERENA (Robert Paul; \"Bob\")"
        for other in by_name:
            if other != nm and other.startswith(cand):
                return other
        return None
    # Written as {slug, name}, not as a bare name. The blood chart folds an alias onto the person
    # it is a spelling of - so that a man is not drawn twice, once under each reading - and it will
    # only do that on a SLUG. Handing it a name would be asking it to decide that two rows are one
    # person by looking at what they are called, which is the one thing that library refuses to do.
    for p in people:
        tgt = alias_target(p["name"])
        p["aliasOf"] = {"slug": by_name[tgt]["slug"], "name": tgt} if tgt else None

    # A father/mother edge is also a CHILD edge seen from the other end. Until 13 September 2026
    # this was not reversed, so every parent in the archive showed an empty children list unless
    # somebody had also written an explicit "child" row. Thirty-eight parent edges were being read
    # one way only. Reversed here, and de-duplicated against the explicit rows.
    for p in people:
        for par_key in ("father", "mother"):
            par = p[par_key]
            if not par:
                continue
            tgt = by_name.get(par["name"])
            if not tgt:
                continue
            if p.get("aliasOf"):
                continue
            if any(c["name"] == p["name"] for c in tgt["children"]):
                continue
            kid = node(p["name"], p.get("born_est", ""), par["via"])
            kid["note"] = par.get("note", "")
            tgt["children"].append(kid)
    for p in people:
        p["children"].sort(key=lambda c: (c.get("dates") or "", c["name"]))

    # siblings: anyone sharing a parent, drawn from the same edge list
    kids_of = {}
    for p in people:
        if p.get("aliasOf"):
            continue
        for par in (p["father"], p["mother"]):
            if par:
                kids_of.setdefault(par["name"], set()).add(p["name"])
    for p in people:
        # An alias shares its person's parents, so the sibling pass handed it its own self as a
        # brother: /bloodline/ drew Pablo Armando standing next to Pablo Armando, labelled
        # "aunt or uncle". An alias has no brothers and sisters of its own; the person does.
        if p.get("aliasOf"):
            p["siblings"] = []
            continue
        sibs = set()
        for par in (p["father"], p["mother"]):
            if par:
                sibs |= kids_of.get(par["name"], set())
        sibs.discard(p["name"])
        p["siblings"] = [node(s, "", "register") for s in sorted(sibs)]

    # every relationship counted, so the page can say how much is documented
    for p in people:
        rels = [x for x in [p["father"], p["mother"]] if x] + p["spouses"] + p["children"]
        p["relTotal"] = len(rels)
        p["relRegister"] = sum(1 for x in rels if x["via"] in ("register", "line"))
        p["relTree"] = sum(1 for x in rels if x["via"] == "tree")

# ---------------------------------------------------------------------------
# RECORDS READ ABOUT A NAMED PERSON.
#
# Until 17 September 2026 a person page was built from the register and the
# relations file and nothing else, so evidence written into topic files never
# reached the person it was about: Cipriano and Vitalino of Trinidad had pages
# saying "No relationships are recorded for this person. The source names them
# and nothing more" while this archive held their wives, their children and,
# for Cipriano, his parents.
#
# THIS LOOP FAILS LOUDLY ON AN UNKNOWN NAME. relations.tsv silently `continue`s
# past a name the register does not hold, which is the same class of fault that
# caused this one - a build that drops data without refusing.
for p in people:
    p["evidence"] = []
if EVID.exists():
    rows = [l.rstrip("\n").split("\t") for l in EVID.open(encoding="utf-8")
            if l.strip() and not l.startswith("#")][1:]
    missing = []
    for r in rows:
        r = (r + [""] * 5)[:5]
        who, says, source, ark, read_on = (x.strip() for x in r)
        subj = by_name.get(who)
        if not subj:
            missing.append(who)
            continue
        subj["evidence"].append({"says": says, "source": source,
                                 "ark": "" if ark in ("-", "") else ark, "readOn": read_on})
    if missing:
        raise SystemExit(
            "build-people: person-evidence.tsv names %d person(s) absent from the register:\n  %s\n"
            "Every evidence row must attach to a register name, or the evidence never reaches a page."
            % (len(missing), "\n  ".join(sorted(set(missing)))))

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "people.json").write_text(json.dumps(people, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
(OUT / "places.json").write_text(json.dumps(places, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
ev = sum(len(p["evidence"]) for p in people)
print(f"{len(people)} people, {len(places)} places, {ev} record(s) read about a named person")
