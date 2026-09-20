#!/usr/bin/env python3
"""An end-to-end audit of the code and the built site.

NOT A GATE. verify.sh refuses a build; this one only LOOKS, and prints what it
finds. Every check here is something the gates do not cover: the gates were each
written to stop one specific thing going wrong again, which means they are sharp
and narrow, and nothing had ever swept the whole estate at once.

Run it with `python3 tools/audit.py` after a build. `--verbose` lists every hit
instead of the first few.

WHAT IT LOOKS AT
  code     every .py compiles, every .js parses, verify.sh is valid bash
  render   unrendered template syntax, emphasis markers that never became <strong>,
           "undefined" / "NaN" / "[object Object]" reaching a reader
  html     duplicate ids, images without alt text, skipped heading levels,
           pages with no title
  assets   every local src= and href= that points at a file which must exist
  data     ragged TSV rows, emphasis parity, control characters, duplicate slugs
  privacy  email addresses and phone numbers in the built site
  reach    pages in the build that nothing links to

WHY "***" IN THE BUILT HTML IS A BUG AND NOT A TYPO. The TSVs mark emphasis as
*** like this ***, and emph() in src/lib/text.js turns it into <strong>. A pair
of asterisks surviving into dist means a field was rendered WITHOUT passing
through emph() - the text is right and the markup was dropped on the floor.
"""
import collections
import html
import json
import pathlib
import py_compile
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"
DATA = ROOT / "data"
SRC = ROOT / "site" / "src"
VERBOSE = "--verbose" in sys.argv

TAGS = re.compile(r"<[^>]+>")
SHOW = 40 if VERBOSE else 4

# Script and style are CODE, not content. The first run of this audit reported four
# pages carrying an "unrendered ${...} template literal"; every one was minified
# JavaScript doing its job inside a <script>. An audit that reports its own blind
# spot as a site defect is worse than no audit, so everything that reads TEXT reads
# it with code removed.
CODE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.S | re.I)


def visible(d):
    return CODE.sub(" ", d)


class Report:
    def __init__(self):
        self.sections = []

    def add(self, name, hits, note="", good=""):
        self.sections.append((name, hits, note, good))

    def out(self):
        bad = 0
        for name, hits, note, good in self.sections:
            if hits:
                bad += len(hits)
                print(f"\n  ✖ {name}: {len(hits)}")
                for h in hits[:SHOW]:
                    print(f"      {h}")
                if len(hits) > SHOW:
                    print(f"      ... and {len(hits) - SHOW} more (--verbose)")
                if note:
                    print(f"      → {note}")
            else:
                print(f"  ✓ {name}{(' - ' + good) if good else ''}")
        return bad


def pages():
    return sorted(DIST.rglob("*.html"))


def rel(p):
    return "/" + p.relative_to(DIST).parent.as_posix().strip(".") + "/"


# --------------------------------------------------------------------------- code
def check_code(r):
    bad = []
    for f in sorted(ROOT.glob("tools/*.py")):
        try:
            py_compile.compile(str(f), doraise=True, cfile=str(f) + "c")
        except py_compile.PyCompileError as e:
            bad.append(f"{f.name}: {str(e).splitlines()[-1][:110]}")
        finally:
            pathlib.Path(str(f) + "c").unlink(missing_ok=True)
    r.add("python compiles", bad, good=f"{len(list(ROOT.glob('tools/*.py')))} tools")

    bad = []
    js = sorted(SRC.glob("lib/*.js"))
    for f in js:
        p = subprocess.run(["node", "--check", str(f)], capture_output=True, text=True)
        if p.returncode:
            bad.append(f"{f.name}: {p.stderr.strip().splitlines()[-1][:110]}")
    r.add("javascript parses", bad, good=f"{len(js)} modules")

    p = subprocess.run(["bash", "-n", str(ROOT / "tools" / "verify.sh")],
                       capture_output=True, text=True)
    r.add("verify.sh is valid bash",
          [p.stderr.strip()[:160]] if p.returncode else [], good="parses")


# ------------------------------------------------------------------------- render
def check_render(r, docs):
    leaks, emph, tmpl = [], [], []
    for p, d in docs:
        body = visible(d)
        for bad in ("[object Object]", "undefined,", ">undefined<", "NaN", "Infinity"):
            if bad in body:
                leaks.append(f"{rel(p)} contains {bad!r}")
        # PAIRED markers only. The changelog entry that created this rule says it
        # outright: "A lone *** in prose is not an unconverted field - the TSV
        # convention is always paired - and flagging it would train me to ignore the
        # check." The first run of this audit flagged that very sentence.
        pairs = re.findall(r"\*\*\*[^*]{1,400}?\*\*\*", body, re.S)
        if pairs:
            emph.append(f"{rel(p)} has {len(pairs)} unconverted *** ... *** span(s)")
        if re.search(r"\$\{[a-zA-Z_]", body):
            tmpl.append(f"{rel(p)} has an unrendered ${{...}} template literal")
    r.add("no placeholder values reach the reader", leaks, good="clean")
    r.add("emphasis markers all became markup", emph,
          note="*** in dist means a field skipped emph() - the markup was dropped")
    r.add("no unrendered template literals", tmpl)


# --------------------------------------------------------------------------- html
def check_html(r, docs):
    dupes, noalt, notitle, skips = [], [], [], []
    for p, d in docs:
        ids = re.findall(r'\sid="([^"]+)"', d)
        for i, n in collections.Counter(ids).items():
            if n > 1:
                dupes.append(f"{rel(p)} id={i!r} x{n}")
        for img in re.findall(r"<img\b[^>]*>", d):
            if "alt=" not in img:
                noalt.append(f"{rel(p)} {img[:70]}")
        t = re.search(r"<title[^>]*>(.*?)</title>", d, re.S)
        if not t or not t.group(1).strip():
            notitle.append(rel(p))
        levels = [int(m) for m in re.findall(r"<h([1-6])\b", d)]
        prev = 0
        for lv in levels:
            if prev and lv > prev + 1:
                skips.append(f"{rel(p)} h{prev} → h{lv}")
                break
            prev = lv
    r.add("no duplicate element ids", dupes)
    r.add("every image has alt text", noalt)
    r.add("every page has a title", notitle, good=f"{len(docs)} pages")
    r.add("no skipped heading levels", skips)


# ------------------------------------------------------------------------- assets
def check_assets(r, docs):
    missing = set()
    for p, d in docs:
        for attr in re.findall(r'(?:src|href)="([^"]+)"', d):
            if attr.startswith(("http", "//", "#", "mailto:", "tel:", "data:")):
                continue
            path = attr.split("?")[0].split("#")[0]
            if not path.startswith("/"):
                continue
            # the site is served under a base; strip it
            for base in ("/TheLerena/", "/"):
                if path.startswith(base):
                    stub = path[len(base):]
                    break
            if not stub or stub.endswith("/"):
                continue
            if "." not in stub.rsplit("/", 1)[-1]:
                continue
            if not (DIST / stub).exists():
                missing.add(f"{rel(p)} → {path}")
    r.add("every local asset exists", sorted(missing))


# --------------------------------------------------------------------------- data
def check_data(r):
    ragged, parity, ctrl = [], [], []
    for f in sorted(DATA.glob("*.tsv")):
        lines = [l.rstrip("\n") for l in f.read_text(encoding="utf-8").splitlines()]
        # MANY OF THESE FILES HOLD SEVERAL TABLES. 1812-union-act.tsv opens with a
        # two-column reading of the act and then starts a three-column one, header
        # and all. The first version of this audit took the first row as THE header
        # and reported 174 "ragged" rows, every one of them a second table doing
        # exactly what it meant to.
        #
        # A stray tab does not look like that. It makes ONE row a different width
        # from everything around it, so only a cell-count that occurs exactly ONCE
        # in a file is worth reporting.
        rows = [(n, line.split("\t")) for n, line in enumerate(lines, 1)
                if line.strip() and not line.startswith("#")]
        widths = collections.Counter(len(c) for _, c in rows)
        for n, cells in rows:
            if widths[len(cells)] == 1 and len(widths) > 1:
                ragged.append(f"{f.name}:{n} is the only {len(cells)}-cell row in the file "
                              f"(others: {', '.join(str(w) for w in sorted(widths) if w != len(cells))})")
            for i, c in enumerate(cells):
                if c.count("***") % 2:
                    parity.append(f"{f.name}:{n} column {i+1} has an odd *** count")
            if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "\t".join(cells)):
                ctrl.append(f"{f.name}:{n} contains a control character")
    r.add("no lone odd-width TSV rows", ragged,
          note="a stray tab makes one row a different width from its neighbours")
    r.add("emphasis parity in data", parity, good="all even")
    r.add("no control characters in data", ctrl)

    people = json.loads((SRC / "data" / "people.json").read_text(encoding="utf-8"))
    slugs = collections.Counter(p.get("slug") for p in people)
    r.add("no duplicate slugs", [f"{s} x{n}" for s, n in slugs.items() if n > 1 and s],
          good=f"{len(people)} people")
    r.add("every person has a name and a slug",
          [f"index {i}" for i, p in enumerate(people) if not p.get("name") or not p.get("slug")])


# ------------------------------------------------------------------------ privacy
def check_privacy(r, docs):
    # An institutional address is CONTENT here: the archive publishes the contact
    # for every repository it asks things of, so a reader can write to them too.
    # A personal mailbox would be a leak. They are not the same finding.
    PERSONAL = re.compile(r"@(gmail|googlemail|hotmail|outlook|yahoo|icloud|me|proton"
                          r"|aol|live|msn)\.", re.I)
    mail, phone, inst = set(), set(), set()
    MAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]{2,}")
    # A BARE RUN OF DIGITS IS A FILM NUMBER, NOT A TELEPHONE. This archive is full of
    # them - 007713686, 004098792, 101485627 - and the first version of this check
    # reported 88 "phone-shaped numbers", 87 of which were microfilm. A published
    # telephone number carries a separator or a country code; a DGS number never does.
    # STRICT. Loosening this twice taught the same lesson twice: a genealogy archive
    # is made of numbers. The first pattern caught 88 microfilm ids; the second caught
    # page ranges and centuries ("1634-2003", "951-956"). A number is only treated as a
    # telephone when it announces itself as one - an international +, or a trunk 0 and
    # a separator, with at least nine digits in total.
    PHONE = re.compile(r"(?<![\w/-])(?:\+\d{1,3}[\s.-]?\d[\d\s.-]{7,}|0\d{1,4}[\s.-]\d{6,})(?![\w/-])")
    for p, d in docs:
        text = html.unescape(TAGS.sub(" ", visible(d)))
        for m in MAIL.findall(text):
            if m.lower().endswith((".png", ".jpg", ".webp")):
                continue
            (mail if PERSONAL.search(m) else inst).add(m)
        for m in PHONE.findall(text):
            digits = re.sub(r"\D", "", m)
            if len(digits) >= 9:
                phone.add(f"{rel(p)} {m.strip()[:28]}")
    r.add("no PERSONAL email addresses in the build", sorted(mail),
          good=f"{len(inst)} institutional contact(s), published on purpose: "
               + ", ".join(sorted(inst)[:3]) + (" ..." if len(inst) > 3 else ""))
    r.add("no unexpected telephone numbers", sorted(phone),
          note="a number with separators is probably a real telephone - check it is meant to be public")


# -------------------------------------------------------------------------- reach
def check_reach(r, docs):
    linked = set()
    for _, d in docs:
        for a in re.findall(r'href="([^"]+)"', d):
            a = a.split("?")[0].split("#")[0]
            if a.startswith("/"):
                linked.add(a.rstrip("/") + "/")
    orphans = []
    for p, _ in docs:
        route = "/TheLerena" + ("/" + p.relative_to(DIST).parent.as_posix()).replace("/.", "") + "/"
        route = route.replace("//", "/")
        if route in ("/TheLerena/",):
            continue
        if route not in linked:
            orphans.append(route)
    r.add("every page is linked from somewhere", sorted(orphans),
          note="an unlinked page is reachable only by guessing its URL")


def main():
    if not DIST.exists():
        print("no build to audit - run npm run build first")
        return 1
    docs = [(p, p.read_text(encoding="utf-8", errors="replace")) for p in pages()]
    print(f"AUDIT — {len(docs)} built pages, {len(list(DATA.glob('*.tsv')))} data files, "
          f"{len(list(ROOT.glob('tools/*.py')))} tools\n")
    r = Report()
    check_code(r)
    check_render(r, docs)
    check_html(r, docs)
    check_assets(r, docs)
    check_data(r)
    check_privacy(r, docs)
    check_reach(r, docs)
    bad = r.out()
    print(f"\n{'-' * 72}")
    print(f"{bad} finding(s). This is a REPORT, not a gate: nothing here fails a build.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
