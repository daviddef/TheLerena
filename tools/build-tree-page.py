#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Roots & Routes: the tree page for this archive, built from this archive's own committed data.

    python3 tools/build-tree-page.py            # rebuild data/tree-page/ (tree.json, atlas-data.json, roots.html, roots.embed.html) and site/public/roots-links.json
    python3 tools/build-tree-page.py --check    # exit 1 if the page is older than the data it was built from

WHERE THE PEOPLE COME FROM. There is no committed GEDCOM. The people are the ones site/src/data/people.json holds (written from data/lerena-register.tsv by
tools/build-people.py), minus every person it marks `living` or `noindex` (a held-out or undated stub): a living person is a name, relationships, a town and
a country in that file and is not drawn, and nobody is drawn who has no page of their own. The rest is turned into a small GEDCOM
(data/tree-page/people.ged, not committed) and handed to the family-tree-page skill's converter, vendored in tools/tree-page/ so CI and other sessions do not
depend on ~/.claude. The converter then adds its own floor: nobody with no death recorded and a birth year in the last 110 years is drawn.

WHAT IS FOLLOWED. A father, mother, spouse or child link is followed unless it rests only on a family tree (`via: tree`), as tools/build-family-lines.py and
tools/build-lines.py do not follow one either. A birth year is the register's (a circa year is flagged as an estimate on the page); a person with no
birth year is dated only from a parent, child or spouse who has one (the converter flags it) and is not drawn when none has.

SEX is not held by this archive, and is never inferred from a given name. It is stated only where the register's own data states or entails it: a person
named as a father or a mother in a parent link, or a title in the register's name (Don, Dona). Everyone else has no SEX line, the converter says 'u', and the
viewer uses neutral words (parent, child, spouse, sibling, uncle or aunt); tree.report.json (adapter.sex_unknown_drawn) says how many that is.

COLOUR is the surname of the person's name (the capitalised word of the register, the first when there are two), taken to its family in the Record Atlas
catalogue (data/surname-families.json, read here, never copied): which spellings are one name is the catalogue's to say (surname-variants skill), and this
archive keeps no list of them. A surname the catalogue does not hold is its own colour. The seven commonest are coloured; the rest share the last.

PLACES are resolved through data/tree-page/place_map.json, never guessed. The only place the register gives a person is the BIRTHPLACE AS PRINTED (the
register's `where found` is the search that produced the person, not a residence, and no death place is held), so each person has one place. A string is
placed where data/era-ground.tsv decided it (the town of that row, at that town's point in data/era-towns.tsv, with the country the Atlas's geo.country_of
gives for the point); a string era-ground.tsv refused (no town) stays unresolved unless data/tree-page/place-additions.json decides it, with its reason, or
the Atlas names it once, in the country the string itself names (the converter's). A point that stands for a department or a section is
labelled as the town era-towns.tsv gives, and says so in `how`. Anything unresolved is listed in tree.report.json (unresolved_places); the person is then
drawn at a relative's birth place (and the page says so) or, with no relative placed, not drawn.
"""
import argparse, collections, datetime, hashlib, io, json, math, os, re, subprocess, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "site", "src", "data")
OUT = os.path.join(ROOT, "data", "tree-page")
TP = os.path.join(ROOT, "tools", "tree-page")
EXT = os.path.join(TP, "painted-lines.ext.html")
HOST = "lerena.defranceski.com"
ATLAS_CANDIDATES = [os.environ.get("RECORD_ATLAS", ""), os.path.expanduser("~/Projects/Family Projects/Record Atlas"),
                    os.path.join(os.path.dirname(ROOT), "Record Atlas")]
INPUTS = ["people.json"]
COUNTRY_ONLY = {"Uruguay", "Argentina", "Italy", "South Africa"}   # drawn at the Atlas's place of that name: a country, not a town
PARTICLES = {"de", "del", "la", "las", "los", "y", "da", "das", "do", "dos", "van", "von", "di", "le"}

def jl(path): return json.load(io.open(path, encoding="utf-8"))
def run(args):
    print("$", " ".join(os.path.relpath(a, ROOT) if os.path.isabs(a) and a.startswith(ROOT) else a for a in args)); r = subprocess.run(args)
    if r.returncode: sys.exit(r.returncode)
def inputs_hash():
    h = hashlib.sha1()
    for n in INPUTS: h.update(io.open(os.path.join(DATA, n), "rb").read())
    for n in ("era-ground.tsv", "era-towns.tsv"): h.update(io.open(os.path.join(ROOT, "data", n), "rb").read())
    for n in ("tree-views.template.html", "painted-lines.ext.html", "gedcom_to_tree.py"): h.update(io.open(os.path.join(TP, n), "rb").read())
    h.update(io.open(os.path.abspath(__file__), "rb").read())
    pa = os.path.join(OUT, "place-additions.json")
    if os.path.exists(pa): h.update(io.open(pa, "rb").read())
    return h.hexdigest()[:16]
def atlas_path():
    for c in ATLAS_CANDIDATES:
        if c and os.path.exists(os.path.join(c, "data", "places.json")): return c
    sys.exit("Record Atlas checkout not found (set RECORD_ATLAS)")

def fold(s): return re.sub(r"[^a-z0-9]+", " ", unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()).strip()
def km(a, b, c, d):
    p = math.pi / 180; x = math.sin((c - a) * p / 2) ** 2 + math.cos(a * p) * math.cos(c * p) * math.sin((d - b) * p / 2) ** 2
    return 12742 * math.asin(math.sqrt(x))

# ---------------------------------------------------------------- names
CAPS = re.compile(r"^[A-ZÁÉÍÓÚÑ]{2,}$")
def clean_name(name):
    n = re.sub(r"\([^)]*\)", " ", name or "")          # the register keeps a relative's name, a date or a note in brackets
    n = re.split(r"\s=\s", n)[0]                         # "Don Luis LERENA (the godfather) = probably Luis ..."
    n = re.sub(r"[\[\]]", "", n)
    return re.sub(r"\s+", " ", n).strip(" ,;")
def split_name(name):
    """given names, surname (the register writes the surname in capitals and a Spanish second surname in ordinary case straight after it)."""
    w = clean_name(name).split(" ")
    w = [x for x in w if x]
    idx = [i for i, x in enumerate(w) if CAPS.match(x) and x.lower() not in PARTICLES]
    if not idx:
        return " ".join(w[:-1]), (w[-1] if w else "")
    i = idx[0]
    if i == 0 and len(idx) > 1 and idx[1] == 1: i = 1                      # "ROQUE LARENA": the first capital word is a given name
    while i > 0 and w[i - 1].lower() in PARTICLES: i -= 1                  # "Juan Carlos DE LEON"
    sur = []
    for j, x in enumerate(w[i:]):
        sur.append(x.capitalize() if CAPS.match(x) and x.lower() not in PARTICLES else x)
    return " ".join(w[:i]), " ".join(sur)
def surname_word(name):
    """the word the colour follows: the first capitalised surname word."""
    w = clean_name(name).split(" ")
    idx = [i for i, x in enumerate(w) if CAPS.match(x) and x.lower() not in PARTICLES]
    if not idx: return fold(w[-1]) if w and w[-1] else ""
    i = idx[0]
    if i == 0 and len(idx) > 1 and idx[1] == 1: i = 1
    return w[i]

def catalogue(atlas):
    """form -> (family id, headline) from the Atlas surname catalogue, for the forms a record has shown to be that family's (same, attested, rule)."""
    d = jl(os.path.join(atlas, "data", "surname-families.json"))
    fam = {}
    for f in d["families"]:
        for m in f.get("members", []):
            if m.get("status") in ("same", "attested", "rule"):
                fam[unicodedata.normalize("NFC", m["form"]).lower()] = (f["id"], f.get("name") or f["id"])
    return fam

# ---------------------------------------------------------------- people.json -> a small GEDCOM
def gdate(v):
    v = "" if v is None else str(v).strip()
    return "" if v in ("-", "") else v

def circa(v):
    """the register writes an approximate year as 1875c or c.1812."""
    v = str(v or ""); return bool(re.search(r"\d{4}", v) and re.search(r"c", v, re.I))

def drawable(people):
    """the people who may be drawn at all: dead on the archive's own reckoning (not living), with a page of their own (not noindex)."""
    return [p for p in people if not p.get("living") and not p.get("noindex") and p.get("slug")]

def edges(people, ids):
    """parent links (child -> {'father','mother'}) and spouse pairs, as the register draws them (not a link that rests only on a tree)."""
    par = collections.defaultdict(dict)
    sp = set()
    for p in people:
        s = p["slug"]
        for k in ("father", "mother"):
            n = p.get(k)
            if n and n.get("slug") in ids and n.get("via") != "tree" and s in ids: par[s].setdefault(k, n["slug"])
        for c in p.get("children") or []:
            if c.get("slug") in ids and c.get("via") != "tree" and s in ids:
                # the child's own father/mother field decides which; a child edge says only that this person is a parent
                q = c["slug"]
                if q not in par or s not in par[q].values():
                    par[q].setdefault("_unsexed", []); par[q]["_unsexed"].append(s)
        for n in p.get("spouses") or []:
            if n.get("slug") in ids and n.get("via") != "tree" and s in ids and n["slug"] != s: sp.add(tuple(sorted((s, n["slug"]))))
    return par, sp

def infer_sex(people, par):
    by = {p["slug"]: p for p in people}
    male, female = set(), set()
    for c, d in par.items():
        if d.get("father"): male.add(d["father"])
        if d.get("mother"): female.add(d["mother"])
    sex, how = {}, collections.Counter()
    for p in people:
        s = p["slug"]
        if s in male and s not in female: sex[s] = "M"; how["named as a father in the register"] += 1; continue
        if s in female and s not in male: sex[s] = "F"; how["named as a mother in the register"] += 1; continue
        nm = clean_name(p["name"]).split(" ")[0]
        if nm == "Don": sex[s] = "M"; how["the title Don in the register's name"] += 1; continue
        if nm in ("Dona", "Doña"): sex[s] = "F"; how["the title Dona in the register's name"] += 1; continue
    return sex, how

def write_ged(people, par, spouses, sex, path):
    ids = {p["slug"] for p in people}
    out = ["0 HEAD", "1 CHAR UTF-8"]
    fams, fam_of_child, fam_of_spouse = {}, {}, collections.defaultdict(list)
    def fam(h, w):
        k = (h or "", w or "")
        if k not in fams: fams[k] = "@F%d@" % (len(fams) + 1)
        return fams[k]
    for p in people:
        s = p["slug"]; d = par.get(s, {})
        f, m = d.get("father"), d.get("mother")
        extra = [x for x in d.get("_unsexed", []) if x not in (f, m)]
        for x in extra:                                                   # a parent the child's own fields do not name: by sex if known, else the free slot
            if sex.get(x) == "F" and not m: m = x
            elif sex.get(x) == "M" and not f: f = x
            elif not f and sex.get(x) != "F": f = x
            elif not m: m = x
        if f or m: fam_of_child[s] = fam(f, m)
    for a, b in sorted(spouses):
        h, w = a, b
        if (sex.get(a) == "F" and sex.get(b) != "F") or (sex.get(b) == "M" and sex.get(a) != "M"): h, w = b, a
        k = fam(h, w)
        for x in (a, b):
            if k not in fam_of_spouse[x]: fam_of_spouse[x].append(k)
    for p in people:
        s = p["slug"]; g, sur = split_name(p["name"])
        out += ["0 @%s@ INDI" % s, "1 NAME %s /%s/" % (g, sur)]
        if sex.get(s): out.append("1 SEX %s" % sex[s])
        b = gdate(p.get("born"))
        if b or p.get("birthplace") not in (None, "", "-"):
            out.append("1 BIRT")
            if b: out.append("2 DATE %s" % b)
            if p.get("birthplace") not in (None, "", "-"): out.append("2 PLAC %s" % p["birthplace"])
        dd = gdate(p.get("died"))
        if dd: out += ["1 DEAT", "2 DATE %s" % dd]
        if s in fam_of_child: out.append("1 FAMC %s" % fam_of_child[s])
        for fx in fam_of_spouse.get(s, []): out.append("1 FAMS %s" % fx)
    for (h, w), fx in fams.items():
        out.append("0 %s FAM" % fx)
        if h: out.append("1 HUSB @%s@" % h)
        if w: out.append("1 WIFE @%s@" % w)
        for cid, f in fam_of_child.items():
            if f == fx: out.append("1 CHIL @%s@" % cid)
    out.append("0 TRLR")
    io.open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")

# ---------------------------------------------------------------- places the archive has already placed
def read_tsv(path):
    rows = []
    for line in io.open(path, encoding="utf-8"):
        if line.startswith("#") or not line.strip(): continue
        rows.append(line.rstrip("\n").split("\t"))
    return rows

def seed_place_map(atlas, used):
    """Place strings this archive has already put on the ground. data/era-ground.tsv decided, for every birthplace string AS PRINTED in people.json, the town it
    belongs to (column 4) or REFUSED it (no town: a country, a continent, a bare name that is several places, a region the Atlas has no ring for); data/era-towns.tsv
    holds each town's point, written by hand. The country is the Atlas's own `geo.country_of` on the point, never a guess from the string; a Record Atlas
    place is linked only where it has the same name within 15 km and the same country."""
    sys.path.insert(0, os.path.join(atlas, "scripts")); import geo
    cj = jl(os.path.join(atlas, "data", "countries.json"))["countries"]
    pj = jl(os.path.join(atlas, "data", "places.json"))["places"]
    byname = collections.defaultdict(list)
    for x in pj:
        for nm in [x["name"]] + [n["n"].split(",")[0] for n in x.get("names", [])]: byname[fold(nm)].append(x)
    towns = {}
    for c in read_tsv(os.path.join(ROOT, "data", "era-towns.tsv")):
        if c[0] == "town" or len(c) < 4: continue
        towns[c[0]] = (float(c[1]), float(c[2]), c[3])
    pm_path = os.path.join(OUT, "place_map.json")
    pm = jl(pm_path) if os.path.exists(pm_path) else {}
    seeded, standin = 0, []
    for c in read_tsv(os.path.join(ROOT, "data", "era-ground.tsv")):
        if len(c) < 4 or c[0] == "place": continue
        raw, town = c[0], c[3].strip()
        if not town or town not in towns or (pm.get(raw) or {}).get("lat") is not None: continue
        lat, lon, how = towns[town]
        iso = geo.country_of(lat, lon)
        if not iso: continue
        plain = re.sub(r"\s*\(.*\)$", "", town)
        hit = next((x for x in byname.get(fold(plain), []) if x.get("country") == iso and km(lat, lon, x["lat"], x["lon"]) <= 15), None)
        pm[raw] = {"name": town, "lat": lat, "lon": lon, "country": cj.get(iso, {}).get("name", iso), "iso": iso, "atlas_id": hit["id"] if hit else None,
                   "how": "data/era-ground.tsv town and data/era-towns.tsv point (%s); country by the Atlas's geo.country_of" % how}
        if "stands for" in how: standin.append(raw)
        seeded += 1
    ap_ = os.path.join(OUT, "place-additions.json")
    if os.path.exists(ap_):
        for k, v in jl(ap_)["places"].items():
            if (pm.get(k) or {}).get("lat") is None: pm[k] = v; seeded += 1
    # last: a string neither era-ground.tsv nor the additions placed, that the Atlas names ONCE, in the country the string itself names. Never a string the
    # archive qualifies (presumed, probably, from a tree, a nationality): that is a guess already, and the page cannot carry the qualifier.
    QUAL = re.compile(r"presum|probabl|likely|perhaps|possibl|\btree|nationality|\?|=", re.I)
    atlas_ok = 0
    for k in sorted(used):
        if (pm.get(k) or {}).get("lat") is not None or QUAL.search(k): continue
        segs = [t.strip() for t in k.split(",")]
        cands = list({x["id"]: x for x in byname.get(fold(segs[0]), [])}.values())
        named = [c for c in cands if fold(cj.get(c["country"], {}).get("name", "")) in fold(k) or fold(c["country"]) == fold(segs[-1])]
        if len(cands) >= 1 and len(named) == 1:
            c = named[0]
            pm[k] = {"name": c["name"], "lat": c["lat"], "lon": c["lon"], "country": cj.get(c["country"], {}).get("name", c["country"]), "iso": c["country"],
                     "atlas_id": c["id"], "how": "the Record Atlas names it once, in the country the string names (the Atlas's own point)"}
            atlas_ok += 1
    standin = [k for k, v in pm.items() if "stands for" in (v.get("how") or "")]
    io.open(pm_path, "w", encoding="utf-8").write(json.dumps(pm, indent=1, ensure_ascii=False))
    print("place_map: %d place strings seeded (era-ground.tsv/era-towns.tsv and place-additions.json), %d from the Atlas by a unique, country-confirmed name" % (seeded, atlas_ok))
    return standin

def build(a):
    os.makedirs(OUT, exist_ok=True)
    allp = jl(os.path.join(DATA, "people.json"))
    people = drawable(allp)
    ids = {p["slug"] for p in people}
    par, spouses = edges(people, ids)
    sex, sexhow = infer_sex(people, par)
    ged = os.path.join(OUT, "people.ged"); write_ged(people, par, spouses, sex, ged)
    io.open(os.path.join(OUT, "slugs.json"), "w", encoding="utf-8").write(json.dumps({s: s for s in ids}, ensure_ascii=False))
    atlas = atlas_path(); standin = seed_place_map(atlas, {p["birthplace"] for p in people if p.get("birthplace") not in (None, "", "-")})
    tree, pm = os.path.join(OUT, "tree.json"), os.path.join(OUT, "place_map.json")
    cmd = [sys.executable, os.path.join(TP, "gedcom_to_tree.py"), ged, "--out", tree, "--place-map", pm, "--atlas", atlas, "--living", "omit",
           "--lines", "8", "--slugs", os.path.join(OUT, "slugs.json"), "--title", "Roots & Routes",
           "--subtitle", "Explore the family tree ten ways: by generation, place, era and relationship. Click anyone and every view follows."]
    run(cmd)
    t = jl(tree)
    by = {p["slug"]: p for p in people}
    cat = catalogue(atlas)
    pmap = jl(pm)
    fam_of = {}
    for s, p in by.items():
        w = surname_word(p["name"]); k = unicodedata.normalize("NFC", w).lower()
        fam_of[s] = cat.get(k) or ("w:" + fold(w), w.capitalize())
    cnt = collections.Counter(fam_of[p["id"]][0] for p in t["people"])
    label = {fam_of[s][0]: fam_of[s][1] for s in fam_of}
    top = [k for k, _ in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))][:7]
    key_i = {k: i for i, k in enumerate(top)}
    for p in t["people"]:
        src = by[p["id"]]
        p["line"] = key_i.get(fam_of[p["id"]][0], 7)
        p["page"] = "/people/%s/" % p["id"]
        g, sur = split_name(src["name"]); p["given"] = g; p["sur"] = sur
        own = pmap.get(src.get("birthplace") or "")
        if not (own and own.get("lat") is not None and own.get("name")): p["bpe"] = True      # drawn at a relative's birth place; the page marks it with an asterisk
        if circa(src.get("born")): p["bye"] = True
        if circa(src.get("died")) and p.get("dy") is not None: p["dye"] = True
    t["lines"] = [{"sur": label[k], "host": HOST} for k in top] + [{"sur": "Other", "host": HOST}]
    t["meta"].update({"rowLabel": "Surname family", "lineLabel": "Surname family"})
    conflicts = drop_conflicts(t, tree)
    rep_path = os.path.splitext(tree)[0] + ".report.json"
    rep = jl(rep_path)
    rep["adapter"] = {
        "people_in_register": len(allp), "living_not_drawn": sum(1 for p in allp if p.get("living")),
        "noindex_not_drawn": sum(1 for p in allp if p.get("noindex") and not p.get("living")),
        "offered_to_converter": len(people), "drawn": len(t["people"]),
        "not_drawn_possibly_living_or_undated_without_a_death": rep["living"],
        "not_drawn_no_birth_year_even_from_kin": len(people) - rep["living"] - rep["dropped_unplaced"] - rep["kept"],
        "not_drawn_no_place_of_their_own_or_a_relatives": rep["dropped_unplaced"],
        "drawn_at_a_relatives_birth_place": rep["placed_from_relative"], "bpe_flagged": sum(1 for p in t["people"] if p.get("bpe")),
        "drawn_at_a_country_only": sum(1 for p in t["people"] if p.get("bp") in COUNTRY_ONLY), "sex_from_the_register": len(sex), "sex_unknown_total": len(people) - len(sex),
        "sex_unknown_drawn": sum(1 for p in t["people"] if sex.get(p["id"]) is None), "sex_how": dict(sexhow),
        "people_with_a_circa_birth_year": sum(1 for p in t["people"] if p.get("bye")),
        "place_strings_standing_in_for_a_department_or_section": sorted(standin), "conflicts_not_drawn": conflicts}
    io.open(rep_path, "w", encoding="utf-8").write(json.dumps(rep, indent=1, ensure_ascii=False))
    io.open(tree, "w", encoding="utf-8").write(json.dumps(t, ensure_ascii=False, separators=(",", ":")))

def drop_conflicts(t, tree):
    """A person whose recorded death comes before their birth, or more than 110 years after it, is not one life. They are not drawn, they are named in
    tree.report.json (conflicts) for the research to settle, and every relation to them is removed so the page stays symmetric."""
    bad = {p["id"] for p in t["people"] if p.get("dy") is not None and not 0 <= p["dy"] - p["by"] <= 110}
    if not bad: return 0
    rep_path = os.path.splitext(tree)[0] + ".report.json"; rep = jl(rep_path)
    rep["conflicts"] = [{"id": p["id"], "born": p["by"], "died": p["dy"]} for p in t["people"] if p["id"] in bad]
    t["people"] = [p for p in t["people"] if p["id"] not in bad]
    for p in t["people"]:
        for k in ("father", "mother"):
            if p.get(k) in bad: p[k] = None
        p["spouse"] = [x for x in p["spouse"] if x not in bad]; p["kids"] = [x for x in p["kids"] if x not in bad]
    if t.get("focus") in bad: t["focus"] = t["people"][0]["id"]
    io.open(rep_path, "w", encoding="utf-8").write(json.dumps(rep, indent=1, ensure_ascii=False))
    print("conflicts: %d people whose death is before their birth are not one life (died before born, or over 110 years) and are not drawn" % len(bad))
    return len(bad)

def write_roots_links(tree):
    """site/public/roots-links.json: the people Roots & Routes DRAWS (one id each)."""
    ids = sorted(p["id"] for p in jl(tree)["people"])
    out = {"note": "The people Roots & Routes draws, by person id. Made by tools/build-tree-page.py; do not edit by hand.", "people": ids}
    io.open(os.path.join(ROOT, "site", "public", "roots-links.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print("roots-links: %d people" % len(ids))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        try: have = jl(os.path.join(OUT, "tree.json"))["meta"]["inputs"]
        except Exception: print("tree page: not built yet. python3 tools/build-tree-page.py"); sys.exit(1)
        if have != inputs_hash(): print("tree page is STALE: the people, the era-ground files, the place additions or the builder changed since it was built.\n  python3 tools/build-tree-page.py"); sys.exit(1)
        print("tree page is current"); return
    build(a)
    tree = os.path.join(OUT, "tree.json"); ad = os.path.join(OUT, "atlas-data.json"); page = os.path.join(OUT, "roots.html"); pm = os.path.join(OUT, "place_map.json")
    run([sys.executable, os.path.join(TP, "build_atlas_data.py"), "--atlas", atlas_path(), "--tree", tree, "--place-map", pm, "--out", ad])
    t = jl(tree); t["meta"]["inputs"] = inputs_hash()
    io.open(tree, "w", encoding="utf-8").write(json.dumps(t, ensure_ascii=False, separators=(",", ":")))
    write_roots_links(tree)
    tpl = os.path.join(TP, "tree-views.template.html")
    run([sys.executable, os.path.join(TP, "build_page.py"), "--template", tpl, "--tree", tree, "--atlas-data", ad, "--out", page, "--ext", EXT])
    embed = os.path.join(OUT, "roots.embed.html")
    run([sys.executable, os.path.join(TP, "build_page.py"), "--template", tpl, "--tree", tree, "--atlas-data", ad, "--out", embed, "--embed", "--ext", EXT])
    run([sys.executable, os.path.join(TP, "check_tree_page.py"), "--tree", tree, "--atlas-data", ad, "--page", page])
    run([sys.executable, os.path.join(TP, "check_tree_page.py"), "--tree", tree, "--atlas-data", ad, "--page", embed])

if __name__ == "__main__": main()
