#!/usr/bin/env python3
"""Compute, for every person, the last date they are DEMONSTRABLY ALIVE.

WHY THIS EXISTS. Worklist row 82: the register records when a person is NAMED, not when
they were last alive, and a man named as a grandfather on a 1900 act may have been twenty
years dead. That confusion is invisible while the two are the same field.

WHAT IT DOES NOT DO. It does not guess. Dates in this archive live in prose, and prose
holds other people's dates too - "son of X, who died 1873" is not a date for this person.
So only two things are read, and both are unambiguous:

  death  - an explicit death date on this person's own row ("d. 15 Nov 1935", "died 1950")
  birth  - born_est, which is a floor and nothing more: everyone is alive at birth

Everything else is reported as UNKNOWN rather than filled in. The coverage number is
printed and is meant to stay honest, in the manner of consistency.py's own warning that
a pass over 106 of 277 is not a pass over the register.

THE USEFUL OUTPUT is not the date. It is the gap: people carried in the register with
nothing but a birth estimate, who are nonetheless cited in later records. Those are the
rows where "named" and "alive" can quietly diverge.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "lerena-register.tsv"
OUT = ROOT / "data" / "last-attested-alive.tsv"

MON = ("jan feb mar apr may jun jul aug sep oct nov dec")
# 1. an explicit death date on this person's own row - exact
DEATH = re.compile(
    r"\b(?:d\.|died)\s*"
    r"(?:(\d{1,2})\s+)?"
    r"(?:(" + "|".join(MON.split()) + r")[a-z]*\s+)?"
    r"(1[6-9]\d{2}|20[0-2]\d)\b", re.I)

# 2. a record type that only exists because the person is dead. These give a CEILING,
#    never a date: this archive has already been burned by treating an estate year as a
#    death year - Anton Armando died 3 April 2003 and was advertised in 2013, ten years
#    later. So they are tiered DEATH BY, and the file says so on every row.
DEATH_CERT = re.compile(r"\bdeath (?:cert\w*|notice)\b[^.;]{0,24}?(1[6-9]\d{2}|20[0-2]\d)", re.I)

# 3. *** AN ACT THE PERSON STOOD IN FRONT OF. Added 11 October 2026. ***
#    This file is called LAST DEMONSTRABLY ALIVE and until today it could only read
#    DEATHS. Everyone else fell to "born_est only - a floor, not an attestation", which
#    filed a man who appeared before a notary and signed his name on a stated day as
#    though nothing was known of him after his birth. Four such people arrived that day
#    (the Lerena y Lerena of Navarrete, at the Spanish consulate in Buenos Aires on
#    14 November 1900) and the gap became impossible to ignore.
#
#    *** BEING NAMED ON AN ACT IS NOT BEING ALIVE ON IT, which is why this is narrow. ***
#    A baptism names dead grandparents; an inventory names "el finado"; a marriage names
#    a widow's first husband. So a date is only taken when ALL of these hold:
#      - the row has no death date and no death-bearing record at all;
#      - the row's prose holds EXACTLY ONE full day-month-year date, so there is nothing
#        to rank and no chance of preferring one person's date over another's - this is
#        the same corroborate-don't-rank rule the 8 October bug below forced;
#      - the prose does not mark the person as already dead or as somebody's late spouse.
#    Anything else stays BIRTH ONLY. A missing attestation costs nothing; a wrong one
#    would put a living date on a dead man.
#    *** AND IT WAS WRONG TWICE WITHIN AN HOUR OF BEING WRITTEN, which is why the three
#    guards below exist. First attempt promoted 82 rows and 13 were nonsense:
#      - SEVEN HAD A 2026 DATE. This archive stamps its own prose - "*** TRANSCRIPT READ
#        11 OCTOBER 2026 ***", "withdrawn 9 October 2026" - so nearly every good note
#        carries the date somebody worked on it, and the tool read that as the day a man
#        born in 1836 was last seen alive. *** A DATE IN THE ARCHIVE'S OWN WORKING YEARS
#        IS THE ARCHIVE TALKING ABOUT ITSELF ***, never an attestation; and it cannot be
#        a living person either, because living people carry no dates here at all
#        (site/src/data/living.json, "named only - no dates, no places").
#      - SIX WERE DEATH OR BURIAL RECORDS whose one date is the day the person was
#        registered DEAD. "Flores Death Records - acta of 28 January 1919" says nothing
#        about anyone being alive, and the DEATH pattern above misses it because the
#        prose never writes "died <date>".
#    Both classes are now refused outright, and a candidate must also fall inside the
#    person's own possible lifetime.
ALIVE_DMY = re.compile(
    r"\b(\d{1,2})\s+(" + "|".join(
        "january february march april may june july august september october november december".split()
    ) + r")\s+(1[6-9]\d{2}|20[0-2]\d)\b", re.I)
# the words that mean "this person was already gone when the act was written"
# the archive's own working years - any date here is a note about the research, not a life
SELF_DATED = range(2020, 2031)
# a record that exists BECAUSE the person is dead. Its date is a death, not a life, and
# it is written in prose that never says "died", so DEATH above cannot see it.
DEAD_RECORD = re.compile(
    r"\b(?:death records?|death registrations?|death notices?|defunciones?|burials?|"
    r"interments?|cemeter(?:y|ies)|cementerio|entierro|sepelio|funerals?|obituar\w*|"
    r"probate|estate files?)\b", re.I)
# *** AND ANY MENTION OF A DEATH AT ALL STOPS THIS TIER. ***
# The first run tiered Rieta Maria Lerena "alive at 28 August 1937" off a row that says
# "*** Died *** *** 28 AUGUST 1937 ***, aged *** 1 ***", and Celia Juanico "alive at
# 24 August 1940" off "died Montevideo 24 August 1940". Both are DEATHS. The DEATH
# pattern missed them because it wants "died" followed by the date, and this register
# writes emphasis markers and place names in between - so a hole in the OLDER pattern
# was being filled by the NEWER one with the wrong label, on the wrong side of the
# line between living and dead.
# *** SO ALIVE AT IS NOW THE MOST TIMID THING IN THIS FILE: *** if the prose mentions a
# death - anyone's - the row is left alone, and where it mentions a death that DEATH
# could not parse, the tool SAYS SO at the end instead of quietly retiering it.
# *** EVERY PATTERN HERE TOLERATES THE PLURAL, and that is not a detail. *** Three
# separate leaks on 11 October 2026 were one bug wearing three hats: "Death Records"
# beat \bdeath record\b, "FreeBMD deaths" beat \bdeath\b, and "los finados" - an act
# calling a man and his wife THE DEAD - beat \bfinad[oa]\b. A word boundary after a
# singular noun is a trap in prose that pluralises freely in two languages.
DEATH_WORD = re.compile(r"\b(?:died|dies|deaths?|deceased|falleci\w*|muri[oó]s?|"
                        r"finad[oa]s?|difunt[oa]s?|muert[oa]s?|d\.)\b", re.I)
POSTHUMOUS = re.compile(
    r"\b(?:finad[oa]s?|difunt[oa]s?|deceased|the late|late husband|late wife|posthumous|"
    r"widow of|widower of|viud[oa] de|su esposo difunto|already dead|d\. by)\b", re.I)
FILE_YR    = re.compile(r"\b(?:estate|death notice|MHG|MOOC)\s*[\w/]*?(\d{3,6})/(\d{2})\b", re.I)


def file_year(mm):
    """SA estate/death-notice files are numbered NNNN/YY. Expand YY to a full year."""
    yy = int(mm.group(2))
    return 1900 + yy if yy > 30 else 2000 + yy


def rows(path):
    lines = [l.rstrip("\n") for l in path.open(encoding="utf-8")
             if l.strip() and not l.startswith("#")]
    hdr = lines[0].split("\t")
    return hdr, [dict(zip(hdr, (l.split("\t") + [""] * len(hdr))[:len(hdr)])) for l in lines[1:]]


def main():
    hdr, people = rows(REG)
    out, n_death, n_by, n_birth, n_none = [], 0, 0, 0, 0
    n_alive = 0
    unparsed_death = []
    ambiguous = []
    for p in people:
        name = p["name"]
        born = (p.get("born_est") or "").strip()
        hay = " ".join([p.get("source", ""), p.get("note", "")])
        ms = list(DEATH.finditer(hay))
        mc = DEATH_CERT.search(hay)
        mf = FILE_YR.search(hay)

        # *** A ROW'S PROSE CAN HOLD SOMEBODY ELSE'S DEATH, AND THIS USED TO TAKE IT. ***
        # Fixed 8 October 2026. This read the FIRST "died <date>" anywhere in the row and
        # called it "an explicit death date on this person's row". On that day Pablo
        # Armando's note gained a sentence describing the three burials in his own grave -
        # including "Careen Maria, two weeks old, died 27 June 1947" - and the tool moved
        # his death from "by 1950" to 1947-Jun-27, promoting it from a CEILING to a stated
        # DEATH. check-spines caught it, because the /uruguay/ ladder still said 1950.
        #
        # The bug is worse than one wrong cell: it fires precisely when a note gets BETTER.
        # The richer the prose, the more likely it names another person's death, and the
        # tool silently preferred whichever came first in the string.
        #
        # SO MATCHES ARE NOW CORROBORATED RATHER THAN RANKED BY POSITION. A death
        # certificate or an estate file gives an independent ceiling YEAR. Where the prose
        # offers several distinct death years, the ones that do not agree with that ceiling
        # are not this person's, and are dropped. Where nothing corroborates, the tool
        # refuses to choose: it falls back to the ceiling if there is one and says the row
        # was ambiguous, because a confident wrong date is worse than a stated bound.
        ceiling = int(mc.group(1)) if mc else (file_year(mf) if mf else None)
        yrs = {int(x.group(3)) for x in ms}
        chosen, basis = None, "explicit death date on this person's row"
        if len(yrs) == 1:
            chosen = ms[0]
        elif len(yrs) > 1 and ceiling is not None:
            keep = [x for x in ms if int(x.group(3)) == ceiling]
            if keep:
                chosen = keep[0]
                basis = (f"explicit death date on this person's row, chosen from {len(yrs)} "
                         f"different death years in the prose because it agrees with the "
                         f"{ceiling} record - the others are other people's")
            else:
                ambiguous.append(f"{name}: prose holds {sorted(yrs)}, none matching the {ceiling} record")
        elif len(yrs) > 1:
            ambiguous.append(f"{name}: prose holds {sorted(yrs)} and nothing corroborates any of them")

        if chosen is not None:
            day, mon, yr = chosen.groups()
            date = yr if not mon else (f"{yr}-{mon[:3].title()}" + (f"-{day}" if day else ""))
            out.append((name, born, date, basis, "DEATH"))
            n_death += 1
        elif mc or mf:
            yr = mc.group(1) if mc else str(file_year(mf))
            what = ("a death certificate" if mc and "cert" in mc.group(0).lower()
                    else "a death notice" if mc else "an estate or death-notice file numbered /%s" % mf.group(2))
            out.append((name, born, "by " + yr,
                        "%s dated %s - a CEILING, not a date: the file year can trail the death by years" % (what, yr),
                        "DEATH BY"))
            n_by += 1
        else:
            # *** AN ACT THE PERSON STOOD IN FRONT OF *** - see ALIVE_DMY above for why
            # this is deliberately narrow. Only ever reached when nothing above fired.
            dmy = [x for x in ALIVE_DMY.finditer(hay)
                   if int(x.group(3)) not in SELF_DATED]
            byr = None
            mb = re.match(r"(1[6-9]\d{2}|20[0-2]\d)", born)
            if mb:
                byr = int(mb.group(1))
                dmy = [x for x in dmy if byr <= int(x.group(3)) <= byr + 110]
            uniq = {(d.lower(), m.lower(), y) for d, m, y in (x.groups() for x in dmy)}
            if DEATH_WORD.search(hay) and len(uniq) == 1:
                unparsed_death.append(
                    f"{name}: prose mentions a death but DEATH could not parse a date "
                    f"from it; left on a birth floor rather than tiered ALIVE AT off "
                    f"{dmy[0].group(0)}")
            if (len(uniq) == 1 and not POSTHUMOUS.search(hay)
                    and not DEAD_RECORD.search(hay) and not DEATH_WORD.search(hay)):
                d, m, y = dmy[0].groups()
                out.append((name, born, f"{y}-{m[:3].title()}-{int(d):02d}",
                            "named on an act of that date and not marked as already dead - "
                            "ALIVE AT, not a death: it is the last day this archive can "
                            "SHOW the person living, and says nothing about when they died",
                            "ALIVE AT"))
                n_alive += 1
            elif born:
                out.append((name, born, born, "born_est only - a floor, not an attestation", "BIRTH ONLY"))
                n_birth += 1
            else:
                out.append((name, "", "", "no date of any kind on this row", "UNKNOWN"))
                n_none += 1

    with OUT.open("w", encoding="utf-8") as f:
        f.write("# *** LAST DEMONSTRABLY ALIVE - computed by tools/last-alive.py, not typed. ***\n")
        f.write("# *** BIRTH ONLY is not an attestation of life. *** It is the floor below which the\n")
        f.write("# *** ALIVE AT is the one tier that is neither. *** It is a day this archive can\n")
        f.write("# SHOW the person living - they appeared on a dated act and nothing marks them\n")
        f.write("# dead - and it says nothing whatever about when they died. Taken only from a\n")
        f.write("# row holding exactly one full date, because a richer note is likelier to hold\n")
        f.write("# somebody else's: see the 8 October note in this tool.\n")
        f.write("# SHOW the person living - they appeared on a dated act and nothing marks them\n")
        f.write("# dead - and it says nothing whatever about when they died. Taken only from a\n")
        f.write("# row holding exactly one full date, because a richer note is likelier to hold\n")
        f.write("# somebody else's: see the 8 October bug in tools/last-alive.py.\n")
        f.write("# person certainly existed, and it is exactly the row where 'named' and 'alive'\n")
        f.write("# can diverge without anyone noticing.\n")
        f.write("name\tborn_est\tlast_attested_alive\tbasis\ttier\n")
        for r in out:
            f.write("\t".join(r) + "\n")

    tot = len(people)
    known = n_death + n_by
    print(f"  last-alive  {tot} people: {n_death} exact death date, {n_by} dead-by-a-ceiling, "
          f"{n_alive} shown alive on a dated act, {n_birth} birth-estimate only, "
          f"{n_none} no date at all")
    print(f"              NOTE: {known} of {tot} ({100*known//tot}%) are known to have died, and "
          f"{n_alive} more can at least be SHOWN LIVING on a stated day without anything being "
          f"known of their death. The remaining {n_birth + n_none} carry a BIRTH FLOOR and nothing "
          f"more - being named in a later record is still not evidence they were alive for it, "
          f"which is why ALIVE AT is only taken from a row holding exactly one full date and no "
          f"word marking the person already dead.")
    if unparsed_death:
        print(f"              *** {len(unparsed_death)} row(s) say somebody died and the death "
              f"pattern could not read a date out of the prose. These are holes in DEATH, not "
              f"in ALIVE AT, and they are printed so they get fixed in the PROSE:")
        for u in unparsed_death:
            print(f"                - {u}")
    if ambiguous:
        print(f"              *** {len(ambiguous)} row(s) name more than one death and could not be "
              f"resolved; each fell back to a ceiling or a floor rather than guess:")
        for a in ambiguous:
            print(f"                - {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
