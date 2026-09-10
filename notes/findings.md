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

---

# 8 September 2026 — image 51 read, and a much better method found

Chrome reconnected. **Image 51 of the 88-image "Índice de matrimonios 1860-1904" was read** at fit zoom
with region crops.

## What image 51 holds
Pages **150 / 151**, "Libro 8º" and "Libro 9º", under year headings
**1876 · 1877 · 1878 · 1879 · 1880 · 1881 · 1882 · 1883 · 1884 · 1885** — the whole window that matters.
Dozens of L surnames: Luraschi, Lucero, Ludueña, López, Lucas, Lara, Laguna, Lorenzo, Leguizamón,
Lanfranconi, Ledesma, Lavena, Llanari and many more.

### One candidate, and it is NOT confirmed
Under **Libro 9º, 1884**: ***"Larena V · Sarmiento A · 20"***.

At maximum legible resolution I **cannot distinguish `Larena` from `Lavena` or `Lerena`** — and *Lavena*
is a real Rosario surname (a Lavena appears in the baptism index for 1885). **Recorded as a candidate
only.** If it is Lerena, note the date: **1884, two years after Pablo Armando's birth** — which is exactly
the pattern his own son shows (Roque born 1905, parents married 1911).
**To settle it: DGS 4531041 (Matrimonios 1884-1891), Libro 9, folio 20.**

## *** THE METHOD FINDING: THE MARRIAGE REGISTERS ARE INDEXED ***
Opening **DGS 4531041** revealed an **"Image Index" panel beneath the viewer**, tabulating each act with
**Name · Sex · Age · Birth Year · Father's Name · Mother's Name**. Reading the handwriting is
**not necessary** — these registers are searchable.

**This changes the whole approach to Rosario. Search, do not read.**

## What the search returns
- **`surname=Lerena` + Argentina: 6,017 indexed records.**
- **`surname=Lerena` + Santa Fe: 730.**

### *** A SECOND ROSARIO PARISH, WITH LERENAS IN IT ***
> **Carmen Román Lerena** — Baptism **1918**, ***Santa Rosa de Lima, ROSARIO***, Santa Fe.
> Parents: Diego Román and **Manuela Lerena**.

**This is the confirmation that the cathedral is not the only Rosario parish**, and that Lerenas appear at
another one. It is the hypothesis this archive raised after four clean years at Nuestra Señora del Rosario,
and it is now evidenced.

### Other Santa Fe Lerenas
- ***Armando Lerena*** — baptism **1917**, Nuestra Señora del Carmen, **Santa Fe city**. Parents
  **Casimiro Lerena** and **Amelia Lepiani**. *(The same Casimiro also baptised a child at Colón,
  **Entre Ríos**, in 1911 — so that family moved Entre Ríos → Santa Fe.)* **The given name ARMANDO in a
  Santa Fe Lerena family is worth pursuing.**
- **Leon José Lerena** — christening 1892, Cayastá, Garay, Santa Fe. Parents José Lerena, Rosa Eurietto.

### The Montevideo Lerena Lenguas — now documented
- **Ema Sixta Lerena**, christened 1881 at the **Catedral, Montevideo**; parents **Luís Serena Lenguas**
  and **Julia Juanicó**; extended family **Justiniana Lenguas**.
  → *Justiniana Lenguas* is plainly where **Gilberto ***Justiniano*** Lerena ***Lenguas*** of the Argentine
  Stud Book gets his names. <a>The stud-book family is a **Montevideo** family.</a>
- **Gilberto Lerena** m. **Julia Salvañach**, Montevideo — children **Carlos Augusto Federico** (1883) and
  **Raul** (b. 1885, later married at Buenos Aires).
  → And the family's own **Gilberto Lerena (1957-2020)** carries the same name.

## A caution to carry
***There is a Rosario in URUGUAY as well*** (Rosario, Colonia). An 1825 Uruguayan marriage index gives
*Alexandro Lerena, born "Rosario"*, parents Ramon Lerena and Maria Josefa Gonsales. **Do not assume every
"Rosario" in a Lerena record is Rosario, Santa Fe.** Given Uruguay has the world's densest Lerena
population, this is a live trap.

---

# 8 September 2026 — *** THE CATHEDRAL WAS ROSARIO'S ONLY PARISH IN 1882 ***

Searched the indexed church records for a Lerena baptism at **Santa Rosa de Lima, Rosario**. Then checked
when that parish began — and the answer reverses this archive's working assumption.

## The parish history
Published parish and diocesan sources (parroquiasantarosa.com.ar; Conclusión, Aug 2021; Wikipedia
*Iglesia de Santa Rosa (Rosario)*):

> *"Hasta ese momento, en materia eclesiástica, la ciudad de Rosario contaba **solamente con la Iglesia
> Catedral**."*
> A chapel stood on land given by Ramón Sánchez from **1863**, passing to the bishopric in 1866. But
> *"recién el **19 de febrero de 1888** se obtiene el título oficial de parroquia. Se celebró ese día la
> inauguración, **juntamente con el primer bautismo**."*

**Santa Rosa de Lima became a parish on 19 February 1888, and its first baptism was performed that day.**
Rosario's other parishes — San José, Inmaculada Concepción — are later still; they appear in the indexed
records only from the 1910s.

## *** WHAT THIS MEANS ***
In **February 1882, Nuestra Señora del Rosario — the cathedral — was the ONLY parish in Rosario.**

This archive has now read that cathedral's baptism index **line by line for 1882, 1883, 1884 and 1885**,
plus the whole **Ll-** section for 1880-84, and found **no Lerena and no Llerena**.

Those two facts together give a far stronger conclusion than "he was probably baptised at another parish":

> ***PABLO ARMANDO LERENA WAS NOT BAPTISED IN ROSARIO IN 1882-1885 — because there was nowhere else in
> Rosario to be baptised.***

The "other Rosario parish" hypothesis, raised earlier today, is **closed**. It was a reasonable idea and it
is wrong for these years.

## Which leaves four live possibilities
1. **A late baptism, after 1885.** Still open — the index runs to 1900 and only 1882-85 has been read.
   The family's own habit supports it: his son Roque was born 1905 and baptised **1911**.
2. **He was baptised in another town.** Born at Rosario but christened where the family had come from, or
   where they moved to.
3. ***He was not born at Rosario at all.*** The passport is his own document and says *"Rosario de Santa
   Fe"* explicitly — but a man states where his family is from as readily as where he was delivered.
   **And there is a Rosario in URUGUAY (Colonia)**, in the country with the world's densest Lerena
   population. The passport's "de Santa Fe" argues against it; it is not conclusive.
4. **The date is inexact.** Least likely — the passport gives a precise day, 22 February 1882.

**Priority 1 is now the cheapest test**: read the same cathedral index for **1886-1900**.

## Also found in the Rosario search
- **Only ONE genuine Lerena** appears in the indexed Rosario church records at all:
  **Carmen Román Lerena**, baptised **1918** at Santa Rosa de Lima, mother **Manuela Lerena**.
- **Bartolomé LLERENA**, in the **1869 National Census at Rosario**, born **1824 in Córdoba**. A *Llerena*
  household at Rosario a decade before Pablo Armando.
- Several **LLORENS** families at Rosario parishes (Santa Rosa de Lima, San José, Inmaculada Concepción) —
  Vicente Llorens m. Rosa Noce 1914; Antonio Llorens and María Roqué's daughters married 1917 and 1919.
  **Relevant to the unproven Llorens hypothesis**: Llorens are demonstrably a Rosario family, which is
  presumably why the 1872 San Miguel baptism looked plausible. It remains unproven and Buenos Aires-based.
- The search is heavily fuzzy — *Lorena, Loroña, Llorens, Lorens, Llerena, Loranse* all return. Filter hard.

---

# 8 September 2026 — 1886-1895 read. Still nothing.

First checked whether these years were already indexed and could be searched instead: a control search
(`Lopez`, Rosario, births 1888-1892) returned **0 results**. **The cathedral's 19th-century baptisms are NOT
indexed** — only the 1910s material is. So they had to be read.

## Coverage now
Read at fit zoom with region crops in Chrome, images **377-393** of DGS 4530325 (plus 369-376 earlier):

**LIBROS 24 THROUGH 38. YEARS 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893,
1894 and 1895.** Full table in `data/rosario-index-searched.tsv`.

### *** NO LERENA. FOURTEEN CONSECUTIVE YEARS. ***
Nor any Llerena — that section was read separately for 1880-84.

The L pages are dense with Rosario's actual L families, the same names recurring year on year: López,
Lucero, Ludueña, Leguizamón, Luraschi, Lencina, Ledesma, Leiva, Lescano, Lujan, Luque, Lanfranconi,
Lombardo, Lavena, Larrechea. **Lerena is simply not among them.**

## Two small gaps, stated
- **Image 392** (part of 1894) was not opened.
- On **images 387 and 389** the lower half of each page rendered blurred — the deep-zoom tiles did not
  load. Those portions were not read.
- **1896-1900 (images ~394-403) remains unread.**

Neither gap is likely to matter: a baptism at age 12-18 is improbable, and the run is otherwise unbroken.

## What this now means
Combined with the parish finding — that **the cathedral was Rosario's ONLY parish until 1888** — the
position is:

> **From his birth in February 1882 until he was thirteen, Pablo Armando Lerena does not appear in the
> baptismal index of the only church in Rosario that could have baptised him for the first six of those
> years, nor in any of the seven years after Santa Rosa de Lima opened.**

**The Rosario baptism should now be treated as unlikely to exist**, and effort moved to:
1. ***Whether he was born at Rosario at all.*** His passport says so, and it is his own document — but the
   record does not corroborate it. **Remember there is a Rosario in Uruguay (Colonia)**, in the country
   with the world's densest Lerena population.
2. **The Uruguayan records.** Montevideo's Lerenas are numerous, documented, and already surfacing in
   searches (the Lerena Lenguas; Pedro A. Lerena; Alberto Lerena; Gilberto Lerena).
3. **Argentine civil registration** rather than church records.
4. **His marriage or death papers in South Africa** for a stated birthplace — the 1950 death certificate
   says only "South America".

---

# 8 September 2026 — Uruguay searched. He is not there either.

## The search
FamilySearch historical records, **fuzzy** on both names (`Pablo~ Lerena~`), **births 1878-1886**,
**worldwide** (a Uruguay-only filter with a date range returned 0, so the filter was dropped and the whole
index searched instead).

### Result: only TWO records exist in the world for this man
1. **South Africa, Civil Marriage Records** — the 1911 Wynberg marriage. *(known)*
2. **Find a Grave Index** — b. 22 Feb 1882, d. 19 Mar 1950, burial place not stated. *(known; the memorial
   itself is unopened and may carry a cemetery and a headstone photograph — worth a look)*

**Nothing from Uruguay. Nothing from Argentina. Nothing from South America at all.**

Every other Pablo Lerena in that window is demonstrably someone else — **Pablo Timoteo Lerena Muñoz** of
Atienza, Guadalajara (Spain, b.1878, parents Pedro Lerena Pérez and Baltasara Muñoz Bermejos), and a scatter
of Mexican, Colombian, Guatemalan and Philippine men.

## Where that leaves it
The largest genealogical index in the world holds **no South American record of Pablo Armando Lerena**.
Taken with fourteen clean years of Rosario baptisms, the position is now:

> **His South American origin rests entirely on his own passport.** No register, index or civil record on
> that continent has yet been found to corroborate it.

That is not a reason to doubt the passport — it is his own document, sworn at a consulate, giving a city, a
province and a day. It is a reason to accept that **the corroborating record may simply not be digitised**:
Uruguayan and Argentine coverage on FamilySearch is patchy, and Rosario's civil registration is not indexed
at all for the 1880s.

## *** THE CARMEN QUESTION *** (raised by David)
> *"my aunt was Patricia Carmen Lerena. would Carmen not be related?"*

A fair question, and it repays a careful answer rather than a quick one.

**Against reading much into it:** *Carmen* is one of the commonest female names in the Spanish-speaking
world — a devotional name from *Nuestra Señora del Carmen*, Our Lady of Mount Carmel. On its own it points
at no particular ancestor, and this family was Catholic, so a devotional choice needs no explanation.

**But there is something in it.** Look at the given names this family actually used in South Africa:

| Male | Female |
|---|---|
| Pablo Armando · Roque Luis Armando · Ricardo Juan Carlos · Nuno Fernando · Roberto Juan Roque · Ricardo Paul · Anton Armando · Juan Carlos · Gilberto | Yvonne Paulette · **Patricia Carmen** · Panola Maria · Juanita Ramond · Catherine Tersia |

The **male** Spanish names are abundant and persistent. The **female** ones are scarce — and *Carmen*, in
1958, is the clearest survival among them.

Spanish naming custom names children for grandparents. **Patricia Carmen's** grandmothers were
**Mary Septima Taylor** (English, d. 1935) and the mother of **Catherine Mary Sophia Booyzen** (Afrikaner).
**Neither was a Carmen.** So if the name descends rather than being freshly chosen, its likeliest source is
**further back on the Lerena side — Pablo Armando's own mother or grandmother.**

**HYPOTHESIS, recorded as such:** *a Carmen stands somewhere in Pablo Armando Lerena's own maternal line.*
Weak on its own; useful as a filter. **When searching Argentine and Uruguayan Lerena records, give extra
weight to any household containing a Carmen.**

---

# 8 September 2026 — THE 1895 NATIONAL CENSUS: a Lerena household, and it is the stud-book family

Searched the **Argentine National Census of 1895** (indexed and searchable) for the surname.
Full table: `data/census-1895-lerena.tsv`.

## A whole household in Buenos Aires — Sección 21, Subdivisión 15
| Name | Age | Born | Where |
|---|---:|---:|---|
| **Gilberto Lerena** (head, married) | 41 | 1854 | **Uruguay** |
| Maria E. C. | 26 | 1869 | Uruguay |
| Maria Luisa | 15 | 1880 | Uruguay |
| **Carlos A.** | 11 | 1884 | Uruguay |
| **Raul A.** | 9 | 1886 | Uruguay |
| Maria A. | 8 | 1887 | Uruguay |
| Maria C. | 6 | 1889 | **Buenos Aires** |
| Maria E. | 5 | 1890 | Buenos Aires |
| Luis F. | 2 | 1893 | Buenos Aires |
| *Josefa Lerena De L.* (widow, same subdivision) | 43 | 1852 | Uruguay |

### This is Gilberto Justiniano Lerena Lenguas
The Uruguayan records already found give **Gilberto Lerena m. Julia Salvañach**, with sons
**Carlos Augusto Federico** (b. 9 Jul 1883, Montevideo) and **Raul** (b. 1885, Montevideo). Here they are
in Buenos Aires in 1895 as *Carlos A., 11, b. Uruguay* and *Raul A., 9, b. Uruguay*.

→ **The co-founder of the Argentine Stud Book was a Uruguayan**, born 1854 — which fits a Group 1 race
being renamed in his honour in **1914**, at or just after his death, aged about sixty.
→ **The birthplaces date the family's move.** Uruguay through 1887; Buenos Aires from 1889.
**They crossed the Plate between 1887 and 1889.**

## *** AND A THIRD NEGATIVE FOR ROSARIO ***
- **No Lerena appears in Santa Fe or Rosario in the 1895 census at all.**
- **No Pablo Armando Lerena appears anywhere in it**, though he would have been thirteen.

The Lerenas the census does show are: this **Uruguayan** household in Buenos Aires; a separate
**Spanish-born** family (Leandro, b.1857 Spain) in another Buenos Aires section; two in **Tucumán**; one in
**Entre Ríos** (b. Uruguay); and an Italian-born Lola on Isla Martín García.

So three independent bodies of evidence now decline to place this family at Rosario — fourteen years of
cathedral baptisms, the whole FamilySearch index, and now the national census — while **Uruguay keeps
answering**.

## The Gilberto echo, and what it might mean
David's family named a son **Gilberto Lerena (1957-2020)**. The stud-book Gilberto is now a documented man
with a documented household. **A South African family of Argentine horsemen naming a son Gilberto is a
thread worth pulling** — either they were kin, or they knew perfectly well who he was.
<span>Recorded as a question, not a claim.</span>

---

# 8 September 2026 — why Rosario has no second source, and where the ships come in

## *** THE STRUCTURAL FACT ***
**Argentine civil registration only began around 1886** (provinces vary, 1886–1900). Before that,
*"los registros parroquiales constituyen la fuente principal y, en muchos casos, la única disponible."*

→ **For a birth at Rosario in February 1882 the parish register is the ONLY possible record.**
→ This archive has read that parish's baptism index **line by line for 1882–1895** and he is not in it.
→ **There is no civil fallback to go to.** That is not a gap in our searching; it is the shape of the
   Argentine record system.

So the choice narrows hard: either he was **baptised somewhere other than Rosario**, or he was **not born
at Rosario**.

## Military records are NOT the easy route
Checked: a FamilySearch search of **indexed military records for the surname Lerena returns ZERO**. The
Argentine army collection is not indexed for this name. The *libreta de enrolamiento* — still the single
document most likely to name his parents — has to be requested by **email from the Archivo General del
Ejército**. Draft letter (in Spanish) written: `requests/argentina-army-enrolment.md`.

## CEMLA is gated
The immigrant-arrivals database at `cemla.com/buscador/` is free and would find **his parents arriving**,
but the form is behind a **CAPTCHA**, which this archive's researcher will not complete. **David must run
it**; the exact five searches and the fields to record are set out in `requests/cemla-ship-search.md`.

## *** SHIPS: the assumption worth dropping ***
We have been looking for a **passenger**. He may never have been one.

The South African War shipped ~**360,000 horses** into the country, **Argentina among the main sources**.
Pablo Armando was **17 when it began and 20 when it ended**, a horseman, and a *horse-dealer* at the Cape
by 1911. Horses travel with **conductors, grooms and muleteers**, engaged at the port of loading — and
those men are written down in **military remount paperwork, not civilian passenger lists**.

**That would explain why he is invisible in the passenger indexes.**

Where to look — none of it tried:
- **The National Archives, Kew** — Remount Department, **WO 108** and related WO series: overseas
  purchasing commissions, shipping returns, depot registers.
- The Cape remount depots, chiefly **Stellenbosch**.
- British purchasing-commission correspondence at Buenos Aires.

Written up as `requests/ships-and-the-remount-trade.md`. **This is the largest untried idea in the project
and it fits every fact held about him.**

---

# 8 September 2026 (night) — four new records, and a theory worth testing

## New, from a South-Africa-filtered surname search (412 hits)
1. ***LDS Church Census, South African Mission, 1935.*** Two entries:
   **Nuno Fernando Lerena**, b. 1924 *"Wyneberg C.P."*, and **Ricardo Juan Carlos Lerena**, b. 1920
   *"Cleremont C.P."* — **both indexed as "Son", so a HEAD OF HOUSEHOLD exists on that page.**
   That head should be **Pablo Armando**, stating his own birthplace in **1935 — five years before the
   passport, and independent of it.**
   **The image is not available** ("Check Image Availability" yields nothing). Neither Pablo Armando,
   Mary Septima nor Roque is separately indexed. *Why two Catholic boys of 11 and 15 appear in a Mormon
   mission census in the year their mother died is itself a question.*
   Arks: `1:1:ZYWT-S8N2` (Nuno), `1:1:ZYWT-S86Z` (Ricardo).
2. ***"Luis Roque Armando Lerena" m. "Rosaline Wilhermina FORBES CHAPPELL", 21 September 1936,
   Potchefstroom*** (South Africa, Civil Marriage Records). **Both surnames in one entry** — a third
   independent confirmation that Forbes and Chappell are the same woman, exactly as inferred.
   *(Note: the civil entry says Potchefstroom; the Corpus Christi annotation said St Joseph's,
   Johannesburg. Registration district vs church, presumably.)*
3. ***An infant Lerena died at BLOEMFONTEIN, 22 May 1932***, father **Louis Lerena** (Orange Free State
   Civil Death Registration). This is the "Unknown Lerena, 17–22 May 1932" of David's tree — and it puts
   Roque in the **Orange Free State** in 1932, a place this archive had not placed him.
4. **Careen Maria Lerena**, burial Cape, d. 27 June 1947; **Doreen May Lerena** b.1921; **Rhena May
   Lerena** b.1913 d. 1 Apr 1998 — all consistent with the tree.

## Tested and negative
- **No "Pablo Armando" born 1880–1884 anywhere in indexed Argentine records, under ANY surname.**
  (The 1880s Rosario registers are unindexed, so this is not decisive — but it is worth knowing.)
- **No Cape birth registrations** for the three sons are indexed.
- **FamilySearch indexed military records: zero Lerena.**

## *** THE THEORY THAT DESERVES TESTING: he may not be indexed under Lerena at all ***
This family's documented practice was to have children first and marry later. **Roque was born in November
1905 and his parents did not marry until September 1911** — the register calls them bachelor and spinster.
The child was baptised in June 1911, three months before the wedding, and the mother received into the
church that December. The whole family was regularised in one year.

**In Spanish civil and parish practice a child born outside marriage is commonly registered under the
MOTHER'S surname.** If Pablo Armando was himself born that way — and the habit evidently ran in the
family — then:

- he would be **born at Rosario exactly as his passport says**, and
- he would **not appear in the baptism index under Lerena**,

which is precisely the pattern the evidence shows. Note too that his passport gives **one** surname where
Spanish practice normally gives two.

**And David's own tree already gestures at this.** It carries **Roberto Llorens** (b. 1850) and
**Francisca Fernández *Lerena*** (b. c.1850) as Pablo Armando's presumed parents — i.e. a **Lerena
mother** and a **Llorens father**. David flags the San Miguel 1872 baptism behind it as unproven, and it
stays in `sources/unproven/`. But the *shape* of his hypothesis — mother Lerena, father something else —
is exactly what an illegitimate birth would produce, and it would also explain why **Roberto** and
**Roque** recur in this family (a **Roberto Juan Roque Lerena** was born in 1944).

**Recorded as a hypothesis, not a finding.** What would test it:
- the **F section** of the Rosario baptism index for 1882, for a *Fernández*;
- any Rosario baptism of a **"Pablo Armando"** in 1882 under any surname (the index is by surname, so this
  means reading 1882 across every letter — expensive but finite);
- and, decisively, **his enrolment record or the consular file**, which would name the parents outright.

## *** THE ARMY LETTER IS SENT — 8 September 2026 ***
At David's explicit request, the Spanish letter went to the **Archivo General del Ejército**,
**`age@ejercito.mil.ar`** — an address verified from **argentina.gob.ar**, the Ministry of Defence's own
archive directory (Defensa 628/630, Buenos Aires; +54 11 4342-0196; Mon–Fri 08:00–13:00 ART; they offer
*referencia a distancia* by email).

Sent from David's own Gmail so the reply reaches him. Message id `1a0811e9ee49a43e`. It asks for four
things — whether the legajo survives, **the names of his parents**, the Distrito Militar of enrolment, and
the cost of a copy — and sets out why: the parish index read 1882–1895, the cathedral being Rosario's only
parish until 1888, his absence from the 1895 census, and the non-existence of a provincial civil registry
in 1882.

**CEMLA was NOT run.** Its search form is behind a **CAPTCHA**, and this archive's researcher does not
complete those. It remains a five-minute job for David; the five exact searches are in
`requests/cemla-ship-search.md`.

## Progress on route 5 (reading 1882 across the letters)
Located the sections of the baptism index **DGS 4530325**: **D at image ~201** (1889–90),
**F at image ~255** (1890), **L at 369–403**. So **F for 1882 lies earlier, around images 240–248** —
that is where to start looking for a *Fernández* child called Pablo Armando. Not yet read.

---

# 8 September 2026 (late) — route 5 begun: reading 1882 across the letters

**Purpose:** to test the theory that Pablo Armando is in the Rosario baptism index but **not under Lerena** —
because a child born outside marriage was commonly registered under the **mother's surname**, and this
family's documented habit was children first, marriage later.

**Method (proven and fast):** in Chrome, `familysearch.org/search/film/004530325`, switch to single-image
view, type the image number in the box, then `computer` **region zoom** on `[210,105,620,720]` (left page)
and `[580,105,1025,720]` (right page). One call per image. Look down the **NOMBRES** column for
*Pablo Armando* or *Pablo*.

## Covered so far
| Letter | 1882 images | Result |
|---|---|---|
| **F** | 239 (right), 240 | ***READ IN FULL — no Pablo Armando.*** One curiosity: **"Funes · Armando · 1882 · folio 163"** — an *Armando*, but the wrong surname and not *Pablo* Armando. |
| **C** | 118 (folios 95–244) | Read — no Pablo. **Folios 1–94 on image 117 still to read.** |
| **L** | 369–371 | Already read — no Lerena. (1883–1895 also read.) |
| **Ll** | 404 | Already read — no Llerena; the whole 1880–84 Ll section is seven entries. |

**→ The Fernández hypothesis fails.** There is no Pablo Armando under F in 1882.

## The map, for resuming
Sampled positions, so the 1882 band of each letter can be found quickly:
**C ≈ 120 (1883) · D ≈ 201 (1889–90) · F ≈ 255 (1890) · G ≈ 320 (1894) · L 369–403 · Ll 404–406.**
Because each letter's section runs chronologically, **1882 always sits early in its letter's band**.
Full grid: `data/rosario-index-map.tsv`.

## Honest status
**Three letters of twenty-six.** Completing the sweep is a defined, finite job — roughly 40–60 more image
reads, one call each — and it would answer conclusively whether he was baptised at Rosario in 1882 under
*any* surname. It has not been done, and this note says so rather than implying more coverage than exists.

## Sweep progress — 9 letters of ~26 done

**A · B · C · D · E · F · L · Ll complete for 1882; G partial.** No Pablo Armando in any of them.
Coverage grid: `data/rosario-index-map.tsv`.

### Two things learned that make the rest faster
1. ***The index flags illegitimacy.*** Entries carry **"(N.)"** — *natural*, i.e. born out of wedlock —
   e.g. *"Eduardo · Paul (N.) · 1882 · f.505"*. **So if Pablo Armando was born outside marriage and
   registered under his mother's surname, his entry should carry that mark.** That is a second thing to
   scan for, not just the given name.
2. ***"Expósito" is a surname in this index*** — the name given to foundlings. It sits in the E section and
   there are many of them. **If he was abandoned or of unknown father he could be an Expósito**, and the E
   section for 1882 has now been read with no Pablo Armando among them.

### Near misses, recorded so they are not re-chased
- **"Chaparro · Pablo H." 1882 f.67** — a Pablo, wrong second initial and surname.
- **"Funes · Armando" 1882 f.163** — an Armando, wrong given name and surname.
- **"Eduardo · Paul (N.)" 1882 f.505** — a Paul, flagged illegitimate, wrong surname.
- **"Gorosito · Pablo" 1881 f.71** — a Pablo, wrong year and surname.

**None is him.** But the fact that all four exist shows the sweep is sensitive enough to catch the name if
it is there.

### What remains
**G (tail) · H · I/J/K · M · N/O · P · Q/R · S · T/U/V · W–Z.** Roughly **25–35 more image reads**.
Rough positions: G runs to ~330, so **H starts ~331**; **L starts 369**; **M starts ~407**.

## Sweep progress, second sitting — TWELVE letters complete

**A · B · C · D · E · F · G · H · L · Ll** are now read in full for 1882. **No Pablo Armando in any of them.**
**I** is located but its 1882 band (images ~346–347) is not yet read.

### Letter positions now firmly established
**A** 11–12 · **B** 56–57 · **C** 117–118 · **D** 190 · **E** 223 · **F** 239–240 · **G** 280–283 ·
**H** 337 · **I** ~346–347 · **L** 369–371 · **Ll** 404 · **M** from ~407.
(Useful bracketing samples: C at 120=1883 and 181=1898; D at 216=1901; E at 224=1884; G at 320=1894 and
334=1900; H at 344=1895; I at 351=1888 and 353=1893.)

### Near misses now numbering six — all excluded
*Chaparro · Pablo H.* (1882 f.67) · *Funes · Armando* (1882 f.163) · *Eduardo · Paul (N.)* (1882 f.505) ·
*Gorosito · Pablo* (1881 f.71) · a *Pablo J.* in G (1882 f.568) · a *Pablo* in I (1884 f.141).
**None is Pablo Armando** — but six near hits confirm the method catches the name when it is present.

### Remaining
**I (finish) · J/K · M · N/O · P · Q/R · S · T/U/V · W–Z** — perhaps **15–25 more image reads**.
**P** and **S** are the big ones and should be done first if the sweep is ever cut short.

### A note on conditions
Chrome dropped its connection twice during this sitting and the viewer sometimes renders one image behind
the number requested. Neither loses data — it only costs re-reads — but it is why progress is recorded
after each letter rather than at the end.

## THE 1882 SWEEP IS COMPLETE — all 26 letter sections read

**Every letter section of the Rosario cathedral baptism index (DGS 4530325) has now been read for the
year 1882, looking for the given name *Pablo Armando* under any surname whatsoever.**

**Result: he is not there.**

A · B · C · D · E · F · G · H · I · J · K · L · Ll · M · N · O · P · Q · R · S · T · U · V · W · Y · Z —
twenty-six headings, plus the finding that **there is no X section at all** in this index. Two sections
turned out to contain no 1882 entries at all (**K**, which jumps from Libro 24/1881 straight to
Libro 26/1883, and **Y**, whose entire section is a single line for 1900). Full image-by-image coverage
in `data/rosario-index-map.tsv`.

### The last eleven sections, for the record
- **P** (images 503–505) — 1882 runs Libro 24 f.367 → Libro 25 f.257. Clear.
- **Q** (548–549) — a short letter, both books read. Clear.
- **R** (563–565) — Libro 24 f.363 → Libro 25 f.239. Clear.
- **S** (612–614) — Libro 24 f.368 → Libro 25 f.248. Clear.
- **T** (654) — the whole 1882 band on one opening. Clear.
- **U** (678) — eight entries in total for 1882. Clear.
- **V** (684–685) — Libro 24 f.371 → Libro 25 f.246. Clear.
- **W** (705) — exactly one 1882 entry in the whole letter. Clear.
- **X** — no section exists.
- **Y** (707) — one entry, 1900. No 1882.
- **Z** (708) — Libro 24 f.330 → Libro 25 f.246, one opening. Clear.

### Near misses, now eleven, every one excluded
*Chaparro · Pablo H.* (f.67) · *Funes · Armando* (f.163) · *Eduardo · Paul (N.)* (f.505) ·
*Gorosito · Pablo* (1881 f.71) · *Pablo J.* in G (f.568) · *Pablo* in I (1884 f.141) ·
*Pablo Eduardo* in O (f.555) · surname-only *Pablo · (N.)* in P (Libro 25 f.83) ·
*Quevedo · Juan B. Pablo* (f.427) · **_Ronillon · Armando Juan_ (Libro 24 f.498)** ·
*Villarreal · Pablo del R.* (f.559) · *Suárez? · Pedro Pablo* in S (Libro 25 f.237).

*Ronillon · Armando Juan* is the closest the sweep came in 718 images. It is not him: wrong given name
order, wrong surname, and nothing else about the family attaches to it.

**Eleven near hits prove the method is sensitive.** If a *Pablo Armando* had been baptised at the
cathedral in 1882 under any surname, this sweep would have caught it.

### What this negative actually proves — and what it does not
It **rules out one specific thing**: baptism at the **Iglesia Matriz / Catedral de Rosario in the calendar
year 1882** under the given name *Pablo Armando*. Since the cathedral was the **only parish in Rosario
until 1888**, and civil registration in Santa Fe did not begin until about 1886, this was the single most
likely record of his birth. It is not there.

It **does not** rule out:
1. **A different given name at baptism.** He was "Robert Paul" in South Africa and "Pablo Armando" on the
   passport. If he was baptised, say, *Juan Pablo* or *Pablo* alone, or under a name later dropped, the
   sweep would not flag him — I searched for the pair. *(The near-miss list is the partial answer to this:
   every 1882 entry containing "Pablo" or "Armando" is recorded above, and none fits.)*
2. **A different year.** 22 Feb 1882 is the passport date; a baptism could sit in late 1881 or 1883 if the
   birth date on the passport was wrong or approximate.
3. **A different place.** Born elsewhere in Santa Fe province, or in Buenos Aires, Uruguay, or Spain, and
   only later associated with Rosario.
4. **Never baptised, or baptised privately** and never entered in this index.

**Point 2 is now the cheapest next test** — the same index, the same method, one year either side. The
letter positions are all mapped, so 1881 and 1883 would cost far less than 1882 did.

### Method note
Per image: set the image number, wait, then read the two page-halves. Coverage checkpointed to the grid
after each letter. The sweep took three sittings and roughly 120 image reads across a 718-image film.

## CEMLA run in full — 9 September 2026

All four spellings searched at `cemla.com/buscador/`, forename blank, range left at the form's default of
**1800/01/01 – 1960/12/31**. David completed the CAPTCHAs; the searches were otherwise driven from here.

| Spelling | Results | Earliest arrival |
|---|---|---|
| LERENA | ~31 rows (with duplicates) | **1907** |
| LLERENA | **27** | **1910** |
| LARENA | **6** | **1905** |
| LERINA | **4** | 1889 — one wholly Italian household, a different surname |

### The decisive finding is negative
**The earliest arrival of a Lerena, Llerena or Larena is 1905.** Pablo Armando was born at Rosario in
February 1882. **His parents cannot be in this index.** They were in Argentina before the record becomes
useful. Route closed, and closed cleanly rather than left hanging.

### What it did give us
1. ***Gilberto LERENA, ARGENTINE national, aged 49 on arrival 27 Feb 1928*** (ship CAP. NORTE), travelling
   with **Gilberto Lerena, 12, student**, also Argentine. Born about **1879 — within three years of Pablo
   Armando**, and carrying the given name of **Gilberto Justiniano Lerena Lenguas**, the Uruguayan-born
   co-founder of the **Argentine Stud Book** who headed a Buenos Aires household at the 1895 census. He is
   **not** among the children listed in that 1895 household. This is now the strongest lead in the
   Argentine work: a Lerena of the right generation, the right nationality, and — through the name — the
   right *trade*, given that the family story is about horses.
2. **Carlos LERENA, Uruguayan, b. c.1885**, arriving from **Montevideo** on 27 May 1926 with **Rosa M. E.
   Lerena, Argentine, b. c.1887** — evidently his wife. The Uruguay thread again, and again unresolved.
3. **Josefina LLERENA**, Argentine *propietaria* born about 1868, crossing in 1918, 1926 and 1931, single
   throughout.
4. **Paolo LERENA**, Italian, b. c.1891 — the only Pablo/Paolo of the surname anywhere in the index, and
   far too late to be ours.
5. Spanish bearers cluster hard on **Logroño, La Rioja** — corroborating the Forebears distribution work
   independently.

### A register, at David's suggestion
He asked whether all these variant Lerenas should be kept and marked unrelated-for-now, with their
provenance. Yes — and it is now `data/lerena-register.tsv`, published at `/register/`. **Seventy people**,
each with the record that produced them and one of three marks: **Connected**, **Excluded**, **Unplaced**.
Nothing is claimed as kin. Given that Forebears counts only ~2,124 Lerenas worldwide, most bearers probably
*are* related at some depth — but "probably" is not evidence, and the page says so. When Pablo Armando's
parents are finally named, this is the list that should snap into place.

## Sweep of 1881 and 1883 — begun

The 1882 year is closed. The passport's 22 February 1882 is the only authority for that year, and a birth
date written on a document issued fifty-eight years after the fact is not sacred — so the same sweep is now
running across the two neighbouring years. **A, B and C are complete for both 1881 and 1883. No Pablo
Armando in any of the six bands.** Coverage in `data/rosario-index-1881-1883.tsv`.

### A warning about image numbers, recorded so it does not bite anyone later
Part-way through, the viewer switched from presenting the film as **718 images** ("Film # 004530325") to
**655 images** (the waypoint "Índice de bautismos 1879-1900"). **The offset between the two numbering
systems is not constant** — a page that is image 55 in the 718 view is image 52 in the 655 view, but near
the end of the alphabet the two diverge by about 56. So image numbers in this project are **locators only,
never evidence**. Every page is verified on arrival by its letter, year, Libro and folio range, and those
are what the coverage files actually record. The 1882 grid is in 718-view numbers; the 1881/1883 grid is in
655-view numbers, and each file says so.

### Near misses so far in the new years
*Alberdi · Adelino Pablo* (1881, Libro 23 f.649) · *Basualdo · Felix Pablo* (1881, Libro 24 f.355) ·
*Carara · Pablo* (1881, Libro 24 f.146) · *Ahumada · Pedro Pablo* (1883, f.543). None is him.

## *** A new lead from the family: he fled Argentina in political trouble ***

David reports a story his mother repeated to him on 8 September 2026 — carried in the family, never proven
— that **Pablo Armando "ran away from Argentina as he was a communist on the run."**

Written up in full at `notes/communist-story.md` and published as hypothesis 6. The short of it:

- It is the **only family story that explains a departure**. Every other thing the family remembers says
  what he *was*; this alone says why he *left* — and a reason to leave is exactly what the record has
  refused to give us.
- **"Communist" is almost certainly a later relabel.** The Argentine Communist Party dates from 1918; he
  left around **1903–05**, when the Argentine radical movement was **anarchist and anarcho-syndicalist**.
- The mechanism that would make it true is **Ley 4144, the *Ley de Residencia*** (Nov 1902) — deportation
  of foreign-born agitators without trial, used heavily in exactly those years. **Rosario**, a great river
  port and rail head, was among the most militant anarchist cities in Argentina.
- ***The Ley de Residencia applied to foreigners.*** An Argentine national could be prosecuted but not
  deported under it. **So if he was expelled, he was not Argentine-born** — and the failure to find him in
  the Rosario baptism index stops being a puzzle and becomes a consequence. That would sit with the
  Uruguayan density of the surname, the Uruguayan-born Lerenas in the 1895 census, the Uruguayan Carlos
  Lerena in the CEMLA arrivals, and the family note that the consulship may have been Uruguayan.
- Untried archives it points at: **Ministerio del Interior expulsion files** at the Archivo General de la
  Nación; **Santa Fe / Rosario police records 1902–05**; the anarchist press, chiefly ***La Protesta***,
  much of it at the **International Institute of Social History**, Amsterdam.

## findmypast, 9 September 2026 — the best day this project has had

David took a trial subscription and opened it to the archive. Full transcripts read; nothing purchased
beyond the trial. Four findings, in order of importance.

### 1. *** Pablo Armando's Argentine nationality is now corroborated from outside the family ***
Two British passenger manifests, twenty-six years apart, record **Mary Septima's** declared nationality:

- **19 Feb 1909**, SS *Guelph*, Cape Town to Southampton — **English**
- **20 May 1935**, RMS *Balmoral Castle*, Cape Town to Southampton — **"Agentine"** *(Argentine)*

She was born and baptised at Northam, Devon. Under the law of the period **a British woman who married a
foreign national took his nationality**. They married in **September 1911** — between the two voyages.
English before, Argentine after. **The only thing that can have made a Devon woman Argentine is the
nationality of the man she married**, and a ship's purser in 1935 wrote it down with no interest in this
family. Full argument in `notes/nationality-chain.md`. It does not settle where he was *born*.

### 2. *** She was "Mrs Lerena" in 1909, with a child, two years before the marriage ***
The 1909 manifest lists on **consecutive lines**: line 17 **Mrs M T Lerena**, English; line 18
**Mast. L Lerena**, male, British Colonial. *Mast.* is Master — a boy. **Roque Luis Armando was born at
Cape Town on 25 Nov 1905**, so he was three, and his father's estate calls him "**LOUIS** Lerena, major
son". So Mary Septima was travelling to England as Mrs Lerena with their small son in February 1909.
The 1911 marriage regularised a household that already existed — **exactly the pattern already documented**
for Roque himself, and the basis of the mother's-surname theory.

### 3. She went home to her sister to die
**Arrived Southampton 20 May 1935** on the *Balmoral Castle*, occupation *housewife*, age 50, address in
Britain **"C/O DALLING, FORE ST, NORTHAM, DEVON"**. Her elder sister **Isabella Temple "Edie" Taylor
married a DALLING** — already in David's tree, now joined to a document. She sailed home from Southampton
on the **Armadale Castle on 28 June 1935**, a five-week visit, and **died on 15 November 1935**.

### 4. An Argentine diplomat named Lerena
**Carlos Gustavo Lerena**, b. 20 Jan 1915, **Argentine**, occupation **DIPLOMATIC**, arrived London
17 Nov 1958 from La Plata en route to a posting in **Iran**, with his wife and children — one of whom is
**Carlos Gilberto**. Does not prove the Consul General tradition and is not our man, but it establishes
that Lerenas really did serve in Argentine diplomacy, and it is the **third** independent appearance of
the Carlos-and-Gilberto pairing. Written up in `notes/an-argentine-diplomat-named-lerena.md`.

### Also established
- **Only eight Lerenas ever arrived in Britain**, and **only two ever left**. **Pablo Armando is not among
  them** — he never entered Britain under that surname.
- **Juanita Ramona Lerena**, b. **16 June 1937**, Roque's daughter, arrived Southampton 12 Apr 1957,
  **ballet teacher**, to **"Vicosa, Westward Ho, N Devon"** — the village adjoining Northam. She went to
  the Taylor country, and married at Portsmouth in 1961, becoming Hutson.
- **Mary Septima's baptism**: 30 October 1884, Northam, father William, mother Mary Ann Ellen —
  archive ref 1843A/PR/1/16, South West Heritage Trust. *A citation for what the tree already held, not a
  new fact; recorded here because this archive cites its sources.*
- **A newspaper trace**: the *Western Times* and *North Devon Herald* both print
  "**Mary Septima Taylor, 16, Northam**" in what reads as a scholarship or pupil-teacher list, c.1900-01.
  Not yet opened — the newspaper search path defeated me and should be retried.

### The newspaper search, retried and cracked
The path is `/search-newspapers/results?names=...`, and the page image hides its OCR behind an **Articles**
button. Two 1901 articles are ours; the rest of the "Septima Taylor" hits are 1960s racing cards for a
horse called *Septima* ridden by a **B. Taylor**, and a 1938 amateur theatricals review. A separate
newspaper search on **Lerena** returns 1,344 articles that are almost entirely OCR noise — Nissan *Serena*
advertisements misread — and nothing of ours. That avenue is closed and should not be retried.

***Mary Septima Taylor was a pupil teacher.*** *Western Times*, 4 April 1901, p.7, and *North Devon
Herald*, 11 April 1901, p.2, both print the Exeter Diocesan Board of Education results. Under
**Set II — monitors over sixteen and pupil teachers in their first year, 88 examined** — she appears in
**Class III**: *"Mary Septima Taylor, 16, Northam."* She was training to teach in her own village school.
Full write-up in `notes/mary-septima-pupil-teacher.md`, and now on the Taylors page.

**The gap this exposes is the important part.** A pupil teacher at Northam in **April 1901**. "Mrs Lerena",
crossing from Cape Town to Southampton with a three-year-old son, by **February 1909**. Eight years, and
the whole distance between a Devon parish school and an Argentine horseman's household at the Cape.
**How she got from one to the other is now the largest single hole in this family's story** — larger, and
more likely to be answerable, than the question of where Pablo Armando was born.

### The censuses — and a correction worth having
1891 and 1901, Northam, Devon. Full households in `data/taylor-censuses.tsv`.

***William Taylor was a retired cavalry sergeant.*** The 1891 enumerator writes his occupation as
**"Cab driver retired sergt p cavaloy"** — cab driver, retired sergeant, cavalry. By 1901, a widower at
North Street, Northam, he is an **army pensioner**. This archive had him as a *coachman*, from the tree;
the censuses are sharper and more interesting. His eldest son drove a cab beside him and his second son
was a footman.

**So horses stand behind both sides of the marriage.** Pablo Armando's whole story is horses — trainer,
breeder, stables, four generations of jockeys after him. Mary Septima's father spent his working life in
the saddle and on the box. That proves nothing and explains nothing, but this archive had been treating
her as the ordinary English half of the story, and that was wrong. Written up in
`notes/the-taylors-had-horses-too.md` and on the Taylors page.

**The pupil-teacher finding is independently corroborated.** The 1901 census was taken 31 March; the
*Western Times* printed the diocesan results on 4 April. Two unrelated sources four days apart, the same
fact: **"Mary Taylor, daughter, 16, School teacher, born Northam."**

**Her mother was a Londoner.** The 1891 census gives *Mary A H Taylor*, 47, as born **London, Middlesex** —
though Brayley is a north Devon surname. Unresolved.

**And an anomaly, recorded not explained: Mary Septima is absent from the 1891 census.** She should be six
years old in that household. She is not there, and no Mary Taylor born 1883-85 anywhere in Devon fits.
Most likely she was away that night or the index has mangled her. It needs checking against the image.

## *** THE SWEEP IS FINISHED. THREE YEARS, TWENTY-SIX LETTERS, NO PABLO ARMANDO. ***

**1881, 1882 and 1883 are now all read in full** across every letter section of the Rosario cathedral
baptism index (DGS 4530325), looking for the given name *Pablo Armando* under **any surname whatsoever**.

**He is not in any of them.**

That is fifty-two letter-bands for the two new years on top of the twenty-six done for 1882 — roughly
**two hundred image-reads across a 718-image film**. Coverage grids: `data/rosario-index-map.tsv` (1882)
and `data/rosario-index-1881-1883.tsv` (1881 and 1883).

### The last stretch, N through Z
N, O, P, Q, R, S, T, U, V, W, Y, Z all clear for both years; **X has no section at all**. Several sections
turn out to be tiny, and the numbers are worth stating because they show how thin this parish's register
is at the edges of the alphabet: **Q has ten entries in the whole of 1881** and thirteen in 1883;
**W has exactly one entry in each year** (Williams, Josefa Aurelia, 1881; Windels, María Elisa, 1883);
**Y's entire section is a single line** for 1900; and **Ll has no 1881 entries at all**.

### The near misses, now more than twenty
Across the three years every entry containing *Pablo*, *Paul* or *Armando* was logged. The closest remain
**_Ronillon · Armando Juan_** (1882, Libro 24 f.498) and **_Funes · Armando_** (1882, f.163) — the only two
Armandos in three years. The Pablos are numerous and none is ours: Chaparro Pablo H., Gorosito Pablo,
Carara Pablo, López Pablo, Lamberti Atilio Pablo Juan, Morón Juan Pablo, Días José Pablo, Ledesma Juan
Pablo, Leguisamón Pedro Pablo, López Pablo Gregorio, Luraschi Santos Pablo, Medina Pablo Mauricio,
Mendieta José Pablo, Olivieri Juan Pablo, Olguín Pablo Fabio A., Ojeda Pablo Eduardo, Pantaro Juan Pablo,
Quevedo Juan B. Pablo, Tello Pedro Paulino, Velez Juan Pablo, Villarreal Pablo del R., Zárate Pablo Jorge,
and bare *Pablo* entries in G, H and I.

**More than twenty near hits in three years.** That is the number that makes the negative worth something:
the method plainly catches the name when it is there.

### What is now established, and what is not
**Established:** no child named *Pablo Armando* was baptised at the **Iglesia Matriz / Catedral de
Rosario** in **1881, 1882 or 1883**, under any surname. The cathedral was the **only parish in Rosario
until 1888**, and civil registration in Santa Fe did not begin until about 1886. So for a three-year window
centred on his stated birth date, **the single most likely record of his birth anywhere does not contain
him**.

**Not established:** that he was not born at Rosario. He may have been baptised under a **different given
name** — he was *Robert Paul* in South Africa and *Pablo Armando* only on a passport issued in 1940 — or
outside this three-year window, or privately, or not at all.

### Where this leaves the project
The Rosario baptism route is now **exhausted**, not merely unsuccessful, and it should not be reopened
without a new reason. The weight of the argument shifts decisively to the other evidence, which has been
getting stronger while this sweep ran:

1. ***He held Argentine nationality by 1911***, proved from outside the family by his wife's declared
   nationality changing from **English (1909)** to **Argentine (1935)** on British passenger manifests.
   Nationality, however, is not birthplace.
2. **The Uruguayan kindred at Trinidad, Flores** — six brothers of this rare surname fathering children in
   one small town in the 1870s — remains the best candidate for where the family actually comes from, and
   **Uruguayan civil registration began in 1879**, three years before his stated birth.
3. **The political-refugee story**, if it means expulsion under the *Ley de Residencia*, requires him to
   have been **foreign-born** — which would explain this null result completely.

**The cheapest untried test is now Uruguayan civil registration for 1882**, not another parish register.

## Uruguayan civil registration, 1882 — run, and negative

The successor test to the Rosario sweep, chosen because **Uruguayan civil registration began in 1879** —
three years before his stated birth and seven before Santa Fe's. Full write-up in
`notes/uruguay-civil-registration.md`.

***There is no Pablo Armando Lerena in the Uruguayan records at all***, and **no Pablo Lerena born in
1882**. The complete list of Pablo Lerenas in Uruguay is four people: Pablo Granero *Llerena* (b.1870,
Montevideo), **Pablo Evaristo Lerena Harrison** (m.1902, Flores), Pedro Pablo Lerena (b.1910, Montevideo)
and Regino Pablo Olivera Lerena (b.1912, Flores). Nor is there a *Pablo Armando* of any surname born in
Uruguay in 1882 — the nearest two are both 1885 and neither is a Lerena.

**The control matters and it holds.** The index *does* contain Lerena births from this exact window,
including **María Luisa Lerena, born 19 July 1882, Río Negro**. So this is an absence in the record, not a
hole in the coverage. It remains an index rather than the registers themselves, so it **substantially
weakens the Uruguayan-birth idea without finally killing it**.

### What it gave us instead — the Uruguayan kindred, much enlarged
**Flores:** Bernabé Lerena m. Casimira Peláez · **Pio C. Lerena m. Bernardina Harrison** · Custodio Lerena
m. Ema Cardozo · Emilio Lerena m. Paula Casares · Venancio Alejandro Lerena m. Venancia · Luisa Lerena ·
and ***Gregorio ARMANDO Lerena***, marrying at Flores 1930, son of María Luisa Lerena — **the only Armando
Lerena in any of these records.**
**Montevideo:** Gilberto Lerena m. Julia Salvañach · Manuel Lerena m. Dolores Espíndola · Pedro A. Lerena
m. Manuela Lemos, and with Trinidad Morales · Pedro Segundo Lerena m. Paulina Grande.
**San José:** Alberto Lerena m. María Inés Larriera · Arturo Lerena m. Ema Regules.

### Three of four candidate birthplaces are now tested and failed
Rosario cathedral (three years, every letter) · Argentine baptisms generally (two Lerena entries in the
whole indexed country) · Uruguayan civil registration. **Spain is untested** — where the surname is most
numerous in absolute terms, concentrated on **Logroño, La Rioja**, exactly as the CEMLA arrivals showed.

## The estate in modern money
At David's request the conversion is now on the site. **£15,527 15s in 1950** — and these are **South
African pounds**, the Union having kept its own pound until 1961, **at par with sterling** in 1950, so the
conversion runs straight. By **retail prices** roughly **£500,000** today; measured against **average
earnings**, the better gauge of standing, closer to **£1.4 million**. Both are orders of magnitude, not
figures, and the site says so. He died **comfortably off rather than rich** — a working horseman who had
done well. The **£26 owed for carrots** is about **£830**, which is a great many carrots, and among the
plainer pieces of evidence that there were horses in the yard when he died.

## Spain — tested, and the forename turns out to be the sharper tool

The fourth and last candidate birthplace, run 9 September 2026 across FamilySearch's Spanish collections.
Full write-up in `notes/spain.md`.

**No Pablo Lerena born 1882 in Spain.** The whole country yields one of the right generation —
*Pablo Timoteo Lerena Muñoz*, **born 1878** at Bochones, Atienza, Guadalajara, son of Pedro Lerena Pérez
and Baltasara Muñoz Bermejos — and **he married at Atienza and stayed**.

### *** The finding that actually discriminates ***
***There is no Armando Lerena in Spain at all*** — not one, in any collection, in any century. Every result
is fuzzy noise (*Loreno*, *Lorena*, the Inquisición de Llerena registers of Almendral).

And **Armando is the name this family keeps**: Pablo **Armando**; his son Roque Luis **Armando**;
**Anton Armando** of the 1980 divorce and the 2013 estate; and **Gregorio Armando Lerena**, marrying at
Flores, Uruguay in 1930.

**Armando is a Río de la Plata name, not a Spanish peninsular one of the 1880s.** It entered Spanish usage
through Italian influence — the demographic signature of Buenos Aires, Rosario and Montevideo in exactly
that period, and not of rural La Rioja or Guadalajara. Across **three entire years** of the Rosario index
there were **two** Armandos: rare, but present. Across four centuries of indexed Spanish records: **none**.

**Of every test run in this archive, this is the first that argues FOR one origin over another rather than
merely failing to find him.** The name points back across the Atlantic.

### Two supporting observations
- **The Spanish Lerenas are scattered, not a kindred** — Almería, Écija, Barcelona, Valencia, Valladolid,
  Navarra, Guadalajara, Huelva, León, Ferrol — and in most of them **Lerena is the second, maternal
  surname** (*Manuel Fernández Lerena*, *Juan García Lerena*). Nothing like the six brothers at Trinidad.
- **Spanish practice gives two surnames.** His 1940 passport carries one. Long noted here as odd; against
  the Spanish evidence it is odder still, and fits Río de la Plata usage or the mother's-surname reading.

### The honest limit
Weaker as a negative than the Uruguayan test. **Spanish parish registers are enormous and only patchily
indexed**; an 1882 baptism in an unindexed Riojan parish would not surface. The fair statement is that
**he is not in the indexed Spanish records, and the given name his family carried does not belong to Spain.**

### A footnote now on the name page
**Llerena is a town in Badajoz, Extremadura**, and the surname is toponymic from it — a place important
enough to hold a tribunal of the Inquisition. *Lerena*, one L, is the Río de la Plata form. That is why the
two spellings have shadowed each other through every search in this project.

## Where all four stand
| Candidate birthplace | Status |
|---|---|
| **Rosario cathedral, 1881–83** | Tested exhaustively. Not there. |
| **Argentina generally** | Two Lerena baptisms in the whole indexed country. Not there. |
| **Uruguay, civil registration 1882** | Tested. Not there — with 1882 Lerena births present as a control. |
| **Spain** | Tested at index level. Not there — and the forename argues against it. |

**Everything now points at the Río de la Plata, and nothing in the Río de la Plata contains him.** The
remaining explanations are the ones that were always hardest to test: a **different given name** at
baptism, a **birth never registered**, or a record in a parish or department that no one has yet indexed.
The strongest untried leads are no longer birth records at all — they are the **1940 consular file** that
proves his nationality, and the **Ley 4144 expulsion files** that the family's own political-refugee story
points to.

## Two letters — one sent, one blocked

**Sent 9 September 2026 — Archivo Histórico de Cancillería**, `archivo@cancilleria.gob.ar`, Gmail msg
`1a084cbef3384599`. Address **verified from the Cancillería's own contact page**, which carries it as text
and as a live `mailto:` link. Asks for the **matrícula consular** of the Cape Town consulate 1930–50, the
**1940 passport file** and above all **what he produced to prove Argentine nationality and whether it names
his parents**, the consular correspondence, and — flagged as minor and explicitly not worth staff time —
whether he ever held a **consular appointment**, which puts the Consul General tradition to the one body
that could settle it. Details in `requests/cancilleria-matricula-consular.md`.

**Not sent — Ley 4144 expulsion files, Archivo General de la Nación.** Two things to record honestly:

1. ***A correction to the brief.*** These are **not army records**. The letter already with the Archivo
   General del Ejército asks for his *libreta de enrolamiento* — military **enrolment**, a different thing.
   **Ley 4144 expulsions were run by the Ministerio del Interior and the police**, and the files sit with
   the AGN. The two requests are complementary, not duplicates.
2. ***The AGN has closed its email channel.*** Its only remote route is a "Canal único de contacto" portal
   at `agnbicentenario.mininterior.gob.ar` requiring a **registered account**. No AGN email is published
   anywhere on argentina.gob.ar. **None has been invented.** The Spanish text is written out in full in
   `requests/agn-ley-4144-expulsiones.md`, ready to paste, and the account is David's to make.

Two alternatives noted there if the portal leads nowhere: the **Archivo Histórico de la Provincia de Santa
Fe** and provincial police holdings (a Rosario arrest would be recorded provincially before it reached
Buenos Aires), and the **International Institute of Social History, Amsterdam**, which holds the major
Argentine anarchist collections including *La Protesta* — the anarchist press **named** militants who were
arrested and deported, and the IISH answers email.

**Sent 9 September 2026 — International Institute of Social History, Amsterdam**, `ask@iisg.nl`, Gmail msg
`1a084e17877f1a41`. Address verified from the IISH's own contact page (`ask@` is collections and reading
room; `info@` is general, `communicatie@` is press). Written up in
`requests/iisg-argentine-anarchist-press.md`.

**Why Amsterdam for an Argentine question:** the AGN has no email and its portal is account-gated, while
the IISH answers email and holds a major collection of Latin American anarchist material. **The anarchist
press named names** — arrests, imprisonments and deportations of individual militants, often in lists. If
he was caught in the Ley 4144 expulsions the press is at least as likely to have recorded it as the
surviving state files, and far more reachable from Australia.

The letter asks four things — the 1902–06 Argentine anarchist periodicals and whether any are
text-searchable; Rosario/Santa Fe labour papers; FORA and prisoners'-committee records naming those
deported; and whether a surname search can be done remotely or needs a reader in Amsterdam. It gives
**LERENA · LLERENA · LARENA**, states plainly that this is family history rather than scholarship, offers
to pay or commission a researcher, and explicitly invites the answer that it cannot be done remotely. It
**asserts nothing** about what the IISH holds — every point is a question.

## Back to the film — and the state of play

**The 1881/1882/1883 sweep is finished.** All twenty-six sections, three years. There is no remaining work
under it, and it should not be restarted.

The concrete film item still open is the **1884 marriage candidate**: *"Larena V · Sarmiento A"*, **Libro
9, folio 20**, seen on image 51 of the marriage index and unreadable at that resolution — *Larena*,
*Lavena* and *Lerena* could not be told apart. To settle it: **DGS 4531041 (Matrimonios 1884–1891),
Libro 9, folio 20**.

### What today established about it, short of reading the page
1. ***Lavena is a real Rosario surname, and a well-documented one.*** An Italian family: **Francisco
   Lavena, born Italy 1880**, in Rosario at the 1895 census; children baptised at **San José, Rosario** and
   at the **Cathedral** between 1900 and 1915 (Albina 1906, Alfonzo 1909, Amalia 1912, Lucia Angela 1902,
   Teresa 1900); also Lavenas at Totoras and Cañada de Gómez. A Lavena marrying at Rosario in 1884 is
   entirely ordinary.
2. ***No Larena or Lerena marriage appears anywhere in Rosario's indexed records.***

**On the balance of evidence the 1884 entry reads *Lavena*.** That is a judgement, not a reading, and it is
recorded as such — the page itself has still not been seen.

### Why it was not settled today
The register is **handwriting**, and **the in-app browser cannot crop to a region** — it returns only full
screenshots, at which scale a nineteenth-century marginal folio number is illegible. The Chrome extension
*can* region-zoom and is what the whole baptism sweep was read with; it is **disconnected**. Reconnecting
it is all that stands between us and closing this item.

## *** A real find on the way past: a Larena household at Cayastá ***
Searching *Larena* in Santa Fe province turned up:

> **Antonio LARENA**, of **Cayastá, Garay, Santa Fe** — children **María, baptised 19 July 1890** and
> **Carmela, baptised 10 September 1892**; mother **Inés Azela / Raiela**.

**And Cayastá is where the only Lerena baptism indexed in the whole of Argentina sits** — *Leon José
Lerena, baptised 1892, Cayastá, Santa Fe, father José* (found in the Spain/Argentina baptism work).

**Two households of this rare surname, in one small village, in the same two years.** Cayastá is about
100 km north of Santa Fe city and some 250 km north of Rosario — not our city, but **the only
Larena/Lerena cluster anywhere in Santa Fe province**, and the first time the surname has been found
settled *in the province at all* rather than passing through it. Worth its own look.

## Cayastá looked at — and retracted

**The Cayastá "cluster" was a transcription artefact, and I was wrong to flag it as a lead.** Cayastá was
an **Italian agricultural colony**: its baptism register runs *Laurini ×5, Lauron, Castelarin, Masorini,
Panluzzi, Gaetta, Salvaserra, Llorin, Mazi/Massi/Mossi*. "Larena" sits in the middle of that — and the
**same mother is transcribed "Inés Azela" for one child and "Inés Raiela" for the other**, which is what an
indexer does with a name they cannot read. The apparent coincidence of a Larena and a Lerena in one small
village is the index mangling two different Italian families. Recorded rather than deleted, because a lead
chased and killed is worth as much to the next person as a right one. Full note in
`notes/cayasta-and-gualeguaychu.md`.

## What the same search found instead — the Gualeguaychú kindred
A **four-generation Larena family at Gualeguaychú, Entre Ríos**, densely documented in the Entre Ríos civil
registration: **Juan Larena m. Petrona López → Juan Antonio (b.1837, d.1908) m. Macedonia Lozano →
Victorino Severo (b.1878) m. Plácida Epifania Alarcón**, with **Vicente Antonio m. Vicenta Mercedes
Fuentes**, **Tito Gregorio**, **Juan José**, **Aureliano Emiliano** — and ***Roque Larena***, m. Florencia
Calixta Ramos, who appears at the **1895 census born 1881**. It is also the town of ***Juan Pablo Lerena***,
baptised 1891 — one of only two Lerena baptisms indexed in all Argentina.

***Roque*** is why it caught the eye: the name Pablo Armando gave his eldest son, on a man born within a
year of him.

**But there is no Pablo Larena and no Armando Larena anywhere in Entre Ríos** — both searches return only
fuzzy noise. Four generations, and neither of our names in any of them. And Gualeguaychú is on the far side
of the country from Rosario, which is the one thing about his origin the family has always been consistent
about. **Recorded on the register as unplaced; a candidate for elimination, not a discovery.**

## *** METHOD: the registers can be read as text — and a correction ***

I twice told David that settling the 1884 marriage candidate required the **Chrome extension**, because the
in-app browser cannot crop to a region and a nineteenth-century hand is illegible at full-page scale.
**He challenged it, and he was right to.** The premise was wrong twice over: the viewer has **its own zoom**,
so magnification never depended on the screenshot tool; and, far more importantly, **the handwriting does
not need to be read at all.**

**Every image carries an "Image Index" panel that is HTML text, not an image.** For a marriage act it gives
**both parties, their ages, and BOTH SETS OF PARENTS**, plus date and parish — the entire genealogical
content of the act — extractable with `document.querySelector('table').innerText`.

**This turns the Rosario marriage registers into a database.** It applies to the whole series, and had it
been understood earlier it would have saved much of the baptism sweep. Written up as
`notes/reading-registers-without-handwriting.md`, with the practical notes: get into single-image mode by
clicking a thumbnail, then step with the **arrows** — navigating by number or `?i=` URL bounces back to
the grid.

**Proved on 8 June – 8 July 1884** at the Cathedral: about fifteen marriages captured in full, all four
parents each, tabulated in that note. **No Sarmiento and no L-surname of interest in that stretch.**

**Still open:** the candidate at **Libro 9 folio 20** was not reached — the viewer kept resetting position
and the index panel appears on some loads and not others. A mechanical obstacle, not a research one. About
twenty images cover all of 1884, six marriages each.

## *** FOLIO 20 SETTLED. The candidate is Vicente LAVENA, and he is not ours. ***

Using the index-panel method, **8 June – 29 September 1884 was read act by act** at Rosario cathedral —
about ninety marriages. **One hit in the whole stretch:**

> ***Vicente LAVENA***, 26, b.1858, son of **Miguel Lavena** and **Lucía Lavena**, married
> ***Angela BELMONTE***, 21, b.1863, daughter of **Pascual Belmonte** and **María Cozsi**,
> on **3 August 1884** at the Catedral de Nuestra Señora del Rosario.

The index line was *"Larena/Lavena V · Sarmiento A · folio 20"*. The first surname is **Lavena**,
confirmed from the register. **"V" is Vicente. "A" is Angela.** Both initials match in order, and this is
the only L-surname marriage in three and a half months.

***The "Sarmiento" was my own misreading of BELMONTE*** in the low-resolution index image — recorded
because it is why this candidate survived as a lead for two days.

**This closes the last open candidate for a Lerena marriage at Rosario.** Vicente Lavena was Italian, which
fits the Lavenas of Rosario exactly: present from about 1880, children baptised at San José and the
Cathedral through 1915. **There is no Lerena marriage at Rosario cathedral in 1884.**

**Residual:** October–December 1884 unscanned. The candidate is identified so the item is closed, but four
or five more arrow-steps would make the year airtight.

### The residual closed: all of Libro 9's 1884 is read
**8 June – 31 December 1884**, act by act, running into 2 January 1885 to be sure of the boundary —
roughly **two hundred marriages**, each with both parties and all four parents.

**Libro 9 begins in June 1884**: the film's title card reads *1884–1888*, *PRINCIPIO* is at image 4, the
register starts at image 5, and the earliest dated act in the book is **8 June 1884**. January–May 1884 is
**not in this book** — it is Libro 8, a different film. The index entry said *"Libro 9º"*, so the relevant
year is covered end to end.

**In the whole year, exactly one marriage involves any of Sarmiento · Larena · Lavena · Lerena · Llerena:
Vicente LAVENA × Angela BELMONTE, 3 August 1884.** No Sarmiento anywhere in 1884. **No Lerena anywhere in
1884.**

## Libro 8 as well — answered by index, and the first Lerenas found in Rosario

**Libro 8 is a different film** — *Matrimonios 1868–1884*, DGS 4531040: sixteen years, ~3,000 marriages,
500-odd images. Rather than page it, the searchable index was used — **after first proving the index covers
those years.** A control search returns cathedral marriages of **1874, 1875 and 1876 with full parentage**
(Gonzalez × Castro, Gonzalez × Galvan, Gonzalez × Puccio, Gonzalez × Santander). **The 1868–1884 Rosario
marriages are indexed.** So the null that follows is about the record, not the coverage.

***There is no Lerena marriage at Rosario cathedral in Libro 8 (1868–1884).*** Searching LERENA at Rosario
in the collection returns 38 records and **not one is a marriage before 1900**.

**Taken with the act-by-act read of Libro 9's 1884: no Lerena marriage at Rosario across 1868–1891.**

**The difference in standard is stated rather than glossed:** Libro 9's 1884 was read *act by act*; Libro 8
rests on the *index*. The control proves the index is good, but an index carries gaps and mis-spellings in
a way a page-by-page read does not. Strong, not identical.

### *** And the first Lerenas ever found living in Rosario ***
This archive had never found a Lerena *in the city*. Two now appear, both at **Santa Rosa de Lima** — the
parish that opened in **1888**, after Pablo Armando's birth:
- **Luis LLERENA m. Clementina Baranda** → *Luis Alejandro*, baptised **1903**
- **Manuela LERENA m. Diego Román** → *Carmen Román Lerena*, baptised **1918** *(note the name Carmen)*

Neither can be his parents — both a generation too late — but they are the first evidence the surname
existed in Rosario at all. Added to the register.

## *** THE 1869 CENSUS OF ROSARIO — the surname in the city, before he was born ***

Working Santa Rosa de Lima turned up the most interesting thing in days. **The 1869 National Census shows
people of this surname living in ROSARIO** — the first time this archive has found any, anywhere in the
city, before 1882.

***Bartolomé LLERENA, born 1824 in CÓRDOBA*** — and alongside him a household indexed as *Lorena*:
**Agustín (b.1829)** with children born at **Córdoba** between 1853 and 1868 — Guillermo, Gerónima,
Mercedes, Feliz, María — plus **Luis and José Loroña**. A family that moved **Córdoba → Rosario** in the
1860s.

**Bartolomé would be 58 in 1882; Agustín 53** — either old enough to be Pablo Armando's *grandfather*, and
**the children born in the 1850s are exactly the right age to be his parents.**

### The objection, stated honestly
***Lorena is a real and separate surname***, and so is *Loroña*. The index may simply be right. But the
same small group is indexed under **three spellings** — Llerena, Lorena, Loroña — which is what an indexer
does with one difficult hand; the three names differ by a single letter; and this project has already
watched *Belmonte* be read as *Sarmiento* and *Laurini* as *Larena*. **A hypothesis, not a finding.**

### How to settle it
**Look at the 1869 census image.** The schedules are digitised. The hand will show whether it is *Lerena*,
*Lorena* or *Llerena*, and the schedule gives **the household structure** — head, wife, children, ages —
which the index strips away. One image. It would either hand us a Lerena household in Rosario in 1869 or
kill the idea outright. ***It is now the most valuable single unexamined document in the Argentine work.***

### Two more threads from the same search
- ***Gabino L. Llerena***, a groom in the Uruguayan church records **whose birthplace is given as ROSARIO** —
  a Rosario-born Llerena marrying in Uruguay, tying the two countries together as this family's evidence
  keeps hinting.
- ***Camilo Llerena***, 1869 census at **Nogoyá, Entre Ríos**, **born 1842 in Santa Fe** — a Santa Fe-born
  Llerena in the province of the Gualeguaychú Larena kindred.

Full write-up: `notes/the-1869-census-of-rosario.md`. All nine added to the register.

### The 1869 image read — and I have to correct myself
**Film #004331984, image 86, Sección 2ª.** The schedule was opened, panned and magnified until every field
was legible.

***My "household" reading last night was wrong.*** There is no Lerena family on that page. **Every line
carries its own number**, and the twelve people are of a dozen different surnames — washerwomen, a
laundress, day labourers, a peon, a carpenter, a Spanish shopkeeper. It is **a list of individuals at one
address, a conventillo or lodgings**. The *Lorena*/*Loroña* entries I grouped with Bartolomé are elsewhere
in the census entirely; the line I expected to be a Lorena is **Vachalo**.

**So there is no Lerena family in Rosario in 1869. There is one man:**

> ***Bartolomé LLERENA — 45, married, Argentine, born CÓRDOBA, JORNALERO — Rosario, Sección 2ª, 1869.***

He is still **the only person of this surname found in Rosario before 1882**, which is worth having. But
**he lodges among strangers** with no wife or children beside him though recorded married; **he is a day
labourer**, not a horseman or a man of property; and the surname on the page reads ***Llerena***, with the
Castilian double L.

**Weaker than it looked last night, and still the best pre-1882 Rosario evidence there is.** The next step
is the rest of the 344-image census: whether Bartolomé appears again with a household, and whether the
Lorena/Loroña entries are a family or, as here, scattered lodgers.

## Which Rosario? — a correction, and a caution the project should have had all along

**Gabino L. Llerena's "Rosario" is ROSARIO, COLONIA, URUGUAY — not Rosario de Santa Fe.** His record was
opened, and every other person on it is Uruguayan: *Solís Grande, Maldonado, Punta de Carretas, Cordón
Montevideo, Monte Video*. Flagging him last night as a Rosario-born Llerena linking the two countries was
wrong; corrected on the register before it hardened into a claim.

***Uruguay has its own Rosario.*** Any Uruguayan record naming *Rosario* means the Colonia town unless it
says otherwise — and given how much of this family's evidence runs through Uruguay, that ambiguity has been
sitting unremarked in the middle of the problem.

**The hypothesis it raises is recorded and is weak:** if the family's memory of "Rosario" came down through
a Uruguayan branch, the town could be the wrong one and the whole Santa Fe effort misdirected. **But the
passport says "Rosario de Santa Fe"** — naming the province, in his own document. It would take far more
than an ambiguity to overturn that. Written up in `notes/which-rosario.md`.

### A third Uruguayan Llerena cluster — Colonia
After Trinidad in Flores and Montevideo: **Tomás Llerena m. María Morales** (daughter Vicenta b.1861,
d. Carmelo 1927) · ***Pedro Llerena m. Sofía Clavijo*** (daughter Susana **b.1884**) · **María Llerena m.
Antonio Medero** · **Ramón** and **Gabino Llerena** at Rosario, Colonia · Manuel Medero Llerena · Isabel
Llarena.

**Pedro Llerena, fathering a daughter in 1884, is exactly the generation that could have fathered a son in
1882.** ***But there is still no Pablo Armando.*** Uruguay has now been searched across civil registration,
church records and baptisms — Flores, Montevideo, San José, Colonia — and he is in none of it.

## The five-point push — what each returned

### 1 · FamilySearch full-text search — *live, and worth returning to*
The instrument works, and the important question is answered: ***Argentine records ARE in the full-text
corpus.*** A query surfaced **"Santa Fe, La Capital, Santa Fe. Religious Marriage Records 1879–1882"** and
**"1882–1883"** as searchable, several showing matches. This is the first tool in the whole project that
reads **handwriting nobody has indexed**.

**Two caveats, stated plainly.** The coverage seen is **Santa Fe *La Capital*, not Rosario** — a different
city 170 km away. And the search interface is **badly behaved under automation**: the React textarea drops
programmatic input and swallows roughly half the submissions, so queries have to be typed and verified one
at a time. **No Lerena hit yet — but nothing like a proper sweep has been run.** This stays open as a real
lead rather than a closed door.

### 2 · Argentine military records — nothing
No **Pablo Armando** of any surname born 1880–84 appears in the Argentine records, and no military entry
for the surname. The passport's *Guardia Nacional, 6º de Caballería, 1915* still has to come from the
**Archivo General del Ejército** directly, and that letter is already with them.

### 5 · *** The Gilberto thread — two independent sources just joined up ***
This is the find of the round.

> **Carlos LERENA**, groom, Nuestra Señora del Socorro, **Retiro, Buenos Aires** — **born 1884,
> MONTEVIDEO** — parents ***Alberto\* Lerena*** and ***Julia SALVANACH*** — married
> ***Rosa María EPPENS***.
>
> *\* almost certainly **Gilberto** mis-transcribed, or a brother: Julia Salvañach is Gilberto Lerena's
> wife, already documented as the mother of Carlos Augusto Federico Lerena, b. 9 July 1883, Montevideo.*

**And that identifies the CEMLA couple.** The immigrant arrivals recorded **"CARLOS LERENA, 41, Uruguayan"**
and **"ROSA M. E. LERENA, 39, Argentine"** landing at Buenos Aires from **Montevideo on 27 May 1926**.
***Rosa M. E. is Rosa María Eppens.*** Two entirely independent sources — a Buenos Aires marriage register
and a shipping index — describing the same couple.

**A second link, also new:** ***Avelino Carlos Lerena, baptised 12 March 1904 at San Nicolás de Tolentino,
Mendoza***, parents **Carlos Lerena** and **Adela Camiglia** — which gives a birth and a parentage to the
Avelino Carlos who crossed to New York in 1940 and Rio in 1949 and 1953.

So the Stud Book family now runs: **Gilberto Lerena m. Julia Salvañach** (Montevideo, moving to Buenos
Aires between 1887 and 1889) → **Carlos Augusto Federico** (1883), **Raúl** (1885), **María Angélica Julia**
(1885) and others → **Carlos m. Rosa María Eppens** → and a **Carlos m. Adela Camiglia** whose son
**Avelino Carlos** was born at Mendoza in 1904.

***Still no connection to Pablo Armando.*** But this is now a real, documented, multi-generation Argentine
family rather than a name recurring in indexes — and it is the family whose forename stock (Gilberto,
Carlos, Raúl) the South African branch kept using.

### 3 and 4 — not advanced this round
The rest of the **1869 Rosario census** (whether Bartolomé appears again with a household) and the
**1901–1909 gap in Mary Septima's life** were not touched. They remain the two most tractable jobs left.

## The eight-year gap, narrowed to two ships

Pursuing point 4 of the five. **No Mary Taylor of her age left Britain for South Africa at all** — the
outward lists 1890–1960, searched on forename, age and destination, return **zero**.

**But the index often carries no forename.** Dropping it and filtering on surname, age and destination
produces **two candidates in exactly the right window**:

- ***MISS Taylor, 19, single, DOMESTIC*** — Southampton → **Cape, 9 September 1903**, ship
  ***Harlech Castle*** — TNA **BT 27/0420**, p.68, image 0004F
- ***MISS Taylor, 19, single*** — Southampton → **Cape, 9 April 1904**, ship ***Walmer Castle*** —
  TNA **BT 27/0448**

**Mary Septima was born 17 September 1884**, so on **9 September 1903 she was eight days short of
nineteen** — and the manifest says nineteen. The occupation fits the life too: a pupil teacher at sixteen
in a cab driver's household of ten children, at a moment when the Cape was **actively recruiting British
domestic servants** with assisted passage. That would put her in Cape Town about two years before Roque
was born there.

***A candidate, not an identification.*** Taylor is among the commonest English surnames and "Miss Taylor,
19" will have sailed for the Cape many times. **The original images would show the forename** — the
transcripts read perfectly but findmypast's tile viewer would not render in this browser, so the images
remain unopened. Two minutes' work in an ordinary browser. Written up in `notes/the-eight-year-gap.md`.

## Córdoba opened, and an Armando born in 1882

**#2 — the 1895 census re-run under variants — confirms rather than overturns.** There is no *Llerena* in
Santa Fe in 1895, and the *Lorena* entries at Rosario are **Spanish-born** (Amadora De Lorena, b.1849
Spain) — a different family, exactly as suspected at Cayastá. Bartolomé Llerena, there in 1869, is gone by
1895; he would have been 71.

**#1 — Córdoba, never searched before, has a Llerena family.** Bartolomé was *born* at Córdoba in 1824, so
the province mattered and had been overlooked. At Córdoba Cathedral: **Francisco Llerena m. Rafaela Daraz →
Baldomero (b.1851) m. Margarita Correas, 16 Feb 1876 → Sahara, Carlos, Julia Rosa**; also **Rafael Llerena
m. Rosario Moyano**, **Lucrecia Llerena**, **Amalia**. **Bartolomé belongs to Francisco and Rafael's
generation** — plausibly a brother. **No Pablo and no Armando among them.**

### *** And then this ***
In the **Argentine military records 1911–1936**:

> ***Armand[o] LORENA*** — **born 1882** — birthplace ***Rosario*** de Lerma, **Salta** —
> father Juan Carlos Lorena Serena, ***mother MARÍA LERENA***

Born 1882; named Armando — a name shown to be *rare* (two in three years of the Rosario index, **none** in
four centuries of Spanish records); born at a place called **Rosario**; **mother surnamed Lerena**, which is
precisely the mother's-surname hypothesis this archive has carried for days; and sitting in the **military
records**, where a man of the *clase 1882* belongs and where the passport's *Guardia Nacional 1915* points.

**The objections are serious and are not being softened.** **Rosario de Lerma is in SALTA**, 1,400 km from
Rosario de Santa Fe, and **the passport names the province**. The forename is *Armando*, not *Pablo
Armando*. The surname is *Lorena*. And **FamilySearch states the record was indexed by a computer** —
"Lorena Serena" reads like machine mangling.

***Probably not him. Worth opening anyway*** — the original document is linked and would settle it in a
minute. Written up in `notes/cordoba-and-the-1882-armando.md`, and on the register as a candidate.

**#4 — Carlos Gustavo Lerena, b. 1915** is not in FamilySearch's Argentine records at all. That thread
needs the foreign-ministry staff lists, not a genealogical index.

**#3 and #5 — Trinidad's six brothers, and a full-text sweep — were not reached.** Said plainly rather
than glossed.

## 10 September 2026 — the card that answers the question

**Item 1 on the list was "open the Armando Lorena military document." It took two minutes, and it is
Pablo Armando.**

The image is an Argentine army *ficha de enrolamiento* — a printed card with blank rules, filled in by
hand. FamilySearch image group **#112342450**, image **665 of 1,119**, volume **Cajón 985 (Lera)**,
creator **Ejército Argentino**. It reads:

> **Clase de 1882** · **LERENA — Pablo Armando**
> hijo de **Juan Carlos Lerena** y de **María Lerena**
> Nacido en **Rosario de Santa Fé**
> Oficina enroladora de **Capetown** · Serie **3885** · Sección **I 3322**

**The class of 1882. Born at Rosario de Santa Fe. Enrolled at Cape Town.** Three facts already known
from his own passport and his own death certificate, meeting on one card, in a drawer filed under
*Lera*. The passport's annotation *Guardia Nacional 1915* is the paperwork this card belongs to.

### The parents

> ### Juan Carlos LERENA and María LERENA

### The corroboration, from the other side of the ocean

Pablo Armando's eldest son — named with his exact birth date in the 1950 liquidation account — is
**Ricardo JUAN CARLOS Lerena, b. 6 January 1920, Cape Town**. A grandson of the same names died in
infancy in the Transvaal. The name came out of Argentina with him and was given to his first son at the
Cape. An Argentine army card and a South African deceased estate, with no possible knowledge of each
other, name the same man.

### How close this came to being thrown away

The previous round called this candidate **"probably not him"** and listed four objections. Three were
artefacts of a machine transcription: *Salta* for *Santa Fe*, *Lorena* for *Lerena*, and a second
surname *"Serena"* invented out of the word **SERIE** printed on the line below. The fourth — the
missing *Pablo* — was the index simply dropping a name. Only the image could separate them.

**The rule that follows: an index entry is a pointer, not a fact.** The archive has spent days
excluding candidates on indexed detail. Where that detail was the *only* ground for exclusion, the
exclusion is worth nothing until the image is opened.

### What is now open, and stated plainly

**María Lerena is written with her husband's surname.** On these cards *hijo de X y de Y* usually gives
each parent's own name — which would make her a Lerena by birth and the marriage one between kin. Some
clerks used the married name. **The card cannot decide it**, and neither can I. Her maiden name is the
next thing to find.

And the Rosario baptism index for 1881–1883 — swept letter by letter, twice — contains **no Lerena at
all**. A boy born in Rosario in February 1882 to a Lerena father is not in the cathedral's index. That
is now a real and specific puzzle rather than a null: he was baptised somewhere the index does not
reach, or under a spelling the sweep did not catch, or not baptised as an infant.

### Also picked up in the same hour

- **LDS Church Census Records (Worldwide), 1914–1960, South African Mission, 1935** — *Ricardo Juan
  Carlos Lerena*, b.1920, **Claremont C.P.**, and *Nuno Fernando Lerena*, b.1924, **Wynberg C.P.**
  A wholly new source, and one that places the family by suburb in the year Mary Septima died.
- **Careen Maria Lerena**, buried Cape, d. 27 June 1947 — not previously in the register.
- **Rhena May Lerena**, b.1913, d. 1 April 1998, Braamfontein — Roque's second wife (m. 1966).
- Confirmations of **Luis Roque Armando m. Rosaline Chappell**, 21 Sep 1936, Potchefstroom, and of the
  two infant deaths, **Rieta Maria** (1937) and **Antoinette Septima Lynette** (1943) — the second
  carrying her grandmother's name.

## Same day, later — the Chappell–Forbes knot, and a correction to our own record

Chasing the LDS Church Census entry that turned up beside the enrolment card led to the
**FamilySearch Family Tree**, where a small branch for this family already exists. **Nobody has
attached parents to Pablo Armando** — the enrolment card is genuinely new — but the branch carried
something else.

This archive had Roque's first wife as **"Rosalina Wilhelmina CHAPPELL"** and Ricardo's wife as
**"Doreen ?"**. Both wrong in the same way:

> **Roseline Wilhelmina FORBES** m. **Frederick Christian Chappell**, 1 Nov 1920, Woodstock, Cape Town.
> Chappell died 1933. His widow married **Roque Luis Armando Lerena** in 1936.
> Her daughter **Doreen May Chappell**, b.1921, married Roque's brother **Ricardo Juan Carlos Lerena**.

**Chappell was her married name. Her maiden name was FORBES.** The 1936 register calls her *Rosaline
Wilhermina Forbes Chappell* because that is what a remarrying widow is called — and this archive read it
as a maiden name.

**Two brothers married a mother and her daughter.** Verified before writing: the 1920 marriage exists in
*both* the SA civil registers and the Anglican parish registers, and Frederick Christian Chappell has his
own Western Cape estate file naming *Rose Forbes Chappell*. What is **not** proved is that this Doreen is
that Doreen — that rests on the tree plus the surname, and is marked inferred.

Also picked up: **Careen Maria Lerena** (d. 27 Jun 1947, Cape), **Rhena May** (b.1913, d. 1998 — Roque's
second wife, and the "R. M. Lerena" who signed his 1973 death notice), **Anton Lerena** (1952–2003, son
of Ricardo), and the two infant daughters of Roque and Roseline. Register: **125 people, 14 connected.**

**And the naming discipline is now visible as a rule rather than a coincidence.** Roque and Roseline
named a son **Ricardo Juan Carlos** — his uncle's name and his Argentine grandfather's — and a daughter
**Antoinette Septima Lynette**, carrying Mary Septima's. This family gave the grandparents' names back,
every generation. That is precisely why *Ricardo Juan Carlos*, b.1920, is good corroboration of a card
naming **Juan Carlos Lerena**.

## Published, and a letter sent

At David's instruction, two outward-facing things were done on 10 September 2026.

**1. The enrolment card is now on the public FamilySearch tree.** Pablo Armando `GPWH-72S` has gained
parents: **Juan Carlos Lerena `PFPY-23C`** and **María Lerena `PFPY-ZG1`**. The Source Linker's offer to
copy the indexed values was *refused* — accepting it would have written *Rosario de Lerma, Salta* over
his birthplace and created a father called *Juan Carlos Lorena Serena*. The parents were typed by hand
from the image. The reason statement on María carries the caution about her surname in capitals, so the
doubt travels with the finding. Written up in `notes/published-to-familysearch.md`.

**2. The Western Cape Archives letter is sent** — `archives.clientservices@westerncape.gov.za`,
address verified from the Western Cape Government's own service page, Gmail id `1a087da08db5ca31`. It
asks for the Death Notice in **MOOC 6/9/17017** and states the prediction: question 19 should name
**Juan Carlos Lerena and María**.

## And the L section is closed

David asked for the Rosario baptism index to be finished properly so it could be left behind. It has been.

**Every opening of the L section and of the Ll section, first to last, in order** — 41 frames, 38 distinct
and 3 duplicate exposures, each verified on arrival by year and Libro/folio, running continuously from
**Libro 23 folio 145** to **Libro 48 folio 546**, covering **1879 to 1901**.

> **No Lerena. No Llerena. No Larena. No Lorena. In any year. In either section.**

L opens at **1880** — there are no L entries for 1879 at all — and runs past 1900 into 1901. The whole Ll
section across twenty-two years is **twenty-six entries**. The nearest thing to the name in either
section is **LLERA** — Pedro (1898) and Ida C. (1900).

**The Armandos.** The forename does exist at Rosario — four times in the L band, and never in the right
year: **Lofré** 1889, **Luján** 1895, **Lunardi** 1895, **Limonetti** 1897. All after 1889. *Armando*
looks like a name that came into fashion at Rosario in the **1890s**, which makes a boy christened Pablo
*Armando* in February 1882 unusual for his date — and more likely to have been named for someone.

**The method is the transferable part.** The index is **typewritten**, not handwritten; the obstacle was
never the hand but the viewer's zoom. FamilySearch serves the pages as **DeepZoom tiles**, level 13 being
20 × 15 tiles of 257 px — about 5100 × 3800 for an opening. Assembled into a plain HTML grid at 42%, a
whole opening fits one screen with every surname legible. Image *numbers* drift between viewer states;
the image **ark** is stable and is what the data records.

**What it does not settle** is said plainly on the page: he was not baptised as an infant, or was
baptised outside the cathedral's books — **or the index itself is incomplete**, being a later typescript
compiled from the registers rather than the registers. That last is why an *act-by-act* reading of the
1882 register is still worth doing one day. Written up in `notes/the-L-section-closed.md` and
`data/rosario-index-L-complete.tsv`.

## The five, and how far they got

### ✅ 2. The marriage index, read at full resolution — DONE, and clean

The enrolment card gives a father, **Juan Carlos Lerena**. If he married at Rosario, his wife's maiden
name is in the marriage index — the one thing the card could not settle.

The *Índice de matrimonios 1860–1904* was read by the tile method across the whole window in which such
a marriage could have happened. Unlike the baptism index this one is **handwritten**, so level 13 was
needed — at level 12 the initials are illegible and the surnames merely guessable, **which is exactly how
"Lavena" became "Larena" in an earlier session.**

> **No Lerena marriage at Rosario cathedral, 1867–1885.**

Nearest approaches, checked at 1.4× to be certain: **Lercari L.** (1875) — Genoese — and
**Llisalinos J.** (1882). And the old error is now settled beyond argument: Libro 9, 1884, folio 20
reads **LAVENA V. × BELMONTE A.**, not *Larena × Sarmiento*.

Recorded in `data/rosario-marriage-index-L.tsv`.

### ◐ 4. Gilberto Lerena Lenguas — done as far as the open web allows

**Gilberto Justiniano Lerena Lenguas, b. 24 May 1855, d. 8 Dec 1912, m. Julia Salvañach.** Founded Stud
Oriental in 1887; **promoter, founder and Secretary of the Stud Book Argentino**, signing its first act
on 11 June 1893; bred **Old Man**, the Quadruple Crown winner; Haras El Viejo, Stud Bend Or, Haras La
Guardia, Haras El Moro, Haras Las Ortigas. The *Premio Abril* was renamed the **Gran Premio Gilberto
Lerena** in 1914 and is still run as a Group 1.

The **Lerena Lenguas were Uruguayan and rich** — *Luis Lerena Lenguas* had a fifteen-room country house
at Juanicó photographed for the **1889 Paris exhibition**.

**And nothing connects him to Pablo Armando.** The temptation is obvious — rare surname, famous horseman,
a family that remembered horses, a great-grandson who trained at the Cape — and it is refused. Two doors
that would answer the only useful question (*was there a Juan Carlos in that family?*) are shut against
automation: **geni.com** behind an hCaptcha and **Geneanet** behind Cloudflare. Both are a one-minute job
for a person. Written up in `notes/gilberto-lerena-lenguas.md`.

### ✕ 1, 3 and 5 — blocked, and the block is mine

**FamilySearch cut this session off.** `www.familysearch.org` now returns
*"Access Denied — Error 15 — This request was blocked by our security service."* After a day of heavy
automated reading — the drawer, the whole L section, the marriage index — their bot protection has had
enough, and that is a fair response to what I was doing.

That blocks all three of the remaining items, because all three live there:

- **1. The 1882 baptism register act by act** — the test of whether the index typescript is complete.
- **3. The 1935 LDS household card** — the card listing the household Ricardo was a *son* in.
- **5. The rest of the 1869 census** — 344 images, whether Bartolomé Llerena recurs.

**One useful detail for whoever picks this up:** the block is on `www.familysearch.org` only. The tile
host `sg30p0.familysearch.org` **still serves**, so any image whose *ark is already recorded* can still
be read. What cannot be done is discovering new arks, because that needs the viewer.

**Stated plainly rather than dressed up: two of the five are done, and three are stopped by a wall I
walked into myself.** These blocks usually lift within hours.

## The block lifted, and three more things done

FamilySearch released the session after about an hour. Work resumed, more gently.

### ✓ 3. The LDS household card — answered, and it is a wall not a null

The 1935 South African Mission census card **exists as an image**. FamilySearch reports
*"Image Available — to view these images: access the site at a FamilySearch Center / affiliate
library."* So it is **centre-only**, the same restriction as the Cape estate file. Worth knowing
exactly: Ricardo is recorded as **"Relationship to Head of Household: Son"**, so the card lists a
household with a head — almost certainly Pablo Armando, in November 1935, the month Mary Septima died.
**A visit to any FamilySearch Centre would get it.**

### ✓ 1. The 1882 register, act by act — the real work of the day

The index that every Rosario null depends on is a **typescript**, and whether the typist missed anything
had never been tested. It has now been tested.

**Libro 24, read act by act** — film 004098792, waypoint *Bautismos 1881-1882*. Every act carries the
child's name in the margin; all 183 margins in the span were read.

> **1 February to 15 March 1882 — acts 113 to 295, pages 390 to 435 — no Lerena.**

He was born **22 February**. That is three weeks either side of his birth, act by act, nothing skipped.

**And the book gave up a rate**: Rosario cathedral baptised **112 children in January 1882, 122 in
February** — four a day. The first time this archive has had a denominator.

**A filming detail worth keeping**: page 425 carries a slip pasted on **29 May 1905** that hides four
acts, and **the next frame is the same page refilmed with the slip lifted**. Nothing is lost. The 1974
filming was careful.

**What it settles**: the index is not hiding him, at least not here — register and index agree.
**What it does not**: six weeks is not a year. April, or 1883, or an adult baptism, are all still open.
Written up in `notes/the-register-itself.md` and `data/rosario-1882-register-actbyact.tsv`, with the
stopping point recorded so it can be resumed exactly.

### ✓ A date that gives the consul story a mechanism

Argentina and South Africa **established diplomatic relations only on 10 September 1947**; Argentina
opened its legation at Pretoria in **1950**, and the earliest consulate the published histories mention
is South Africa's at Buenos Aires in **1938**.

Yet this family holds two Argentine documents proving a consular office at **Cape Town in 1908** (the
card's *"Oficina enroladora de Capetown"*) and **in 1940** (the passport's *Oficina Consular Argentina*,
sealed and stamped). **Thirty-nine years before there were diplomatic relations.**

Not a contradiction — consular relations are not diplomatic relations, and the usual instrument is the
**honorary consul**: a resident merchant, unpaid, commissioned to stamp passports and register
nationals. *A. B. Bayne* is not a Spanish name.

**So the "Consul General" tradition is not proved, but it is now explicable** — a different and more
honest thing. It also sharpens two targets: the **exequatur in the Government Gazette**, which would
name every holder of the post across 1900–1950; and the **consular matrícula**, already requested from
the Cancillería. Written up in `notes/the-consulate-that-should-not-exist.md`.

**And a footnote against the family lore**: a man fleeing Argentina as a communist does not walk into his
own government's consular office in 1908 and put his name, his class, his birthplace and his parents on
a form. Not proof — but evidence on the other side, and it belongs on the record.

## The DNA — a third leg, and a hypothesis with teeth

A granddaughter of Pablo Armando has tested at MyHeritage; her son shared the result. **She is living, so
this archive omits her**: she is not named, her ethnicity profile is not published, and only the figures
that bear on Pablo Armando — dead since 1950 — are recorded.

**What it settles.** A genetic group at **high confidence**: *Argentina (Corrientes and Buenos Aires),
Uruguay and Paraguay*, built from **178 kits, 61 with trees**. That is a cluster of people sharing actual
chromosome segments whose documented trees converge on the Río de la Plata. **It can only have come from
him** — her other three grandparents are English Devon and Cape Afrikaner.

So the Argentine origin now stands on **three independent legs**: the 1940 passport, the 1908 enrolment
card, and a chromosome. A fortnight ago it stood on one. **And the group's top places for 1900–1950 name
SANTA FE** — the first time anything outside the family's own paperwork has pointed at that province.

**What it questions, and this is the interesting half.**

> **Iberian: 0.0%. Italian: 11.1%** — North 6.1, South 3.6, Sardinian 1.4.

**There is no Spanish component at all.** A Spanish-descended criollo great-grandfather should show as
roughly 25% Iberian in a granddaughter. He shows as none. What she does carry is **Italian**, which has
no other source in her tree, and at one quarter **11.1% in her implies about 44% in him — one Italian
parent.** The split is **northern-dominant**, the signature of the Ligurian and Piedmontese emigration
that made Rosario the most Italian city in Argentina.

**Why it would explain rather a lot.** A couple who married **in Italy before emigrating** would never
appear in the Rosario marriage register — which has now been read clean for 1867–1885. The register
around his birth, read act by act, is full of Piaggio, Ricotti, Savoni, Bianchi, Ferrari, Daneri,
Scorzetti, Louraschi, Ranieri, Figallo. And **his death was registered LERINA** — treated here for a
month as a clerk's slip, while **CEMLA records Lerina as an *Italian* surname arriving from Genova**. The
"error" may be the one document that got it right.

**Stated as a hypothesis, not a finding.** Ethnicity estimates are not records; at one quarter the noise
is large; MyHeritage distributes Iberian awkwardly. The *genetic group* is the stronger signal, and it
says Río de la Plata — not Italian.

**Four consequences for the work.** See the other five genetic groups (only 3 of 8 are shown). Work the
matches rather than the percentages. **Re-read the Rosario sweeps for LERINA — it was never separately
looked for**, and it sorts adjacent to Lerena. And re-run CEMLA treating LERINA and LARENA as primary
spellings.

Written up on `/dna/`, in `notes/what-the-dna-says.md` and `data/dna-evidence.tsv`, and as hypothesis 1b.

### And the very next screenshot weakened it

The slider was moved to low confidence: **8 of 8** genetic groups. Five are legible —
**South Africa · South Africa and Zimbabwe · Argentina (Corrientes and Buenos Aires), Uruguay and
Paraguay · England · Ireland (Cork, Kerry and Limerick) and England.** Three sit below the fold, unseen.

**No Italian group among the five.** That is evidence *against* hypothesis 1b, and it arrived within an
hour of the hypothesis being written down. It does not kill it — a cluster needs enough tested people
with documented trees, and an Italian great-grandparent's group can fail to form — but the easiest
confirmation was available and did not appear.

**The asymmetry, stated plainly:** the Río de la Plata group is a *positive* result, a cluster formed at
high confidence from 178 kits. The Italian claim rests on a *negative* — no Iberian — plus arithmetic on
11.1%. Not the same class of evidence, and this archive will not treat them as though they were.

**And the eight groups strengthen the thing that was already proved.** Every group except the Río de la
Plata one is accounted for by her other three grandparents: two South African, two British Isles. That is
a clean four-grandparent reading, and it makes the Argentine group *harder* to explain away, not easier.

*Also recorded: the confidence slider governs the genetic groups only. The ethnicity percentages are
identical in both views.*

## Compared against the Defranceski archive

David asked for a side-by-side. It forced two corrections of my own before it produced anything useful.

**The palette.** I said earlier the Lerena tokens matched *Falco's*, then that they were a deliberate
cool variant. Both wrong. **The Lerena `styles.css` root block is byte-identical to Defranceski's** —
every token, the same typefaces, the same `--maxw`. Lerena inherited the **Defranceski** system exactly;
**Falco is the outlier** with a warm palette. Corrected in
`notes/consistency-with-the-falco-archive.md` and written up properly in
`notes/compared-with-the-defranceski-archive.md`.

**The scale.** Defranceski: **65 pages, 38 components**. Lerena: **21 and 2**. Mostly a depth difference,
not a defect — but it means the list is dominated by things that are *absent* rather than *wrong*.

**Three things that ARE wrong, because this site contradicts itself:**

1. **The living-person rule is broken by our own pages.** The footer says living people are *excluded*;
   `/direct-line/` publishes a living person's **name, exact birth date, two cities and both marriages**
   under a chip reading "Omitted" and a caption reading "Details withheld." Defranceski's rule is
   different and workable — *"by name only: no dates, no places, no photographs."* **Pick one and honour
   it.** The present state claims a protection it does not provide, and `/dna/` now sits on top of it.
2. **Two chip vocabularies on one site** — the home page advertises *Documented · Inferred · Family lore*
   while the register uses *Connected · Excluded · Unplaced*. Both fine; both unexplained is not.
3. **The footer promises corrections with nowhere to put them.** This archive has made **at least eight
   documented corrections in a fortnight** and they are buried in notes. Defranceski publishes them,
   counted, with a "serious" tally. It is the most credible thing an archive owns.

**And the mechanical reason our register links five rows out of 125:** Defranceski stores a bare
FamilySearch id and builds the URL with an `ark()` helper. We store whole URLs, so we mostly store
nothing.

## Amsterdam answered, and it goes against the family story

The letter of 9 September was answered on the 10th. The **International Institute of Social History** —
the principal repository for the international left — replied that its Latin American periodicals,
Argentinian included, are **digitised and OCR'd** as *Latin American Anarchist and Labour Periodicals
Online, c. 1880–1940*, and that their archivist had searched **Lerena and its variants**: *"nothing
popped up."* They will scan specific items at **€0.50 each**, but cannot research on our behalf.

**Re-run here the same day**, because "nothing" is a weaker record than a description of the noise:

- **Lerena — 171 hits**, almost all the **Conde de Lerena** (Charles III's finance minister, whose 1787
  *Censo* is quoted in Spanish economic history) and **"Osimani y Llerena"**, a *street in Montevideo*
  where the anarchist weekly *La Tierra* had its office.
- **Lerina — 16 hits**, every one OCR breakage of **"ballerina"**.

**No person of this family in the Latin American left press, 1880–1940.**

**And the weight of that, stated honestly rather than banked.** It is the *weakest* of the three
objections to the tradition. A horse-dealer in his twenties would not be in the anarchist press unless he
were notable, and most people never appear in any periodical at all. **The objection that actually bites
is the enrolment card**: in 1908 he walked into his own government's consular office at Cape Town and
wrote down his name, his class, his birthplace and both his parents. A man hiding from the Argentine
state does not do that. And **Ley 4144 deported foreigners, not nationals** — the mechanism the story
implies could not have been used on him.

**Not disproved. Now unlikely.** The AGN expulsion files remain the only place that could settle it
positively, and that request still needs David to register with a passport.

*One down of four: the Army, the Cancillería and the Western Cape Archives are still out.*
