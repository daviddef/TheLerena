#!/usr/bin/env python3
"""A living person must show their FULL TOWN AND COUNTRY - and nothing beyond it.

THIS GATE USED TO DO THE OPPOSITE, and the history is worth keeping. Until 16 October 2026 it
refused to ship a build that gave a living person a PLACE, because this archive's own rule, written
on /direct-line/, was "No dates, no places, no photographs." A country counts as a place, so it
caught a country pill on a spine row and a "Johannesburg" in a fact position, and it kept a Victorian
almswoman ("LIVING ON MEANS") from being taken for a living person. Its four traps are still true
and are kept in the code:

  1. "LIVING" is a word in records about the dead. The marker is never a word in a sentence now:
     living is a STATUS the shared rule computes (80 or younger, no death recorded), not a grep.
  2. A bare place name proves nothing. "Johannesburg" is all over this archive, attached to the dead.
     So a place is only checked where this gate knows whose it is: the page of the person it belongs to.
  3. A card ends where the next begins. Looking backwards from a name reads the person above.
  4. Proximity is not possession. A town in the prose beside a name is somebody else's line.

THE RULE NOW (David, 16 October 2026): a living person is named with their relationships and their
town and country, and nothing more. So this gate fails when

  A  a living person's page shows NO town or country although the data records one;
  B  it shows the wrong one, or a country without the town, or a town without a country the data
     gives;
  C  it shows ANY OTHER PLACE - another town, a street, an address-like string, a hospital or a care
     home - or the raw birth-place string when that string was an address or an institution and
     should have been reduced to the town;
  D  the generator (people.json) and the rule disagree about WHO is living or WHAT their town and
     country are.

Who is living is reckoned independently, in tools/livingcheck.py, from the raw data and the kit's one
definition (living_rule.py). The structure of a living page (noindex, no table, no year ...) is the
other gate, tools/check-living-standard.py.

A build with nobody living passes with a printed note; a build with no pages is refused.
Usage:  python3 tools/check-living-places.py [--root DIR] [--dist DIR]
"""
import argparse
import html
import json
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import livingcheck as L  # noqa: E402


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
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", body)).split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(L.ROOT))
    ap.add_argument("--dist", default="")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    dist = dist_dir(root, a.dist)
    if not dist.exists() or not list(dist.rglob("index.html")):
        print(f"  FAIL  places    no built pages under {dist}: refusing to pass on an empty build")
        return 1
    people, lr, year = L.population(root)
    if sum(1 for p in people if p.kind == "register") < 100:
        print(f"  FAIL  places    the reckoning found only {sum(1 for p in people if p.kind == 'register')} register rows: the register was not read")
        return 1
    pj = {p["slug"]: p for p in json.loads((root / "site/src/data/people.json").read_text(encoding="utf-8"))}
    places = json.loads((root / "site/src/data/places.json").read_text(encoding="utf-8"))
    place_names = {pl["name"] for pl in places if pl.get("name") and pl["name"] != "Unrecorded"}
    if not L.roster_rows(root):
        print("  FAIL  places    data/living-roster.tsv is empty or missing: 0 living people examined, and this gate "
              "refuses at zero")
        return 1
    living = [p for p in people if p.living]
    if not living:
        print("  ok    places    the rule finds nobody living, so there is nobody to show a place "
              "(NOTE: if that is not expected, the data or the rule changed)")
        return 0

    fails, shown = [], {"both": 0, "town": 0, "none": 0}
    for p in living:
        q = pj.get(p.slug)
        if q is None:
            fails.append(f"/people/{p.slug}/ is living by the rule and absent from people.json")
            continue
        # D -- the generator and the rule agree about the place
        if (q.get("town") or "") != p.town or (q.get("country") or "") != p.country:
            fails.append(f"/people/{p.slug}/: people.json holds town «{q.get('town')}» / country «{q.get('country')}»; "
                         f"the data gives «{p.town}» / «{p.country}»")
        page = dist / "people" / p.slug / "index.html"
        if not page.exists():
            fails.append(f"/people/{p.slug}/ was not built")
            continue
        text = main_text(page.read_text(encoding="utf-8"))
        url = f"/people/{p.slug}/"
        if not p.town:
            shown["none"] += 1
            if p.raw_place:
                fails.append(f"{url}: the data records a place only as an address or institution; the town was not recovered")
            continue
        # A / B -- the town and the country, both, where the data gives them
        if p.town not in text:
            fails.append(f"{url} shows no town, although the data records one")
        if p.country and p.country not in text:
            fails.append(f"{url} shows the town but not the country ({p.country}) the data gives")
        if p.country and f"{p.town}, {p.country}" not in text:
            fails.append(f"{url} does not give the town and country together as «{p.town}, {p.country}»")
        shown["both" if p.country else "town"] += 1
        # C -- no other place on the page: another known place, or the raw string when it was an address
        rest = text.replace(f"{p.town}, {p.country}", " ").replace(p.town, " ")
        if p.country:
            rest = rest.replace(p.country, " ")
        for other in sorted(place_names):
            if other and len(other) > 3 and re.search(r"\b" + re.escape(other) + r"\b", rest):
                fails.append(f"{url} shows another place, «{other}», beyond the town and country")
        if p.raw_place and p.raw_place.strip() not in (p.town, f"{p.town}, {p.country}") and p.raw_place in text:
            fails.append(f"{url} prints the raw place «{p.raw_place}», which is an address or an institution, "
                         "not a town and country")
        # C -- an address-like string anywhere in the person's own page
        if re.search(r"\b\d+\s+[A-Z][a-z]+\s+(Street|Road|Avenue|Lane|Drive|Close|Crescent)\b", text):
            fails.append(f"{url} contains an address-like string")

    # D -- nobody the data would call living is missing a `living` flag in the other direction
    for slug, q in pj.items():
        if q.get("living") and not any(p.slug == slug and p.living for p in people):
            fails.append(f"/people/{slug}/ is marked living in people.json and the rule says otherwise")

    if fails:
        print(f"  FAIL  places    {len(fails)} living-person place breach(es):")
        for f in dict.fromkeys(fails):
            print(f"          - {f}")
        print("          This archive's rule is a name, relationships, and the FULL TOWN AND COUNTRY - nothing more.")
        return 1
    print(f"  ok    places    {len(living)} living person(s): {shown['both']} with town and country, "
          f"{shown['town']} town only, {shown['none']} with no place recorded; no other place on their pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
