#!/usr/bin/env python3
"""The living-people standard, version 2 (David, 16 October 2026), enforced on what was BUILT.

    A living person (80 or younger, with no death recorded) is named with their relationships
    and their town and country, and nothing more.

WHO IS LIVING is reckoned in tools/livingcheck.py from the raw data and the kit's one definition
(living_rule.py), NOT read back from the generator. This file then asks of the build, and of the
files committed with it:

  a  AGREE      the generator (people.json) and the rule name the same living people and the same
                held-out people. A person here and not there is a person nobody is guarding.
  b  PAGE       every living person has a page, `noindex`, with no table, no image, no Person
                structured data and no year anywhere in it; and it is in neither the sitemap nor
                this site's search index.
  c  DATES      no date or year sits against a living person's name in ANY tracked file (data/, notes/,
                site/src ...) or any built page or served file, and no literal full date of theirs is served.
                A living person is recorded by data/living-roster.tsv (name, slug, town, country, no date).
  r  ROSTER     the roster is not empty, holds no digit, and lists nobody the data records as dead.
  d  NAME PAGES a /who/ page whose every bearer is living is noindex and names no canonical elsewhere.
  e  HELD OUT   an undated person with a living parent, or a person promised privacy, appears nowhere: not in a data file,
                a tsv, a built page or a served file. (This archive's inputs are COMMITTED, so a
                undated child entered in the register is itself a leak: the gate fails on the row.)
  f  NAMED      every person this archive names in its chart has a person page, and no name in a
                chart is drawn without a link.
  g  EMPTY      refuses to pass on a build with no pages, or on a reckoning that found nobody.
  h  SUSPECT    a person the rule calls living whose own source speaks of a death or burial.

Every rule has a planted-fault control in tools/test-living-gates.py, run with the build.
Usage:  python3 tools/check-living-standard.py [--root DIR] [--dist DIR]
"""
import argparse
import html
import json
import os
import pathlib
import re
import subprocess
import sys
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import livingcheck as L  # noqa: E402

YEAR = re.compile(r"\b(1[0-9]{3}|20[0-9]{2})\b")
TEXT_EXT = {".html", ".json", ".xml", ".txt", ".js", ".css", ".tsv", ".md", ".astro", ".py", ".webmanifest", ".csv"}


def slugify(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    s = re.sub(r"[̀-ͯ]", "", s)
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()


def dist_dir(root, arg):
    if arg:
        return pathlib.Path(arg)
    ao = os.environ.get("ARCHIVE_OUT")
    if ao:
        return pathlib.Path(ao) if os.path.isabs(ao) else root / "site" / ao
    return root / "site" / "dist"


def main_text(doc):
    m = re.search(r"<main\b[^>]*>(.*)</main>", doc, re.S | re.I)
    body = m.group(1) if m else doc
    body = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", body)
    return html.unescape(re.sub(r"<[^>]+>", " ", body))


def tracked_files(root):
    """Everything committed OR about to be: a gate that scans only `git ls-files` cannot see a file
    that was added and not yet staged (Luwinski's failed on exactly that)."""
    try:
        out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=root, capture_output=True,
                             text=True, check=True).stdout.splitlines()
        if out:
            return [root / p for p in out if "node_modules/" not in p]
    except Exception:
        pass
    res = []                                    # not a git checkout (a scratch copy): walk instead
    for dp, dn, fns in os.walk(root):
        dn[:] = [d for d in dn if d not in {"node_modules", ".git", ".astro"} and not d.startswith("dist")]
        for f in fns:
            res.append(pathlib.Path(dp) / f)
    return res


def read(p):
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(L.ROOT))
    ap.add_argument("--dist", default="")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    dist = dist_dir(root, a.dist)
    fails = []

    def fail(rule, msg):
        fails.append((rule, msg))

    # g -- an empty build is a refusal, not a pass
    if not dist.exists() or not list(dist.rglob("index.html")):
        print(f"  FAIL  living-std  no built pages under {dist}: refusing to pass on an empty build")
        return 1
    people, lr, year = L.population(root)
    if sum(1 for p in people if p.kind == "register") < 100:
        print(f"  FAIL  living-std  the reckoning found only {sum(1 for p in people if p.kind == 'register')} register rows: the register was not read")
        return 1

    pj = json.loads((root / "site" / "src" / "data" / "people.json").read_text(encoding="utf-8"))
    byslug = {p["slug"]: p for p in pj}
    living = [p for p in people if p.living]
    held = [p for p in people if p.held]
    quiet = {p["slug"] for p in pj if p.get("noindex")}

    # r -- the roster: refused when empty, and when it holds a date
    rrows = L.roster_rows(root)
    if not rrows:
        fail("r", "data/living-roster.tsv is empty or missing: the gate refuses to guard nobody")
    rtext = (root / "data" / "living-roster.tsv")
    if rtext.exists():
        for line in rtext.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#") and re.search(r"\d", line):
                fail("r", "data/living-roster.tsv holds a digit: the roster records a living person with NO date")
    for p in people:
        if getattr(p, "roster_problem", ""):
            fail("r", f"roster row for /people/{p.slug or '?'}/ is refused: {p.roster_problem}")

    # a -- the generator and the rule agree
    for p in people:
        if p.held:
            if p.slug in byslug:
                fail("a", f"/people/{p.slug}/ is in people.json but the rule HOLDS THIS PERSON OUT (kind: {p.kind})")
            continue
        q = byslug.get(p.slug)
        if q is None:
            fail("a", f"/people/{p.slug or '?'}/ ({p.kind}) is named by the data and has no entry in people.json")
        elif bool(q.get("living")) != bool(p.living):
            fail("a", f"/people/{p.slug}/ is {'LIVING' if p.living else 'not living'} by the rule and "
                      f"{'living' if q.get('living') else 'not living'} in people.json")
    known = {p.slug for p in people}
    for s in byslug:
        if s not in known:
            fail("a", f"/people/{s}/ is in people.json and nobody in the data accounts for them")
    for p in people:
        if p.suspect:                                                                       # h
            fail("h", f"/people/{p.slug}/ is LIVING by the rule, but their own source speaks of a death, burial "
                      "or cemetery: the death is missing from the data, or the wording is about somebody else")

    # living people's structural rules
    sitemap = read(dist / "sitemap.xml")
    if "<loc>" not in sitemap:
        fail("b", "sitemap.xml is missing or empty, so 'not in the sitemap' proves nothing")
    try:
        sidx = json.loads(read(dist / "searchindex.json") or "[]")
    except Exception:
        sidx = []
    if not sidx:
        fail("b", "searchindex.json is missing or empty in the build, so 'not in the search index' proves nothing")
    sidx_hrefs = {str(r.get("h", "")) for r in sidx if isinstance(r, dict)}
    live_slugs = {p.slug for p in living}
    for slug in sorted(live_slugs | (quiet & set(byslug))):
        is_living = slug in live_slugs
        p = L.P(slug=slug)
        page = dist / "people" / p.slug / "index.html"
        url = f"/people/{p.slug}/"
        if not page.exists():
            fail("f", f"{url} was not built")
            continue
        doc = read(page)
        if not re.search(r'name=["\']robots["\'][^>]*noindex', doc[:6000], re.I):
            fail("b", f"{url} lacks <meta name=robots noindex>")
        if re.search(r"<loc>[^<]*" + re.escape(url) + r"</loc>", sitemap):
            fail("b", f"{url} is in sitemap.xml")
        if any(h.rstrip("/") .endswith(url.rstrip("/")) for h in sidx_hrefs):
            fail("b", f"{url} is in the search index")
        if not is_living:
            continue                                                  # a noindex stub need not be bare
        for blob in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', doc, re.S):
            if re.search(r'"@type"\s*:\s*"Person"', blob):
                fail("b", f"{url} carries Person structured data")
        if re.search(r"<table\b", doc, re.I):
            fail("b", f"{url} has a table")
        if re.search(r"<(img|picture|video|canvas)\b", re.sub(r"(?s)<footer.*?</footer>|<nav.*?</nav>", "", doc), re.I):
            fail("b", f"{url} has an image")
        txt = main_text(doc)
        # "All 1003 entries" is the size of the register, printed on every person page: a count, not a year
        # (it began to read as one when the register passed a thousand people, 29 October 2026)
        txt = re.sub(r"\bAll\s+\d+\s+entries\b", "", txt)
        ys = sorted(set(YEAR.findall(txt)))
        if ys:
            fail("b", f"{url} shows a year ({', '.join(ys)}): a living person has no dates")

    # c -- no full date of a living person anywhere in what is served
    served = [f for f in dist.rglob("*") if f.is_file() and f.suffix.lower() in TEXT_EXT]
    forbidden = {}
    for p in living:
        for d in p.private_dates:
            if len(d) >= 8:
                forbidden.setdefault(d, p.slug)
    for f in served:
        t = read(f)
        for d, owner in forbidden.items():
            if d in t:
                fail("c", f"{f.relative_to(dist)} contains the full date «{d}», which the data attaches to a "
                          f"living person (/people/{owner}/)")
                break
    # c, continued -- a date or year against a living person's NAME, in any tracked file or served file.
    # This is the test that works once the date is gone from the repo: it needs no copy of the date.
    for p in living:
        for f in tracked_files(root):
            rel = f.relative_to(root).as_posix()
            if f.suffix.lower() not in TEXT_EXT or rel.startswith("tools/") or "/dist" in rel \
                    or rel.startswith("site/dist") or rel.startswith("site/public/atlas"):
                continue
            hits = L.dated_mentions(read(f), p.name, is_tsv=f.suffix.lower() in (".tsv", ".csv"))
            if hits:
                fail("c", f"committed file {rel} puts a date against a living person's name («{hits[0].strip()[:40]}»)")
        for f in served:
            if f.suffix.lower() not in (".html", ".json", ".txt", ".xml"):
                continue
            t = read(f)
            if f.suffix.lower() == ".html":
                t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", t)))
            hits = L.dated_mentions(t, p.name)
            if hits:
                fail("c", f"{f.relative_to(dist)} puts a date against a living person's name («{hits[0].strip()[:40]}»)")

    # d -- name pages
    pj_by_name = {}
    for q in pj:
        pj_by_name.setdefault(slugify(q["name"]), []).append(q)
    for wdir in sorted((dist / "who").glob("*/index.html")) if (dist / "who").exists() else []:
        bearers = pj_by_name.get(wdir.parent.name, [])
        if bearers and all(b["slug"] in live_slugs or b.get("living") for b in bearers):
            doc = read(wdir)
            if not re.search(r'name=["\']robots["\'][^>]*noindex', doc[:6000], re.I):
                fail("d", f"/who/{wdir.parent.name}/ names only living people and is not noindex")
            for c in re.findall(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', doc):
                if f"/who/{wdir.parent.name}" not in c:
                    fail("d", f"/who/{wdir.parent.name}/ names a canonical elsewhere ({c})")
        elif bearers and all(b.get("noindex") for b in bearers):
            if not re.search(r'name=["\']robots["\'][^>]*noindex', read(wdir)[:6000], re.I):
                fail("d", f"/who/{wdir.parent.name}/ names only unindexed people and is itself indexable")

    # e -- held out: nowhere at all
    if held:
        files = served + [f for f in tracked_files(root) if f.suffix.lower() in TEXT_EXT and "/dist" not in f.as_posix()
                          and not f.relative_to(root).as_posix().startswith("tools/")]
        for h in held:
            needles = {L.fold(h.name)}
            if h.slug:
                needles.add(h.slug)
            for f in files:
                t = html.unescape(re.sub(r"<[^>]+>", " ", read(f))).casefold()
                t = " ".join(unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().split())
                if any(n and n in t for n in needles):
                    where = f.relative_to(dist).as_posix() if str(f).startswith(str(dist)) else f.relative_to(root).as_posix()
                    fail("e", f"a HELD-OUT person ({h.kind}, /people/{h.slug or '?'}/) appears in {where}")
                    break

    # f -- every named person has a page, and no chart node is drawn without a link
    for q in pj:
        for k in ("father", "mother"):
            n = q.get(k)
            if n and not n.get("slug"):
                fail("f", f"/people/{q['slug']}/ names a {k} ({n['name']}) who has no person page")
        for k in ("spouses", "children", "siblings"):
            for n in q.get(k, []):
                if not n.get("slug"):
                    fail("f", f"/people/{q['slug']}/ names a {k[:-1]} ({n['name']}) who has no person page")
                elif n["slug"] not in byslug:
                    fail("f", f"/people/{q['slug']}/ links {n['slug']}, who is not in people.json")
    for page in sorted((dist / "people").glob("*/index.html")) if (dist / "people").exists() else []:
        doc = read(page)
        for m in re.finditer(r'<div class="node(?![^"]*\bme\b)[^"]*"[^>]*>\s*(?:<span class="mar">[^<]*</span>\s*)?<span class="nm">([^<]*)', doc):
            fail("f", f"/people/{page.parent.name}/ draws {html.unescape(m.group(1)).strip()} in its chart with no link")
    for p in people:
        if not p.held and p.slug and not (dist / "people" / p.slug / "index.html").exists():
            fail("f", f"/people/{p.slug}/ ({p.kind}) was not built")

    # report
    n_noidx = sum(1 for p in pj if p.get("noindex"))
    if fails:
        print(f"  FAIL  living-std  {len(fails)} breach(es) of the living-people standard:")
        for rule, msg in dict.fromkeys(fails):
            print(f"          - [{rule}] {msg}")
        return 1
    print(f"  ok    living-std  {len(living)} living, {len(held)} held out, {n_noidx} noindex of {len(pj)} people; "
          f"living pages: noindex, not in sitemap or search, no table/image/Person JSON-LD/year; "
          f"{len(forbidden)} full-date string(s) absent from {len(served)} served files")
    print(f"          roster: {len(rrows)} living person(s) recorded with no date; no tracked file or served file puts a date against a living name")
    if not living:
        print("          NOTE  the rule found NOBODY living: if that is not expected, the data or the rule changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
