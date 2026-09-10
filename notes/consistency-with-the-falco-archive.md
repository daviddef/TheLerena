# Consistency with the Falco archive

*10 September 2026. David asked whether the Lerena site has the equivalent of the Falco register, and
said the two sites need to stay consistent. It did have one. It was not consistent. It is now.*

## What was already shared — corrected

**An earlier version of this note said the two palettes were identical. They are not, and the error was
mine.** I read the Falco tokens, assumed ours matched, and wrote Falco's hex values as though they were
ours. What is actually shared is the **design system**, not the colours:

- **The same token names**: `--ground --panel --ink --ink-2 --ink-3 --rule --rule-strong --accent
  --ochre --terra --serif --sans --mono`.
- **The same three typefaces**: EB Garamond, Libre Franklin, IBM Plex Mono.
- **The same component vocabulary**: `.wrap .lab .dek .cap .prose .panel .grid .chip .cardlink .scroll
  .rec .nm .txt` — and now `.ptree` as well.

**The values differ, and look deliberate.** Falco is warm — ink `#221D18`, accent `#8A2B16`, a brick
red. Lerena is cool — ink `#16222A`, accent `#1F5C6B`, a teal, with `--terra #A8442B` for warnings.
Each archive has its own colour and shares its grammar. If the two are meant to be indistinguishable
that is a one-line change to `styles.css`; it has not been made, because it looks like a choice rather
than a drift.

## What was different, and is no longer

The Falco register is a very different scale — **9,058 entries for 4,356 distinct names** against our
125 — but scale was never the inconsistency. The *conventions* were.

| | Falco had | Lerena had | Now |
|---|---|---|---|
| Title | *The register* | *Name Register* | **The register** |
| Eyebrow | *Every named individual this archive has found* | *Every Lerena encountered anywhere* | **matched** |
| Opening stat | *"N entries for M distinct names, X with a link… the other Y say why no link exists"* | none | **matched** |
| Caveat heading | *Read this before you read the list* | *Why keep this* | **matched** |
| Grouping | by surname, with a count on each heading | one flat table | **grouped, with counts** |
| Columns | Name / What the source says / Source | six separate columns | **matched** |
| Source column | a link, **or a stated reason there is none** | plain text, no links | **matched** |
| Filter | *Filter by name, place, year or source* · "N entries shown" | *Search the register* · "Showing all N people" | **matched** |

Nav labels were aligned too: **The Register**, **The People**, **What Has Been Read**.

## The one convention worth adopting for its own sake

**Every row now links to its source, or says in the Source column why it cannot.** That is the Falco
discipline and it is the right one, because it makes the archive's reach auditable: 5 of our 125 entries
carry a live link, and the other 120 now say precisely *why not* —

- *CEMLA results are not addressable — search the surname at cemla.com/buscador/*
- *FamilySearch index — ark not recorded for this entry*
- *family papers — held offline, not on a public site*
- *GRO index — no public per-record link*

**5 out of 125 is a poor showing, and saying so on the page is the point.** Falco links 8,377 of 9,058
because its harvests recorded the ark as they went; ours mostly did not. Every future entry should carry
its ark, and the `source_url` column now exists in `data/lerena-register.tsv` to hold it.

## Two differences deliberately kept

1. **The status chips** — *Connected · Excluded · Unplaced*. Falco marks provenance (*family tree*,
   *read in the register*, *reconstructed*); Lerena marks **connection to the line**. Both answer
   "how much should I trust this row?", and each is right for its project. Ours stays.
2. **&ldquo;The Line&rdquo; rather than &ldquo;The Spine&rdquo;.** Falco calls its descent page *The
   Spine*. Ours is titled *The line* throughout its own prose, and renaming the nav alone would leave the
   page contradicting its own heading. Flagged for David rather than changed unilaterally.

---

## Round two — the person pages

David asked for the person pages to follow the Falco pattern, with the lineage shown as a chart. They now
do, using the **same structure, the same class names and the same CSS** as
`daviddef.github.io/TheFalco/people/vincenzo-falco/`.

### The chart

A `<figure class="ptree">` with tiers — **Parents**, the subject with **Married** beside them, **N
children**, **N siblings** — and a legend. Class names match Falco exactly: `.tier .lab .row .node .nm
.dt .via .drop .sibs .key .sw`, and the `via-line` / `via-register` / `via-tree` modifiers.

**The point of the chart is not decoration. It is that every single edge says how it is known:**

| | |
|---|---|
| solid dark left border | **the archive's own line**, argued on `/direct-line/` |
| solid accent left border | **from a record this archive has read** |
| dotted left border | **from a family chart or tree — unverified** |

And under it, in words: *"Of the 6 relationships in the chart above, 3 are written in a record this
archive has read and 3 come from a family chart or a user-contributed tree, unverified."*

That sentence is the whole discipline of both archives in one line, and it is now on every page that has
a chart.

### Where the relationships come from

A new file, `data/relations.tsv` — one edge per row, `person · relation · other · dates · via · note`.
The build resolves each name against the register so a node links to a person page when we hold one, and
stands as a plain card when we do not. **Fifty-three edges** so far, covering four generations of the
direct line and the people who married into it.

### Two bugs the rebuild exposed

1. **`.prose` is a flex column**, not a paragraph class. Using it on a `<p>` made every inline `<strong>`
   its own row — which is why a bare **6** was floating in the middle of a sentence. Now wrapped properly.
2. **A place that escaped normalisation** — `arr. Buenos Aires 1907-07-14` had been sitting as its own
   one-person "place" beside the 43-person *Buenos Aires — arrivals*. The pattern only matched
   `arr. YYYY`. Fixed; the arrivals place now holds 44, and there are 28 places rather than 29.
