# Estate clean-up, 23 November 2026: menu counts and the reach proof

David's three decisions of 23 November 2026 ("roots and routes, remove it"; "github links, no"; "menus, do all"), done in one pull request, one commit each.
Not live until David merges.

## Menu links, before and after

Counting every link in the header menu (a group heading that is a link counts one; the pulse button, search and the Tree Canvas button are not menu links).

| Group | Before | After | What changed |
|---|---:|---:|---|
| Start | 3 | 3 | Home, The story, About: as is |
| Our line | 5 | 5 | The Spine, The Estate, The Passport, The Enrolment Card, The Horses: as is (the archive's own voice) |
| People | 9 | 5 | Lists (The People, Every Name, The Register, The Marriages) and ONE link, "Drawn" (`/drawn/`). Households does not exist here |
| Places & families | 9 | 9 | Same shape; the group is now "The families" with its first link the hub "All the families" (`/families/`), then Taylor (the archive's own line) and Fernandez; Places, The Atlas, The Lines, Argentina, Uruguay, South Africa as is |
| The name | 1 | 1 | The Name. There is no forenames page here (absent, would need a decision) |
| Research | 17 | 13 | The eight core pages in the three groups plus the group heads and this archive's Roadmap; ONE "Deep dives" heading that links to `/research/deep-dives/` |
| **Total** | **44** | **36** | |

## What left a menu, and where it is reached from now

| Page | Left | Reached from |
|---|---|---|
| `/tree/` Our line, drawn | People > Drawn | `/drawn/` |
| `/trees/` The trees | People > Drawn | `/drawn/` (and `/roots/` redirects here) |
| `/bloodline/` Blood relatives | People > Drawn | `/drawn/` |
| `/timeline/` The Timeline | People > Drawn | `/drawn/` |
| `/direct-line/` The Spine | stays in Our line | also listed on `/drawn/` |
| `/roots/` Roots & Routes | People > Drawn | removed: now a redirect to `/trees/` |
| `/hypotheses/`, `/family-papers/`, `/dna/`, `/naairs/`, `/national-archives/` | Research > Deep dives (five links) | `/research/deep-dives/` (the heading in the menu), `/research/sources-and-method/`, `/research/` |
| the nine family pages other than Taylor and Fernandez | (already out of the menu since 12 Nov) | `/families/` ("All the families"), which links every one |

The hubs read the same lists as the menus (`lib/drawn.js`; `lib/research-menu.js`), so a menu and its hub cannot disagree. Both are indexable, in the sitemap, in the search index
(`tools/build-pages.py`) and in the book (`site/src/data/book.json`, so `check:book` places them).

## The kit's inventory

`scripts/menu-inventory-kit.py` (this archive's wrapper for the kit's `menu_inventory.py`; run from the repo root), the old build of `origin/main` against the new one:

- `compare` (the 55 in-scope pages of `docs/menu-scope.json`, `/roots/` excluded from the snapshot because the page was removed on purpose): every old URL still answers; every text
  block is kept except ONE, the paragraph on `/changes/` whose last sentence lost its GitHub link (declared in `docs/menu-text-changes.json`; blocks are stored as hashes, so the kit cannot match it by its start).
- `/roots/` itself: the old address answers (a redirect to `/trees/`, a `noindex` stub, not in the sitemap). Its 71 text blocks went with the page, on purpose.
- `sitediff` (every page of the old build against the new one): 3,283 pages before, 3,285 after; none gone; two new (`/drawn/`, `/research/deep-dives/`); every changed page is declared
  in `docs/menu-text-changes.json` (`/roots/`, `/contents/`, `/part/how-we-know/`, `/part/everyone/`, `/changes/`, `/search/`, and every `/people/*` page, which lost one paragraph).
