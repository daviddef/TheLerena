# Four things the Lerena archive owes the estate — 15 September 2026

Raised as work-list rows owned by *the kit & estate* rather than by this archive,
because they are not about the Lerenas. Each one cost this archive something to
learn.

---

## 1. FamilySearch images are addressable BY NUMBER, with no viewer and no `www`

The DeepZoom tile service accepts a plain identifier:

```
dgs:{film9}.{film9}_{image5}
```

so `dgs:008166578.008166578_02687` is film 8166578, image 2687 — **no ark, no
viewer, no catalogue lookup**. `{id}/manifest.json` converts an ark to that form
and back, which means every stored ark in an archive can be turned into something
re-openable.

**Why it matters more than convenience.** `www.familysearch.org` is regularly
behind an Imperva block (Error 15) that takes down `/search/` and `ark:` pages
together, for an hour at a time. **The tile host is not behind it.** This archive
found Sancho Llerena's 1791 marriage act while `www` was returning *Access
Denied*, and mapped three reels the same way.

Working code, with the traps documented: **`tools/fsimage.js`** in this
repository. The traps are worth repeating because each cost real time:

- never cache-bust a failed tile — re-request the *same* URL, or the mosaic
  silently scrambles;
- wait ~2.5s after `naturalWidth > 0` or tiles render white;
- **never batch the scroll/scale call and the screenshot** — the CSS transform
  has not repainted and you get the previous view.

Thumbnails (`thumb_p200.jpg`) are **public** — plain `curl` gets them, no
session. A contact sheet of them is the cheapest way to find filming target
boards, volume seams and blank leaves.

---

## 2. Assume your catalogue-derived film numbers are wrong until you open them

This archive held two Montevideo film attributions taken from a catalogue rather
than from a film. **Both failed inspection on the same day.**

- **DGS 7713373** was recorded as *"Bautismos, matrimonios y defunciones,
  1781-1814, del Regimiento de Infantería de Buenos Ayres"*. The film's own
  boards say *Uruguay, Archivo de la Curia* and *Montevideo, Archivos
  Parroquiales*. The regiment's book **is** on it — item 5, from image 623 — so
  the substance held and the label did not.
- **DGS 7713386** was recorded as *"Índices de bautismos, matrimonios y
  defunciones, 1726-1800"* and called *the cheapest test in the archive*. Images
  300 and 1500 are Montevideo cathedral **burial registers of 1887 and 1905**.
  The attribution is simply wrong.

An ark resolves to its true film in **one `manifest.json` call**. If two of two
failed here, other archives' unverified citations are worth a pass.

Related: a film can have **gaps**. This archive probed images 1, 500 and 1000 of
one reel, found nothing, and published that the film held nothing below image
1057. It has two blocks — 72–478 and 1057–3295 — and the first block is a parish
baptism register the archive had an ark into all along. **Three samples are not a
survey.**

---

## 3. `pdftotext -layout` will weld two strangers into one person

The South African *Government Gazette* sets **two columns**, and `pdftotext
-layout` interleaves them line by line. A grep for a surname on one page returned

> *"…who died on 26 June 1971"* … *"Bedfordview"*

and both belonged to the entry in the **left** column — a different estate, a
different man. It was caught only because two gazettes gave two different death
dates for one estate number, and the discrepancy was the warning.

**Print context, never grep matches.** `grep -n -B2 -A5` and then follow a single
column down. Any archive in this estate using the gazette pipeline will hit this.

The pipeline itself: the site is behind Cloudflare, but the PDFs are open at
`archive.gazettes.africa/archive/za/<year>/<slug>.pdf` — fetch, `pdftotext
-layout`, read. The slug is predictable from the issue: e.g.
`za-government-gazette-legal-notices-a-dated-1996-03-15-no-17029.pdf`.

---

## 4. A `death_year` column harvested from an index may not be one

This archive's `sa-deceased-estates.tsv` was built from **ancestors.co.za** and
its `death_year` column turned out to hold **the year the estate was
advertised** — for all eleven rows.

- Ricardo Juan Carlos Lerena **died 21 December 1994** and was filed under
  **1996**.
- Anton Armando Lerena **died 3 April 2003** and was filed under **2013**.

It is invisible until you fetch the gazette the row points at, and it caused this
archive to believe, for several hours, that two records described two different
men. **Any sibling archive that harvested the same index has the same bug.**
Renamed here to `gazette_year`, with true dates recorded separately.

---

*Raised by the Lerena archive. Nothing here is Lerena-specific; all four came out
of one day's work and all four are estate-wide.*
