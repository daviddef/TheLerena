#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The given-name vocabulary for the linking standard (kit/tools/checkstandard.py, names.given_names_file).

    python3 ../tools/build-given-names.py            # from site/: writes site/given.json (gitignored, rebuilt every run)
    python3 ../tools/build-given-names.py --counts   # counts only

checkstandard reads a name-like phrase only if it holds a word the archive uses as a GIVEN name. The names index gives it the given
names of the people it lists; this adds every other given name the register holds, so that a person read from a record whose given
name the register uses is seen.

WHERE IT COMES FROM. site/src/data/people.json only, which is committed, so CI builds the same file as the machine that holds the
rest of the data. A person the register marks `living`, `noindex` or an alias row (and anyone whose name has no clean given name)
contributes NOTHING: a living person's given name is not written into a file because they bear it. A word is a given name if it is
not the last word of the cleaned name, is not written in capitals (the register's mark of a surname), is not a particle (de, del, y...), is not an honorific and holds no digit or bracket. Counts
only are printed.
"""
import io, json, pathlib, re, sys, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = SITE / "given.json"
PARTICLES = {"de", "del", "la", "las", "los", "y", "da", "do", "dos", "van", "von", "di", "du", "le", "el", "e"}
HONORIFICS = {"don", "dona", "dr", "dr.", "sr", "sr.", "sra", "sra.", "capitan", "general", "exmo", "fray", "padre", "mr", "mr.",
              "mrs", "mrs.", "miss", "sir", "rev", "rev."}
WORD = re.compile(r"^[^\W\d_]+(?:['\-][^\W\d_]+)*$")


def build():
    rows = json.load(io.open(SITE / "src" / "data" / "people.json", encoding="utf-8"))
    got, skipped = set(), 0
    for r in rows:
        if r.get("living") or r.get("noindex") or r.get("aliasOf"):
            skipped += 1
            continue
        s = re.sub(r"\(.*?\)", " ", str(r.get("name") or ""))
        words = [w for w in s.replace('"', " ").split() if w]
        while len(words) > 1 and words[0].casefold() in HONORIFICS:
            words.pop(0)
        if len(words) < 2:
            skipped += 1
            continue
        for w in words[:-1]:
            if w.casefold() in PARTICLES or not WORD.match(w) or len(w) < 2:
                continue
            if len(w) >= 3 and w == w.upper():           # the register writes a surname in capitals: never a given name
                continue
            got.add(w[:1].upper() + w[1:].lower() if w == w.upper() else w)
    return sorted(got, key=lambda s: unicodedata.normalize("NFKD", s).casefold()), skipped


def main(argv):
    words, skipped = build()
    print("build-given-names: %d given-name words from the register (%d rows contribute nothing: living, held out, an alias or one word)"
          % (len(words), skipped))
    if "--counts" in argv:
        return 0
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(words, ensure_ascii=False, indent=0) + "\n")
    print("build-given-names: wrote %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
