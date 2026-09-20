#!/usr/bin/env python3
"""What this archive has found, and a reader cannot see.

THE GAP THIS FILLS. `check-onsite.py` asks whether a data file is IMPORTED by a page,
and 136 files answer "no" and are declared working logs, which is allowed. `drift.py`
asks whether a REGISTER finding reaches a page. Nothing asks the obvious third
question: those 136 working logs hold three quarters of a megabyte of research, and
125 of them carry emphasised findings. How much of that has a reader ever seen?

HOW IT DECIDES, and it is drift.py's method because drift.py paid for it:

    Long words are not distinctive words - "September" and "parents" are everywhere.
    And presence in the corpus is not presence of the claim; what is missing when a
    finding goes unpublished is the words appearing TOGETHER.

So each emphasised span is reduced to its three RAREST words, measured across the
built pages, and the finding counts as published only if those three co-occur on a
SINGLE page. That is the same bar the register findings are held to.

WHAT IT IS NOT. Not a gate. A working log is allowed to hold working notes - a control
that returned nothing, a query shape, a reminder. The report ranks files by how much
UNSEEN SUBSTANCE they hold so the worst offenders can be published first, and says
plainly that a high count is a prompt to look, not a verdict.

Usage:  python3 tools/unpublished.py [--verbose] [--file NAME] [--top N]
"""
import collections
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DIST = ROOT / "site" / "dist"
DECL = DATA / "_not-on-site.txt"

VERBOSE = "--verbose" in sys.argv
ONLY = None
TOP = 18
for i, a in enumerate(sys.argv):
    if a == "--file" and i + 1 < len(sys.argv):
        ONLY = sys.argv[i + 1]
    if a == "--top" and i + 1 < len(sys.argv):
        TOP = int(sys.argv[i + 1])

TAGS = re.compile(r"<[^>]+>")
CODE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.S | re.I)

# Words that are everywhere in a family archive and so distinguish nothing.
STOP = re.compile(
    r"^(january|february|march|april|may|june|july|august|september|october|november|december|"
    r"archive|archives|record|records|register|registers|document|documents|parents|children|"
    r"surname|familysearch|montevideo|rosario|argentina|uruguay|however|because|between|"
    r"september|marriage|baptism|burial|census|father|mother|daughter|brother|sister|"
    r"nothing|anything|something|everything|already|against|through|without|another|"
    r"reading|written|searched|control|controlled|tested|untested|found|finding|findings)$")

# A CLAIM asserts something about this family. A TRANSCRIPT or a catalogue title is
# working material - the reader is owed what it MEANS, not the shelfmark it came from.
# Without this split the report's top file was 17 "unseen findings" that were all
# archive catalogue headings: 'CAUSAS VARIAS, SIGLO XVIII', 'TITULO DEL REGISTRO...'.
CLAIMY = re.compile(r"\b(is|was|are|were|has|have|had|means|shows?|proves?|refutes?|"
                    r"confirms?|gives?|names?|settles?|stands?|rests?|cannot|does not|"
                    r"did not|is not|are not|never|now|makes?|puts?|places?|leaves?|"
                    r"turns? out|belongs?|explains?|answers?|opens?|closes?)\b", re.I)
SPANISH = re.compile(r"\b(de|del|la|el|los|las|que|por|con|anos|dias|mes|hijo|hija|"
                     r"natural|vecino|dicho|legitimo|libro|folio|tomo)\b", re.I)


def claimy(s):
    """Is this a statement a reader is owed, or working material?"""
    if not CLAIMY.search(s):
        return False
    words = s.split()
    if sum(1 for w in words if SPANISH.match(w)) > len(words) * 0.28:
        return False                      # a Spanish transcript, quoted for the record
    letters = [c for c in s if c.isalpha()]
    if letters and sum(1 for c in letters if c.isupper()) / len(letters) > 0.75:
        return False                      # A CATALOGUE HEADING IN CAPITALS
    return True


# A span that is only process talk is not a finding a reader is owed.
PROCESS = re.compile(
    r"^(not tested|untested|to test|test|open|closed|done|pending|next|todo|"
    r"controlled null|no result|zero|none|n/a|see |cf\.|as above|ditto)\b", re.I)


def prose_pages():
    """Every built page, as plain lowercase text. Dump pages count: a reader can read
    them. The register and the work list ARE published, whatever drift.py decides for
    its own purposes."""
    out = []
    for f in sorted(DIST.rglob("index.html")):
        t = CODE.sub(" ", f.read_text(encoding="utf-8", errors="replace"))
        t = html.unescape(TAGS.sub(" ", t)).lower()
        out.append((f, re.sub(r"\s+", " ", t)))
    return out


def spans(path):
    """Every *** emphasised *** span in a TSV, comments included - a working log keeps
    most of its findings in the comment block, which is exactly the point."""
    txt = path.read_text(encoding="utf-8")
    got = []
    for m in re.finditer(r"\*\*\*(.+?)\*\*\*", txt, re.S):
        s = re.sub(r"\s+", " ", m.group(1)).strip(" #\t")
        if len(s) < 25 or PROCESS.match(s) or not claimy(s):
            continue
        got.append(s)
    return got


def main():
    if not DIST.exists():
        print("no build to read - run npm run build first")
        return 1
    pages = prose_pages()
    freq = collections.Counter()
    for _, t in pages:
        for w in set(re.findall(r"[a-z]{4,}", t)):
            freq[w] += 1

    files = [l.strip() for l in DECL.read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]
    if ONLY:
        files = [f for f in files if ONLY in f]

    report = []
    for name in files:
        p = DATA / f"{name}.tsv"
        if not p.exists():
            continue
        unseen, seen = [], 0
        for s in spans(p):
            words = [w for w in re.findall(r"[a-z]{5,}", s.lower()) if not STOP.match(w)]
            if len(words) < 3:
                continue
            rare = sorted(set(words), key=lambda w: freq.get(w, 0))[:3]
            if any(all(r in t for r in rare) for _, t in pages):
                seen += 1
            else:
                unseen.append((s, rare))
        if unseen:
            report.append((len(unseen), seen, name, unseen))

    report.sort(reverse=True)
    tot_unseen = sum(r[0] for r in report)
    tot_seen = sum(r[1] for r in report)
    print(f"UNPUBLISHED RESEARCH — {len(files)} working logs read, "
          f"{tot_unseen} finding(s) no page carries, {tot_seen} that a page does\n")
    for n, s, name, unseen in report[:TOP]:
        print(f"  {n:3} unseen ({s} published)  data/{name}.tsv")
        for span, rare in (unseen if VERBOSE else unseen[:2]):
            print(f"        · {span[:132]}")
            print(f"          rarest: {'+'.join(rare)}")
        if not VERBOSE and len(unseen) > 2:
            print(f"        ... and {len(unseen) - 2} more")
    if len(report) > TOP:
        print(f"\n  ... and {len(report) - TOP} more file(s) with unseen findings")
    print("\n" + "-" * 74)
    print("A high count is a PROMPT TO LOOK, not a verdict: a working log is allowed to")
    print("hold working notes. But a finding about this family that no page carries is")
    print("research the reader paid for and never got.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
