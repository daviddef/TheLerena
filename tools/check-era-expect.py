#!/usr/bin/env python3
"""Does every built person page carry exactly the "at the time" note the data and the snapshot call for, and no other?

The kit's gate (checkera.py) holds each note it finds to the snapshot. It cannot know a note is MISSING, or that a note stands on a year this
archive does not trust, because that depends on what this archive prints. This re-derives, from site/src/data/people.json and the committed snapshot
alone, the note each page should carry (the Born row beside the Birthplace row, only for a person who is neither living nor noindex, only for a
plain year, a bare year only where no era boundary of the region lies within ESTIMATE_YEARS of it: the same rule as site/src/lib/eraYear.js,
written again here) and compares it with the built page: the era id, the year, the boundary wording and the marks the kit puts on a note. A note on a page that should have none, a
missing note and a differing note each fail. It prints COUNTS ONLY: never a person, a place or a date. Zero pages examined, or an archive with no
note at all, is exit 2, not a pass.

    python3 tools/check-era-expect.py [--dist site/dist] [--report FILE]     (--report: counts of the events left silent, by reason and region)
"""
import argparse
import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KIT = ROOT / "site" / "node_modules" / "@daviddef" / "archive-kit" / "kit" / "tools"
sys.path.insert(0, str(KIT))
import eralib  # noqa: E402

ESTIMATE_YEARS = 5
NOTE = re.compile(r'<span class="era-note"([^>]*)>')
ATTR = re.compile(r'([\w-]+)="([^"]*)"')


def boundaries(snap, region):
    out = set()
    for e in (snap.get("regions") or {}).get(region, []):
        for k in ("from", "to"):
            if isinstance(e.get(k), int):
                out.add(e[k])
    for d in snap.get("dropped") or []:
        if d.get("region") == region:
            for k in ("from", "to"):
                if isinstance(d.get(k), int):
                    out.add(d[k])
    return out


def expect(snap, p):
    """-> (reason, era or None). reason is 'ok' or why the event is silent; None for no event at all."""
    if p.get("living") or p.get("noindex"):
        return None, None
    bp = p.get("birthplace")
    if not bp or not any(c.isalnum() for c in bp):
        return None, None
    born = str(p.get("born") or "").strip()
    m = re.match(r"\d{4}", born)
    year = eralib.plain_year(born, int(m.group(0)) if m else None)
    if year is None:
        return "year", None
    key = eralib.fold(bp)
    region = (snap.get("places") or {}).get(key)
    if re.fullmatch(r"\d{4}", born) and isinstance(region, str):
        if any(year - ESTIMATE_YEARS < b <= year + ESTIMATE_YEARS for b in boundaries(snap, region)):
            return "estimate", None
    why = eralib.why_not(snap, bp, year)
    return why, (eralib.era_at(snap, bp, year) if why == "ok" else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(ROOT / "site" / "dist"))
    ap.add_argument("--report", default=None)
    a = ap.parse_args()
    dist = pathlib.Path(a.dist)
    snap = json.load(open(ROOT / "site" / "src" / "data" / "era-snapshot.json", encoding="utf-8"))
    people = json.load(open(ROOT / "site" / "src" / "data" / "people.json", encoding="utf-8"))
    pages = bad = want = found = unchecked = unassessed = 0
    reasons = collections.Counter()
    by_region = collections.Counter()
    for p in people:
        f = dist / "people" / p["slug"] / "index.html"
        if not f.exists():
            continue
        pages += 1
        html = f.read_text(encoding="utf-8")
        got = [dict(ATTR.findall(m)) for m in NOTE.findall(html)]
        reason, era = expect(snap, p)
        if reason is not None:
            reasons[reason] += 1
            if reason == "ok":
                want += 1
                unchecked += 1 if era["unchecked"] else 0
                unassessed += 1 if era["unassessed"] else 0
                by_region[era["region"]] += 1
        found += len(got)
        if era is None:
            if got:
                bad += 1
            continue
        # the era, the year, the boundary wording, and the marks the kit puts on a note (data-era-assessed "1"/"0", and data-era-approx,
        # -contested, -margin-unsourced, -edge-agree: "1" or absent), each the same as the snapshot says of the era
        marks = ("data-era-approx", "approx"), ("data-era-contested", "contested"), ("data-era-margin-unsourced", "unsourced"), \
                ("data-era-edge-agree", "edgeAgree"), ("data-era-boundary", "boundary")
        if len(got) != 1 or got[0].get("data-era") != era["id"] or got[0].get("data-era-year") != str(era["year"]) \
                or got[0].get("data-era-assessed") != ("0" if era["unassessed"] else "1") \
                or any((got[0].get(attr) == "1") != (era.get(key) is True) for attr, key in marks):
            bad += 1
    if pages == 0:
        print("  --    era-expect  not run: no person page found in %s" % dist)
        return 2
    if want == 0 and found == 0:
        print("  --    era-expect  not run: the data calls for no note and the pages carry none; a gate that found nothing has not found that nothing is wrong")
        return 2
    print("  %s  era-expect  %d pages; %d notes expected, %d found; %d page(s) differ (%d notes rest on a place with no coordinates, %d on an era the Atlas has not assessed)"
          % ("ok  " if bad == 0 and want == found else "FAIL", pages, want, found, bad, unchecked, unassessed))
    if a.report:
        json.dump({"pages": pages, "reasons": dict(reasons), "notes_by_region": dict(by_region), "unchecked": unchecked, "unassessed": unassessed},
                  open(a.report, "w"), indent=1, sort_keys=True)
    return 0 if bad == 0 and want == found else 1


if __name__ == "__main__":
    sys.exit(main())
