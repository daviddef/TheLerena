#!/usr/bin/env python3
"""A person this archive says has NO RECORD must not also be in its register.

WHY THIS EXISTS. On 12 October 2026 this archive made the same serious mistake twice in one
day, and no gate could see either.

  (1) It published, on 10 October, that LEANDRO LORENA and his wife LLANOS appear in
      "one record in the index, in any country" - the army card of their son - and offered
      it as the model of a properly controlled null. The search was sound. But FOUR of that
      household were already in data/lerena-register.tsv, entered from the 1895 Buenos
      Aires census, under the spelling LERENA rather than LORENA.

  (2) It published a search mechanism as a new finding when data/compound-surname-sweep.tsv
      had carried it since 14 September.

*** NEITHER WAS A RETRACTION, SO check-superseded.py WAS BLIND. *** That gate reads
corrections.tsv and asks whether the site has stopped saying what it took back. Nothing had
been taken back here. Two live claims simply contradicted each other in two files, and every
gate stayed green. drift.py asks whether a page has fallen behind its data; check-onsite asks
whether a row reaches a reader. *** NOTHING ASKED WHETHER THE ARCHIVE AGREED WITH ITSELF. ***

WHAT IT DOES, AND THE FIRST VERSION OF THIS GATE GOT IT WRONG. It reads every data row that
asserts a null - "true null", "only record", "no record in any country" and their kin - pulls
the personal names out of that row and folds the surname through the archive's published
spelling variants. *** THE FIRST ATTEMPT THEN FAILED ON ANY NAME THE REGISTER HELD, AND
REPORTED 91. *** That rule is nonsense: half this register is people known from a SINGLE
document, and a row saying "the card is the only record of this household" is not in conflict
with the household having a row. Being in the register is not the same as having records.

*** SO IT COMPARES SOURCES, NOT PRESENCE. *** For each person named in a null claim it takes
the SOURCE FIELD of their register row and asks whether any significant word of it appears in
the claim. If the register cites the very record the null concedes, they agree and it passes.
*** IF THE REGISTER CITES SOMETHING ELSE ENTIRELY, THE ARCHIVE IS HOLDING TWO ANSWERS. ***
That is exactly the Leandro case: the claim conceded an army card in Cajon 985, and his
register row cited the 1895 Buenos Aires census.

THE FOLD IS THE WHOLE POINT. The card says LORENA and the census says LERENA. A gate that
compares strings cannot catch this archive's characteristic error, because this archive's
characteristic error IS the spelling. The variants come from data/name-variants.tsv, which is
what /name/ publishes, so the gate and the page cannot drift apart.

WHAT IT DOES NOT DO. It is not a word ban. A null claim may legitimately sit beside a
retraction ("this was wrong", "corrected on", "withdrawn"), and corrections.tsv and
false-zeros.tsv exist to carry exactly these sentences - so those files are exempt and a
match within RETRACT_WINDOW characters of a word of retraction is allowed.

It is a GATE. It exits 1.
"""
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Files whose job is to hold a claim that was wrong.
DATA_EXEMPT = {"corrections.tsv", "false-zeros.tsv", "gedcom-import.tsv",
               "gedcom-graded.tsv", "gedcom-current.tsv", "family-memory.tsv"}

# *** ONLY BLANKET NULLS. *** The first run also caught SCOPED ones - "no marriage of Fidel
# Lerena TO Maria Rueda", "no Lerena in this volume" - and those are not in conflict with a
# register row at all: a man can be absent from one marriage index and present in an 1812
# padron. The dangerous claim is the one that says a person has NO RECORDS AT ALL.
NULL_CLAIM = re.compile(
    r"true null|only record|in any country|anywhere in the index|on earth|"
    r"exists in (?:exactly )?one record|no record of (?:him|her|them|this \w+) anywhere",
    re.I)

RETRACT_WINDOW = 420
RETRACT = re.compile(
    r"used to (?:say|read|carry)|(?:was|were|is|are) wrong|no longer|struck|retir|disprov|"
    r"refus|withdraw|withdrew|corrected|correction|broke[nr]?|that was wrong|not a null|"
    r"turned out", re.I)

# A capitalised word, or an ALL-CAPS word of two or more letters.
WORD = r"(?:[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+|[A-ZÁÉÍÓÚÑ]{2,})"
NAME = re.compile(r"\b(%s(?:\s+(?:y|de|del|la)\s+%s|\s+%s){1,2})\b" % (WORD, WORD, WORD))

STOP = {"don", "dona", "dn", "da", "sr", "sra", "the", "of", "and", "y", "de", "del",
        "la", "el", "los", "las"}


def variants():
    """The spellings /name/ publishes, so the gate cannot drift from the page."""
    f = ROOT / "data" / "name-variants.tsv"
    out = set()
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") or not line.strip():
                continue
            form = line.split("\t")[0].strip()
            for part in re.split(r"[/,]", form):
                part = norm(part).strip()
                # HERENCIA is a word, not a name; LERENA is the canonical target.
                if part and part not in ("lerena", "herencia") and " " not in part:
                    out.add(part)
    return out or {"llerena", "serena", "gerena", "lorena", "larena", "lerina"}


def norm(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z ]+", " ", s)


def key(name, var):
    """ALL forenames plus the canonical surname.

    *** KEYING ON THE FIRST FORENAME ALONE IS WHAT check-duplicates.py DOES, and it is wrong
    here. *** That gate asks a human to compare two rows, so a loose key costs a glance. This
    one ASSERTS a contradiction, so a loose key publishes a false one - and on the first run it
    did exactly that, matching "Juan Carlos Lerena" to Juan JOSE Lerena and "Angelica Maria" to
    Angelica TERESA. The whole forename sequence has to agree.
    """
    bare = norm(re.sub(r"\(.*?\)", " ", str(name)))
    words = [w for w in bare.split() if w not in STOP]
    if len(words) < 2:
        return None
    fore, sur = [], None
    for w in words:
        c = "lerena" if w in var else w
        if c == "lerena":
            sur = c
            break
        fore.append(c)
    if sur is None:
        if len(words) < 2:
            return None
        fore, sur = words[:-1], words[-1]
    return (tuple(fore), sur) if fore and sur else None


SRC_STOP = {"the", "and", "with", "from", "that", "this", "read", "image", "ark", "index",
            "record", "records", "registration", "found", "none", "only", "also", "which",
            "where", "been", "have", "has", "was", "were", "its", "for", "not", "but"}


def tokens(s):
    """Words of four letters or more, plus years and ark stems - what names a SOURCE."""
    n = norm(s)
    out = {w for w in n.split() if len(w) >= 4 and w not in SRC_STOP}
    out |= set(re.findall(r"\b1[6-9]\d\d\b|\b20\d\d\b", str(s)))
    out |= {m.lower() for m in re.findall(r"[0-9A-Z]{4}-[0-9A-Z]{3,4}", str(s))}
    return out


def declared(var):
    """Pairs this archive has already said are different people.

    *** REUSES data/_person-pairs.txt RATHER THAN INVENTING A SECOND LIST. *** The disease this
    gate exists for is two rows that never meet; answering it with a private exemption file of
    its own would be the same mistake in miniature.
    """
    f = ROOT / "data" / "_person-pairs.txt"
    out = set()
    if not f.exists():
        return out
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0]
        if "||" not in line:
            continue
        a, b = [x.strip() for x in line.split("||", 1)]
        ka, kb = key(a, var), key(b, var)
        if ka and kb:
            out.add((ka, kb))
            out.add((kb, ka))
    return out


def register(var):
    """key -> (display name, source field)."""
    f = ROOT / "data" / "lerena-register.tsv"
    out = {}
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        cols = line.split("\t")
        name = cols[0].strip()
        if not name or name == "name":
            continue
        k = key(name, var)
        if k:
            out.setdefault(k, (name, cols[6] if len(cols) > 6 else ""))
    return out


def main():
    var = variants()
    reg = register(var)
    ok_pairs = declared(var)
    bad = []
    scanned = claims = 0

    for f in sorted((ROOT / "data").glob("*.tsv")):
        if f.name in DATA_EXEMPT:
            continue
        scanned += 1
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("#") or not line.strip():
                continue
            m = NULL_CLAIM.search(line)
            if not m:
                continue
            claims += 1
            lo = max(0, m.start() - RETRACT_WINDOW)
            if RETRACT.search(line[lo:m.end() + RETRACT_WINDOW]):
                continue
            ctx = tokens(line)
            seen = set()
            for cand in NAME.findall(line):
                k = key(cand, var)
                if not k or k in seen:
                    continue
                seen.add(k)
                if k not in reg:
                    continue
                who, src = reg[k]
                if (k, key(who, var)) in ok_pairs or (key(who, var), k) in ok_pairs:
                    continue
                st = tokens(src)
                if not st:
                    continue              # no source to disagree with
                if st & ctx:
                    continue              # the register cites what the claim concedes
                bad.append((f.name, n, cand.strip(), who, src))

    if bad:
        print("  FAIL  nulls      %d null claim(s) name someone who IS in the register:"
              % len(bad))
        for fn, n, cand, who, src in bad[:20]:
            print("          - %s:%d says %r has no record" % (fn, n, cand))
            print("              but %r is in the register from a source the claim never"
                  " mentions:" % who)
            print("                %s" % src[:150])
        print("          Either the null is wrong - correct it and say so in"
              " data/corrections.tsv -")
        print("          or the register row is a different person, in which case declare the"
              " pair in data/_person-pairs.txt")
        print("          with the reason, the same way the duplicates gate is answered.")
        return 1

    print("  ok    nulls      %d null claim(s) across %d data file(s); every person named"
          " in one is" % (claims, scanned))
    print("                   absent from the register, or held there from the very record"
          " the claim concedes")
    print("                   (%d spellings folded, from data/name-variants.tsv)" % len(var))
    return 0


if __name__ == "__main__":
    sys.exit(main())
