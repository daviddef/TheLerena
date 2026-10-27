# Lerena Family

## Record Atlas

The shared map lives at `../Record Atlas`. Research done here is only
useful to the next person if it gets there.

Invoke the `record-atlas-feedback` skill whenever you finish a search,
open a register, write to an archive, or find a source the atlas does
not list — as you do it, not in a sweep at the end. Record the
FamilySearch waypoint, not just the film number; the skill explains why.

## The linking standard (18 October 2026)

The eleven narrative pages named in `site/standard.json` are held to five rules (kit `docs/linking-standard.md`); the build ends with
`npm run check:standard`, which may only see each count go down (`site/.standardfloor.json`: counts, no name).
After research that adds an ark, a film or a person, `npm run build` is the check; if a count fell, `npm run floor:standard` locks it in.

- **L1/L2, names.** `tools/run-autolink.py` makes the names index from `people.json` (and the living list, outside the checkout). A person
  read from an act and not yet in the register gets a row in `data/lerena-register.tsv` (UNPLACED, the act in `source`, an existing place
  in `where_found`, and no `died <date>` or `death` wording about somebody else: `tools/last-alive.py` reads it). Only people the living
  rule shows dead; hold out anyone named only in a post-1946 paper. A spelling the data states for a person goes in
  `data/names-aliases.tsv` with its basis. A name that is a given name and the family surname ("Juan Lerena"), or the start of another
  person's longer name, is shared and links to the filtered people list (a marked, dotted link, `data-autolink="search"`), unless the data decides it:
  `tools/run-autolink.py` writes `resolve` rules from SPOUSE and CO-PARENT edges only ("a relative of exactly one bearer of this name is named in the
  same block within 120 characters"), and the link then goes to that bearer (`data-autolink="near"`). Never make a rule from a parent, child or
  sibling edge (a son is taken for his namesake father); a spouse recorded only in a note or not at all makes no rule, so record the edge.
- **L3/L4, records.** `tools/build-records.py` makes `site/src/data/records.json` from committed data (every ark the data prints, the films it
  cites, `data/record-plates.json` for the family papers). After the build `tools/link-records.py` links a DGS film or image number in a
  passage, applies `data/record-links.tsv` (the exact words that become the link, or `exempt:` with a reason, or `thumb:` for a held
  scan), and draws the kit's `Rec` markup. Never invent an address: where none is held the passage stays counted, or is exempted with
  that reason. FamilySearch plates, the Cape estate images and TNA downloads are link-only; only the family papers already on
  `/family-papers/` may be shown (never the 1971 and 1973 death notices). `src/components/Rec.astro` is the wrapper for a hand-written passage.
- **L5.** A ratchet only. `~/Downloads/audit-briefs/links/lerena-editorial.md` lists what an author can settle.

## The lines of the name (25 October 2026; /lines/, 27 October 2026)

The drawing is the kit's `BranchRivers` (kit `docs/lines.md`) on its own page, `/lines/` ("The Lines", Part I after The Name; `/name/` keeps
a pointer at `#s-lines`). `tools/build-lines.py` makes `site/src/data/lerena-lines.json` (the drawing) and `lerena-lines-ledger.json` (the
tables) from `data/lerena-lines.tsv` (a lane's status, span, note and node persons: a status is a research decision, written by hand),
`data/lerena-lines-unplaced.tsv` (the households written up; `people` names their register people), `data/lerena-lines-joins.tsv` (every
join the archive has a verdict on: documented | candidate | refused | open, in its own words; a candidate is drawn as a bridge) and
`data/people-lines.tsv` (`anchor`/`spouse` rows by hand, each with the act it rests on; `kin` rows derived). **Every person in people.json
stands in exactly one place** by the RULE in the tool (printed on the page): the register's own links (not `via: tree`) make family groups;
a group holding a lane's seeds is on that lane; a group holding two lanes' seeds fails unless the join is documented in the joins file;
any other group is a household in a pen, and a person alone is in the pen of the name alone or of the acts. A person is named only if a
page prints a birth year before the living line or a death; the rest are counts. Where a register note quotes an act naming a parent
the register does not link, record the edge (or an `anchor` row with the act); never decide a join here that the archive has not.
`npm run check:lines` is the kit gate. Never type a count of lines in prose: `ledger()` counts them. Living: the kit's `--years` gate runs
beside `check-living-years.py`; `data/living-year-allow.json` is the registry for both.

## The family ribbons and the direct-line tint (27 October 2026)

Every family page (`/families/<slug>/` and `/taylor/`) opens with the kit's `FamilyRibbon` (kit `docs/family-ribbon.md`), through
`site/src/components/FamilyLine.astro`: the family's own generations, then **how our line connects**. Two generated files, never typed:
`site/src/data/direct-line.json` (the kit's `directline.py` from `story.json`; `npm run check:directline`) and
`site/src/data/family-lines.json` (`tools/build-family-lines.py` from people.json, story.json and direct-line.json; `--report` lists each
family and every link the story states that the register does not draw). The tint (`is-ours`) is on the story ribbon and trees, the
`/lines/` lane whose people are all on the line (derived in `tools/build-lines.py`), the Spines, person-page charts, and the band on the
pages of the people in direct-line.json. A mother is on the line only where the story card says `spouseDirect` (the story's own tree
draws her as the parent of the next card). The line's break (generation 3, Sancho's children, no person) is never bridged: a family
that married into that generation says so in its not-connected block. `npm run check:familyribbon` is the kit gate.
