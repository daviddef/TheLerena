#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The records table for the linking standard (kit/components/Rec.astro, L3 and L4): every record a passage may link to.

    python3 ../tools/build-records.py            # from site/: writes site/src/data/records.json
    python3 ../tools/build-records.py --check    # fails if the committed table is not what the committed data gives
    python3 ../tools/build-records.py --counts   # prints counts only, writes nothing

There is no one records table in this archive, so this builds it from data the archive already holds and commits:
  * data/ark-to-film.tsv     every image ark resolved to a DGS film and an image number: one `ark` row each, keyed "film/image";
  * data/film-register.tsv, the `search/film/<n>` addresses in data/*.tsv and the pages, and every DGS or film number the data cites:
    one `film` row each (https://www.familysearch.org/search/film/<9 digits>, the address /sources/ already uses for 33 rows);
  * the FamilySearch arks that data/sources-consulted.tsv, data/person-evidence.tsv and site/src/data/people.json hold: one `ark` row
    each (the record's own page, link only);
  * data/record-plates.json   the family papers the archive publishes (show true, because /family-papers/ already shows them) and the
    records it holds and will not show (`hold`: the 1971 and 1973 death notices, which name living children);
  * the archive's own pages that transcribe a record (/passport/, /estate/, /naairs/, /national-archives/, /enrolment-card/).
Nothing is invented: a row exists only where the committed data holds the number, the ark or the file. A FamilySearch plate is never
held (it is read in the viewer and cited by ark), so no row has `plate` unless data/record-plates.json says the family published it.
THE LIVING GATE. A row is never made for a record whose label holds a living or held-out person's name (the living list, when this
machine has it: tools/run-autolink.py writes it), and no row names a person at all except a family paper's label (all dead). A row
flagged `hold` is never drawn by Rec and is never written.
Counts only are printed.
"""
import argparse, io, json, os, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = ROOT / "site"
OUT = SITE / "src" / "data" / "records.json"
DATA = ROOT / "data"
PEOPLE = SITE / "src" / "data" / "people.json"
PLATES = DATA / "record-plates.json"
FS = "https://www.familysearch.org"
ARK = re.compile(r"\b([0-9]:[0-9]:[A-Z0-9]{4,}(?:-[A-Z0-9]+)*)\b")   # the same shape arkify() in site/src/lib/text.js links
FILM_URL = re.compile(r"familysearch\.org/search/film/0*(\d{6,9})")
FILM_REF = re.compile(r"\b(?:film|DGS|microfilm)\s*(?:no\.?\s*)?0*(\d{6,9})\b", re.I)
OWN = [("own-passport", "/passport/", "The 1940 Argentine passport (this archive's transcription)"),
       ("own-estate", "/estate/", "The estate file MOOC 6/9/17017 (this archive's transcription)"),
       ("own-naairs", "/naairs/", "The South African archives search (NAAIRS), as this archive read it"),
       ("own-national-archives", "/national-archives/", "The British National Archives search, as this archive read it"),
       ("own-enrolment", "/enrolment-card/", "The Argentine army enrolment card (this archive's transcription)")]


def tsv(path):
    out = []
    p = pathlib.Path(path)
    if not p.exists():
        return out
    lines = [l.rstrip("\n") for l in p.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    if not lines:
        return out
    h = lines[0].split("\t")
    for l in lines[1:]:
        c = l.split("\t") + [""] * len(h)
        out.append(dict(zip(h, c)))
    return out


def living_terms():
    """The living list tools/run-autolink.py writes outside the checkout, when this machine has it (names only)."""
    p = pathlib.Path(os.environ.get("AUTOLINK_LIVING") or pathlib.Path.home() / ".local" / "state" / "lerena" / "autolink-living.json")
    if not p.exists():
        return set(), False
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set(), False
    return {n.casefold() for n in d.get("names", []) if len(n.split()) >= 2}, True


def build():
    rows, stats = [], {}
    # --- arks resolved to a film and an image
    a2f = {}
    for r in tsv(DATA / "ark-to-film.tsv"):
        fi = (r.get("film_and_image") or "")
        m = re.fullmatch(r"dgs:0*(\d+)\.0*(\d+)_0*(\d+)", fi)
        if m and r.get("state", "").startswith("resolved") and m.group(1) == m.group(2):
            a2f[r["ark"]] = (int(m.group(1)), int(m.group(3)))
    films = {}                         # int -> label
    reg = tsv(DATA / "film-register.tsv")
    for r in reg:
        try:
            n = int(r["film"])
        except (KeyError, ValueError):
            continue
        what = (r.get("what it is") or "").strip()
        films[n] = what if what and not what.startswith("not yet identified") else ""
    for ark, (f, i) in a2f.items():
        films.setdefault(f, "")
    old_rolls = set()                  # data/dgs-audit.tsv lists the old microfilm roll numbers that look like DGS numbers: never a film row
    for r in tsv(DATA / "dgs-audit.tsv"):
        if "OLD MICROFILM" in " ".join(r.values()).upper():
            old_rolls |= {n for n in (int(x) for x in re.findall(r"\b0*(\d{6,9})\b", " ".join(r.values()))) if n < 3000000}
    texts = ""
    for p in sorted(DATA.glob("*.tsv")):
        texts += p.read_text(encoding="utf-8") + "\n"
    for p in sorted((SITE / "src" / "pages").rglob("*.astro")):
        texts += p.read_text(encoding="utf-8") + "\n"
    for m in FILM_URL.finditer(texts):
        films.setdefault(int(m.group(1)), "")
    # a number is a DGS film (not an old microfilm roll number, which the archive writes beside it: "DGS 7713373 (film 2124160...)")
    # when the data writes it as DGS, or in the nine-digit form with its leading zeros, or the table already holds it
    for m in FILM_REF.finditer(texts):
        n = int(m.group(1))
        if n in old_rolls or (n < 3000000 and n not in films):
            continue                      # an old microfilm roll number (the DGS numbers here run from 4,000,000)
        if re.search(r"\bDGS\s*(?:no\.?\s*)?0*%d\b" % n, texts, re.I) or ("%09d" % n) in texts:
            films.setdefault(n, "")
    for n in [n for n in films if n in old_rolls]:
        del films[n]
    for n, what in sorted(films.items()):
        lab = "FamilySearch film %09d" % n + (": " + re.sub(r"\s+", " ", re.sub(r"\*\*\*", "", what)).strip()[:90] if what else "")
        rows.append({"id": "film-%d" % n, "url": "%s/search/film/%09d" % (FS, n), "label": lab, "kind": "film", "key": [str(n)]})
    stats["film rows"] = len(films)
    # an image of a film the archive links itself: .../search/film/<film>?i=<image> (the address as the archive wrote it)
    fimg = {}
    for m in re.finditer(r"familysearch\.org/search/film/0*(\d{6,9})\?i=(\d+)", texts):
        fimg[(int(m.group(1)), int(m.group(2)))] = m.group(0)
    for (f, i), u in sorted(fimg.items()):
        rows.append({"id": "fimg-%d-%d" % (f, i), "url": "https://www." + u, "label": "FamilySearch film %09d image %d" % (f, i), "kind": "ark",
                     "key": ["%d/%d" % (f, i)]})
    stats["film image rows (an address with ?i= as the archive wrote it)"] = len(fimg)
    # --- arks: the image arks that resolve, then every other ark the data holds a FamilySearch address for. A row's label is the
    #     source line the archive wrote for it, where there is one (data/sources-consulted.tsv, then data/person-evidence.tsv)
    def clean_label(t):
        return re.sub(r"\s+", " ", re.sub(r"\*\*\*", "", t)).strip()
    said = {}
    for a, lab in (json.loads((DATA / "record-labels.json").read_text(encoding="utf-8")).get("arks") or {}).items() if (DATA / "record-labels.json").exists() else []:
        said[a] = lab
    for r in tsv(DATA / "sources-consulted.tsv"):
        for a in ARK.findall(r.get("link", "")):
            said.setdefault(a, clean_label(r.get("source", "")))
    for r in tsv(DATA / "person-evidence.tsv"):
        for a in ARK.findall(r.get("ark", "")):
            said.setdefault(a, clean_label(r.get("source", "")))
    # an act file (data/<act>.tsv) names its ark in its header: that file's title line is the label
    for f in sorted(DATA.glob("*.tsv")):
        head = f.read_text(encoding="utf-8").splitlines()[:30]
        title = next((clean_label(l.lstrip("# ")) for l in head if l.startswith("#") and len(clean_label(l.lstrip("# "))) > 12), "")
        for a in ARK.findall("\n".join(head)):
            if title:
                said.setdefault(a, title.rstrip(" .-"))
    held_arks = set(said)
    # every ark the archive's data and pages print: the address the archive itself links (arkify) is the address in the table
    for m in ARK.finditer(texts):
        held_arks.add(m.group(1))
    try:
        for p in json.loads(PEOPLE.read_text(encoding="utf-8")):
            if p.get("ark"):
                held_arks |= set(ARK.findall(p["ark"]))
            for e in p.get("evidence") or []:
                for a in ARK.findall(e.get("ark", "")):
                    held_arks.add(a)
                    said.setdefault(a, clean_label(e.get("source", "")))
    except (OSError, ValueError):
        pass
    seen = set()
    for ark, (f, i) in sorted(a2f.items()):
        lab = "FamilySearch image, film %09d image %05d" % (f, i)
        if said.get(ark):
            lab = said[ark][:110].rstrip(" ,;-") + " [film %09d, image %05d]" % (f, i)
        rows.append({"id": "ark-" + ark.replace(":", "-"), "url": "%s/ark:/61903/%s" % (FS, ark), "label": lab, "kind": "ark",
                     "key": ["%d/%d" % (f, i)]})
        seen.add(ark)
    n_other = 0
    for ark in sorted(held_arks - seen):
        kind = "index entry" if ark.startswith("1:") else "image"
        lab = said[ark][:130].rstrip(" ,;-") if said.get(ark) else "FamilySearch %s %s" % (kind, ark)
        rows.append({"id": "ark-" + ark.replace(":", "-"), "url": "%s/ark:/61903/%s" % (FS, ark), "label": lab, "kind": "ark", "key": [ark]})
        n_other += 1
    stats["ark rows resolved to a film and image"] = len(a2f)
    stats["other ark rows (link only)"] = n_other
    # --- the family papers the archive publishes, and what it holds and will not show
    pl = json.loads(PLATES.read_text(encoding="utf-8"))
    n_show = 0
    for q in pl["plates"]:
        if not (SITE / "public" / "docs" / q["file"]).exists():
            raise SystemExit("build-records: a plate is not in site/public/docs (%s)" % q["file"])
        if q.get("show") is True and len(str(q.get("basis", "")).strip()) >= 20:
            rows.append({"id": q["id"], "url": "/docs/" + q["file"], "label": q["label"], "kind": "plate", "plate": q["file"],
                         "w": q["w"], "h": q["h"], "show": True})
            n_show += 1
    held = {h["record"] for h in pl.get("hold", [])}
    for h in pl.get("hold", []):
        if len(str(h.get("reason", "")).strip()) < 20:
            raise SystemExit("build-records: a hold entry needs a reason (%s)" % h.get("record"))
    stats["plate rows (published family papers)"] = n_show
    stats["held, no row made"] = len(held)
    for oid, url, label in OWN:
        rows.append({"id": oid, "url": url, "label": label, "kind": "own"})
    stats["own pages"] = len(OWN)
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("build-records: an id is used twice")
    keys = [(r["kind"], k) for r in rows for k in r.get("key", [])]
    if len(keys) != len(set(keys)):
        raise SystemExit("build-records: two rows share a key")
    # living gate: no row's label holds a living or held-out person's name
    lv, have = living_terms()
    bad = [r["id"] for r in rows if any(t in r["label"].casefold() for t in lv)]
    if bad:
        raise SystemExit("build-records: %d row(s) name a living or held-out person: refused" % len(bad))
    stats["living list read"] = 1 if have else 0
    return {"records": rows}, stats


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--counts", action="store_true")
    a = ap.parse_args(argv)
    table, stats = build()
    for k, v in stats.items():
        print("  %-48s %d" % (k, v))
    print("  %-48s %d" % ("rows", len(table["records"])))
    text = json.dumps(table, ensure_ascii=False, indent=1) + "\n"
    if a.counts:
        return 0
    if a.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("build-records: FAIL, %s is not what the committed data gives; run tools/build-records.py and commit it" % OUT.relative_to(ROOT))
            return 1
        print("build-records: ok (equal to the committed data)")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print("build-records: wrote %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
