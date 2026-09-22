#!/usr/bin/env python3
"""Refuse to ship a build that gives a living person a PLACE.

WHY THIS IS SEPARATE FROM THE KIT'S check:living. The kit enforces `named-bare`:
a living person may be named, and no DATE of theirs may appear. That is the estate
rule and three archives share it. This archive's own rule, written on /direct-line/,
is stricter and says so in its own words:

    "No dates, no places, no photographs."

A COUNTRY IS A PLACE. On 20 September 2026 country pills were added to the tree
pages, and the living row on the spine was left without one BY HAND, because the
author happened to remember. Nothing would have caught it. The kit screens dates.
This screens places, and only for this archive, because imposing it on the Falco and
Defranceski builds is not this file's decision to make.

THREE TRAPS, TWO OF THEM ALREADY SPRUNG ONCE WHILE WRITING THIS:

  1. "LIVING" IS A WORD THAT APPEARS IN RECORDS ABOUT THE DEAD. The 1891 Northam
     census describes GEORGINA BRAYLEY, a widow of 77, as "LIVING ON MEANS". She
     died over a century ago. A grep for /LIVING/ makes her a living person and the
     gate then guards a Victorian almswoman. So the marker must be a STATUS, matched
     as a whole cell - `OMITTED-LIVING`, or a cell opening `LIVING - `.

  2. A BARE PLACE NAME IS EVERYWHERE AND PROVES NOTHING. "Johannesburg" appears all
     over this archive, legitimately, attached to the dead. Screening for the word
     would fire on every page and the gate would be switched off inside a day - which
     is the lesson the kit's own header pays for twice. So a place is only a leak
     when it is a place THE DATA ATTACHES TO THAT PERSON, found beside THEIR name.

  3. A WINDOW THAT LOOKS BACKWARDS READS THE CARD ABOVE. On the spine, generation 2
     ends with a SOUTH AFRICA pill and generation 3 is the living row. Look 200
     characters back from her name and you find his pill and fail an innocent build.
     So the window only ever looks FORWARD, and is cut short at the first boundary -
     the end of the list item, or the next heading - whichever comes first.

  4. AND PROXIMITY ALONE IS NOT ENOUGH EVEN LOOKING FORWARD. The first run of this
     gate failed the build on /direct-line/, where the prose reads that this person
     "married into the Defranceski family, whose line runs back through JOHANNESBURG
     to Gracisce". That Johannesburg belongs to somebody else's line. It is not a
     statement about her and it is not a leak, and failing on it is how a guard gets
     switched off inside a day.

     So a place is only a leak when it sits in a FACT POSITION: a country pill, or
     one of the containers this site prints facts in. WHAT THIS GATE DOES NOT DO,
     said plainly rather than left to be discovered: *** it does not screen PROSE. ***
     A sentence that gave a living person a place in running text would pass here.
     That is a deliberate limit, not an oversight - the alternative fires on innocent
     sentences, and a noisy gate is worse than a narrow one.

A build with no living people in its data passes with nothing to check. That is
correct rather than a gap, and it is printed rather than passed over in silence,
because a gate that guards nobody should have to say so.
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DIST = ROOT / "site" / "dist"

# A living marker is a STATUS, not a word in a sentence. See trap 1.
LIVING_CELL = re.compile(r"^(OMITTED-LIVING|LIVING\s*[-–—:]\s*.*)$", re.I)

# Columns that hold a place. Matched on the header, so a new place column is covered.
PLACE_COL = re.compile(r"place|birthplace|^where", re.I)
NAME_COL = re.compile(r"^(person|name|who)$", re.I)

# Where a card ends, for trap 3.
BOUNDARY = re.compile(r"</li>|<h[1-4][\s>]|class=\"sp-g", re.I)
WINDOW = 900

# Containers this site prints FACTS in, as opposed to prose. See trap 4. A place is
# only a leak when it lands in one of these, or in a country pill.
FACT = re.compile(r'class="[^"]*\b(sp-f|yr|ac-p|ac-m|sp1-gen|fact)\b[^"]*"|<t[dh][\s>]', re.I)
FACT_SPAN = 240

TAGS = re.compile(r"<[^>]+>")
EMPH = re.compile(r"\*\*\*")


def strip(s):
    return html.unescape(TAGS.sub(" ", s))


def clean(s):
    return EMPH.sub("", str(s or "")).strip()


def living_people():
    """{display name: {places}} for everyone the DATA marks as living."""
    found = {}
    for f in sorted(DATA.glob("*.tsv")):
        lines = [l.rstrip("\n") for l in f.read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.startswith("#")]
        if not lines:
            continue
        hdr = lines[0].split("\t")
        ni = next((i for i, h in enumerate(hdr) if NAME_COL.match(h.strip())), None)
        if ni is None:
            continue
        pis = [i for i, h in enumerate(hdr) if PLACE_COL.search(h.strip())]
        for line in lines[1:]:
            cells = line.split("\t")
            if not any(LIVING_CELL.match(clean(c)) for c in cells):
                continue
            name = clean(cells[ni]) if ni < len(cells) else ""
            if not name:
                continue
            places = {clean(cells[i]) for i in pis if i < len(cells)}
            places = {p for p in places if p and p != "-"}
            # One person, spelled two ways. direct-line.tsv writes "Cheryl Anne LERENA"
            # and lerena-siblings-gen3.tsv writes "Cheryl Anne Lerena"; without folding
            # the key this gate reports two living people and withholds a place from
            # only one of them.
            key = name.lower()
            if key in found:
                found[key][1].update(places)
            else:
                found[key] = [name, set(places)]
    return {v[0]: v[1] for v in found.values()}


def reconcile():
    """The kit's gate and this one must agree about WHO IS ALIVE.

    *** ON 23 SEPTEMBER 2026 THEY DID NOT, AND NOBODY COULD HAVE NOTICED. *** This gate
    reads data/*.tsv for an OMITTED-LIVING cell and found Cheryl Anne Lerena. The kit's
    check:living reads site/src/data/*.json for a `living` flag and found NOBODY, so it
    printed «0 flagged in the data ... no living person reaches the build» and passed.
    It was guarding an empty set, and a gate that guards nobody cannot fail.

    Nothing had leaked - her dates appear nowhere in the build, and that was checked
    before anything was changed - but the estate's most important rule was being kept
    BY HAND while a green check said otherwise. tools/build-pages.py now writes
    src/data/living.json from the same TSV markers this file reads, and this refuses
    the build if the two ever disagree again.

    THE DIRECTION MATTERS. A person here and not there is a person the kit is not
    guarding. A person there and not here is a marker this file has stopped
    recognising. Both are failures and both are named.
    """
    import json
    seen = {k.lower() for k in living_people()}
    f = ROOT / "site" / "src" / "data" / "living.json"
    if not f.exists():
        print("  FAIL  living-x   site/src/data/living.json is missing, so the kit's "
              "check:living has no input")
        print("        Run tools/build-pages.py, which writes it from the TSV markers.")
        return 1
    try:
        j = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  FAIL  living-x   living.json could not be read: {e}")
        return 1
    theirs = {str(r.get("name", "")).lower() for r in j if r.get("living") is True}
    only_here = sorted(seen - theirs)
    only_there = sorted(theirs - seen)
    if only_here or only_there:
        print(f"  FAIL  living-x   the two living-person gates disagree")
        for n in only_here:
            print(f"          - {n}: marked living in data/*.tsv, ABSENT from living.json "
                  f"- the kit's gate is not guarding them")
        for n in only_there:
            print(f"          - {n}: in living.json, NOT marked living in any data/*.tsv "
                  f"- this gate has stopped recognising the marker")
        return 1
    print(f"  ok    living-x   both living-person gates see the same {len(seen)} person(s)")
    return 0


def main():
    if not DIST.exists():
        print("  ok    places    no build to read - run the build first")
        return 0
    people = living_people()
    if not people:
        print("  ok    places    the data marks nobody as living, so there is nothing to guard")
        return 0

    pages = [(p, p.read_text(encoding="utf-8")) for p in sorted(DIST.rglob("index.html"))]
    fails = []
    guarded = 0

    for name, places in sorted(people.items()):
        # A name is matched case-insensitively as a whole phrase.
        pat = re.compile(re.escape(name).replace(r"\ ", r"\s+"), re.I)
        lowered = {p.lower() for p in places}
        guarded += 1
        for path, doc in pages:
            for m in pat.finditer(doc):
                win = doc[m.end(): m.end() + WINDOW]
                cut = BOUNDARY.search(win)
                if cut:
                    win = win[: cut.start()]
                rel = path.relative_to(DIST).parent.as_posix() or "/"

                # (a) a country pill inside this person's own card
                if re.search(r'class="[^"]*\btag\b[^"]*\bplace\b', win):
                    fails.append(f'/{rel}/ gives "{name}" a COUNTRY PILL. '
                                 f"A country is a place, and a living person gets none")

                # (b) a place this archive privately attaches to them, in a FACT
                #     position - never in prose. See trap 4.
                for fm in FACT.finditer(win):
                    text = strip(win[fm.start(): fm.start() + FACT_SPAN]).lower()
                    for p in sorted(lowered):
                        if p and p in text:
                            fails.append(f'/{rel}/ prints "{p}" as a FACT beside "{name}". '
                                         f"That place is attached to them in data/ and must not be published")

    if fails:
        print(f"  FAIL  places    {len(fails)} living-person place leak(s):")
        for f in dict.fromkeys(fails):
            print(f"          - {f}")
        print("          This archive's rule is \"no dates, no places, no photographs\".")
        return 1

    tally = ", ".join(f"{n} ({len(p)} place{'s' if len(p) != 1 else ''} withheld)"
                      for n, p in sorted(people.items()))
    print(f"  ok    places    {guarded} living person(s) named and given no place: {tally}")
    print("              NOTE: pills and fact positions only. PROSE IS NOT SCREENED, because the "
          "one sentence that\n              forced this limit was innocent - a Johannesburg "
          "belonging to another family's line.")
    return 0


if __name__ == "__main__":
    # BOTH, ALWAYS, AND THE WORST EXIT WINS. reconcile() is the cheaper check and the
    # more important one: it asks whether the OTHER gate is looking at anybody at all.
    sys.exit(max(main(), reconcile()))
