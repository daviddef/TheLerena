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
    # Parentheses are stripped because PERSON names in this register carry disambiguators -
    # "Alejandro M. LERENA (m.1 Elisa VILLADEMOROS)" must not slug them into the id.
    # *** BUT PLACE NAMES RUN THROUGH THE SAME FUNCTION AND THE KIT'S SEARCH INDEX DOES NOT
    # STRIP THEM ***, so a place written "La Paz (Canelones), Uruguay" slugged to
    # "la-paz-uruguay" here and "la-paz-canelones" there, and check:searchindex caught a link
    # to a page that was never built (10 October 2026). Until the two agree,
    # *** DO NOT PUT PARENTHESES IN A where_found VALUE. ***
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

_LEDGER = ROOT / "site" / "src" / "data" / "person-slugs.json"
try:
    _ledger_doc = json.loads(_LEDGER.read_text(encoding="utf-8"))
except Exception:
    _ledger_doc = {"_why": ["Written by tools/build-people.py"], "slugs": {}}
_frozen = _ledger_doc["slugs"]
_taken = set(_frozen.values())
_minted = []

# DEATHS THIS REGISTER NEVER CARRIED, and why they arrive from here and not from
# the line files.
#
# data/lerena-register.tsv has no death column at all — it is a surname sweep,
# recording where each person was FOUND. So people.json carried no `died`, and
# the kit's kin gate, whose every test needs a birth and a death, skipped all 357
# rows while reporting «ok · 357 people · 0 impossible relationship(s)». Green
# since it was written, having examined nobody.
#
# The obvious fix is wrong. The line files DO hold deaths — direct-line.tsv,
# gen1-children.tsv, lerena-siblings-gen3.tsv, taylor-line.tsv, 23 of them — and
# only 2 of those 23 names match a register name exactly. The rest differ as
# «Mary Septima LERENA, née TAYLOR» differs from «Mary Septima TAYLOR», or carry
# a nickname, or belong to the Taylor line and not to this register at all.
# Joining them would mean normalising names and deciding that two spellings are
# one person, which is the single inference this archive refuses.
#
# data/last-attested-alive.tsv is the file where that reconciliation was already
# done BY HAND, person by person, with the basis written beside each one. Its 356
# names match 356 register names exactly. So the deaths are taken from there, and
# only where `tier` is DEATH — the 3 DEATH BY rows are ceilings and say so in
# their own basis text: "a CEILING, not a date: the file year can trail the
# death". A ceiling is not a death and must never be published as one.
DEATHS = {}
_la = ROOT / "data" / "last-attested-alive.tsv"
if _la.exists():
    _lines = [l for l in _la.read_text(encoding="utf-8").splitlines()
              if l.strip() and not l.startswith("#")]
    if _lines:
        _hdr = _lines[0].split("\t")
        for _l in _lines[1:]:
            _c = dict(zip(_hdr, _l.split("\t")))
            if (_c.get("tier") or "").strip() == "DEATH":
                _who = (_c.get("name") or "").strip()
                _when = (_c.get("last_attested_alive") or "").strip()
                if _who and _when:
                    DEATHS[_who] = _when

people, seen = [], {}
for r in rows:
    r = (r + [""] * 10)[:10]
    name, born, bp, nat, occ, where, src, st, note, ark = r
    # A PERSON'S URL IS MINTED ONCE AND NEVER RECOMPUTED.
    #
    # This used to be `seen[base] += 1` counted in the ROW ORDER of
    # data/lerena-register.tsv, so inserting a row above a namesake renumbered
    # every namesake below it. The ledger is read first and used unchanged;
    # only a name this archive has never published is minted.
    base = slugify(name)
    if name in _frozen:
        slug = _frozen[name]
        seen[base] = seen.get(base, 0) + 1
    else:
        seen[base] = seen.get(base, 0) + 1
        slug = base if seen[base] == 1 else f"{base}-{seen[base]}"
        while slug in _taken:
            seen[base] += 1
            slug = f"{base}-{seen[base]}"
        _minted.append((name, slug))
    _taken.add(slug)
    place = norm_place(where)
    people.append({
        "slug": slug, "name": name, "born": born, "died": DEATHS.get(name, ""),
        "birthplace": bp,
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
        # GODPARENTS ARE KEPT, AND KEPT OUT OF THE CHART. Added 8 October 2026, after
        # twenty-nine godparent edges had been written into relations.tsv and reached
        # NOBODY: this loop handled four relation words and dropped the rest silently,
        # so check-tree.py counted the edges and the person page rendered none of them.
        # They are NOT folded into relTotal, because the page says "of the N
        # relationships IN THE CHART ABOVE" and the chart draws parents, spouses,
        # children and siblings. Counting them there would make that sentence false.
        # They get their own prose line instead - which is what the register's own
        # notes already say, now said from the data.
        elif rel in ("godfather", "godmother", "godparent"):
            subj.setdefault("godparents", []).append({**n, "role": rel})
            other_row = by_name.get(other)
            if other_row is not None:
                other_row.setdefault("godchildren", []).append({**node(who, "", via), "role": rel})

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
        p.setdefault("godparents", [])
        p.setdefault("godchildren", [])
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

# Written EVERY run and deterministically — byte-identical when nothing new
# was minted — so a stamp or an orphan check can account for it. A file only
# sometimes written looks exactly like one whose generator has been deleted.
for _n, _s in _minted:
    _frozen.setdefault(_n, _s)
_ledger_doc["slugs"] = dict(sorted(_frozen.items()))
_LEDGER.write_text(json.dumps(_ledger_doc, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
if _minted:
    print(f"  person-slugs.json: {len(_minted)} new slug(s) frozen")

(OUT / "people.json").write_text(json.dumps(people, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
(OUT / "places.json").write_text(json.dumps(places, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
ev = sum(len(p["evidence"]) for p in people)
print(f"{len(people)} people, {len(places)} places, {ev} record(s) read about a named person")
