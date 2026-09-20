#!/bin/sh
# One gate, run as one command, so no exit code can be swallowed.
#
# AND THE SAME TRAP CATCHES THIS SCRIPT. On 15 September 2026 a commit went in on a RED GATE
# because the command was `./tools/verify.sh 2>&1 | tail -3 && git commit ...`. check-links.py had
# found a broken anchor and verify.sh exited non-zero - but a PIPELINE exits with the status of its
# LAST command, which is tail, which always succeeds. So the && fired. Running this script through
# a pipe defeats the whole point of it. Run it bare, or redirect to a file and check $? by hand:
#   ./tools/verify.sh > /tmp/v.log 2>&1; echo "EXIT=$?"; tail -5 /tmp/v.log
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
# Use `npm run build`, NOT `npx astro build`. CI runs `npm run build`, which chains
# check:living, check:kit, check:worklist and check:covers after astro. Running astro
# alone meant this gate said ALL GATES PASSED while the deploy failed: on 16 September
# 2026 three pushes in a row failed on a worklist row with an invalid state, and nothing
# local ever saw it. The local gate must run what CI runs.
# THE LOG IS PRIVATE TO THIS RUN, and that is not fussiness. /tmp/astro-build.log was
# shared with every other archive on this machine, so a parallel build in a DIFFERENT
# project overwrote it and this gate printed somebody else's failure as its own.
BUILDLOG="${TMPDIR:-/tmp}/lerena-build.$$.log"
# AND A KILLED BUILD MUST NOT LOOK LIKE A DATA FAULT. On 21 September 2026 three runs of
# this script died mid-build because another archive's publish script ran
# `pkill -f "astro build"`, which matches EVERY astro process on the machine and not only
# its own. The chain had already printed several `ok` lines by then, so the failure
# surfaced as a bare EXIT=1 under a clean-looking log, and two rounds went into looking
# for a fault in this archive's data before anyone thought to run `ps`. A process killed
# by a signal exits 128+N, so say so plainly instead of dumping a truncated build log.
if ( cd site && npm run build > "$BUILDLOG" 2>&1 ); then
  :
else
  rc=$?
  if [ "$rc" -ge 128 ]; then
    echo ""
    echo "  KILLED  the build was terminated by signal $((rc - 128)) - it did NOT fail on its own."
    echo "          Nothing here is evidence about this archive's data. Something outside this"
    echo "          script stopped the build; on this machine that has been another project's"
    echo "          publish script running pkill against a bare \"astro build\" pattern."
    echo "          Check with:  ps -eo pid,etime,command | grep \"[a]stro build\""
    echo "          Then simply run this script again."
    echo ""
  fi
  tail -30 "$BUILDLOG"
  rm -f "$BUILDLOG"
  exit 1
fi
rm -f "$BUILDLOG"
python3 tools/check-links.py
python3 tools/check-errands.py
python3 tools/check-evidence.py
python3 tools/check-corrections.py
python3 tools/last-alive.py
python3 tools/check-onsite.py
python3 tools/check-duplicates.py
python3 tools/check-living-places.py
python3 tools/drift.py
echo "ALL GATES PASSED"
