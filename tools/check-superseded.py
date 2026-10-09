#!/usr/bin/env python3
"""A claim this archive has retracted must stop being asserted on its own pages.

WHY THIS EXISTS. On 9 October 2026 David asked, for the second time, whether the research
was reaching the sites and the charts. It was. What it was NOT doing was displacing the
claims it had replaced.

/taylor/ carried, in one scroll: a new section proving from the GRO index that IRENE WAS
ALONE IN 1879, and an older section stating that "the family had TWO SETS of twins, this
pair and Irene's in 1879". Both were published. The page contradicted itself, and /trees/
still advertised the whole line with "her parents named her after the fact that she was
their seventh daughter" - the exact sentence the registers had refused the day before.

*** NO GATE COULD SEE IT. *** drift.py asks whether a page has fallen behind its DATA.
check-rows asks whether rows reach a reader. /corrections/ records what was wrong. Nothing
asked whether the REST OF THE SITE had stopped saying it, so a correction could be
published and contradicted on the same page and every gate stayed green.

HOW IT WORKS, AND WHY IT IS NOT A WORD BAN. A retired claim may legitimately appear in
three shapes: on /corrections/ and /changes/, which exist to record it; inside a sentence
that retracts it ("this used to say", "that was wrong", "no longer"); and nowhere else.
So a match is a failure only when it is NOT within RETRACT_WINDOW characters of a word of
retraction. That keeps the archive able to quote its own mistakes, which is most of what
it does.

It is a GATE. It exits 1.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"

# Pages whose job is to carry retired claims.
EXEMPT = {"corrections", "changes", "method", "search", "searchindex.json"}
# Files whose job is to hold what was believed: corrections.tsv IS the retraction, and the
# gedcom and family-memory files exist to carry a tree's or a family's claims so they can be
# graded against records.
DATA_EXEMPT = {"corrections.tsv", "gedcom-import.tsv", "gedcom-graded.tsv",
               "gedcom-current.tsv", "family-memory.tsv"}

RETRACT_WINDOW = 420
RETRACT = re.compile(
    r"used to (say|read|carry)|(was|were|is|are) wrong|no longer|struck|retir|disprov|refus|"
    r"correct|superseded|does not exist|never existed|is not what|cannot be true|"
    r"this archive had|for three weeks|and that was wrong|does not come out|"
    r"and it does not|had carried|has carried|downgrad|"
    # *** ADDED ON THE GATE'S FIRST RUN. *** Six of its ten hits were this archive
    # retracting a claim in its own words - "CORRECTS the family's account", "the
    # register CONTRADICTED it" - and the regex was too narrow to hear them. A gate
    # that cannot recognise a retraction will send people to edit their corrections.
    r"contradict|moves the grave|but the register|not newlands|rather than newlands|"
    # This archive kills an argument in words no dictionary of retraction would list:
    # "the whole argument is dead", "how it died", "read it as history". Bare "died" is
    # deliberately NOT here - in a genealogy half the sentences contain it.
    r"is dead|was killed|how it died|as history|what it said|kept because|"
    # A person-merge retires a NAME, and the note that records it quotes the old one.
    # "merged with", "merged into", "carried separately" are how this archive says so.
    r"merged|carried separately|two rows|one man",
    re.I)

# *** EACH ENTRY IS A CLAIM THIS ARCHIVE PUBLISHED AND THEN RETRACTED. *** The `why` is
# written for the person who trips the gate, so they can tell at once whether they have
# revived an old error or simply used an unlucky phrase.
RETIRED = [
    (r"two sets of twins|two sets</strong>, this pair",
     "The unnamed twin of Irene, 1879, does not exist. The GRO index shows Irene alone - no "
     "second birth to this mother that year, of either sex. There is ONE set of twins."),
    (r"(?:household|family) of ten children|the ten children(?! above is now)",
     "William Taylor and Mary Ann Hellen Brayley had NINE children, not ten. The tree's ten "
     "drove three weeks of searching for a child who does not exist."),
    (r"she was (?:their|the) seventh daughter|is the seventh daughter",
     "Mary Septima is the SIXTH daughter and the eighth child. The name does not describe "
     "her place in the family."),
    (r"a piece of arithmetic, and it turns out to be exactly right",
     "The arithmetic does not come out. Septima means seventh; she is the sixth daughter."),
    (r"unmarked grave at Newlands|buried at Newlands",
     "The grave is at MAITLAND, not Newlands - grave 7719, Cemetery No. 1, read 8 October 2026."),
    (r"Mauricio[^.]{0,90}(died|d\.)[^.]{0,40}1925|1925[^.]{0,60}Mauricio",
     "3 March 1925 is his DAUGHTER CLARA's death date. Mauricio was born about 1815, so the "
     "archive was asserting he died at about 110. He has no attested death date at all."),
    (r"knew the name from a completely different direction",
     "'Her sister EDIE' was never independent evidence of a sister named Edith. Edie IS Isabella "
     "Temple Dalling - the argument was counting one woman twice."),
    (r"Edith[^.]{0,130}strong candidate|strong candidate[^.]{0,130}Edith",
     "Edith is downgraded to weak and then disproved: she is not in the Northam baptism register, "
     "and the GRO index gives her a different mother. There is no tenth child."),
    (r"neither has been checked against a burial register",
     "The register WAS checked on 8 October 2026. All three are at Maitland - 7719 A, B and C - "
     "and the last column of his own entry reads 'In Plot of R. P. Lerina'."),
    (r"STILL NOT NAMED BY ANY RECORD",
     "Alejandro M. Lerena's parents ARE named: AVELINO LERENA and AMBROSIA TRAIBEL, on the Cordon "
     "act of 26 December 1877, film 007713388 image 02455, read 27 September 2026."),
    (r"Alejandro LERENA \(m\. Elisa VILLARDEMOROS\)",
     "Merged 9 October 2026 into Alejandro M. LERENA (m.1 Elisa VILLADEMOROS; m.2 Julia BASSANI). "
     "They were proved one man on 27 September; two rows is the old state."),
    (r"William John[^.]{0,60}1 November 1870|1870-11-01",
     "No source gives his day of birth. The archive invented 1 November and manufactured a "
     "three-day gap between twins; consistency.py caught it. The sources say 'Nov 1870'."),
]


# *** THE DATA FILES ARE SCANNED TOO, AND THAT WAS NOT THE FIRST DESIGN. ***
# This gate first read only rendered pages. On 9 October 2026 a hand review of the serious
# corrections found THREE live retractions it could not possibly have seen, because they sat
# in TSV comment lines that no page renders: brayley-bmd.tsv still ended "Mary Septima is the
# seventh daughter and her name means what it says" four lines after striking the argument
# for it, and two more files closed with verdicts their own strikes had killed.
# *** A STRIKE INSERTED MID-PARAGRAPH LEAVES THE PARAGRAPH'S CONCLUSION STANDING ***, and the
# conclusion is the part the next person reads.
#
# WIDENING IS SAFE ONLY BECAUSE THE CLAIM LIST IS HAND-WRITTEN. The same day, generating
# claims automatically from every what_was_said in corrections.tsv returned 39 hits of which
# every one checked was a collision on a NAME rather than on a claim. Curated regexes carry
# no such noise, so pointing them at more text costs nothing.
DATA = ROOT / "data"


def sources():
    for p in sorted(DIST.rglob("index.html")):
        yield "page", p.relative_to(DIST).as_posix().replace("/index.html", "") or "HOME", p
    for p in sorted(DATA.glob("*.tsv")):
        yield "data", p.name, p


def main():
    bad = []
    for kind, name, path in sources():
        if kind == "page" and name.split("/")[0] in EXEMPT:
            continue
        if kind == "data" and name in DATA_EXEMPT:
            continue
        raw = path.read_text(errors="ignore")
        text = re.sub(r"<[^>]+>", " ", raw) if kind == "page" else raw
        text = re.sub(r"\s+", " ", text)
        for rx, why in RETIRED:
            for m in re.finditer(rx, text, re.I):
                a = max(0, m.start() - RETRACT_WINDOW)
                window = text[a:m.end() + RETRACT_WINDOW]
                if RETRACT.search(window):
                    continue
                where = f"/{name}/" if kind == "page" else f"data/{name}"
                bad.append((where, m.group(0)[:60], why))

    if bad:
        print(f"  FAIL  superseded {len(bad)} retired claim(s) still asserted:")
        for name, frag, why in bad:
            print(f"          {name}  —  “{frag}”")
            print(f"              {why}")
        print("\n          Either correct the sentence, or write the retraction beside it so a")
        print("          reader can see the claim is being quoted rather than made.")
        return 1

    print(f"  ok    superseded {len(RETIRED)} retired claim(s); none asserted outside a retraction")
    return 0


if __name__ == "__main__":
    sys.exit(main())
