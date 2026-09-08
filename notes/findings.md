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
