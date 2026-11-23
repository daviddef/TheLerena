#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One page per person: does every person's page list exactly the other people of their name, and does every old name address land?

    python3 ../tools/checknamesakes.py --dist "${ARCHIVE_OUT:-dist}"        # from site/; `npm run check:namesakes`
    python3 ../tools/checknamesakes.py --selftest --dist "${ARCHIVE_OUT:-dist}"   # plants one fault per rule

WHAT CHANGED (23 November 2026). A name used to have a page, /who/<name>/, beside the person's page. The name pages are gone: a person's
page lists the other people who carry the same name (#others-of-this-name), and every old /who/<name>/ address is a static redirect.
This archive had no name-page gate (the kit's checknamepages.py is not wired here), so this one is new, and it checks the NEW rule from the
BUILD and from nothing the page generator used:

  sets      The sets are derived here from the <title> of every built person page (/people/<slug>/): the register name, accents and case
            folded (the key the old name pages had). The others of a page are the rest of its set.
  missing   a page's "Others of this name" list lacks a person of its name.
  extra     it lists a page that does not carry the name, or itself.
  absent    a name is shared and the page has no list, or the page has a list and nobody shares its name
            (a living person's page is a name and a town and carries no list, as the kit draws it).
  stub      /who/<name>/ must be a redirect for EVERY name a person page carries; one that is a page still drawn, a redirect whose
            target is not built or is not a page of that name, whose #fragment is not on the target (a shared name lands on the
            section; a name one person bears on no fragment), that is not noindex, or that is in the sitemap.
  index     /who/ links to a /who/<name>/ page, or does not link a person page of the archive.

A living person is never named in a message (their slug can carry a year): their page is reported as "a living person's page"
(any page the kit marks data-living). Exit 0 clean, 1 findings, 2 it could not see what it checks (no build, no person page, no stub).

On 23 November 2026 no name is shared (the register writes a different whole name for every person), so the real build has no list to
check; the self-test therefore MAKES a shared pair in memory (two unshared pages given one name, the redirects and the lists to match),
shows that this pair is clean, and plants each fault on it.
"""
import argparse
import html
import os
import re
import sys
import unicodedata

SECTION = "others-of-this-name"
SUFFIX = " — The Lerena Archive"


def fold(s):
    s = unicodedata.normalize("NFD", html.unescape(s or ""))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def read_pages(dist):
    pages = {}
    for root, _dirs, files in os.walk(dist):
        if "index.html" in files:
            rel = os.path.relpath(root, dist).replace(os.sep, "/")
            route = "/" if rel == "." else "/" + rel + "/"
            with open(os.path.join(root, "index.html"), encoding="utf-8", errors="replace") as f:
                pages[route] = f.read()
    sm = os.path.join(dist, "sitemap.xml")
    sitemap = open(sm, encoding="utf-8").read() if os.path.exists(sm) else ""
    return pages, sitemap


def is_stub(raw):
    return 'http-equiv="refresh"' in raw[:900]


def stub_target(raw):
    m = re.search(r'http-equiv="refresh" content="0;url=([^"]+)"', raw[:900])
    return html.unescape(m.group(1)) if m else None


def title_of(raw):
    m = re.search(r"<title>(.*?)</title>", raw, re.S)
    t = html.unescape(m.group(1)).strip() if m else ""
    return t[: -len(SUFFIX)] if t.endswith(SUFFIX) else t


def listed(raw):
    """(has the section, the person pages its list links to, in order)"""
    m = re.search(r'id="%s"' % SECTION, raw)
    if not m:
        return False, []
    tail = raw[m.end():]
    ul = re.search(r'<ul class="oth-list[^"]*"[^>]*>(.*?)</ul>', tail, re.S)
    hrefs = re.findall(r'href="(/people/[^"#?]+/)"', ul.group(1)) if ul else []
    return True, hrefs


def check(pages, sitemap):
    """(findings, counts, setof) over an in-memory build: route -> html."""
    findings = []
    persons = {}
    for route, raw in pages.items():
        if route.startswith("/people/") and route != "/people/" and "data-person-page" in raw and not is_stub(raw):
            persons[route] = {"key": fold(title_of(raw)), "living": 'data-living="1"' in raw}
    stubs = {r: s for r, s in pages.items() if r.startswith("/who/") and r != "/who/" and is_stub(s)}
    named = {r: s for r, s in pages.items() if r.startswith("/who/") and r != "/who/" and not is_stub(s)}
    if not persons or "/who/" not in pages:
        return None, {}, {}
    label = lambda r: "a living person's page" if persons.get(r, {}).get("living") else r

    # ---- the sets, from the built titles
    group = {}
    for r, p in persons.items():
        group.setdefault(p["key"], []).append(r)
    setof = {r: set(group[p["key"]]) - {r} for r, p in persons.items()}
    shared = {k for k, m in group.items() if len(m) > 1}

    with_section = 0
    for r, others in sorted(setof.items()):
        has, got = listed(pages[r])
        if persons[r]["living"]:
            continue
        if has:
            with_section += 1
        if others and not has:
            findings.append("absent: %s shares its name with %d other page(s) and has no #%s section" % (label(r), len(others), SECTION))
            continue
        if has and not others:
            findings.append("absent: %s has a #%s section and nobody shares its name" % (label(r), SECTION))
        miss = sorted(others - set(got))
        extra = sorted(set(got) - others)
        if miss:
            findings.append("missing: %s does not list %d of its name: %s" % (label(r), len(miss), ", ".join(label(x) for x in miss)))
        if extra:
            findings.append("extra: %s lists %d that do not carry its name: %s" % (label(r), len(extra), ", ".join(label(x) for x in extra)))

    # ---- the old addresses: one for every name a person page carries
    for k in sorted(group):
        if "/who/%s/" % k not in stubs and "/who/%s/" % k not in named:
            findings.append("stub: the name of %s has no /who/%s/ address at all (it was published)" % (label(group[k][0]), k))
    for r, raw in sorted(stubs.items()):
        key = r[len("/who/"):-1]
        tgt = stub_target(raw)
        if not tgt:
            findings.append("stub: %s is a redirect with no target" % r)
            continue
        path, _, frag = tgt.partition("#")
        if path not in persons:
            findings.append("stub: %s lands on %s, which is not a built person page" % (r, path))
            continue
        if persons[path]["key"] != key:
            findings.append("stub: %s lands on %s, which is not a page of that name" % (r, label(path)))
        must = key in shared and not persons[path]["living"]
        if frag and frag != SECTION:
            findings.append("stub: %s lands on #%s, which is not the section" % (r, frag))
        elif must and not frag:
            findings.append("stub: %s is a name %d people carry and has no #%s fragment" % (r, len(group[key]), SECTION))
        elif frag and not must:
            findings.append("stub: %s has a #%s fragment and its page has no list to land on" % (r, SECTION))
        elif frag and 'id="%s"' % SECTION not in pages[path]:
            findings.append("stub: %s lands on #%s, which is not on %s" % (r, SECTION, path))
        if 'name="robots" content="noindex"' not in raw[:900]:
            findings.append("stub: %s is not noindex" % r)
        if re.search(r"<loc>[^<]*%s</loc>" % re.escape(r), sitemap):
            findings.append("stub: %s is in the sitemap" % r)
    for r in sorted(named):
        findings.append("stub: %s is a page still drawn: a name a person page carries has no page of its own (and no name here is held without one)" % r)

    # ---- the index
    idx = pages["/who/"]
    for h in sorted(set(re.findall(r'href="(/who/[^"#?]+/)"', idx))):
        findings.append("index: /who/ links to %s, which is a redirect or a page of no use to a reader" % h)
    index_people = set(re.findall(r'href="(/people/[^"#?]+/)"', idx))
    gone = sorted(set(persons) - index_people)
    if gone:
        findings.append("index: /who/ does not link %d person page(s): %s" % (len(gone), ", ".join(label(x) for x in gone[:6])))
    counts = {"person pages": len(persons), "with a list": with_section, "shared names": len(shared),
              "old name addresses (redirects)": len(stubs), "name pages left": len(named)}
    return findings, counts, setof


def make_shared_pair(pages, setof):
    """In memory: two unshared, not-living person pages given ONE name, their lists, and the redirects to match.
    Returns (pages, a, b) with a, b the two person routes (a sorts first, so it is the one the shared name lands on)."""
    v = dict(pages)
    solo = sorted(r for r in v if r.startswith("/people/") and r != "/people/" and "data-person-page" in v[r]
                  and not is_stub(v[r]) and 'data-living="1"' not in v[r] and not setof.get(r))
    a, b = solo[0], solo[1]
    ta, tb = title_of(v[a]), title_of(v[b])
    ka, kb = fold(ta), fold(tb)
    v[b] = v[b].replace("<title>%s%s</title>" % (html.escape(tb, quote=True), SUFFIX), "<title>%s%s</title>" % (html.escape(ta, quote=True), SUFFIX), 1)
    if title_of(v[b]) != ta:      # the title may carry quotes as &quot; and not &#x27;
        v[b] = re.sub(r"<title>.*?</title>", "<title>%s%s</title>" % (html.escape(ta), SUFFIX), v[b], count=1, flags=re.S)
    assert fold(title_of(v[b])) == ka, "could not rename the planted page"
    sec = lambda to: ('<div id="%s"><p class="oth-lede">One other person carries this name.</p><ul class="oth-list"><li><a href="%s">x</a></li></ul></div>' % (SECTION, to))
    for me, other in ((a, b), (b, a)):
        assert "</main>" in v[me]
        v[me] = v[me].replace("</main>", sec(other) + "</main>", 1)
    # the redirects: the shared name lands on a's section; b's own old name is now a's name (its address stays a redirect to a)
    ra, rb = "/who/%s/" % ka, "/who/%s/" % kb
    v[ra] = v[ra].replace("url=%s" % a, "url=%s#%s" % (a, SECTION)).replace('href="%s"' % a, 'href="%s#%s"' % (a, SECTION), 1)
    if rb in v:
        del v[rb]
    return v, a, b, ra


def selftest(pages, sitemap):
    f0, c0, setof0 = check(pages, sitemap)
    ok = True
    print("  control: the untouched build -> %d finding(s)%s" % (len(f0), "" if not f0 else "  <-- SHOULD BE 0"))
    if f0:
        ok = False
    base, a, b, ra = make_shared_pair(pages, setof0)
    f1, c1, _s = check(base, sitemap)
    want = c0.get("shared names", 0) + 1
    print("  control: two pages given one name, lists and redirects to match -> %d finding(s), %d shared name(s)%s"
          % (len(f1), c1.get("shared names", -1), "" if not f1 and c1.get("shared names") == want else "  <-- SHOULD BE 0 AND %d" % want))
    if f1 or c1.get("shared names") != want:
        return False
    solo = sorted(r for r in base if r.startswith("/people/") and r != "/people/" and "data-person-page" in base[r]
                  and not is_stub(base[r]) and 'data-living="1"' not in base[r] and r not in (a, b) and not setof0.get(r))
    stub = sorted(r for r in base if r.startswith("/who/") and r != "/who/" and is_stub(base[r]) and r != ra)[0]

    def planted(name, mutate, want):
        nonlocal ok
        v = dict(base)
        mutate(v)
        got, _c, _s = check(v, sitemap)
        hit = any(g.startswith(want) for g in (got or []))
        print("  %-56s %s" % (name, "caught" if hit else "MISSED  <-- the gate cannot see this"))
        ok = ok and hit

    def drop_one(v):
        i = v[a].index('<ul class="oth-list')
        v[a] = v[a][:i] + re.sub(r"<li>.*?</li>", "", v[a][i:], count=1, flags=re.S)
    planted("a person of the name left off a list", drop_one, "missing")

    def add_stranger(v):
        i = v[a].index('<ul class="oth-list')
        j = v[a].index("</ul>", i)
        v[a] = v[a][:j] + '<li><a href="%s">x</a></li>' % solo[0] + v[a][j:]
    planted("a stranger added to a list", add_stranger, "extra")
    planted("a list on a name nobody shares",
            lambda v: v.__setitem__(solo[0], v[solo[0]].replace("</main>", '<div id="%s"><ul class="oth-list"><li><a href="%s">x</a></li></ul></div></main>' % (SECTION, a), 1)), "absent")
    planted("a shared name with no section", lambda v: v.__setitem__(a, v[a].replace('id="%s"' % SECTION, 'id="nothing"')), "absent")
    planted("a shared name's redirect with no fragment", lambda v: v.__setitem__(ra, v[ra].replace("#" + SECTION, "")), "stub")
    planted("a redirect to a page that was never built", lambda v: v.__setitem__(stub, v[stub].replace("/people/", "/nowhere/")), "stub")
    own = stub_target(base[stub]).partition("#")[0]
    elsewhere = next(r for r in solo if r != own)
    planted("a redirect to a page of another name", lambda v: v.__setitem__(stub, re.sub(r"url=/people/[^\"#]+/", "url=" + elsewhere, v[stub], count=1)), "stub")
    planted("a redirect that can be indexed", lambda v: v.__setitem__(stub, v[stub].replace('name="robots" content="noindex"', 'name="robots" content="index"')), "stub")
    planted("a name page drawn again (no redirect)", lambda v: v.__setitem__(stub, v[solo[0]]), "stub")
    planted("a name with no old address", lambda v: v.pop(stub), "stub")
    got, _c, _s = check(dict(base), sitemap + "<loc>https://x%s</loc>" % stub)
    hit = any(g.startswith("stub") and "sitemap" in g for g in (got or []))
    print("  %-56s %s" % ("a redirect in the sitemap", "caught" if hit else "MISSED  <-- the gate cannot see this"))
    ok = ok and hit
    planted("a link on /who/ to an old name address", lambda v: v.__setitem__("/who/", v["/who/"].replace("</main>", '<a href="%s">x</a></main>' % stub, 1)), "index")
    planted("a person page /who/ no longer links", lambda v: v.__setitem__("/who/", v["/who/"].replace('href="%s"' % solo[0], 'href="/nowhere/"')), "index")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dist", default="dist")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if not os.path.isdir(a.dist):
        print("checknamesakes: %s is not a directory; nothing was checked" % a.dist)
        return 2
    pages, sitemap = read_pages(a.dist)
    if a.selftest:
        if not any(r.startswith("/who/") and r != "/who/" and is_stub(s) for r, s in pages.items()):
            print("checknamesakes: no redirect under /who/ in %s; nothing was checked" % a.dist)
            return 2
        return 0 if selftest(pages, sitemap) else 1
    findings, counts, _setof = check(pages, sitemap)
    if findings is None:
        print("checknamesakes: no person page or no /who/ index in %s; nothing was checked" % a.dist)
        return 2
    if not [r for r in pages if r.startswith("/who/") and r != "/who/" and is_stub(pages[r])]:
        print("checknamesakes: no redirect under /who/ in %s; nothing was checked" % a.dist)
        return 2
    for f in findings:
        print("  FAIL  " + f)
    print("checknamesakes: " + ", ".join("%d %s" % (v, k) for k, v in counts.items()) + "; %d finding%s" % (len(findings), "" if len(findings) == 1 else "s"))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
