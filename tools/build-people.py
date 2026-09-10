#!/usr/bin/env python3
"""Generate site/src/data/people.json and places.json from data/lerena-register.tsv.

The register is the single source of truth. Run this after every edit to it, so the
pages and the data cannot drift apart.
"""
import json, re, unicodedata, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG  = ROOT / "data" / "lerena-register.tsv"
REL  = ROOT / "data" / "relations.tsv"
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
    name, born, bp, nat, occ, where, src, st, note, src_url = r
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
        "sourceUrl": src_url,
        "noLink": "" if src_url else no_link_reason(src),
    })

places = {}
for p in people:
    places.setdefault(p["placeSlug"], {"slug": p["placeSlug"], "name": p["place"], "people": []})
    places[p["placeSlug"]]["people"].append(p["slug"])
places = sorted(places.values(), key=lambda x: -len(x["people"]))
for pl in places:
    pl["count"] = len(pl["people"])

# ---- relationships -------------------------------------------------------
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

    # siblings: anyone sharing a parent, drawn from the same edge list
    kids_of = {}
    for p in people:
        for par in (p["father"], p["mother"]):
            if par:
                kids_of.setdefault(par["name"], set()).add(p["name"])
    for p in people:
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

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "people.json").write_text(json.dumps(people, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
(OUT / "places.json").write_text(json.dumps(places, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"{len(people)} people, {len(places)} places")
