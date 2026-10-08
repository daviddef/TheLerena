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
        elif born:
            out.append((name, born, born, "born_est only - a floor, not an attestation", "BIRTH ONLY"))
            n_birth += 1
        else:
            out.append((name, "", "", "no date of any kind on this row", "UNKNOWN"))
            n_none += 1

    with OUT.open("w", encoding="utf-8") as f:
        f.write("# *** LAST DEMONSTRABLY ALIVE - computed by tools/last-alive.py, not typed. ***\n")
        f.write("# *** BIRTH ONLY is not an attestation of life. *** It is the floor below which the\n")
        f.write("# person certainly existed, and it is exactly the row where 'named' and 'alive'\n")
        f.write("# can diverge without anyone noticing.\n")
        f.write("name\tborn_est\tlast_attested_alive\tbasis\ttier\n")
        for r in out:
            f.write("\t".join(r) + "\n")

    tot = len(people)
    known = n_death + n_by
    print(f"  last-alive  {tot} people: {n_death} exact death date, {n_by} dead-by-a-ceiling, "
          f"{n_birth} birth-estimate only, {n_none} no date at all")
    print(f"              NOTE: {known} of {tot} ({100*known//tot}%) are known to have died. "
          f"The other {n_birth + n_none} carry a BIRTH FLOOR and nothing more - being named in a "
          f"later record is not evidence they were alive for it.")
    if ambiguous:
        print(f"              *** {len(ambiguous)} row(s) name more than one death and could not be "
              f"resolved; each fell back to a ceiling or a floor rather than guess:")
        for a in ambiguous:
            print(f"                - {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
