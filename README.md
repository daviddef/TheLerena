# The Lerena Archive

An evidence-first family archive for the **Lerena** family — by family account of **Rosario** on the
Paraná, then **South Africa**, then **Brisbane**.

> *Lerena* is borne by about **2,124 people in the whole world**. That single fact shapes the method. Where
> the sibling *Falco* archive must prove that any two Falcos are related, this archive may reasonably
> propose that any two Lerenas are — and must still prove it.

## Where this one starts

**Almost nowhere, and it says so.** The Falco and Defranceski archives were built on registers already
read. This is day one. Nearly everything specific to the family is presently **testimony**; what is
**documented** is context — the shape of the surname, the town of Llerena, the Argentine Stud Book, the
Oudtshoorn feather boom.

## What the family remembers

Recorded from David Defranceski, 8 September 2026:

- **Cheryl Anne Lerena** married **Ivan Defranceski**; their son was born at Johannesburg and the family
  later moved to Brisbane.
- Cheryl's **grandfather came from Argentina** — **Rosario**.
- He was **Consul General** between Argentina and South Africa.
- He **brought horse breeding and racing to South Africa from Argentina**.
- He kept an **ostrich farm**.

## What the baseline already shows

- **The name is rare** — 2,124 worldwide, 197,177th commonest, 1 in 3.43 million.
- **The River Plate is its heartland.** Spain has the largest total (888), but **Uruguay has the world's
  highest density** (1:7,962, ~6.6x Spain's) and Argentina 293. The Rosario tradition points where the name
  actually concentrates.
- **South Africa holds ~3% of every Lerena alive** — 61 people, in a country with no Spanish colonial past.
  That has the signature of one family arriving and multiplying, which is what the testimony describes.
- **The horse thread is real on both continents.** **Gilberto Justiniano Lerena Lenguas** co-founded the
  **Argentine Stud Book**, bred Quadruple Crown winner *Old Man*, and has a **Group 1 at Palermo** named for
  him since 1914. In South Africa, **Gavin Lerena** is a leading jockey. *No relationship is claimed.*
- **The name may be two names.** Basque `-ena`, "the house of" — or a reduction of **Llerena** in Badajoz,
  whose own surname has 36,828 bearers. Unresolved, and closed only in the registers.
- **The tree already reaches an Afrikaner family**: the MyHeritage tree is titled *Defranceski, Lerena,
  Taylor, Barry, Blazevic, **Booyzen***.

## The blocking question

**Generation 1 has no name.** The consular lists, the stud books and the Argentine registers are all
unsearchable without it. See `notes/QUEUE.md` § 0.

## Method

| | |
|---|---|
| **Documented** | A named source with a reference, and where possible the scan. |
| **Inferred** | A reasoned conclusion from documented facts, with the reasoning written out so it can be overturned. |
| **Superseded** | Asserted in the family record, and now displaced by a document that says otherwise. |
| **Disputed** | Asserted in the family record but unsupported, or contradicted, by what can be seen. |
| **Family lore** | Told, remembered, not corroborated. Kept because it is precious; labelled because pretending otherwise is how family myths become family history. |

**Living people are omitted from the build entirely** — not hidden, not gated, not present in the output.
Because this line reaches the present within three generations, that removes a large part of the story from
public view. A removal request is honoured within days, without argument and without requiring a reason.

## Running it

```bash
cd site
npm install
npm run dev      # http://localhost:4323
npm run build    # static output in site/dist
```

Deploys to GitHub Pages on every push to `main`.

## Layout

```
data/                  direct-line.tsv, surname-distribution.tsv
notes/                 baseline-surname.md, findings.md, QUEUE.md
site/src/pages/        the archive itself
sources/ photos/       scans and images as they are gathered
requests/              drafted archive and record requests
```

## Sibling archives

**The Defranceski** (Istria) and **The Falco** (Arienzo, Campania) — same method, same author. Cheryl Anne
Lerena's marriage to Ivan Defranceski is the hinge between this archive and the Defranceski one.

## Sources

Forebears · Wikipedia (*Gran Premio Gilberto Lerena*; *Llerena, Badajoz*; *Basque surnames*; *Basque
Uruguayans*) · Sporting Post · the Defranceski archive · family testimony.

Identified and not yet worked: NAAIRS · SA Government Gazette · South African and Argentine Stud Books ·
Boletín Oficial · Santa Fe civil registration · Rosario parish registers · CEMLA · INE · the C.P. Nel
Museum, Oudtshoorn.
