# Method — the Rosario registers can be read as TEXT, in the in-app browser

## The correction first
This archive recorded, twice, that settling the 1884 marriage candidate needed the **Chrome extension**,
because the in-app browser "cannot crop to a region" and a nineteenth-century hand cannot be read at
full-page scale. **David pushed back on that, and he was right.** The premise was wrong in two ways:

1. The **viewer has its own zoom controls**, so magnification never depended on the screenshot tool's
   ability to crop.
2. **More importantly, the handwriting does not need to be read at all.**

## The finding
Every image in the Rosario church-record films carries an **"Image Index" panel beneath the viewer**, and
that panel is **HTML text, not an image**. It can be pulled straight out with JavaScript.

For the marriage registers it gives, for **every act on the page**:

> **Name · Sex · Age · Birth Year (estimated) · Father's Name · Mother's Name ·
> Spouse's Name · Spouse's Sex · Spouse's Age · Spouse's Birth Year ·
> Spouse's Father's Name · Spouse's Mother's Name · Event Type · Event Date · Event Place**

**Both sets of parents, for both parties, typed out.** That is the entire genealogical content of a
marriage act, without reading a word of the hand.

### How to pull it
Get into **single-image** mode — navigating by URL lands in the thumbnail grid, so click a thumbnail — then:

```js
document.querySelector('table').innerText
```

Stepping between images with the viewer's **left/right arrows** is reliable; typing into the image-number
box and navigating by `?i=` URL both tend to bounce back to the grid.

## Why this matters well beyond one folio
**It turns the Rosario marriage registers from handwriting into a database.** Any future question of the
form *"who were X's parents?"* can be answered by paging the index panel rather than transcribing. It
applies to the whole series — and had it been understood earlier it would have saved a great deal of the
baptism sweep.

## Proved on
Images around **8 June – 8 July 1884**, Catedral de Nuestra Señora del Rosario — about fifteen marriages
captured in full, with all four parents each. Sample:

| Groom | Age | His parents | Bride | Age | Her parents | Date |
|---|---|---|---|---|---|---|
| Mariano Salas | 28 | Mariano Salas Castro · Escolástica Castro | Joaquina Rosas | 27 | Pascual Rosas · Eusebia Rodríguez | 8 Jun 1884 |
| Andres Jeklin | 36 | Cristian Jeklin · Elisa Bueti | Mauricia Ferreyra | 20 | Damian Ferreyra · Florentina Rosales | 30 Jun 1884 |
| Antonio Miguel Damiani | 36 | Antonio Damiani · Teresa Basadone | Geronima Balleto | 21 | Juan B Balleto · Magdalena Basadone | 30 Jun 1884 |
| José d'Emmanuele | 30 | Pascual d'Emmanuele · Catalina Parodi | Elena Perez | 15 | Onofre Perez · Micaela Molina | 3 Jul 1884 |
| Isidoro Ledesma | 29 | Nicolas Ledesma · Andrea De Ledesma | Paula Centeno | 16 | Eugenio Centeno · Juana Vivas | 4 Jul 1884 |
| Roman Arregui | 23 | Rosa Arregui · Josefa Casas | Cecilia Sanchez | 21 | Pablo Sanchez · Facunda Rios | 5 Jul 1884 |
| Julio Zeballos | 26 | José Zeballos · Dorotea Arroyos | Niceda Gatica | 23 | Nieves Gatica · Simona Moyano | 1 Jul 1884 |
| Juan Antonio Gonzalez | 34 | Hermenegildo Gonzalez · Maria Garcia Cabuano | Isabel Irribarria | 16 | Vicente Irribarria · Eufemia Ramirez | 5 Jul 1884 |
| Luis Aressi | 22 | Pedro Aressi · Clara Borge | Angela Giglioni | 19 | Nicolas Giglioni · Catalina Pinosa | 5 Jul 1884 |
| Jorge Regino Piñero | 27 | Lino Piñero · Manuela Soza | Manuela Dominguez | 19 | Hilario Dominguez · Rosario Piñero | 5 Jul 1884 |
| Alejo Mosqueira | 30 | Benito Mosqueira · Marta Lavallen | Angela Paroni | 17 | Andres Paroni · Eusebia Goya | 7 Jul 1884 |
| Juan Maria Casanova | 28 | Pedro Casanova · Josefina Majeaureau | Vicenta Leinate | 18 | José Leinate · Catalina Rosoe | 8 Jul 1884 |
| Protasio Martinez | | | Gabriela Plaza | | | 30 Jun 1884 |
| Bautista Gomez | | | Jacinta Andrada | | | 30 Jun 1884 |
| Guillermo Erasquin | | | Luisa Ricardo | | | 1 Jul 1884 |

**No Sarmiento, and no L-surname of interest, in that stretch.**

## What still stands open
**The candidate at Libro 9 folio 20 has not been reached.** The viewer's grid/single-mode switching keeps
resetting position, and the Image Index panel materialises on some loads and not others. That is a
mechanical obstacle, not a research one — **the method is proven and the target is small.** Roughly twenty
images cover the whole of 1884; each yields six marriages as text. Anyone resuming should step with the
arrows from a known single-mode image rather than navigating by number.

---

# *** FOLIO 20 SETTLED — the candidate is Vicente LAVENA, and it is not ours ***

Reached **9 September 2026**, using the method above: single-image mode entered by clicking a thumbnail,
then stepped forward with the viewer's arrows, extracting the Image Index panel as text at each image and
scanning it for *Sarmiento · Larena · Lavena · Lerena · Llerena*.

**Scanned act by act: 8 June – 29 September 1884**, Catedral de Nuestra Señora del Rosario — roughly ninety
marriages. **Exactly one hit in the whole stretch:**

> **Vicente LAVENA**, male, **26**, b. 1858 — father **Miguel Lavena**, mother **Lucía Lavena**
> **× Angela BELMONTE**, **21**, b. 1863 — father **Pascual Belmonte**, mother **María Cozsi**
> **Marriage, 3 August 1884**, Catedral de Nuestra Señora del Rosario, Rosario, Santa Fe.

## Why this is certainly the index entry
The index line recorded from the alphabetical volume was ***"Larena/Lavena V · Sarmiento A · 20"***, with a
note that the surname could not be told apart at that resolution.

- The first surname is **LAVENA** — confirmed from the register itself.
- **"V" is Vicente.** ✓
- **"A" is Angela.** ✓
- Both initials match, in order, and it is the **only** L-surname marriage in three and a half months of
  the register.

***The "Sarmiento" was my own misreading of BELMONTE*** in the low-resolution index image. That error is
recorded here rather than quietly dropped, because it is the reason this candidate survived as long as it
did.

## What this closes
**The last open candidate for a Lerena marriage at Rosario is eliminated.** Vicente Lavena was an Italian —
son of Miguel and Lucía Lavena — which fits everything else known about the Lavenas of Rosario: an Italian
family present from about 1880, with children baptised at San José and the Cathedral through to 1915.

**There is no Lerena marriage at Rosario cathedral in 1884.**

## *** THE WHOLE OF LIBRO 9's 1884 IS NOW READ ***
The residual has been closed. **8 June to 31 December 1884** — the entire year as this book holds it — has
been read **act by act** through the index panel, running on into **2 January 1885** to be sure of the
boundary.

**Libro 9 begins in June 1884.** Image 3 of the film is a title card reading *1884–1888*, image 4 is
*PRINCIPIO*, the register starts at image 5, and **the earliest dated act anywhere in the book is 8 June
1884**. January to May 1884 is therefore **not in this book at all** — it belongs to **Libro 8**, a
different film. Since the index entry was explicitly *"Libro 9º"*, the relevant year is covered end to end.

### The result for the whole year
**One** marriage in Libro 9's 1884 involves any of the surnames *Sarmiento · Larena · Lavena · Lerena ·
Llerena*:

> **Vicente LAVENA × Angela BELMONTE, 3 August 1884.**

**No Sarmiento anywhere in the year. No Lerena anywhere in the year.**

Month by month, all clear: June · July · August (the Lavena act) · September · October · November ·
December. Roughly **two hundred marriages** read, each with both parties and all four parents.

---

# Libro 8 (Matrimonios 1868–1884) — answered by index, not by paging

**Libro 8 is a different film**: *Matrimonios 1868–1884*, film 1091470, **DGS 4531040**. Sixteen years,
some three thousand marriages, five hundred-odd images. Paging it act by act was not sensible when a
cheaper test existed.

## The control first
Before trusting a null from the search index, it has to be shown that the index actually **covers** those
years. It does. A control search for a common surname at the cathedral, 1870–1880, returns marriages with
full parentage:

> *Ramon Gonzalez × Cristina Castro, 18 Aug 1874* — parents Pablo Gonzalez & Laureana Crinejo
> *Zenona Gonzalez × Vicente Galvan, 11 Oct 1875* — mother Lucia Gonzalez
> *Nemecio Gonzalez × Clorinda Puccio, 1 Jan 1876* — parents Severo Gonzalez & Rosario Gutierrez
> *Silvano Gonzalez × Rufina Santander, 2 Oct 1876* — parents Juan José Gonzalez & Juana Villareal

**The 1868–1884 Rosario marriages are indexed and searchable.** The null that follows is therefore a null
about the record, not about the coverage.

## The result
Searching **LERENA at Rosario** within *Argentina, Santa Fe, Catholic Church Records* returns **38
records** — and **not one is a marriage before 1900**. Every hit is twentieth century, and most are
*Llorens* fuzzy matches.

***There is no Lerena marriage at Rosario cathedral in Libro 8 (1868–1884).*** Taken with the act-by-act
read of Libro 9's 1884, **there is no Lerena marriage at Rosario across the whole period 1868–1891.**

### The honest difference in standard
Libro 9's 1884 was read **act by act**. Libro 8 rests on the **index**. The index is demonstrably good —
the control proves it — but indexes carry gaps and mis-spellings in a way a page-by-page read does not.
**Strong, but not the same standard**, and recorded as such.

## What it did turn up: the first Lerenas actually in Rosario
Until now this archive had found **no Lerena living in Rosario at all**. The search produces two, both at
**Santa Rosa de Lima** — the parish that opened in **1888**, after Pablo Armando was born:

- **Luis LLERENA** m. **Clementina Baranda** → *Luis Alejandro Llerena*, baptised **1903**
- **Manuela LERENA** m. **Diego Román** → *Carmen Román Lerena*, baptised **1918**

Neither can be his parents — both are a generation too late — but they are the first evidence that the
surname existed in the city at all, and they belong on the register.
