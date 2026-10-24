#!/usr/bin/env python3
"""Plant a fault for every living-people rule and show the gate catches it.

A GATE THAT CAN ONLY PASS PROVES NOTHING. Every rule in tools/check-living-standard.py and
tools/check-living-places.py has a control here: the unmodified build is checked first and must
pass (the positive control); then a COPY has one fault planted and the gate must fail on exactly
that rule. The real files are never touched.

Planted values are ones no living person can have (the year 1799, a name that is nobody's). The
living person's real date is held NOWHERE in this repository (the roster records who is living with
no date), so this file never contains one and never needs to: faults are planted with the year 1799.

Also proved here, against the generator and the shared rule:
  - the 80-year bound moves the line (80 is living, 81 is not), in the shared rule and in the generator;
  - a recorded death, and a public-source citation, each make a young person not living;
  - the two people recorded dead only by a burial registration cannot be marked living, and the net
    catches it if the burial rows are ever lost;
  - an undated person with a living parent is held out of people.json, and the standard gate fails if the
    row is committed; a child with a KNOWN birth year is not held out but is a living person like any other;
  - the roster: an empty roster, a roster holding a digit, a roster naming a dead person, and a date put back
    in each of the four files that once held it, are all refused;
  - a planted living person in the register is scrubbed to name, relationships, town, country;
  - (25 October 2026) a public-source citation does NOT make a DATED person under 81 "not living" (the kit's rule would);
    tools/check-living-years.py fails on a birth on or after the living line (this year minus 80) printed anywhere,
    built or committed, for a person with no death beside it - a year in prose, in a commit message, in a data row,
    in JSON-LD - and the line moves with the calendar; the registry of unpublished deaths is enforced both ways;
    and a living person's date is withheld from a commit message before /changes/ prints it.

Usage:  python3 tools/test-living-gates.py [--dist site/dist-wt] [--full]
   --full  also runs two real builds in scratch copies (a planted living person, and a planted leak).
"""
import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import livingcheck as L  # noqa: E402

STD = HERE / "check-living-standard.py"
PLC = HERE / "check-living-places.py"
YRS = HERE / "check-living-years.py"
results = []


def run(gate, root, dist, env=None):
    e = dict(os.environ)
    e.pop("ARCHIVE_OUT", None)
    e.update(env or {})
    r = subprocess.run([sys.executable, str(gate), "--root", str(root), "--dist", str(dist)],
                       capture_output=True, text=True, env=e)
    return r.returncode, r.stdout + r.stderr


def scratch(src_dist):
    """A cheap copy of everything the gates read: data, generated data, tools, the kit (linked), dist."""
    t = pathlib.Path(tempfile.mkdtemp(prefix="living-gates-"))
    for rel in ("data", "tools", "notes", "site/src/data"):
        (t / rel).parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-Rc", str(ROOT / rel), str(t / rel)], check=True)
    (t / "site" / "node_modules" / "@daviddef").mkdir(parents=True, exist_ok=True)
    os.symlink(ROOT / "site" / "node_modules" / "@daviddef" / "archive-kit",
               t / "site" / "node_modules" / "@daviddef" / "archive-kit")
    subprocess.run(["cp", "-Rc", str(src_dist), str(t / "dist")], check=True)
    return t


def case(label, gate, expect, mutate, dist, env=None, expect_pass=False):
    """expect: substring that must appear in the failure output (or None for a must-pass control)."""
    t = scratch(dist)
    try:
        mutate(t)
        code, out = run(gate, t, t / "dist", env)
    finally:
        shutil.rmtree(t, ignore_errors=True)
    if expect_pass:
        ok = code == 0
        results.append((ok, label, "passes" if ok else "FAILED: " + out.strip().splitlines()[-1][:160]))
    else:
        ok = code == 1 and expect in out
        results.append((ok, label, "caught" if ok else f"NOT CAUGHT (exit {code}): {out.strip()[:200]}"))


def page(t, rel):
    return t / "dist" / rel / "index.html"


def edit(path, fn):
    s = path.read_text(encoding="utf-8")
    path.write_text(fn(s), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(ROOT / "site" / "dist"))
    ap.add_argument("--full", action="store_true")
    a = ap.parse_args()
    dist = pathlib.Path(a.dist)
    if not (dist / "people").exists():
        raise SystemExit(f"no build at {dist}: build first (ARCHIVE_OUT=dist-wt npm run build)")

    people, lr, year = L.population(ROOT)
    live = [p for p in people if p.living]
    if not live:
        raise SystemExit("the rule finds nobody living: these controls need one living person in the data")
    C = next((p for p in live if p.roster and (p.roster.get("town") or "").strip()), live[0])   # the living person the controls are aimed at (one with a town on the roster)
    cslug = C.slug
    CD = "14 Oct 1799"                            # a date no living person can have

    # ---------------- positive controls: the real build passes both gates -------------------------
    case("POSITIVE  real build passes the standard gate", STD, None, lambda t: None, dist, expect_pass=True)
    case("POSITIVE  real build passes the places gate", PLC, None, lambda t: None, dist, expect_pass=True)
    case("POSITIVE  real build passes the living-years gate", YRS, None, lambda t: None, dist, expect_pass=True)

    # ---------------- check-living-standard.py ----------------------------------------------------
    def drop_noindex(t):
        edit(page(t, f"people/{cslug}"), lambda s: re.sub(r'<meta name="robots"[^>]*noindex[^>]*>', "", s))
    case("b  living page without noindex", STD, "lacks <meta name=robots noindex>", drop_noindex, dist)

    def in_sitemap(t):
        edit(t / "dist" / "sitemap.xml", lambda s: s.replace("</urlset>",
             f"<url><loc>https://x.invalid/people/{cslug}/</loc></url></urlset>"))
    case("b  living page in the sitemap", STD, "is in sitemap.xml", in_sitemap, dist)

    def in_search(t):
        f = t / "dist" / "searchindex.json"
        j = json.loads(f.read_text(encoding="utf-8"))
        j.append({"k": "Person", "t": "planted", "s": "", "h": f"/people/{cslug}/", "q": "planted"})
        f.write_text(json.dumps(j), encoding="utf-8")
    case("b  living page in the search index", STD, "is in the search index", in_search, dist)

    def jsonld(t):
        edit(page(t, f"people/{cslug}"), lambda s: s.replace("</head>",
             '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Person","name":"x"}</script></head>', 1))
    case("b  living page carrying Person JSON-LD", STD, "carries Person structured data", jsonld, dist)

    def table(t):
        edit(page(t, f"people/{cslug}"), lambda s: s.replace("</main>", "<table><tr><td>x</td></tr></table></main>", 1))
    case("b  living page with a table", STD, "has a table", table, dist)

    def image(t):
        edit(page(t, f"people/{cslug}"), lambda s: s.replace("</main>", '<img src="/x.jpg" alt=""></main>', 1))
    case("b  living page with an image", STD, "has an image", image, dist)

    def year_(t):
        edit(page(t, f"people/{cslug}"), lambda s: s.replace("</main>", "<p>1799</p></main>", 1))
    case("b  living page showing a year (1799)", STD, "shows a year (1799)", year_, dist)

    def date_elsewhere(t):
        edit(page(t, "about"), lambda s: s.replace("</main>", f"<p>{C.name}, b. {CD}</p></main>", 1))
    case("c  a date against a living person's name on a built page", STD, "puts a date against a living person's name", date_elsewhere, dist)

    def date_json(t):
        (t / "dist" / "leak.json").write_text(json.dumps({"x": f"{C.name} {CD}"}), encoding="utf-8")
    case("c  ... or in any served file", STD, "leak.json puts a date", date_json, dist)

    def date_committed(t):
        with open(t / "data" / "relations.tsv", "a", encoding="utf-8") as f:
            f.write(f"# a planted note: {C.name}, b. {CD}\n")
    case("c  ... or in any committed file", STD, "committed file data/relations.tsv puts a date", date_committed, dist)

    # the four files that once held her full birth date: put a date back in each, expect a refusal
    def put_back(rel, how):
        def m(t):
            f = t / rel
            s0 = f.read_text(encoding="utf-8")
            f.write_text(how(s0), encoding="utf-8")
        return m
    cell = lambda s0: re.sub(r"(?m)^(.*\t?)(" + re.escape(C.name.split()[0]) + r" Anne[^\t\n]*)\t\t", lambda m_: m_.group(1) + m_.group(2) + "\t" + CD + "\t", s0, count=1)
    case("c  a date put back in data/direct-line.tsv", STD, "committed file data/direct-line.tsv puts a date",
         put_back("data/direct-line.tsv", cell), dist)
    case("c  a date put back in data/lerena-siblings-gen3.tsv", STD, "committed file data/lerena-siblings-gen3.tsv puts a date",
         put_back("data/lerena-siblings-gen3.tsv", cell), dist)
    # (These two used to substitute into a sentence that no longer exists in the notes, changed nothing, and so
    # proved nothing; 25 October 2026 they append, so they always plant.)
    case("c  a date put back in notes/compared-with-the-defranceski-archive.md", STD, "compared-with-the-defranceski-archive.md puts a date",
         put_back("notes/compared-with-the-defranceski-archive.md", lambda s0: s0.rstrip("\n") + f"\n\n{C.name}, born {CD}\n"), dist)
    case("c  a year put back in notes/findings.md", STD, "notes/findings.md puts a date",
         put_back("notes/findings.md", lambda s0: s0.rstrip("\n") + f"\n\n{C.name} 1799 (living)\n"), dist)

    # the roster
    def roster_empty(t):
        (t / "data" / "living-roster.tsv").write_text("name\tslug\ttown\tcountry\tbasis\n", encoding="utf-8")
    case("r  an empty roster", STD, "living-roster.tsv is empty or missing", roster_empty, dist)

    def roster_digit(t):
        edit(t / "data" / "living-roster.tsv", lambda s: s.rstrip("\n") + " 1799\n")
    case("r  a date in the roster", STD, "holds a digit", roster_digit, dist)

    def roster_dead(t):
        with open(t / "data" / "living-roster.tsv", "a", encoding="utf-8") as f:
            f.write("Gayle LERENA (born PRESTON)\tgayle-lerena\tPlanted\tPlanted\tplanted\n")
    case("r  a roster row naming a person the data records dead", STD, "refused: a recorded death", roster_dead, dist)

    def whocanon(t):
        edit(page(t, f"who/{cslug}"), lambda s: re.sub(r'<meta name="robots"[^>]*noindex[^>]*>', "", s))
    case("d  name page of only-living bearers, not noindex", STD, "names only living people and is not noindex", whocanon, dist)

    def whocanon2(t):
        edit(page(t, f"who/{cslug}"), lambda s: s.replace("</head>", '<link rel="canonical" href="https://x.invalid/elsewhere/"></head>', 1))
    case("d  name page naming a canonical elsewhere", STD, "names a canonical elsewhere", whocanon2, dist)

    def known_child(t):
        row = "\t".join(["Planted Minor LERENA", "2015", "Montevideo", "Uruguayan", "-", "Montevideo", "planted", "UNPLACED", "", ""])
        with open(t / "data" / "lerena-register.tsv", "a", encoding="utf-8") as f:
            f.write(row + "\n")
    case("c  a KNOWN child's year committed in the register (a child is a living person: no date in a public file)",
         STD, "puts a date against a living person's name", known_child, dist)

    def undated_child(t):
        with open(t / "data" / "lerena-register.tsv", "a", encoding="utf-8") as f:
            f.write("\t".join(["Planted Child LERENA", "-", "-", "-", "-", "Montevideo", "planted", "UNPLACED", "", ""]) + "\n")
        with open(t / "data" / "relations.tsv", "a", encoding="utf-8") as f:
            f.write("\t".join([C.name, "child", "Planted Child LERENA", "", "register", "planted"]) + "\n")
    case("e  an undated person with a living parent (held out), committed", STD, "HELD-OUT person", undated_child, dist)

    def child_page(t):
        undated_child(t)
        edit(page(t, "about"), lambda s: s.replace("</main>", "<p>Planted Child LERENA</p></main>", 1))
    case("e  ... and on a built page", STD, "appears in about/index.html", child_page, dist)

    def unbuilt(t):
        shutil.rmtree(t / "dist" / "people" / "paul-raymond-lerena")
    case("f  a named person whose page was not built", STD, "/people/paul-raymond-lerena/", unbuilt, dist)

    def noslug(t):
        f = t / "site" / "src" / "data" / "people.json"
        j = json.loads(f.read_text(encoding="utf-8"))
        for p in j:
            if p["slug"] == "nuno-fernando-lerena":
                p["children"][0]["slug"] = ""
        f.write_text(json.dumps(j), encoding="utf-8")
    case("f  a relative named in a chart with no page", STD, "who has no person page", noslug, dist)

    def unlinked(t):
        edit(page(t, "people/nuno-fernando-lerena"),
             lambda s: s.replace('<a class="node', '<div class="node', 1).replace("</a>", "</div>", 1))
    case("f  a name drawn in a chart with no link", STD, "in its chart with no link", unlinked, dist)

    def flip(t):
        f = t / "site" / "src" / "data" / "people.json"
        j = json.loads(f.read_text(encoding="utf-8"))
        for p in j:
            if p["slug"] == cslug:
                p["living"] = False
        f.write_text(json.dumps(j), encoding="utf-8")
    case("a  the generator calls a living person not living", STD, "by the rule and not living in people.json", flip, dist)

    def ghost(t):
        f = t / "site" / "src" / "data" / "people.json"
        j = json.loads(f.read_text(encoding="utf-8"))
        g = dict(j[0]); g["slug"] = "planted-ghost"; g["name"] = "Planted Ghost"
        j.append(g)
        f.write_text(json.dumps(j), encoding="utf-8")
    case("a  a person in people.json that nobody's data accounts for", STD, "nobody in the data accounts for them", ghost, dist)

    def hidden(t):
        f = t / "site" / "src" / "data" / "people.json"
        j = [p for p in json.loads(f.read_text(encoding="utf-8")) if p["slug"] != cslug]
        f.write_text(json.dumps(j), encoding="utf-8")
    case("a  a living person the generator dropped", STD, "has no entry in people.json", hidden, dist)

    def lose_burials(t):
        f = t / "data" / "johannesburg-cemetery-1999.tsv"
        f.write_text("# emptied for the control\nperson\twhat the register gives\tark\twhat it settles\n", encoding="utf-8")
    case("h  the two burial-only deaths lost from the data: marked living", STD, "speaks of a death, burial", lose_burials, dist)

    def empty_dist(t):
        shutil.rmtree(t / "dist"); (t / "dist").mkdir()
    case("g  an empty build (standard gate)", STD, "refusing to pass on an empty build", empty_dist, dist)
    case("g  an empty build (places gate)", PLC, "refusing to pass on an empty build", empty_dist, dist)

    def no_register(t):
        (t / "data" / "lerena-register.tsv").write_text("name\tborn_est\n", encoding="utf-8")
    case("g  a reckoning that found nobody", STD, "the register was not read", no_register, dist)

    # ---------------- check-living-years.py (25 October 2026) --------------------------------------
    def about_adds(txt):
        return lambda t: edit(page(t, "about"), lambda s_: s_.replace("</main>", f"<p>{txt}</p></main>", 1))
    case("Y  a birth year in prose on a built page, no death beside it", YRS, "prints a birth (1990",
         about_adds("Planted Person, b. 1990, lived in Plantedville."), dist)
    case("Y  ... a full birth date", YRS, "prints a birth (1990", about_adds("Planted Person was born 24 April 1990."), dist)
    case("Y  ... an open life span", YRS, "prints a birth (1990", about_adds("Planted Person (1990-) of Plantedville."), dist)
    case("Y  ... the same birth WITH a death beside it is fine", YRS, None, about_adds("Planted Person, b. 1990, d. 2001."), dist, expect_pass=True)
    case("Y  ... and 'born and died' is a death", YRS, None, about_adds("A baby, born and died 1990."), dist, expect_pass=True)

    def ld_birth(t):
        edit(page(t, "about"), lambda s_: s_.replace("</head>", '<script type="application/ld+json">{"@type":"Person","name":"Planted Person","birthDate":"1990-04-24"}</script></head>', 1))
    case("Y  structured data: a Person birthDate", YRS, "prints a birth (1990", ld_birth, dist)

    def served_json(t):
        (t / "dist" / "leak.json").write_text(json.dumps({"x": "Planted Person (b. 1991)"}), encoding="utf-8")
    case("Y  a birth in any served data file", YRS, "leak.json prints a birth (1991", served_json, dist)

    def commit_text(t):
        f = t / "site" / "src" / "data" / "changes.json"
        j = json.loads(f.read_text(encoding="utf-8"))
        j["days"][0]["commits"][0]["body"] += "\nHe recorded Planted Person (b.1947) by mistake."
        f.write_text(json.dumps(j), encoding="utf-8")
    case("Y  a birth typed into a commit message (what /changes/ prints, and what once leaked)", YRS,
         "site/src/data/changes.json prints a birth (1947", commit_text, dist)

    def note_adds(t):
        with open(t / "notes" / "findings.md", "a", encoding="utf-8") as f:
            f.write("\nPlanted Person (b. 1992) is a cousin.\n")
    case("Y  a birth in a research note (the repository is public)", YRS, "committed file notes/findings.md prints a birth (1992", note_adds, dist)

    def tsv_adds(t):
        with open(t / "data" / "passenger-lists.tsv", "a", encoding="utf-8") as f:
            f.write("Planted Traveller\tx\tarr. 1 Jan 1999\tx\tx\tx\tb. 1949\tx\tx\tx\n")
    case("Y  a birth in a committed data row", YRS, "committed file data/passenger-lists.tsv prints a birth (1949", tsv_adds, dist)

    # the line: 1945 is below it, 1946 on it (2026); in 2027 the line is 1947
    case("Y  the line: a birth in 1945 is below it", YRS, None, about_adds("Planted Person, b. 1945."), dist, expect_pass=True)
    case("Y  the line: a birth in 1946 is on it (2026 - 80)", YRS, "prints a birth (1946", about_adds("Planted Person, b. 1946."), dist)
    case("Y  the line moves with the calendar: in 2027 a birth in 1946 is below it", YRS, None, about_adds("Planted Person, b. 1946."), dist,
         env={"LIVING_TODAY_YEAR": "2027"}, expect_pass=True)
    case("Y  ... and 1947 is on it in 2027", YRS, "prints a birth (1947", about_adds("Planted Person, b. 1947."), dist,
         env={"LIVING_TODAY_YEAR": "2027"})

    # a dead person's name excuses a birth only when the year agrees
    dead_y = [p for p in people if p.dead and p.by is not None and p.by >= L.current_cutoff(lr, year)]
    if dead_y:
        D0 = dead_y[0]
        fn = D0.name.split("(")[0].strip()
        case(f"Y  a recorded-dead person's name beside their own birth year is excused", YRS, None,
             about_adds(f"{fn}, b. {D0.by}."), dist, expect_pass=True)
        case("Y  ... but not beside a year ten years later (a living namesake)", YRS, "prints a birth",
             about_adds(f"{fn}, b. {D0.by + 10}."), dist)

    def snip(t):
        edit(t / "data" / "living-year-allow.json", lambda s_: s_.replace('"snippets": [', '"snippets": [{"file": "*", "contains": "Planted Person, b. 1990", "reason": "planted"},', 1))
    case("Y  the registry's snippet excuses exactly its text", YRS, None,
         lambda t: (snip(t), about_adds("Planted Person, b. 1990, lived in Plantedville.")(t)), dist, expect_pass=True)

    def reg_edit(fn):
        def m(t):
            f = t / "data" / "living-year-allow.json"
            j = json.loads(f.read_text(encoding="utf-8"))
            fn(j)
            f.write_text(json.dumps(j), encoding="utf-8")
        return m
    drop_registry = reg_edit(lambda j: j.__setitem__("unpublished_deaths", [e for e in j["unpublished_deaths"] if e["slug"] != "paul-raymond-lerena"]))
    case("Y  a person the data records dead, whose page prints no death, left out of the registry", YRS, "does not list them", drop_registry, dist)

    stale_registry = reg_edit(lambda j: j["unpublished_deaths"].append({"slug": "cheryl-anne-lerena", "reason": "planted"}))
    case("Y  a registry entry the data no longer supports (a living woman)", YRS, "delete the entry", stale_registry, dist)
    no_reason = reg_edit(lambda j: j["unpublished_deaths"].append({"slug": "gayle-lerena", "reason": ""}))
    case("Y  a registry entry with no reason", YRS, "no slug or no reason", no_reason, dist)
    case("Y  an empty build (living-years gate)", YRS, "refusing to pass on an empty build", empty_dist, dist)
    case("Y  a reckoning that found nobody (living-years gate)", YRS, "the register was not read", no_register, dist)


    # ---------------- check-living-places.py ------------------------------------------------------
    town, country = C.town, C.country

    def no_place(t):
        edit(page(t, f"people/{cslug}"), lambda s: s.replace(f"{town}, {country}", ""))
    case("A  a living page that shows no town and country", PLC, "shows no town", no_place, dist)

    def town_only(t):
        edit(page(t, f"people/{cslug}"), lambda s: s.replace(f"{town}, {country}", town))
    case("B  a town without its country", PLC, "shows the town but not the country", town_only, dist)

    def other_place(t):
        edit(page(t, f"people/{cslug}"), lambda s: s.replace("</main>", "<p>Rosario, Santa Fe</p></main>", 1))
    case("C  another place on a living page", PLC, "shows another place", other_place, dist)

    def street(t):
        edit(page(t, f"people/{cslug}"), lambda s: s.replace("</main>", "<p>42 Planted Street</p></main>", 1))
    case("C  an address-like string on a living page", PLC, "address-like string", street, dist)

    def wrong_json(t):
        f = t / "site" / "src" / "data" / "people.json"
        j = json.loads(f.read_text(encoding="utf-8"))
        for p in j:
            if p["slug"] == cslug:
                p["town"] = "Planted"
        f.write_text(json.dumps(j), encoding="utf-8")
    case("D  the generator holds a different town", PLC, "people.json holds town", wrong_json, dist)

    # ---------------- the generator and the shared rule ---------------------------------------------
    def gen_in_scratch(t, env=None):
        e = dict(os.environ); e.update(env or {})
        r = subprocess.run([sys.executable, str(t / "tools" / "build-people.py")], capture_output=True, text=True, env=e)
        return r

    def check(label, ok, detail=""):
        results.append((bool(ok), label, ("proved" if ok else "NOT PROVED: " + detail)))

    # 80 is living, 81 is not; a death and a public source each mean not living
    check("rule  born 80 years ago is living; 81 is not",
          lr.is_living(2000, False, [], 2080) and not lr.is_living(2000, False, [], 2081))
    check("rule  a recorded death means not living, however young",
          not lr.is_living(2005, True, [], 2026))
    check("rule  THE KIT'S GAP, kept visible: its is_living says a FamilySearch citation makes a person born 2005 not living "
          "(a private tree entry does not); this archive never passes a dated person's citations (cites_for_living)",
          not lr.is_living(2005, False, ["FamilySearch Family Tree"], 2026)
          and lr.is_living(2005, False, ["MyHeritage family tree"], 2026)
          and lr.is_living(2005, False, L.cites_for_living(2005, ["FamilySearch Family Tree"]), 2026)
          and not lr.is_living(None, False, L.cites_for_living(None, ["FamilySearch Family Tree"]), 2026))
    check("rule  the independent reckoning (livingcheck) and the generator withhold the citation the same way, and a recorded "
          "death still beats everything",
          L.cites_for_living(1950, ["FamilySearch"]) == [] and L.cites_for_living(None, ["FamilySearch"]) == ["FamilySearch"]
          and not lr.is_living(1950, True, L.cites_for_living(1950, ["FamilySearch"]), 2026))
    check("line  the living line is derived: this year minus 80, 1946 in 2026 and 1947 in 2027",
          L.current_cutoff(lr, 2026) == 1946 and L.current_cutoff(lr, 2027) == 1947)
    check("rule  no birth year is not living", not lr.is_living(None, False, [], 2026))
    check("rule  an undated person with a living parent is held out; a child with a known year, and the dead, are not",
          lr.possible_minor(None, False, [], True, 2026) and not lr.possible_minor(2015, False, [], True, 2026)
          and not lr.possible_minor(None, True, [], True, 2026) and not lr.possible_minor(None, False, [], False, 2026))

    # the two people recorded dead only by a burial registration
    by_slug = {p.slug: p for p in people}
    for s in ("gayle-lerena", "jeffrey-lerena"):
        p = by_slug.get(s)
        check(f"dead  /people/{s}/ is not living by the rule", p is not None and not p.living and p.dead)
    pj = {p["slug"]: p for p in json.loads((ROOT / "site/src/data/people.json").read_text(encoding="utf-8"))}
    for s in ("gayle-lerena", "jeffrey-lerena"):
        check(f"dead  /people/{s}/ is not living in people.json", s in pj and not pj[s]["living"] and not pj[s]["noindex"])

    # a planted living person, a planted minor and a planted public-source person through the real generator
    t = scratch(dist)
    try:
        reg = t / "data" / "lerena-register.tsv"
        rows = [
            ["Planted Living LERENA", "2001-03-05", "Hospital Planted, 12 Planted Street, Plantedville, Uruguay", "Uruguayan",
             "student", "Plantedville, Uruguay", "A private family tree, planted", "UNPLACED", "a planted note 1799", ""],
            ["Planted Minor LERENA", "2015", "Plantedville, Uruguay", "Uruguayan", "-", "Plantedville, Uruguay",
             "planted", "UNPLACED", "", ""],
            ["Planted Child LERENA", "-", "-", "-", "-", "Plantedville, Uruguay", "planted", "UNPLACED", "", ""],
            ["Planted Edge LERENA", "1946", "Plantedville, Uruguay", "Uruguayan", "-", "Plantedville, Uruguay",
             "planted", "UNPLACED", "", ""],
            ["Planted Public LERENA", "2001", "Plantedville, Uruguay", "Uruguayan", "-", "Plantedville, Uruguay",
             "FamilySearch, planted record", "UNPLACED", "", ""],
        ]
        with open(reg, "a", encoding="utf-8") as f:
            for r in rows:
                f.write("\t".join(r) + "\n")
        with open(t / "data" / "relations.tsv", "a", encoding="utf-8") as f:
            f.write("\t".join(["Planted Living LERENA", "father", "Nuno Fernando LERENA", "", "register", "planted 1799"]) + "\n")
            f.write("\t".join(["Planted Minor LERENA", "father", "Nuno Fernando LERENA", "", "register", "planted"]) + "\n")
            f.write("\t".join(["Planted Living LERENA", "child", "Planted Child LERENA", "", "register", "planted"]) + "\n")
        r = gen_in_scratch(t)
        ok = r.returncode == 0
        j = {p["slug"]: p for p in json.loads((t / "site/src/data/people.json").read_text(encoding="utf-8"))} if ok else {}
        pl = j.get("planted-living-lerena", {})
        check("generator  runs on the planted register", ok, r.stderr[-200:])
        check("generator  a planted living person is living and noindex", pl.get("living") is True and pl.get("noindex") is True)
        bare = {k: v for k, v in pl.items() if v not in ("", [], None, False)}
        allowed = {"slug", "name", "surname", "living", "noindex", "town", "country", "status", "statusRaw", "isLine",
                   "father", "mother", "siblings", "spouses", "children", "relTotal", "relRegister", "relTree"}
        check("generator  ... scrubbed to name, relationships, town and country (no field beyond them)",
              ok and set(bare) <= allowed, str(sorted(set(bare) - allowed)))
        check("generator  ... town reduced from an institution and street to the town, and the country kept",
              pl.get("town") == "Plantedville" and pl.get("country") == "Uruguay", f"{pl.get('town')!r}, {pl.get('country')!r}")
        blob = json.dumps(pl)
        check("generator  ... none of the planted date, note or occupation reaches the JSON",
              not any(x in blob for x in ("2001", "1799", "student", "Hospital", "Street", "private family tree")))
        check("generator  an undated person with a living parent is held out of people.json",
              "planted-child-lerena" not in j and "Planted Child" not in json.dumps(j))
        check("generator  ... and is nobody's relative",
              all("Planted Child" not in c["name"] for p_ in j.values() for c in p_.get("children", [])))
        pm = j.get("planted-minor-lerena", {})
        check("generator  a child with a KNOWN birth year (2015) is NOT held out: a living person, noindex, scrubbed",
              pm.get("living") is True and pm.get("noindex") is True and "2015" not in json.dumps(pm))
        check("generator  a planted FamilySearch-cited young person (born 2001, no death) IS living: a public source cannot "
              "make a dated person under 81 not living (the kit's rule would; cites_for_living withholds the citation)",
              j.get("planted-public-lerena", {}).get("living") is True and j.get("planted-public-lerena", {}).get("noindex") is True
              and "2001" not in json.dumps(j.get("planted-public-lerena", {})))
        code, out = run(STD, t, t / "dist")
        results.append((code == 1 and "HELD-OUT" in out, "standard gate, on that same scratch tree: the committed undated-child row fails it",
                        "caught" if code == 1 and "HELD-OUT" in out else out[:200]))
        gen_in_scratch(t, {"LIVING_TODAY_YEAR": "2027"})
        j2 = {p["slug"]: p for p in json.loads((t / "site/src/data/people.json").read_text(encoding="utf-8"))}
        check("generator  80-year bound: born 80 years ago is living in 2026 and not in 2027",
              j.get("planted-edge-lerena", {}).get("living") is True and j2.get("planted-edge-lerena", {}).get("living") is False,
              f"{j.get('planted-edge-lerena', {}).get('living')} / {j2.get('planted-edge-lerena', {}).get('living')}")
    finally:
        shutil.rmtree(t, ignore_errors=True)

    # a living person's date is withheld from a commit message before /changes/ prints it
    wnames = ["Planted Living LERENA", "Lynn Derrick LUWINSKI"]
    w = L.withhold_dates('He is LYNN DERRICK LUWINSKI, born 24 April 1949 - and "Derrick Luwinski (b.1947)". Planted Living LERENA 1799 stays hers.', wnames)
    check("changes  a date against a roster name in a commit message is replaced by a marker (full date, '(b.1947)', a bare year)",
          "1949" not in w and "1947" not in w and "1799" not in w and w.count("[date withheld]") == 3, w)
    check("changes  ... and a date against somebody who is not on the roster is left alone",
          L.withhold_dates("Pablo Armando LERENA, born 22 February 1882", wnames) == "Pablo Armando LERENA, born 22 February 1882")

    # a roster row cannot make a dead person living: the generator itself refuses
    t = scratch(dist)
    try:
        with open(t / "data" / "living-roster.tsv", "a", encoding="utf-8") as f:
            f.write("Gayle LERENA (born PRESTON)\tgayle-lerena\tPlanted\tPlanted\tplanted\n")
        r = gen_in_scratch(t)
        check("roster  the generator refuses a roster row for a person the data records dead",
              r.returncode != 0 and "living-roster" in (r.stderr + r.stdout), (r.stderr + r.stdout)[-160:])
    finally:
        shutil.rmtree(t, ignore_errors=True)

    # burial-only deaths lost: the generator itself would publish them as living, and the gate net says so
    t = scratch(dist)
    try:
        (t / "data" / "johannesburg-cemetery-1999.tsv").write_text(
            "# emptied for the control\nperson\twhat the register gives\tark\twhat it settles\n", encoding="utf-8")
        r = gen_in_scratch(t)
        j = {p["slug"]: p for p in json.loads((t / "site/src/data/people.json").read_text(encoding="utf-8"))}
        check("net  with the burial rows lost the generator WOULD mark them living (so the net is needed)",
              j.get("gayle-lerena", {}).get("living") is True and j.get("jeffrey-lerena", {}).get("living") is True)
        code, out = run(STD, t, t / "dist")
        results.append((code == 1 and out.count("speaks of a death, burial") >= 2,
                        "net  ... and the standard gate refuses that build, naming both", "caught" if code == 1 else out[:200]))
    finally:
        shutil.rmtree(t, ignore_errors=True)

    if a.full:
        full_builds(dist)

    bad = [r for r in results if not r[0]]
    for ok, label, note in results:
        print(f"  {'ok  ' if ok else 'FAIL'}  {label}  [{note}]")
    caught = sum(1 for r in results if r[0])
    print(f"\n  {caught} of {len(results)} controls behaved as required" + ("" if not bad else f"; {len(bad)} did NOT"))
    return 1 if bad else 0


def full_builds(dist):
    """Two REAL builds in scratch copies: a planted living person, then a planted leak in the template."""
    src = ROOT
    n_live = sum(1 for p_ in L.population(ROOT)[0] if p_.living) + 1          # the roster's own people, and the planted one
    for label, leak in (("planted living person through the whole build", False),
                        ("planted leak in the person template", True)):
        t = pathlib.Path(tempfile.mkdtemp(prefix="living-full-"))
        try:
            subprocess.run(["rsync", "-a", "--exclude", "dist*", "--exclude", ".git", "--exclude", "node_modules", str(src) + "/", str(t) + "/"], check=True)
            subprocess.run(["cp", "-Rc", str(src / "site" / "node_modules"), str(t / "site" / "node_modules")], check=True)
            with open(t / "data" / "lerena-register.tsv", "a", encoding="utf-8") as f:
                f.write("\t".join(["Planted Living LERENA", "-", "-", "-", "-",
                                   "Plantedville, Uruguay", "A private family tree, planted", "UNPLACED", "", ""]) + "\n")
            with open(t / "data" / "living-roster.tsv", "a", encoding="utf-8") as f:
                f.write("Planted Living LERENA\tplanted-living-lerena\tPlantedville\tUruguay\tplanted\n")
            with open(t / "data" / "relations.tsv", "a", encoding="utf-8") as f:
                f.write("\t".join(["Planted Living LERENA", "father", "Nuno Fernando LERENA", "", "register", "planted"]) + "\n")
            with open(t / "data" / "_tree-offsite.txt", "a", encoding="utf-8") as f:
                f.write("")
            subprocess.run([sys.executable, str(t / "tools" / "build-people.py")], check=True, capture_output=True)
            subprocess.run([sys.executable, str(t / "tools" / "build-pages.py")], check=True, capture_output=True)
            if leak:
                tpl = t / "site" / "src" / "pages" / "people" / "[slug].astro"
                s = tpl.read_text(encoding="utf-8")
                s = s.replace("<h2>Town and country</h2>", "<h2>Town and country</h2><p>Born 1799</p>", 1)
                tpl.write_text(s, encoding="utf-8")
            env = {k: v for k, v in os.environ.items() if k != "ARCHIVE_OUT"}   # the repo's own checks read site/dist
            r = subprocess.run(["npm", "run", "build"], cwd=t / "site", capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL)
            out = r.stdout + r.stderr
            if not leak:
                m = re.search(r"ok\s+living-std\s+(.*)", out)
                ok = r.returncode == 0 and bool(m) and f"{n_live} living" in out
                results.append((ok, f"FULL BUILD  {label}: build exits 0 and both gates see {n_live} living",
                                (m.group(1)[:90] if m and r.returncode == 0 else f"exit {r.returncode}: " + out[-300:])))
            else:
                ok = r.returncode != 0 and "shows a year (1799)" in out
                results.append((ok, f"FULL BUILD  {label}: the build FAILS at the standard gate",
                                "caught" if ok else out[-300:]))
        finally:
            shutil.rmtree(t, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
