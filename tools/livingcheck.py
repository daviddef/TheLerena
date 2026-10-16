#!/usr/bin/env python3
"""The living-people gates' shared INDEPENDENT reckoning. Not a gate itself.

WHY THIS IS NOT IMPORTED FROM tools/build-people.py. A gate that asks the generator who is
living can only ever agree with it: if the generator drops a person, the gate drops them too and
reports a pass. So this file reads the RAW DATA (the register, the working files, the relations
list) and applies the estate's one definition of living (the kit's living_rule.py, pinned in
site/package.json) with its own parsing, then the gates compare that answer with what the
generator wrote (people.json) and with what the build printed (dist).

If this file and build-people.py ever disagree about a person, THE BUILD FAILS and says who, which
is the point: neither is trusted alone.

THE POPULATION. Everybody the archive names who has a page or should have one:
  - every row of data/lerena-register.tsv (born_est, citations, the `source` column);
  - every other name in data/relations.tsv, whose birth and death are read from the family chart's
    working files (lerena-siblings-gen3.tsv, direct-line.tsv) or, failing that, from the dates the
    chart already prints on a node.
A RECORDED DEATH OR BURIAL, however this archive records it: last-attested-alive.tsv (any tier
beginning DEATH, ceilings included - a ceiling is a death of uncertain year), the Johannesburg
cemetery register's burial and death rows, the working files' own death columns.

THE NET. The two 1999 deaths of a wife and a younger son were recorded ONLY as burial registrations,
in a file the old generator did not read, so a rule that looked only at a death column would have
published them as living. So a person this reckoning calls living whose register `source` or recorded
evidence speaks of a death, burial or cemetery is reported as SUSPECT and fails the gate: either the
death is missing from the data, or the wording is about somebody else, and a human decides.
"""
import json
import os
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent


def kit_rule(root):
    d = pathlib.Path(root) / "site" / "node_modules" / "@daviddef" / "archive-kit" / "kit" / "tools"
    if not (d / "living_rule.py").exists():
        raise SystemExit(f"  FAIL  kit        {d}/living_rule.py is missing - the kit pin must be 0a56c86 or later "
                         "and `npm install` run in site/")
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))
    import living_rule
    return living_rule


def fold(s):
    s = re.sub(r"\(.*?\)", " ", str(s or ""))
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return " ".join(s.replace('"', " ").casefold().split())


def byear(s):
    m = re.search(r"\b(1[0-9]{3}|20[0-9]{2})", str(s or ""))
    return int(m.group(1)) if m else None


def plainmark(s):
    return re.sub(r"\*\*\*\s*(.+?)\s*\*\*\*", r"\1", str(s or ""), flags=re.S).strip()


def tsv(path):
    path = pathlib.Path(path)
    if not path.exists():
        return []
    lines = [l.rstrip("\n") for l in path.read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]
    if not lines:
        return []
    h = lines[0].split("\t")
    return [dict(zip(h, (l.split("\t") + [""] * len(h))[:len(h)])) for l in lines[1:]]


def edges(root):
    out = []
    p = pathlib.Path(root) / "data" / "relations.tsv"
    if p.exists():
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.strip() and not l.startswith("#"):
                out.append((l.split("\t") + [""] * 6)[:6])
    return out[1:]


# ---- town and country, reckoned here and not borrowed from the generator --------------------
_COUNTRIES = {"south africa", "uruguay", "argentina", "england", "scotland", "wales", "ireland",
              "australia", "spain", "italy", "chile", "brazil", "paraguay", "france", "portugal",
              "germany", "canada", "new zealand", "united states", "usa", "namibia", "zimbabwe",
              "mozambique", "croatia", "united kingdom", "uk", "netherlands", "switzerland"}
_TOWN_COUNTRY = {"johannesburg": "South Africa", "cape town": "South Africa", "pretoria": "South Africa",
                 "durban": "South Africa", "bloemfontein": "South Africa", "germiston": "South Africa",
                 "montevideo": "Uruguay", "buenos aires": "Argentina", "rosario": "Argentina",
                 "brisbane": "Australia", "sydney": "Australia", "perth": "Australia",
                 "melbourne": "Australia", "london": "England", "bideford": "England"}
_ADDRESSY = re.compile(r"\d|\b(street|st\.|road|rd\.?|avenue|ave\.?|lane|drive|close|crescent|hospital|"
                       r"clinic|infirmary|care|nursing|home|hospice|asylum|prison|school|college|farm|"
                       r"po box|p\.o\.)\b", re.I)


def expected_place(*raws):
    """(town, country, raw) a living person may show; raw is the string the data actually holds."""
    for raw in raws:
        parts = [x.strip() for x in str(raw or "").replace("/", ",").split(",") if x.strip() and x.strip() != "-"]
        if not parts:
            continue
        country = ""
        if parts[-1].casefold() in _COUNTRIES:
            country = parts.pop()
        towns = [x for x in parts if not _ADDRESSY.search(x)]
        if not towns:
            continue
        town = towns[0]
        if not country:
            country = _TOWN_COUNTRY.get(town.casefold(), "")
        return town, country.title() if country.islower() else country, raw
    return "", "", ""


def date_variants(s):
    """Every way a full date in `s` might be printed. A BARE YEAR IS NOT SCREENED SITE-WIDE: on a
    genealogy site every year appears somewhere, and a gate that fires on all of them is switched off.
    (A living person's OWN page is screened for any year at all: see check-living-standard.py.)"""
    out = set()
    mon = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep",
                                            "oct", "nov", "dec"])}
    full = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
            "October", "November", "December"]
    for m in re.finditer(r"\b(\d{1,2})\s+([A-Za-z]{3,9})\.?\s+((?:1[89]|20)\d\d)\b", str(s or "")):
        d, mn, y = int(m.group(1)), m.group(2)[:3].lower(), m.group(3)
        if mn in mon:
            k = mon[mn]
            out |= {m.group(0), f"{d} {full[k-1]} {y}", f"{d} {full[k-1][:3]} {y}", f"{y}-{k:02d}-{d:02d}",
                    f"{d:02d}/{k:02d}/{y}", f"{d}/{k}/{y}", f"{full[k-1]} {d}, {y}"}
    for m in re.finditer(r"\b((?:1[89]|20)\d\d)-(\d{2})-(\d{2})\b", str(s or "")):
        y, k, d = m.group(1), int(m.group(2)), int(m.group(3))
        if 1 <= k <= 12:
            out |= {m.group(0), f"{d} {full[k-1]} {y}", f"{d} {full[k-1][:3]} {y}"}
    return out


class P:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __repr__(self):
        return f"P({self.slug})"


def population(root=ROOT, today=None):
    """Everybody, with living / held-out reckoned from the raw data by the estate's one rule."""
    root = pathlib.Path(root)
    lr = kit_rule(root)
    year = int(today or os.environ.get("LIVING_TODAY_YEAR") or lr.this_year())
    ledger = json.loads((root / "site" / "src" / "data" / "person-slugs.json").read_text(encoding="utf-8"))["slugs"]

    dead_exact, dead_arks, dead_folded = set(), set(), set()
    for r in tsv(root / "data" / "last-attested-alive.tsv"):
        if (r.get("tier") or "").strip().upper().startswith("DEATH"):
            dead_exact.add((r.get("name") or "").strip())
    for r in tsv(root / "data" / "johannesburg-cemetery-1999.tsv"):
        if re.search(r"\b(death|burial|buried)\b", plainmark(r.get("what the register gives")), re.I):
            dead_folded.add(fold(plainmark(r.get("person"))))
            a = (r.get("ark") or "").strip()
            if re.fullmatch(r"\d:\d:[A-Z0-9-]+", a):
                dead_arks.add(a)

    ev = {}
    for l in (root / "data" / "person-evidence.tsv").read_text(encoding="utf-8").splitlines():
        if l.strip() and not l.startswith("#"):
            c = (l.split("\t") + [""] * 5)[:5]
            ev.setdefault(c[0].strip(), []).append((c[1], c[2]))

    held_ids = []
    hf = root / "data" / "held-out-ids.txt"
    if hf.exists():
        held_ids = [l.split("#")[0].strip() for l in hf.read_text(encoding="utf-8").splitlines() if l.split("#")[0].strip()]

    rows = tsv(root / "data" / "lerena-register.tsv")
    people, names = [], set()
    fold_count = {}
    for r in rows:
        fold_count[fold(r["name"])] = fold_count.get(fold(r["name"]), 0) + 1
    for r in rows:
        name = r["name"]
        names.add(name)
        ark = (r.get("ark") or "").strip()
        url = ("https://www.familysearch.org/ark:/61903/" + ark) if ark and not ark.startswith("tree:") else \
              ("https://www.familysearch.org/tree/person/details/" + ark[5:] if ark.startswith("tree:") else "")
        cites = [r.get("source", ""), url] + [x[1] for x in ev.get(name, [])]
        evtext = [r.get("source", "")] + [x[0] for x in ev.get(name, [])]
        people.append(P(name=name, slug=ledger.get(name, ""), kind="register",
                        by=byear(r.get("born_est")),
                        dead=(name in dead_exact or any(a in r.get("source", "") for a in dead_arks)
                              or (fold(name) in dead_folded and fold_count[fold(name)] == 1)),
                        cites=cites,
                        evtext=evtext, raw_places=[r.get("birthplace", ""), r.get("where_found", "")],
                        private_dates=date_variants(r.get("born_est")) , born_raw=r.get("born_est", "")))

    sib = {fold(r.get("person")): r for r in tsv(root / "data" / "lerena-siblings-gen3.tsv")}
    dln = {fold(r.get("person")): r for r in tsv(root / "data" / "direct-line.tsv")}
    edge_dates = {}
    for who, rel, oth, dt, via, note in edges(root):
        if dt and dt != "-":
            edge_dates.setdefault(oth, dt)
    seen_supp = []
    for who, rel, oth, *_ in edges(root):
        for n in (who, oth):
            if n and n not in names and n not in seen_supp:
                seen_supp.append(n)
    for n in seen_supp:
        f = fold(n)
        s, d = sib.get(f, {}), dln.get(f, {})
        pb = (d.get("born") or s.get("born") or "").strip()
        pd = (d.get("died") or s.get("died") or "").strip()
        ed = re.fullmatch(r"\s*(\d{4})\s*[-–]\s*(\d{4})\s*", edge_dates.get(n, ""))
        if not pb and not pd and ed:
            pb, pd = ed.group(1), ed.group(2)
        people.append(P(name=n, slug=ledger.get(n, ""), kind="supplementary",
                        by=byear(pb), dead=bool(pd), cites=[], evtext=[],
                        raw_places=[d.get("born_place", "")],
                        private_dates=date_variants(pb) | date_variants(pd), born_raw=pb))

    # living, then parents' living-ness for the undated minors
    for p in people:
        p.living = lr.is_living(p.by, p.dead, p.cites, year)
    living_names = {p.name for p in people if p.living}
    parents = {}
    for who, rel, oth, *_ in edges(root):
        if rel in ("father", "mother"):
            parents.setdefault(who, set()).add(oth)
        elif rel == "child":
            parents.setdefault(oth, set()).add(who)
    for p in people:
        pl = any(x in living_names for x in parents.get(p.name, ()))
        p.held = lr.is_held_out(p.slug, p.by, p.dead, p.cites, pl, held_ids, year)
        if p.held:
            p.living = False
        town, country, raw = expected_place(*p.raw_places)
        p.town, p.country, p.raw_place = town, country, raw
        net = re.compile(r"\b(burial|buried|interment|interred|cemetery|died|death|deceased)\b", re.I)
        p.suspect = bool(p.living and any(net.search(t or "") for t in p.evtext))
    return people, lr, year
