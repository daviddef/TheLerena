#!/bin/sh
# THE BOX GATE ON THE RIBBON FLAGS (27 October 2026; kit docs/ribbon-flags.md). The kit's checkflagfit.mjs opens the built pages in
# Chrome and measures every ribbon card with its mini flags and with them hidden, at 1440, 1100 and 390: a card one pixel taller or
# wider, or a strip that touches the glyph, "Gen. n", the name or the years, fails. Pages: /story/ and every family page
# family-lines.json holds (its `page`). It serves site/dist itself on a local port and stops the server after.
#
# Needs playwright-core and an installed Google Chrome; neither is a dependency of this site (the kit says so too). CI installs
# playwright-core without saving it, in the checkout's root node_modules (outside site/), then runs this; locally the same:
#   npm i --prefix . --no-save --no-package-lock playwright-core@1.63.0   (from the checkout's root; node_modules/ is ignored)
# Exit 0 clean, 1 a card changed size or a strip touches a word, 2 it could not run (which fails CI: not run is not a pass).
set -e
cd "$(dirname "$0")/../site"
KIT=node_modules/@daviddef/archive-kit/kit/tools
DIST="${ARCHIVE_OUT:-dist}"
[ -f "$DIST/story/index.html" ] || { echo "  --    flagfit    not run: $DIST/story/index.html is missing (build first)"; exit 2; }
PORT="${FLAGFIT_PORT:-4391}"
python3 -m http.server "$PORT" --bind 127.0.0.1 -d "$DIST" > /dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null || true' EXIT INT TERM
i=0
until python3 -c "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:$PORT/story/')" 2>/dev/null; do
  i=$((i + 1)); [ $i -gt 50 ] && { echo "  --    flagfit    not run: the local server did not start"; exit 2; }
  sleep 0.2
done
URLS=$(python3 -c "
import json
pages = ['/story/'] + [f['page'] for f in json.load(open('src/data/family-lines.json'))['families'] if f.get('cards')]
print(' '.join('--url http://127.0.0.1:$PORT' + p for p in pages))")
# shellcheck disable=SC2086
node "$KIT/checkflagfit.mjs" $URLS --widths 1440,1100,390
node "$KIT/checkflagfit.mjs" --selftest
