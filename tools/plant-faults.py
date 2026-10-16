#!/usr/bin/env python3
"""PLANT A FAULT IN EVERY CHECK AND SEE WHETHER IT REFUSES.  (16 October 2026)

    python3 tools/plant-faults.py              # makes a scratch copy of the repo and works there
    python3 tools/plant-faults.py check-nulls  # only the cases whose check name contains this

WHY. A check that has never been seen to fail is a belief, not a check. On 13 October 2026
check-links.py was found to have examined 0 of 136,414 links since the domain move and said "ok";
a sweep on the 16th planted one fault in each of the other checks and found twelve that printed
"0 examined" and passed, one that could not see a four-word name, and a kit gate that guards an
empty set. Every case is: CONTROL (must pass) -> PLANT -> RUN (must FAIL, and name the plant)
-> RESTORE -> CONTROL AGAIN. It works on a COPY (the repo is never touched, and node_modules is
linked, not copied); it needs a built site/dist, so run tools/verify.sh first.

KINDS. plant = a real fault of the kind the check exists for; zero = the check's input is emptied or
missing, and it must refuse rather than report "0 examined"; unguarded = a generator or advisory
tool that has no failing mode, listed so the gap stays visible and is never mistaken for a pass.
EXPECTED MISSES, and why: last-alive and drift never fail by design; check:living and check:covers
(kit) pass on an empty input, which is the kit's to fix - the first is covered by the sibling
check-living-places 'living-x' gate."""
import json, os, pathlib, re, shutil, subprocess, sys, tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
_ARGS = [a for a in sys.argv[1:]]
if _ARGS and pathlib.Path(_ARGS[0]).is_dir():
    SC = pathlib.Path(_ARGS.pop(0)); _TMP = None
else:
    _TMP = pathlib.Path(tempfile.mkdtemp(prefix="plant-faults-"))
    SC = _TMP / "repo"
    shutil.copytree(REPO, SC, ignore=shutil.ignore_patterns(".git", "node_modules", ".astro"))
    os.symlink(REPO / "site" / "node_modules", SC / "site" / "node_modules")
sys.argv = [sys.argv[0], str(SC)] + _ARGS
K = "node_modules/@daviddef/archive-kit/kit/tools"
SITE, ROOT = SC / "site", SC


def sh(cmd, cwd):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=900)
    return p.returncode, (p.stdout + p.stderr)


class Plant:
    """Mutate files; restore on exit."""
    def __init__(self):
        self.undo = []
    def edit(self, path, fn):
        p = pathlib.Path(path)
        old = p.read_text(encoding="utf-8")
        new = fn(old)
        assert new != old, f"plant changed nothing in {path}"
        self.undo.append((p, old)); p.write_text(new, encoding="utf-8")
    def create(self, path, text):
        p = pathlib.Path(path); assert not p.exists(); self.undo.append((p, None)); p.write_text(text, encoding="utf-8")
    def delete(self, path):
        p = pathlib.Path(path)
        if p.is_dir():
            tmp = pathlib.Path(str(p) + ".sweepbak"); shutil.move(p, tmp); self.undo.append((p, ("dir", tmp)))
        else:
            self.undo.append((p, p.read_text(encoding="utf-8"))); p.unlink()
    def snapshot(self, path):
        p = pathlib.Path(path); tmp = pathlib.Path(str(p) + ".snapbak")
        if tmp.exists(): shutil.rmtree(tmp)
        shutil.copytree(p, tmp); self.undo.append((p, ("snap", tmp)))
    def restore(self):
        for p, old in reversed(self.undo):
            if old is None:
                p.unlink(missing_ok=True)
            elif isinstance(old, tuple):
                if p.exists(): shutil.rmtree(p)
                shutil.move(old[1], p)
            else:
                p.write_text(old, encoding="utf-8")
        self.undo = []


def line_edit(match, fn):
    """edit the first line (of the non-comment lines) for which match(line) is true"""
    def go(t):
        L = t.split("\n")
        for i, l in enumerate(L):
            if not l.startswith("#") and match(l):
                L[i] = fn(l); return "\n".join(L)
        raise SystemExit("no line matched for a plant")
    return go


def append(text):
    return lambda t: (t if t.endswith("\n") else t + "\n") + text


CASES = []
def case(check, plant_desc, cmd, cwd, plant, expect=None, kind="plant"):
    CASES.append(dict(check=check, desc=plant_desc, cmd=cmd, cwd=cwd, plant=plant, expect=expect, kind=kind))


D = SC / "data"
DIST = SITE / "dist"
REG = D / "lerena-register.tsv"
PY = lambda t: f"python3 tools/{t}.py"
KIT = lambda t, a="": f"python3 {K}/{t}.py {a}"

# ---------------------------------------------------------------- repo checks (root)
case("consistency", "an unpaired *** marker in a register note", PY("consistency"), SC,
     lambda P: P.edit(REG, line_edit(lambda l: l.startswith("Mary Septima TAYLOR"), lambda l: l + " *** unpaired")), "marker|CONTRADICT|unpaired|odd")
case("check-links", "a broken internal link on the home page", PY("check-links"), SC,
     lambda P: P.edit(DIST / "index.html", lambda t: t.replace("</body>", '<a href="/zz-no-such-page/">x</a></body>', 1)), "zz-no-such|broken")
case("check-links", "the configured base is wrong, so it examines nothing", PY("check-links"), SC,
     lambda P: P.edit(SITE / "astro.config.mjs", lambda t: re.sub(r"base:\s*['\"]/['\"]", "base: '/TheLerena'", t, 1)), "examined|0 ", "zero")
case("check-errands", "a ready errand whose detail says THIS ERRAND IS CLOSED", PY("check-errands"), SC,
     lambda P: P.edit(D / "errands.tsv", line_edit(lambda l: "\tready\t" in l, lambda l: l + " THIS ERRAND IS CLOSED")), "finished|CLOSED")
case("check-errands", "errands.tsv has no rows at all", PY("check-errands"), SC,
     lambda P: P.edit(D / "errands.tsv", lambda t: "\n".join(l for l in t.split("\n") if l.startswith("#") or l.startswith("key\t"))), None, "zero")
case("check-evidence", "evidence about a person who is not in the register", PY("check-evidence"), SC,
     lambda P: P.edit(D / "person-evidence.tsv", append("Zzyzx Nobody\tx\tx\tx\tx\n")), "Zzyzx")
case("check-evidence", "person-evidence.tsv is gone", PY("check-evidence"), SC,
     lambda P: P.delete(D / "person-evidence.tsv"), None, "zero")
case("check-corrections", "a retracted reading asserted bare in a data file", PY("check-corrections"), SC,
     lambda P: (P.edit(D / "corrections.tsv", append("2026-10-16\tminor\tx\tx\tx\tZzyzx Retracted Reading\n")),
                P.create(D / "zz-plant.tsv", "k\tv\nrow\tThe archive says Zzyzx Retracted Reading was here\n")), "Zzyzx")
case("check-corrections", "every `retired` cell emptied, so nothing is enforced", PY("check-corrections"), SC,
     lambda P: P.edit(D / "corrections.tsv", lambda t: "\n".join(l if l.startswith("#") or l.startswith("date\t") or not l.strip()
                      else "\t".join(l.split("\t")[:5] + [""]) for l in t.split("\n"))), None, "zero")
case("check-onsite", "a data file that is neither on the site nor declared a notebook", PY("check-onsite"), SC,
     lambda P: P.create(D / "zz-orphan.tsv", "a\tb\n1\t2\n"), "zz-orphan")
case("check-duplicates", "the same person entered twice in the register", PY("check-duplicates"), SC,
     lambda P: P.edit(REG, lambda t: t.rstrip("\n") + "\n" + [l for l in t.split("\n") if l.startswith("Careen Maria LERENA")][0].replace("Careen Maria LERENA", "Careen Maria LERENA ", 1) + "\n"), "Careen|duplicate|same")
case("check-nulls", "a blanket null naming someone the register holds", PY("check-nulls"), SC,
     lambda P: P.create(D / "zz-null.tsv", "claim\tsays\nnull\tTRUE NULL: no record of Roque Luis Armando LERENA exists in any country\n"), "Roque")
case("check-addresses", "a stranded address whose redirect stub is gone", PY("check-addresses"), SC,
     lambda P: P.delete(DIST / "people" / "emilia-lerena-vega"), "emilia")
case("check-addresses", "the slug ledger is empty", PY("check-addresses"), SC,
     lambda P: P.edit(SITE / "src/data/person-slugs.json", lambda t: "{}"), None, "zero")
case("check-living-places", "a living person's place beside her name on a page", PY("check-living-places"), SC,
     lambda P: P.edit(DIST / "index.html", lambda t: t.replace("</body>", '<ul><li><td>Cheryl Anne LERENA</td><td>Johannesburg</td></li></ul></body>', 1)), "Johannesburg|Cheryl|living")
case("check-living-places", "living.json missing (the kit's check has no input)", PY("check-living-places"), SC,
     lambda P: P.delete(SITE / "src/data/living.json"), "living.json")
case("check-tree", "an edge naming somebody the register does not hold", PY("check-tree"), SC,
     lambda P: P.edit(D / "relations.tsv", append('Nuno Fernando LERENA\tchild\tZzyzx Nobody\t-\tregister\tplant\n')), "Zzyzx")
case("check-tree", "relations.tsv has no edges", PY("check-tree"), SC,
     lambda P: P.edit(D / "relations.tsv", lambda t: "\n".join(l for l in t.split("\n") if l.startswith("#") or l.startswith("person\t"))), None, "zero")
case("check-spines", "a spine date that disagrees with the register", PY("check-spines"), SC,
     lambda P: P.edit(REG, line_edit(lambda l: l.startswith("Nuno Fernando LERENA\t"), lambda l: l.replace("\t1924-10-06\t", "\t1924-10-07\t", 1))), "1924|Nuno|disagree")
case("check-sources", "a row says an image was read and does not say which", PY("check-sources"), SC,
     lambda P: P.edit(REG, append("Zzyzx Nobody\t-\t-\t-\t-\t-\tIMAGE READ somewhere\tCONNECTED\tnote\t-\n")), "Zzyzx|WHICH")
case("check-sources", "sources-consulted.tsv is empty", PY("check-sources"), SC,
     lambda P: P.edit(D / "sources-consulted.tsv", lambda t: "# nothing\nfilm\tnote\n"), None, "zero")
case("check-people-named", "a person named on a record who is not in the register", PY("check-people-named"), SC,
     lambda P: P.edit(D / "gro-taylor-brayley-births.tsv", append("99\tZzyzx Nobody\t1870\tref\tF\tplant\n")), "Zzyzx")
case("check-superseded", "a retracted claim asserted on a built page", PY("check-superseded"), SC,
     lambda P: P.edit(DIST / "taylor/index.html", lambda t: t.replace("</body>", "<p>The family had two sets of twins in this house.</p></body>", 1)), "twins|two sets")
case("check-arity", "a register row with the wrong number of columns", PY("check-arity"), SC,
     lambda P: P.edit(REG, append("Zzyzx Nobody\t1900\tx\n")), "Zzyzx|match|column")
case("check-arity", "a data file with no trailing newline", PY("check-arity"), SC,
     lambda P: P.edit(D / "errands.tsv", lambda t: t.rstrip("\n")), "newline")
case("last-alive", "a dated phrase that makes someone ALIVE AT a false day (a generator, not a gate)", PY("last-alive"), SC,
     lambda P: P.edit(REG, line_edit(lambda l: l.startswith("Ricardo Juan Carlos LERENA"), lambda l: l + " a letter of 21 August 1997 names him")), "ALIVE", "unguarded")
case("drift", "a page that has fallen behind its data (advisory by design)", PY("drift"), SC,
     lambda P: P.edit(REG, line_edit(lambda l: l.startswith("Careen Maria LERENA"), lambda l: l + " *** A NEW FINDING NO PAGE MAKES, planted. ***")), None, "unguarded")

# ---------------------------------------------------------------- kit checks (site/)
case("check:pin", "the pin file names a different kit commit", KIT("checkpin", "--root ."), SITE,
     lambda P: P.edit(SITE / ".kitpin", lambda t: "0" * 40 + "\n"), "pin|differ|0000")
case("check:living", "a living person's birth date printed on a page", KIT("checkliving", "--dist dist --data src/data --policy named-bare"), SITE,
     lambda P: P.edit(DIST / "index.html", lambda t: t.replace("</body>", "<p>Cheryl Anne LERENA, born 14 Oct 1955</p></body>", 1)), "Cheryl|1955|living")
case("check:living", "living.json is emptied (the gate guards nobody)", KIT("checkliving", "--dist dist --data src/data --policy named-bare"), SITE,
     lambda P: P.edit(SITE / "src/data/living.json", lambda t: "[]"), None, "zero")
case("check:kin", "a person who would be 200 years old", KIT("checkkin", "--data src/data/people.json --born born --died died --max 0"), SITE,
     lambda P: P.edit(SITE / "src/data/people.json", lambda t: t.replace('"born": "1882-02-22"', '"born": "1700-02-22"', 1)), "110|aged|impossible")
case("check:kin", "people.json is an empty list", KIT("checkkin", "--data src/data/people.json --born born --died died --max 0"), SITE,
     lambda P: P.edit(SITE / "src/data/people.json", lambda t: "[]"), None, "zero")
case("check:templates", "an unclosed tag in a page", KIT("checktemplates", "--root ."), SITE,
     lambda P: P.edit(SITE / "src/pages/atlas.astro", lambda t: t + '\n<div class="zz-unclosed">\n'), "zz-unclosed|atlas|close")
case("check:kit", "a link to an anchor that is not there", KIT("checkarchive", "--dist dist"), SITE,
     lambda P: P.edit(DIST / "index.html", lambda t: t.replace("</body>", '<a href="#zz-nope-anchor">x</a></body>', 1)), "zz-nope|anchor")
case("check:kit", "dist holds no pages", KIT("checkarchive", "--dist dist"), SITE,
     lambda P: P.delete(DIST / "people"), None, "zero")
case("check:worklist", "a row with a state that is not allowed", KIT("checkworklist", "--root ."), SITE,
     lambda P: P.edit(SITE / "src/data/worklist.json", lambda t: t.replace('"state": "next"', '"state": "zzz"', 1)), "zzz|state")
case("check:worklist", "the work list has no rows", KIT("checkworklist", "--root ."), SITE,
     lambda P: P.edit(SITE / "src/data/worklist.json", lambda t: json.dumps({**json.loads(t), "rows": []})), None, "zero")
case("check:covers", "a row that covers something which does not exist", KIT("checkcovers", "--root ."), SITE,
     lambda P: P.edit(SITE / "src/data/worklist.json", lambda t: (lambda w: (w["rows"][-1].__setitem__("covers", w["rows"][-1].get("covers", []) + ["err:zz-no-such-errand"]), json.dumps(w, indent=1))[1])(json.loads(t))), "zz-no-such")
case("check:covers", "the accounts block is emptied, so nothing counts as outstanding", KIT("checkcovers", "--root ."), SITE,
     lambda P: P.edit(SITE / "src/data/worklist.json", lambda t: json.dumps({**json.loads(t), "accounts": []})), None, "zero")
case("check:rows", "a data file shrinks below its declared floor", KIT("checkrows", "--root ."), SITE,
     lambda P: P.edit(SC / ".rowfloor", lambda t: t.replace('"rows": 22', '"rows": 999')), "rows|floor|lost")
case("check:inline", "too many evidence lists left inside templates", KIT("checkinline", "--root . --max-inline 7"), SITE,
     lambda P: [P.create(SITE / f"src/pages/zzcopy{i}.astro", (SITE / "src/pages/passport.astro").read_text(encoding="utf-8")) for i in range(1, 4)], "inline|zzcopy|exceed")
case("check:nav", "the navigation drifts from the estate's convention", KIT("checknav", "--dist dist --strict"), SITE,
     lambda P: P.edit(DIST / "index.html", lambda t: t.replace("Investigations", "Zzzgations")), "Zzz|Investig|conform")


# ---------------------------------------------------------------- round 2: corrected plants
DROP = {("check-errands", "plant"), ("check-duplicates", "plant"), ("check-nulls", "plant"), ("check-addresses", "plant"),
        ("check-spines", "plant"), ("check:pin", "plant"), ("check:kin", "plant"), ("check:kit", "plant"),
        ("check:rows", "plant"), ("check:nav", "plant")}
CASES[:] = [c for c in CASES if (c["check"], c["kind"]) not in DROP]

def spine_person():
    L = [l.split("\t") for l in (D / "descent-spines.tsv").read_text(encoding="utf-8").split("\n") if l and not l.startswith("#")]
    h = L[0]; ri = h.index("register"); bi = h.index("born")
    for r in L[1:]:
        if len(r) > ri and r[ri].strip() and r[ri].strip() != "-" and re.search(r"\b1[5-9]\d\d\b", r[bi] if len(r) > bi else ""):
            return r[ri].strip(), re.search(r"\b(1[5-9]\d\d)\b", r[bi]).group(1)
    raise SystemExit("no spine person")

def errand_detail(l):
    f = l.split("\t"); f[4] = f[4] + " THIS ERRAND IS CLOSED"; return "\t".join(f)
case("check-errands", "a ready errand whose DETAIL says THIS ERRAND IS CLOSED", PY("check-errands"), SC,
     lambda P: P.edit(D / "errands.tsv", line_edit(lambda l: l.split("\t")[3:4] == ["ready"], errand_detail)), "finished|CLOSED")
case("check-duplicates", "the same person entered twice (through build-people, as the gate does)",
     "python3 tools/build-people.py > /dev/null && python3 tools/check-duplicates.py", SC,
     lambda P: (P.snapshot(SITE / "src/data"), P.edit(REG, lambda t: t.rstrip("\n") + "\n" + [l for l in t.split("\n") if l.startswith("Careen Maria LERENA")][0] + "\n")), "Careen|duplicate|same")
case("check-nulls", "a blanket null naming a three-word register name", PY("check-nulls"), SC,
     lambda P: P.create(D / "zz-null.tsv", "claim\tsays\nnull\tTRUE NULL: no record of Nuno Fernando LERENA exists in any country\n"), "Nuno")
case("check-nulls", "a blanket null naming a FOUR-word register name", PY("check-nulls"), SC,
     lambda P: P.create(D / "zz-null.tsv", "claim\tsays\nnull\tTRUE NULL: no record of Roque Luis Armando LERENA exists in any country\n"), "Roque")
case("check-addresses", "a stranded address: its redirect is gone from the config and its stub from the build", PY("check-addresses"), SC,
     lambda P: (P.edit(SITE / "astro.config.mjs", lambda t: t.replace("'/people/emilia-lerena-vega'", "'/people/zz-moved'")), P.delete(DIST / "people" / "emilia-lerena-vega")), "emilia")
case("check-spines", "a register birth year moved for a person a spine row names", PY("check-spines"), SC,
     lambda P: (lambda who_y: P.edit(REG, line_edit(lambda l: l.startswith(who_y[0] + "\t"), lambda l: l.replace(who_y[1], str(int(who_y[1]) + 3), 1))))(spine_person()), "disagree|birth|year")
case("check:pin", "package.json pins a different kit commit than the one installed", KIT("checkpin", "--root ."), SITE,
     lambda P: P.edit(SITE / "package.json", lambda t: re.sub(r"(archive-kit\"?: \"github:daviddef/TheArchiveKit#)[0-9a-f]{40}", r"\g<1>" + "0" * 40, t)), "pin|differ|0000|install")
case("check:kin", "a person who dies before they were born", KIT("checkkin", "--data src/data/people.json --born born --died died --max 0"), SITE,
     lambda P: P.edit(SITE / "src/data/people.json", lambda t: t.replace('"died": "1950-Mar-19"', '"died": "1850-Mar-19"', 1)), "impossible|before|died")
case("check:kit", "a link to a different page's anchor that is not there", KIT("checkarchive", "--dist dist"), SITE,
     lambda P: P.edit(DIST / "index.html", lambda t: t.replace("</body>", '<a href="/method/#zz-nope-anchor">x</a></body>', 1)), "zz-nope|anchor")
case("check:kit", "a link to a page that is not there", KIT("checkarchive", "--dist dist"), SITE,
     lambda P: P.edit(DIST / "index.html", lambda t: t.replace("</body>", '<a href="/zz-no-page/">x</a></body>', 1)), "zz-no-page|broken|resolve")
case("check:rows", "a spine mark (grade) falls below its recorded floor", KIT("checkrows", "--root ."), SITE,
     lambda P: P.edit(SC / ".rowfloor", lambda t: t.replace('"grade": 22', '"grade": 999')), "grade|fell|lost")
case("check:nav", "an Evidence-menu route is removed from the built home page", KIT("checknav", "--dist dist --strict"), SITE,
     lambda P: P.edit(DIST / "index.html", lambda t: t.replace('href="/sources/"', 'href="/zz-sources/"')), "sources|Evidence|depart|missing")
case("check-living-places", "living.json emptied (the sibling gate must notice)", PY("check-living-places"), SC,
     lambda P: P.edit(SITE / "src/data/living.json", lambda t: "[]"), "living|disagree", "zero")


# ---------------------------------------------------------------- round 3: zero-input cases for the rest
NAMED6 = ["gro-taylor-brayley-births.tsv", "gro-brailey-temple-births.tsv", "taylor-baptisms-northam.tsv",
          "roque-infants-civil-deaths.tsv", "johannesburg-cemetery-1999.tsv", "trinidad-flores-sweep-2026-09-27.tsv"]
case("check-duplicates", "people.json is missing (the build did not run)", PY("check-duplicates"), SC,
     lambda P: P.delete(SITE / "src/data/people.json"), None, "zero")
case("check-spines", "descent-spines.tsv is gone", PY("check-spines"), SC,
     lambda P: P.delete(D / "descent-spines.tsv"), None, "zero")
case("check-people-named", "all six record files it reads are gone", PY("check-people-named"), SC,
     lambda P: [P.delete(D / f) for f in NAMED6], None, "zero")
case("check-superseded", "dist holds no pages at all", PY("check-superseded"), SC,
     lambda P: P.delete(DIST), None, "zero")
case("check-links", "dist is empty", PY("check-links"), SC,
     lambda P: P.delete(DIST), None, "zero")
case("check-living-places", "dist is empty", PY("check-living-places"), SC,
     lambda P: P.delete(DIST), None, "zero")
case("check-onsite", "the register of data files is empty", PY("check-onsite"), SC,
     lambda P: P.edit(D / "_not-on-site.txt", lambda t: "\n".join(l for l in t.split("\n") if l.startswith("#"))), None, "zero")
case("check-sources", "the register is empty", PY("check-sources"), SC,
     lambda P: P.edit(REG, lambda t: "\n".join(l for l in t.split("\n")[:2])), None, "zero")
case("check-arity", "the register is empty", PY("check-arity"), SC,
     lambda P: P.edit(REG, lambda t: "\n".join(l for l in t.split("\n")[:1]) + "\n"), None, "zero")

def main():
    only = sys.argv[2] if len(sys.argv) > 2 else None
    results = []
    for c in CASES:
        if only and only not in c["check"]:
            continue
        rc0, out0 = sh(c["cmd"], c["cwd"])
        P = Plant()
        try:
            c["plant"](P)
            rc1, out1 = sh(c["cmd"], c["cwd"])
        finally:
            P.restore()
        rc2, _ = sh(c["cmd"], c["cwd"])
        named = bool(c["expect"] and re.search(c["expect"], out1, re.I))
        if rc0 != 0:
            verdict = "CONTROL-FAILED"
        elif rc2 != 0:
            verdict = "RESTORE-FAILED"
        elif rc1 != 0:
            verdict = "CAUGHT" if (named or not c["expect"]) else "CAUGHT-BUT-FOR-ANOTHER-REASON"
        else:
            verdict = "MISSED"
        tail = " | ".join(l.strip() for l in out1.strip().splitlines()[-2:])[:200]
        results.append((c["check"], c["kind"], verdict, c["desc"], rc1, tail))
        print(f"{verdict:30} {c['check']:20} [{c['kind']:9}] {c['desc'][:70]}\n{'':32}rc={rc1} :: {tail}", flush=True)
    caught = sum(1 for r in results if r[2].startswith("CAUGHT"))
    missed = [r for r in results if r[2] == "MISSED"]
    print(f"\n{caught} caught, {len(missed)} missed, of {len(results)} planted")
    for r in missed:
        print(f"  MISSED  {r[0]:20} [{r[1]}] {r[3]}")
    if _TMP: shutil.rmtree(_TMP, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
