# Compared with the Defranceski archive

*10 September 2026. David asked for a side-by-side against
`daviddef.github.io/TheDefranceski/` and the Defranceski project itself, and for a list of what to fix,
improve, add or remove. This is that list, with the corrections it forced first.*

## Two things I had wrong, corrected before anything else

**1. The palette.** I said earlier that the Lerena tokens were identical to *Falco's*, then that they
were a deliberate cool variant. Both wrong. **The Lerena `styles.css` root block is byte-identical to
Defranceski's** — every token, the same three typefaces, the same `--maxw:1080px`. Lerena inherited the
**Defranceski** design system exactly. **Falco is the outlier**, with a warm palette (ink `#221D18`,
accent `#8A2B16`) against the shared cool one (ink `#16222A`, accent `#1F5C6B`).

**2. The scale gap.** Defranceski has **65 page files and 38 components**. Lerena has **21 and 2**. That
is not a defect on its own — the Defranceski research is older and far deeper — but it means most of what
follows is *absent*, not *wrong*.

---

## FIX — where this site contradicts itself

These are not gaps. They are places where the Lerena site says one thing and does another.

### 1. The living-person rule is broken by our own pages ⚠︎

Our footer: *"Living people are excluded from this build."*

Our `/direct-line/` publishes **Cheryl Anne Lerena, b. 14 Oct 1955, born Johannesburg, later Brisbane**,
with **both marriages named**, under a chip that reads **"Omitted"** and a caption that reads *"Details
withheld under the rule on living people."* That is the opposite of withheld. And `/dna/` now discusses
her test.

**Defranceski's rule is different and workable:** *"Living people appear by name only — no dates, no
places, no photographs."*

**Decide one and honour it.** Either adopt the Defranceski rule and strip her dates, places and
marriages; or honour ours and remove the row. The present state is the worst of both — it claims a
protection it does not provide.

### 2. Two chip vocabularies on one site

The home page advertises **Documented · Inferred · Family lore** — the Defranceski *confidence*
vocabulary. The register and person pages use **Connected · Excluded · Unplaced** — a *connection*
vocabulary. Both are legitimate; **having both, unexplained, is not.** A reader cannot tell whether a
chip is about how well a thing is known or about whether the person is kin.

**Fix:** keep both but make them visibly different classes of mark, and say so once, on `/method/`.

### 3. The footer promises corrections with nowhere to put them

Ours: *"Corrections welcome."* Defranceski's: *"Everything this archive got wrong is on **Corrections**"*
— and the page exists, counted, with a "serious" tally.

**This archive has made at least eight documented corrections in a fortnight** — Sarmiento/Belmonte,
Cayastá, the 1869 "household", Gabino at Rosario Colonia, "Chappell" as a maiden name, the 42%-scale
misreadings, the Falco palette claim, the Armando Lorena write-off. **They are buried in notes.** They
are the most credible thing this archive has and there is no page for them.

---

## ADD — pages Defranceski has and we do not

Ranked by what they would actually do for this archive.

| | Page | Why it matters here |
|---|---|---|
| 1 | **`/corrections/`** | See above. The single highest-value page we lack. |
| 2 | **`/search/`** | One box across people, places, register, sources. Defranceski also binds **`/`** as a keyboard shortcut from any page. We have a filter on one page only. |
| 3 | **`/changes/`** | A dated log of what changed. We have `findings.md` doing this privately; it deserves to be public. |
| 4 | **`/errands/`** | The four letters out and the two jobs that need David are in `requests/` as markdown, invisible to a reader. Defranceski publishes them. |
| 5 | **`/gaps/`** | *"What we cannot close"* — distinct from open questions. Ours would be short and honest: the Rosario baptism, María's maiden name. |
| 6 | **`/timeline/`** | We have the material (1882 birth, 1902 remounts, 1905 Roque, 1908 enrolment, 1911 marriage, 1931 stables, 1935 death, 1940 passport, 1950 death) and no timeline. |
| 7 | **`/about/`** | Method, ethics and sources in one place. Ours is scattered across `/method/` and the footer. |
| 8 | **`/households/`** | Falco has it too. A household view of the Cape family. |
| 9 | **`/photograph-these/`** | Maitland Cemetery grave 7719A, 7 Forth Road Newlands, the Koeberg Road stables. Someone in Cape Town could shoot all three in an afternoon. |
| 10 | **`/gallery/` or `/archive/`** | The passport scans and the enrolment card exist; nothing displays them. |

## ADD — components

- **`Rule` + `Motif`** — the labelled section rules used throughout both other archives. Purely visual,
  but it is a signature of the house style and we have none. Cheapest visible win.
- **`Pedigree` / `Lineage` / `TreeNode`** — their tree renderers. We now have `Ptree` from Falco, which
  covers the same ground; **no action, but worth knowing there are two implementations in the family.**

## IMPROVE

1. **The `ark()` helper.** Defranceski's register builds a FamilySearch link from a bare id:
   `familysearch.org/ark:/61903/1:1:{id}`. That is why they link thousands of rows and **we link five**.
   Store the id, not the URL, and build the link.
2. **The `.rec` third column.** Both archives use `.rec` with a `k / v / w` grid. Theirs uses `w` for the
   witness or the reason; **ours is always empty**, so every record grid on this site has a dead column.
3. **Register status filters as chips.** Theirs has clickable All / In the archive / Same name, not
   joined / Lead with live counts. Ours is a text box only.
4. **A `.rec` "why" for the person pages** — we have the material in `relations.tsv` notes and do not
   surface it.
5. **Nav depth.** Ours is five groups of three to six. Theirs is eight groups, several of them long. Ours
   is fine for twenty-one pages; **revisit when the count doubles**, not before.

## REMOVE / decide

- **`/roadmap/` and `/open-questions/` and `/hypotheses/` overlap.** Defranceski separates *gaps* (cannot
  close), *research log* (open/closed), *errands* (requests out) and *corrections* (got wrong). Ours has
  three pages doing two of those jobs and none doing the other two. **Consider folding `/roadmap/` into a
  new `/research-log/`.**
- **`/naairs/`** is a source-specific page. Defranceski would file that under an archive or sources page.
  Low priority, but it is the one page whose title means nothing to a reader.

---

## What is already right, and should not be touched

The **design system is correct and identical** — tokens, type, `.wrap .lab .dek .prose .panel .chip
.cardlink .scroll .rec .nm .txt .foot`, the header with burger and drawer, the `pagehead`, the footer
shape. The **register** now matches the house pattern (spelling groups, the *"N entries for M distinct
names, X with a link"* stat sentence, the source-or-reason column). The **person pages** now carry the
family chart. **None of that needs redoing.**
