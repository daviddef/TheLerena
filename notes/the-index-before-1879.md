# The index before 1879

*13 September 2026. Opened in the morning, half-read by lunchtime, and finished the same day — eighty
openings, a hundred and forty-eight years, and one name.*

## What it is

**FamilySearch film 004530324, 554 images.** The title card at image 5 reads:

> **Parroquia N. S. del Rosario — ÍNDICE DE BAUTISMOS — VOLUMEN 3º**
> **Años 1731–1879 — LETRAS L–Q**
> *Revisado y Restaurado en 1945*

It is the **only index covering Rosario baptisms before 1879** — the companion to the 1879–1900 volume
this archive read end to end on 10 September. And like that one it is **typewritten**, the product of the
same 1945 restoration, with the same four columns: *Apellidos · Nombres · Año · Folio*.

## Why it was the right film

Everything this archive had read started in 1879. That is three years before Pablo Armando was born,
which is fine for him and useless for everyone above him. This volume is where **Juan Carlos Lerena's
own baptism** would be if he was born at Rosario; where **an older brother or sister** of Pablo Armando
would be if the family were in the city in the 1870s; and where **any Lerena at all** would be, across
a hundred and forty-eight years of one parish.

## What was read

**The L section runs from image 6 to image 85.** Image 86 begins the M section — *Libro 1º, 1751*,
Mosqueda and Montenegro and Muñoz. Every opening from 6 to 85 has now been opened and read in full at
tile level 12, a whole opening to a screen, with anything ambiguous re-rendered at level 13.

Eight of those frames are not index at all: **images 35–42** are the roll break — a target card, two
blanks, *"CONTINÚA EN EL PRÓXIMO ROLLO"*, *"ARGN-0030 ROLLO 28"*, *"ROLLO 29"*, *"CONTINUACIÓN"*. Nothing
is lost across the join; image 43 simply re-shoots image 34. Two further frames, **63 and 83**, are
duplicate exposures of the openings before them.

That leaves **seventy openings of actual index**, continuous from 1731 to 1879, and they are recorded
one by one — image, ark, years, libro, result — in `data/rosario-index-pre1879.tsv`.

## What was found

> ### LERENA LENGUAS, María Julia Margarita Josefa E.J.
> ### 1866 · Libro 15 · folio 229

One name. Image 58, ark `9Q97-Y3S2-FPP`, on the right-hand page, low down. And a line above it, the
same child again under **LENGUAS** — *María Julia Margarita Josefa E.J.L.*, same year, same folio. The
1945 typist cross-indexed her under both halves of her name, which is how we can be sure the compound
is real and not a slip: **a Lerena father and a Lenguas mother.**

It was confirmed at full resolution before it was believed — the lesson of the Armando Lorena card,
which this archive got wrong once by reading an index instead of an image.

## What that means, stated carefully

This is **not** Pablo Armando's sister. She is sixteen years too early, and her surname is compound
where his is not.

What she is, is **the only Lerena baptised in the parish of Rosario between 1731 and 1901.** Both
volumes of the index have now been read end to end — this one and the 1879–1901 one — and she is the
sole occurrence in a hundred and seventy years.

Which sharpens the central problem rather than solving it. Pablo Armando was born at Rosario on
22 February 1882 and **his baptism is not in the index.** That was already known from the 1879–1901
volume; what is new is that the family leaves no trace in the parish before then either. Whatever
brought Juan Carlos Lerena and María to Rosario, they were not a Rosario family.

But a 1866 baptism at folio 229 has an **act**, and the act names both parents. That act has not been
read. If María Julia's father turns out to be a Juan Carlos, or the father of a Juan Carlos, the
question moves back a generation in a single page. It is now the first errand on the list.

## The names that are there instead

For a century and a half the L column of this parish is **Leguizamón, Lencina, López, Ledesma, Lescano,
Ludueña, Lucero, Leiva, Luna, León, Luján, Llanos** — over and over, hundreds of times each. Five
near-misses were checked at level 13 and recorded so that nobody has to check them twice:

- **Lerones**, Hortensia (1856) — Ler-, but Lerones.
- **"Lesa (o Lera)"** (1857) — where the index itself offers *Lera* as an alternative reading.
- **Loveras**, Juana Josefa Valeria (1864) — Lov-, not Ler-.
- **Lerré Echeita**, Marián (1870) — a Basque compound, not Lerena.
- **Lensina**, María del Rosario (1816) — read at first glance as *Leprina*; it is Lensina.

## One method note worth keeping

The tile-retry loop must re-request **the same URL**. Appending a cache-busting query returns a
*different tile* and silently scrambles the mosaic — it produced one unreadable, misaligned page before
it was caught. Fixed by dropping the query and re-setting the original src.

And a plainer one: reading eighty openings in an afternoon got this archive rate-limited by FamilySearch
twice in four days. Both blocks were mine, not theirs.
