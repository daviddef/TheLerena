#!/usr/bin/env python3
"""Make site/src/data/lerena-lines.json, the drawing on /name/, from the three TSVs that hold it. (25 October 2026)

    python3 tools/build-lines.py                 re-derive the descendant rows of data/people-lines.tsv from the register, then build the JSON
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
  data/lerena-lines-unplaced.tsv  the two pens: kind unplaced -> not-yet-placed, kind namesake -> different-stock; `href` is the
                                  page that works that household.
  data/people-lines.tsv           the person-to-lane file. Three kinds of row: `anchor` and `spouse` are written by hand, each
                                  with the archive's own statement in `basis` (a node of the lane, a register name that says
                                  "son of Sancho", an act); `descendant` rows are DERIVED by this tool from the anchors through
                                  the parent and child links the register holds (people.json: father, mother, children; a link
                                  that rests only on a family tree is not followed).

WHO MAY BE LISTED. A lane lists people, so it lists no living person and no person the archive holds out. A person is listed
only when the register publishes a birth year before the living line (livingcheck.current_cutoff: 1946 in 2026) or publishes a
death; an undated stub is left off, and so is any person the data records as dead but no page prints (data/living-year-allow.json
unpublished_deaths). A person stands on ONE lane. These are the rules the kit gate holds the built page to (P3, E1); this tool
refuses earlier, so the fault is found where the data is.

THE COUNT UNDER A LANE IS NOT "EVERYONE DESCENDED". It is the people this archive has placed on the line by these links, no more.
The page says so under the figure.
"""
import argparse
import collections
import json
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import livingcheck as L  # noqa: E402

DATA = ROOT / "data"
SITE = ROOT / "site" / "src" / "data"
LANES_TSV = DATA / "lerena-lines.tsv"
PENS_TSV = DATA / "lerena-lines-unplaced.tsv"
PEOPLE_TSV = DATA / "people-lines.tsv"
OUT = SITE / "lerena-lines.json"

TITLE = "The documented lines of the name Lerena, side by side, with the households not yet placed on any of them"
STATUSES = ("documented", "inferred", "origin-unknown", "family-lore")
EVIDENCE = ("read", "indexed", "scanned", "tree", "inferred", "disputed", "none")

PEN_HEAD = {
    "unplaced": "Real households of the name — on none of these lines",
    "namesake": "A different stock of the same name — kept apart on purpose",
}
PEN_NOTE = {
    "unplaced": ("Real, documented households of the name that this archive has read and not joined to any line above. "
                 "They sit below the rule so that the picture cannot imply that everything has been placed. "
                 "What would move one onto a line is a document that names its parents, or an act that ties it to a household already drawn."),
    "namesake": ("Names that look like this one and are kept apart on purpose: found while searching, recorded so that nobody has to "
                 "discover them twice. No connection is claimed between any of them and any line above."),
}
PEN_ID = {"unplaced": "not-yet-placed", "namesake": "different-stock"}

PEOPLE_HEADER = """# *** WHO STANDS ON WHICH LINE (the person-to-lane file for the drawing on /name/). 25 October 2026. ***
#
# Written for the kit's lines contract (kit/docs/lines.md): a lane may list the people on it, and the kit gate holds the built page to
# three rules - nobody living is listed (P3), nobody stands on two lines (E1), every link lands (P1).
#
# lane      the key of a lane in data/lerena-lines.tsv
# slug      the person page, /people/<slug>/
# how       anchor      a person the archive itself puts on the line, with the statement in `basis` (written by hand)
#           spouse      the wife of an anchor, named as such in the register (written by hand)
#           descendant  DERIVED by tools/build-lines.py from the anchors through the register's parent and child links (never
#                       by hand: the build re-derives them whenever the register moves)
# basis     the archive's own words for why
#
# A person is listed only if the register publishes a birth year before the living line or a death. An undated stub, a living
# person and a person the data records dead but no page prints are left off, whatever their links. The number a reader sees under
# a lane is the people placed here by these links; it is not everyone who descended.
lane\tslug\thow\tbasis"""


def tsv(path):
    lines = [l.rstrip("\n") for l in path.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    hdr = lines[0].split("\t")
    return [dict(zip(hdr, (l.split("\t") + [""] * len(hdr))[:len(hdr)])) for l in lines[1:]]


def year_of(s):
    import re
    m = re.search(r"(?<!\d)(\d{4})(?!\d)", str(s or ""))
    return int(m.group(1)) if m else None


def load_people():
    rows = json.loads((SITE / "people.json").read_text(encoding="utf-8"))
    return {r["slug"]: r for r in rows}


def unpublished_dead():
    p = DATA / "living-year-allow.json"
    if not p.exists():
        return set()
    return {e["slug"] for e in json.loads(p.read_text(encoding="utf-8")).get("unpublished_deaths", [])}


def children_graph(people):
    kids = collections.defaultdict(set)
    for r in people.values():
        for k in ("father", "mother"):
            p = r.get(k)
            if p and p.get("slug") in people and p.get("via") != "tree":
                kids[p["slug"]].add(r["slug"])
        for c in r.get("children") or []:
            if c.get("slug") in people and c.get("via") != "tree":
                kids[r["slug"]].add(c["slug"])
    return kids


def eligible(slug, people, cutoff, unpub):
    """May this person stand in a list of people on a public page?"""
    r = people.get(slug)
    if not r or r.get("living") or r.get("noindex") or slug in unpub:
        return False
    by = year_of(r.get("born"))
    return (by is not None and by < cutoff) or bool(str(r.get("died") or "").strip())


def safe(slug, people, unpub):
    """The floor for a person a node or a hand-written row names: a page that exists, not living, not held out, not an unpublished death."""
    r = people.get(slug)
    return bool(r) and not r.get("living") and not r.get("noindex") and slug not in unpub


def derive(people_rows, people, kids, cutoff, unpub):
    """lane -> {slug: basis} for the descendants of the anchors, and the list of people left off for want of a published date."""
    out = collections.defaultdict(dict)
    left_off = collections.defaultdict(set)
    for r in people_rows:
        if r["how"] != "anchor":
            continue
        seen, stack = set(), [r["slug"]]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(kids.get(x, ()))
        for s in seen:
            if s == r["slug"]:
                continue
            if eligible(s, people, cutoff, unpub):
                out[r["lane"]].setdefault(s, "descendant of %s by the register's parent and child links" % r["slug"])
            else:
                left_off[r["lane"]].add(s)
    return out, left_off


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
    kids = children_graph(people)

    lanes_raw = tsv(LANES_TSV)
    lane_keys = [r["key"] for r in lanes_raw]
    hand = [r for r in tsv(PEOPLE_TSV) if r["how"] in ("anchor", "spouse")]
    problems = []
    for r in hand:
        if r["lane"] not in lane_keys:
            problems.append("people-lines.tsv: lane %r is not a lane" % r["lane"])
        if r["slug"] not in people:
            problems.append("people-lines.tsv: %s is not a person page" % r["slug"])
        if not r["basis"].strip():
            problems.append("people-lines.tsv: %s has no basis" % r["slug"])
    if problems:
        print("\n".join("  FAIL  " + p for p in problems))
        return 1

    derived, left_off = derive(hand, people, kids, cutoff, unpub)
    rank = {k: i for i, k in enumerate(lane_keys)}
    new_rows = sorted(
        [(l, s, "descendant", b) for l, d in derived.items() for s, b in d.items()
         if s not in {h["slug"] for h in hand if h["lane"] == l}],
        key=lambda t: (rank[t[0]], t[1]))

    current = [(r["lane"], r["slug"], r["how"], r["basis"]) for r in tsv(PEOPLE_TSV) if r["how"] == "descendant"]
    if not a.check:
        lines = [PEOPLE_HEADER]
        for r in sorted(hand, key=lambda r: (rank[r["lane"]], r["how"] != "anchor", r["slug"])):
            lines.append("\t".join([r["lane"], r["slug"], r["how"], r["basis"]]))
        for t in new_rows:
            lines.append("\t".join(t))
        PEOPLE_TSV.write_text("\n".join(lines) + "\n", encoding="utf-8")
        if sorted(current) != sorted(new_rows):
            print("  lines  data/people-lines.tsv: %d descendant row(s) now, %d before (the register's parent and child links moved)" % (len(new_rows), len(current)))
        current = new_rows
    elif sorted(current) != sorted(new_rows):
        gone = sorted(set(current) - set(new_rows))
        came = sorted(set(new_rows) - set(current))
        print("  FAIL  lines  data/people-lines.tsv is out of date: %d descendant row(s) the register no longer supports, %d it now does." % (len(gone), len(came)))
        for t in (gone + came)[:8]:
            print("          %s %s" % (t[0], t[1]))
        print("        run:  python3 tools/build-lines.py")
        return 1

    # one person, one lane (the kit's E1): across anchors, spouses, descendants and node persons
    where = collections.defaultdict(set)
    for r in hand:
        where[r["slug"]].add(r["lane"])
    for l, s, *_ in new_rows:
        where[s].add(l)

    lanes = []
    node_persons = collections.defaultdict(list)
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
                elif not safe(p, people, unpub):
                    problems.append("lerena-lines.tsv: %s on %s is living or held out and may not be linked" % (p, r["key"]))
                o["person"] = p
                where[p].add(r["key"])
                node_persons[r["key"]].append(p)
            if e:
                if e not in EVIDENCE:
                    problems.append("lerena-lines.tsv: %s has the evidence word %r" % (r["key"], e))
                o["evidence"] = e
            out_nodes.append(o)
        lane = {"key": r["key"], "colour": r["colour"], "label": r["label"], "href": r["href"], "read": r["read"],
                "status": status}
        if r.get("statusnote", "").strip():
            lane["statusNote"] = r["statusnote"].strip()
        sp = (r.get("span", "") or "").strip()
        if sp:
            a1, _, b1 = sp.partition("-")
            lane["span"] = [int(a1), int(b1) if b1 else None]
        lane["nodes"] = out_nodes
        lane["ends"] = [[e] for e in r["ends"].split(";;") if e]      # the kit reads an end as [name, href, why]; no href = the lane's own page
        lanes.append(lane)

    for s, ls in where.items():
        if len(ls) > 1:
            problems.append("%s stands on %d lines (%s): a person stands on one" % (s, len(ls), ", ".join(sorted(ls))))
    if problems:
        print("\n".join("  FAIL  " + p for p in problems))
        return 1

    # members: the anchors, spouses and descendants of a lane that are not already a node of it, once each, in a fixed order
    for lane in lanes:
        k = lane["key"]
        have = set(node_persons[k])
        order = [r["slug"] for r in sorted(hand, key=lambda r: (r["how"] != "anchor", r["slug"])) if r["lane"] == k]
        order += sorted(s for l, s, *_ in new_rows if l == k)
        mem = []
        for s in order:
            if s not in have and s not in mem:
                mem.append(s)
        # a hand-written row is the archive's own word; the rule above still keeps a living person off the page
        mem = [s for s in mem if safe(s, people, unpub)]
        if mem:
            lane["members"] = mem

    pens = []
    prows = tsv(PENS_TSV)
    for kind in ("unplaced", "namesake"):
        items = []
        for r in prows:
            if r["kind"] != kind:
                continue
            label = r["who"] + (" — " + r["where"] if r["where"] else "")
            items.append([label, r.get("href", ""), r["why"]])
        if items:
            pens.append({"id": PEN_ID[kind], "kind": PEN_ID[kind], "head": PEN_HEAD[kind], "note": PEN_NOTE[kind], "items": items})

    drawing = {"title": TITLE, "lanes": lanes, "pens": pens}
    OUT.write_text(json.dumps(drawing, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    n_mem = sum(len(l.get("members", [])) for l in lanes)
    n_node = sum(len(v) for v in node_persons.values())
    print("build-lines: %d lanes, %d pens (%s), %d node person(s), %d other member(s); left off for want of a published date or a death: %s"
          % (len(lanes), len(pens), ", ".join("%d items" % len(p["items"]) for p in pens), n_node, n_mem,
             ", ".join("%s %d" % (k, len(v)) for k, v in sorted(left_off.items(), key=lambda kv: rank[kv[0]])) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
