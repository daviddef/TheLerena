#!/usr/bin/env python3
"""The whole archive is one book: the kit's checkbook.py, wired in.  (17 October 2026)

    python3 tools/check-book.py          (from the repository root or from site/; npm run check:book does the latter)

The kit's tool reads the BUILT site and fails on a page nobody placed in site/src/data/book.json, a chapter with no
built page, a path in the book twice, a page without its running head, and a Previous/Next that differs from the
book's order. This wrapper hands it the built site WITHOUT the redirect stubs.

WHY THE STUBS ARE SET ASIDE. astro.config.mjs keeps every renamed or merged address alive as a one-line HTML redirect
(<meta http-equiv="refresh">), and Astro writes each as an index.html. They are addresses, not pages: they have no
header, no head and no foot, and the kit's own sitemap.py withholds them for the same reason. The kit's checkbook does
not (yet) skip them, so each would fail as 'unplaced' or 'no running head'. The test here is strict: a file under
1,000 bytes whose first 400 bytes carry the refresh tag. A real page is never that small, so a page cannot hide here.
The count is printed, so a growing number of stubs is visible.

Exit codes are the kit's: 0 pass, 1 fail, 2 not run (no book, no kit, nothing built). The build, verify.sh and CI stop
on any nonzero. ARCHIVE_OUT is honoured the way astro.config.mjs reads it.
"""
import os
import sys
import shutil
import pathlib
import tempfile
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
KIT = SITE / "node_modules" / "@daviddef" / "archive-kit" / "kit" / "tools" / "checkbook.py"
BOOK = SITE / "src" / "data" / "book.json"


def is_stub(f):
    try:
        if f.stat().st_size >= 1000:
            return False
        return 'http-equiv="refresh"' in f.read_text(encoding="utf-8", errors="ignore")[:400]
    except OSError:
        return False


def main():
    if not KIT.exists():
        print("  --    book       not run: %s is missing - the kit pin must be 516fad1 or later and `npm install` run in site/" % KIT.relative_to(ROOT))
        return 2
    if not BOOK.exists():
        print("  --    book       not run: site/src/data/book.json is missing")
        return 2
    dist = SITE / (os.environ.get("ARCHIVE_OUT") or "dist")
    if not dist.is_dir():
        print("  --    book       not run: %s is not built" % dist.relative_to(ROOT))
        return 2
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="lerena-book-"))
    stubs = kept = 0
    try:
        for f in dist.rglob("index.html"):
            rel = f.relative_to(dist)
            if any(part in ("node_modules", "_astro", ".git") for part in rel.parts):
                continue
            if is_stub(f):
                stubs += 1
                continue
            (tmp / rel.parent).mkdir(parents=True, exist_ok=True)
            shutil.copyfile(f, tmp / rel)
            kept += 1
        print("  book: %d built page(s) read, %d redirect stub(s) set aside (addresses, not pages)" % (kept, stubs))
        env = dict(os.environ)
        env.pop("ARCHIVE_OUT", None)
        return subprocess.run([sys.executable, str(KIT), "--dist", str(tmp), "--book", str(BOOK)], cwd=SITE, env=env).returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
