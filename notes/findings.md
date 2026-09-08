# Lerena — findings

Started 2026-09-08. **Day one.** Almost everything here is testimony or context, not documentation.

## Family testimony (David Defranceski, 8 Sep 2026)
- **Cheryl Anne Lerena** married **Ivan Defranceski**.
- Cheryl's **grandfather came from Argentina**; **Rosario** is the city named.
- He was **Consul General** between Argentina and South Africa.
- He **brought horse breeding/racing to South Africa from Argentina**.
- He had an **ostrich farm**.
- David notes there is **very little known** about the Lerena family.

Status: all **LORE**. No name, no dates, no document for any of it.

## Established from the Defranceski archive (documented)
- MyHeritage tree title: **"My Family Tree (Defranceski, Lerena, Taylor, Barry, Blazevic, Booyzen)"**.
  - **Booyzen** is Afrikaans → the Lerena line **married into an Afrikaner family** → settlement, not a posting.
  - **Taylor**, **Barry** — English-language, Cape/Rand. *Barry* were a 19th-c. Overberg merchant house,
    same world as the Karoo ostrich trade. **Suggestive only; common surname; no link established.**
- Family map export: **Johannesburg** = "David is born, Ivan Moves, Hedviga dies"; then
  **"David Ivan and Cheryl Move to Brisbane"**. So the Lerena line reaches Australia **via Johannesburg**.

## Context leads (documented, but about the NAME not yet the FAMILY)

### Gilberto Justiniano Lerena Lenguas — the big one
- **Co-founder of the Argentine Stud Book.** Bred **Old Man**, Argentine Quadruple Crown winner.
- Studs: Stud Oriental, Stud Bend Or, Haras La Guardia, Haras El Moro, Haras Las Ortigas, and his own
  **Haras El Viejo**.
- **Gran Premio Gilberto Lerena** — Group 1, Hipódromo Argentino de Palermo, 2,200m turf, fillies & mares
  3yo+. Founded 1905 as Premio Abril; **renamed in his honour 1914**.
- Two inferences worth carrying:
  - **"Lerena Lenguas"** is a River Plate double surname; *Lenguas* is Uruguayan. Matches Uruguay's density
    and *Stud Oriental* (oriental = Uruguayan).
  - **The 1914 renaming** is the kind of honour paid at or just after a death → brackets his life.
- **NO relationship claimed.** Rarity makes it likely; only a document makes it true.

### Gavin Lerena
Leading South African jockey, Turffontein and the major meetings. Living person — noted only as a public
figure. Confirms **surname + turf are linked in South Africa as well as Argentina**, which is what the
testimony predicts.

## Analysis: the claims, assessed

**"Brought horse racing to South Africa"** — cannot stand literally; organised Cape racing predates any
plausible date. Family accounts compress. Testable forms:
1. He **imported Argentine bloodstock** (→ stud book import registers, with country of origin).
2. He brought **Argentine breeding practice** / founded or managed a stud.
3. He was **prominent enough** in SA racing to be remembered as having started it.

**"Ostrich farm"** — more precise than it sounds. SA ostrich farming centred on **Oudtshoorn / Little
Karoo**; the **feather boom ran ~1880s–1914** and collapsed with fashion and the war. So the claim carries
a district and a date: likely **Cape, likely pre-1914**.

**TENSION worth holding:** Oudtshoorn is far from any capital. Either two periods of one life, two
different men, or — most economically — **the consulship was HONORARY**. A resident merchant holding an
honorary post would appear in host-state gazettes but *not* in Argentine career foreign-service lists, and
would reconcile a diplomat who bred horses and farmed ostriches. **Hypothesis, recorded early so it can be
tested.**

## The blocking problem
**Generation 1 has no name.** Consular lists, stud books and Argentine registers are all unsearchable
without it. Everything else is downstream.

---

# 8 September 2026 — NAAIRS: the first real names

Searched NAAIRS (SA National Archives index), database **RSA** (all repositories), for `LERENA`.
**13 documents; 12 genuine.** Tool: `tools/naairs.py`. Raw HTML: `sources/naairs/`. Table: `data/naairs-lerena.tsv`.

## The Cape cluster — ROBERT PAUL LERENA
| Date | Ref | What |
|---|---|---|
| 1931 | KAB 3/CT 4/2/1/3/474 B796 | **PLANS OF PROPOSED STABLES, Koeberg Road, RUGBY. RP Lerena.** |
| 1932 | KAB 3/CT 4/2/1/3/515 B352 | Unauthorised wood and iron structure, Madeira Rd, Rugby |
| 1947-48 | KAB 3/CT 4/2/1/3/1674 B3099 | House + garage, Lot 1202, Hove Rd, **Camps Bay** |
| 1948-50 | KAB 3/CT 4/2/1/3/1793 B2892 | Additions, Madeira St, Rugby |
| 1950 | **KAB MOOC 6/9/17017 ref 1847/50** | **ESTATE PAPERS — he died 1950** |

**THE STABLES (1931) are the first hard corroboration of the horse tradition.** A municipal building file,
not a memory. Rugby is beside **Milnerton** (racecourse). Whether they were *racing* stables is untested —
the building file itself should say.

**MOOC 6/9/17017 is now the single highest-value document in the project.** A Cape estate file of this
period contains the **death notice**, which names parents, birthplace, spouse and children. *If he was born
in Argentina, that is where it will say so.*

## The Transvaal cluster — the Johannesburg generation
| Date | Ref | Who |
|---|---|---|
| 1971 | TAB MHG 6746/71 | **NUNO FERNANDO LERENA** d. — widow **Catherine Mary Sophia** |
| 1973 | TAB MHG 1518/73 | **ROGUE [=ROQUE] LUIS ARMANDO LERENA** d. — widow **Rheena May**; predeceased spouse **Rosina Wilhelmina** |
| 1977 | TAB WLD 8043/77 | Anton Lerena, payment case |
| 1979 | TAB TPD 1248/1979, M680/1979, 2769/1979 | Divorce: **RICARDO PAUL LERENA** v **Anne Margaret (born CORBETT)** |
| 1980 | TAB TPD 1367/1980 | Divorce: **Glynnis Margaret (born BOLTON)** v **ANTON ARMANDO LERENA** |

Record shifts Cape -> Transvaal between **1950** and **1971**: the family moving to the Rand, which is
where David was later born.

## THE GIVEN NAMES ARE THE FINDING
**Nuno Fernando · Roque Luis Armando · Ricardo Paul · Anton Armando.**
Iberian/Latin-American given names, borne by men in South Africa marrying Corbetts and Boltons. *Nuno* is
distinctly **Portuguese**; Roque/Luis/Armando/Ricardo Spanish or Portuguese.

A family still naming sons this way two or three generations after arrival **knows where it came from**.
This is independent support for the River Plate origin — reached from a government index, not from the
family's own account.

Recurring names across clusters: **Paul** (Robert Paul, Cape / Ricardo Paul, Transvaal); **Armando**
(Roque Luis Armando, Anton Armando). Ordinary evidence of descent. Suggestive, **not proof**; no link drawn
that a document has not drawn.

## Useful negatives
- **LLERENA = 0 documents.** SA family spells it with one L, consistently, 1931-1980, both provinces.
  Does not settle the Basque/Extremaduran fork (any reduction predates SA) but there is no variant to chase.
- **GENE (SA Genealogical Society gravestones) = 0.** No indexed Lerena gravestones.
- Doc 6 (KAB HAEC 77/1921, East London marriage) is a **FALSE POSITIVE** — "Lerena Catherine Buys" is a
  given name. Excluded.

## Still unproven
Nothing here is yet tied to **Cheryl Anne Lerena**. Six names and two estate files are now orderable; the
link to David's own line is not made.

---

# 8 September 2026 (later) — THE PASSPORT. Generation 1 is named.

## PABLO ARMANDO LERENA
**Argentine passport, Série A No. 07962, no. 2/1940**, issued by the *Oficina Consular Argentina en Cape
Town, Unión de Sud Africa*, **24 December 1940**. In the family's own papers. Scans:
`sources/pablo-armando-lerena/`. Full transcription: `data/pablo-armando-passport.tsv`.

- **Born Rosario de Santa Fe, República Argentina, 22 February 1882** *** ROSARIO CONFIRMED ***
- Nationality **Argentina — nativo** (native-born, NOT naturalised)
- Domiciled **Rugby, Cape Town**
- **Profesión: TRAINER** *** THE HORSE CLAIM, DOCUMENTED ***
- Military: **Guardia Nacional, 6º de Caballería** (6th Cavalry), 1915 — a horseman in Argentina first
- **Viudo** (widower) by Dec 1940
- Travelling to **Portuguese East Africa** (Mozambique)
- 1m80, blue eyes, grey hair, straight nose, **scar on the forehead**
- Signed **A. B. Bayne, Encargado, Consulado General Argentino**; photo, thumbprint, 16.50-peso stamp

### Three claims tested
1. **Rosario / Argentina — CONFIRMED.** Family tradition was exactly right.
2. **Horses — CONFIRMED.** "Trainer" in his own passport, plus 6th Cavalry in Argentina.
3. **Consul General — DISPUTED.** He is the *bearer*, not the issuer. The consular signature is
   **A.B. Bayne**. Does not disprove an honorary post at another date (the hypothesis this archive recorded
   *before* the document surfaced), but the claim is demoted until something supports it.

### Rugby ties the passport to NAAIRS
Passport domicile **Rugby, Cape Town** = the suburb in NAAIRS KAB 3/CT B796 (1931), *"plans of proposed
**STABLES**, Koeberg Road, **Rugby**. RP Lerena."* Two independent archives, found on different days.

### OPEN: is Pablo Armando the same man as "Robert Paul Lerena"?
- NAAIRS: **LERENA, ROBERT PAUL**, estate 1950, KAB MOOC 6/9/17017; "RP Lerena" at Rugby 1931-1950 and
  Camps Bay 1947-48. Pablo Armando b.1882 would be **68 in 1950**.
- FOR one man: **Pablo = Paul**; same suburb; David's own filing puts the passport in a folder named
  "Roberto Paul Lerena Documents".
- AGAINST: **Robert ≠ Armando**.
- **DECIDED BY MOOC 6/9/17017** — a Cape death notice names parents and birthplace. If it says Rosario,
  one man.

## Generation 2 CONFIRMED, and the MyHeritage link closed
**Nuno Fernando Lerena, b. 6 Oct 1924, d. 1 Jul 1971**, m. **Catherine Mary Sophia BOOYZEN,
b. 25 Mar 1929, d. 25 Dec 2013**.

This is an **exact match** to NAAIRS TAB MHG 6746/71: *"LERENA, NUNO FERNANDO … SURVIVING SPOUSE CATHERINE
MARY SOPHIA LERENA."* The estate file and the tree independently confirm each other, and **Booyzen** is the
Afrikaans surname predicted from the MyHeritage tree title before either was read.

Children (gen 3): Jeanette Marie 1949-2021 · Paul Raymond 1951-2000 · Catherine Tersia 1952-1999 ·
**Cheryl Anne 1955 (living, omitted)** · Patricia Carmen 1958-2023.

**Note "Paul Raymond"** — Paul recurs from gen 1. And **"Carmen"** survives as a given name into 1958.

**NOT YET PROVEN: that Nuno Fernando is Pablo Armando's son.** It is the obvious reading (Pablo was 42 in
1924, and the Iberian naming persists) but no document yet links them. Nuno's birth or death record, or
Pablo's estate, closes it.

## Other family documents seen but not yet read
`Lerena 2.pdf` · estate covers `NUNO+FERNANDO_LERENA_(1971)_0.jpg`, `ROGUE+LUIS+ARMANDO_LERENA_(1973)_0.jpg` ·
`Photos/Rosaline Wilhelmina Forbes Lerena.jpg` (**FORBES** = maiden name of the "Rosina Wilhelmina" in
NAAIRS MHG 1518/73) · `Photos/Mary Septima Burial.jpg` · nine FamilySearch `record-image_*.jpg` in
"Roberto Paul Lerena Documents".

---

# 8 September 2026 (later still) — THE FAMILY PAPERS. The line is closed.

Worked through `Documents/Genealogy & Family History/Lerena`. Everything below is documented.

## GENERATION 1: ROBERTO PAUL LERENA (also Robert Paul; "LERINA" on the death certificate)
**Union of SA death certificate A 214036**, district Wynberg, entry W612/50:
- **76 years** (so b. c.1874) · **birthplace SOUTH AMERICA** · **Widower** · **RACE HORSE OWNER**
- d. **19 March 1950**, 7 Forth Road, Newlands · coronary thrombosis, angina pectoris · Dr J. R. E. Lee
- buried **Maitland Cemetery no 1**

**Wife: MARY SEPTIMA LERENA.** Maitland Road Cemetery interment register p.3215 entry 163, **Nov 1935**,
aged **51** (b. c.1884), of 34 Florence Rd, **Observatory**. Roman Catholic, Cemetery 1, **grave 7719A**,
Father Graham, undertaker L. Pitt. Certified by **J. R. E. Lee — the same doctor as her husband 15 years
later.** Family chart gives her as **Mary Taylor, b. England?** — the source of "Taylor" in the tree title.

## THE DOCUMENT THAT NAMES GEN 1
**Death notice of ROQUE LUIS ARMANDO LERENA** (typed "ROGUE"), estate 1518/73:
- b. **6 Dec 1905, CAPE TOWN**; d. 29 Jan 1973 Johannesburg; ID 331 402089; **retired railwayman**,
  20 Park Lane, Florida, Transvaal
- m.1 **Rosina Wilhelmina** (predeceased) → daughters **Juanita Ramond Hutson (born Lerena)** and
  **Panola Maria Lerena**; m.2 **Rhena May**
- **Q19 PARENTS: Father ROBERTO LERENA · Mother MARY SEPTIMA LERENA** *** THIS IS THE KEYSTONE ***

So the family was at the Cape by **1905**.

## THE 1950 ESTATE — Letters of Administration 1847/50 (= NAAIRS KAB MOOC 6/9/17017)
David already holds this file. Will dated **6 Feb 1942**. Gross **£15,527 15s**; distributable
**£14,450 3s 7d** in four shares of £3,612 5s 11d.
- **LOUIS LERENA, major son** — half a share (= Roque Luis Armando)
- **ROSE LILIAN THEYS, "no relation"** — half a share; spinster, **same address (7 Forth Rd)**, and
  **Executrix Testamentary**
- Residue £10,837 17s 8d on trust for **NUNO FERNANDO LERENA** and **RICHARDO JUAN CARLOS LERENA**,
  major sons, capital payable when **Nuno attains 30 (6 Oct 1954)**
- Succession duty addendum gives exact births: **Ricardo Juan Carlos 6 Jan 1920**, **Nuno Fernando 6 Oct 1924**
- Assets incl. 300 United Fish Canners Ordinary + 300 "A"; SA Permanent Mutual B&I Society deposit
- **Claim paid: W. C. Blake, "claim for CARROTS", £26.** Advertised in Government Gazette and Cape Argus.

## GENERATION 2 CONFIRMED — Nuno Fernando's own death notice (estate 6746/71)
b. **6.10.1924 CAPE TOWN**, d. 1.7.1971 **Germiston**; ID 331 406051W; **Salesman**, 24 Leiden Rd,
Gerdview, Germiston. Married at **Johannesburg**; spouse **Catherine Mary Sophia Lerena**.
Children: **Jeannette Marie Riekstins (born Lerena)**, Paul Raymond, Catherine Tertia, **Cheryl Ann**,
Patricia Carmen. Parents: recorded only as "Deceased" — **names not given** (frustrating).

**THE LINE IS NOW CONTINUOUS AND DOCUMENTED: Roberto Paul → Nuno Fernando → Cheryl Anne.**

## The family descendant chart (`Lerena 2.pdf`)
Root **Roberto Paul Lerena (b. Argentina?) m. Taylor Mary (b. England?)**. Three sons: **Luis**, **Ricardo**,
**Nuno Fernando**. Confirms Luis's children as Juanita and "Pam" (= Panola).
**GAVIN LERENA the jockey appears**: Roberto Paul → Ricardo → **Carlos "Tex"** → **Gavin**. So Gavin is
Cheryl's first cousin once removed and David's second cousin. *Per the family chart; not independently
verified.* This vindicates the day-one prediction that the 61 SA Lerenas are one founder cluster.
Also: Cheryl m.1 **Derrick Luwinski**, m.2 Ivan Defranceski; David's other names recorded as
**David Leonard Luwinski / Luwinski Defranceski**.

## PABLO ARMANDO — DEMOTED, not discarded
The passport man (b. 22 Feb 1882 Rosario, Trainer, Rugby, widower) **is not** Roberto Paul (b. c.1874,
Race Horse Owner, Rugby, widower). Pablo ≠ Roberto/Armando ≠ Paul, and 8 years is too wide.
**Best reading: BROTHERS** — two Argentine horsemen at the Cape. Would explain why one's passport sits in
the other's papers, and why Roberto Paul's eldest son is Roque Luis **ARMANDO**.
Either way **Rosario is the family's town**.

## UNPROVEN / REJECTED
- **San Miguel 1872 baptisms (Llorens)** — David states these are unproven. Surname is LLORENS not Lerena;
  streets and parish point to **Buenos Aires** not Rosario. Filed to `sources/unproven/` with a README.
  Do not chase again without new reason.
- `31843_233558__0002-00065.jpg` is **misfiled** — a Brisbane cemetery index of FALCO burials. Belongs to
  the Falco archive.

---

# 8 September 2026 — CORRECTION: Pablo Armando IS Roberto Paul. One man.

**Source:** baptism register, **Corpus Christi Catholic Church, 2 Clare Road, Wynberg 7800**, sourced by
**Cheryl Defranceski** direct from the parish archives. Transcription: `sources/corpus-christi-wynberg/`.

> Anno **1905** die **25** mensis **Nov.** natus est, et anno **1911** die **12** mensis **Junii**
> baptizatus est **Roque Lois Armando**, filius **PABLO ARMANDO LERENA** et **MARY SEPTIMA LERENA
> (olim TAYLOR)** conjugum: a me **Bertram W. Glynn**.
> Patrinus fuit **José Breton** (proxy), Matrina fuit **Maria Louisa Breton** (proxy).

## The proof
- Roque Luis Armando's **1973 death notice**: parents = **"Roberto Lerena"** and **"Mary Septima Lerena"**.
- Roque's **1911 baptism**: parents = **"Pablo Armando Lerena"** and **"Mary Septima (olim Taylor)"**.
- Same son, same mother → **the father is one man under two forms of his name.** Spanish at the altar,
  English at the registry. *Pablo = Paul.*

**My earlier "brothers" inference was WRONG and is retracted on the site.**

## Consequences
1. **GENERATION 1 = PABLO ARMANDO LERENA, b. Rosario de Santa Fe 22 Feb 1882, d. Newlands 19 Mar 1950.**
   The family's Rosario tradition is confirmed *for the head of the line himself*.
2. **The "76 years" on the 1950 death certificate is WRONG — he was 68.** Informant W. Fraser was the man
   "causing burial", not kin. A passport the deceased carried beats an age reported at second hand.
3. **"Roberto" on the 1973 death notice is explained**: it was signed **R. M. Lerena = Rhena May**, Roque's
   *second* wife, married 1966 — sixteen years after her father-in-law died. She never met him.
4. **Mary Septima's maiden name TAYLOR is now DOCUMENTED** ("olim Taylor"), not just family chart. This is
   the Taylor of the MyHeritage tree title.
5. The family was **Roman Catholic** and at **Wynberg** by 1911. Mary Septima was buried in the Roman
   Catholic allotment at Maitland in 1935.

## New detail from the same entry
- **Baptism delayed six years** (b. 1905, bapt. 1911) — worth a thought; possibly the family arrived in
  South Africa between those dates, and the child was baptised on arrival. **TESTABLE: if so, the crossing
  falls 1905-1911.** Ricardo Juan Carlos b. 1920 and Nuno b. 1924 were Cape-born.
- Godparents **José Breton** and **Maria Louisa Breton**, both *by proxy* — Spanish names, and proxies
  suggest they were **not in South Africa**, i.e. standing in absentia, plausibly from Argentina.
  **A lead: who were the Bretons?**
- Roque m.1 **Rosalina Wilhelmina CHAPPELL**, 21 Sep 1936, St Joseph's, Johannesburg (Rev. P. McCarthy).
  Note: the 1973 death notice calls her **"Rosina Wilhelmina"**, and a family photo is filed as
  **"Rosaline Wilhelmina FORBES Lerena"**. CHAPPELL vs FORBES unresolved — possibly a prior marriage.
- Roque m.2, **as a widower**, 12 Mar 1966, **St Charles Chapel, Victory Park, Johannesburg** (= Rhena May).

## Caution on the circulated translation
The English caption under the circulated image is a machine rendering and **garbles the Latin** — it makes
Pablo Armando the *son* of Roque and turns *Septima* into "seventh". The reading above is this archive's own.

## The racing dynasty — independent public corroboration

South African racing press (Sporting Post, The Citizen, Gold Circle, Sky Sports), searched 8 Sep 2026:

- **"Gavin Lerena's GREAT-GRANDFATHER and GRANDFATHER were trainers."** On the family chart the
  great-grandfather is **Pablo Armando Lerena** and the grandfather **Ricardo Juan Carlos Lerena**.
  → **Independent corroboration of the passport's "Profesión: Trainer".** The racing press and an Argentine
  consular document, with no connection to each other, say the same thing about the same man.
- Gavin's father **Carlos "Tex" Lerena** — top jockey 22 years, also rode in Mauritius. Chart: Tex is
  Ricardo's son, Gavin's father. ✓
- Gavin's uncle **Spike Lerena** — ex-jockey, leading Gauteng trainer (Jungle Rock). Chart: Spike is
  Ricardo's son, so Tex's brother. ✓
- **Stephen Lerena** (Randjesfontein) is Spike's son; **Brandon** a cousin, with the Ricky Maingard stable.
- **"Great Uncle Frederick CHAPELL was also a jockey and trained the winner of the 1957 Durban July —
  the filly MIGRAINE."**
  → ***CROSS-CONFIRMATION.*** The Corpus Christi register records Roque Luis Armando Lerena marrying
  **Rosalina Wilhelmina CHAPPELL** on 21 Sep 1936. A Catholic parish register in Wynberg and the South
  African racing press, neither aware of the other, place a **Chappell/Chapell** beside this family.
- **Kevin Lerena**, the boxer, is publicly associated with the same family (Green Street Bloodstock).

**Note:** sportingpost.co.za and pressreader return 403 / bot-verification to automated fetching. These
facts come from search result summaries and need reading by hand for exact wording and dates.

---

# 8 September 2026 — "BOB LERENA", and the hunt for the death notice

## *** BOB LERENA — the racing press names him directly ***
**Sporting Post, 13 August 2014**, obituary of trainer **Alan Higgins (1929–2014)**
(PDF supplied by David; `sources/press/`):

> "Higgins started out in horseracing as a jockey, first riding in amateur races as a schoolboy … **before
> being apprenticed to Bob Lerena, who was the grandfather of Spike.**"

> "**Peter Kannemeyer was an apprentice to Bob Lerena at the same time as Higgins** and the pair became
> life long friends."

**"Bob" is Robert. Spike's grandfather is Ricardo's father = PABLO ARMANDO / ROBERT PAUL LERENA.**
Higgins was born 1929, so he was apprenticed in roughly **1944–47**, and Pablo Armando died in **1950**.

→ **A third name form: Pablo Armando (Argentine) · Robert/Roberto Paul (civil) · "Bob" (the yard).**
→ **He ran a training yard at Cape Town that took apprentices** — published, and wholly independent of any
document in this archive. Two of his apprentices are named. Higgins later founded the Philippi training
centre; Kannemeyer is a known Cape racing figure.

This is the strongest independent corroboration yet of the passport's *"Profesión: Trainer"*.

## FamilySearch — the death notice is BLOCKED
- The estate images David holds are from **"South Africa, Cape, Probate Records of the Master of the High
  Court, 1822–1990"** (collection `2517051`, waypoint `WV44-9P8`).
- Signed in, the ark `3:1:3Q9M-C913-K9H3-D` returns **"Image Restricted — Image access is typically
  determined by local laws or the custodian who has the original document."**
- **So this collection is viewable only at a FamilySearch affiliate library / Family History Centre.**
  David presumably obtained his pages that way. **DO NOT retry from home.**
- Full-text search does **not** surface this collection's death notices.
- → Routes remaining: (a) an affiliate library visit, then browse the film around the pages held;
  (b) order from the **Western Cape Archives** — request drafted at `requests/wcars-mooc-6-9-17017.md`.

## New from FamilySearch full-text (these ARE readable)
- **Voter Records: South Africa, 1925–1931** — *"1399 **Lerena, Roque Luis Armando**"*, polling district
  (stemdistrik) **No. 770**, in a run of addresses around **Scott Rd / Eden Rd**.
  His full name exactly as the Corpus Christi register has it. He turned 21 in Nov 1926.
  `ark:/61903/3:1:3QHV-GQVF-S7YR-K`
- **Land Records: South Africa, Farm Records 1895–1955** — a deeds entry naming
  *"Huno [Nuno] Fernando Lerena"* with **6.10.1924** (his birth date, as SA deeds records identify people),
  property around **Cologne Road**, 6,600 sq ft, transferor/transferee incl. "Gough Cooper".
  **OCR is badly garbled — needs reading by eye.** `ark:/61903/3:1:3QHK-F7NW-L7PV`
  Two further farm-record hits: `3QHK-N7NW-G375`, `3QHK-G7F2-6WJT`. **Unexamined — and the ostrich-farm
  claim is still open, so these deserve a proper look.**
- Full-text "Lerena" worldwide returns **43,216** matches, concentrated in **Arequipa (Peru)**,
  **Valladolid & Galicia (Spain)**, and **Flores / Trinidad / Montevideo (Uruguay)**. Note again how strong
  **Uruguay** is. No Rosario hits surfaced in the first pages.

## Still needed from David
- **Forebears Spain provincial page** — he opened it in the browser but the tab returned no text to the
  reader. Still outstanding.

---

# 8 September 2026 — the three land records. No farm; and a correction.

FamilySearch full-text, "Land Records: South Africa. Farm Records" (a generic FS label — these are
**Deeds Office transfer registers**, not farm registers). Table: `data/land-records.tsv`.

## 1 & 2 — both NUNO FERNANDO LERENA, and both suburban erven
- `3QHK-F7NW-L7PV` (img 251/260): "Huno Fernando Lerena", **6.10.1924**, lot 245, Cologne Road area,
  **6,600 sq ft (~613 m2)**.
- `3QHK-N7NW-G375` (img 216/260): "Nuno Fernando Lerena", **6.10.24**, lot 210, transfer **2257739**,
  dated **8/53**, **14,560 sq ft (~1,353 m2)**.
- Both identify him by his **birth date**, as SA deeds records do. Both are register G.P.-S. 7282-1937.
- Aug 1953 is suggestive: his father's estate capital fell due when he turned 30 on **6 Oct 1954**.

**These are house plots — 613 and 1,353 square metres. NOT farms.**

## 3 — NOT THIS FAMILY
`3QHK-G7F2-6WJT` (img 73/259): deceased estate of the **late LUCAS LERENA**, spouse
**RACHEL LERENIA (born MALEKA)**, B. Eaton Township, lot 570, 283 Roods.
**Maleka is a Sotho/Tswana surname.** Compare the other full-text hit: *Pretoria, Transvaal, Religious
Membership Records 1939* — **"Hanson Seko Lerena"**.

## *** CORRECTION: the 61 South African Lerenas are NOT all one kindred ***
This archive stated on day one that 61 bearers in a country with no Spanish colonial past "looks like one
family that arrived and multiplied". **That was too strong.** There are **at least two unconnected Lerena
populations in South Africa**: this Argentine-descended family, and one or more **Black South African
families** of the same or near-identical name. Nothing links them and no link is asserted.

The founder-cluster reading still holds *for this family* — the descent from Pablo Armando is documented
and the racing dynasty is public record — but the raw 61 can no longer be used as the argument.
**Corrected on the site rather than quietly removed.**

## *** THE OSTRICH FARM IS NOW DOUBTFUL ***
A deeds sweep returns **no land whatsoever** for Pablo Armando / Robert Paul Lerena. The only Lerena
property found in this family is his son's two suburban plots in the 1950s.

Everything else points the same way: stables at **Rugby**, a **training yard taking apprentices**, a
**Newlands** address, "**Race Horse Owner**" at death. A Cape Town racing man, not a Karoo farmer.

**Not disproof** — deeds coverage is partial, a farm could have been leased, and **Oudtshoorn's own records
remain unsearched**. But it is now the only one of the four family traditions with evidence pointing
against it and none for it.

**Scorecard on the family's four claims:**
| Claim | Status |
|---|---|
| Argentine, from Rosario | **CONFIRMED** — his own passport |
| Brought horses | **CONFIRMED** — passport, death certificate, stables file, the press, and a carrot bill |
| Consul General | **DISPUTED** — he was the bearer; A. B. Bayne signed |
| Ostrich farm | **DOUBTFUL** — no land held; wrong district; wrong trade |

---

# 8 September 2026 — MARY SEPTIMA TAYLOR, and her line

MyHeritage read via the in-app browser. **Trick that works:** re-root the tree with
`?rootIndividualID=<id>` on the tree URL, then read
`window.newTree.genealogy._individualsCollection._allIndividuals`. The tree only loads the visible
viewport, so re-rooting is how you reach any branch. Real site ID is **329786671** (leaked in thumbnail
URLs); tree ID **4**. Person-profile URLs did NOT work; re-rooting did.

## The woman
**MARY SEPTIMA TAYLOR, b. 17 Sep 1884, d. 15 Nov 1935** — matches the Maitland burial register exactly
(Nov 1935, aged 51). MyHeritage id **4000037**. Husband **4000036 "Pablo Armando / Robert Paul Lerena,
Feb 22 1882 – Mar 19 1950"** — *David's tree already merges the two names, independently of this archive.*

## *** SEPTIMA MEANS SEVENTH, AND IT IS LITERAL ***
Parents **William Taylor (11 Feb 1826 – 30 Nov 1902)** and **Mary Ann Hellen BRAYLEY (20 May 1843 –
21 Apr 1900)**. Ten children:

| # | Child | Born | Died |
|---|---|---|---|
| 1 | Kathleen Georgina | 4 Nov 1870 | 29 Feb 1940 |
| 2 | William John | Nov 1870 | 11 May 1951 |
| 3 | Horace A | Apr 1872 | 18 Jan 1934 |
| 4 | Isabella Temple "Edie" (m. Dalling) | 1874 | Dec 1953 |
| 5 | Margaret Hellen Walker "Maggie" (m. Bell) | 1876 | after 1953 |
| 6 | Irene "Rene" (m. Burton) | 1879 | 25 Mar 1969 |
| 7 | **Unknown twin** | 1879 | — |
| 8 | Lucy Elizabeth (m. Sweet) | 4 Aug 1881 | 26 May 1957 |
| 9 | **MARY SEPTIMA** | **17 Sep 1884** | 15 Nov 1935 |
| 10 | Agnes Walker "Aggie" (m. Wood) | 3 Aug 1889 | 29 Apr 1974 |

**Daughters in order: Kathleen(1), Isabella(2), Margaret(3), Irene(4), the twin(5), Lucy(6),
MARY SEPTIMA(7).** The name is a count, and it comes out.
→ **INFERRED: the unnamed 1879 twin was a GIRL**, or the arithmetic fails. Her name is lost; her sister's
name records her.
→ The name persisted: infant **Antoinette SEPTIMA Lynette Lerena**, b. 3 Jan 1943, d. 7 Jan 1943.

## Two generations further back
**James Taylor, b. circa 1796**, m. **Harriet Reynolds (1803 – 12 Nov 1827)**; later **Laura Collins**
(b. before 1827). An earlier **William Taylor b. 29 Dec 1824, d. 10 Sep 1825** (8 months) — our William
(b. Feb 1826) carries the dead child's name.

**So the Taylor line reaches the 1790s — further back than the Lerena line, where Pablo Armando's own
parents are still unknown.**

## PLACES ARE NOT ESTABLISHED
The tree gives no birthplaces. Surnames lean English and **BRAYLEY is a Devon name** (from Bray, north
Devon). *Temple, Walker, Reynolds, Sweet, Dalling, Burton, Bell* fit. **But nothing is written down yet.**
Easiest gap in the archive to close: **1891 and 1901 England censuses** (Mary Septima aged 6 and 16, whole
household with birthplaces); **GRO birth indexes** 1870-1889; the **Taylor–Brayley marriage** c.1869.

## THE SHIP STORY — David's objection, and the answer
David: *"they met on a ship travelling to South Africa, but I find it odd, as she was in England, and why
would he be in England if he went from Argentina to South Africa."* Fair. Three things resolve it:

1. **The River Plate reached the Cape VIA EUROPE.** In the 1900s there was no dense direct BA–Cape Town
   passenger service; the normal route was to sail to Europe and change ships, Southampton being the hub of
   the mail service to the Cape. **He need never have been "in England" in any real sense — he changed
   ships.** "Came from Argentina" and "met on a ship from England" are not in conflict. *Inferred.*
2. **The horses were already moving that way.** *Documented:* of ~519,000 horses used in the South African
   War, **~360,000 were shipped in**, from England, Australia, Canada, NZ, Burma **and ARGENTINA** (British
   officers complained about the "mongrel Argentines"; Australian bushmen broke them). Pablo Armando was
   **17 when that war began and 20 when it ended**, and was a horseman. He was moving *with* a trade.
3. **She had a documented reason to be aboard.** Mother d. Apr 1900, father d. Nov 1902 — orphaned at 15
   and 18. *Documented:* **from 1901 the Colonial Office and emigration societies ran an organised
   programme sending single British women to South Africa**, which the war had turned from charity into
   imperial policy. An orphaned Englishwoman of 19-20 sailing for the Cape in 1903-05 is the type the
   scheme existed to carry.

### THE TEST
**UK outward passenger lists (BT 27)**, surviving from 1890 and name-indexed. If they sailed from
Southampton for the Cape c.1903-05, **both names are on one list.** Roque was born at Cape Town
**25 Nov 1905**, so they were both at the Cape and married by early 1905. That brackets the crossing tightly.

## Also recovered from the tree (large haul — not all worked yet)
- **Rose Lilian Theys, 18 Jan 1896 – 13 Dec 1987** — the "no relation" executrix who lived at 7 Forth Road
  and took a quarter of the estate. She IS in David's tree.
- **CORRECTION to an earlier note:** Roque's first wife was **Rosaline Wilhelmina (Rose) FORBES,
  5 May 1903 – 2 Jul 1950** — *not* Chappell. **Doreen May CHAPPELL (13 Apr 1921 – 17 Nov 1999)** is
  **Ricardo's** wife. So the racing press's "great uncle Frederick Chapell" attaches through **Ricardo's
  marriage**, not Roque's. The Corpus Christi annotation naming "Rosalina Wilhelmina Chappell" therefore
  needs re-reading — possibly a prior married name, possibly an error.
- Roque's 2nd wife: **Rhena May BARICHIEVY, 3 Sep 1913 – 1 Apr 1998**.
- **Ricardo Juan Carlos Lerena, 6 Jan 1920 – 21 Dec 1994.** Children incl. Roberto Juan Roque (1944-2022),
  **Ricardo Paul (b. 1945)**, Pierre Frederick (1948-1999), Yvonne Paulette (b. 1950), **Anton Armando
  (1952-2003)**, Juan Carlos (b. 1955), **Gilberto (1957-2020)** — note *Gilberto*, echoing Gilberto Lerena
  Lenguas of the Argentine Stud Book. Theresa (b. 1961).
- Infant deaths: Unknown Lerena (17-22 May 1932); Rieta Maria Armando Lerena (Dec 1935 – 28 Aug 1937);
  Ricardo Juan Carlos Lerena (May 1939 – 31 Jan 1940); Antoinette Septima Lynette (3-7 Jan 1943);
  Careen Marie (Jun 1947 – 22 Jun 1947).
- **Roberto Llorens (b.1850)** and **Francisca Fernandez Lerena (b. circa 1850)** ARE in David's tree —
  i.e. the San Miguel 1872 baptism is his working hypothesis for Pablo Armando's parents. **David states it
  is unproven**, and this archive keeps it in `sources/unproven/`. Note the tree also holds a
  **Roberto Juan Roque Lerena (1944-2022)** — the same name string as the 1872 Llorens child, which is
  presumably why the link was drawn.

---

# 8 September 2026 — THE MARRIAGE, 3 SEPTEMBER 1911. And it reframes everything.

Went looking for passenger lists; found the marriage instead. FamilySearch, *South Africa, Civil Marriage
Records, 1801-1974*, index ark `1:1:88RY-GF3Z`; image film **#007729519**, item 5, image **40 of 638**,
*Cape Province Marriage Certificates 1-15 Sep 1911*, **images supplied by the National Archives of South
Africa** (and, unlike the probate collection, **NOT restricted**). Full transcription:
`data/marriage-1911.tsv`.

> Marriage solemnized at **WYNBERG**. No. **160**, 3rd September **1911**.
> **Pablo Armando Lerena**, 29, E, **bachelor**, **horse-dealer**, of **Diep River**
> × **Mary Septima Taylor**, 27, E, **spinster**, of **Diep River**
> "Married in **St Dominic's** at **Wynberg** aforesaid, after **banns**."
> Both **signed their own names in full**. Examined by "**Bert…**".

## *** THEY MARRIED SIX YEARS AFTER THEIR FIRST SON WAS BORN ***
- Roque born **25 Nov 1905**, Cape Town.
- Roque baptised **12 June 1911**, Corpus Christi, Wynberg, by **Bertram W. Glynn**.
- Parents married **3 Sept 1911**, St Dominic's, Wynberg — **both "bachelor" and "spinster"**, so
  **neither had been married before**.

**This explains the six-year baptism delay I flagged earlier.** The child was baptised in June and the
parents married in September: **the family was regularised in the Catholic church in the course of 1911**,
almost certainly by the same priest — the examining signature reads "Bert…", and Glynn is Bertram W.

So Roque was born outside marriage and legitimated by it. Stated plainly because the archive states things
plainly; it is also, on the record, a couple who stayed together fifty years and were still husband and
widower at death.

## Other things this record settles
- **"HORSE-DEALER" in 1911** — a fourth occupational term, and they track a career:
  **horse-dealer (1911) → trainer (1940, and "Bob Lerena's" yard in the 1940s) → race horse owner (1950)**.
- **DIEP RIVER** — the earliest address yet known. The address sequence is now
  **Diep River (1911) → Rugby (1931-32) → Observatory (Mary Septima's death, 1935) → Camps Bay (1947-48)
  → Newlands (1950)**.
- **Both literate** — they signed in full, in confident hands.
- **Wynberg is the family's parish.** Marriage at St Dominic's Wynberg; son baptised at Corpus Christi
  Wynberg; his death registered in the Wynberg district in 1950; her death registered at Wynberg in 1935.
- **NO PARENTS NAMED.** Cape marriage registers of this era don't carry them. So this does **not** give
  Pablo Armando's father.

## Effect on the SHIP STORY
It does **not** disprove it — they could still have met crossing in 1904-05. But it removes an assumption
and sharpens the search:
- They did **not** marry on arrival. She remained **Mary Septima TAYLOR until September 1911**, so any
  passenger list before that date carries her under **Taylor**, not Lerena — and they may have travelled
  **separately**.
- Because they were unmarried in 1905, a shared cabin/berth entry should not be expected.

## Her death, independently indexed
*South Africa, Cape Province, Civil Records, 1840-1972*: **"Mary Septima Taylor Lerena", death
15 November 1935, Wynberg, Cape Province** — matching the Maitland burial register exactly.

## AND A CAUTION: no English record for her has been found
A FamilySearch search on "Mary Septima Taylor" returns **only the two South African records**. No English
birth, baptism or census entry has yet been found for a Mary Septima Taylor born 1884. **Her English birth
is family knowledge, not documented.** She could equally have been born at the Cape to an English family —
Victorian settlers named children exactly the same way. **Do not assert England.**
Test: 1891 and 1901 England censuses; GRO birth index Sept quarter 1884; and, if those fail,
Cape baptism registers.

## Also seen
**Find a Grave Index** carries **Pablo Armando Lerena, b. 22 Feb 1882, d. 19 Mar 1950** — a memorial
exists. Not yet opened; may give the grave and a headstone photograph. Likely Maitland Cemetery no. 1,
where his wife lies in grave 7719A.

---

# 8 September 2026 — READING DAVID'S OWN FACTS AND NOTES (a process correction)

**I had not been reading the MyHeritage Biography/Facts/Notes panels — only the rendered tree cards.**
David records everything there. Method, for every future session:

> Re-root the tree with `?rootIndividualID=<id>`, then read the LEFT PANEL's **BIOGRAPHY** and **FACTS**
> sections from `document.body.innerText` (slice from the index of "BIOGRAPHY"). The card data carries only
> names and dates; **the research is in the panels.**

Several things below correct this archive. They are corrections *to me*, from David's own sourced work.

## MARY SEPTIMA TAYLOR — my caution was WRONG
- **Birth: 17 September 1884, BIDEFORD, DEVON, ENGLAND.** Cited to *England and Wales Birth Registration
  Index, 1837-2008* (FamilySearch ark `1:1:2XLQ-C29`), from findmypast, **citing Birth Registration,
  Bideford, Devon, GRO Southport.**
  → **RETIRE the hypothesis that she may have been Cape-born.** My FamilySearch search was simply badly
  filtered. **Her English birth is documented.**
- **Christening: 30 Oct 1884, ANGLICAN — St Margaret's Church, Northam, Devon.**
- **Residence 5 Apr 1891 (the census): Barnes, Surrey** — "2 Crystal(?) Villas, Stanton Road. Living with
  aunt…"
- **Bishop Phillpotts' Prayer Book Prize, 1 Dec 1900, Northam** — Exeter Diocesan Board of Education,
  religious knowledge exam for *monitors, candidates and pupil teachers*; Class III, monitors over 16 and
  pupil teachers, **one of 43 out of 88 who passed**. David: *"Appears to have been a scholar."*
  **She was a pupil teacher at 16.**
- ***BAPTISM (her own): 16 December 1911, CATHOLIC, Corpus Christi, Wynberg.***
  → **SHE CONVERTED.** Anglican at birth; received into the Catholic church **three months after the
  marriage**. The 1911 regularisation is now complete and documented: **son baptised 12 June, parents
  married 3 September, mother received 16 December.**
- **Death 15 Nov 1935, 34 Florence Villas, Observatory. CAUSE: carcinoma of uterus and bladder, septic
  nephritis.** Burial **16 Nov 1935, plot 7719A, Woltemade Cemetery, Maitland**.
- **Her sons were born:** Roque — Cape Town; **Ricardo — CLAREMONT**; **Nuno — WYNBERG**.
- **David's Fact 1 (family memory):** *"She had a difficult time, especially when she got ill, with Luis
  being so challenging and at odds with his father Pablo… it broke her heart when Pablo cut Luis off from
  the family and home… he had always been a difficult person, who also due to the fall out became very
  embittered and unforgiving."*
  → ***THIS EXPLAINS THE WILL.*** In the 1950 estate **Luis (Roque) received only half a share** — the same
  as **Rose Lilian Theys, "no relation"** — while Nuno and Ricardo shared three-quarters. **A documented
  estrangement, and the will is its receipt.**

## PABLO ARMANDO LERENA — David's notes, several of which redirect this archive
- Birth **Rosario, Rosario Department, Santa Fe** ✓. David's own note: *"still need to look through the
  Rosario records here:"* **`familysearch.org/en/search/film/004098791?cat=208788&i=4`** — an actionable
  film for the Rosario baptism. **TOP TARGET.**
- Occupations recorded: **Horse Breeder · Horse dealer and trainer · Ostrich Farmer (unconfirmed, advised
  by Sue Taylor) · Uruguay consulate, Cape Town.**
- ***"Pablo used to import horses into South Africa from Argentina FOR THE ZA GOVERNMENT.* He then also
  brought in some horses for his own stables from there."**
  → **This is exactly "testable form 1" of the horse claim, which this archive framed on day one.** Family
  testimony, not yet a document — but it names a searchable thing: **government remount/bloodstock
  contracts.**
- **"Pablo had big stables in Cape Town and GAVIN KNOTT was given the job of tying the horse business up
  after he died."** A named person to trace.
- ***"He owned a lot of land up around BLOUBERG area."*** → **QUALIFIES my "no land at all" finding.** The
  deeds sweep found none, but the family says Blouberg (north of Cape Town, beyond Milnerton). **Search the
  deeds under Blouberg, and under LERINA/LARENA.**
- **"The 3 brothers left Cape Town for JOHANNESBURG in the 1940s. They all lived together in a house in
  MAYFAIR."** → explains the Cape→Transvaal shift this archive inferred from NAAIRS.
- ***"Friendly with political figures and was the ambassador for Argentina for a while. Although YVONNE
  LERENA claims it was URUGUAY."*** plus an occupation entry **"Uruguay consulate, Cape Town"**.
  → **MAJOR REDIRECT.** The consular tradition may be **URUGUAYAN, not Argentine** — which would explain
  why nothing has been found on the Argentine side, and why he was a *bearer* on an Argentine passport.
  **Search the Uruguayan consulate at Cape Town.** Note also Uruguay has the world's densest Lerena
  population.
- **"He ran from Argentina for a communism related reason"** — David flags it as unsubstantiated family
  claim.
- **Ricardo Juan Carlos was ALSO called "Bob".** So *two* Bob Lerenas. The Sporting Post's "Bob Lerena,
  grandfather of Spike" is still **Pablo Armando** (Ricardo is Spike's *father*), but the ambiguity is a
  real hazard in racing records.
- **David's own open question, in his biography field: *"is roberto paul and pablo armando the same
  person?"*** → **ANSWERED TODAY** by the Corpus Christi baptism register. One man.
- ***"Dates have been manipulated to show earlier year on copy document from 1916. But was 1911."***
  → Someone altered the marriage date on a 1916 copy — presumably to place the marriage before Roque's
  1905 birth. **The family covered up the illegitimacy.** Worth finding that 1916 copy.

## THE CHAPPELL / FORBES TANGLE — SOLVED
David: **"He [Roque] was married to Doreen's mother Rose."**
So **Rosaline Wilhelmina (Rose) Forbes** had first been married to a **Chappell**, bearing
**Doreen May Chappell**; Rose then married **Roque** in 1936, while Doreen married Roque's brother
**Ricardo** in 1941. **Roque married his brother's mother-in-law.**
→ The Corpus Christi annotation "Rosalina Wilhelmina Chappell" is her **previous married name**.
**My hypothesis was right.** And it explains the brothers' feud: *"Cardo and Luis never spoke again."*

## WILLIAM TAYLOR (1826-1902) — her father
- **Born 11 Feb 1826, Worlingworth ["Wollingworth"], SUFFOLK**; christened 12 Mar 1826.
- ***Occupation: PENSIONER, COACHMAN, DOMESTIC SERVANT***, of **Northam, Devon**.
  → **Horses on her side too.** A coachman's daughter married a horse-dealer.
- m.1 **Laura Collins, 1 Jan 1848, Stowmarket ["Stonemarket"], Suffolk.** *(Correction: Laura was
  WILLIAM's first wife, not James Taylor's second, as this archive earlier guessed.)*
- m.2 **Mary Ann Hellen Brayley, 26 Jan 1870, St Mark's Parish Church, BIDEFORD, Devon** — he was 43,
  she 26.
- Children's addresses: **23 Geneva Place, Bideford** (1872) · **North Street, Northam** (1881) ·
  **2 Fore Street, Northam** (1889).
- Wife d. **21 Apr 1900, Home Sweet Terrace, Northam**.
- **Died 30 Nov 1902, 2 Park Terrace, Northam. Cause: chronic bulbar paralysis and asphyxia.** Informant
  was his son **Horace Archibald Taylor**, present at the death.
- **Buried: old grave no. XB28-K8, Northam parish church.**

→ **The family is of NORTHAM and BIDEFORD, north Devon** — which is exactly where **Brayley** comes from
(Bray, north Devon). This archive's inference from the surname alone was right, and is now documented.

---

# 8 September 2026 — THE ROSARIO FILM: an index David did not have

Followed David's own note (`familysearch.org/en/search/film/004098791?cat=208788&i=4`).

## What the film is
Catalog **koha:208788** — ***"Registros parroquiales, 1722-1961", Archidiócesis de Rosario, Iglesia
Católica, NUESTRA SEÑORA DEL ROSARIO (Rosario, Santa Fe)*** — the cathedral parish of Rosario. Filmed by
the Genealogical Society of Utah, 1974. **71 rolls.** Note in the catalog: *"Algunos tomos incluyen su
propio índice."* **Images are NOT restricted** — fully viewable from home.

## *** THE FIND: there are ALPHABETICAL BAPTISM INDEXES ***
David's note pointed at the register volume itself (DGS **4098791**, 543 images) and said *"still need to
look through the rosario records here"*. **He does not need to read it page by page.** The catalog carries
separate index films:

| Index | Film | **DGS** | Images |
|---|---|---|---|
| Bautismos A-K **1731-1879** | 1093077 | 4530323 | |
| Bautismos L-Z **1731-1879** | 1093078 | **4530324** | |
| **Bautismos A-Z 1879-1900** | 1093079 | **4530325** | **718** |
| Bautismos A-Z 1901-1919 | 1093080 | 4530326 | |
| **Matrimonios 1731-1761, 1860-1921** | 1091466 | **4531036** | |

**DGS 4530325 covers 1882.** Full data: `data/rosario-films.tsv`.

## Structure of the index, decoded
Columns: ***APELLIDOS | NOMBRES | AÑO | FOLIO***, in blocks headed **"Libro NN"**.
**It is alphabetical by letter, but WITHIN each letter it runs CHRONOLOGICALLY** — not alphabetically by
given name. So the L section is a run of pages ordered by year.

## Where LERENA will be
- **The L section of DGS 4530325 sits at roughly images 395-406.**
- **Image 403 shows AÑO 1900-1901** — i.e. the **END** of the L run. Read clearly:
  *Lirgua, Lacorte, Luque, Lavena, Lopez, Lescano, Lacurado, Leal, Las Heras, Lejarza, Leonar, Laborante,
  Longo, Leguizamón, Liendo, Leandrini…*
- **Image 406 is already into "Ll-"** (Llanos, Llorens, Lloret…) — Spanish indexes place **Ll after L**.
- → ***1882 entries lie a few pages BEFORE image 403, in the same L run — try images 395-402.***

## Why I did not finish it
The FamilySearch deep-zoom viewer renders unreliably in this browser pane: it needs a click to render, but
a click in the image area hits the filmstrip and jumps pages, and it kept flipping into thumbnail-grid
mode. **This is a tooling limitation, not a record problem.** The images are open and the target is narrow.

## What to do next — a five-minute job by hand
1. Open **`familysearch.org/search/film/004530325`** and go to **image ~397**.
2. Read the **APELLIDOS** column for **LERENA** with **AÑO 1882**. (Watch also **LERENA/LLERENA/LARENA**,
   and remember *Lerena* can be a forename.)
3. Note the **Libro** and **FOLIO**, then open that register volume and photograph the entry.
4. **The entry names his parents** — which is the whole object.

## And an arguably better target
**DGS 4531036, Indice de Matrimonios 1860-1921.** Pablo Armando's parents married before 1882; a Catholic
marriage entry names **both fathers and both mothers** — four names in one line, against two from a
baptism. And **DGS 4530324 (Bautismos L-Z 1731-1879)** would carry his **older siblings**, and possibly his
parents' own baptisms.

---

# 8 September 2026 — THE ROSARIO INDEX, READ. A clean negative.

Done in **Chrome** (the in-app pane could not drive the deep-zoom viewer). **Method that works:**
> Open `familysearch.org/search/film/<DGS>`; if it opens in thumbnail-grid mode click the single-page icon;
> then **triple-click the "Image [nnn]" box, type the number, press Return** to jump. **Do NOT click the
> +/- zoom buttons** — they land on the filmstrip and jump pages. Instead use the
> **`computer` tool's `zoom` action with a region** — in Chrome it crops properly and the typescript is
> perfectly legible.

## What was read
**Indice de Bautismos A-Z 1879-1900, DGS 4530325** — Nuestra Señora del Rosario (the cathedral parish),
Rosario, Santa Fe. Columns **APELLIDOS | NOMBRES | AÑO | FOLIO**, in **Libro** blocks; alphabetical by
letter, **chronological within the letter**.

**The whole L run for 1882 and 1883 has now been read, end to end** — see
`data/rosario-index-searched.tsv`:

| Image | Libro | Year | Folios |
|---|---|---|---|
| 369 right | 24 | 1882 | 402-467 |
| 370 left | 24 | 1882 | 471-567 |
| 370 right | 24 / **25** | 1882 | 574; then **9-137** |
| 371 left | 25 | 1882 | 138-249 (1883 starts at f.268) |
| 372 left | 25 / 26 | 1883 | 457-540; then 7-73 |
| 372 right | 26 | 1883 | 75-209 |
| 404 right | 23-27 | 1880-84 | the entire **Ll-** section |

## *** RESULT: NO LERENA. NO LLERENA. 1882-1885 read end to end. ***
Not in 1882, 1883, 1884 or 1885, and not in the separate **Ll-** section (whose whole 1880-84 content is
seven entries: Llanos, Llorca ×3, Llanes, Llaurer, Llumar).

**Extended 8 Sep 2026** through images 373-376: Libro 25 f.210-299 (1883); Libro 26/27 f.305-453 and
f.2-5 (1884); Libro 27 f.12-100, 112-259, 268-359 (1884); f.363-541, 542-656 (1885); Libro 28 f.2-17,
26-127 (1885). Every line read. Coverage table: `data/rosario-index-searched.tsv`.

### One oddity worth a look
Image 374, left column: ***"Ler · María · 1884 · folio 13"*** (Libro 27). A surname given as bare
**"Ler"** — which could be a clipped or abandoned **Lerena**. A girl, so not Pablo Armando, but
**possibly a sister**. Cheap to check: Libro 27, folio 13, 1884.

**Pablo Armando Lerena was not baptised at the cathedral parish of Rosario in 1882 or 1883.**

This is a solid negative, not a failed search: the index is legible, complete for those years, and was read
line by line.

## What it means — five live possibilities
1. **Another Rosario parish.** By 1882 Rosario was a city of ~50,000 and the cathedral was not its only
   parish. **This is the most likely answer, and the catalogue lists other Rosario parishes.**
2. ***A LATE BAPTISM — and this family demonstrably did that.*** Pablo Armando's own son **Roque was born
   25 Nov 1905 and not baptised until 12 June 1911 — six years**. If the father was treated the same way,
   his baptism could fall anywhere in **1884-1895**. The L runs for those years are images ~373-396 of the
   same index and could be read the same way.
3. **Born at Rosario, baptised elsewhere** — e.g. at the mother's family's parish.
4. **Indexed under another name** — the mother's surname, or a variant. Remember *Lerena* also occurs as a
   forename.
5. **The passport is not exact** about the birth date, though it is his own document and gives a precise day.

**Possibility 2 is the one to test first**, because it costs only a dozen more page-reads in an index
already open, and because the family's own habit points at it.

## Note on the register volume
David's original film, **DGS 4098791**, is a register volume, not an index. Reading it page by page is
**not** the way in — and now that 1882-83 are excluded at this parish, it may be the wrong volume entirely.

## The "Ler / María / 1884 / folio 13" lead — checked, and it does not resolve

Followed it into the register. **Libro 27 is on DGS 4098790 ("Bautismos 1884-1886"); its printed cover,
*"BAUTISMOS 27 · PARROQUIA DE NTRA. SRA. DEL ROSARIO"*, is at image 4.**

Checked, reading the marginal entry-number/name columns:

| Image | Stamped folio | Entries found |
|---|---|---|
| 10 | 11 | 491 Máxima Villa · 492 (Coran?) Vaz · 493 (Rufina?) · 494 Bernardo Castilla |
| 12 | 13 | **502 Juan Eugenio Lugardi** · 505 Rosa Natalia A. Zurbicki · 509 Francisco Javier Navarro · 510 Juan Bustos |
| 13 | 13v / 14 | 515 Manuel Iglesias · 516 Manuel (Guiscardo?) · 517 María (Cadolat?) · 518 Ludovina Pierra |

**No "Ler" and no matching María on any of them.**

### Why the folios do not line up
The index gives **"Luzardi · Juan Eugenio · 1884 · folio 15"**, and that man is physically
**entry 502 on stamped folio 13**. So the index's folio numbers run roughly **two ahead** of the folios
stamped in the book — but that offset was inferred from a single name and is not reliable, and applying it
(index 13 → stamped 11) did not produce the entry either.

### Verdict
**A weak lead, not resolved.** Either my reading of the index line as "Ler" is wrong, or the index folio
numbering diverges from the stamped foliation more than a constant offset. It is not worth more time
against the far stronger options below.

## The register films, now mapped
`data/rosario-films.tsv` carries the full 71-roll list. Two things stand out:
- ***David's film 4098791 is "Bautismos 1882-1884"*** — precisely the years the index has now cleared.
  Reading its 543 pages would have found nothing. **The index saved that work.**
- **DGS 4531040, Matrimonios 1868-1884** (and 4531039, 1853-1867) would hold **Pablo Armando's parents'
  marriage**, which names **all four of his grandparents**. With four years of baptisms clean, this is now
  the better target than any baptism — and there is a **marriage index, DGS 4531036 (1731-1761,
  1860-1921)**, to find it with.

---

# 8 September 2026 — the MARRIAGE index (DGS 4531036): structure decoded, L section located

**Indice de Matrimonios, 1731-1761 and 1860-1921** — Nuestra Señora del Rosario. **180 images**, against
the baptism index's 718.

## How it is built — different from the baptism index
- **HANDWRITTEN**, not typescript. Faint, and needs more magnification to read.
- **Alphabetical by surname**, and within each surname group **sub-divided by YEAR** (headings seen: 1861,
  1863, 1865, 1888, 1902). Some blocks also carry a **"Libro"** heading (e.g. *Libro X*, 1888).
- Columns run: **[groom's surname + initial] · [bride's surname + initial] · [page number]**.
  So one line gives **both families at once** — which is exactly why this index is worth more than the
  baptism one.

## Where L is
| Image | Letter | Names read |
|---|---|---|
| 72 | **J** | Jurgens · Juary · Juriol · Junguets |
| 78 | (in range) | spouse column: Gonzalez, Orlicho, Sigilio, Leonelo, Saile, Aldave, Ramos, Silva; years **1888**, **1902** |
| 90 | **P** | Pacheco · Palma · Paz · Perez · Peralta · Pereira · Pedemonte · Pujol |

→ ***The L section lies between images ~76 and ~84.*** J is at 72 and P at 90, so L, Ll and M fall in
between; image 78 already shows the right kind of content.

## Viewer mechanics — solved, and worth writing down
- The **`+` zoom button is at the FAR RIGHT of the toolbar (~x 1443 at 1462px wide)**. The icon at ~1297 is
  the **grid** toggle — clicking that is what kept throwing earlier sessions back into thumbnail view.
- **Sequence that works:** type the image number → Return → wait ~10s → click **+ three times** → then
  `computer` **`zoom` with a region**. At three clicks of +, the left page sits about x 400-780 and the
  right page about x 750-1130.
- This index needs **more** magnification than the baptism index, and at that magnification the page is
  wider than the viewport, so the groom's surname column can sit off-screen to the left. **Drag right to
  bring it in before cropping.** That is where this session ran out of road.

## Second attempt, same day — legibility solved, navigation broke
**The legibility problem is SOLVED.** At the viewer's **fit** zoom (not zoomed in), a `computer` **region
zoom** on the left page — roughly `[385,110,660,330]` and `[385,320,660,535]` — renders this handwriting
perfectly. Zooming the *viewer* in was the mistake: it makes the page wider than the viewport and pushes
the groom's surname column off-screen.

Confirmed letter positions on the second pass, read cleanly at fit zoom:

| Image | Letter | Sample |
|---|---|---|
| 49 | **D** | Duarte · Durand · Delavega · Diaz · Dominguez · Duran |
| 59 | **F** | Franco · Fernandez · Fonseca · Fresco · Faya |
| 72 | **J** | Jurgens · Juary · Juriol · Junguets |
| 90 | **P** | Pacheco · Palma · Paz · Perez · Peralta · Pereira |

→ ***L remains bracketed to images ~76-84.***

### The viewer's failure mode, so it is not rediscovered
The Chrome image viewer gets into a stuck state on this film:
1. **URL navigation** (`?i=n`) lands in **thumbnail-grid** mode, and the thumbnails sometimes never load.
2. The **single-page toggle** (icon at ~x 1257) does not open the requested image — it **snaps back to the
   last single-page image viewed** (here, 49).
3. Once stuck, **the "Image [n]" number box stops accepting input** and **the forward/back arrows stop
   advancing**. Only image 49 would render.
4. A **fresh page load / new tab** is what clears it. That is where this session ran out of road.

**Next attempt: open the film in a NEW TAB, go to single-page view FIRST, then use the image-number box
before touching anything else, and read at FIT zoom with region crops.**

## Status
**Not found — the L pages are located but were never rendered.** A viewer bug, not a records problem: the
images are open, unrestricted, and legible at fit zoom with region cropping.

---

# 8 September 2026 — *** THE MARRIAGE INDEX NARROWS TO ONE PAGE ***

Third pass, from a fresh tab. **A much better entry point turned up.**

## The waypoint, not the film
Navigating the ark directly — **`familysearch.org/ark:/61903/3:1:9Q97-Y3S9-MPHL`** — resolves not to the
180-image film but to a **named waypoint**:

> Argentina, Santa Fe, Catholic Church Records › **Rosario** › **Nuestra Señora del Rosario** ›
> ***"Índice de matrimonios 1860-1904"*** — **88 images**

Half the size, and scoped exactly to the period that matters. **Use this, not DGS 4531036's 180-image
listing.**

## *** IMAGE 51 IS THE PAGE ***
Read at moderate zoom:

| Image | Content |
|---|---|
| **51** | **L surnames under year headings 1878 · 1880 · 1881 · 1883** |
| 53 | L surnames under 1898 · 1900 · 1901 · 1902 · 1903 |

**Pablo Armando was born 22 February 1882, so his parents married before that** — and
***image 51 already carries 1878, 1880 and 1881***, with the 1860s and 1870s on the pages just before it.

**The target is image 51 and its immediate neighbours (roughly 49-52) of this 88-image index.**

Surnames legible on image 51 include Luraschi, Lucero, Ludueña, Lopez, Lucas, Lara, Laguna, Lorenzo,
Llanari and many more — the L section proper. **Lerena was not positively identified**, but the page was
never rendered sharply enough to exclude it.

## Why it stopped here — and it is now a tooling limit, plainly
- **Chrome disconnected** mid-task and would not come back. Chrome was the only surface where the
  `computer` **region zoom** works, and region zoom is what makes this handwriting legible.
- The **in-app Browser pane does not support region crop at all** ("region crop not yet supported in the
  Browser pane"), and at ~800px wide its deep-zoom tiles go blurry before the script is readable.

So: **the page is identified, open and unrestricted. It simply could not be rendered sharply in the
surface that remained available.**

## For the next attempt
1. Open **`familysearch.org/ark:/61903/3:1:9Q97-Y3S9-MPHL`** (the 88-image *Índice de matrimonios
   1860-1904*).
2. Go to **image 51**; check 49, 50 and 52 either side.
3. In **Chrome**, read at **fit** zoom using `computer` **region zoom** on quarters of each page — that
   combination rendered the baptism index perfectly.
4. Look for **LERENA** under the year blocks **1860-1881**. The line gives **groom's surname · bride's
   surname · page**, and the page number then opens the register:
   **DGS 4531040 (Matrimonios 1868-1884)** or **4531039 (1853-1867)**.
