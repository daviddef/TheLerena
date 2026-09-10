# Consistency with the Falco archive

*10 September 2026. David asked whether the Lerena site has the equivalent of the Falco register, and
said the two sites need to stay consistent. It did have one. It was not consistent. It is now.*

## What was already shared

**The visual language is identical, and was already identical.** Both sites use the same tokens —
`--ground #F2EEE5`, `--panel #FAF7F1`, `--ink #221D18`, `--rule #DAD2C3`, `--accent #8A2B16`,
`--ochre #A8802C`, `--terra #2F5D50` — and the same three typefaces: EB Garamond, Libre Franklin,
IBM Plex Mono. Nothing needed doing there.

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
