#!/usr/bin/env python3
"""Plant a fault for every living-people rule and show the gate catches it.

A GATE THAT CAN ONLY PASS PROVES NOTHING. Every rule in tools/check-living-standard.py and
tools/check-living-places.py has a control here: the unmodified build is checked first and must
pass (the positive control); then a COPY has one fault planted and the gate must fail on exactly
that rule. The real files are never touched.

Planted values are ones no living person can have (the year 1799, a name that is nobody's); a
living person's real dates are never written here as literals: they are read from the data at run
time, so this file can sit in a public repository.

Also proved here, against the generator and the shared rule:
  - the 80-year bound moves the line (80 is living, 81 is not);
  - a recorded death, and a public-source citation, each make a young person not living;
  - the two people recorded dead only by a burial registration cannot be marked living, and the net
    catches it if the burial rows are ever lost;
  - a possible minor is held out of people.json, and the standard gate fails if the row is committed;
  - a planted living person in the register is scrubbed to name, relationships, town, country.

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
    for rel in ("data", "tools", "site/src/data"):
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
    ap.add_argument("--dist", default=str(ROOT / "site" / "dist-wt"))
    ap.add_argument("--full", action="store_true")
    a = ap.parse_args()
    dist = pathlib.Path(a.dist)
    if not (dist / "people").exists():
        raise SystemExit(f"no build at {dist}: build first (ARCHIVE_OUT=dist-wt npm run build)")

    people, lr, year = L.population(ROOT)
    live = [p for p in people if p.living]
    if not live:
        raise SystemExit("the rule finds nobody living: these controls need one living person in the data")
    C = live[0]                                   # the living person the controls are aimed at
    cslug = C.slug
    cdates = sorted(C.private_dates, key=len)
    cdate = max(C.private_dates, key=len)         # a full date string, read from the data and never typed here

    # ---------------- positive controls: the real build passes both gates -------------------------
    case("POSITIVE  real build passes the standard gate", STD, None, lambda t: None, dist, expect_pass=True)
    case("POSITIVE  real build passes the places gate", PLC, None, lambda t: None, dist, expect_pass=True)

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
        edit(page(t, "about"), lambda s: s.replace("</main>", f"<p>{cdate}</p></main>", 1))
    case("c  a living person's full date on another page", STD, "contains the full date", date_elsewhere, dist)

    def date_json(t):
        (t / "dist" / "leak.json").write_text(json.dumps({"x": cdate}), encoding="utf-8")
    case("c  ... or in any served file", STD, "leak.json contains the full date", date_json, dist)

    def date_committed(t):
        with open(t / "data" / "relations.tsv", "a", encoding="utf-8") as f:
            f.write(f"# a planted note {cdate}\n")
    case("c  ... or in a committed file that is not a known input", STD, "committed file data/relations.tsv", date_committed, dist)

    def whocanon(t):
        edit(page(t, f"who/{cslug}"), lambda s: re.sub(r'<meta name="robots"[^>]*noindex[^>]*>', "", s))
    case("d  name page of only-living bearers, not noindex", STD, "names only living people and is not noindex", whocanon, dist)

    def whocanon2(t):
        edit(page(t, f"who/{cslug}"), lambda s: s.replace("</head>", '<link rel="canonical" href="https://x.invalid/elsewhere/"></head>', 1))
    case("d  name page naming a canonical elsewhere", STD, "names a canonical elsewhere", whocanon2, dist)

    def minor(t):
        row = "\t".join(["Planted Minor LERENA", "2015", "Montevideo", "Uruguayan", "-", "Montevideo", "planted", "UNPLACED", "", ""])
        with open(t / "data" / "lerena-register.tsv", "a", encoding="utf-8") as f:
            f.write(row + "\n")
    case("e  a possible minor (born 2015) committed in the register", STD, "HELD-OUT person", minor, dist)

    def minor_page(t):
        edit(page(t, "about"), lambda s: s.replace("</main>", "<p>Planted Minor LERENA</p></main>", 1))
    def minor_both(t):
        minor(t); minor_page(t)
    case("e  ... and on a built page", STD, "appears in about/index.html", minor_both, dist)

    def undated_child(t):
        with open(t / "data" / "lerena-register.tsv", "a", encoding="utf-8") as f:
            f.write("\t".join(["Planted Child LERENA", "-", "-", "-", "-", "Montevideo", "planted", "UNPLACED", "", ""]) + "\n")
        with open(t / "data" / "relations.tsv", "a", encoding="utf-8") as f:
            f.write("\t".join([C.name, "child", "Planted Child LERENA", "", "register", "planted"]) + "\n")
    case("e  an undated person with a living parent (held out)", STD, "HELD-OUT person", undated_child, dist)

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

    # 80-year bound: the gate and the generator both reckon at LIVING_TODAY_YEAR
    ytxt = max(int(x) for x in re.findall(r"\d{4}", " ".join(C.private_dates)) or [0]) if C.private_dates else 0
    case("a  80-year bound: a year later the rule says she is not living", STD, "by the rule", lambda t: None, dist,
         env={"LIVING_TODAY_YEAR": str(ytxt + 81)})

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
    check("rule  a FamilySearch citation means not living; a private tree entry does not",
          not lr.is_living(2005, False, ["FamilySearch Family Tree"], 2026)
          and lr.is_living(2005, False, ["MyHeritage family tree"], 2026))
    check("rule  no birth year is not living", not lr.is_living(None, False, [], 2026))
    check("rule  under 18 and undated-with-a-living-parent are held out; the dead are not",
          lr.possible_minor(2015, False, [], False, 2026) and lr.possible_minor(None, False, [], True, 2026)
          and not lr.possible_minor(2015, True, [], False, 2026))

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
            ["Planted Public LERENA", "2001", "Plantedville, Uruguay", "Uruguayan", "-", "Plantedville, Uruguay",
             "FamilySearch, planted record", "UNPLACED", "", ""],
        ]
        with open(reg, "a", encoding="utf-8") as f:
            for r in rows:
                f.write("\t".join(r) + "\n")
        with open(t / "data" / "relations.tsv", "a", encoding="utf-8") as f:
            f.write("\t".join(["Planted Living LERENA", "father", "Nuno Fernando LERENA", "", "register", "planted 1799"]) + "\n")
            f.write("\t".join(["Planted Minor LERENA", "father", "Nuno Fernando LERENA", "", "register", "planted"]) + "\n")
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
        check("generator  a planted possible minor is held out of people.json",
              "planted-minor-lerena" not in j and "Planted Minor" not in json.dumps(j))
        nuno = j.get("nuno-fernando-lerena", {})
        check("generator  ... and is nobody's relative",
              all("Planted Minor" not in c["name"] for c in nuno.get("children", [])))
        check("generator  a planted FamilySearch-cited young person is NOT living",
              j.get("planted-public-lerena", {}).get("living") is False)
        code, out = run(STD, t, t / "dist")
        results.append((code == 1 and "HELD-OUT" in out, "standard gate, on that same scratch tree: the committed minor row fails it",
                        "caught" if code == 1 and "HELD-OUT" in out else out[:200]))
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
    for label, leak in (("planted living person through the whole build", False),
                        ("planted leak in the person template", True)):
        t = pathlib.Path(tempfile.mkdtemp(prefix="living-full-"))
        try:
            subprocess.run(["rsync", "-a", "--exclude", "dist*", "--exclude", ".git", "--exclude", "node_modules", str(src) + "/", str(t) + "/"], check=True)
            subprocess.run(["cp", "-Rc", str(src / "site" / "node_modules"), str(t / "site" / "node_modules")], check=True)
            with open(t / "data" / "lerena-register.tsv", "a", encoding="utf-8") as f:
                f.write("\t".join(["Planted Living LERENA", "2001", "Plantedville, Uruguay", "Uruguayan", "-",
                                   "Plantedville, Uruguay", "A private family tree, planted", "UNPLACED", "", ""]) + "\n")
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
            env = dict(os.environ, ARCHIVE_OUT="dist-wt")
            r = subprocess.run(["npm", "run", "build"], cwd=t / "site", capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL)
            out = r.stdout + r.stderr
            if not leak:
                m = re.search(r"ok\s+living-std\s+(.*)", out)
                ok = r.returncode == 0 and bool(m) and "2 living" in out
                results.append((ok, f"FULL BUILD  {label}: build exits 0 and both gates see 2 living",
                                (m.group(1)[:90] if m else out[-200:])))
            else:
                ok = r.returncode != 0 and "shows a year (1799)" in out
                results.append((ok, f"FULL BUILD  {label}: the build FAILS at the standard gate",
                                "caught" if ok else out[-300:]))
        finally:
            shutil.rmtree(t, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
