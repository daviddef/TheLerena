#!/usr/bin/env python3
"""Link the names on the built pages to their people (the kit's autolink.py), and gate the number.

    python3 tools/run-autolink.py                 build the index and the living list, then link site/dist
    python3 tools/run-autolink.py --gate          the kit's checklinks.py against site/.linkfloor.json (last step of the build)
    python3 tools/run-autolink.py --write-floor   lock the current counts in as the ceiling (refuses while anything rose)
    python3 tools/run-autolink.py --check         change nothing; exit 1 if a run would
    python3 tools/run-autolink.py --index-only    write site/src/data/names-index.json and the living list, run nothing else

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

THE LIVING LIST (written OUTSIDE the repository, $AUTOLINK_LIVING or ~/.local/state/lerena/autolink-living.json).
  Built from tools/livingcheck.py, the independent reckoning every living gate here uses (the register, the relations list,
  the roster, the held-out ids, the estate's one rule in the kit's living_rule.py), plus every row people.json itself marks
  living. Each living or held-out person contributes their name, the forms a sentence might use for them, and their
  addresses. Nothing in it is private DATA: it is derived from tracked files only, so CI can build it, and CI does.

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


def slugify(s):
    return re.sub(r"[^A-Za-z0-9]+", "-", ascii_fold(str(s or ""))).strip("-").lower()


def clean(raw):
    """The name a sentence would use for this register string, or "" when no honest name can be made of it."""
    s = re.sub(r"\(.*?\)", " ", str(raw or ""))
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
    # accent aliases, and only where nothing else already owns that spelling
    for e in people + ambiguous:
        owned.setdefault(key_of(e["name"]), set()).add(e["url"])
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
            if al == e["name"]:
                continue
            ak = al.casefold()
            if ak in {x.casefold() for x in nl} or key_of(al) in living_keys:
                continue
            # the folded spelling is the person's own name already; an accent form may not be another person's name
            if any(key_of(al) == key_of(o["name"]) and o is not e for o in people + ambiguous):
                continue
            e["aliases"].append(al)
        e["aliases"] = sorted(set(e["aliases"]))
    for e in people + ambiguous:
        e.pop("_key", None)
    people.sort(key=lambda e: e["url"])
    ambiguous.sort(key=lambda e: e["name"].casefold())
    for e in ambiguous:
        e.pop("aliases", None)
    index = {"note": "Generated by tools/run-autolink.py from site/src/data/people.json. Names that already have a public page. "
                     "Never edit by hand.", "people": people, "ambiguous": ambiguous}
    stats = {"people": len(people), "ambiguous": len(ambiguous), "aliases": sum(len(e["aliases"]) for e in people),
             "living_terms": len(nl), "living_people": n_liv, "skipped": skipped}
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


def self_check(index, nl, nladdr, rows):
    """Refuse an index the generator itself cannot stand behind (the kit checks the living overlap again)."""
    by_slug = {r["slug"]: r for r in rows}
    bad = 0
    lk = {key_of(n) for n in nl}
    la = set(nladdr)
    for e in index["people"]:
        slug = e["url"].split("/")[2]
        r = by_slug.get(slug)
        if r is None or r.get("living") or r.get("noindex") or r.get("aliasOf"):
            bad += 1
        elif key_of(clean(r["name"])) != key_of(e["name"]):
            bad += 1
        if key_of(e["name"]) in lk or e["url"] in la:
            bad += 1
        for a in e["aliases"]:
            if key_of(a) != key_of(e["name"]) or key_of(a) in lk:
                bad += 1
    for e in index["ambiguous"]:
        if key_of(e["name"]) in lk:
            bad += 1
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
        if t1 and t1[0].isalpha():
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
    idx = A.load_index(str(INDEX), ln, lu, ["/people/", "/who/"], 2)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--write-floor", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--index-only", action="store_true")
    ap.add_argument("--dist", default="dist", help="relative to site/")
    a = ap.parse_args()
    if not (KIT / "autolink.py").exists():
        print("  --    names      not run: the pinned kit has no kit/tools/autolink.py - the pin must be fcdfefe or later "
              "and `npm install` run in site/")
        return 2
    index, nl, nladdr, st = build(write=True)
    rows = json.loads(PEOPLE.read_text(encoding="utf-8"))
    bad = self_check(index, nl, nladdr, rows)
    sk = ", ".join(f"{v} {k}" for k, v in st["skipped"].items() if v)
    print(f"  names: {st['people']} people, {st['ambiguous']} ambiguous, {st['aliases']} aliases; "
          f"{st['living_people']} living or held-out person(s) in the living list ({st['living_terms']} terms), kept outside the "
          f"repository; rows not indexed: {sk}")
    if bad:
        print(f"  FAIL  names      {bad} index entr{'y' if bad == 1 else 'ies'} the generator cannot stand behind")
        return 1
    if a.index_only:
        return 0
    dist = SITE / a.dist
    common = ["--dist", str(dist), "--index", str(INDEX), "--living", str(living_path()),
              "--allow-prefix", "/people/", "--allow-prefix", "/who/"]
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
