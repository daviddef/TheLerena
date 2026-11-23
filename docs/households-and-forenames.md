# Households and The forenames: the two pages the other archives carry (23 November 2026)

Two pages added to the menu this archive was missing them from (kit `menus.md`: People > Lists "Households where held"; The name "The Name, The forenames").
Not live until David merges. This archive keeps its own Roadmap page; it is unchanged.

## /households/ (People > Lists)

The kit's `Households` component, on `site/src/data/households.json`, made by `tools/build-households.py` (`npm run households:data`; `npm run check:households` fails if the committed file is not what
`people.json` gives). A household is a couple and the children the register records under them, made from the register's own links (a child's `father` and `mother`, a parent's `children` and `spouses`); the
rule is printed at the top of the tool. **It is not the 46 "households not yet placed" of `/lines/`**: those are family groups on no line, found by following every kin link until a group ends
(`tools/build-lines.py`), and the page says so.

- Known from, per household: a marriage in the register, parents named together (no marriage recorded between them), a parent on their own, the family tree. A child carries its own source where it differs.
- Living rule: a person is named only if their page is one this archive publishes and names (`build-lines.py` `safe`: not living, not held out, not an unpublished death) and is not on the independent living list
  every living gate uses (`livingcheck.py`, through `build-lines.living_slugs`). A household with a parent who may not be named is counted, not shown; a child who may not be named is not named. `check:living`,
  `check:living-standard` and `check:living-years` read the built page.
- A child whose rows name more than two parents is placed in no household (the register holds one such row).
- Where it is listed: the menu (People > Lists, `lib/site-menu.js`), the sitemap (built from the HTML), the search index (`tools/build-pages.py`), the book (`book.json`, Part VI, after The Register).

## /forenames/ (The name)

The kit's `SayYourName`, reading Record Atlas's given-name catalogue. **Nothing about forms is kept here.**

```bash
# from site/ : count the forms this archive has met (no person, no date), then fetch the Atlas catalogue with them as --seen
npm run given:atlas            # tools/build-given-forms-seen.py, then the kit's tools/atlas_given_names.py ... --seen ... --strict (online; exit 2 = a form of ours the Atlas lacks)
npm run check:forenames        # the offline gate, in the build: counts current, every form of ours in the committed catalogue (or held there as a different name), `seen` is this archive's
```

A form of ours the Atlas lacks is fixed at the Atlas: `given_name_variants.py add --family ... --status attested --kind archive --n N --ref archive:Lerena` (with its evidence), `publish`, then `npm run given:atlas`.
The Atlas checkout may be on somebody else's branch: clone its main into a scratch directory and run there (see CLAUDE.md, "Given names and old place names").

What the page chooses: eight of the Atlas's languages (Spanish, Latin, English, Italian, Portuguese, Catalan, Galician, Basque) and the names in which this archive has met a form in one of them. The Atlas sets `seen` from a spelling
alone, so a form written the same in several languages would be "attested here" in each; the page attributes a form met in these records to the first of those languages that writes it. Two forms the register holds
(Isabella, Telma) the Atlas records as a different name from the family it files near them (`notSame`), and the Atlas's rule is one family per form, so they cannot be added as forms of a name of their own; the page says so.
