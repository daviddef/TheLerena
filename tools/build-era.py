#!/usr/bin/env python3
"""The place table behind the "at the time" notes: which Record Atlas region each birthplace on a person's page belongs to.

THE DECISION IS data/era-ground.tsv, written by hand: one row per birthplace string exactly as people.json prints it (the Birthplace row of every
person who is not living and not noindex), with the Atlas region it belongs to, or '-' for "looked at, and no region covers it", the reason, and
the town whose point (data/era-towns.tsv) lets the kit refuse a place that is within 15 km of its region's ring edge, outside the ring, or in a
neighbouring region's ring. This tool turns those rows into site/src/data/era-places.json and refuses to pass when the rows and the data disagree:

    python3 tools/build-era.py                       write site/src/data/era-places.json
    python3 tools/build-era.py --check               build gate: the file is what the rows build, every birthplace of a non-living, indexed person
                                                     has a row, and no row is stale
    python3 tools/build-era.py --snapshot <a copy of the Record Atlas>/site/public/context.json
                                                     also rebuild site/src/data/era-snapshot.json from the Atlas's versioned contract (the
                                                     deliberate refresh: nothing in a build ever reads the Atlas). The rings and bboxes come from
                                                     the contract itself (1.8.0 and later); there is no second file.
    python3 tools/build-era.py --living-urls         write the page paths the notes must never appear on (living, held-out and noindex people),
                                                     OUTSIDE the repository ($ERA_LIVING, or $XDG_STATE_HOME/lerena/era-living.json), for check:era

WHAT THIS ARCHIVE OFFERS A NOTE. A person's page prints ONE dated place-event: Born (the register's born_est) beside Birthplace. A death has no
place on the page, and "Where found" is the search that produced the person, with no date, so neither is an event. The note goes under the
Birthplace row. Of the 62 people the standard rollout added from acts (status unplaced), none has a birth date or a birthplace: they print no dated
place-event and so cannot carry a note.

THE REGISTER'S born_est IS OFTEN AN ESTIMATE (a year worked back from an age on a census or a ship list). A full date is taken as the register gives
it; a BARE YEAR is taken only where no era boundary of the region lies within ESTIMATE_YEARS of it (see site/src/lib/eraYear.js), so the note is true
for any year the estimate could stand for. That is stricter than the kit, never looser.

THE POLICY ON ERAS THE ATLAS HAS NOT ASSESSED. Some region eras of the contract still carry `contested` and `approx` as null (England, Scotland and
Santa Fe here): nobody has assessed them. The kit refuses such an era by default, which leaves no note at all, so this archive builds its snapshot
with --unassessed allow (David approved allow for now), on the record: the snapshot's policy says so, each note says which kind it rests on
(data-era-assessed), and the gate prints how many notes rest on an unassessed era. Dropping that flag below (then rebuilding) is the whole of going
strict. --outside-ring refuse is this archive's own, stricter, choice: a place whose point is outside its own region's ring is silent.

THE KIT'S OWN POLICIES, left at their defaults and recorded in the snapshot (kit/docs/era-notes.md, rule l): --approx margin, --contested scope,
--margin-years 5. An approximate or contested-about-its-bounds era is used only for a year more than max(5, the Atlas's margin) from each bound;
the near-edge place keeps its note only where the region across the edge has the same regime (--edge agree, the default).
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = ROOT / "site"
KIT_TOOLS = SITE / "node_modules" / "@daviddef" / "archive-kit" / "kit" / "tools"
DATA = SITE / "src" / "data"
GROUND = ROOT / "data" / "era-ground.tsv"
TOWNS = ROOT / "data" / "era-towns.tsv"
OUT = DATA / "era-places.json"
SNAP = DATA / "era-snapshot.json"
sys.path.insert(0, str(HERE))


def rows_of(path):
    for line in open(path, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        yield line.rstrip("\n").split("\t")


def ground():
    rows = {}
    for cols in rows_of(GROUND):
        if cols[0] == "place":
            continue
        place, region, why, town = (cols + ["", "", "", ""])[:4]
        if not place or not region or not why:
            raise SystemExit("era-ground.tsv: a row needs a place, a region (or '-') and a reason: %r" % cols[0][:60])
        if place in rows:
            raise SystemExit("era-ground.tsv: a place appears twice (a row must say one thing)")
        if region == "-" and town:
            raise SystemExit("era-ground.tsv: a place with no region has no town")
        rows[place] = (region, why, town)
    return rows


def towns():
    out = {}
    for cols in rows_of(TOWNS):
        if cols[0] == "town":
            continue
        out[cols[0]] = (float(cols[1]), float(cols[2]))
    return out


def people():
    return json.load(open(DATA / "people.json", encoding="utf-8"))


def has_name(s):
    """«-» is what a page prints for no place; it folds to nothing, and the kit refuses a table that holds one."""
    return any(c.isalnum() for c in str(s))


def birthplaces():
    """Every birthplace string a non-living, indexed person's page prints beside the Born row."""
    out = {}
    for p in people():
        if p.get("living") or p.get("noindex"):
            continue
        bp = p.get("birthplace")
        if bp and has_name(bp):
            out[bp] = out.get(bp, 0) + 1
    return out


def build():
    rows = ground()
    used = birthplaces()
    pts = towns()
    table = {}
    for place in sorted(rows):
        region, _, town = rows[place]
        if region == "-":
            table[place] = None
            continue
        table[place] = {"region": region}
        if town:
            if town not in pts:
                raise SystemExit("era-ground.tsv: town %r has no row in era-towns.tsv" % town)
            table[place].update(lat=pts[town][0], lon=pts[town][1])
    return rows, used, table


def living_path():
    if os.environ.get("ERA_LIVING"):
        return pathlib.Path(os.environ["ERA_LIVING"])
    base = os.environ.get("XDG_STATE_HOME") or str(pathlib.Path.home() / ".local" / "state")
    return pathlib.Path(base) / "lerena" / "era-living.json"


def living_urls():
    """Every page path a note must never be on: the living and the held-out (from tools/livingcheck.py, the independent reckoning every living
    gate here uses) and anybody people.json marks living or noindex. A held-out person has no page at all; the path is listed anyway."""
    import livingcheck as L
    pop, _lr, _year = L.population(ROOT)
    urls = set()
    for p in pop:
        if (p.living or getattr(p, "held", False)) and p.slug:
            urls.add("/people/%s/" % p.slug)
            urls.add("/who/%s/" % p.slug)
    for p in people():
        if p.get("living") or p.get("noindex"):
            urls.add("/people/%s/" % p["slug"])
    return sorted(urls)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--snapshot", default=None, help="a local copy of the Record Atlas's context.json (the versioned contract): also rebuild era-snapshot.json")
    ap.add_argument("--report", default=None, help="with --snapshot: write per-region counts of eras refused, and why, to this JSON file")
    ap.add_argument("--living-path", action="store_true", help="print where --living-urls writes, and stop")
    ap.add_argument("--living-urls", action="store_true", help="write the living / held-out / noindex page paths (JSON list) outside the repository and stop")
    a = ap.parse_args()
    if a.living_path:
        print(living_path())
        return 0
    if a.living_urls:
        urls = living_urls()
        if not urls:
            print("  FAIL  era-living  no living page found; a list of none would make the living gate a verdict on nothing")
            return 2
        fp = living_path()
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(json.dumps(urls, indent=0) + "\n", encoding="utf-8")
        try:
            os.chmod(fp, 0o600)
        except OSError:
            pass
        print("  era living list: %d page path(s), kept outside the repository" % len(urls))
        return 0
    rows, used, table = build()
    missing = sorted(set(used) - set(rows))
    stale = sorted(set(rows) - set(used))
    out = {"_about": "Built by tools/build-era.py from data/era-ground.tsv and data/era-towns.tsv. Birthplace as printed -> {region, lat, lon}, or null where no Atlas "
                     "region covers it. Read by kit erasnap.py.", "places": table}
    text = json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    if a.check:
        bad = False
        if missing:
            print("  FAIL  era-ground  %d birthplace(s) of a non-living, indexed person have no row in data/era-ground.tsv "
                  "(decide a region, or '-', for each)" % len(missing))
            bad = True
        if stale:
            print("  FAIL  era-ground  %d row(s) in data/era-ground.tsv match no birthplace (stale)" % len(stale))
            bad = True
        try:
            have = OUT.read_text(encoding="utf-8")
        except OSError:
            have = None
        if have != text:
            print("  FAIL  era-ground  site/src/data/era-places.json is not what the rows build (run tools/build-era.py)")
            bad = True
        if not bad:
            mapped = sum(1 for v in table.values() if v)
            print("  ok    era-ground  %d birthplaces decided (%d mapped to a region, %d to none); the table matches" % (len(table), mapped, len(table) - mapped))
        return 1 if bad else 0
    OUT.write_text(text, encoding="utf-8")
    print("era-places.json: %d birthplaces (%d mapped)" % (len(table), sum(1 for v in table.values() if v)))
    if missing:
        print("  WARNING %d birthplace(s) have no row in data/era-ground.tsv" % len(missing))
        return 1
    if a.snapshot:
        cmd = [sys.executable, str(KIT_TOOLS / "erasnap.py"), "--contract", a.snapshot,
               "--places", str(OUT), "--out", str(SNAP), "--unassessed", "allow", "--outside-ring", "refuse"]
        if a.report:
            cmd += ["--report", a.report]
        return subprocess.run(cmd).returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
