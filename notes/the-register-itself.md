# The register itself

*10 September 2026, late. The last thing standing between this archive and his baptism was an
assumption, and it has now been tested.*

## The assumption

Every null this archive holds for Rosario rests on a **typescript index** — a later compilation, made
from the registers, listing surname, forename, year and folio. It is a fine instrument and it has been
read exhaustively: the whole L section, the whole Ll section, every year from 1879 to 1901.

But an index is somebody's transcription. **Whether the typist missed anything has never been tested.**
That was said plainly when the L sweep was closed, and it was the reason to come back.

## The test

**Libro 24 of the Rosario cathedral baptisms, read act by act** — not the index, the register.

FamilySearch film **004098792**, waypoint *Bautismos 1881-1882*. Each opening carries about eight acts,
and **every act has the child's name written in the margin**. At level 12 and 42% scale a whole opening
fits one screen with every margin legible, so the margins were read for **all 183 acts in the span**.

> **From 1 February to 15 March 1882 — acts 113 to 295, pages 390 to 435 — there is no Lerena.**

Pablo Armando was born on **22 February 1882**. The span covers **three weeks before his birth and three
weeks after it**, act by act, with nothing skipped. Recorded frame by frame in
`data/rosario-1882-register-actbyact.tsv`, including where the sweep stops so it can be resumed exactly.

## What the register gave up along the way

**Rosario cathedral baptised 112 children in January 1882 and 122 in February** — about four a day, in a
city of perhaps fifty thousand. That is the first time this archive has had a rate, and it is what makes
the sweep bounded rather than open-ended.

**A filming detail worth knowing.** Page 425 has a paper slip pasted over it — an annotation dated
**29 May 1905**, concerning a foundling at the Hospital de Caridad. On the film it hides four acts. The
next frame is **the same page refilmed with the slip lifted**, so nothing is lost. Whoever filmed this in
1974 was careful. There is also a plain duplicate exposure at image 225.

## What this settles

**The index is not hiding him — at least not here.** For six weeks around his birth, the register itself
says what the index says: no Lerena. The two agree.

That matters because it removes the most comfortable explanation. The archive could have gone on saying
*"perhaps the typist missed it."* For this span, the typist did not.

## What it does not settle, said plainly

**The span is six weeks, not a year.** Catholic infants in 1880s Argentina were usually baptised within
days or weeks, which is why the window was chosen — but families did wait, sometimes months, sometimes
years. **A baptism in April, or in 1883, or at seven years old, is not excluded by this.**

So the honest position is now narrower and sharper than before:

1. He was **not baptised at Rosario cathedral in the six weeks around his birth**. That is established
   from the register, not from an index.
2. The rest of 1882 and 1883 remain unread at act level, and the index says there is no Lerena in them.
3. Which leaves: baptised **elsewhere**, baptised **much later**, or **not baptised as an infant** at
   all — and he was certainly baptised at some point, because he married in a Catholic church after
   banns in 1911.

**The next stretch is a known quantity now**: about fifteen frames per month, eight acts a frame, margins
legible. Finishing 1882 is roughly a hundred and thirty more frames. That is a long afternoon, not a
mystery.

---

## Second pass — and a correction to how the first was done

**The first pass was not read at a high enough resolution, and it has been redone.**

The first sweep rendered whole openings at level 12, 42% scale. That is legible enough to *follow* the
page — but not to be certain of a name. The proof came at act 312, where *"Timoteo Lucero"* had been
read as *"Armando Sara"*. **Both words wrong, and an L-surname missed entirely** — which is precisely
the failure mode that matters when the whole exercise is looking for one L-surname.

So every opening was **re-read from the margin strips at level 13**, the film's maximum. The method:
render tile columns 0–3 and 9–12 — the two margin columns of the opening — side by side in a single
image. One screenshot per opening, every name unambiguous.

**The conclusion did not change. Many individual readings did**, and the corrected ones are now in
`data/rosario-1882-register-actbyact.tsv`. The earlier readings should not be quoted.

## Where it now stands

> **February and March 1882 are complete, act by act, at full resolution.**
> **Acts 113 to 373 — 261 baptisms — and no Lerena in any of them.**

He was born on **22 February 1882**. This is now the whole of the two months around his birth, not a
six-week window, and every margin has been read at a size where the name could not hide.

Also noted along the way: two **duplicate exposures** (images 225 and 239), the **pasted 1905 slip** on
page 425 and its refilmed frame, a marginal cross-reference at act 289 to folio 577, and two foundlings
named **Paul** — *Luis Paul Expósito* at act 369 and *Luis Paul* in the 1882 marriage index. The forename
was in Rosario; the surname was not.

**April begins at act 374.** The sweep stops at act 376, image 242, and the file records the ark so it
resumes without repeating a frame.

---

## The second pass — April to July 1882

*13 September 2026.* The sweep stopped in April. It has been carried to the end of the volume.

**Method, refined.** Every act carries the child's name in the **left margin** in large script. So instead
of rendering a whole opening, the two margin strips — tile columns **0–3** and **10–14** at level 13 —
are rendered **side by side in one image**. One screenshot per opening; every name legible; the eight
acts of an opening readable at a glance.

**Images 243 to 309**, which is the rest of the volume. Five of those frames are not new openings:
**257, 264 and 300** are duplicate exposures, and at **284/285** and **301/302** a loose certificate was
laid on the book when it was filmed, covering one page — each read from the facing frame. The volume
**ends at act 862**, on 22 July 1882.

> **Acts 377 to 862. No Lerena, in any spelling.**

Added to the first pass, the register of Rosario cathedral has now been read **act by act from act 113
(1 February) to act 862 (22 July 1882)** — **seven hundred and fifty baptisms**, every margin read at
full resolution.

### Two near misses, logged and resolved

- **Armando Juan Rouillon**, act 546, born 26 April 1882. An *Armando*, baptised at Rosario in 1882 —
  but born two months after Pablo Armando, and a Rouillon.
- **Pablo Jacinto Gauna**, act 827, 11 July 1882. A *Pablo*, and the margin surname was ambiguous at
  reading size. It was re-rendered at full magnification **specifically in case it read LARENA**. It
  reads **Gauna**.

### What the exercise was for

Every Rosario null this archive holds rests on a **typescript index compiled in 1945** from these
registers. Whether that typescript is complete has never been tested — and an index is exactly the kind
of evidence this archive has been burned by before.

**It has now been tested across 750 consecutive acts, and the index and the register agree.** Where the
index says there is no Lerena, the register says the same. He is not there, and **the index is not the
reason he is not there**.

That is a negative, but it is a load-bearing one: it means the Rosario nulls can be trusted, and the
search belongs somewhere else.
