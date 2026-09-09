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
