#!/usr/bin/env python3
"""Which corrections name which person: ONE source, three readers.

data/corrections.tsv has an optional `who` column: person slug(s) (the page's own /people/<slug>/), separated by
semicolons, written BY HAND where the correction is plainly about that person (a full name in the row, or a person
the row cannot mean anyone else by). Nothing is derived from the free text.

Three things read it, and they read it through here so they cannot disagree:
  - site/src/data/corrections-by-person.json   (written by build-people.py): {slug: [{"d": date}, ...]}; the person page prints the
    count and links each date to the day's first entry on /corrections/ (site/src/lib/corrections-ids.js).
  - data/tree-page/tree.json `cx` (tools/build-tree-page.py): the number of correction rows that name the person. A COUNT ONLY,
    never what a correction says. Omitted when 0.
  - tools/check-corrections.py: every slug must be a built person page and not a living, held-out or noindex person; the JSON
    and tree.json must agree with this reading.

A living, held-out or noindex person is NEVER counted, so a slug naming one is a gate failure, not a silent drop.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORR = ROOT / "data" / "corrections.tsv"
PEOPLE = ROOT / "site" / "src" / "data" / "people.json"
OUTJSON = ROOT / "site" / "src" / "data" / "corrections-by-person.json"


def rows():
    """[(line_no, date, [slug, ...])] for every correction row that has a `who`."""
    out = []
    hdr = None
    for n, line in enumerate(CORR.open(encoding="utf-8"), 1):
        if not line.strip() or line.startswith("#"):
            continue
        c = line.rstrip("\n").split("\t")
        if hdr is None:
            hdr = c
            continue
        if "who" not in hdr:
            continue
        i = hdr.index("who")
        w = c[i].strip() if len(c) > i else ""
        slugs = [s.strip() for s in w.split(";") if s.strip()]
        if slugs:
            out.append((n, c[0], slugs))
    return out


def by_person(people=None):
    """({slug: [date, ...]} for drawable people only, [problem text ...])."""
    if people is None:
        people = json.loads(PEOPLE.read_text(encoding="utf-8"))
    P = {p["slug"]: p for p in people}
    res, bad = {}, []
    for n, date, slugs in rows():
        seen = set()
        for s in slugs:
            if s in seen:
                bad.append(f"data/corrections.tsv:{n} names {s} twice")
                continue
            seen.add(s)
            p = P.get(s)
            if p is None:
                bad.append(f"data/corrections.tsv:{n} `who` {s} is not a built person page")
            elif p.get("living") or p.get("noindex"):
                bad.append(f"data/corrections.tsv:{n} `who` {s} is a living, held-out or noindex person: never counted, never named")
            else:
                res.setdefault(s, []).append(date)
    return {k: sorted(v) for k, v in sorted(res.items())}, bad


def render(res):
    doc = {s: [{"d": d} for d in ds] for s, ds in res.items()}
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def write(people=None):
    res, bad = by_person(people)
    OUTJSON.write_text(render(res), encoding="utf-8")
    return res, bad


if __name__ == "__main__":
    r, b = write()
    print(f"corrections-by-person.json: {len(r)} people, {sum(len(v) for v in r.values())} naming(s)")
    for x in b:
        print("  PROBLEM " + x)
