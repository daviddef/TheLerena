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
