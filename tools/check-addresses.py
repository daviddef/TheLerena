#!/usr/bin/env python3
"""A person address that was published must keep resolving, even after a rename.

WHY THIS EXISTS. On 12 October 2026 this archive moved to its own domain, and
walking the new host page by page turned up /people/pedro-lerena-vega/ — live that
morning, 404 by evening. Asking the frozen ledger the same question found it was
not one address but FIVE, two of them dead since 23 September.

*** THE MECHANISM, AND IT IS THE LEDGER'S OWN STATED WEAKNESS. ***
site/src/data/person-slugs.json freezes a slug per person so that reordering
data/lerena-register.tsv cannot shuffle anybody's URL. It is keyed by NAME. So a
RENAME - correcting a surname, moving a birth estimate inside a parenthetical -
does not move the key: it strands it, and build-people mints a fresh slug for the
new name, usually base-2. The ledger's own _why calls this "the fault this file
exists to prevent, merely made rarer".

*** AND NO EXISTING GATE CAN SEE IT, BY CONSTRUCTION. *** check-links follows the
links a build emits; a stranded address has no inbound link left, precisely
because the rename updated every reference to it. The build is internally
consistent and externally broken. That is why this check reads the LEDGER and the
REDIRECT TABLE rather than the built pages.

WHAT IT DOES. Every ledger key whose name is no longer a row in the register is an
address that was once published. Each one must resolve: either a page still builds
at that slug, or site/astro.config.mjs redirects it. Anything else is a promise
broken silently.

It is a GATE. It exits 1.
"""
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MIN_KEYS = 100          # 714 on 16 October 2026; the ledger only grows
LEDGER = ROOT / "site" / "src" / "data" / "person-slugs.json"
REGISTER = ROOT / "data" / "lerena-register.tsv"
CONFIG = ROOT / "site" / "astro.config.mjs"
PAGES = ROOT / "site" / "dist" / "people"


def main():
    # REFUSES AT ZERO, AND BELOW A FLOOR (16 October 2026 sweep). The ledger only ever grows;
    # emptied, it printed "0 ledger keys" and passed, promising nothing about every address
    # the site had published.
    if not LEDGER.exists():
        print("  FAIL  addresses data: site/src/data/person-slugs.json is missing - 0 addresses examined")
        return 1
    led = json.loads(LEDGER.read_text(encoding="utf-8")).get("slugs", {})
    if len(led) < MIN_KEYS:
        print(f"  FAIL  addresses only {len(led)} ledger key(s), under the floor of {MIN_KEYS} - "
              "the slug ledger has lost entries, and every address it forgot is no longer promised")
        return 1
    names = set()
    with REGISTER.open(encoding="utf-8") as fh:
        for row in csv.reader((l for l in fh if not l.startswith("#")), delimiter="\t"):
            if row and row[0] and row[0] != "name":
                names.add(row[0].strip())
    cfg = CONFIG.read_text(encoding="utf-8") if CONFIG.exists() else ""

    orphans = {k: v for k, v in led.items() if k not in names}
    bad = []
    for name, slug in sorted(orphans.items(), key=lambda x: x[1]):
        has_page = (PAGES / slug).is_dir()
        has_redirect = f"'/people/{slug}'" in cfg
        if not has_page and not has_redirect:
            bad.append((slug, name))

    if bad:
        print("  FAIL  addresses %d published person address(es) resolve to nothing:"
              % len(bad))
        for slug, name in bad:
            print("          - /people/%s/" % slug)
            print("              minted for %r, which is no longer a row in the register" % name)
        print("          A rename strands its ledger key and mints a new slug; the old")
        print("          address stays published. Add a redirect in site/astro.config.mjs")
        print("          pointing it at the page that person is on now.")
        return 1

    print("  ok    addresses %d ledger key(s), %d stranded by a rename, every one still"
          % (len(led), len(orphans)))
    print("                   resolving by a page or a redirect")
    return 0


if __name__ == "__main__":
    sys.exit(main())
