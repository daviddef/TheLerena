#!/usr/bin/env python3
"""Generate site/src/data/people.json and places.json from data/lerena-register.tsv.

The register is the single source of truth. Run this after every edit to it, so the
pages and the data cannot drift apart.
"""
import json, re, unicodedata, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG  = ROOT / "data" / "lerena-register.tsv"
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
    if re.match(r"^arr\.?\s*\d{4}", w) or "arrival" in w.lower():
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

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "people.json").write_text(json.dumps(people, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
(OUT / "places.json").write_text(json.dumps(places, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"{len(people)} people, {len(places)} places")
