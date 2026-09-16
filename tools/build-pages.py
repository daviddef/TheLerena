#!/usr/bin/env python3
"""Turn the plain TSVs into JSON the site can import.

Same discipline as build-people.py: the TSV is the source of truth, the page is generated,
so a page and its data cannot drift apart.
"""
import json, pathlib, re

# --- the shared row contract -------------------------------------------------
# All seven archives emit {k,t,s,h,q}: kind, title, subtitle, href, and a
# lowercased accent-folded haystack, because one component in
# @daviddef/archive-kit reads all seven indexes.
def _fold(s):
    import unicodedata
    s = unicodedata.normalize("NFD", str(s or ""))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()

def to_contract(rows):
    out = []
    for r in rows:
        k = str(r.get("k", "Page")); t = r.get("t", "")
        s = r.get("s", r.get("d", "")); h = r.get("h", r.get("u", ""))
        q = r.get("q", r.get("x", ""))
        out.append({"k": k[:1].upper() + k[1:], "t": t, "s": s, "h": h,
                    "q": _fold(" ".join([str(t), str(s), str(q)]))})
    return out

def plain(s):
    """The TSVs mark emphasis as *** like this ***. The search index is plain text
    rendered into JS, so strip the markers rather than carry them into the box."""
    return re.sub(r"\*\*\*\s*(.+?)\s*\*\*\*", r"\1", str(s or ""), flags=re.S)

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "src" / "data"
OUT.mkdir(parents=True, exist_ok=True)

def rows(name):
    p = ROOT / "data" / f"{name}.tsv"
    lines = [l.rstrip("\n") for l in p.open(encoding="utf-8")
             if l.strip() and not l.startswith("#")]
    hdr = lines[0].split("\t")
    out = []
    for l in lines[1:]:
        cells = (l.split("\t") + [""] * len(hdr))[:len(hdr)]
        out.append(dict(zip(hdr, cells)))
    return out

# The Taylor page carried its ten siblings as a HARDCODED ARRAY duplicating data/taylor-line.tsv -
# the exact drift this whole build exists to prevent. On 14 September 2026 the TSV gained five
# husbands' names and the page went on saying "m. Dalling". Generated from the TSV since.
# Every column is passed through, which is how the `key` column on errands.tsv
# reaches errands.json. That key is what the work-list gate counts outstanding
# errands against, and it has to live in the TSV: keys written into the JSON by
# hand lasted exactly until the next build, and the gate then reported nothing
# to count for an archive with twenty outstanding items.
for name in ("corrections", "errands", "gaps", "timeline", "photograph-these",
             "sources-consulted", "taylor-line", "dna-match-probes",
             "marriage-1911", "death-notices-read", "pablo-armando-passport",
             "tab-pull-list-2026-09-22", "family-memory", "death-notice-1950", "llorens-1872", "gedcom-2018", "gedcom-harvest", "brayley-convergence"):
    data = rows(name)
    (OUT / f"{name}.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n",
                                      encoding="utf-8")
    print(f"{name}: {len(data)} rows")

# ---- search index -------------------------------------------------------
# One box across everything the site holds. Built from the same data the pages use,
# so a thing cannot be findable and absent, or present and unfindable.
people = json.loads((OUT / "people.json").read_text(encoding="utf-8"))
places = json.loads((OUT / "places.json").read_text(encoding="utf-8"))

idx = []
for p in people:
    idx.append({"t": plain(p["name"]), "k": "person", "u": f"/people/{p['slug']}/",
                "d": plain(" · ".join(x for x in [p["born"], p["birthplace"], p["occupation"], p["source"]]
                                if x and x != "-")),
                "s": p["statusRaw"]})
for pl in places:
    idx.append({"t": pl["name"], "k": "place", "u": f"/places/{pl['slug']}/",
                "d": f"{pl['count']} of this surname recorded here", "s": ""})
for r in rows("timeline"):
    idx.append({"t": plain(f"{r['year']} — {r['what'][:90]}"), "k": "timeline", "u": "/timeline/",
                "d": r["source"], "s": r["kind"]})
for r in rows("corrections"):
    idx.append({"t": f"Correction, {r['date']}", "k": "correction", "u": "/corrections/",
                "d": plain(r["what_is_true"])[:180], "s": r["severity"]})
for r in rows("errands"):
    idx.append({"t": plain(r["what"]), "k": "errand", "u": "/errands/", "d": r["who"], "s": r["status"]})
for r in rows("gaps"):
    idx.append({"t": plain(r["gap"]), "k": "gap", "u": "/gaps/", "d": plain(r["why_it_may_never_close"])[:180], "s": ""})
for r in rows("photograph-these"):
    idx.append({"t": plain(r["what"]), "k": "photograph", "u": "/photograph-these/", "d": r["where"], "s": ""})
for r in rows("sources-consulted"):
    idx.append({"t": plain(r["source"])[:90], "k": "source", "u": "/sources/",
                "d": plain(r["used_for"])[:180], "s": r["tier"]})

PAGES = [
    ("The line", "/direct-line/", "The descent, generation by generation, with a record behind every step"),
    ("The enrolment card", "/enrolment-card/", "The 1908 army card that named Juan Carlos and María Lerena"),
    ("The passport", "/passport/", "Série A No. 07962, Cape Town, 24 December 1940"),
    ("The estate", "/estate/", "The 1950 liquidation account, and £26 of carrots"),
    ("The DNA", "/dna/", "A granddaughter's test: a Río de la Plata genetic group, and no Iberian at all"),
    ("The horses", "/horses/", "Trainer, horse-dealer, race horse owner, and a yard at Rugby"),
    ("The Taylors", "/taylor/", "Mary Septima, of Bideford and Northam in north Devon"),
    ("Argentina", "/argentina/", "Rosario, the registers, and what has been read there"),
    ("South Africa", "/south-africa/", "The Cape, the Rand, the estates and the graves"),
    ("The name", "/name/", "2,124 Lerenas worldwide, and the densest concentration in Uruguay"),
    ("The register", "/register/", "Every named individual this archive has found"),
    ("What has been read", "/searched/", "Every search made, including the ones that led nowhere"),
    ("Hypotheses", "/hypotheses/", "Everything unproved, set out together"),
    ("Open questions", "/open-questions/", "Published so strangers can help"),
    ("Method", "/method/", "How this archive decides what it is willing to say"),
    ("Sources", "/sources/", "Consulted, and identified but not yet consulted"),
    ("The archives", "/naairs/", "NAAIRS and the South African depots"),
    ("Roadmap", "/roadmap/", "What is being worked on next"),
]
for t, url, d in PAGES:
    idx.append({"t": t, "k": "page", "u": url, "d": d, "s": ""})

(OUT / "searchindex.json").write_text(json.dumps(to_contract(idx), ensure_ascii=False) + "\n", encoding="utf-8")
print(f"searchindex: {len(idx)} entries")
