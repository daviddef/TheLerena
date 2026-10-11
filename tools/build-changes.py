#!/usr/bin/env python3
"""Build the public changelog from the git history.

Every commit in this repository is written as a paragraph, not a slug, because the reason
for a change is the interesting half. So the log IS the changelog; it only needs shaping.
"""
import json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "src" / "data"
SEP, FS = "\x1e", "\x1f"


def _balance(text):
    """Drop a trailing unmatched *** so emph() never leaves one on the page."""
    if text.count("***") % 2 == 0:
        return text
    cut = text.rfind("***")
    return (text[:cut] + text[cut + 3:]).replace("  ", " ").strip()

raw = subprocess.run(
    ["git", "log", f"--pretty=format:%H{FS}%ad{FS}%s{FS}%b{SEP}", "--date=format:%Y-%m-%d"],
    cwd=ROOT, capture_output=True, text=True, check=True).stdout

# Commits whose entire purpose is to regenerate this page carry no reasoning: they are the
# mechanical consequence of the commit before them. They are COUNTED and declared on the page
# rather than silently dropped, because an archive that quietly shortens its own log is doing
# the opposite of what this log is for.
MECHANICAL = {"Rebuild the changelog"}

days = {}
mechanical = 0
for chunk in raw.split(SEP):
    if not chunk.strip():
        continue
    sha, date, subject, body = (chunk.strip().split(FS) + ["", "", "", ""])[:4]
    if subject.strip() in MECHANICAL:
        mechanical += 1
        continue
    body = "\n".join(l for l in body.splitlines()
                     if l.strip() and not l.startswith("Co-Authored-By"))
    # *** A COMMIT MESSAGE CANNOT BE REWRITTEN, SO IT MUST BE MADE SAFE HERE. ***
    # Added 11 October 2026. changes.astro renders both fields through emph(), which turns
    # PAIRS of *** markers into <strong>. Thirty-five commits in this history quote register
    # prose and carry the markers with it, and SIX of them carry an ODD number - a quotation
    # that opened an emphasis and ended at the line break. emph() converts the pairs and
    # leaves the orphan standing, so three raw *** reached the published page and
    # check:pages refused the build, correctly.
    # The TSV guard that fails on an odd count stays exactly as it is: there, an unbalanced
    # marker is an author's mistake to fix. Here the author is the past and cannot be asked.
    subject, body = (_balance(subject), _balance(body))
    days.setdefault(date, []).append({"sha": sha[:7], "subject": subject, "body": body.strip()})

data = {"mechanical": mechanical,
        "days": [{"date": d, "commits": c} for d, c in sorted(days.items(), reverse=True)]}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "changes.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"changes: {sum(len(d['commits']) for d in data['days'])} commits across {len(data['days'])} days ({mechanical} mechanical rebuilds omitted)")
