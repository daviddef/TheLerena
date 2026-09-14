#!/bin/sh
# One gate, run as one command, so no exit code can be swallowed.
#
# WHY THIS EXISTS. Through 14 September 2026 every check in this session was run as
#   python3 tools/consistency.py | tail -1
# and a pipeline exits with the status of its LAST command - tail, which always succeeds.
# So consistency.py's exit code gated nothing for a whole day, and an unpaired emphasis
# marker was committed while the checker was sitting there printing CONTRADICTION.
# The output was on screen. Nobody read it, because it had scrolled.
#
# Never pipe a checker into tail. Run this instead.
set -e
cd "$(dirname "$0")/.."
python3 tools/build-pages.py  > /dev/null
python3 tools/build-people.py > /dev/null
python3 tools/consistency.py
# Build from CLEAN. A half-written dist from a previously FAILED build poisons the next one:
# on 14 September 2026 astro reported "Cannot find module .../dist/chunks/astro/server_*.mjs"
# because leftovers from the broken PlaceSpark build were still on disk.
rm -rf site/dist
( cd site && npx astro build > /tmp/astro-build.log 2>&1 || { tail -20 /tmp/astro-build.log; exit 1; } )
python3 tools/check-links.py
python3 tools/drift.py
echo "ALL GATES PASSED"
