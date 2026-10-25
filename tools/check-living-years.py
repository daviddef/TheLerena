#!/usr/bin/env python3
"""No year or date at or after the living line is printed for a person with no death. (25 October 2026)

    THE LINE  =  this year minus 80  (livingcheck.current_cutoff: the kit's own bound and the calendar,
                 derived, never typed: 1946 in 2026, 1947 in 2027).
    Born in that year or later, with no death recorded, is a LIVING person: named with relationships and
    town and country, and nothing more. This gate fails when ANY public page, data file or tracked file
    prints a birth year or birth date on or after the line without a death beside it.

WHY THIS GATE EXISTS, and why the others did not catch it. tools/check-living-standard.py guards the people
the living RULE calls living: it looks for a date against each of their names. That is a gate on the rule's
answer, and the answer was wrong in two ways that left real people unguarded:

  1. The rule's answer. The kit's living_rule.is_living returns "not living" for ANY person with a public-source
     citation, whatever their birth year. A person aged 78 with no death recorded was therefore "not living" and
     nobody was looking for their date (Mazza, 25 October 2026). tools/build-people.py and tools/livingcheck.py
     now withhold the citations from the rule for anyone with a birth year (cites_for_living).
  2. Where the year lives. The rule reads a birth year from the register and the chart's working files. A
     year typed into a commit message (which /changes/ prints word for word), a passenger-list transcription,
     a research note or a work-list row is in neither, so the person has no birth year, is "not living", and
     the standard gate has no name to look for. This gate does not start from a person. It starts from the
     SHAPE of a birth in the text ("b. 1949", "born 24 April 1949", "(1950-)", "birthDate") and asks what is
     beside it.

WHAT COUNTS AS A DEATH BESIDE IT (the occurrence is then fine):
  - a death word within 90 characters after the year ("d.", died, dead, death, buried, burial, killed ...),
    or a closed span ("1950-1999");
  - a name before it that the archive's own data records dead (the population in livingcheck.py: a death or burial
    in the register, the chart's working files, the burial register);
  - an entry in data/living-year-allow.json, which names the exception and the reason. That file holds two
    kinds of entry and nothing else: a person whose death the archive's data records but no page prints
    (listed for David to confirm; the death is never added by a tool), and a single stated snippet.

ALSO FAILED: a person the data records dead, born on or after the line, whose page publishes no death, who is not
in that registry: every such person is a decision somebody made, not an accident.

THE LINE MOVES WITH THE CALENDAR: LIVING_TODAY_YEAR=2027 makes it 1947 and the planted faults prove it.

Usage:  python3 tools/check-living-years.py [--root DIR] [--dist DIR]
Exit 0 pass; 1 breach, or a run that could not look (an empty build, an unread register, too few files): a run that
could not look is not a pass.
"""
import argparse
import html
import json
import os
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import livingcheck as L  # noqa: E402

SERVED_EXT = {".html", ".json", ".xml", ".txt", ".webmanifest", ".csv", ".tsv", ".md"}
TRACKED_EXT = {".json", ".tsv", ".csv", ".md", ".txt", ".astro", ".html", ".xml"}
SKIP_TRACKED = ("tools/", "site/package-lock.json", "site/node_modules/", "package-lock.json")
ALLOW = "data/living-year-allow.json"

# How a BIRTH is written. A bare year is not screened (every year appears somewhere on a genealogy site and a gate
# that fires on all of them gets switched off); the SHAPE of a birth is. {Y} is the 4-digit year, tested against the line.
Y = r"(1[0-9]{3}|20[0-9]{2})"
BIRTH = [
    # b. 1949   b.1949   b 1949   (c. / ca.)
    ("b.", re.compile(r"(?<![\w])b\.?\s?(?:c\.?\s?|ca\.?\s?)?" + Y + r"(?!\d)")),
    # born 1949   born 24 April 1949   born in Johannesburg in 1949   Born 1991-01-02   born JUNE 1947
    ("born", re.compile(r"\b[Bb][Oo][Rr][Nn](?: on| in| at)?(?: [A-Za-z]+){0,3}? (?:\d{1,2} )?(?:[A-Za-z]{3,9}\.? )?(?:c\. )?" + Y + r"(?!\d)")),
    # (1950-)   (b. 1950-)   an open life span
    ("open", re.compile(r"\((?:b\. ?)?" + Y + r"\s?[–—-]\s?\)")),
    # structured: "birthDate": "1949-04-24"
    ("birthDate", re.compile(r"birthDate\W{1,6}" + Y)),
]
DEATH = re.compile(r"(?<![A-Za-z])(?:d\.|died|dies|dead|death|deaths|buried|burial|killed|deceased|murdered|funeral|"
                   r"obituary|estate notice|widow)(?![a-z])|†|[–—-]\s*(?:\d{1,2}\s+\w+\s+)?(?:1[0-9]{3}|20[0-9]{2})", re.I)


def dist_dir(root, arg):
    if arg:
        return pathlib.Path(arg)
    ao = os.environ.get("ARCHIVE_OUT")
    if ao:
        return pathlib.Path(ao) if os.path.isabs(ao) else root / "site" / ao
    return root / "site" / "dist"


def read(p):
    try:
        return pathlib.Path(p).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def text_of(path, raw):
    """What a reader (or a crawler) is given. HTML: the visible text and the JSON-LD; everything else: as written."""
    if path.suffix.lower() != ".html":
        return raw
    ld = " ".join(re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', raw, re.S))
    body = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", raw)
    return html.unescape(re.sub(r"<[^>]+>", " ", body)) + " " + ld


def tracked_files(root):
    try:
        out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=root, capture_output=True,
                             text=True, check=True).stdout.splitlines()
        if out:
            return [root / p for p in out]
    except Exception:
        pass
    res = []
    for dp, dn, fns in os.walk(root):
        dn[:] = [d for d in dn if d not in {"node_modules", ".git", ".astro"} and not d.startswith("dist")]
        res += [pathlib.Path(dp) / f for f in fns]
    return res


def births_in(text, cut, top):
    """[(start, end, year, kind)] for every birth-shaped year in [cut, top]."""
    hits = []
    for kind, rx in BIRTH:
        for m in rx.finditer(text):
            y = int(m.group(1))
            if cut <= y <= top:
                hits.append((m.start(), m.end(), y, kind))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(L.ROOT))
    ap.add_argument("--dist", default="")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    dist = dist_dir(root, a.dist)
    if not dist.exists() or not list(dist.rglob("index.html")):
        print(f"  FAIL  living-years  no built pages under {dist}: refusing to pass on an empty build")
        return 1
    people, lr, year = L.population(root)
    if sum(1 for p in people if p.kind == "register") < 100:
        print("  FAIL  living-years  the reckoning found too few register rows: the register was not read")
        return 1
    cut = L.current_cutoff(lr, year)
    fails = []

    # ---- the registry of exceptions: no digit-free guessing; each entry says WHY
    allow = {}
    af = root / ALLOW
    if af.exists():
        try:
            allow = json.loads(af.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  FAIL  living-years  {ALLOW} is not valid JSON ({e})")
            return 1
    reg = {}
    for e in allow.get("unpublished_deaths", []):
        if not (e.get("slug") and str(e.get("reason", "")).strip()):
            fails.append(f"{ALLOW}: an unpublished_deaths entry has no slug or no reason")
        else:
            reg[e["slug"]] = e
    spellings = {}
    for e in allow.get("spellings", []):
        if not (e.get("slug") and e.get("also_written") and str(e.get("reason", "")).strip()):
            fails.append(f"{ALLOW}: a spellings entry needs slug, also_written and reason")
        else:
            spellings[e["slug"]] = e
    snippets = [e for e in allow.get("snippets", [])]
    for e in snippets:
        if not (e.get("file") and e.get("contains") and str(e.get("reason", "")).strip()):
            fails.append(f"{ALLOW}: a snippets entry needs file, contains and reason")

    # ---- the population: who the archive's data says is dead and was born on or after the line
    pj = {q["slug"]: q for q in json.loads((root / "site" / "src" / "data" / "people.json").read_text(encoding="utf-8"))}
    dead_young = [p for p in people if p.by is not None and p.by >= cut and p.dead and not p.held]
    for p in people:
        if p.by is not None and p.by >= cut and not p.dead and not p.held and p.slug in pj and not pj[p.slug].get("living"):
            fails.append(f"/people/{p.slug}/ was born on or after {cut}, has no death recorded, and people.json does not "
                         "call them living")
    unpublished = []
    for p in dead_young:
        q = pj.get(p.slug, {})
        if not (q.get("died") or "").strip():
            unpublished.append(p.slug)
            if p.slug not in reg:
                fails.append(f"/people/{p.slug}/ is recorded dead in the archive's data but no page prints the death, and "
                             f"{ALLOW} does not list them: add them with the reason, or publish the death after David confirms")
    for s in reg:
        if s not in {p.slug for p in dead_young}:
            fails.append(f"{ALLOW} lists /people/{s}/ as a death the archive records but does not print, and the data no longer "
                         "shows that: delete the entry")
    # The names the data's dead people are written under, each with the birth year the data holds for them. A form
    # beside a birth only excuses it when the year agrees (within three: the archive's own sources disagree by one or
    # two), so a living namesake born in another decade is not excused by a dead man's name.
    dead_forms = []
    for p in dead_young:
        toks = L.fold(p.name).split()
        forms = {" ".join(toks)}
        if len(toks) >= 2:
            forms |= {" ".join(toks[:2]), toks[0] + " " + toks[-1]}
        for w in reg.get(p.slug, {}).get("also_written", []) + spellings.get(p.slug, {}).get("also_written", []):
            forms.add(L.fold(w))
        dead_forms += [(f, p.by) for f in forms if len(f) > 5]

    def named_dead(window, y):
        w = L.fold(window)
        return any(abs(by - y) <= 3 and re.search(r"(?<![a-z])" + re.escape(n) + r"(?![a-z])", w) for n, by in dead_forms)

    dead_by = {p.slug: p.by for p in dead_young}

    def own_page(rel, y):
        """A dead-by-the-data person's OWN page (people/<slug>/): a birth on it is theirs, and the page is where the
        death is (or is registered as not yet printed)."""
        m = re.match(r"people/([^/]+)/", rel)
        return bool(m) and m.group(1) in dead_by and abs(dead_by[m.group(1)] - y) <= 3

    def allowed(rel, ctx):
        return any(e.get("file") and e.get("contains") and (e["file"] in ("*", rel) or rel.endswith(e["file"])) and e["contains"] in ctx
                   for e in snippets)

    # ---- scan: served files, then every tracked text file
    scanned = 0
    files = []
    for f in dist.rglob("*"):
        if f.is_file() and f.suffix.lower() in SERVED_EXT:
            files.append(("served", f, f.relative_to(dist).as_posix()))
    for f in tracked_files(root):
        rel = f.relative_to(root).as_posix()
        if f.suffix.lower() in TRACKED_EXT and f.is_file() and not rel.startswith(SKIP_TRACKED) and "/dist" not in rel \
                and not rel.startswith("site/dist") and rel != ALLOW and not rel.startswith("site/public/atlas"):
            files.append(("tracked", f, rel))
    top = year
    seen = set()
    for kind, f, rel in files:
        raw = read(f)
        if f.suffix.lower() == ".json":
            raw = raw.replace("\\n", " ")               # a JSON string's escaped line break is a space to a reader
        t = re.sub(r"\s+", " ", text_of(f, raw))
        scanned += 1
        for s, e, y, shape in births_in(t, cut, top):
            after = t[e:e + 90]
            before = t[max(0, s - 160):s]
            ctx = t[max(0, s - 60):e + 40]
            if DEATH.search(after) or DEATH.search(t[s:e]) or named_dead(before + " " + t[s:e] + after[:30], y) \
                    or own_page(rel, y) or allowed(rel, ctx):
                continue
            key = (rel, ctx)
            if key in seen:
                continue
            seen.add(key)
            fails.append(f"{'built' if kind == 'served' else 'committed'} file {rel} prints a birth ({y}, on or after {cut}) "
                         f"with no death beside it: «{ctx.strip()[:100]}»")

    if scanned < 50:
        print(f"  FAIL  living-years  only {scanned} file(s) examined: refusing to pass on a scan that looked at nothing")
        return 1
    if fails:
        print(f"  FAIL  living-years  {len(fails)} breach(es): a birth on or after {cut} (the living line for {year}) with no death:")
        for m in list(dict.fromkeys(fails))[:60]:
            print(f"          - {m}")
        if len(set(fails)) > 60:
            print(f"          ... and {len(set(fails)) - 60} more")
        return 1
    print(f"  ok    living-years  line {cut} (= {year} - {lr.LIVING_YEARS}); {scanned} files read (built and tracked); no birth on or after "
          f"the line without a death beside it; {len(dead_young)} dead-by-the-data people born on or after the line, "
          f"{len(unpublished)} with no death printed" + (f", all registered in {ALLOW} for David to confirm" if unpublished else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
