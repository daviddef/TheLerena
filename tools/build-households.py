#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make site/src/data/households.json, the data behind /households/ (the kit's Households component).  (23 November 2026)

    python3 ../tools/build-households.py            # from site/: write the file
    python3 ../tools/build-households.py --check    # fail if the committed file is not what people.json gives (nothing written)

A HOUSEHOLD HERE IS A COUPLE AND THE CHILDREN THE REGISTER RECORDS UNDER THEM, the shape a register writes and not the shape of a pedigree. It is
made from site/src/data/people.json only (committed), from the register's own links: a child's `father` and `mother`, a parent's `children` and
`spouses`. Nothing is typed and nothing is added from a family tree except where a link says `via: tree`, and then the household SAYS so.

WHAT THE LINKS MAKE.
  * Every person is looked at once as a child: the set of parents is the father and mother on the child's own row plus anybody whose `children`
    lists the child. A set of one or two parents makes (or joins) a household: the pair, or the lone parent.
  * Every spouse link between two people makes a household too, if the pair has no child recorded: a couple with nothing recorded under them is a
    finding, not a blank (the component says «No children recorded under this couple»).
  * A child whose rows name MORE than two parents is placed in no household and is counted (the register holds one such row: two sets of parents
    for one woman, which is a question and not a household).
  * A household is KNOWN FROM: «a marriage in the register» (a spouse link, `via: register`), «parents named together» (the pair is named as the
    parents of the same child and no marriage is recorded between them), «a parent on their own» (one parent named) or «the family tree» (the
    spouse link, or every parent link, rests on a family tree and not on a record). A child carries its own «via» only where it is not the
    household's.

THE LIVING RULE, AND WHO IS NAMED. A person is named on this page only if their page is one this archive publishes and names (build-lines.py `safe`: not
living, not held out (`noindex`), not an unpublished death: the rule /people/ prints its names by) AND is not on the independent living list every
living gate here uses (livingcheck.py, through build-lines.living_slugs), which holds the undated child of a living parent and the person born inside
the living line with no death. Stricter than /people/, never looser. (The lines page lists a person by name only with a published year as well; this
page is not a list of the people on the lines but of the couples the register records, and names them as /people/ does.) A household with a parent who may not be named is NOT SHOWN:
it is counted, nothing more. A child who may not be named is not named; the household then says, without saying who or how many, that not every
child recorded under the couple is named here. Nobody living, held out or unlisted appears by name, year, place or number beside a household.
The counts the page prints are of the households and children shown, and of the households kept back, each as one number.

DATES are the person's own row: a year of birth (a trailing c on the register's year is «c.»), a year of death, as «1905–1973», «c. 1868–1931»,
«b. 1868» or «d. 1931». The component's dagger (a child who did not live five years) is switched OFF for a child whose birth is c.: it reads two
printed years and would otherwise turn an estimate into a death in infancy.
"""
import importlib.util
import io
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = ROOT / "site"
DATA = SITE / "src" / "data"
OUT = DATA / "households.json"

sys.path.insert(0, str(HERE))
_spec = importlib.util.spec_from_file_location("build_lines", HERE / "build-lines.py")
BL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(BL)

V_MARRIED = "a marriage in the register"
V_TOGETHER = "parents named together"
V_ALONE = "a parent on their own"
V_TREE = "the family tree"
V_REGISTER = "the register"


def clean_name(n):
    """The register name without its bracketed gloss and without the register's own marks: «Cipriano LERENA (of Trinidad)» -> «Cipriano LERENA»."""
    n = re.sub(r"\s*\([^)]*\)", "", str(n or "")).replace('"', "")
    n = re.sub(r"\s*=.*$", "", n)
    n = n.replace("***", "")
    return re.sub(r"\s+", " ", n).strip()


def year_of(s):
    m = re.search(r"(?<!\d)(\d{4})(?!\d)", str(s or ""))
    return int(m.group(1)) if m else None


def plain(s):
    return re.sub(r"\s+", " ", str(s or "").replace("***", "")).strip()


def dates_of(r):
    b, d = str(r.get("born") or ""), str(r.get("died") or "")
    by, dy = year_of(b), year_of(d)
    circa = bool(by) and bool(re.search(r"[c~]|abt|about|circa", b, re.I))
    bs = ("c. " if circa else "") + str(by) if by else ""
    if by and dy:
        return "%s–%d" % (bs, dy), circa
    if by:
        return "b. " + bs, circa
    if dy:
        return "d. %d" % dy, circa
    return "", circa


def build():
    people = BL.load_people()
    unpub = BL.unpublished_dead()
    never = set(BL.living_slugs())
    order = {s: i for i, s in enumerate(people)}
    line = {p["slug"] for p in json.loads((DATA / "direct-line.json").read_text(encoding="utf-8")).get("people", [])}

    def nameable(s):
        return BL.safe(s, people, unpub) and s not in never and not people[s].get("aliasOf")

    # edges: (parent, child) -> via (the weakest wins: a tree link anywhere makes the link a tree link); spouse edges -> (via, note)
    pc, sp = {}, {}

    def put_pc(p, c, via, note=""):
        if p in people and c in people and p != c and not people[p].get("aliasOf") and not people[c].get("aliasOf"):
            old = pc.get((p, c))
            if old is None:
                pc[(p, c)] = [via, note]
            else:
                if via == "tree":
                    old[0] = "tree"
                if note and not old[1]:
                    old[1] = note

    for s, r in people.items():
        for k in ("father", "mother"):
            e = r.get(k)
            if isinstance(e, dict) and e.get("slug"):
                put_pc(e["slug"], s, e.get("via") or "register", e.get("note") or "")
        for e in r.get("children") or []:
            if e.get("slug"):
                put_pc(s, e["slug"], e.get("via") or "register", e.get("note") or "")
        for e in r.get("spouses") or []:
            o = e.get("slug")
            if o and o in people and o != s and not people[o].get("aliasOf") and not r.get("aliasOf"):
                key = tuple(sorted((s, o), key=order.get))
                old = sp.get(key)
                via = e.get("via") or "register"
                if old is None:
                    sp[key] = [via, e.get("note") or ""]
                else:
                    if via == "tree":
                        old[0] = "tree"
                    if e.get("note") and not old[1]:
                        old[1] = e["note"]

    parents_of = {}
    for (p, c) in pc:
        parents_of.setdefault(c, set()).add(p)
    over = [c for c, ps in parents_of.items() if len(ps) > 2]
    units = {}                      # frozenset(parents) -> [children]
    for c, ps in parents_of.items():
        if len(ps) > 2:
            continue
        units.setdefault(frozenset(ps), []).append(c)
    for key in sp:
        units.setdefault(frozenset(key), [])

    rows, kept_back = [], 0
    n_children = n_unnamed_children = 0
    for ps, kids in units.items():
        ps = sorted(ps, key=lambda s: order[s])
        # the father (the parent a child's `father` names) heads the household
        fathers = {pc_s for (pc_s, c) in pc if c in kids and (people[c].get("father") or {}).get("slug") == pc_s}
        ps.sort(key=lambda s: (s not in fathers, order[s]))
        if not all(nameable(p) for p in ps):
            kept_back += 1
            continue
        pair = tuple(sorted(ps, key=order.get))
        spo = sp.get(pair) if len(ps) == 2 else None
        tree_pair = bool(spo) and spo[0] == "tree"
        kid_edges = [pc[(p, c)] for c in kids for p in ps if (p, c) in pc]
        all_tree = bool(kid_edges) and all(e[0] == "tree" for e in kid_edges)
        if len(ps) == 2:
            via = V_TREE if (tree_pair or (not spo and all_tree)) else (V_MARRIED if spo else V_TOGETHER)
        else:
            via = V_TREE if all_tree else V_ALONE
        shown, hidden = [], 0
        for c in sorted(kids, key=lambda s: (year_of(people[s].get("born")) or 9999, order[s])):
            if not nameable(c):
                hidden += 1
                continue
            r = people[c]
            dts, circa = dates_of(r)
            ev = [pc[(p, c)] for p in ps if (p, c) in pc]
            ctree = any(e[0] == "tree" for e in ev)
            cvia = V_TREE if ctree else (via if via != V_TREE else V_REGISTER)
            note = plain(next((e[1] for e in ev if e[1]), ""))
            kid = {"name": clean_name(r["name"]), "href": "/people/%s/" % c, "dates": dts, "via": cvia}
            if circa:
                kid["short"] = False
            if c in line:
                kid["line"] = True
            if note:
                kid["note"] = note
            shown.append(kid)
        n_children += len(shown)
        n_unnamed_children += hidden
        head, spouse = people[ps[0]], (people[ps[1]] if len(ps) == 2 else None)
        row = {"head": clean_name(head["name"]), "headHref": "/people/%s/" % ps[0], "via": via, "children": shown}
        if spouse:
            row["spouse"] = clean_name(spouse["name"])
            row["spouseHref"] = "/people/%s/" % ps[1]
        hb = year_of(head.get("born"))
        if hb:
            row["born"] = ("c. " if re.search(r"[c~]", str(head.get("born")), re.I) else "") + str(hb)
        if spo and spo[1]:
            row["note"] = "<span class=\"hh-lk\">the couple</span>" + esc(plain(spo[1]))
        if hidden:
            row["more"] = True
            tail = "Not every child recorded under this couple is named on this page."
            row["note"] = (row.get("note", "") + (" " if row.get("note") else "") + "<span class=\"small\">" + tail + "</span>")
        rows.append(row)

    rows.sort(key=lambda r: (r["head"].casefold(), r.get("spouse", "").casefold()))
    out = {
        "_note": "Made by tools/build-households.py from site/src/data/people.json and direct-line.json; never typed. Only people the lines page may list are named; "
                 "a household with a parent who may not be named is counted in `keptBack` and is not here.",
        "counts": {
            "households": len(rows),
            "keptBack": kept_back,
            "children": n_children,
            "withChildren": sum(1 for r in rows if r["children"]),
            "withNone": sum(1 for r in rows if not r["children"] and not r.get("more")),
            "marriage": sum(1 for r in rows if r["via"] == V_MARRIED),
            "together": sum(1 for r in rows if r["via"] == V_TOGETHER),
            "alone": sum(1 for r in rows if r["via"] == V_ALONE),
            "tree": sum(1 for r in rows if r["via"] == V_TREE),
            "moreThanTwoParents": len(over),
            "carryTheLine": sum(1 for r in rows for k in r["children"] if k.get("line")),
        },
        "rows": rows,
    }
    return out


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main(argv):
    out = build()
    text = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    c = out["counts"]
    summary = ("%d households shown (%d with children, %d with none recorded; %d children named; %d kept back because a parent may not be named; "
               "%d child row(s) with more than two parents)" % (c["households"], c["withChildren"], c["withNone"], c["children"], c["keptBack"],
                                                               c["moreThanTwoParents"]))
    if "--check" in argv:
        have = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if have != text:
            print("  FAIL  households: %s is not what people.json gives (run `python3 ../tools/build-households.py`)" % OUT.relative_to(ROOT))
            return 1
        print("  ok    households: " + summary + ", as committed")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print("build-households: " + summary + " -> " + str(OUT.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
