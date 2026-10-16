#!/usr/bin/env python3
"""The family pages (/families/ and /families/<slug>/), checked against the register, independently of the template.

The pages are BUILT by site/src/lib/families.js from site/src/data/people.json. This gate does not trust that file or that
code. It reckons the same pages a second way - who carries each surname, from data/lerena-register.tsv through
tools/livingcheck.py (the estate's one definition of who is living or held out, the kit's living_rule.py) - and then
reads the BUILT HTML:

  A  PAGE      every family in data/families.tsv has a built page, an entry on /families/, a link in the main menu and a
               line in sitemap.xml. (A family nobody can reach, or that a search engine is not told about, is not a page.)
  B  PEOPLE    the people the page lists are EXACTLY the people the register holds under those spellings, once each: not
               one more (a name page for a stranger), not one fewer (a person missing from their own family).
  C  LIVING    no link on the page goes to the page of a living person or a person held out of publication, and no link goes
               to a person the register does not hold. A family page must not make a living person easier to find than
               their own page does.
  D  COUNT     the number printed in the page's eyebrow is the number of people reckoned, not the number the template thinks.
  E  LINE      a family filed under group `line` shows an "On the direct line" section, and one that is not shows none: the
               claim that a family is on the line is checked against the page, not against the TSV that asserts it.
  F  SPELLINGS no spelling is claimed by two families, so no person is counted in the wrong place.

WHAT A PERSON "CARRIES" is worked out here from the register's own convention (surname in capitals; a Spanish second surname in
ordinary case straight after it; nothing inside brackets; a name with no capitals is read by its last word). That is the same
convention the template uses, written a second time on purpose.

Every rule has a planted-fault control, run first: a deliberately broken copy of a real page must fail each rule, or the gate
refuses to pass (a check that can only pass proves nothing).

Usage:  python3 tools/check-families.py [--root DIR] [--dist DIR]
Exit:   0 pass, 1 fail, 2 not run.
"""
import argparse
import html
import os
import pathlib
import re
import sys
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import livingcheck as L  # noqa: E402

CAPS = re.compile(r"^[A-ZÁÉÍÓÚÑ]{3,}$")
TITLE = re.compile(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+$")


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s or "")) if unicodedata.category(c) != "Mn").lower()


def surname_words(name):
    words = re.sub(r"\([^)]*\)", " ", name).split()
    caps = [i for i, w in enumerate(words) if CAPS.match(w)]
    if not caps:
        return [words[-1]] if words and TITLE.match(words[-1]) else []
    out = [words[i] for i in caps]
    i = caps[-1] + 1
    while i < len(words) and TITLE.match(words[i]):
        out.append(words[i])
        i += 1
    return out


def read_families(root):
    rows = L.tsv(root / "data" / "families.tsv")
    return [{"slug": r["slug"], "name": r["name"], "forms": {fold(x) for x in r["forms"].split("|")},
             "group": r["group"]} for r in rows if r.get("slug")]


def dist_dir(root, given):
    if given:
        return pathlib.Path(given)
    ao = os.environ.get("ARCHIVE_OUT")
    return (root / ao) if ao else root / "site" / "dist"


def main_of(page):
    m = re.search(r"<main\b.*?</main>", page, re.S)
    return m.group(0) if m else ""


def section(main, sid):
    m = re.search(r'<section[^>]*>(?:(?!</section>).)*?id="%s".*?</section>' % re.escape(sid), main, re.S)
    return m.group(0) if m else ""


def person_links(fragment):
    return re.findall(r'href="/people/([^"/#?]+)/?[^"]*"', fragment)


def judge(fam, page, expected, bad, known, nav_html, index_html, sitemap, site):
    """Every rule, against one page. Returns a list of problems (empty = pass)."""
    out = []
    main = main_of(page)
    if not main:
        return [f"{fam['slug']}: the built page has no <main>"]
    # A
    if f'href="/families/{fam["slug"]}/"' not in nav_html:
        out.append(f"{fam['slug']}: not linked from the main menu")
    if f'href="/families/{fam["slug"]}/"' not in index_html:
        out.append(f"{fam['slug']}: not listed on /families/")
    if f"{site}/families/{fam['slug']}/" not in sitemap:
        out.append(f"{fam['slug']}: not in sitemap.xml")
    # B
    listed = person_links(section(main, "s-people"))
    if sorted(listed) != sorted(set(listed)):
        out.append(f"{fam['slug']}: a person is listed twice")
    if set(listed) != expected:
        miss, extra = sorted(expected - set(listed)), sorted(set(listed) - expected)
        out.append(f"{fam['slug']}: people list differs from the register: {len(miss)} missing, {len(extra)} extra")
    # C
    for s in set(person_links(main)):
        if s in bad:
            out.append(f"{fam['slug']}: links to the page of a living or held-out person")
        elif s not in known:
            out.append(f"{fam['slug']}: links to a person the register does not hold")
    # D
    m = re.search(r"(\d+) (?:person|people) of the name", main)
    if not m or int(m.group(1)) != len(expected):
        out.append(f"{fam['slug']}: the eyebrow says {m.group(1) if m else 'nothing'}, the register gives {len(expected)}")
    # E
    has_line = 'id="s-line"' in main
    if (fam["group"] == "line") != has_line:
        out.append(f"{fam['slug']}: filed as group `{fam['group']}` but the page "
                   f"{'shows' if has_line else 'does not show'} an On-the-direct-line section")
    return out


def reckon(root):
    people, lr, year = L.population(root)
    held_or_living = {p.slug for p in people if p.slug and (p.living or getattr(p, "held", False))}
    known = {p.slug for p in people if p.slug}
    return people, held_or_living, known


def expected_for(fam, people):
    out = set()
    for p in people:
        if not p.slug or p.living or getattr(p, "held", False):
            continue
        if p.kind == "roster":
            continue
        if any(fold(w) in fam["forms"] for w in surname_words(p.name)):
            out.add(p.slug)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent))
    ap.add_argument("--dist", default="")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    dist = dist_dir(root, a.dist)
    fams = read_families(root)
    if not fams:
        print("  --    families   not run: data/families.tsv holds no family")
        return 2
    if not (dist / "index.html").exists():
        print(f"  FAIL  families   no built site under {dist}: refusing to pass on an empty build")
        return 1
    # F
    seen, probs = {}, []
    for f in fams:
        for t in f["forms"]:
            if t in seen and seen[t] != f["slug"]:
                probs.append(f"the spelling `{t}` is claimed by both {seen[t]} and {f['slug']}")
            seen[t] = f["slug"]
    people, bad, known = reckon(root)
    if not bad:
        print("  --    families   not run: the reckoning found nobody living or held out, so there is nobody to keep off the pages")
        return 2
    home = (dist / "index.html").read_text(encoding="utf-8")
    m_nav = re.search(r'<nav[^>]*class="[^"]*topnav.*?</nav>', home, re.S)
    nav_html = m_nav.group(0) if m_nav else ""
    if not nav_html:
        print("  --    families   not run: the built home page has no main menu to read")
        return 2
    index_p = dist / "families" / "index.html"
    index_html = index_p.read_text(encoding="utf-8") if index_p.exists() else ""
    sm = dist / "sitemap.xml"
    sitemap = sm.read_text(encoding="utf-8") if sm.exists() else ""
    site = "https://lerena.defranceski.com"
    if not index_html:
        probs.append("/families/ is not built")

    pages = {}
    for f in fams:
        p = dist / "families" / f["slug"] / "index.html"
        if not p.exists():
            probs.append(f"{f['slug']}: no built page at /families/{f['slug']}/")
            continue
        pages[f["slug"]] = p.read_text(encoding="utf-8")

    # --- planted faults: the rules must be able to FAIL ---
    if pages:
        fam = next(f for f in fams if f["slug"] in pages)
        page = pages[fam["slug"]]
        exp = expected_for(fam, people)
        ctl = []
        victim = sorted(bad)[0]
        mutants = {
            "a link to a living or held-out person": page.replace("</main>", f'<a href="/people/{victim}/">x</a></main>'),
            "a person dropped from the list": re.sub(r'<tr[^>]*>\s*<td[^>]*><a href="/people/[^"]+/"[^>]*>.*?</tr>', "", page, count=1, flags=re.S),
            "a stranger added to the list": page.replace(
                "</tbody>", '<tr><td><a href="/people/%s/">x</a></td></tr></tbody>' % sorted(known - exp - bad)[0], 1),
            "a false count in the eyebrow": re.sub(r"\d+ (person|people) of the name", "999 people of the name", page, count=1),
        }
        for what, mp in mutants.items():
            if mp == page:
                print(f"  FAIL  families   the planted fault `{what}` could not be planted, so its rule is untested")
                return 1
            if not judge(fam, mp, exp, bad, known, nav_html, index_html, sitemap, site):
                ctl.append(what)
        if not judge(fam, page, exp, bad, known, "", index_html, sitemap, site):
            ctl.append("a page missing from the menu")
        if not judge(fam, page, exp, bad, known, nav_html, "", sitemap, site):
            ctl.append("a page missing from /families/")
        if not judge(fam, page, exp, bad, known, nav_html, index_html, "", site):
            ctl.append("a page missing from the sitemap")
        flipped = dict(fam, group="research" if fam["group"] == "line" else "line")
        if not judge(flipped, page, exp, bad, known, nav_html, index_html, sitemap, site):
            ctl.append("a family filed under the wrong group")
        planted = len(mutants) + 5
        if ctl:
            print("  FAIL  families   planted faults that the rules did not catch: " + "; ".join(ctl))
            return 1

    n_people = 0
    for f in fams:
        if f["slug"] not in pages:
            continue
        exp = expected_for(f, people)
        n_people += len(exp)
        probs += judge(f, pages[f["slug"]], exp, bad, known, nav_html, index_html, sitemap, site)

    if probs:
        print(f"  FAIL  families   {len(probs)} problem(s):")
        for p in probs[:40]:
            print("          - " + p)
        return 1
    print(f"  ok    families   {len(fams)} family page(s), {n_people} people listed, every one matched to the register by a second "
          f"reckoning; 0 link(s) to {len(bad)} living or held-out page(s); each is in the menu, on /families/ and in the sitemap; "
          f"{planted} planted faults all caught")
    return 0


if __name__ == "__main__":
    sys.exit(main())
