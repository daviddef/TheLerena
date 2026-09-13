#!/usr/bin/env python3
"""Check the built site: internal links, asset paths, and in-page anchors.

Run after `npm run build`. Exits non-zero if anything is broken, so it can be
trusted in a commit sequence rather than eyeballed.

It skips hrefs containing a quote or a plus sign: those are JavaScript template
strings inside inline <script> blocks, not links, and treating them as links
produced a run of false positives the first time this was written.
"""
import os, re, sys
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

print(f"{len(pages)} pages, {len(html_files)} html files, {sum(len(v) for v in ids.values())} ids")
print(f"{len(bad)} broken")
for b in sorted(set(bad))[:40]:
    print("   ", b[0], "->", b[1], f"({b[2]})")
sys.exit(1 if bad else 0)
