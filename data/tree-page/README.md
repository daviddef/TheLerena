# Roots & Routes (the tree page)

Ten views of every person in the register who has died and has a page of their own: hourglass, fan, whole-tree and close-family maps, Atlas map, movements,
kinship, place lanes, eras, lifespans, an Orphans tab, a Surnames view and the five animated views (Night sky, Ink ledger, Household, Generations, Where they
lived). It is served at `/roots/`, and bare at `/roots/view.html` for frames (the kit's `PersonRootsViews`, which this archive's person page cannot use yet: see below).

| File | What it is | Edit by hand? |
|---|---|---|
| `tree.json` | people, parent links, years, places | no, generated |
| `place_map.json` | each place string with coordinates, country and Record Atlas id | no, generated (see below) |
| `place-additions.json` | place strings decided by hand, each with its reason | yes, with a reason |
| `atlas-data.json` | the Record Atlas slice: outlines, regimes, flags, events, collections | no, generated |
| `roots.html`, `roots.embed.html` | the page, whole and as a fragment for the site layout | no, generated |
| `tree.report.json` | counts, `unresolved_places`, and an `adapter` block with every number below | read it |
| `people.ged`, `slugs.json` | intermediates, not committed (`.gitignore`); a raw GEDCOM is never published | no |

## Rebuild

```bash
python3 tools/build-tree-page.py           # rebuild everything and run the page's own checks
python3 tools/build-tree-page.py --check   # exit 1 if the page is older than the data it was built from
```

Needs the Record Atlas checkout (`RECORD_ATLAS`, default `~/Projects/Family Projects/Record Atlas`), read only. The skill's scripts are vendored in
`tools/tree-page/` (the family-tree-page skill, template 1.6.0), so CI and other sessions do not depend on `~/.claude`.

## What is and is not on the page

- **Who.** `site/src/data/people.json`, minus every person marked `living` or `noindex` (nobody is drawn who has no page of their own). The converter then adds its
  own floor: nobody with no death recorded and a birth year in the last 110 years, or none at all, is drawn. A link that rests only on a tree (`via: tree`) is not followed.
- **Years.** A circa year (`1875c`) and a year worked out from a parent, child or spouse are flagged on the page ("c. 1875"); a death not recorded shows "1809–?".
- **Places are never guessed, and each person has one.** The register's only place for a person is the birthplace as printed (`where found` is the search that produced
  the person, not a residence, and no death place is held), so the page draws a person where they were born; the viewer shows a person with no death place as dying where born.
  A string is placed where `data/era-ground.tsv` put it (its town, at that town's point in `data/era-towns.tsv`, the country from the Atlas's `geo.country_of`); a string
  era-ground refused is left unresolved, except where `place-additions.json` decides it (with its reason, at the Atlas's own point) or the Atlas names it once in the country the string
  itself names. A string the archive qualifies (presumed, probably, from a tree) is never placed. Where era-towns.tsv's point stands for a department or section, the page says the
  department's town or the department (`how` in `place_map.json`). A person whose own place is not resolved is drawn at a parent's, spouse's or child's birth place, or not drawn.
- **Colour** is the surname family in the Record Atlas catalogue (`data/surname-families.json`, read at build, never copied); a surname the catalogue does not hold is its own colour.
- **Sex** is not held by the register. It is taken from a father/mother role, a title (Don, Dona), or a first given name that the register's own parent links show only as a father's or only as a mother's; otherwise the viewer's two-value default ('m') is used, and `adapter.sex_unknown_drawn` says how many.
- **Two lives that cannot be one** (died before born, or over 110 years) are not drawn and are listed under `conflicts`.

## The person page

`site/src/pages/people/[slug].astro` is the kit's `PersonPage` in chart mode. The kit's `where` slot (where `PersonRootsViews` goes) is drawn only in story mode, and this
archive has no person in story mode, so the embed is not wired. When a person gets a story, pass `<PersonRootsViews pid=...>` in the `where` slot for the ids in
`site/public/roots-links.json` (the people the page draws), as the Blažević archive does.
