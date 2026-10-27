#!/usr/bin/env python3
"""Make site/src/data/lerena-lines.json (the drawing on /lines/) and site/src/data/lerena-lines-ledger.json (the tables under
it) from the archive's own data. (25 October 2026; every person placed, 27 October 2026)

    python3 tools/build-lines.py                 place every person in the register on one lane or in one pen, re-derive the
                                                 `kin` rows of data/people-lines.tsv, then write both JSON files
                                                 (the build runs this, as it runs same:data: a register commit moves the rows, never fails)
    python3 tools/build-lines.py --check         fail (and rewrite nothing in data/) if data/people-lines.tsv is out of date
    python3 tools/build-lines.py --living-slugs  write the list of slugs the kit's lines gate (P3) must never find on a lane or in a
                                                 pen, OUTSIDE the repository (--living-path prints where), and stop

THE DRAWING IS THE KIT'S (BranchRivers); THE DATA IS THIS ARCHIVE'S. The kit's contract is kit/docs/lines.md and its gate is
`npm run check:lines`. What this archive adds to the contract is where the lines come from:

  data/lerena-lines.tsv           one row per lane: its status (documented | inferred | origin-unknown | family-lore), the
                                  documented years (span), the note after the tier, the nodes ("place|year|what the document
                                  says", ";;"-separated) and, in parallel lists, the person page and the evidence word of
                                  each node. A status is a research decision: it is written here by hand and by nobody else.
  data/lerena-lines-unplaced.tsv  the households the archive has written up that are on no lane: kind unplaced (-> the pen
                                  of households not yet placed) or namesake (-> the different-stock pen); `people` names the
                                  register people the row is about, and `href` is the page that works it.
  data/lerena-lines-joins.tsv     every join between two lines, or a line and a household, that the archive has a verdict on:
                                  documented | candidate | refused | open, in the archive's own words. A candidate is drawn as
                                  the kit's bridge; all of them are printed in the table on /lines/. Written by hand.
  data/people-lines.tsv           the person-to-lane file. `anchor` and `spouse` rows are written by hand, each with the
                                  archive's own statement in `basis` (a node of the lane, an act that names a parent); `kin`
                                  rows are DERIVED by this tool (never by hand).

THE RULE THAT PLACES EVERY PERSON (it is printed on /lines/ from RULE below, so the page and the tool cannot disagree):

  1. Kin are the register's own links: father, mother, child, spouse, brother and sister (people.json). A link that rests only on
     a family tree (`via: tree`) is not followed. A godparent, a witness, an official or a neighbour is not kin.
  2. Following those links splits the register into family groups. A lane holds the groups that contain one of its SEEDS: a
     person on one of its nodes, or a person data/people-lines.tsv puts on it with the archive's statement.
  3. A group that holds the seeds of two lanes is a join. It is allowed only where data/lerena-lines-joins.tsv records that join
     as documented (the direct line and the Taylor line, by the marriage of 1911); each person then goes to the lane of the
     nearest seed counted in links, a tie going to the lane drawn first. Any other such group stops the build.
  4. A group on no lane is a household not yet placed. Where a row of data/lerena-lines-unplaced.tsv names one of its people
     it is that row's household (a namesake row puts it with the different stock); otherwise it is drawn as a household of its
     own when it has two people or more and one of them carries the name.
  5. A person on no lane and in no such household is counted in one of two pens: people of the name with no family recorded
     here, or people in the acts who are not of the name (godparents, witnesses, officials) and are kin to nobody here.
  6. Everybody is counted. A person is LISTED by name only if their page publishes a birth year before the living line or a
     death, and they are not living or held out by any rule this archive keeps (tools/livingcheck.py, people.json, the
     unpublished deaths). Everybody else is a number only.

THE COUNT UNDER A LANE IS NOT "EVERYONE DESCENDED". It is the people this archive has placed on the line by these links, no more.
"""
import argparse
import collections
import json
import os
import pathlib
import re
import sys
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import livingcheck as L  # noqa: E402

DATA = ROOT / "data"
SITE = ROOT / "site" / "src" / "data"
LANES_TSV = DATA / "lerena-lines.tsv"
PENS_TSV = DATA / "lerena-lines-unplaced.tsv"
JOINS_TSV = DATA / "lerena-lines-joins.tsv"
PEOPLE_TSV = DATA / "people-lines.tsv"
OUT = SITE / "lerena-lines.json"
LEDGER = SITE / "lerena-lines-ledger.json"
DIRECT = SITE / "direct-line.json"
OURS = ({p["slug"] for p in json.loads(DIRECT.read_text(encoding="utf-8")).get("people", [])} if DIRECT.exists() else set())

TITLE = "The lines of the name Lerena, side by side, with every household and person the archive holds that is on none of them"
STATUSES = ("documented", "inferred", "origin-unknown", "family-lore")
EVIDENCE = ("read", "indexed", "scanned", "tree", "inferred", "disputed", "none")
JOIN_STATUSES = ("documented", "candidate", "refused", "open")

# The spellings this archive has met for the name (data/name-variants.tsv, less HERENCIA, which is not a name at all). A person
# "carries the name" when one of these is a word of their register name after the first word, outside brackets.
SPELLINGS = ("LERENA", "LLERENA", "SERENA", "GERENA", "PERENA", "LORENA", "LEVENA", "LERESA", "LARENA", "LERINA", "LERRENA")

RULE = [
    "Kin are the register's own links: father, mother, child, spouse, brother and sister. A link that rests only on a family tree is not followed, and a godparent, a witness, an official or a neighbour is not kin.",
    "Following those links splits the register into family groups. A line holds every group that contains one of its seeds: a person on one of its dated stops, or a person the archive puts on it by an act it quotes (data/people-lines.tsv).",
    "A group that holds the seeds of two lines is a join. It is allowed only where the archive records that join as documented, as it does for the direct line and the Taylor line, joined by the marriage of 1911; each person then goes to the line of the nearest seed, counted in links.",
    "A group on no line is a household not yet placed. Where a household the archive has written up names one of its people, it is that household; otherwise it is counted as a household of its own when it holds two people or more and one of them carries the name.",
    "Anyone on no line and in no household is counted in one of two pens: people of the name with no family recorded here, or people in the acts who are not of the name and are kin to nobody here.",
    "Everybody is counted, and nobody is counted twice. A person is listed by name only when their page publishes a birth year before the living line or a death, and no rule of this archive holds them as living or out of publication; everybody else is a number only.",
]

PEN_HEAD = {
    "households": "Real households of the name — on none of these lines",
    "single": "People of the name with no family recorded here — on none of these lines",
    "others": "In the acts but not of the name, and kin to nobody on a line",
    "namesake": "A different stock of the same name — kept apart on purpose",
}
PEN_NOTE = {
    "households": ("Real, documented households of the name that this archive has read and not joined to any line above. "
                   "They sit below the rule so that the picture cannot imply that everything has been placed. "
                   "What would move one onto a line is a document that names its parents, or an act that ties it to a household already drawn."),
    "single": ("People of the name the register holds with no parent, child, spouse, brother or sister recorded here: arrivals off a ship, "
               "godparents, a name on one act. Each is a real person on a real record; none is joined to anybody, so none is on a line."),
    "others": ("Godparents, witnesses, priests, judges and neighbours, kept in the register because an act of the family names them. "
               "They are not of the name and are not kin to anybody on a line, so they are counted here and drawn on no lane."),
    "namesake": ("Names that look like this one and are kept apart on purpose: found while searching, recorded so that nobody has to "
                 "discover them twice. No connection is claimed between any of them and any line above."),
}
PEN_KIND = {"households": "not-yet-placed", "single": "not-yet-placed", "others": "not-yet-placed", "namesake": "different-stock"}
PEN_ID = {"households": "not-yet-placed", "single": "of-the-name-alone", "others": "not-of-the-name", "namesake": "different-stock"}
PEN_ORDER = ("households", "single", "others", "namesake")

PEOPLE_HEADER = """# *** WHO STANDS ON WHICH LINE (the person-to-lane file for the drawing on /lines/). 25 October 2026; every person placed, 27 October 2026. ***
#
# Written for the kit's lines contract (kit/docs/lines.md): a lane may list the people on it, and the kit gate holds the built page to
# three rules - nobody living is listed (P3), nobody stands on two lines (E1), every link lands (P1).
#
# lane      the key of a lane in data/lerena-lines.tsv
# slug      the person page, /people/<slug>/
# how       anchor      a person the archive itself puts on the line, with the statement in `basis` (written by hand): a node of the
#                       lane, a register name that says "son of Sancho", or an act the register's note quotes that names a parent on
#                       the line when the register does not yet draw that link
#           spouse      the wife of an anchor, named as such in the register (written by hand)
#           kin         DERIVED by tools/build-lines.py: in the same family group as a seed of the lane by the register's own links
#                       (never by hand: the build re-derives them whenever the register moves)
# basis     the archive's own words for why
#
# A `kin` row is written only for a person who may be listed (a birth year before the living line or a death on their page, and not
# living or held out); everybody else on the lane is counted and not named. The number a reader sees under a lane is the people
# placed here by these links; it is not everyone who descended.
lane\tslug\thow\tbasis"""


def tsv(path):
    lines = [l.rstrip("\n") for l in path.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    hdr = lines[0].split("\t")
    return [dict(zip(hdr, (l.split("\t") + [""] * len(hdr))[:len(hdr)])) for l in lines[1:]]


def year_of(s):
    m = re.search(r"(?<!\d)(\d{4})(?!\d)", str(s or ""))
    return int(m.group(1)) if m else None


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s or "")) if unicodedata.category(c) != "Mn").upper()


def clean_name(n):
    """The register name without its bracketed gloss: «Cipriano LERENA (of Trinidad)» -> «Cipriano LERENA»."""
    n = re.sub(r"\s*\([^)]*\)", "", str(n or "")).replace('"', "")
    n = re.sub(r"\s*=.*$", "", n)
    return re.sub(r"\s+", " ", n).strip()


def carries_name(n):
    words = re.findall(r"[A-Z]+", fold(clean_name(n)))
    return any(w in SPELLINGS for w in words[1:])


def load_people():
    rows = json.loads((SITE / "people.json").read_text(encoding="utf-8"))
    return {r["slug"]: r for r in rows}


def unpublished_dead():
    p = DATA / "living-year-allow.json"
    if not p.exists():
        return set()
    return {e["slug"] for e in json.loads(p.read_text(encoding="utf-8")).get("unpublished_deaths", [])}


def kin_graph(people):
    """The register's own links, both ways round: father, mother, children, spouses, siblings; never a link resting on a tree."""
    g = collections.defaultdict(set)
    for r in people.values():
        for k in ("father", "mother", "children", "spouses", "siblings"):
            v = r.get(k)
            for x in ([v] if isinstance(v, dict) else (v or [])):
                o = (x or {}).get("slug")
                if o and o in people and o != r["slug"] and x.get("via") != "tree":
                    g[r["slug"]].add(o)
                    g[o].add(r["slug"])
    return g


def groups_of(people, g):
    comp, out = {}, []
    for s in sorted(people):
        if s in comp:
            continue
        stack, members = [s], []
        comp[s] = len(out)
        while stack:
            x = stack.pop()
            members.append(x)
            for y in sorted(g.get(x, ())):
                if y not in comp:
                    comp[y] = len(out)
                    stack.append(y)
        out.append(sorted(members))
    return comp, out


def eligible(slug, people, cutoff, unpub):
    """May this person stand in a list of people on a public page? (the rule build-lines.py has kept since 25 October)"""
    r = people.get(slug)
    if not r or r.get("living") or r.get("noindex") or slug in unpub:
        return False
    by = year_of(r.get("born"))
    return (by is not None and by < cutoff) or bool(str(r.get("died") or "").strip())


def safe(slug, people, unpub):
    """The floor for a person a node or a hand-written row names: a page that exists, not living, not held out, not an unpublished death."""
    r = people.get(slug)
    return bool(r) and not r.get("living") and not r.get("noindex") and slug not in unpub


def living_path():
    if os.environ.get("LINES_LIVING"):
        return pathlib.Path(os.environ["LINES_LIVING"])
    base = os.environ.get("XDG_STATE_HOME") or str(pathlib.Path.home() / ".local" / "state")
    return pathlib.Path(base) / "lerena" / "lines-living.json"


def living_slugs():
    """Everybody a list of people must not carry: the living and the held-out by the independent reckoning every living gate here uses
    (tools/livingcheck.py), anybody people.json marks living or noindex, and the people the data records dead but no page prints."""
    pop, _lr, _year = L.population(ROOT)
    out = {p.slug for p in pop if (p.living or getattr(p, "held", False)) and p.slug}
    out |= {sl for sl, r in load_people().items() if r.get("living") or r.get("noindex")}
    out |= unpublished_dead()
    return sorted(out)


def nearest(seeds_by_lane, g, members, rank):
    """In one family group holding the seeds of more than one lane: each person -> the lane of the nearest seed (links), ties to
    the lane drawn first."""
    best = {}
    for lane in sorted(seeds_by_lane, key=lambda k: rank[k]):
        dist = {s: 0 for s in seeds_by_lane[lane]}
        q = collections.deque(sorted(seeds_by_lane[lane]))
        while q:
            x = q.popleft()
            for y in sorted(g.get(x, ())):
                if y in members and y not in dist:
                    dist[y] = dist[x] + 1
                    q.append(y)
        for s, d in dist.items():
            if s not in best or d < best[s][0]:
                best[s] = (d, lane)
    return {s: v[1] for s, v in best.items()}


def span_of(slugs, people, listable):
    """The first and last year printed on the pages of the listable people of a household: births, and deaths."""
    ys = []
    for s in slugs:
        if s not in listable:
            continue
        for k in ("born", "died"):
            y = year_of(people[s].get(k))
            if y:
                ys.append(y)
    return [min(ys), max(ys)] if ys else None


def places_of(slugs, people, listable):
    """Where the listable people of a household are, with the years their pages print: [[place, first, last], ...]."""
    by = collections.defaultdict(list)
    for s in slugs:
        if s not in listable:
            continue
        pl = (people[s].get("place") or "").strip()
        if not pl:
            continue
        for k in ("born", "died"):
            y = year_of(people[s].get(k))
            if y:
                by[pl].append(y)
        by.setdefault(pl, [])
    out = [[pl, min(ys) if ys else None, max(ys) if ys else None] for pl, ys in by.items()]
    return sorted(out, key=lambda t: (t[1] is None, t[1] or 0, t[0]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail when data/people-lines.tsv is out of date, and change nothing")
    ap.add_argument("--living-path", action="store_true", help="print where --living-slugs writes, and stop")
    ap.add_argument("--living-slugs", action="store_true", help="write the slugs a lane or pen must never list, outside the repository, and stop")
    a = ap.parse_args()
    if a.living_path:
        print(living_path())
        return 0
    if a.living_slugs:
        slugs = living_slugs()
        if not slugs:
            print("  FAIL  lines-living  no living slug found; a list of none would make the gate's P3 a verdict on nothing")
            return 2
        fp = living_path()
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(json.dumps(slugs, indent=0) + "\n", encoding="utf-8")
        try:
            os.chmod(fp, 0o600)
        except OSError:
            pass
        print("  lines living list: %d slug(s), kept outside the repository" % len(slugs))
        return 0

    people = load_people()
    cutoff = L.current_cutoff()
    unpub = unpublished_dead()
    never = set(living_slugs())
    listable = {s for s in people if eligible(s, people, cutoff, unpub) and s not in never}
    g = kin_graph(people)
    comp, groups = groups_of(people, g)
    problems = []

    # ------------------------------------------------------------------ lanes: their rows, nodes and seeds
    lanes_raw = tsv(LANES_TSV)
    lane_keys = [r["key"] for r in lanes_raw]
    rank = {k: i for i, k in enumerate(lane_keys)}
    hand = [r for r in tsv(PEOPLE_TSV) if r["how"] in ("anchor", "spouse")]
    for r in hand:
        if r["lane"] not in lane_keys:
            problems.append("people-lines.tsv: lane %r is not a lane" % r["lane"])
        if r["slug"] not in people:
            problems.append("people-lines.tsv: %s is not a person page" % r["slug"])
        if not r["basis"].strip():
            problems.append("people-lines.tsv: %s has no basis" % r["slug"])
    seen_hand = collections.Counter(r["slug"] for r in hand)
    for s, n in seen_hand.items():
        if n > 1:
            problems.append("people-lines.tsv: %s is written by hand %d times; a person stands on one line" % (s, n))
    if problems:
        print("\n".join("  FAIL  " + p for p in problems))
        return 1

    seeds = collections.defaultdict(set)
    for r in hand:
        seeds[r["lane"]].add(r["slug"])
    lanes, node_persons = [], collections.defaultdict(list)
    for r in lanes_raw:
        status = r["status"].strip()
        if status not in STATUSES:
            problems.append("lerena-lines.tsv: %s has status %r, which is not a tier" % (r["key"], status))
        nodes = [n for n in r["nodes"].split(";;") if n]
        pers = (r.get("node_person", "") or "").split(";;") if r.get("node_person", "") else [""] * len(nodes)
        evs = (r.get("node_evidence", "") or "").split(";;") if r.get("node_evidence", "") else [""] * len(nodes)
        if len(pers) != len(nodes) or len(evs) != len(nodes):
            problems.append("lerena-lines.tsv: %s has %d nodes but %d node_person and %d node_evidence entries" % (r["key"], len(nodes), len(pers), len(evs)))
            continue
        out_nodes = []
        for n, p, e in zip(nodes, pers, evs):
            parts = n.split("|")
            o = {"place": parts[0], "year": parts[1], "why": "|".join(parts[2:])}
            if p:
                if p not in people:
                    problems.append("lerena-lines.tsv: %s node %s names %s, which is not a person page" % (r["key"], parts[0], p))
                elif not safe(p, people, unpub) or p in never:
                    problems.append("lerena-lines.tsv: %s on %s is living or held out and may not be linked" % (p, r["key"]))
                o["person"] = p
                if p not in node_persons[r["key"]]:
                    node_persons[r["key"]].append(p)
                seeds[r["key"]].add(p)
            if e:
                if e not in EVIDENCE:
                    problems.append("lerena-lines.tsv: %s has the evidence word %r" % (r["key"], e))
                o["evidence"] = e
            out_nodes.append(o)
        lane = {"key": r["key"], "colour": r["colour"], "label": r["label"], "href": r["href"], "read": r["read"], "status": status}
        if r.get("statusnote", "").strip():
            lane["statusNote"] = r["statusnote"].strip()
        sp = (r.get("span", "") or "").strip()
        if sp:
            a1, _, b1 = sp.partition("-")
            lane["span"] = [int(a1), int(b1) if b1 else None]
        lane["nodes"] = out_nodes
        # THE DIRECT-LINE TINT (27 October 2026; kit/docs/family-ribbon.md): a lane is "ours" when every person on its nodes is one
        # of the story ribbon's generations (site/src/data/direct-line.json, made from the story by the kit's directline.py).
        # Derived, never typed. Sancho's lane is not ours although he is: it runs on through children and grandchildren whom no
        # paper puts on our line (the story's break), so only his node is tinted, never the lane.
        lane_people = [n["person"] for n in out_nodes if n.get("person")]
        if lane_people and all(s in OURS for s in lane_people):
            lane["ours"] = True
        lane["ends"] = [[e] for e in r["ends"].split(";;") if e]      # the kit reads an end as [name, href, why]; no href = the lane's own page
        lane["_note"] = r.get("note", "")
        lanes.append(lane)

    # ------------------------------------------------------------------ joins (data/lerena-lines-joins.tsv)
    joins_raw = tsv(JOINS_TSV)
    documented_pairs = set()
    for j in joins_raw:
        if j["status"] not in JOIN_STATUSES:
            problems.append("lerena-lines-joins.tsv: status %r is not one of %s" % (j["status"], ", ".join(JOIN_STATUSES)))
        if j["status"] == "documented" and j["a"].startswith("lane:") and j["b"].startswith("lane:"):
            documented_pairs.add(frozenset((j["a"][5:], j["b"][5:])))

    # ------------------------------------------------------------------ every person onto one lane (rules 2 and 3)
    lane_of = {}
    basis_of = {}
    group_lanes = collections.defaultdict(lambda: collections.defaultdict(set))
    for lane, ss in seeds.items():
        for s in ss:
            group_lanes[comp[s]][lane].add(s)
    for gi, by_lane in group_lanes.items():
        members = set(groups[gi])
        if len(by_lane) > 1:
            ks = sorted(by_lane, key=lambda k: rank[k])
            for i in range(len(ks)):
                for k2 in ks[i + 1:]:
                    if frozenset((ks[i], k2)) not in documented_pairs:
                        problems.append("one family group holds the seeds of %s and %s (%s and %s): an undeclared join. Record it in "
                                        "data/lerena-lines-joins.tsv as documented, or correct the register."
                                        % (ks[i], k2, sorted(by_lane[ks[i]])[0], sorted(by_lane[k2])[0]))
            assign = nearest(by_lane, g, members, rank)
        else:
            (only,) = by_lane
            assign = {s: only for s in members}
        for s, lane in assign.items():
            lane_of[s] = lane
            seed = sorted(by_lane[lane])[0]
            basis_of[s] = "in one family group with %s by the register's own links" % seed
    if problems:
        print("\n".join("  FAIL  " + p for p in problems))
        return 1

    # ------------------------------------------------------------------ the households and pens (rules 4 and 5)
    rows = tsv(PENS_TSV)
    row_of_group = {}
    row_on_lane = {}
    for i, r in enumerate(rows):
        if r["kind"] not in ("unplaced", "namesake"):
            problems.append("lerena-lines-unplaced.tsv: %r has kind %r" % (r["who"], r["kind"]))
        for s in [x.strip() for x in (r.get("people") or "").split(";") if x.strip()]:
            if s not in people:
                problems.append("lerena-lines-unplaced.tsv: %r names %s, which is not a person page" % (r["who"], s))
                continue
            if s in lane_of:
                row_on_lane.setdefault(i, set()).add(lane_of[s])
                continue
            gi = comp[s]
            if gi in row_of_group and row_of_group[gi] != i:
                problems.append("lerena-lines-unplaced.tsv: %r and %r both claim the family group of %s" % (rows[row_of_group[gi]]["who"], r["who"], s))
            row_of_group[gi] = i
    if problems:
        print("\n".join("  FAIL  " + p for p in problems))
        return 1

    pen_of = {}          # slug -> pen key
    hh = []              # households: dicts
    row_hh = {}
    for i, r in enumerate(rows):
        h = {"row": i, "who": r["who"], "where": r["where"], "why": r["why"], "href": r.get("href", ""),
             "pen": "households" if r["kind"] == "unplaced" else "namesake", "people": [],
             "status": r.get("status", "").strip(), "statusNote": r.get("statusnote", "").strip(),
             "onLane": sorted(row_on_lane.get(i, set()), key=lambda k: rank[k])}
        row_hh[i] = h
        hh.append(h)
    for gi, members in enumerate(groups):
        if any(s in lane_of for s in members):
            continue
        if gi in row_of_group:
            h = row_hh[row_of_group[gi]]
            h["people"].extend(members)
            for s in members:
                pen_of[s] = h["pen"]
            continue
        if len(members) >= 2 and any(carries_name(people[s]["name"]) for s in members):
            h = {"row": None, "who": None, "where": None, "why": None, "href": None, "pen": "households", "people": list(members),
                 "status": "", "statusNote": "", "onLane": []}
            hh.append(h)
            for s in members:
                pen_of[s] = "households"
            continue
        for s in members:
            pen_of[s] = "single" if carries_name(people[s]["name"]) else "others"

    # a household the data writes up by its own label; one the tool found is named from its eldest listable bearer of the name
    for h in hh:
        h["people"] = sorted(set(h["people"]))
        lst = [s for s in h["people"] if s in listable]
        h["listed"] = lst
        h["span"] = span_of(h["people"], people, listable)
        h["places"] = places_of(h["people"], people, listable)
        if h["row"] is not None:
            h["label"] = h["who"] + (" — " + h["where"] if h["where"] else "")
            continue
        bearers = [s for s in lst if carries_name(people[s]["name"])]
        pool = bearers or lst
        if pool:
            head = sorted(pool, key=lambda s: (year_of(people[s].get("born")) or 9999, -len(g.get(s, ())), s))[0]
            place = h["places"][0][0] if h["places"] else ""
            h["label"] = "The household of %s" % clean_name(people[head]["name"]) + (" — " + place if place else "")
            h["href"] = "/people/%s/" % head
            h["head"] = head
        else:
            # nobody in it may be named (no page prints a year for any of them): the household is drawn by its size and its town
            towns = collections.Counter((people[s].get("place") or "").strip() for s in h["people"] if (people[s].get("place") or "").strip())
            town = towns.most_common(1)[0][0] if towns else "a place the register does not give"
            h["label"] = "A household of %d at %s" % (len(h["people"]), town)
            h["href"] = "/register/"
        names = [clean_name(people[s]["name"]) for s in lst if carries_name(people[s]["name"])][:5]
        h["why"] = ("%d people the register joins to one another by its own links and to no line by any. %s"
                    % (len(h["people"]), ("Of the name: " + ", ".join(names) + ("…" if len(bearers) > 5 else "") + ".") if names else "")).strip()

    # a label is how a bridge names a household, so two must not share one: two the tool found in one town are numbered
    seen_lab = collections.Counter()
    for h in hh:
        if h["row"] is None and h["label"].startswith("A household of "):
            seen_lab[h["label"]] += 1
            if seen_lab[h["label"]] > 1:
                h["label"] += " (%d)" % seen_lab[h["label"]]
    labs = collections.Counter(h["label"] for h in hh)
    for l, n in labs.items():
        if n > 1:
            problems.append("two households are both labelled %r" % l)

    # ------------------------------------------------------------------ kin rows of data/people-lines.tsv (derived; listable only)
    hand_slugs = {r["slug"] for r in hand}
    new_rows = sorted(
        [(lane_of[s], s, "kin", basis_of[s]) for s in lane_of
         if s in listable and s not in hand_slugs and s not in node_persons[lane_of[s]]],
        key=lambda t: (rank[t[0]], t[1]))
    current = [(r["lane"], r["slug"], r["how"], r["basis"]) for r in tsv(PEOPLE_TSV) if r["how"] not in ("anchor", "spouse")]
    if not a.check:
        out_lines = [PEOPLE_HEADER]
        for r in sorted(hand, key=lambda r: (rank[r["lane"]], r["how"] != "anchor", r["slug"])):
            out_lines.append("\t".join([r["lane"], r["slug"], r["how"], r["basis"]]))
        for t in new_rows:
            out_lines.append("\t".join(t))
        PEOPLE_TSV.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        if sorted(current) != sorted(new_rows):
            print("  lines  data/people-lines.tsv: %d kin row(s) now, %d before (the register's links moved)" % (len(new_rows), len(current)))
    elif sorted(current) != sorted(new_rows):
        gone = sorted(set(current) - set(new_rows))
        came = sorted(set(new_rows) - set(current))
        print("  FAIL  lines  data/people-lines.tsv is out of date: %d derived row(s) the register no longer supports, %d it now does." % (len(gone), len(came)))
        for t in (gone + came)[:8]:
            print("          %s %s" % (t[0], t[1]))
        print("        run:  python3 tools/build-lines.py")
        return 1

    # one person, one place: every slug in people.json is on exactly one lane or in exactly one pen
    placed = collections.Counter()
    for s in people:
        placed[s] += (s in lane_of) + (s in pen_of)
    for s, n in placed.items():
        if n != 1:
            problems.append("%s is placed %d times: every person stands in exactly one place" % (s, n))
    if problems:
        print("\n".join("  FAIL  " + p for p in problems))
        return 1

    # ------------------------------------------------------------------ the drawing
    for lane in lanes:
        k = lane["key"]
        have = set(node_persons[k])
        order = [r["slug"] for r in sorted(hand, key=lambda r: (r["how"] != "anchor", r["slug"])) if r["lane"] == k]
        order += sorted(s for l, s, *_ in new_rows if l == k)
        mem = []
        for s in order:
            if s not in have and s not in mem and s in listable:
                mem.append(s)
        if mem:
            lane["members"] = mem

    pens = []
    for key in PEN_ORDER:
        items = []
        members = []
        for h in hh:
            if h["pen"] != key:
                continue
            items.append([h["label"], h["href"] or "", h["why"] or ""])
            members.extend(s for s in h["listed"])
        if key in ("single", "others"):
            members = sorted(s for s, p in pen_of.items() if p == key and s in listable)
        if not items and not members:
            continue
        pen = {"id": PEN_ID[key], "kind": PEN_KIND[key], "head": PEN_HEAD[key], "note": PEN_NOTE[key]}
        if items:
            pen["items"] = items
        if members:
            pen["members"] = sorted(dict.fromkeys(members))
        pens.append(pen)

    label_of_row = {h["who"]: h["label"] for h in hh if h["row"] is not None}

    def end(ref):
        """a join's end -> (label, href, kind, bridge-name)"""
        kind, _, v = ref.partition(":")
        if kind == "lane":
            ln = next((l for l in lanes if l["key"] == v), None)
            if not ln:
                problems.append("lerena-lines-joins.tsv: %r is not a lane" % ref)
                return None
            return {"label": ln["label"], "href": ln["href"], "kind": "lane", "key": v, "bridge": v}
        if kind == "row":
            if v not in label_of_row:
                problems.append("lerena-lines-joins.tsv: %r names no household row" % ref)
                return None
            h = next(h for h in hh if h["row"] is not None and h["who"] == v)
            return {"label": h["label"], "href": h["href"], "kind": "household", "bridge": h["label"]}
        if kind == "person":
            slug, _, lab = v.partition("|")
            if slug not in people:
                problems.append("lerena-lines-joins.tsv: %r is not a person page" % ref)
                return None
            if slug in never or not safe(slug, people, unpub):
                problems.append("lerena-lines-joins.tsv: %s is living or held out and may not be named" % slug)
                return None
            return {"label": lab or clean_name(people[slug]["name"]), "href": "/people/%s/" % slug, "kind": "person",
                    "line": lane_of.get(slug), "bridge": None}
        if kind == "text":
            return {"label": v, "href": "", "kind": "text", "bridge": None}
        problems.append("lerena-lines-joins.tsv: %r is not lane:, row:, person: or text:" % ref)
        return None

    joins, bridges = [], []
    for j in joins_raw:
        x, y = end(j["a"]), end(j["b"])
        if not x or not y:
            continue
        joins.append({"a": x, "b": y, "status": j["status"], "says": j["says"], "href": j["href"], "label": j.get("label", "")})
        if j["status"] == "candidate":
            if not (x["bridge"] and y["bridge"]):
                problems.append("lerena-lines-joins.tsv: the candidate %r - %r must join a lane to a lane or to a household row, to be drawn" % (j["a"], j["b"]))
                continue
            if x["kind"] != "lane":
                x, y = y, x
            bridges.append({"from": x["bridge"], "to": y["bridge"], "conf": "inf", "label": j.get("label") or j["says"][:90], "href": j["href"]})
    if problems:
        print("\n".join("  FAIL  " + p for p in problems))
        return 1

    for lane in lanes:
        lane.pop("_note", None)
    drawing = {"title": TITLE, "lanes": lanes, "pens": pens}
    if bridges:
        drawing["bridges"] = bridges
    OUT.write_text(json.dumps(drawing, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    # ------------------------------------------------------------------ the ledger: the tables on /lines/, all counts derived
    def tally(slugs):
        slugs = list(slugs)
        return {"people": len(slugs), "listed": sum(1 for s in slugs if s in listable)}

    by_lane = collections.defaultdict(list)
    for s, l in lane_of.items():
        by_lane[l].append(s)
    by_pen = collections.defaultdict(list)
    for s, p in pen_of.items():
        by_pen[p].append(s)
    raw_by_key = {r["key"]: r for r in lanes_raw}
    ledger = {
        "_note": "Made by tools/build-lines.py from people.json and the lines TSVs; never typed. Counts only for anybody who may not be listed.",
        "rule": RULE,
        "total": len(people),
        "listed": len(listable),
        "lanes": [dict({"key": l["key"], "label": l["label"], "href": l["href"], "read": l["read"], "status": l["status"],
                        "statusNote": l.get("statusNote", ""), "span": l.get("span"), "note": raw_by_key[l["key"]].get("note", ""),
                        "places": [[n["place"], n["year"]] for n in l["nodes"]],
                        "ends": [e[0] for e in l["ends"]], "people": len(by_lane[l["key"]]),
                        # named = what the drawing names on the lane (its node persons and its members), as the kit counts it
                        "listed": len(set(node_persons[l["key"]]) | set(l.get("members", [])))}) for l in lanes],
        "pens": [dict({"id": PEN_ID[k], "key": k, "kind": PEN_KIND[k], "head": PEN_HEAD[k],
                       "households": sum(1 for h in hh if h["pen"] == k)}, **tally(by_pen[k])) for k in PEN_ORDER],
        "households": [{"label": h["label"], "pen": PEN_ID[h["pen"]], "href": h["href"] or "", "why": h["why"] or "",
                        "status": h["status"] or ("origin-unknown" if h["pen"] == "households" else "different-stock"),
                        "statusNote": h["statusNote"], "span": h["span"], "places": h["places"],
                        "onLane": h["onLane"], "written": h["row"] is not None, **tally(h["people"])} for h in hh],
        "joins": joins,
    }
    LEDGER.write_text(json.dumps(ledger, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    n_lane = sum(len(v) for v in by_lane.values())
    print("build-lines: %d people: %d on %d lanes (%s), %d in %d pens (%s); %d households (%d written up); %d listed by name, %d counted only; "
          "%d joins (%s), %d drawn as bridges"
          % (len(people), n_lane, len(lanes), ", ".join("%s %d" % (l["key"], len(by_lane[l["key"]])) for l in lanes),
             sum(len(v) for v in by_pen.values()), len(pens), ", ".join("%s %d" % (k, len(by_pen[k])) for k in PEN_ORDER),
             len(hh), sum(1 for h in hh if h["row"] is not None), len(listable), len(people) - len(listable), len(joins),
             ", ".join("%s %d" % (s, sum(1 for j in joins if j["status"] == s)) for s in JOIN_STATUSES), len(bridges)))
    for h in hh:
        if h["onLane"]:
            print("  note  the household %r is written up as unplaced, and its people stand on %s: drawn as a household with none of its people"
                  % (h["who"], ", ".join(h["onLane"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
