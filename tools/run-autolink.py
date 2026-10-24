#!/usr/bin/env python3
"""Link the names on the built pages to their people (the kit's autolink.py), and gate the number.

    python3 tools/run-autolink.py                 build the index and the living list, then link site/dist
    python3 tools/run-autolink.py --gate          the kit's checklinks.py against site/.linkfloor.json (last step of the build)
    python3 tools/run-autolink.py --write-floor   lock the current counts in as the ceiling (refuses while anything rose)
    python3 tools/run-autolink.py --check         change nothing; exit 1 if a run would
    python3 tools/run-autolink.py --index-only    write site/src/data/names-index.json and the living list, run nothing else
    python3 tools/run-autolink.py --standard      the kit's checkstandard.py (the linking standard) against site/.standardfloor.json
    python3 tools/run-autolink.py --write-standard-floor   lock the standard's counts in as the ceiling (refuses while anything rose)
    python3 tools/run-autolink.py --pick-same [--top N]   count the unresolved shared-name links in site/dist and write the N commonest (10) to data/same-names.tsv
    python3 tools/run-autolink.py --same-data     write site/src/data/same-name.json (the pages' bearer lists) from people.json; the build runs it before astro

WHY (David, 18 October 2026: "why do so many names on our narrative pages have no link to their person page?"). The audit
of the same day found 23 of 1,254 resolvable mentions linked on this archive's twelve longest pages (1.8%) and none of the
360 shared-name mentions; the only linking was a person() function on /taylor/ and a few typed hrefs. The kit now holds one
build-time tool for it (kit/tools/autolink.py, docs in kit/docs/autolink.md). This file is THIS ARCHIVE'S side of it: it
makes the two inputs the tool asks for, from data the build already reads, and runs the tool.

THE NAMES INDEX (site/src/data/names-index.json, committed: it holds only names that already have public pages).
  people     a name that is borne by ONE person in the archive's data, who has an indexable /people/<slug>/ page, is not
             living, is not held out, is not an alias row and is not a person born within a hundred years with no death
             recorded. The name is written as the prose writes it ("Given Family"), not as the register does ("Given FAMILY").
  aliases    only the accent forms the archive's own namefold.json holds for a word of the name (Fernandez -> Fernandez with
             an acute): a spelling fold, never a change of letter, and never an alias another name already owns.
  ambiguous  a name borne by several people, none of whom is living or held, sent to /people/?q=<name>, the people list
             pre-filtered (the kit's FilterTable reads ?q=). /who/<slug>/ is NOT used: that page is keyed by the register's
             whole string, descriptor and all, so it gathers one spelling of a name and not everybody who bore it.
  A name is only the cleaned name: brackets and what is inside them are dropped, and a leading honorific. A one-word
  name, a name with a digit, a comma, a slash, an "=" or a bracket, an initial-only ending, or a name the cleaning cannot
  stand behind, is never indexed. A bare given name is never linked (the kit's --min-words 2 as well).

  RESOLVE RULES (19 October 2026; kit docs/autolink.md, "Shared names"). David clicked "Maria Lerena" in the card of her husband and
  landed on a list of 18 people. An ambiguous entry now carries `resolve: [{near, url}]`: "a relative of exactly one bearer of this name,
  `near`, is named in the same block within 120 characters, so the name there is that bearer, `url`". They are made by resolve_rules()
  below from SPOUSE and CO-PARENT edges only (a husband or wife, or the other recorded parent of a child), and only when that relative
  is related, by ANY recorded kind of relationship (spouse, parent, child, sibling, co-parent, a relative the data writes inside a
  bearer's own register name or note), to exactly ONE bearer of the name. Parent, child and sibling edges never make a rule: names run
  down families and the same recipe built from them took a groom, a godfather and a father for the namesake son (the kit's Lerena trial:
  about 10 of 39 extra links wrong); spouse and co-parent rules read 95 for 95 in their sentences. A relative of a bearer who cannot be
  linked (living, held out, no page) makes a counter-rule `{near, url: null}`. `bearers` lists the dead, paged bearers who are not in
  `people`. A link the rules do not decide stays the search link, marked (class lk-shared, title and aria-label from labels.shared).

THE LIVING LIST (written OUTSIDE the repository, $AUTOLINK_LIVING or ~/.local/state/lerena/autolink-living.json).
  Built from tools/livingcheck.py, the independent reckoning every living gate here uses (the register, the relations list,
  the roster, the held-out ids, the estate's one rule in the kit's living_rule.py), plus every row people.json itself marks
  living. Each living or held-out person contributes their name, the forms a sentence might use for them, and their
  addresses. Nothing in it is private DATA: it is derived from tracked files only, so CI can build it, and CI does.

THE SAME-NAME PAGES (19 October 2026; David: "build proper disambiguation pages for the most-shared names"). A shared name no rule decides used to
  land the reader on the filtered people list, a long table. For the N commonest such names (data/same-names.tsv, written by --pick-same from the
  count of data-autolink="search" links in the built site) the unresolved target is now /same-name/<slug>/, a page that lists every dead person
  with a page who bears the name (the resolve rules' own bearer set: is_subseq, so a "Maria Adelina LERENA Traibel" is a bearer of "Maria Lerena"
  and a rule may send a reader to her), what the data says to tell them apart, and a link to each. Only the url of the index entry changes: the
  entry is still `ambiguous`, the link is still data-autolink="search", and every resolve rule stands. The page data is site/src/data/same-name.json
  (--same-data; committed, like the names index). A bearer who is living, held out or undated-and-recent is NEVER listed; if a name has one, the
  generator stops (exit 2) rather than print a count the page could not stand behind. The kit has one label for every search link
  (labels.shared), so the cue is the same on every unresolved link.

CI. The deploy runs `npm run build`, which runs this file on the tracked data: nothing here needs a gitignored file. If the
living list cannot be built (no kit, nobody living found, no people.json) this file exits 2 and the build stops: a linker that
cannot check the living list does not run. It prints COUNTS only, never a name.
"""
import argparse
import html as _html
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = ROOT / "site"
ALIASES = ROOT / "data" / "names-aliases.tsv"
SAME_PICK = ROOT / "data" / "same-names.tsv"
SAME_DATA = ROOT / "site" / "src" / "data" / "same-name.json"
SAME_PREFIX = "/same-name/"
SAME_TOP = 10
sys.path.insert(0, str(HERE))
import livingcheck as L  # noqa: E402

KIT = SITE / "node_modules" / "@daviddef" / "archive-kit" / "kit" / "tools"
INDEX = SITE / "src" / "data" / "names-index.json"
FLOOR = SITE / ".linkfloor.json"
PEOPLE = SITE / "src" / "data" / "people.json"
NAMEFOLD = SITE / "src" / "data" / "namefold.json"

HONORIFICS = {"don", "dona", "dr", "dr.", "doctor", "sr", "sr.", "sra", "sra.", "capitan", "general", "exmo", "fray", "padre",
              "mr", "mr.", "mrs", "mrs.", "miss", "sir", "rev", "rev."}
PARTICLES = {"de", "del", "la", "las", "los", "y", "da", "do", "dos", "van", "von", "di", "du", "le", "el", "e"}
# A word of a name: letters (with accents), joined by a hyphen or an apostrophe. No digit, bracket, comma, slash or "=".
WORD = re.compile(r"^[^\W\d_]+(?:['\-][^\W\d_]+)*$")
RECENT_YEARS = 100          # born this recently with no death recorded: not asserted dead here, never linked


def living_path():
    if os.environ.get("AUTOLINK_LIVING"):
        return pathlib.Path(os.environ["AUTOLINK_LIVING"])
    base = os.environ.get("XDG_STATE_HOME") or str(pathlib.Path.home() / ".local" / "state")
    return pathlib.Path(base) / "lerena" / "autolink-living.json"


def ascii_fold(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def accent_fold(s):
    """Remove the accents of a word, the n-tilde included (the register writes ASCII: Lavina for the Lavina with a tilde on the n
    that the pages print), but leave the family's own surname alone: Lerena and Lerena-with-a-tilde are two spellings of that
    surname which name-variants.tsv records one by one, not one word with an accent."""
    base = unicodedata.normalize("NFKD", s)
    base = "".join(c for c in base if not unicodedata.combining(c))
    if base.casefold() in FAMILY_SURNAMES_ASCII and base != s and "\u00f1" in s.casefold():
        return s
    return base


def slugify(s):
    return re.sub(r"[^A-Za-z0-9]+", "-", ascii_fold(str(s or ""))).strip("-").lower()


def clean(raw):
    """The name a sentence would use for this register string, or "" when no honest name can be made of it."""
    s = re.sub(r"\(.*?\)|\[.*?\]", " ", str(raw or ""))
    s = " ".join(s.replace('"', " ").split())
    words = s.split(" ") if s else []
    while len(words) > 1 and words[0].casefold() in HONORIFICS:
        words.pop(0)
    if len(words) < 2:
        return ""
    for w in words:
        if w.casefold() in PARTICLES:
            continue
        if not WORD.match(w):
            return ""
    if words[-1].casefold() in PARTICLES or len(words[-1]) < 2:
        return ""
    return " ".join(words)


def display(cleaned):
    """As prose writes it: a word the register capitalised whole (LERENA) is written Lerena; D'ARCY is D'Arcy."""
    out = []
    for w in cleaned.split(" "):
        if len(w) >= 2 and w == w.upper() and any(c.isalpha() for c in w):
            w = re.sub(r"[^\W\d_]+", lambda m: m.group(0)[0].upper() + m.group(0)[1:].lower(), w)
        out.append(w)
    return " ".join(out)


def key_of(cleaned):
    return " ".join(ascii_fold(cleaned).casefold().split())


def accent_forms():
    """word (lower, no accent) -> accented spellings the archive's own fold table holds for it. Accent only: a form is
    kept when removing its accents gives back exactly the word, so no letter ever changes."""
    out = {}
    try:
        fold = json.loads(NAMEFOLD.read_text(encoding="utf-8")).get("fold", {})
    except (OSError, ValueError):
        return out
    for v in fold:
        base = ascii_fold(v).casefold()
        if v != base and ascii_fold(v).casefold() == base:
            out.setdefault(base, set()).add(v)
    return out



# ---------------------------------------------------------------------------------------------------------------------------
# ALIASES: three kinds, each one a form THE ARCHIVE'S OWN DATA STATES (nothing is guessed, no letter is ever changed except
# where the data's own spelling is named in data/names-aliases.tsv).
#   accent    the same name with the accents the archive's committed text writes it with (Jose -> Jose with an acute, Fernandez
#             -> Fernandez with an acute). Accent only: removing the accents gives the name back exactly. The accented spellings
#             are read from data/*.tsv and the page sources, so a form never seen in the archive's own text is never made.
#   short     the contraction the register's own capital-letter convention marks: the first surname is the ALL-CAPS word, so
#             "Maria Adela LERENA Carniglia" is also "Maria Adela Lerena" and "Maria Lerena". Made only when that form belongs
#             to ONE person among everybody the register holds (living and held-out included), is not another person's whole
#             name, and is not a living person's name.
#   stated    data/names-aliases.tsv: one line per form, naming the person (their register name), and the file in which the
#             data writes that form for them. This is how a spelling the data records (Treibel for Traibel, a surname the
#             machine read) and a person whose register name carries an initial or an editorial bracket get their links.
# ---------------------------------------------------------------------------------------------------------------------------
TOKEN = re.compile(r"[^\W\d_]+(?:['\u2019\-][^\W\d_]+)*", re.U)


def corpus_accents():
    """ascii word (lower) -> the accented spellings (lower) that the committed text writes, at least twice each."""
    counts = {}
    paths = sorted((ROOT / "data").glob("*.tsv")) + sorted((SITE / "src" / "pages").rglob("*.astro"))
    for p in paths:
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in TOKEN.finditer(text):
            w = m.group(0)
            if accent_fold(w) != w and len(w) > 2:
                lw = w.casefold()
                counts[lw] = counts.get(lw, 0) + 1
    out = {}
    for w, n in counts.items():
        if n >= 2:
            out.setdefault(accent_fold(w).casefold(), []).append((n, w))
    return {k: [w for _n, w in sorted(v, reverse=True)[:2]] for k, v in out.items()}


def accent_variants(name, acc):
    words = name.split(" ")
    variants = [[]]
    for w in words:
        forms = [w]
        for a in acc.get(accent_fold(w).casefold(), ()):
            forms.append(a[:1].upper() + a[1:] if w[:1].isupper() else a)
        variants = [v + [f] for v in variants for f in forms][:64]
    return sorted({" ".join(v) for v in variants} - {name})


# the surname of the family itself, in the spellings this archive meets (name-variants.tsv): "Given Lerena" is not a form that
# belongs to one person, whoever the register holds under it, so it is never made a short form
FAMILY_SURNAMES = {"lerena", "llerena", "lerina", "larena", "lorena", "serena", "gerena", "perena", "levena", "leresa", "lerrena",
                   "ledena", "alerena"}
FAMILY_SURNAMES_ASCII = FAMILY_SURNAMES


def short_forms(raw):
    """The contractions the register's capital-letter convention marks (see above), as display strings; [] when none.
    The first surname is the first capital-letter word (a capitalised DE and the word after it stay: RUIZ DE CARVALLO; a lower-case
    de ends it: POU de ZALDUONDO is Pou, wife of Zalduondo; a second capitalised word, LERENA LARRIERA, is the second surname). The forms are
      every given name and the first surname   (two or more given names, or any surname that is not the family's own)
    and never the first given name with the surname alone ("Roberto Lerena", "Horace Taylor", "Mary Taylor" name a dozen people
    between them, and the archive's own pages use them for people the register does not hold)."""
    s = re.sub(r"\(.*?\)|\[.*?\]", " ", str(raw or ""))
    words = " ".join(s.replace('"', " ").split()).split(" ")
    while len(words) > 1 and words[0].casefold() in HONORIFICS:
        words.pop(0)
    if len(words) < 2:
        return []
    def is_cap(w):
        return len(w) >= 2 and w == w.upper() and any(c.isalpha() for c in w)
    caps = [i for i, w in enumerate(words) if is_cap(w) and w.casefold() not in PARTICLES]
    if not caps:
        return []
    i = caps[0]
    j = i
    # the first surname runs on only through a capitalised particle and the capitalised word after it (RUIZ DE CARVALLO); a second
    # capitalised word with no particle (LERENA LARRIERA) is the second surname
    while j + 2 < len(words) and is_cap(words[j + 1]) and words[j + 1].casefold() in PARTICLES and is_cap(words[j + 2]):
        j += 2
    sur = words[i:j + 1]
    family = ascii_fold(" ".join(sur)).casefold() in FAMILY_SURNAMES
    forms = []
    if i >= 2 or (i == 1 and not family):
        forms.append(words[:i] + sur)                    # every given name and the first surname
    out = []
    for f in forms:
        c = clean(" ".join(f))
        if c and len(f) < len(words):
            out.append(display(c))
    return out


def stated_aliases(rows):
    """data/names-aliases.tsv -> [(alias, register name, slug, basis)]. A line naming nobody, or with no basis, stops the build."""
    out = []
    if not ALIASES.exists():
        return out
    by_name = {r["name"]: r for r in rows}
    for n, line in enumerate(ALIASES.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#") or line.startswith("alias\t"):
            continue
        cells = (line.split("\t") + ["", "", ""])[:3]
        alias, who, basis = [c.strip() for c in cells]
        r = by_name.get(who)
        if not alias or len(alias.split()) < 2 or r is None or len(basis) < 12:
            print(f"  FAIL  names      data/names-aliases.tsv line {n}: needs a two-word alias, a register name that exists and a basis")
            raise SystemExit(2)
        out.append((alias, who, r["slug"], basis))
    return out


def living_terms(pop, rows):
    """Every living or held-out person's names and addresses, for the tool's --living."""
    spouses = {}
    for who, rel, oth, *_ in L.edges(ROOT):
        if rel == "spouse":
            spouses.setdefault(who, set()).add(oth)
            spouses.setdefault(oth, set()).add(who)
    names, addrs = set(), set()
    people = [p for p in pop if p.living or getattr(p, "held", False)]
    for p in people:
        raws = {p.name}
        c = clean(p.name)
        forms = {c, display(c)} if c else set()
        forms |= {v for v in L.name_variants(p.name)}
        given = p.name.split()[0] if p.name.split() else ""
        for sp in spouses.get(p.name, ()):
            sur = sp.split()[-1] if sp.split() else ""
            if given and sur and len(sur) > 3:
                forms |= {f"{given} {sur}", f"{given} {sur.title()}"}
        for f in forms:
            f = " ".join(str(f).split())
            if f:
                names.add(f)
                names.add(display(f))
                names.add(ascii_fold(f))
                names.add(ascii_fold(display(f)))
        slug = p.slug or ""
        if slug:
            addrs.add(f"/people/{slug}/")
        addrs.add(f"/who/{slugify(p.name)}/")
    for r in rows:
        if r.get("living"):
            c = clean(r["name"])
            forms = {c, display(c)} if c else set()
            forms |= {v for v in L.name_variants(r["name"])}
            for f in forms:
                if f:
                    names.add(f); names.add(display(f)); names.add(ascii_fold(f)); names.add(ascii_fold(display(f)))
            addrs.add(f"/people/{r['slug']}/")
            addrs.add(f"/who/{slugify(r['name'])}/")
    names = {n for n in names if n and len(n) > 3}
    return sorted(names), sorted(addrs), len(people) + sum(1 for r in rows if r.get("living"))


# ---------------------------------------------------------------------------------------------------------------------------
# RESOLVE RULES for the shared names (see the docstring). Spouse and co-parent edges make a rule; every kind of relationship (and a
# relative the data writes into a bearer's own name or note) can stop one.
# ---------------------------------------------------------------------------------------------------------------------------
NEAR_WINDOW = 120
SHARED_LABEL = "Several people share this name: opens the page that tells them apart"
RULE_KINDS = {"spouse", "coparent"}


def tokens_of(raw):
    s = re.sub(r"\(.*?\)|\[.*?\]", " ", str(raw or "")).replace('"', " ")
    return [ascii_fold(w).casefold().strip(".,;:") for w in s.split() if w.strip(".,;:")]


def is_subseq(needle, hay):
    """The name's words, in order, among the register name's words, the first word the same: 'Maria Lerena' is borne by 'Maria Josefa
    LERENA Carniglia' and by 'Maria GONZALEZ Lerena'. Wide on purpose: it can only count more bearers, so fewer rules."""
    if not hay or not needle or hay[0] != needle[0]:
        return False
    it = iter(hay)
    return all(any(x == w for x in it) for w in needle)


def relationship_graph(rows, pop):
    """slug -> {slug: {kinds}} where kinds are what the OTHER person is to this one: spouse, parent, child, sibling, coparent.
    Every form the data holds: the father/mother fields, the spouses/children/siblings lists (either direction), two people who
    are the recorded parents of one child. Also `written`: slug -> {slug} for a relative the data writes inside a bearer's own
    register name, and the register's own relations list (data/relations.tsv): these cannot make a rule, only stop one. A relative
    named in a bearer's NOTE is not a relationship and stops nothing (a note that says "aunt of Juan Carlos" would otherwise take
    the rule from the very couple it names)."""
    by = {r["slug"]: r for r in rows}
    kinds = {s: {} for s in by}

    def edge(a, b, a_is_to_b, b_is_to_a):
        if a == b or a not in by or b not in by:
            return
        kinds[b].setdefault(a, set()).add(a_is_to_b)
        kinds[a].setdefault(b, set()).add(b_is_to_a)

    for r in rows:
        for k in ("father", "mother"):
            o = r.get(k)
            if o and o.get("slug") in by:
                edge(r["slug"], o["slug"], "child", "parent")
        for k, (x, y) in (("spouses", ("spouse", "spouse")), ("children", ("parent", "child")), ("siblings", ("sibling", "sibling"))):
            for o in r.get(k) or []:
                if o.get("slug") in by:
                    edge(r["slug"], o["slug"], x, y)
    for r in rows:
        f, m = (r.get("father") or {}).get("slug"), (r.get("mother") or {}).get("slug")
        if f in by and m in by and f != m:
            kinds[f].setdefault(m, set()).add("coparent")
            kinds[m].setdefault(f, set()).add("coparent")
    # a relative the data only writes: the register's relations list (by register name), and a person's cleaned name inside another's
    # raw name ("Alejandro LERENA (m. Margarita Fernandez)": a wife the data holds only there), either way round
    written = {s: set() for s in by}
    slug_of = {r["name"]: r["slug"] for r in rows}
    for who, rel, oth, *_ in L.edges(ROOT):
        a, b = slug_of.get(who), slug_of.get(oth)
        if a and b and a != b:
            written[a].add(b)
            written[b].add(a)
    flat = lambda x: " " + " ".join(tokens_of(re.sub(r"[()\[\]\"]", " ", str(x or "")))) + " "
    raw_flat = {s: flat(r["name"]) for s, r in by.items()}
    name_flat = {s: flat(r["name"]) for s, r in by.items()}
    key = {s: " " + " ".join(tokens_of(clean(r["name"]) or "")) + " " for s, r in by.items()}
    two = {s for s, k in key.items() if len(k.split()) >= 2}
    index_of_key = {}
    for s in two:
        index_of_key.setdefault(key[s], set()).add(s)
    for s in by:
        for k, who in index_of_key.items():
            if k in raw_flat[s]:
                for t in who:
                    if t != s:
                        written[s].add(t)
                        written[t].add(s)
    return kinds, written


def resolve_rules(ambiguous, people, rows, pop, year, living_addr):
    """Add `resolve` and `bearers` to every ambiguous entry (in place). Returns counts."""
    by = {r["slug"]: r for r in rows}
    kinds, written = relationship_graph(rows, pop)
    people_urls = {e["url"] for e in people}

    def eligible(r):
        if r.get("aliasOf") or r.get("living") or r.get("noindex") or not clean(r["name"]):
            return False
        if f"/people/{r['slug']}/" in living_addr:
            return False
        by_ = re.search(r"\b(1[0-9]{3}|20[0-9]{2})", str(r.get("born") or ""))
        if by_ and not str(r.get("died") or "").strip() and int(by_.group(1)) > year - RECENT_YEARS:
            return False
        return True

    row_names = {r["name"] for r in rows}
    stats = {"names": 0, "with_rules": 0, "rules": 0, "counter": 0, "bearers": 0, "unrowed": 0}
    for e in ambiguous:
        n = tokens_of(e["name"])
        bs = {r["slug"] for r in rows if not r.get("aliasOf") and is_subseq(n, tokens_of(r["name"]))}
        # a bearer the register holds that people.json does not (living and held-out people included): with one, no rule at all
        unrowed = [p for p in pop if is_subseq(n, tokens_of(p.name)) and p.name not in row_names]
        stats["names"] += 1
        stats["unrowed"] += len(unrowed)
        elig = [by[s] for s in sorted(bs) if eligible(by[s])]
        bearer_urls = sorted(f"/people/{r['slug']}/" for r in elig if f"/people/{r['slug']}/" not in people_urls)
        if bearer_urls:
            e["bearers"] = bearer_urls
            stats["bearers"] += len(bearer_urls)
        if unrowed:
            continue
        # relative -> the bearers it is related to, by any kind of relationship the data holds
        cand = {}
        for b in bs:
            for rr in kinds[b]:
                cand.setdefault(rr, set()).add(b)
            for rr in written[b]:
                cand.setdefault(rr, set()).add(b)
        rules = []
        for rs, bset in sorted(cand.items()):
            if len(bset) != 1 or rs in bs:
                continue
            b = next(iter(bset))
            if not (kinds[b].get(rs, set()) & RULE_KINDS):
                continue                                   # a parent, a child, a sibling or a mere mention can stop a rule, never make one
            ru = f"/people/{rs}/"
            if ru not in people_urls or ru in living_addr:
                continue
            rules.append({"near": ru, "url": f"/people/{b}/" if eligible(by[b]) else None})
        if rules:
            e["resolve"] = sorted(rules, key=lambda x: (x["url"] or "", x["near"]))
            stats["with_rules"] += 1
            stats["rules"] += len(rules)
            stats["counter"] += sum(1 for x in rules if x["url"] is None)
    return stats


def check_rules(index, rows, living_addr):
    """The generator's own test of what it wrote, recomputed from the rows by a second, plainer path: every rule's `near` is an indexed
    single-bearer person and the husband, wife or co-parent of `url`'s person, and of no other bearer of the name; `url` is indexed
    or listed in `bearers`, is not living; a counter-rule stands for a bearer who is not eligible. Returns the number of faults."""
    by = {r["slug"]: r for r in rows}
    people_urls = {e["url"] for e in index["people"]}
    slug = lambda u: u.strip("/").split("/")[-1]
    spouse_or_co = {s: set() for s in by}
    anyrel = {s: set() for s in by}
    for r in rows:
        for o in r.get("spouses") or []:
            if o.get("slug") in by:
                spouse_or_co[r["slug"]].add(o["slug"]); spouse_or_co[o["slug"]].add(r["slug"])
        f, m = (r.get("father") or {}).get("slug"), (r.get("mother") or {}).get("slug")
        if f in by and m in by:
            spouse_or_co[f].add(m); spouse_or_co[m].add(f)
        for k in ("father", "mother"):
            o = r.get(k)
            if o and o.get("slug") in by:
                anyrel[r["slug"]].add(o["slug"]); anyrel[o["slug"]].add(r["slug"])
        for k in ("spouses", "children", "siblings"):
            for o in r.get(k) or []:
                if o.get("slug") in by:
                    anyrel[r["slug"]].add(o["slug"]); anyrel[o["slug"]].add(r["slug"])
    bad = 0
    for e in index["ambiguous"]:
        n = tokens_of(e["name"])
        bs = {r["slug"] for r in rows if not r.get("aliasOf") and is_subseq(n, tokens_of(r["name"]))}
        for u in e.get("bearers") or []:
            if u in people_urls or u in living_addr or slug(u) not in bs:
                bad += 1
        for ru in e.get("resolve") or []:
            near, url = ru["near"], ru["url"]
            if near not in people_urls or near in living_addr or slug(near) in bs:
                bad += 1; continue
            if url is not None and (url in living_addr or not (url in people_urls or url in (e.get("bearers") or [])) or slug(url) not in bs):
                bad += 1; continue
            # the one bearer the relative leads to: through a spouse or co-parent edge, and no other bearer by any edge
            leads = {b for b in bs if slug(near) in anyrel[b] or slug(near) in spouse_or_co[b]}
            if url is not None:
                if slug(url) not in leads or leads != {slug(url)} or slug(near) not in spouse_or_co[slug(url)]:
                    bad += 1
            elif len(leads) != 1 or not (slug(near) in spouse_or_co[next(iter(leads))]):
                bad += 1
    return bad



# ---------------------------------------------------------------------------------------------------------------------------
# THE SAME-NAME PAGES (see the docstring). data/same-names.tsv (name, slug, links) names the shared names that have a page; --pick-same
# writes it from the built site; the index sends those names' unresolved links to /same-name/<slug>/; --same-data writes the pages' data.
# ---------------------------------------------------------------------------------------------------------------------------
STANDING_ORDER = {"connected": 0, "high": 1, "interest": 2, "unplaced": 3, "excluded": 4}


def read_same_picks():
    """data/same-names.tsv -> [(name, slug, links)]. A malformed line stops the build."""
    out = []
    if not SAME_PICK.exists():
        return out
    for n, line in enumerate(SAME_PICK.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#") or line.startswith("name\t"):
            continue
        cells = (line.split("\t") + ["", "", ""])[:3]
        name, slug, links = [c.strip() for c in cells]
        if not name or len(name.split()) < 2 or slug != slugify(name) or not links.isdigit():
            print(f"  FAIL  same-name  data/same-names.tsv line {n}: needs a two-word name, its slug and a link count")
            raise SystemExit(2)
        out.append((name, slug, int(links)))
    if len({s for _n, s, _l in out}) != len(out):
        print("  FAIL  same-name  data/same-names.tsv names a slug twice")
        raise SystemExit(2)
    return out


def same_old_url(name):
    return "/people/?q=" + name.replace(" ", "%20")


def apply_same_urls(ambiguous, picks):
    """Send the unresolved target of every picked shared name (accent forms included: they share the url) to its page. Returns the count of
    index entries changed. A pick that is not a shared name stops the run: the file is stale."""
    n = 0
    for name, slug, _links in picks:
        old = same_old_url(name)
        hit = [e for e in ambiguous if e["url"] == old]
        if not hit:
            print(f"  FAIL  same-name  data/same-names.tsv names a name that is not a shared name now (slug {slug}); run --pick-same")
            raise SystemExit(2)
        for e in hit:
            e["url"] = SAME_PREFIX + slug + "/"
            n += 1
    return n


def listed_bearer(r, year, living_addr):
    """A dead person with a page of their own, who may be listed: not an alias row, not living, not held out (noindex), not at an address
    the living list holds, and not born within a hundred years with no death recorded. Unlike `eligible` in resolve_rules this does not
    need a clean name: Alejandro M. Lerena is a bearer of Alejandro Lerena."""
    if r.get("aliasOf") or r.get("living") or r.get("noindex") or f"/people/{r['slug']}/" in living_addr:
        return False
    by_ = re.search(r"\b(1[0-9]{3}|20[0-9]{2})", str(r.get("born") or ""))
    return not (by_ and not str(r.get("died") or "").strip() and int(by_.group(1)) > year - RECENT_YEARS)


def year_text(raw):
    """'1865-10-08' -> '1865'; 'c.1877' or '1827c' -> 'about 1877'; no year -> ''."""
    raw = str(raw or "")
    m = re.search(r"\b(1[0-9]{3}|20[0-9]{2})", raw)
    if not m:
        return ""
    approx = bool(re.search(r"\bc\.?\s*\d|\d\s*c\b|\bcirca\b|\babout\b|\bby\b|\?", raw))
    return ("about " if approx else "") + m.group(1)


def source_line(raw, limit=170):
    """A one-line summary of the register's `source` cell: the markers removed, cut at the first ";", " - " or sentence end after 30 characters, or at
    `limit` characters on a word boundary, with an ellipsis when anything was left out. Only words the cell itself holds."""
    t = " ".join(re.sub(r"\*+", "", str(raw or "")).split())
    if len(t) <= 60:
        return t
    cut = len(t)
    for m in re.finditer(r";\s| - |\.\s(?=[A-Z])", t):
        if m.start() >= 30:
            cut = m.start()
            break
    cut = min(cut, limit)
    if cut >= len(t):
        return t
    head = t[:cut]
    if cut == limit and cut < len(t) and t[cut] != " " and " " in head:
        head = head[:head.rfind(" ")]
    return head.rstrip(" ,;:.") + " \u2026"


def same_name_data(rows, pop, year, living_addr, picks):
    """The data of the pages: for each picked name, every dead person with a page whose register name carries the name (its words, in order,
    the first word the same: the resolve rules' own bearer set), what the data says of them, and their dead relatives who have a page.
    Stops (exit 2) when any bearer of the name is living, held out or not asserted dead: the page counts people and must not be
    able to leave one out unseen."""
    by = {r["slug"]: r for r in rows}
    row_names = {r["name"] for r in rows}
    pages = []
    for name, slug, links in picks:
        n, k = tokens_of(name), key_of(name)
        hits = [r for r in rows if not r.get("aliasOf") and is_subseq(n, tokens_of(r["name"]))]
        withheld = [r for r in hits if not listed_bearer(r, year, living_addr)]
        unrowed = [p for p in pop if is_subseq(n, tokens_of(p.name)) and p.name not in row_names]
        if withheld or unrowed:
            print(f"  FAIL  same-name  a page for a shared name cannot be made while a bearer is living or held out "
                  f"({len(withheld)} in the people list, {len(unrowed)} outside it) - for one of the {len(picks)} names")
            raise SystemExit(2)

        def rel(o):
            t = by.get((o or {}).get("slug"))
            if t is None or not listed_bearer(t, year, living_addr) or o.get("living"):
                return None
            return {"slug": t["slug"], "name": t["name"], "tree": o.get("via") == "tree"}

        bearers = []
        for r in hits:
            c = clean(r["name"])
            exact = bool(c) and key_of(c) == k
            bearers.append({
                "slug": r["slug"], "name": r["name"], "exact": exact, "status": r["status"],
                "born": year_text(r.get("born")), "died": year_text(r.get("died")),
                "where": " · ".join(x for x in (r.get("place"), r.get("nationality")) if x and x != "-"),
                "source": source_line(r.get("source")),
                "father": rel(r.get("father")), "mother": rel(r.get("mother")),
                "spouses": [x for x in (rel(o) for o in (r.get("spouses") or [])) if x],
                "children": [x for x in (rel(o) for o in (r.get("children") or [])) if x],
            })
        bearers.sort(key=lambda b: (not b["exact"], STANDING_ORDER.get(b["status"], 9),
                                    int(b["born"][-4:]) if b["born"] else 9999, b["name"].casefold()))
        pages.append({"name": name, "slug": slug, "links": links, "exact": sum(1 for b in bearers if b["exact"]),
                      "bearers": bearers})
    return {"note": "Generated by tools/run-autolink.py --same-data from site/src/data/people.json and data/same-names.tsv. Never edit by hand.",
            "pages": pages}


def pick_same(index, top):
    """Count the data-autolink="search" links in the built site by the name they carry (folded: case and accent) and write the `top`
    commonest to data/same-names.tsv. Counted by link text, so it gives the same answer before and after the links are redirected."""
    counts = {}
    for d, ds, fs in os.walk(SITE / "dist"):
        ds[:] = [x for x in ds if x not in ("node_modules", "_astro")]
        for f in fs:
            if not f.endswith(".html"):
                continue
            page = (pathlib.Path(d) / f).read_text(encoding="utf-8")
            for m in re.finditer(r'<a href="[^"]*" data-autolink="search"[^>]*>(.*?)</a>', page, re.S):
                t = " ".join(_html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).split())
                counts[key_of(t)] = counts.get(key_of(t), 0) + 1
    if not counts:
        print("  --    same-name  not run: no data-autolink=\"search\" link in site/dist (build first)")
        raise SystemExit(2)
    names = {}
    for e in index["ambiguous"]:
        k = key_of(e["name"])
        if k not in names or (e["name"] == ascii_fold(e["name"]) and names[k] != ascii_fold(names[k])):
            names[k] = e["name"]
    ranked = sorted(((c, names[k]) for k, c in counts.items() if k in names), key=lambda x: (-x[0], x[1].casefold()))[:top]
    lines = ["# The shared names that have a /same-name/<slug>/ page: the commonest unresolved shared-name links of the built site.",
             "# Written by `python3 tools/run-autolink.py --pick-same [--top N]` (N=%d); the links column is the count then. The name is the ascii form;" % SAME_TOP,
             "# the accent forms and every other spelling of the name go to the same page. Edit by hand only to drop a name.",
             "name\tslug\tlinks"]
    lines += [f"{nm}\t{slugify(nm)}\t{c}" for c, nm in ranked]
    SAME_PICK.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return ranked


def build(write=True):
    """Return (index, living_terms_list, living_addresses, stats). Raises SystemExit(2) when it cannot look."""
    try:
        rows = json.loads(PEOPLE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        print("  --    names      not run: site/src/data/people.json is missing or unreadable")
        raise SystemExit(2)
    if not rows:
        print("  --    names      not run: people.json is empty")
        raise SystemExit(2)
    pop, lr, year = L.population(ROOT)
    nl, nladdr, n_liv = living_terms(pop, rows)
    if n_liv == 0:
        print("  --    names      not run: the reckoning found nobody living, so there is no living list to check against. "
              "That is itself wrong for this archive")
        raise SystemExit(2)
    living_keys = {key_of(n) for n in nl}
    # every bearer of a name, living and held-out included: keyed by the cleaned name folded to ascii lower case
    bearers = {}                       # key -> {raw register strings}
    for p in pop:
        c = clean(p.name)
        if c:
            bearers.setdefault(key_of(c), set()).add(p.name)
    for r in rows:
        c = clean(r["name"])
        if c:
            bearers.setdefault(key_of(c), set()).add(r["name"])
    tainted = {key_of(p.name) for p in pop if (p.living or getattr(p, "held", False)) and clean(p.name)}
    tainted |= {key_of(clean(p.name)) for p in pop if (p.living or getattr(p, "held", False)) and clean(p.name)}

    # indexable, dead, ordinary rows
    ok = []
    skipped = {"alias row": 0, "living": 0, "noindex": 0, "recent": 0, "no clean name": 0}
    for r in rows:
        if r.get("aliasOf"):
            skipped["alias row"] += 1; continue
        if r.get("living"):
            skipped["living"] += 1; continue
        if r.get("noindex"):
            skipped["noindex"] += 1; continue
        by = re.search(r"\b(1[0-9]{3}|20[0-9]{2})", str(r.get("born") or ""))
        if by and not str(r.get("died") or "").strip() and int(by.group(1)) > year - RECENT_YEARS:
            skipped["recent"] += 1; continue
        c = clean(r["name"])
        if not c:
            skipped["no clean name"] += 1; continue
        ok.append((r, c))

    people, ambiguous = [], []
    stats_prefix = []
    by_key = {}
    for r, c in ok:
        by_key.setdefault(key_of(c), []).append((r, c))
    af = accent_forms()
    owned = {}                         # name key -> addresses claiming it (names and aliases)
    for k, lst in by_key.items():
        if k in living_keys or k in tainted:
            continue
        raws = bearers.get(k, set())
        if len(lst) == 1 and len(raws) == 1:
            r, c = lst[0]
            people.append({"name": display(c), "aliases": [], "url": f"/people/{r['slug']}/", "_key": k})
        elif len(lst) >= 2 and len(raws) >= 2 and len(raws) == len({r["name"] for r, _ in lst}):
            # several people, every one of them a dead person with a page: send to the people list filtered on the name
            needle = display(lst[0][1])
            if all(needle.casefold() in r["name"].casefold() for r, _ in lst):
                ambiguous.append({"name": needle, "url": "/people/?q=" + needle.replace(" ", "%20"), "_key": k})
    # A NAME THAT IS THE START OF ANOTHER PERSON'S LONGER NAME is not one person's: "Arturo Lerena" is the Arturo of the register and
    # also the first two words of "Arturo Lerena Garcia", and a page that writes "Arturo Lerena" may mean either. It goes to the
    # people list filtered on the name, like any shared name (found 18 October 2026 by sampling the links: "Arturo Lerena's parents"
    # on /argentina/ was linked to the wrong Arturo). Living and held-out people count: their longer names make it shared too.
    longer = set()
    for k_ in list(bearers):
        longer.add(k_)
    def starts_another(k, slug):
        return any(o.startswith(k + " ") for o in longer)
    # A GIVEN NAME AND THE FAMILY'S OWN SURNAME, NOTHING ELSE ("Juan Lerena", "Socorro Lerena"), is shared too. The register holds
    # one row of that name, but the family has a dozen Juans and the pages write "Juan Lerena" for several of them (found by sampling:
    # the one row, "Child of Felisa, arrived 1923", was being linked from a dispensation of 1894). It goes to the people list filtered
    # on the name, where a reader sees them all.
    still = []
    for e in people:
        w = e["name"].split()
        if starts_another(e["_key"], e["url"].split("/")[2]) or (len(w) == 2 and ascii_fold(w[1]).casefold() in FAMILY_SURNAMES):
            needle = e["name"]
            ambiguous.append({"name": needle, "url": "/people/?q=" + needle.replace(" ", "%20"), "_key": e["_key"]})
            stats_prefix.append(e["name"])
        else:
            still.append(e)
    people[:] = still
    for e in people + ambiguous:
        owned.setdefault(key_of(e["name"]), set()).add(e["url"])
    prov = {}                          # (address, alias as written) -> "accent" | "short" | "stated" | "fold"

    def add_alias(e, al, kind):
        """Add one alias to an entry unless a living person, another entry or the entry itself already holds that key."""
        k = key_of(al)
        if len(al.split()) < 2 or k in living_keys or k in tainted or k in {key_of(x) for x in nl}:
            return False
        if k in owned and owned[k] != {e["url"]}:
            return False
        if al == e["name"] or al in e["aliases"]:
            return False
        e["aliases"].append(al)
        owned.setdefault(k, set()).add(e["url"])
        prov[(e["url"], al)] = kind
        return True

    # (1) the folds the archive's own namefold.json holds for a word of the name (Fernandez -> Fernandez with an acute)
    for e in people:
        words = e["name"].split(" ")
        variants = [[]]
        for w in words:
            forms = [w]
            for acc in sorted(af.get(ascii_fold(w).casefold(), ())):
                forms.append(acc if not w[:1].isupper() else acc[:1].upper() + acc[1:])
            variants = [v + [f] for v in variants for f in forms][:64]
        for v in variants:
            al = " ".join(v)
            if key_of(al) == key_of(e["name"]) and al != e["name"] and not any(
                    key_of(al) == key_of(o["name"]) and o is not e for o in people + ambiguous):
                add_alias(e, al, "fold")
    # (2) short forms: one person's, and nobody else's whole name or short form
    claims = {}                        # key -> {identity}
    ident = lambda slug, name: slug or ("name:" + name)
    for r in rows:
        who = ident(r.get("slug"), r["name"])
        c = clean(r["name"])
        if c:
            claims.setdefault(key_of(c), set()).add(who)
        for f in short_forms(r["name"]):
            claims.setdefault(key_of(f), set()).add(who)
    for p in pop:
        who = ident(p.slug, p.name)
        c = clean(p.name)
        if c:
            claims.setdefault(key_of(c), set()).add(who)
        for f in short_forms(p.name):
            claims.setdefault(key_of(f), set()).add(who)
    by_slug_row = {r["slug"]: r for r in rows}
    n_short = 0
    for e in people:
        slug = e["url"].split("/")[2]
        r = by_slug_row.get(slug)
        if r is None:
            continue
        for f in short_forms(r["name"]):
            if claims.get(key_of(f)) == {slug} and not any(o.startswith(key_of(f) + " ") and o != key_of(e["name"]) and not o.startswith(key_of(e["name"])) for o in longer) and add_alias(e, f, "short"):
                n_short += 1
    # (3) forms the data states for a person, in data/names-aliases.tsv (also gives a person whose register name carries an
    #     initial or a bracket an entry of their own)
    n_stated = 0
    for alias, who, slug, basis in stated_aliases(rows):
        r = by_slug_row.get(slug)
        if r is None or r.get("living") or r.get("noindex") or r.get("aliasOf"):
            continue
        k = key_of(alias)
        if k in living_keys or k in tainted:
            continue
        e = next((x for x in people if x["url"] == f"/people/{slug}/"), None)
        if e is None:
            if k in owned:
                continue
            e = {"name": alias, "aliases": [], "url": f"/people/{slug}/", "_key": k}
            people.append(e)
            owned.setdefault(k, set()).add(e["url"])
            prov[(e["url"], alias)] = "stated"
            n_stated += 1
        elif add_alias(e, alias, "stated"):
            n_stated += 1
    # (4) accent forms of every name and alias the archive's committed text writes with accents
    acc = corpus_accents()
    for e in people:
        for base in [e["name"]] + list(e["aliases"]):
            for v in accent_variants(base, acc):
                if key_of(v) == key_of(base) and not any(
                        key_of(v) == key_of(o["name"]) and o["url"] != e["url"] for o in people + ambiguous):
                    add_alias(e, v, "accent")
    amb_extra = []
    for e in ambiguous:
        for v in accent_variants(e["name"], acc):
            if key_of(v) == key_of(e["name"]) and key_of(v) not in living_keys:
                amb_extra.append({"name": v, "url": e["url"]})
                prov[(e["url"], v)] = "accent"
    ambiguous += amb_extra
    same_n = apply_same_urls(ambiguous, read_same_picks())
    for e in people:
        e["aliases"] = sorted(set(e["aliases"]))
    for e in people + ambiguous:
        e.pop("_key", None)
    people.sort(key=lambda e: e["url"])
    ambiguous.sort(key=lambda e: e["name"].casefold())
    for e in ambiguous:
        e.pop("aliases", None)
    rstats = resolve_rules(ambiguous, people, rows, pop, year, set(nladdr))
    index = {"note": "Generated by tools/run-autolink.py from site/src/data/people.json. Names that already have a public page. "
                     "Never edit by hand.", "people": people, "ambiguous": ambiguous,
             "labels": {"shared": SHARED_LABEL}, "nearWindow": NEAR_WINDOW}
    kinds = {}
    for v in prov.values():
        kinds[v] = kinds.get(v, 0) + 1
    stats = {"people": len(people), "ambiguous": len(ambiguous), "aliases": sum(len(e["aliases"]) for e in people),
             "kinds": kinds, "stated": n_stated, "living_terms": len(nl), "living_people": n_liv, "skipped": skipped,
             "prefix_ambiguous": len(stats_prefix), "_prov": prov, "resolve": rstats, "same": same_n}
    if write:
        INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        lp = living_path()
        lp.parent.mkdir(parents=True, exist_ok=True)
        lp.write_text(json.dumps({"names": nl, "addresses": nladdr}, ensure_ascii=False), encoding="utf-8")
        try:
            os.chmod(lp, 0o600)
        except OSError:
            pass
    return index, nl, nladdr, stats


def self_check(index, nl, nladdr, rows, prov):
    """Refuse an index the generator itself cannot stand behind (the kit checks the living overlap again). Every alias must be
    of a kind the generator may make and must pass that kind's own test, recomputed here from the register."""
    by_slug = {r["slug"]: r for r in rows}
    stated = {(f"/people/{slug}/", key_of(alias)) for alias, _who, slug, _b in stated_aliases(rows)}
    bad = 0
    lk = {key_of(n) for n in nl}
    la = set(nladdr)
    for e in index["people"]:
        slug = e["url"].split("/")[2]
        r = by_slug.get(slug)
        if r is None or r.get("living") or r.get("noindex") or r.get("aliasOf"):
            bad += 1
            continue
        nk = key_of(e["name"])
        if (e["url"], nk) not in stated and nk != key_of(clean(r["name"])):
            bad += 1
        if nk in lk or e["url"] in la:
            bad += 1
        shorts = {key_of(f) for f in short_forms(r["name"])}
        base = {nk} | {key_of(a) for a in e["aliases"] if prov.get((e["url"], a)) in ("short", "stated")}
        for a in e["aliases"]:
            k = key_of(a)
            kind = prov.get((e["url"], a))
            ok = {"short": k in shorts, "stated": (e["url"], k) in stated}.get(kind, kind in ("fold", "accent") and k in base)
            if not ok or k in lk:
                bad += 1
    for e in index["ambiguous"]:
        if key_of(e["name"]) in lk:
            bad += 1
    bad += check_rules(index, rows, la)
    return bad


# ---------------------------------------------------------------------------------------------------------------------------
# THE GUARD: a name that is the tail or the head of a LONGER name is not linked.
#
# The kit matches whole words and stops at nothing else, so "Juan Carlos Lerena" inside "Richardo Juan Carlos Lerena" (the
# son's name, written with a spelling this archive has no page for) was going to be linked to the father. Both strings are a
# whole-word match; only the neighbouring word says they are different people. The kit has no option for this, so this
# archive does it: BEFORE the kit runs, every place the kit WOULD link is read in its context (tags that flow inline are
# looked through, tags that break a line or a cell are not), and a mention directly beside another name-like word
# (Title Case beside Title Case, CAPITALS beside CAPITALS, a "de"/"del"/"y" and a surname after it, an initial before it) is
# wrapped in <span data-no-autolink>, the kit's own opt-out. The kit then skips it, the gate does not count it, a later
# mention of the same person in the section is linked instead, and a second run finds nothing to do. Nothing is ever
# unwrapped, and no text moves.
# ---------------------------------------------------------------------------------------------------------------------------
BLOCK_TAGS = (r"td|th|tr|p|li|ul|ol|div|section|article|br|h[1-6]|table|thead|tbody|tfoot|caption|dt|dd|dl|figure|"
              r"figcaption|blockquote|details|summary|header|footer|nav|main|aside|label|option|select|button|hr|pre|"
              r"form|fieldset|legend")
BLOCK_RX = re.compile(r"</?(?:%s)\b[^>]*>" % BLOCK_TAGS, re.I)
ANY_TAG = re.compile(r"<!--.*?-->|<[^>]*>", re.S)
HONORIFIC = {"don", "dona", "dn", "dr", "sr", "sra", "srta", "mr", "mrs", "ms", "miss", "capt", "captain", "capitan", "general",
             "gen", "padre", "father", "fr", "rev", "fray", "sir", "lady", "senor", "senora", "dª", "da", "d.a", "d.", "dña",
             "exmo", "doctor", "the", "d.n", "dn.", "d.ª", "dña", "dñ", "dna", "d.", "d"}
# function words and the commonest capitalised sentence openers: beside a name they are not part of it
STOP = set("""a an the and or but nor of in on at by to for with from as is was were be been are am has have had having not no
so if that this these those it its his her their he she they we you i who whom whose which what when where while after before
during since until about into over under than then also both either neither only same each other another one two three four
five six seven eight nine ten first second third last next both all any some none many most more less few several every
wife husband widow widower son daughter mother brother sister uncle aunt cousin child children parents parent family
married marries marry born died dies buried baptised baptized named called known documented noted found read see seen says
said wrote writes written signed witnessed witness witnesses godfather godmother godparent godparents bride groom
january february march april june july august september october november december
monday tuesday wednesday thursday friday saturday sunday
y e o u con por para sin sobre entre desde hasta segun hijo hija hijos padres esposa esposo viuda viudo casado casada
nacio murio bautizado bautizada testigo testigos padrino madrina abuelo abuela abuelos nieto nieta
montevideo uruguay argentina canelones buenos aires fe santa san entre rios devon
bideford africa south cape town johannesburg transvaal england britain london brisbane australia chile spain italy
mayo las les los del""".split())
PARTICLE = {"de", "del", "la", "las", "los", "di", "da", "du", "van", "von", "le", "el"}


def _flat(s):
    s = BLOCK_RX.sub("\x00", s)
    return _html.unescape(ANY_TAG.sub("", s)).replace("\xa0", " ")


def _style(w):
    letters = [c for c in w if c.isalpha()]
    if len(letters) >= 2 and all(c.isupper() for c in letters):
        return "upper"
    return "title" if w[:1].isupper() else "lower"


def _name_like(tok, name_styles):
    """A capitalised word that could be part of the same name. A word of another case style (a word in capitals beside a
    Title Case name, the register's AND / WAS / OF) is the sentence, not the name."""
    core = tok.strip("\"'“”‘’«»()[]*,;:!?–—-")
    if not core or not core[0].isalpha() or not core[0].isupper():
        return False
    if any(c.isdigit() for c in core):
        return False
    base = ascii_fold(core).casefold().rstrip(".")
    if base in STOP or base in HONORIFIC:
        return False
    st = _style(core)
    if st == "title":
        return "title" in name_styles or "mixed" in name_styles
    return "upper" in name_styles or "mixed" in name_styles


def _styles(text):
    sts = {_style(w) for w in text.split() if w.lower() not in PARTICLE and any(c.isalpha() for c in w)}
    out = set()
    if "upper" in sts and "title" in sts:
        out |= {"mixed", "title", "upper"}
    else:
        out |= {s for s in sts if s != "lower"}
    return out


def beside_a_longer_name(page, a, b):
    """True when the text page[a:b] directly continues into another name-like word, before or after."""
    text = _flat(page[a:b])
    styles = _styles(text)
    before = _flat(page[max(0, a - 600):a])
    after = _flat(page[b:b + 600])
    if before and not before.endswith("\x00"):
        m = re.search(r"(\S+)[ \t\r\n]+$", before)
        if m:
            tok = m.group(1)
            if re.fullmatch(r"[A-CE-Z]\.", tok):                # (D. is Don, not an initial)
                return True                                    # "J. Pedro Lerena": an initial before the name
            if tok[-1].isalnum() or tok[-1] in "\"'”’)":
                if _name_like(tok, styles):
                    return True
    m = re.match(r"^[ \t\r\n]+(\S+)(?:[ \t\r\n]+(\S+))?(?:[ \t\r\n]+(\S+))?", after)
    if m:
        t1, t2, t3 = m.group(1), m.group(2), m.group(3)
        if t1 and t1.lstrip("[(")[:1].isalpha():
            t1 = t1.lstrip("[(")
            low = ascii_fold(t1).casefold().rstrip(",.;:")
            if low in PARTICLE and t2:                         # "Maria Lerena de Martinez", "del Rio", "de la Cruz"
                nxt = t3 if (ascii_fold(t2).casefold() in PARTICLE and t3) else t2
                core = nxt.strip("\"'“”()[]*,;:!?")
                if core[:1].isalpha() and core[:1].isupper():
                    return True
            elif low == "y" and t2:                            # "Luis Lerena y Fernandez" (a surname) but not "... y Julia Salvanach"
                core = t2.strip("\"'“”()[]*,;:!?")
                if core[:1].isalpha() and core[:1].isupper() and ascii_fold(core).casefold() not in GIVEN_NAMES:
                    return True
            elif _name_like(t1, styles):
                return True
    return False


GIVEN_NAMES = set()


def load_kit_module():
    spec = importlib.util.spec_from_file_location("kit_autolink", str(KIT / "autolink.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(KIT))
    spec.loader.exec_module(mod)
    return mod


def guard_pass(dist, rows, living_file):
    """Wrap every mention the kit is about to link that sits beside a longer name. Returns (wrapped, pages)."""
    A = load_kit_module()
    for r in rows:
        c = clean(r["name"])
        if c:
            GIVEN_NAMES.add(ascii_fold(c.split(" ")[0]).casefold())
    ln, lu = A.load_living(str(living_file))
    idx = A.load_index(str(INDEX), ln, lu, ["/people/", "/who/", SAME_PREFIX], 2)
    wrapped = pages = 0
    for rounds in range(8):
        again = False
        for path in A.html_pages(str(dist)):
            page = A.read_page(path)
            sc = A.scan_html(page, idx, "main")
            if not sc.scope_seen or not sc.inserts:
                continue
            bad = [(a, b) for (a, b, _u, _k) in sc.inserts if beside_a_longer_name(page, a, b)]
            if not bad:
                continue
            out, last = [], 0
            for (a, b) in sorted(bad):
                out += [page[last:a], "<span data-no-autolink>", page[a:b], "</span>"]
                last = b
            out.append(page[last:])
            A.write_page(path, "".join(out))
            wrapped += len(bad)
            pages += 1
            again = True
        if not again:
            break
    return wrapped, pages


def merged_standard_config(rows):
    """site/standard.json plus, when it says names.surname_words_from_register, every word the register writes in capitals (its mark
    of a surname) as names.surname_words. The kit takes every word but the last of an index name for a GIVEN name, so a person
    named Given SURNAME Surname would otherwise teach the gate that SURNAME is a given name. Made from people.json (committed), written
    next to standard.json so its relative paths hold, removed after the run."""
    cfg = json.loads((SITE / "standard.json").read_text(encoding="utf-8"))
    n = cfg.setdefault("names", {})
    if n.get("surname_words_from_register"):
        caps = set(n.get("surname_words") or [])
        for r in rows:
            if r.get("living") or r.get("noindex") or r.get("aliasOf"):
                continue
            s = re.sub(r"\(.*?\)|\[.*?\]", " ", str(r.get("name") or ""))
            for w in s.split():
                if len(w) >= 3 and w == w.upper() and w.casefold() not in PARTICLES and WORD.match(w):
                    caps.add(ascii_fold(w).casefold())
        n["surname_words"] = sorted(caps)
    out = SITE / ".standard-merged.json"
    out.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--write-floor", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--index-only", action="store_true")
    ap.add_argument("--standard", action="store_true", help="the kit's checkstandard.py against site/.standardfloor.json (the last step of the build)")
    ap.add_argument("--write-standard-floor", action="store_true", help="lock the standard's current counts in (refuses while anything rose)")
    ap.add_argument("--pick-same", action="store_true", help="write data/same-names.tsv from the unresolved links of the built site")
    ap.add_argument("--top", type=int, default=SAME_TOP, help="with --pick-same: how many names (default %d)" % SAME_TOP)
    ap.add_argument("--same-data", action="store_true", help="write site/src/data/same-name.json (before astro builds the pages)")
    ap.add_argument("--dist", default="dist", help="relative to site/")
    a = ap.parse_args()
    if not (KIT / "autolink.py").exists():
        print("  --    names      not run: the pinned kit has no kit/tools/autolink.py - the pin must be fcdfefe or later "
              "and `npm install` run in site/")
        return 2
    if a.pick_same:
        # the index as it stands: the names several people share (a name already sent to a page is found by its folded text)
        index, _nl, _nladdr, _st = build(write=False)
        ranked = pick_same(index, a.top)
        print(f"  same-name: {len(ranked)} names picked, {sum(c for c, _ in ranked)} of the unresolved links: " + ", ".join(str(c) for c, _ in ranked))
        return 0
    index, nl, nladdr, st = build(write=not a.same_data)
    rows = json.loads(PEOPLE.read_text(encoding="utf-8"))
    if a.same_data:
        pop, _lr, year = L.population(ROOT)
        data = same_name_data(rows, pop, year, set(nladdr), read_same_picks())
        SAME_DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"  same-name: {len(data['pages'])} page(s), {sum(len(p['bearers']) for p in data['pages'])} bearer(s) listed")
        return 0
    bad = self_check(index, nl, nladdr, rows, st["_prov"])
    sk = ", ".join(f"{v} {k}" for k, v in st["skipped"].items() if v)
    kinds = ", ".join(f"{v} {k}" for k, v in sorted(st["kinds"].items()))
    print(f"  names: {st['people']} people, {st['ambiguous']} ambiguous ({st['prefix_ambiguous']} because the name starts a longer one or is a given name and the family surname), {st['aliases']} aliases ({kinds}); "
          f"{st['living_people']} living or held-out person(s) in the living list ({st['living_terms']} terms), kept outside the "
          f"repository; rows not indexed: {sk}")
    rs = st["resolve"]
    print(f"  names: {rs['rules']} resolve rule(s) on {rs['with_rules']} of {rs['names']} shared names (spouse and co-parent only; {rs['counter']} counter-rule(s)), "
          f"{rs['bearers']} paged bearer(s) listed")
    if bad:
        print(f"  FAIL  names      {bad} index entr{'y' if bad == 1 else 'ies'} the generator cannot stand behind")
        return 1
    if a.index_only:
        return 0
    dist = SITE / a.dist
    if a.standard or a.write_standard_floor:
        cfg_path = merged_standard_config(rows)
        cmd = [sys.executable, str(KIT / "checkstandard.py"), "--dist", str(dist), "--index", str(INDEX), "--config", str(cfg_path),
               "--living", str(living_path()), "--floor", str(SITE / ".standardfloor.json"), "--strict-config"]
        if a.write_standard_floor:
            cmd.append("--write-floor")
        try:
            return subprocess.run(cmd, cwd=SITE).returncode
        finally:
            try:
                cfg_path.unlink()
            except OSError:
                pass
    common = ["--dist", str(dist), "--index", str(INDEX), "--living", str(living_path()),
              "--allow-prefix", "/people/", "--allow-prefix", "/who/", "--allow-prefix", SAME_PREFIX]
    if a.gate or a.write_floor:
        cmd = [sys.executable, str(KIT / "checklinks.py")] + common + ["--floor", str(FLOOR)]
        if a.write_floor:
            cmd.append("--write-floor")
    else:
        if not a.check:
            wrapped, gpages = guard_pass(dist, rows, living_path())
            print(f"  guard: {wrapped} mention(s) beside a longer name left unlinked on {gpages} page(s)")
        cmd = [sys.executable, str(KIT / "autolink.py")] + common + (["--check"] if a.check else [])
    return subprocess.run(cmd, cwd=SITE).returncode


if __name__ == "__main__":
    sys.exit(main())
