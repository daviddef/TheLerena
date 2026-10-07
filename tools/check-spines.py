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


DIRECT = ROOT / "data" / "direct-line.tsv"
PAGE = ROOT / "site" / "src" / "pages" / "direct-line.astro"


def direct_line():
    """The archive's own spine is kept TWICE, and this gates both joins.

    *** FOUND 7 OCTOBER 2026. *** data/direct-line.tsv holds the direct line with its
    evidence - arks, a passport serial, an interment register page and entry. And
    site/src/pages/direct-line.astro holds the SAME LINE AGAIN as a hard-coded array.
    *** THE PAGE RENDERS THE ARRAY. *** The TSV was declared a working log and read by
    nobody. They did not disagree, which was luck: hand-written descent has gone stale
    twice in this archive, which is why this file exists at all.

    THE OBVIOUS FIX WAS REFUSED, DELIBERATELY. The two are not the same shape - the TSV
    gives each wife her own row, the page folds her into a `spouse` field - so rendering
    the TSV would redraw the archive's most important page, and the TSV's `evidence`
    column was never written for publication: generation 3's names a LIVING person and
    carries a birth year inside a quoted retraction. Migrating would have published it.

    So the duplication STAYS and both joins are gated instead:
        the PAGE must agree with the TSV about every date it states, and
        the TSV must agree with the REGISTER, through the `register` column.
    A reader sees exactly what they saw before, and neither copy can drift alone.
    """
    bad = []
    if not DIRECT.exists() or not PAGE.exists():
        return bad, 0
    tsv = {}
    for r in rows(DIRECT):
        for k in ("born", "died"):
            v = (r.get(k) or "").strip()
            if v and v != "-":
                tsv.setdefault(r.get("person", ""), {})[k] = v
    page = PAGE.read_text(encoding="utf-8")
    checked = 0
    # SPLIT ON THE ENTRIES, do not try to bound them with a lookahead. The first
    # version used `.{0,400}?` and matched ONE row of four, because these notes run
    # longer than that - a gate that silently checks a quarter of what it claims.
    start = page.find("const rows = [")
    block = page[start:page.find("];", start)] if start >= 0 else ""
    for chunk in block.split("{ gen:")[1:]:
        m = re.search(r'name:\s*"([^"]+)"', chunk)
        if not m:
            continue
        nm, body = m.group(1), chunk
        low = nm.lower().split()
        row = next((v for k, v in tsv.items()
                    if low[0] in k.lower() and low[-1] in k.lower()), None)
        if not row:
            continue
        for key in ("born", "died"):
            pm = re.search(key + r':\s*"([^"]+)"', body)
            if not pm or key not in row:
                continue
            checked += 1
            # COMPARE THE DAY, NOT ONLY THE YEAR. The first version of this join used
            # years() alone, and a deliberate test changing "6 Oct 1924" to "7 Oct 1924"
            # SAILED THROUGH IT. Two copies of one line drifting by a day is the likeliest
            # error there is here, and a gate that cannot see it is decoration.
            if years(pm.group(1)) != years(row[key]) or daymonth(pm.group(1)) != daymonth(row[key]):
                bad.append(f'direct-line: the PAGE says {nm} {key} "{pm.group(1)}", '
                           f'data/direct-line.tsv says "{row[key]}"')
    return bad, checked


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

    dbad, dchecked = direct_line()
    bad += dbad

    if bad:
        print(f"  FAIL  spines     {len(bad)} spine claim(s) disagree:")
        for b in bad:
            print(f"          - {b}")
        print("\n          A ladder on a page is a claim like any other. Fix the spine, or correct")
        print("          the register and say so on /corrections/.")
        return 1

    print(f"  ok    spines     {checked} date(s) on {linked} linked spine row(s) agree with the "
          f"register; {dchecked} on /direct-line/ agree with data/direct-line.tsv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
