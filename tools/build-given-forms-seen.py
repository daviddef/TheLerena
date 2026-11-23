#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""How many times THIS archive has met each given-name form: the --seen file for the forenames page (/forenames/).  (23 November 2026)

    python3 ../tools/build-given-forms-seen.py            # from site/: writes site/src/data/given-forms-seen.json
    python3 ../tools/build-given-forms-seen.py --check    # fail if the committed file is not what people.json gives (nothing written)

WHAT IT IS, AND WHAT IT IS NOT. A COUNT PER FORM, and nothing else: {"observed": {"Joaquin": 3, ...}}. No person, no slug, no date. The forms
themselves are NOT kept here: they are kept ONCE, in Record Atlas (data/given-name-families.json, written only through
scripts/given_name_variants.py), and the Archive Kit's tools/atlas_given_names.py fetches them into site/src/data/given-names.json with this file
as `--seen`, so the page can say a form was met in THESE records and not merely in some family's. This file says how often a form was met; the
Atlas says which name it is a form of. Never add a table of forms, a language or a spelling here.

THE REGISTER FOLDS ACCENTS (people.json writes Joaquin, Concepcion); the Atlas's fold (kit atlas_given_names.fold) matches without accents and
case, so the count joins to the Atlas's Joaquín without a table.

WHO COUNTS. The rows of site/src/data/people.json that are not living, not held out (`noindex`) and not an alias row: the rows build-given-names.py
(the linking standard's vocabulary) reads, so the two cannot disagree about who may contribute. A living person's given name is not counted because
they bear it. A person counts once for each form they bear, so «Maria Luisa» is one Maria and one Luisa.

WHAT IS A GIVEN NAME. The words of the name before the first word written in capitals (the register's mark of a surname: «Juan Facundo Frutuoso
BARROS Lerena» -> Juan, Facundo, Frutuoso). Not particles (de, del, las, y...), not honorifics or titles (Don, Dona, Dr., General, Fr...), and not the
register's own annotations («(wife of ...)», «= probably ...», a quotation, «in Gilberto's 1895 household»). A row that marks no surname in capitals
gives all its words but the last, unless an annotation followed its name, when they are all given names («Juana (a godmother written Llerena...)»).
What survives that and is still not a name stays in the output, is reported by the Archive Kit's `--strict` and is dealt with at its source (the
record, or the Atlas with its evidence). It is never hidden here.
"""
import io
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
PEOPLE = SITE / "src" / "data" / "people.json"
OUT = SITE / "src" / "data" / "given-forms-seen.json"

PARTICLES = {"de", "del", "la", "las", "los", "y", "da", "do", "dos", "van", "von", "di", "du", "le", "el", "e", "in", "of", "the", "a"}
TITLES = {"don", "dona", "dr", "dr.", "d.", "sr", "sr.", "sra", "sra.", "capitan", "general", "gen.", "exmo", "fray", "fr", "fr.", "padre",
          "mr", "mr.", "mrs", "mrs.", "miss", "sir", "rev", "rev.", "doctor", "mayor", "infant", "canonigo", "vicar", "priest", "presbitero", "obispo", "juez"}
WORD = re.compile(r"^[^\W\d_]+(?:['\-][^\W\d_]+)*$")


def given_words(name):
    raw = str(name or "")
    had_note = bool(re.search(r"[(=\"]|,| in ", raw))
    s = re.sub(r"\([^)]*\)", " ", raw)
    s = re.sub(r'"[^"]*"', " ", s)
    s = s.split("=")[0].split(",")[0]
    s = re.split(r"\s+in\s+", s)[0]
    words = [w for w in s.split() if w]
    while words and words[0].casefold() in TITLES:
        words.pop(0)
    caps = [i for i, w in enumerate(words) if len(w) >= 2 and w == w.upper() and w.isalpha()]
    if caps:
        words = words[:caps[0]]
    elif not had_note and len(words) > 1:
        words = words[:-1]
    out = []
    for w in words:
        if w.casefold() in PARTICLES or w.casefold() in TITLES or not WORD.match(w) or len(w) < 2:
            continue
        out.append(w[:1].upper() + w[1:])
    return out


def counts():
    rows = json.load(io.open(PEOPLE, encoding="utf-8"))
    seen, used = {}, 0
    for r in rows:
        if r.get("living") or r.get("noindex") or r.get("aliasOf"):
            continue
        ws = set(given_words(r.get("name")))
        if ws:
            used += 1
        for w in ws:
            seen[w] = seen.get(w, 0) + 1
    key = lambda s: unicodedata.normalize("NFKD", s).casefold()
    return {k: seen[k] for k in sorted(seen, key=key)}, used


def main(argv):
    seen, used = counts()
    doc = {
        "_note": "Made by tools/build-given-forms-seen.py from site/src/data/people.json; never typed. A COUNT PER FORM (people bearing it), no person, no date. "
                 "The forms are kept in Record Atlas, not here; this is the --seen file for the Archive Kit's tools/atlas_given_names.py.",
        "observed": seen,
    }
    text = json.dumps(doc, ensure_ascii=False, indent=0) + "\n"
    if "--check" in argv:
        have = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if have != text:
            print("  FAIL  given-forms-seen: %s is not what people.json gives (run `python3 ../tools/build-given-forms-seen.py`)" % OUT.relative_to(ROOT))
            return 1
        print("  ok    given-forms-seen: %d forms from %d people, as committed" % (len(seen), used))
        return 0
    OUT.write_text(text, encoding="utf-8")
    print("build-given-forms-seen: %d forms met in the records of %d people -> %s" % (len(seen), used, OUT.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
