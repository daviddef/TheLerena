#!/usr/bin/env python3
"""Lerena's places, for the map — Argentina, South Africa and the English west."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "site", "node_modules",
                                "@daviddef", "archive-kit", "kit", "tools"))
import atlasdata
D = os.path.join(HERE, "..", "site", "src", "data")
J = lambda n: json.load(open(os.path.join(D, n), encoding="utf-8"))
OUT = os.path.join(HERE, "..", "site", "public", "atlas-data.json")

def cat(p):
    s = p.lower()
    if re.search(r"argentin|rosario|buenos|montevideo|uruguay|santa fe", s): return "ar"
    if re.search(r"south africa|cape|natal|transvaal|johannesburg|durban|kimberley", s): return "za"
    if re.search(r"england|london|devon|suffolk|northam|somerset|bristol|cornwall", s):  return "en"
    return "other"

def main():
    places = J("places.json")
    ppl = {}
    for p in J("people.json"):
        if p.get("slug"): ppl[p["slug"]] = p
    rows = []
    for p in places:
        name = p["name"]
        slugs = p.get("people") or []
        rows.append({
            "name": name.split(",")[0].strip() or name,
            "_lookup": name, "cat": cat(name),
            "n": p.get("count") or len(slugs),
            "what": name,
            "people": [{"n": (ppl.get(s) or {}).get("name") or s.replace("-", " ").title(),
                        "w": f"/people/{s}/" if s in ppl else None} for s in slugs[:12]],
            "more": max(0, len(slugs) - 12) or None,
            "href": f"/places/{p['slug']}/" if p.get("slug") else None,
        })
    atlasdata.build(rows, OUT, countries=["Argentina","Uruguay","South Africa","Suid-Afrika","United Kingdom","Ireland","Australia"])

if __name__ == "__main__":
    sys.exit(main())
