#!/usr/bin/env python3
"""Make site/src/data/family-lines.json, the family ribbons and the "how our line connects" blocks, from this archive's own data.
(27 October 2026)

    python3 tools/build-family-lines.py            write the file (the build runs this, as it runs lines:data)
    python3 tools/build-family-lines.py --check    fail, and write nothing, if the committed file is not what the data makes
    python3 tools/build-family-lines.py --report   print each family: cards, connections or why not

THE CONTRACT IS THE KIT'S (kit/docs/family-ribbon.md; components/FamilyRibbon.astro draws it; kit/tools/checkfamilyribbon.py is
the gate). WHAT THIS ARCHIVE ADDS is where every word comes from. Nothing about a family is typed here: a family page is the one
data/families.tsv names (site/src/data/families.json), plus /taylor/, which is the Taylors' own page (the families index files it
under the line, and src/lib/families.js sends the Taylor name there). Every card, every connection and every reason comes from:

  site/src/data/people.json        the register, as every person page draws it: the names, the years, the birthplace, and the
                                   father, mother, spouse and child links. A link that rests only on a family tree (via "tree")
                                   is not followed, as tools/build-lines.py does not follow one.
  site/src/data/story.json         the story's own statements: the ribbon's marriages (a card's person and spousePerson) and the
                                   households its chapter trees draw (a couple and their children). The story passed its own
                                   fact-check; the register does not yet hold every one of these links (see --report).
  site/src/data/direct-line.json   who is on our direct line: made from the story by the kit's directline.py, never typed.

THE RIBBON OF A FAMILY. Its own generations, earliest first, each a person whose parent is the card before, by a documented link.
  * A family the direct line TOUCHES: the line of that family down to the person who touches ours (who married one of ours, or is
    the parent of one of ours), each step up by the parent who carries the family's name. Where the touch is through a daughter
    who carries her father's name (Georgina Temple's daughter is a Brayley), that daughter is the last card, under her own name.
  * A family the direct line does not touch: the longest documented chain of parent and child among the people of the name (ties
    go to the earliest-born first card), and the status note says it is the longest of the chains, not "the" family.
  * Fewer than two generations: no ribbon. The kit draws no blocks without a ribbon, so such a family is left out of the file and
    --report says so; nothing is invented to fill it.

THE CARD. name (the register's, capitals and brackets taken out), years (birth and death years as the register prints them; a
death the data holds and no page prints is never shown, because such a person is not listed at all), "from" the register's
birthplace (graded: a birthplace the register qualifies as presumed or probable is inferred, one it says comes from a tree is
family lore, an empty one is "place not known"), and the spouse: the other parent of the next card's person where the register
or the story names one, else the person's one recorded spouse, else, on a card whose child is the next card, "spouse not named
in the records". No "at" line: the register's "where found" is the search that produced a person, not a dated residence.

WHO MAY APPEAR. Only a person who may stand in a public list (tools/build-lines.py's rule: not living, not held out, not an
unpublished death, and a birth year before the living line or a published death). A spouse who may not is not named.

HOW OUR LINE CONNECTS. For every person in direct-line.json (people and partners) and every parent, spouse and child of theirs
that the register or the story draws: if that relative is of this family (or is the touching daughter above), one connection.
The relation is OUR person's to theirs ("married", "son of", "daughter of", "child of" where the register does not say which);
the grade is the link's own (a register or line link is documented; a story link takes the story's grade); the note is the
register's own note on that link. A family with none says why not, from the same data: whom of ours it married into if that
was the story's unnamed generation (the break), else that no link joins it to the line.
"""
import argparse
import collections
import json
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
OUT = SITE / "family-lines.json"
STORY_BASE = "/story/"

# The Taylors' page is the one family page not built from data/families.tsv (site/src/pages/families.astro, TAYLOR; and
# src/lib/families.js sends the name there). Its forms and its address are the archive's, as written in those two files.
TAYLOR = {"slug": "taylor", "name": "Taylor", "forms": "Taylor", "page": "/taylor/"}

CAPS = re.compile(r"^[A-ZÁÉÍÓÚÑ]{3,}$")
TITLE = re.compile(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+$")
YEAR = re.compile(r"(?<!\d)(1[5-9]\d\d|20\d\d)(?!\d)")
INF_WORDS = re.compile(r"presum|probabl|likely|perhaps|possibl|\?|reckon|inferred|assumed", re.I)
LORE_WORDS = re.compile(r"\btree\b|\btrees\b|family chart", re.I)


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s or "")) if unicodedata.category(c) != "Mn").lower()


def surname_words(name):
    """The register's convention, as src/lib/families.js and tools/check-families.py read it."""
    words = re.sub(r"\([^)]*\)", " ", str(name or "")).split()
    caps = [i for i, w in enumerate(words) if CAPS.match(w)]
    if not caps:
        return [words[-1]] if words and TITLE.match(words[-1]) else []
    out = [words[i] for i in caps]
    i = caps[-1] + 1
    while i < len(words) and TITLE.match(words[i]):
        out.append(words[i])
        i += 1
    return out


def display(name):
    """'Mary Ann Hellen BRAYLEY' -> 'Mary Ann Hellen Brayley'; brackets and an '= probably ...' gloss are the register's notes."""
    s = str(name or "").split(" = ")[0]
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return " ".join(w[0] + w[1:].lower() if re.match(r"^[A-ZÁÉÍÓÚÑ]{2,}$", w) else w for w in s.split(" "))


def said(v):
    s = str(v if v is not None else "").strip()
    return "" if s in ("", "-", "?") else s


def clean_note(s, n=220):
    s = re.sub(r"\*{3}", "", str(s or ""))
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


def years_of(p):
    b, d = said(p.get("born")), said(p.get("died"))
    by = YEAR.search(b)
    dy = YEAR.search(d)
    bt = (("c." if re.match(r"^\s*(c\.|circa|about|abt)", b, re.I) else "") + by.group(1)) if by else ""
    dt = dy.group(1) if dy else ""
    if bt and dt:
        return "%s–%s" % (bt, dt)
    if bt:
        return "b. %s" % bt
    if dt:
        return "† %s" % dt
    return ""


def first_year(p):
    for k in ("born", "died"):
        m = YEAR.search(said(p.get(k)))
        if m:
            return int(m.group(1))
    return None


def origin_of(p):
    """(origin, grade): the register's birthplace, its first clause, graded by the register's own words about it."""
    raw = said(p.get("birthplace"))
    if not raw:
        return "place not known", "inf"
    head = re.sub(r"\([^)]*\)", " ", raw)
    head = re.split(r";|\s-\s|\s—\s", head)[0]
    head = re.sub(r"\s+", " ", head).strip(" ,.")
    if not head:
        return "place not known", "inf"
    if LORE_WORDS.search(raw) and not INF_WORDS.search(raw):
        return head, "lore"
    if INF_WORDS.search(raw) or LORE_WORDS.search(raw):
        return head, "inf"
    return head, "doc"


def citation_patterns():
    """The linking standard's citation patterns (site/standard.json, kit docs/linking-standard.md): a block's note that matched
    one would be a passage citing a record with no link to it (L3), and a generated block has no way to link it. So such a
    note is left off: the card's hover title and the person pages still carry it."""
    cfg = json.loads((ROOT / "site" / "standard.json").read_text(encoding="utf-8"))
    pats = ((cfg.get("citations") or {}).get("patterns")) or []
    return [re.compile(p["regex"], re.I if "i" in (p.get("flags") or "") else 0) for p in pats if p.get("regex")]


CITES = None


def cites(s):
    global CITES
    if CITES is None:
        CITES = citation_patterns()
    return any(r.search(s or "") for r in CITES)


def note_ok(s):
    """A block's note: the register's own words on the link, unless they cite a record (above) or only point at another
    note ("Same act."), which on its own says nothing."""
    return bool(s) and not cites(s) and not re.match(r"^\s*same\b", s, re.I)


def load():
    people = {p["slug"]: p for p in json.loads((SITE / "people.json").read_text(encoding="utf-8")) if p.get("slug")}
    fams = json.loads((SITE / "families.json").read_text(encoding="utf-8"))
    story = json.loads((SITE / "story.json").read_text(encoding="utf-8"))
    dl = json.loads((SITE / "direct-line.json").read_text(encoding="utf-8"))
    return people, fams, story, dl


def unpublished_dead():
    p = DATA / "living-year-allow.json"
    if not p.exists():
        return set()
    return {e["slug"] for e in json.loads(p.read_text(encoding="utf-8")).get("unpublished_deaths", [])}


class Graph:
    """Parent, spouse and child links, from the register (people.json) and the story (ribbon marriages, chapter trees)."""

    def __init__(self, people, story):
        self.people = people
        self.parents = collections.defaultdict(dict)    # child -> {parent: (grade, note, source)}
        self.spouses = collections.defaultdict(dict)    # a -> {b: (grade, note, source)}
        self.male, self.female = set(), set()
        self.gaps = []                                   # links the story states and the register does not draw
        for r in people.values():
            s = r["slug"]
            for k in ("father", "mother"):
                n = r.get(k)
                if n and n.get("slug") in people and n.get("via") != "tree":
                    self._parent(s, n["slug"], "doc", n.get("note", ""), "register")
                    (self.male if k == "father" else self.female).add(n["slug"])
            for c in r.get("children") or []:
                if c.get("slug") in people and c.get("via") != "tree":
                    self._parent(c["slug"], s, "doc", c.get("note", ""), "register")
            for n in r.get("spouses") or []:
                if n.get("slug") in people and n.get("via") != "tree":
                    self._spouse(s, n["slug"], "doc", n.get("note", ""), "register")
        # the story: the ribbon's marriages and each chapter tree's households
        cards = (story.get("ribbon") or {}).get("cards") or []
        for c in cards:
            a, b = c.get("person"), c.get("spousePerson")
            if a in people and b in people:
                if b not in self.spouses[a]:
                    self.gaps.append("the story marries %s to %s; the register draws no marriage" % (a, b))
                self._spouse(a, b, c.get("originGrade") or "lore", ("The story: %s" % c["title"]) if c.get("title") else "", "story")
        for ch in story.get("chapters") or []:
            t = ch.get("tree") or {}
            byid, couple = {}, []
            for row in t.get("rows") or []:
                for n in row.get("nodes") or []:
                    byid[n.get("id")] = n
                if row.get("kind") == "couple":
                    couple = [n for n in row.get("nodes") or [] if n.get("person") in people]
                    if len(couple) == 2:
                        g = worst(couple[0].get("grade"), couple[1].get("grade"))
                        a, b = couple[0]["person"], couple[1]["person"]
                        if b not in self.spouses[a]:
                            self.gaps.append("the story's '%s' tree draws %s and %s as a couple; the register draws no marriage" % (ch.get("id"), a, b))
                        self._spouse(a, b, g, "", "story:" + ch.get("id", ""))
            for row in t.get("rows") or []:
                if row.get("kind") != "children":
                    continue
                for k in row.get("nodes") or []:
                    if k.get("person") not in people or k.get("living"):
                        continue
                    par = [byid[k["of"]]] if k.get("of") in byid else couple
                    for pn in par:
                        if pn.get("person") in people:
                            if pn["person"] not in self.parents[k["person"]]:
                                self.gaps.append("the story's '%s' tree draws %s as a child of %s; the register draws no such link" % (ch.get("id"), k["person"], pn["person"]))
                            self._parent(k["person"], pn["person"], worst(k.get("grade"), pn.get("grade")), "", "story:" + ch.get("id", ""))

    def _parent(self, child, parent, grade, note, src):
        old = self.parents[child].get(parent)
        if old is None or (old[2] != "register" and src == "register"):
            self.parents[child][parent] = (grade, note or (old[1] if old else ""), src)

    def _spouse(self, a, b, grade, note, src):
        for x, y in ((a, b), (b, a)):
            old = self.spouses[x].get(y)
            if old is None or (old[2] != "register" and src == "register"):
                self.spouses[x][y] = (grade, note or (old[1] if old else ""), src)

    def children(self, s):
        return [c for c, ps in self.parents.items() if s in ps]

    def sex(self, s):
        return "m" if s in self.male and s not in self.female else "f" if s in self.female and s not in self.male else ""


def worst(*gs):
    order = {"doc": 0, "inf": 1, "lore": 2}
    gs = [g if g in order else "lore" for g in gs]
    return max(gs, key=lambda g: order[g])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()

    people, fams, story, dl = load()
    cutoff = L.current_cutoff()
    unpub = unpublished_dead()

    def listable(s):
        """the family page's own rule (src/lib/families.js listable): never living, never held out; and never an unpublished death"""
        r = people.get(s)
        return bool(r) and not r.get("living") and not r.get("noindex") and s not in unpub

    G = Graph(people, story)
    ours = {}
    for p in dl.get("people") or []:
        ours[p["slug"]] = p
    for p in dl.get("partners") or []:
        ours.setdefault(p["slug"], p)
    cards_story = (story.get("ribbon") or {}).get("cards") or []

    # the story's unnamed generation(s): a ribbon card with no person; its people are the children its previous card's chapter tree draws
    unnamed = {}
    for u in dl.get("unlinked") or []:
        g = u["generation"]
        prev = next((p for p in dl.get("people") or [] if p["generation"] == g - 1), None)
        if not prev:
            continue
        kids = {c for c in G.children(prev["slug"])}
        unnamed[g] = {"of": prev, "kids": kids, "next": next((p for p in dl.get("people") or [] if p["generation"] > g), None)}

    def bearers_of(forms):
        toks = {fold(x) for x in forms.split("|")}
        return {s for s, r in people.items() if listable(s) and any(fold(w) in toks for w in surname_words(r.get("name")))}

    def bearer_parent(s, B):
        ps = [(q, v) for q, v in G.parents.get(s, {}).items() if q in B and listable(q)]
        if not ps:
            return None
        ps.sort(key=lambda qv: (G.sex(qv[0]) != "m", qv[0]))      # the father first, the name in this register passes through him
        return ps[0]

    def coparent(s, child):
        if not child:
            return None
        others = [q for q in G.parents.get(child, {}) if q != s]
        return others[0] if len(others) == 1 else None

    def card_for(s, nxt, is_last):
        r = people[s]
        origin, grade = origin_of(r)
        sp = coparent(s, nxt)
        if sp is None:
            sps = [q for q in G.spouses.get(s, {}) if listable(q) or q in people]
            sp = sps[0] if len(sps) == 1 else None
        spouse = spouse_origin = sp_person = ""
        if sp and listable(sp):
            spouse = display(people[sp]["name"])
            so, _ = origin_of(people[sp])
            spouse_origin = "of %s" % so if so != "place not known" else "place not known"
            sp_person = sp
        elif sp is None and nxt and not is_last:
            spouse, spouse_origin = "spouse not named in the records", ""
        card = {"name": display(r["name"]), "years": years_of(r), "origin": origin, "originGrade": grade,
                "spouse": spouse, "spouseOrigin": spouse_origin, "atPlace": "", "atYear": "", "living": False, "person": s}
        if sp_person:
            card["spousePerson"] = sp_person
        return card

    def chain_cards(chain, after=None):
        out = []
        for i, s in enumerate(chain):
            nxt = chain[i + 1] if i + 1 < len(chain) else after
            c = card_for(s, nxt, i + 1 == len(chain))
            if i > 0:
                g, note, src = G.parents[s][chain[i - 1]]
                why = clean_note(note) if note else ("drawn in the story" if src.startswith("story") else "")
                if why:
                    c["title"] = "Child of the card before: %s" % why
            out.append(c)
        return out

    def relation(our, their):
        """our person's relation to theirs, and the link's (grade, note, source); None if no link"""
        if their in G.spouses.get(our, {}):
            return ("married",) + G.spouses[our][their]
        if their in G.parents.get(our, {}):
            sx = G.sex(our)
            return ({"m": "son of", "f": "daughter of"}.get(sx, "child of"),) + G.parents[our][their]
        if our in G.parents.get(their, {}):
            sx = G.sex(our)
            return ({"m": "father of", "f": "mother of"}.get(sx, "parent of"),) + G.parents[their][our]
        return None

    out_fams, report = [], []
    for f in [dict(x, page="/families/%s/" % x["slug"]) for x in fams] + [TAYLOR]:
        B = bearers_of(f["forms"])
        # the touches: a relative of one of ours who is of this family; or our parent whose own parent is (the daughter step)
        touches = []
        # a CHILD of one of ours is our own family, whatever second surname it carries: only spouses and parents are touches
        for o in sorted(ours, key=lambda s: (ours[s]["generation"], s)):
            rel_people = set(G.spouses.get(o, {})) | set(G.parents.get(o, {}))
            for x in sorted(rel_people):
                if not listable(x) or x == o:
                    continue
                if x in B:
                    touches.append((o, x, None))
                elif x in G.parents.get(o, {}) and x not in ours:
                    bp = bearer_parent(x, B)
                    if bp:
                        touches.append((o, x, bp[0]))
        conns, chain, after = [], [], None
        if touches:
            # the family's line down to the member of it who is on our line, else to the touching person nearest the top of our line
            own = sorted((s for s in ours if s in B and listable(s)), key=lambda s: (ours[s]["generation"], s))
            if own:
                end, via = own[0], None
            else:
                _, end, via = touches[0]
            chain = [end]
            cur = via or end
            if via:
                chain.insert(0, via)
            seen = set(chain)
            while True:
                bp = bearer_parent(cur, B)
                if not bp or bp[0] in seen:
                    break
                chain.insert(0, bp[0])
                seen.add(bp[0])
                cur = bp[0]
            # whose parent the last card is, on our line: the spouse on that card is that child's other parent
            after = next((s for s in sorted(ours, key=lambda s: ours[s]["generation"]) if chain[-1] in G.parents.get(s, {})), None)
            for o, x, via in touches:
                rel = relation(o, x)
                if not rel:
                    continue
                word, grade, note, src = rel
                conns.append({"ourSlug": o, "ourGeneration": ours[o]["generation"], "theirSlug": x,
                              "theirName": display(people[x]["name"]),
                              "theirOrigin": ("of %s" % origin_of(people[x])[0]) if origin_of(people[x])[0] != "place not known" else "",
                              "relation": word, "grade": grade, "storyHref": "%s#%s" % (STORY_BASE, ours[o]["storyChapter"]),
                              **({"note": clean_note(note)} if note_ok(clean_note(note)) else {} if note else {"note": "Drawn in the story (%s)." % src.split(":", 1)[1]} if src.startswith("story:") else {"note": "On the story's ribbon."} if src == "story" else {})})
            # one block per pair and relation; a married pair is drawn once, from the side of our line it is told from
            uniq, seen_pairs = [], set()
            for c in conns:
                k = frozenset((c["ourSlug"], c["theirSlug"])) if c["relation"] == "married" else (c["ourSlug"], c["theirSlug"], c["relation"])
                if k in seen_pairs:
                    continue
                seen_pairs.add(k)
                uniq.append(c)
            conns = uniq
        else:
            # the longest documented chain among the people of the name
            kids = {s: sorted(c for c in G.children(s) if c in B) for s in B}
            memo = {}

            def longest(s, path=()):
                if s in memo:
                    return memo[s]
                best = [s]
                for c in kids[s]:
                    if c in path:
                        continue
                    l = [s] + longest(c, path + (s,))
                    if len(l) > len(best) or (len(l) == len(best) and (first_year(people[l[-1]]) or 9999) < (first_year(people[best[-1]]) or 9999)):
                        best = l
                memo[s] = best
                return best
            cands = sorted((longest(s) for s in B), key=lambda l: (-len(l), first_year(people[l[0]]) or 9999, l[0]))
            chain = cands[0] if cands else []
            n_max = sum(1 for l in cands if len(l) == len(chain) and l[0] not in chain[1:]) if chain else 0
        fam = {"id": f["slug"], "title": f["name"], "page": f["page"]}
        cards = chain_cards(chain, after) if len(chain) >= 2 else []
        yrs = [y for s in chain for y in [first_year(people[s])] if y]
        if cards:
            first_grade = cards[0]["originGrade"]
            fam["status"] = "documented" if first_grade == "doc" else "origin-unknown" if cards[0]["origin"] == "place not known" else "inferred" if first_grade == "inf" else "family-lore"
            if touches:
                fam["statusNote"] = "%d generations, each the child of the one before by a record this archive holds, down to where our line meets it" % len(cards)
            else:
                fam["statusNote"] = "the longest chain of parent and child the archive holds among the %d people of the name, not the whole family" % len(B)
            if yrs:
                fam["span"] = [min(yrs), None]
            fam["cards"] = cards
        if conns:
            fam["connections"] = conns
        else:
            why = None
            for g, u in sorted(unnamed.items()):
                hits = []
                for b in sorted(B):
                    for k in sorted(u["kids"]):
                        if k == b or k in G.spouses.get(b, {}):
                            hits.append((b, k))
                if hits:
                    b, k = hits[0]
                    who = display(people[b]["name"])
                    kid = display(people[k]["name"])
                    nm = u["of"].get("name") or display(people[u["of"]["slug"]]["name"])
                    lead = ("%s is one of %s's children" % (who, nm)) if b == k else ("%s married %s, one of %s's children" % (who, kid, nm))
                    nxt = u["next"]
                    why = ("%s (generation %d of our line). The story draws that generation as one card with nobody named, because no paper "
                           "says which of %s's children, if any, carries the line on; between it and generation %d the line is broken."
                           % (lead, g, nm, nxt["generation"] if nxt else g + 1))
                    break
            if not why:
                why = ("No parent, child or marriage the register or the story holds joins any of the %d people of this name to anyone on our line."
                       % len(B))
            fam["notConnected"] = {"why": why}
        if not cards:
            report.append("  --    %-10s NOT IN THE FILE: no chain of two documented generations (%d people of the name); %s"
                          % (f["slug"], len(B), "%d connection(s) cannot be drawn without a ribbon" % len(conns) if conns else "not connected"))
            continue
        out_fams.append(fam)
        report.append("  ok    %-10s %d card(s) [%s]; %s" % (f["slug"], len(cards), " > ".join(c["name"] for c in cards),
                      ("%d connection(s): " % len(conns)) + "; ".join("%s %s %s (%s)" % (c["ourSlug"], c["relation"], c["theirSlug"], c["grade"]) for c in conns)
                      if conns else "not connected: " + fam["notConnected"]["why"][:120]))

    doc = {"_note": "Made by tools/build-family-lines.py from people.json, story.json and direct-line.json; do not edit by hand.",
           "families": out_fams}
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    if a.report:
        print("\n".join(report))
        if G.gaps:
            print("  the story states, the register does not draw (%d):" % len(G.gaps))
            for gp in G.gaps:
                print("        - " + gp)
    if a.check:
        cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if cur != text:
            print("  FAIL  family-lines  site/src/data/family-lines.json is not what the data makes: run python3 tools/build-family-lines.py")
            return 1
        print("  ok    family-lines  %d family ribbon(s), the file is what the data makes" % len(out_fams))
        return 0
    OUT.write_text(text, encoding="utf-8")
    print("build-family-lines: %d family ribbon(s), %d connection(s), %d not connected"
          % (len(out_fams), sum(len(f.get("connections", [])) for f in out_fams), sum(1 for f in out_fams if f.get("notConnected"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
