#!/usr/bin/env python3
"""Build the public changelog from the git history.

Every commit in this repository is written as a paragraph, not a slug, because the reason
for a change is the interesting half. So the log IS the changelog; it only needs shaping.
"""
import json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "src" / "data"
SEP, FS = "\x1e", "\x1f"

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
    days.setdefault(date, []).append({"sha": sha[:7], "subject": subject, "body": body.strip()})

data = {"mechanical": mechanical,
        "days": [{"date": d, "commits": c} for d, c in sorted(days.items(), reverse=True)]}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "changes.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"changes: {sum(len(d['commits']) for d in data['days'])} commits across {len(data['days'])} days ({mechanical} mechanical rebuilds omitted)")
