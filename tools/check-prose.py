#!/usr/bin/env python3
"""The living standard on what somebody TYPED: the kit's prose gate (checkprose.py), wired in.

    A living person (80 or younger, with no death recorded) is named with their relationships and their
    full town and country, and nothing else. (David, 16 October 2026.)

tools/check-living-standard.py guards what was BUILT; the kit's checkliving.py guards the built pages against the
dates the data attaches. Neither reads a sentence somebody wrote in a page, a note or a hand-edited data file. This
does, by handing the kit's tools/checkprose.py a FEED of who is living.

THE FEED IS WRITTEN OUTSIDE THE REPOSITORY, on every run, from the raw data and the estate's one rule (the kit's
living_rule.py, through tools/livingcheck.py - the same independent reckoning the other living gates use, not the
generator's answer). It holds each living person's id and the phrases a sentence might name them by, and `deadNames`:
every person the archive records as DEAD, so that a living person who shares a name with an ancestor is counted and
skipped rather than guessed at. deadNames comes from the dead rows, never from "everybody not on the living list".

WHY THE NAMES ARE NOT KEPT IN A TRACKED FILE FOR THE GATE. The standard allows a living person's name on the site, so
the names are not secret - but a gate configuration is exactly where a stray detail beside a name would live. The feed
lives in $LIVING_FEED, or $XDG_STATE_HOME/lerena/living-feed.json (default ~/.local/state/lerena/), and this file
reads the names out of the data each time rather than carrying them.

ALIASES. A sentence names somebody by the name they used then: a married surname is as much theirs as the one on the
register. The aliases added are the given name with the surname of each spouse the chart records for them.

EXIT CODES, passed through from the kit: 0 pass; 1 fail; 2 NOT RUN (no living person found, no feed, no kit). verify.sh
and CI both stop on any nonzero, so a run that could not look never counts as a pass.

The gate reads TRACKED files only, and fails on a matching file that is not tracked: `git add` first.
Usage:  python3 tools/check-prose.py [--root DIR]
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import livingcheck as L  # noqa: E402

KIT = pathlib.Path("site") / "node_modules" / "@daviddef" / "archive-kit" / "kit" / "tools"
ALLOW = pathlib.Path("data") / "_prose-allow.json"


def feed_path():
    if os.environ.get("LIVING_FEED"):
        return pathlib.Path(os.environ["LIVING_FEED"])
    base = os.environ.get("XDG_STATE_HOME") or str(pathlib.Path.home() / ".local" / "state")
    return pathlib.Path(base) / "lerena" / "living-feed.json"


def build_feed(root):
    people, lr, year = L.population(root)
    spouses = {}
    for who, rel, oth, *_ in L.edges(root):
        if rel == "spouse":
            spouses.setdefault(who, set()).add(oth)
            spouses.setdefault(oth, set()).add(who)
    living, dead = [], set()
    first = {}
    for p in people:
        g = L.fold(p.name).split()[0] if L.fold(p.name).split() else ""
        first[g] = first.get(g, 0) + 1
    for p in people:
        if p.dead:
            dead |= L.name_variants(p.name)
    for p in people:
        if not (p.living or getattr(p, "held", False)):
            continue
        names = set(L.name_variants(p.name))
        given = p.name.split()[0] if p.name.split() else ""
        for sp in spouses.get(p.name, ()):
            sur = sp.split()[-1] if sp.split() else ""
            if given and sur and len(sur) > 3:
                names.add(f"{given} {sur}")
                names.add(f"{given} {sur.title()}")
        # THE GIVEN NAME ALONE ("X was fifteen"), but only when nobody else in the archive, living or dead,
        # starts with it: then it can only be this person. Otherwise it would be a guess.
        gf = L.fold(p.name).split()[0] if L.fold(p.name).split() else ""
        uniq_given = given if (gf and len(gf) > 4 and first.get(gf, 0) == 1) else ""
        # an alias that is also a DEAD person's name is the dead person's, not this one's
        names = {n for n in names if n not in dead}
        living.append({"id": p.slug or f"p{len(living)}", "names": sorted(names), "given": uniq_given})
    return {"living": living, "deadNames": sorted(dead)}


# THE KIT'S GATE SKIPS A ONE-WORD NAME ON PURPOSE (a lone given name is a guess). "Anna was told in 2020 ..." names a
# living person as plainly as a full name does, though, and the archive's own testimony log is written that way. So THIS
# supplements it, for one case only: a living person's GIVEN NAME ALONE, when nobody else in the archive starts with it,
# beside a year, a full date, a month and year, or a life-event word, inside one line or paragraph. It reads the same
# files the kit reads, prints counts and places and never a name, and proves itself on a planted sentence first.
YEAR = r"\b(?:1[89]\d\d|20\d\d)\b"
MON = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?"
DETAIL = re.compile(YEAR + r"|\b\d{1,2}\s+" + MON + r"\b|\b" + MON + r"\s+\d{4}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|"
                    r"\b(?:died|buried|baptised|baptized|christened|funeral|obituary|aged|born)\b", re.I)


def given_scan(root, feed, files, no_git=False):
    givens = sorted({e["given"] for e in feed["living"] if e.get("given")})
    if not givens:
        return None, "no unique given name to look for"
    rx = re.compile(r"(?<![\w'])(?:" + "|".join(re.escape(g) for g in givens) + r")(?![\w])")
    n_files = n_places = 0
    fails = []
    for f in files:
        t = (root / f).read_text(encoding="utf-8", errors="ignore")
        n_files += 1
        for blk in re.split(r"\n\s*\n|\n", t):
            for m in rx.finditer(blk):
                n_places += 1
                if DETAIL.search(blk[max(0, m.start() - 150): m.end() + 150]):
                    fails.append(f)
                    break
    return (n_files, n_places, sorted(set(fails)), len(fails)), ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent))
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    kit = root / KIT / "checkprose.py"
    if not kit.exists():
        print(f"  --    prose      not run: {kit.relative_to(root)} is missing - the kit pin must be 575409a or later "
              "and `npm install` run in site/")
        return 2
    feed = build_feed(root)
    if not feed["living"]:
        print("  --    prose      not run: the reckoning found nobody living, so there is nothing to scan for. "
              "That is itself wrong for this archive - see data/living-roster.tsv")
        return 2
    fp = feed_path()
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(json.dumps(feed, ensure_ascii=False), encoding="utf-8")
    try:
        os.chmod(fp, 0o600)
    except OSError:
        pass

    # Hand-edited data files that name a living person are read too; GENERATED data (site/src/data) stays with
    # its generator's own scrub gate. A file is "hand-edited" if it is a tracked data/*.tsv or *.txt.
    no_git = os.environ.get("LIVING_PROSE_NO_GIT") == "1"        # tests only: a scratch copy has no .git
    if no_git:
        tracked = [str(f.relative_to(root)) for f in root.rglob("*")
                   if f.is_file() and not any(x in f.parts for x in ("node_modules", "dist", ".git", ".astro"))]
    else:
        tracked = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True).stdout.split("\n")
    phrases = [re.compile(re.escape(n).replace(r"\ ", r"\s+"), re.I)
               for e in feed["living"] for n in e["names"]]
    includes = []
    for f in tracked:
        if f.startswith("data/") and f.endswith((".tsv", ".txt")):
            t = (root / f).read_text(encoding="utf-8", errors="ignore")
            if any(r.search(t) for r in phrases):
                includes.append(f)
    # book.json (17 October 2026) is hand-edited: every chapter title, blurb and part paragraph is typed. It is a tracked
    # data file the kit's default file set does not reach, so it is named here, like the components and layouts.
    # story.json (25 October 2026) is hand-edited too: the whole text of /story/, and it names the living generation.
    # flag-countries.json (27 October 2026) is hand-edited: this archive's own country for a ribbon card's place, with the
    # evidence for each in its words. ribbon-flags.json beside it is GENERATED (tools/build-ribbon-flags.py, with the kit's
    # ribbonflags.py), names no person, and is held by the kit's gate (check:ribbonflags: no year on a living card's flag).
    for extra in ("requests/*.md", "site/src/components/*.astro", "site/src/layouts/*.astro", "site/src/data/book.json",
                  "site/src/data/story.json", "site/src/data/flag-countries.json"):
        includes.append(extra)

    cmd = [sys.executable, str(kit), "--root", str(root), "--feed", str(fp)]
    # The story's ribbon card for the living generation (kit docs/story.md) carries five structural fields beside the name,
    # relationships and place the default allows: the card's chapter and glyph, the origin (her town) and its grade, the
    # page slug as `person`, and the spouse's living flag. None is a detail about the person; a year, a date or a
    # life-event word in any field still fails, as everywhere else.
    cmd += ["--allow-keys", "chapter,glyph,origin,originGrade,person,spouseLiving"]
    for f in includes:
        cmd += ["--include", f]
    if (root / ALLOW).exists():
        cmd += ["--allow", str(root / ALLOW)]
    if no_git:
        cmd += ["--no-git"]
    print(f"  feed: {len(feed['living'])} living person(s), {len(feed['deadNames'])} dead name(s), "
          f"{len(includes)} data/extra include(s); kept outside the repository")
    r = subprocess.run(cmd, cwd=root)

    # --- the supplement: a unique given name alone, beside a detail ---
    import fnmatch
    defaults = [f for f in tracked if f.startswith(("site/src/pages/", "site/src/content/", "notes/", "docs/"))
                or ("/" not in f and f.endswith(".md"))]
    extra = [f for f in tracked if any(fnmatch.fnmatch(f, g) for g in includes)]
    files = sorted({f for f in defaults + extra if (root / f).is_file() and f.endswith(
        (".astro", ".md", ".tsv", ".txt", ".json", ".mjs", ".js", ".ts", ".html"))})
    # self-proof: a planted sentence must be caught before the real run counts for anything
    givens = [e["given"] for e in feed["living"] if e.get("given")]
    for g in givens[:1]:
        probe = f"{g} was told in 1899 that it was so."
        rx = re.compile(r"(?<![\w'])" + re.escape(g) + r"(?![\w])")
        if not (rx.search(probe) and DETAIL.search(probe)):
            print("  FAIL  prose      the given-name supplement could not catch its own planted sentence")
            return 1
    res, why = given_scan(root, feed, files, no_git)
    if res is None:
        print(f"  --    prose      given-name supplement not run: {why}")
        sup = 0
    else:
        n_files, n_places, bad, nbad = res
        print(f"  given-name supplement: {n_files} files read, {n_places} place(s) name a living person by given name alone, "
              f"{nbad} carry a detail")
        for f in bad:
            print(f"    - {f}: a living person's given name beside a date, year or life-event word")
        sup = 1 if nbad else 0
    return 1 if (r.returncode == 1 or sup) else r.returncode


if __name__ == "__main__":
    sys.exit(main())
