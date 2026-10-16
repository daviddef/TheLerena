#!/usr/bin/env python3
"""Generate site/src/data/people.json and places.json from data/lerena-register.tsv.

The register is the single source of truth. Run this after every edit to it, so the
pages and the data cannot drift apart.
"""
import json, os, re, sys, unicodedata, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# THE ESTATE'S ONE DEFINITION OF WHO IS LIVING (David, 16 October 2026). Imported from the
# kit this archive is pinned to, never re-implemented: an archive that keeps its own test
# is how eight archives came to hold eight different ones.
_KIT = ROOT / "site" / "node_modules" / "@daviddef" / "archive-kit" / "kit" / "tools"
if not (_KIT / "living_rule.py").exists():
    raise SystemExit("build-people: the pinned kit has no kit/tools/living_rule.py - run "
                     "`npm install` in site/ (the kit pin must be 0a56c86 or later)")
sys.path.insert(0, str(_KIT))
import living_rule as lr
# Tests only: the gate harness (tools/test-living-gates.py) sets this to prove the 80-year
# bound moves the line. It is refused outside a scratch copy by that harness, not here.
TODAY = int(os.environ.get("LIVING_TODAY_YEAR") or lr.this_year())
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

# ===========================================================================
# WHO IS LIVING, WHO IS HELD OUT, AND WHO ELSE THE ARCHIVE NAMES (16 October 2026).
#
# David's living-people standard, version 2. The archive used to keep ONE living person
# by hand (an OMITTED-LIVING cell in direct-line.tsv, copied into site/src/data/living.json
# WITH HER BIRTH DATE, so the kit's gate could guard it) and refused her every fact,
# her town included. The rule now is the estate's, in the kit, and it is applied to
# everyone whose birth and death this archive holds:
#
#   living  = born 80 years ago or less (by year), with no death or burial recorded, and
#             no citation from a public record source. No birth year = not living.
#   shown   = a living person is NAME, RELATIONSHIPS, and FULL TOWN AND COUNTRY. Nothing else.
#   held out = an UNDATED person with a living parent (who might be a child), or a person
#             promised privacy by id: not published at all, and not named as anyone's relative.
#             A child with a KNOWN birth year follows the standard like any living person.
#
# THE GENERATOR SCRUBS AT THE SOURCE. This file is the only reader of a living person's
# birth year, and it writes none of it: people.json is committed and public, so what a living
# person carries into it is name, relationships, town, country - and nothing a build could
# print by mistake. A living person whose year is not held in any public file is recorded in
# data/living-roster.tsv (name, slug, town, country, no date); no committed file holds a living
# person's date.
# ===========================================================================
def fold(s):
    """A name as the data spells it, brought to one form: no brackets, no quotes, no case."""
    s = re.sub(r"\(.*?\)", " ", str(s or ""))
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return " ".join(s.replace('"', " ").casefold().split())

def byear(s):
    m = re.search(r"\b(1[0-9]{3}|20[0-9]{2})", str(s or ""))
    return int(m.group(1)) if m else None

def tsv_rows(path):
    if not path.exists():
        return []
    lines = [l.rstrip("\n") for l in path.read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]
    if not lines:
        return []
    h = lines[0].split("\t")
    return [dict(zip(h, (l.split("\t") + [""] * len(h))[:len(h)])) for l in lines[1:]]

def plainmark(s):
    return re.sub(r"\*\*\*\s*(.+?)\s*\*\*\*", r"\1", str(s or ""), flags=re.S).strip()

# ---- a RECORDED DEATH OR BURIAL, dated or not, however this archive records it ----------
# 1. last-attested-alive.tsv: tier DEATH (an explicit death date) AND DEATH BY (a ceiling:
#    a death is still recorded, only its year is uncertain - and for THIS question that is a death).
DEAD_EXACT, DEAD_ARKS, DEAD_FOLDED = set(), set(), set()
for _c in tsv_rows(ROOT / "data" / "last-attested-alive.tsv"):
    if (_c.get("tier") or "").strip().upper().startswith("DEATH"):
        DEAD_EXACT.add((_c.get("name") or "").strip())     # the register's own exact name, unique by construction
# 2. The Johannesburg cemetery register file: a row that gives a death OR a burial.
#    *** THIS IS THE ENTRY THAT KEEPS TWO PEOPLE DEAD. *** The register has no death column
#    and last-attested-alive.tsv holds no row for the wife and the younger son of the 1999
#    family: their only record of death is a burial registration. Without this they are
#    "born 1950 and 1991, no death recorded" - LIVING - and would be published as such.
#    Matched on the record's ARK (which the register row's source text carries) and, failing that, on
#    a name that folds to exactly ONE register row: this archive does not merge people on a name.
for _c in tsv_rows(ROOT / "data" / "johannesburg-cemetery-1999.tsv"):
    _who = plainmark(_c.get("person"))
    _says = plainmark(_c.get("what the register gives"))
    if _who and re.search(r"\b(death|burial|buried)\b", _says, re.I):
        DEAD_FOLDED.add(fold(_who))
        if re.fullmatch(r"\d:\d:[A-Z0-9-]+", (_c.get("ark") or "").strip()):
            DEAD_ARKS.add(_c["ark"].strip())

# ---- supplementary people: everyone the archive's chart names who has no register row ----
SIB = {fold(r.get("person")): r for r in tsv_rows(ROOT / "data" / "lerena-siblings-gen3.tsv")}
DLN = {fold(r.get("person")): r for r in tsv_rows(ROOT / "data" / "direct-line.tsv")}
REL_EDGES = []
if REL.exists():
    for l in REL.open(encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            REL_EDGES.append((l.rstrip("\n").split("\t") + [""] * 6)[:6])
    REL_EDGES = REL_EDGES[1:]
PARTNERS, EDGE_DATES = {}, {}
for _who, _rel, _oth, _dt, _via, _nt in REL_EDGES:
    PARTNERS.setdefault(_who, set()).add(_oth); PARTNERS.setdefault(_oth, set()).add(_who)
    if _dt and _dt != "-":
        EDGE_DATES.setdefault(_oth, _dt)

def years_of(dates):
    """'1929–2013' -> ('1929', '2013'); anything else -> ('', '')."""
    m = re.fullmatch(r"\s*(\d{4})\s*[-–]\s*(\d{4})\s*", dates or "")
    return (m.group(1), m.group(2)) if m else ("", "")

def mint(name):
    base = slugify(name)
    if name in _frozen:
        return _frozen[name]
    seen[base] = seen.get(base, 0) + 1
    slug = base if seen[base] == 1 else f"{base}-{seen[base]}"
    while slug in _taken:
        seen[base] += 1
        slug = f"{base}-{seen[base]}"
    _taken.add(slug); _minted.append((name, slug))
    return slug

_have = {p["name"] for p in people}
_supp_names = []
for _who, _rel, _oth, *_ in REL_EDGES:
    for _n in (_who, _oth):
        if _n and _n not in _have and _n not in _supp_names:
            _supp_names.append(_n)

for _n in _supp_names:
    _f = fold(_n)
    _s, _d = SIB.get(_f, {}), DLN.get(_f, {})
    # DATES HELD ONLY IN THE FAMILY CHART'S WORKING FILES decide who is living and are NOT published.
    # data/lerena-siblings-gen3.tsv and the direct-line row carry births and deaths this archive has
    # not sourced (check-people-named.py keeps one sibling out for exactly that: her death "rests on one
    # commercial index row"). A recorded death is a death for THIS question; it is not a fact to print.
    priv_born = (_d.get("born") or _s.get("born") or "").strip()
    priv_died = (_d.get("died") or _s.get("died") or "").strip()
    bp = (_d.get("born_place") or "").strip()
    born, died = years_of(EDGE_DATES.get(_n, ""))      # dates the chart already prints on a node
    if _s:
        src = ("Named among the children of Nuno Fernando Lerena in his 1971 death notice "
               "(estate 6746/71). Their dates are in the family chart, are not sourced here, and are not published")
    elif _d:
        src = "Named on the direct line, data/direct-line.tsv"
    else:
        src = ("Named as a relative in data/relations.tsv; no record of their own has been "
               "read into this register")
    people.append({
        "slug": mint(_n), "name": _n, "born": born, "died": died,
        "birthplace": bp, "nationality": "", "occupation": "", "where": "",
        "source": src, "status": "unplaced", "statusRaw": "UNPLACED",
        "note": "", "place": "", "placeSlug": "",
        "surname": surname_of(_n) if surname_of(_n) != "OTHER" else _n.split()[-1].upper(),
        "ark": "", "sourceUrl": "", "noLink": no_link_reason(src),
        "_supp": True, "_privborn": priv_born, "_privdied": priv_died,
        # a person this archive holds nothing of its own about: named in the chart, and that is all
        "relOnly": not _s and not _d,
        "datesFrom": "the family chart (data/relations.tsv)" if (born or died) else "",
    })

# A supplementary person is "connected" when the person who names them is: the standing is the
# chart partner's, because a record of their own is exactly what they lack. Two passes, so a spouse
# of a child of the line is reached.
_st = {p["name"]: p["status"] for p in people}
for _ in range(2):
    for p in people:
        if p.get("_supp") and p["status"] != "connected" and \
                any(_st.get(x) == "connected" for x in PARTNERS.get(p["name"], ())):
            p["status"], p["statusRaw"] = "connected", "CONNECTED"
            _st[p["name"]] = "connected"

# ---- classification -----------------------------------------------------------------------
# Citations a person is evidenced by: the register's source column, its FamilySearch link, and the
# source line of every record read about them. A PRIVATE TREE ENTRY IS NOT A PUBLIC SOURCE
# (that is living_rule's call, not this file's). Supplementary people are cited by a family
# document and the family chart, neither of which is public.
_EV = {}
if EVID.exists():
    for _l in EVID.open(encoding="utf-8"):
        if _l.strip() and not _l.startswith("#"):
            _r = (_l.rstrip("\n").split("\t") + [""] * 5)[:5]
            _EV.setdefault(_r[0].strip(), []).append(_r[2].strip())
_HELD_FILE = ROOT / "data" / "held-out-ids.txt"       # promised privacy, by slug; absent = none
HELD_IDS = [l.split("#")[0].strip() for l in _HELD_FILE.read_text(encoding="utf-8").splitlines()
            if l.split("#")[0].strip()] if _HELD_FILE.exists() else []

ROSTER = {r["name"].strip(): r for r in tsv_rows(ROOT / "data" / "living-roster.tsv") if r.get("name")}
_unknown = sorted(set(ROSTER) - {p["name"] for p in people})
if _unknown:
    raise SystemExit("build-people: data/living-roster.tsv names %d person(s) the chart does not hold" % len(_unknown))
_fold_count = {}
for p in people:
    _fold_count[fold(p["name"])] = _fold_count.get(fold(p["name"]), 0) + 1
for p in people:
    p["_by"] = byear(p.get("_privborn") or p["born"])
    p["_dead"] = (bool(p["died"] or p.get("_privdied")) or p["name"] in DEAD_EXACT
                  or any(a in p["source"] for a in DEAD_ARKS)
                  or (fold(p["name"]) in DEAD_FOLDED and _fold_count[fold(p["name"])] == 1))
    p["_cit"] = [] if p.get("_supp") else [p["source"], p["sourceUrl"]] + _EV.get(p["name"], [])
    p["living"] = lr.is_living(p["_by"], p["_dead"], p["_cit"], TODAY)
    # THE ROSTER (data/living-roster.tsv): a living person whose birth year is NOT held in any public
    # file is recorded as living by name and slug, with their town and country and no date. It cannot
    # make a dead person living: a recorded death, or a public-source citation, refuses the build.
    _rr = ROSTER.get(p["name"])
    if _rr:
        if p["_dead"] or lr.public_source(p["_cit"]):
            raise SystemExit("build-people: data/living-roster.tsv lists a person the data records as dead or "
                             "cites to a public source (%s). Delete the roster row." % p["slug"])
        if _rr.get("slug") != p["slug"]:
            raise SystemExit("build-people: living-roster slug %r does not match %r" % (_rr.get("slug"), p["slug"]))
        p["living"], p["_roster"] = True, _rr

_parents = {}                      # child name -> parent names, from the chart's own edges
for _who, _rel, _oth, *_ in REL_EDGES:
    if _rel in ("father", "mother"):
        _parents.setdefault(_who, set()).add(_oth)
    elif _rel == "child":
        _parents.setdefault(_oth, set()).add(_who)
_living_names = {p["name"] for p in people if p["living"]}
HELD = {}
for p in people:
    _pl = any(x in _living_names for x in _parents.get(p["name"], ()))
    if lr.is_held_out(p["slug"], p["_by"], p["_dead"], p["_cit"], _pl, HELD_IDS, TODAY):
        HELD[p["name"]] = p["slug"]
people = [p for p in people if p["name"] not in HELD]
for _p in people:
    _p["living"] = _p["living"] and _p["name"] not in HELD

# ---- town and country: all a living person has of a place -----------------------------------
COUNTRIES = {"south africa", "uruguay", "argentina", "england", "scotland", "wales", "ireland",
             "australia", "spain", "italy", "chile", "brazil", "paraguay", "france", "portugal",
             "germany", "canada", "new zealand", "united states", "usa", "namibia", "zimbabwe",
             "mozambique", "croatia", "united kingdom", "uk", "netherlands", "switzerland"}
# A town this archive has met, where the data wrote the town and not the country.
TOWN_COUNTRY = {"johannesburg": "South Africa", "cape town": "South Africa", "pretoria": "South Africa",
                "durban": "South Africa", "bloemfontein": "South Africa", "germiston": "South Africa",
                "montevideo": "Uruguay", "buenos aires": "Argentina", "rosario": "Argentina",
                "brisbane": "Australia", "sydney": "Australia", "perth": "Australia",
                "melbourne": "Australia", "london": "England", "bideford": "England"}
# Not a town: a street, an address-like string, an institution.
NOT_A_TOWN = re.compile(r"\d|\b(street|st\.|road|rd\.?|avenue|ave\.?|lane|drive|close|crescent|"
                        r"hospital|clinic|infirmary|care|nursing|home|hospice|asylum|prison|"
                        r"school|college|farm|po box|p\.o\.)\b", re.I)

def town_country(*places):
    """(town, country) from the first place string that yields a clean town. Never a street,
    an address-like string or an institution: those parts are dropped and the town kept."""
    for pl in places:
        parts = [x.strip() for x in str(pl or "").replace("/", ",").split(",") if x.strip() and x.strip() != "-"]
        if not parts:
            continue
        country = ""
        if parts[-1].casefold() in COUNTRIES:
            country = parts.pop()
            country = {"usa": "United States", "uk": "United Kingdom"}.get(
                country.casefold(), country.title() if country.islower() else country)
        towns = [x for x in parts if not NOT_A_TOWN.search(x)]
        if not towns:
            continue
        town = towns[0]
        if not country:
            country = TOWN_COUNTRY.get(town.casefold(), "")
        return town, country
    return "", ""

# ---- places: where the DEAD were found. A living person was not "found" anywhere; their town
# and country are on their own page and nowhere else a place is counted. --------------------------
places = {}
for p in people:
    if p["living"] or p.get("_supp"):
        p["place"], p["placeSlug"] = "", ""
        continue
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
       "roseline-wilhelmina-forbes-m-1-chappell-m-2-lerena": 2, "rhena-may-lerena": 2,
       "cheryl-anne-lerena": 3, "jeanette-marie-lerena": 3, "paul-raymond-lerena": 3,
       "catherine-tersia-lerena": 3, "patricia-carmen-lerena": 3,
       "catherine-mary-sophia-booyzen": 2}
LINE = {"juan-carlos-lerena", "maria-lerena", "pablo-armando-lerena", "mary-septima-taylor",
        "nuno-fernando-lerena", "cheryl-anne-lerena"}

def node(name, dates, via):
    """A chart node: links to a person page when the register holds that name."""
    tgt = by_name.get(name)
    if tgt is not None and tgt.get("living"):
        dates = ""                   # a living person is a name on someone else's chart, never a date
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
        if other in HELD:            # a held-out person is nobody's relative, not even as a name
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

    # *** A MARRIAGE IS SYMMETRIC AND WAS BEING READ ONE WAY ONLY. 11 October 2026. ***
    # Exactly the fault fixed for parent edges above, in the one relationship where the two ends
    # are interchangeable. "Avelino LERENA Villademoros | spouse | Carmen LORENTE" gave Avelino a
    # wife and gave Carmen nothing, so /people/carmen-lorente/ told its reader
    # "No relationships are recorded for this person" while this archive held her marriage.
    # FIFTEEN PAGES WERE SAYING THAT, found by a site-wide audit and not by any gate:
    # check-evidence.py guards data/person-evidence.tsv and never looks at relations.tsv, so the
    # sentence it was written to abolish had come back through a different door.
    # Mirrored here rather than in the data, because asking every future session to write both
    # directions of every marriage is asking to be told half of them.
    for p in list(people):
        if p.get("aliasOf"):
            continue
        for sp in list(p["spouses"]):
            tgt = by_name.get(sp["name"])
            if not tgt or tgt.get("aliasOf"):
                continue
            if any(x["name"] == p["name"] for x in tgt["spouses"]):
                continue
            back = node(p["name"], p.get("born_est", ""), sp.get("via", "register"))
            back["note"] = sp.get("note", "")
            tgt["spouses"].append(back)
    for p in people:
        p["spouses"].sort(key=lambda c: (c.get("dates") or "", c["name"]))


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
            if who not in HELD:      # a held-out person's record goes unpublished with them
                missing.append(who)
            continue
        subj["evidence"].append({"says": says, "source": source,
                                 "ark": "" if ark in ("-", "") else ark, "readOn": read_on})
    if missing:
        raise SystemExit(
            "build-people: person-evidence.tsv names %d person(s) absent from the register:\n  %s\n"
            "Every evidence row must attach to a register name, or the evidence never reaches a page."
            % (len(missing), "\n  ".join(sorted(set(missing)))))

# ---------------------------------------------------------------------------
# THE SCRUB. A living person leaves this generator as a NAME, RELATIONSHIPS, A TOWN AND A COUNTRY.
# Every other field is emptied here, at the source, because people.json is a committed file and
# every committed file in this repo is public. The relationship edges keep a name, a slug and how
# the edge is known; their dates and their notes (which hold marriage dates) are emptied both on
# a living person's own edges and on every other person's edge that points at one.
# ---------------------------------------------------------------------------
LIVING_NAMES = {p["name"] for p in people if p["living"]}
def _scrub_node(n):
    if n:
        n["dates"] = ""; n["note"] = ""
        if n["name"] in LIVING_NAMES:
            n["living"] = True
for p in people:
    for n in [p["father"], p["mother"]] + p["spouses"] + p["children"] + p["siblings"] \
            + p.get("godparents", []) + p.get("godchildren", []):
        if p["living"] or (n and n["name"] in LIVING_NAMES):
            _scrub_node(n)

KEEP_LIVING = {"slug", "name", "surname", "gen", "isLine", "status", "statusRaw", "father", "mother",
               "spouses", "children", "siblings", "godparents", "godchildren", "aliasOf",
               "relTotal", "relRegister", "relTree", "living", "town", "country"}
EMPTY = {"born": "", "died": "", "birthplace": "", "nationality": "", "occupation": "", "where": "",
         "source": "", "note": "", "place": "", "placeSlug": "", "ark": "", "sourceUrl": "",
         "noLink": "", "evidence": []}
no_place = []
for p in people:
    if p["living"]:
        _rr = p.get("_roster")
        town, country = ((_rr["town"].strip(), _rr["country"].strip()) if _rr
                         else town_country(p["birthplace"], p["where"]))
        for k in list(p):
            if k not in KEEP_LIVING and k not in EMPTY and not k.startswith("_"):
                del p[k]
        p.update({k: (list(v) if isinstance(v, list) else v) for k, v in EMPTY.items()})
        p["town"], p["country"] = town, country
        if not town:
            no_place.append(p["slug"])
    # A page that holds a name and one relationship and nothing else - no date, no record - has
    # nothing to be found by and is not indexed (a living person's page never is).
    undated_stub = bool(p.get("_supp")) and not p["born"] and not p["died"]
    p["noindex"] = bool(p["living"] or undated_stub)
for p in people:
    for k in [k for k in p if k.startswith("_")]:
        del p[k]

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
_liv = [p for p in people if p["living"]]
print(f"{len(people)} people, {len(places)} places, {ev} record(s) read about a named person")
print(f"living: {len(_liv)} ({sum(1 for p in _liv if p['town'] and p['country'])} with town and country, "
      f"{sum(1 for p in _liv if p['town'] and not p['country'])} town only, "
      f"{sum(1 for p in _liv if not p['town'])} with no place); "
      f"held out: {len(HELD)}; noindex: {sum(1 for p in people if p['noindex'])}")
