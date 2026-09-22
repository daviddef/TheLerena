#!/usr/bin/env python3
"""A descent spine may not disagree with the register about a date.

WHY THIS EXISTS, and it is one day old.

On 22 September 2026 the spine on /uruguay/ said AVELINO LERENA FERNANDEZ died on
*** 23 August 1890 at La Paz, Canelones ***. His register row, data/last-attested-alive.tsv,
data/1852-aguada-union-certificates.tsv and data/alberto-lerena-larriera.tsv all say the
*** 22nd, at Montevideo, registered the next day ***. Both wrong values came from one row of
data/montevideo-lerena-trunk.tsv - a FamilySearch tree file whose own header reads
"TIER: SECONDARY THROUGHOUT ... no row here may be cited as fact". The page cited it as fact,
and had done since the page was built.

The same morning, gen 4 of the same ladder had to be corrected for asserting
"Alejandro Maximo (1839-1903)" - an identification data/the-three-alejandros.tsv has never been
able to make, on a year two Montevideo birth acts put five years out.

*** TWO HAND-WRITTEN DESCENT FAILURES IN ONE DAY, IN ONE LADDER. *** Moving the ladders into
data/descent-spines.tsv put them where the emphasis, raggedness and drift checks can see them.
It did NOT make them agree with the register, because nothing compared the two. This does.

WHAT IT COMPARES. Only what it can compare exactly: a spine row that names a register row in its
`register` column must agree with that row's BIRTH YEAR, and with the DEATH DATE that
tools/last-alive.py computed from the register's own prose. A spine cell that says "about 1767"
or "about 1775-85" is a hedge and is checked as a year; an empty cell asserts nothing and is
skipped; a "-" means the person has no register row at all, which is allowed.

WHY NOT MATCH ON NAMES. Because the two files do not spell people the same way - "Avelino Lerena
Fernandez" against "Avelino LERENA Fernandez (son of Sancho)" - and a fuzzy match that silently
matches nothing is worse than no check, which is the whole lesson of the file above.

It is a GATE. It exits 1.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPINE = ROOT / "data" / "descent-spines.tsv"
ALIVE = ROOT / "data" / "last-attested-alive.tsv"
REG = ROOT / "data" / "lerena-register.tsv"

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def rows(path):
    lines = [l for l in path.read_text(encoding="utf-8").split("\n")
             if l.strip() and not l.startswith("#")]
    hdr = lines[0].split("\t")
    return [dict(zip(hdr, (l.split("\t") + [""] * len(hdr))[:len(hdr)])) for l in lines[1:]]


def years(s):
    """Every 4-digit year a cell mentions - 'about 1775-85' gives {1775}."""
    return set(int(y) for y in re.findall(r"\b(1[6-9]\d\d|20\d\d)\b", s or ""))


def daymonth(s):
    """(day, month) from '22 August 1890' or '1890-Aug-22'; None if absent."""
    s = (s or "").strip()
    m = re.search(r"\b(\d{1,2})\s+([A-Za-z]{3,})\s+(1[6-9]\d\d)", s)
    if m:
        mo = MONTHS.get(m.group(2)[:3].lower())
        return (int(m.group(1)), mo) if mo else None
    m = re.search(r"\b1[6-9]\d\d-([A-Za-z]{3})-(\d{1,2})\b", s)
    if m:
        mo = MONTHS.get(m.group(1).lower())
        return (int(m.group(2)), mo) if mo else None
    return None


def main():
    alive = {r["name"]: r for r in rows(ALIVE)}
    reg = {r["name"]: r for r in rows(REG)}
    bad, checked, linked = [], 0, 0

    for r in rows(SPINE):
        name, target = r.get("name", ""), (r.get("register") or "-").strip()
        if target in ("", "-"):
            continue
        linked += 1
        if target not in reg:
            bad.append(f'{name}: register column names "{target}", WHICH IS NOT A REGISTER ROW')
            continue

        # ---- birth year
        sp, rg = years(r.get("born", "")), years(reg[target].get("born_est", ""))
        if sp and rg:
            checked += 1
            if not (sp & rg):
                bad.append(f'{name}: spine says born "{r["born"]}", register says '
                           f'"{reg[target]["born_est"]}"')

        # ---- death date, as last-alive.py computed it from the register's own prose
        a = alive.get(target)
        if a and (a.get("tier") or "").strip() == "DEATH" and r.get("died", "").strip():
            checked += 1
            sd, rd = daymonth(r["died"]), daymonth(a["last_attested_alive"])
            sy, ry = years(r["died"]), years(a["last_attested_alive"])
            if sy and ry and not (sy & ry):
                bad.append(f'{name}: spine died "{r["died"]}", register "{a["last_attested_alive"]}"')
            elif sd and rd and sd != rd:
                bad.append(f'{name}: spine died "{r["died"]}", register "{a["last_attested_alive"]}" '
                           f'- SAME YEAR, DIFFERENT DAY. A registration date is not a death date.')

    if bad:
        print(f"  FAIL  spines     {len(bad)} spine claim(s) disagree with the register:")
        for b in bad:
            print(f"          - {b}")
        print("\n          A ladder on a page is a claim like any other. Fix the spine, or correct")
        print("          the register and say so on /corrections/.")
        return 1

    print(f"  ok    spines     {checked} date(s) on {linked} linked spine row(s) agree with the register")
    return 0


if __name__ == "__main__":
    sys.exit(main())
