#!/usr/bin/env python3
"""Catch a narrative page that has fallen behind the data.

The sibling Booyzen archive has carried a check like this for a while. This one was
written on 13 September 2026, the day it was needed three times:

  - /sources/ sat unchanged for three days under a heading claiming to list everything
    consulted, while five days of reading went unrecorded.
  - GILBERTO LERENA was established as a brother of Luis Eugenio - the single biggest
    structural finding in the archive - and NO PAGE SAID SO. /horses/ named him seven
    times as an unplaced coincidence and /hypotheses/ four times, both unaware.

    *** AND THIS FILE WOULD NOT HAVE CAUGHT THAT ONE. *** It was tested against exactly
    that failure, by stripping the fix back out of both pages, and it stayed quiet - because
    the words of the claim ("Justiniana Lenguas") were already on /searched/ from the
    marriage-act writeup. A NEW RELATIONSHIP BETWEEN TWO PEOPLE THE SITE ALREADY DISCUSSES
    introduces no new vocabulary, and a word-presence check cannot see it. Said plainly here
    so nobody reads a clean run as proof the pages are current. What this file does catch is
    research that never reached the site AT ALL - which is the other half of what went wrong
    that day, and it found one on its first run.
  - Three errands still described work that had been finished hours earlier, one of
    them asserting a FamilySearch block that had long since lifted.

Each check compares something the DATA knows against something the PAGES claim.
Findings print; nothing here fails the build, because drift is a judgement call and a
check that cries wolf is a check nobody reads.
"""
import json, re, sys, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "site" / "src" / "pages"
DATA = ROOT / "data"
NOTES = ROOT / "notes"

def norm(t):
    """Compare on letters alone - case, accents and curly quotes are not drift."""
    t = unicodedata.normalize("NFD", str(t))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", t.lower())

prose = []
for fp in PAGES.rglob("*.astro"):
    prose.append(norm(fp.read_text(encoding="utf-8")))
ALL_PROSE = " ".join(prose)

warns = []

# ---------------------------------------------------------------- 1. emphasised findings
# A register note wraps its headline in *** like this ***. If the archive thought a fact
# worth shouting in its own data, some page should be saying it.
#
# Two things this check learned the hard way, on the day it was written:
#   - Long words are not distinctive words. Scoring on length alone let the Gilberto
#     finding pass, because "parents" and "September" are all over the site.
#   - Presence in the CORPUS is not presence of the CLAIM. Every word of that finding
#     already appeared somewhere; what was missing was the words appearing TOGETHER.
# So: rank the claim's words by how rare they are across the pages, take the rarest few,
# and require them to co-occur on a SINGLE page.
import collections
people = json.loads((ROOT / "site/src/data/people.json").read_text(encoding="utf-8"))
freq = collections.Counter()
for page in prose:
    for w in set(page.split()):
        freq[w] += 1
STOP = re.compile(r"^(september|october|november|december|january|february|archive|records?|"
                  r"register|document|documents|parents|children|surname|familysearch|montevideo|"
                  r"rosario|argentina|uruguay|however|because|between)$")
SKIP = re.compile(r"^(image read|documented|corrected|confirmed)\b", re.I)
silent = []
# Only people the NARRATIVE is about. An unplaced Lerena's register note is meant to
# live in the register and nowhere else; a CONNECTED person, or one the archive has
# itself flagged HIGH INTEREST, is one the prose pages are supposed to keep up with.
# Without this filter the check reported 28 findings and would have been ignored.
# A finding can be fully published and still trip a word-matcher, because prose does not
# repeat a register note verbatim. The sibling Booyzen archive keeps a list like this for
# the same reason: a warning that fires on every build is a warning nobody reads. Adding a
# name here is a CLAIM THAT SOMEBODY LOOKED - so it carries where the finding was published.
PUBLISHED = {
    "Don Luis Eugenio LERENA LENGUAS":
        "the Serena misindexing is written up at /searched/#searching-the-rarest-name-not-the-surname",
    "Gilberto LERENA (Gilberto Justiniano LERENA LENGUAS)":
        "his household and the 1886-1890 bracketing are on /horses/; the matcher trips on the word "
        "'assembled', which the page has no reason to use",
    "Carlos LERENA Salvanach (b.1884, son of Gilberto)":
        "the Cordon baptism parish is named on /horses/ inside his father's household table",
}
WATCHED = ("connected", "high")
for p in people:
    if p.get("aliasOf"):
        continue
    if not any(w in (p.get("statusRaw") or "").lower() for w in WATCHED):
        continue
    for m in re.finditer(r"\*\*\*\s*(.+?)\s*\*\*\*", p.get("note") or "", re.S):
        claim = m.group(1)
        if SKIP.match(claim):
            continue
        # A short claim is not a weak one. "HIS PARENTS ARE NOW NAMED: LUIS LERENA and
        # JUSTINIANA LENGUAS" has only two distinctive words once stopwords go, and a
        # three-word floor skipped it - which is how this check first missed the very
        # finding it was written for.
        words = [w for w in dict.fromkeys(norm(claim).split())
                 if len(w) > 4 and not STOP.match(w)]
        if len(words) < 2:
            continue
        rare = sorted(words, key=lambda w: freq.get(w, 0))[:3]
        if any(page.count(rare[0]) and all(r in page for r in rare) for page in prose):
            continue
        if p["name"] in PUBLISHED:
            continue
        silent.append((p["name"], claim[:90], "+".join(rare)))
        break
if silent:
    warns.append("%d register finding(s) the archive emphasised in its own data that no single page "
                 "makes:\n      " % len(silent)
                 + "\n      ".join(f"{n} - \u201c{c}\u2026\u201d  [{k}]" for n, c, k in silent[:8]))

# ---------------------------------------------------------------- 2. research never published
# A TSV is a piece of research. If no page and no note mentions its filename or its
# subject, the work exists only on disk.
cited = ALL_PROSE + " " + " ".join(norm(f.read_text(encoding="utf-8")) for f in NOTES.glob("*.md"))
sources = norm((DATA / "sources-consulted.tsv").read_text(encoding="utf-8"))
orphan = []
for tsv in sorted(DATA.glob("*.tsv")):
    stem = tsv.stem
    if stem in ("corrections", "errands", "gaps", "timeline", "photograph-these",
                "sources-consulted", "lerena-register", "relations", "direct-line"):
        continue
    key = norm(stem.replace("-", " "))
    words = [w for w in key.split() if len(w) > 4]
    if not words:
        continue
    if not any(w in cited for w in words) and not any(w in sources for w in words):
        orphan.append(stem)
if orphan:
    warns.append("%d research file(s) nothing on the site or in the notes appears to mention: %s"
                 % (len(orphan), ", ".join(orphan)))

# ---------------------------------------------------------------- 3. errands that lie
# An errand whose detail says it is finished, still marked open - or the reverse.
rows = [l.rstrip("\n").split("\t") for l in (DATA / "errands.tsv").open(encoding="utf-8")
        if l.strip() and not l.startswith("#")]
hdr = rows[0]
for r in rows[1:]:
    d = dict(zip(hdr, r + [""] * len(hdr)))
    detail, status = d.get("detail", ""), d.get("status", "").strip()
    # Only a claim that the WHOLE errand is finished counts, and such a claim is made at
    # the START of the detail. Matching anywhere fired on "a trap FOUND on the way" and on
    # "four of the five are DONE" - progress narration inside a legitimately open errand.
    done_words = re.search(r"\b(DONE|ANSWERED|CLOSED)\b", detail[:90])
    if done_words and status in ("ready", "sent", "waiting-on-david"):
        warns.append("errand still %r but its own detail says %s: %s"
                     % (status, done_words.group(1), d.get("what", "")[:70]))
    # "was not blocked" and "could not be reached" are ordinary narration inside a
    # finished errand; only an explicit statement of unfinished work counts.
    if status == "done" and re.search(r"\b(still to do|not done|never been (?:done|turned|opened))\b",
                                      detail, re.I):
        warns.append("errand marked 'done' but its detail says otherwise: %s" % d.get("what", "")[:70])

print(f"{len(people)} people, {len(list(DATA.glob('*.tsv')))} data files, {len(prose)} pages")
if warns:
    print(f"\n{len(warns)} sign(s) a page has fallen behind the data:")
    for w in warns:
        print("   ", w)
else:
    print("nothing looks stale")
sys.exit(0)
