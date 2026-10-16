# Plant-a-fault sweep, 16 October 2026

Asked for by the estate's landing-site session, run here at David's request: plant one fault in every
check and confirm it refuses; where a tool can print a count of 0, make it print what it examined and
refuse at zero. Re-runnable: `python3 tools/plant-faults.py` (works on a copy; needs a built `site/dist`).

**Result: 54 faults planted across 28 checks and generators; 50 caught, 4 not.** The first pass, before any fix and with some bad plants of mine, caught 23 of 42.

## What was wrong, and is fixed in this repo
Twelve tools printed "0 examined" and passed when given nothing, and one could not see a long name:

| tool | what passed that should not have |
|---|---|
| check-errands | an emptied errands file ("0 checked") |
| check-evidence | the evidence file missing ("nothing to check") |
| check-corrections | every `retired` cell emptied ("not enforced yet") - 19 enforced readings, silently off |
| check-addresses | an empty slug ledger ("0 ledger keys") |
| check-tree | no edges at all ("0 edge(s)") |
| check-duplicates | people.json missing ("run the build first") |
| check-people-named | all six record files gone ("0 file(s)") |
| check-superseded | no built pages ("18 retired claims; none asserted") |
| check-living-places | no build ("no build to read") |
| check-sources | an empty register ("0 plate(s)") |
| check-arity | an empty register ("0 register row(s)") |
| check-nulls | a blanket null about a FOUR-word register name ("Roque Luis Armando LERENA"): the name pattern cut it to three words; also now refuses when it scans nothing |

Each now prints what it examined and refuses at zero; the ones whose input only grows also have a floor
(addresses 100, tree 100, duplicates 100, superseded 100 pages).

Also: **CI did not run three of the local gate's checks** (check-errands, check-nulls, check-addresses).
They are now steps in `.github/workflows/deploy.yml`.

## Not fixed here, and why
- **last-alive** (a generator) and **drift** (advisory, `exit(0)` by design) cannot fail. On 13 October a
  dated phrase in a note made a man "alive on 21 August 1997"; the gate stayed green. Only reading the
  diff of `data/last-attested-alive.tsv` catches it. Needs a design decision: a reviewed-list ratchet for
  ALIVE AT entries is the candidate.
- **Kit, `check:living`**: passes with nobody flagged ("0 flagged"). Covered here by `check-living-places`
  and `check-living-standard`, which refuse on an empty roster (living.json no longer exists; 16 October,
  living-people standard v2); the kit's own check should refuse too.
- **Kit, `check:covers`**: with `accounts` emptied it prints a note and passes, counting nothing outstanding.
- **Kit, `check:rows`**: the floor file's `rows` key is never compared (only the six MARKS are), so a
  spine row lost with its marks intact is not seen.
- **Kit, `check:pages`**: prints "not run" and exits 0 without the other archives beside it - which is
  every CI run. It cannot fail there.
- **Kit, `check:kin`**: someone aged 250 is "Rare, not refused" - a note, not a failure (design).
