#!/usr/bin/env python3
"""An errand that is finished must not still say "ready".

WHY THIS EXISTS. On 15 September 2026 the errand "Sancho's 1791 marriage - FIVE
FILMED BOOKS" sat at status `ready`, addressed to David, for hours after the act
had been found, read, transcribed and published - still telling him to go and
find it, and still calling a disproved film attribution "THE CHEAPEST TEST IN THE
ARCHIVE". Nothing was checking, so nothing complained.

Every convention that held in this estate held because a build refused when it
slipped. This one refuses.

The rule is deliberately narrow, because a noisy check gets switched off:
an errand whose status is NOT done, whose own detail text announces that it is
finished, is a contradiction and fails the build.
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ERRANDS = ROOT / "data" / "errands.tsv"

# Phrases an errand uses about ITSELF when it is over. Kept tight on purpose:
# "found" alone is far too common in a research note to mean anything.
# Tightened on its first run, which threw a false positive: an errand said the
# task "cannot be closed online at all", meaning the WORK was impossible, and the
# checker read it as the ERRAND being finished. A bare "closed" is useless here.
# Each pattern below must assert that THIS ERRAND is over, not that something
# else is shut.
FINISHED = [
    r"\bCLOSED\s+\d{1,2}\s+\w+\s+\d{4}",      # "CLOSED 15 September 2026"
    r"\bTHIS ERRAND IS (NOW )?CLOSED\b",
    r"\bERRAND IS CLOSED\b",
    r"\bIS DONE\s*[-\u2013]\s*DO NOT REDO\b",
    r"\bDO NOT REDO IT\b",
    r"\bnothing here is left for david to do\b",
    r"\bthis errand is no longer needed\b",
    r"\bthis errand is superseded\b",
]
OPEN_STATES = {"ready", "waiting-on-david", "sent", "replied", "status"}


def main():
    rows = [l.rstrip("\n") for l in ERRANDS.open(encoding="utf-8")
            if l.strip() and not l.startswith("#")]
    hdr = rows[0].split("\t")
    try:
        i_what, i_status, i_detail = hdr.index("what"), hdr.index("status"), hdr.index("detail")
    except ValueError:
        print("  FAIL  errands    header is not what/who/status/detail/sent_on")
        return 1

    bad = []
    for n, line in enumerate(rows[1:], start=2):
        f = line.split("\t")
        if len(f) <= max(i_what, i_status, i_detail):
            continue
        status, detail, what = f[i_status].strip(), f[i_detail], f[i_what]
        if status not in OPEN_STATES:
            continue
        for pat in FINISHED:
            if re.search(pat, detail, re.I):
                bad.append((n, status, what[:70], re.search(pat, detail, re.I).group(0)))
                break

    for n, status, what, hit in bad:
        print(f'  FAIL  errands    row {n} is "{status}" but its detail says "{hit}" — {what}')
    if bad:
        print(f"  FAIL  errands    {len(bad)} errand(s) finished but still open. "
              f"An errand nobody closes is an errand somebody repeats.")
        return 1
    print(f"  ok    errands    {len(rows)-1} checked, none finished-but-open")
    return 0


if __name__ == "__main__":
    sys.exit(main())
