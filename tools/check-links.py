#!/usr/bin/env python3
"""Check the built site: internal links, asset paths, and in-page anchors.

Run after `npm run build`. Exits non-zero if anything is broken, so it can be
trusted in a commit sequence rather than eyeballed.

It skips hrefs containing a quote or a plus sign: those are JavaScript template
strings inside inline <script> blocks, not links, and treating them as links
produced a run of false positives the first time this was written.
"""
import os, pathlib, re, sys
from collections import defaultdict

ROOT = "site/dist"
BASE = "/TheLerena"
ASSET = (".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".xml", ".ico", ".webp", ".json", ".pdf")

pages, ids = set(), defaultdict(set)
html_files = []
for d, _, fs in os.walk(ROOT):
    if "index.html" in fs:
        rel = os.path.relpath(d, ROOT)
        pages.add("/" if rel == "." else "/" + rel.replace("\\", "/") + "/")
    for f in fs:
        if f.endswith(".html"):
            html_files.append(os.path.join(d, f))

for fp in html_files:
    s = open(fp, encoding="utf-8").read()
    rel = os.path.relpath(os.path.dirname(fp), ROOT)
    page = "/" if rel == "." else "/" + rel.replace("\\", "/") + "/"
    for m in re.finditer(r'\bid="([^"]+)"', s):
        ids[page].add(m.group(1))

bad = []
for fp in html_files:
    s = open(fp, encoding="utf-8").read()
    rel = os.path.relpath(os.path.dirname(fp), ROOT)
    here = "/" if rel == "." else "/" + rel.replace("\\", "/") + "/"
    for m in re.finditer(r'href="([^"]+)"', s):
        h = m.group(1)
        if "'" in h or "+" in h:
            continue
        if h.startswith("#"):
            if h[1:] and h[1:] not in ids[here]:
                bad.append((fp, h, "no such id on this page"))
            continue
        if not h.startswith(BASE):
            continue
        target, _, frag = h[len(BASE):].partition("#")
        # Assets carry a ?v=<hash> cache-busting fingerprint; strip it before testing the path.
        target = target.split("?", 1)[0] or "/"
        if target.endswith(ASSET):
            if not os.path.exists(os.path.join(ROOT, target.lstrip("/"))):
                bad.append((fp, h, "missing asset"))
            continue
        if not target.endswith("/"):
            target += "/"
        if target not in pages:
            bad.append((fp, h, "no such page"))
        elif frag and frag not in ids[target]:
            bad.append((fp, h, f"no id '{frag}' on {target}"))

# A page that carries an id="contents" list promises to list every section on it.
# Check that promise, so the promise can be made in the page's own prose.
for fp in html_files:
    s = open(fp, encoding="utf-8").read()
    if 'id="contents"' not in s:
        continue
    rel = os.path.relpath(os.path.dirname(fp), ROOT)
    here = "/" if rel == "." else "/" + rel.replace("\\", "/") + "/"
    linked = set(re.findall(r'href="#([^"]+)"', s))
    for m in re.finditer(r'<h2 id="([^"]+)"', s):
        hid = m.group(1)
        if hid != "contents" and hid not in linked:
            bad.append((fp, "#" + hid, "section missing from the contents list"))

# CONTAINER CLASSES ON LEAF ELEMENTS.
# .prose is display:flex/column - a container style for a <div> wrapping paragraphs.
# It was also on 21 <p> elements, and a flex container blockifies its children, so every
# <em> and <strong> inside them was thrown onto its own full-width line. 27 phrases across
# six pages read as fragments for days before anyone looked. The CSS now neutralises
# p.prose, but the misuse itself is still worth catching at the source.
CONTAINERS = ("prose", "grid", "scroll", "cols2")
LEAVES = ("p", "li", "td", "th", "span", "em", "strong", "a", "h1", "h2", "h3")
for fp in html_files:
    s = open(fp, encoding="utf-8").read()
    for m in re.finditer(r'<(' + "|".join(LEAVES) + r')\b[^>]*\bclass="([^"]*)"', s):
        tag, classes = m.group(1), m.group(2).split()
        for c in classes:
            if c in CONTAINERS and not (tag == "p" and c == "prose"):
                bad.append((fp, f"<{tag} class=\"{c}\">",
                            "container class on a leaf element - it will blockify the inline text inside"))

# LITERAL EMPHASIS MARKERS.
# The TSVs mark emphasis as *** like this ***; site/src/lib/text.js converts it. Anything
# that reaches the rendered HTML is a field somebody forgot to pass through emph().
for fp in html_files:
    s = open(fp, encoding="utf-8").read()
    # Only a PAIR means a field escaped emph() - the TSV convention is always paired.
    # A lone *** is ordinary prose (a commit subject once said "stop printing *** at readers"),
    # and flagging that would train me to ignore this check.
    n = len(re.findall(r"\*\*\*[^*]+\*\*\*", s))
    if n:
        bad.append((fp, f"{n} unconverted *** ... *** field(s)",
                    "emphasis markers reached the page - render it through emph()"))

# ---- and one fault this checker CANNOT see from dist, so it reads the source ----
#
# On 20 September 2026 a peer session found a dead link on /direct-line/ that had been
# there since the line was written, pointing at the enrolment card - the document that
# page calls its own best evidence for Pablo Armando. The source said:
#
#     <a href="{u("/enrolment-card/")}">enrolment card</a>
#
# QUOTED. So it is a literal string, not an expression. It shipped as href="{u(" - the
# inner quotes end the attribute - and rendered as words that still looked like a link.
#
# *** THIS CHECKER'S OWN SAFEGUARD IS WHAT HID IT. *** The docstring at the top says it
# skips any href containing a quote, because those are JavaScript template strings in
# inline <script> blocks and treating them as links produced a run of false positives.
# That rule is right, and it is exactly the rule that let a broken attribute through.
#
# So the fault is caught where it is legible: in the .astro SOURCE, where a quoted {u(
# is never correct. Inside a template literal ${u(...)} IS correct and is not matched,
# because the { there is preceded by a $.
SRC = pathlib.Path("site/src/pages")
QUOTED_EXPR = re.compile(r"(?:href|src)=[\"'](?<!\$)\{\s*u\s*\(")
for fp in sorted(SRC.rglob("*.astro")):
    for n, line in enumerate(fp.read_text(encoding="utf-8").splitlines(), 1):
        if QUOTED_EXPR.search(line):
            bad.append((str(fp) + ":" + str(n), "a QUOTED Astro expression in an href",
                        'href="{u(...)}" is a literal string - drop the quotes: href={u(...)}'))

# An EMPTY dist is not a clean bill of health. On 14 September 2026 a broken import left
# `astro build` exiting 0 with nothing written, and this checker printed "0 pages ... 0 broken"
# and passed - the deploy gate reporting success over a site that did not exist. A checker that
# cannot fail on nothing is not a gate.
MIN_PAGES = 50
print(f"{len(pages)} pages, {len(html_files)} html files, {sum(len(v) for v in ids.values())} ids")
if len(pages) < MIN_PAGES:
    print(f"\nREFUSING TO PASS: only {len(pages)} pages in dist, expected at least {MIN_PAGES}.")
    print("   An empty or near-empty build means `astro build` failed while still exiting 0.")
    print("   Run it and read its output - the last error is the real one.")
    sys.exit(1)
print(f"{len(bad)} broken")
for b in sorted(set(bad))[:40]:
    print("   ", b[0], "->", b[1], f"({b[2]})")
sys.exit(1 if bad else 0)
