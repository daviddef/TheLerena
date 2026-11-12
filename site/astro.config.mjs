import { defineConfig } from 'astro/config';

// Custom domain, from 12 October 2026: https://lerena.defranceski.com/
// Served by GitHub Pages from this project repo. `base` is '/' and BASE is ''
// because every link here is site-root relative; site/public/CNAME is what
// keeps the domain attached across Actions deploys — see the note there.
/* 9 October 2026. Two pages folded into pages that do the same job; their published
   addresses stay alive and land on the section that now holds them. */
const BASE = '';
const redirects = {
  /* 12 October 2026. The army card spells him LORENA; the baptism act of San Cristobal,
     read at the plate the same day, spells him LERENA - and that act is what proved his
     parents are the 1895 census household. The row was renamed to what the act says, so
     the address it had for a few hours is kept pointing at him. */
  /* 12 October 2026. *** A SWEEP, NOT A SIGHTING. *** Walking the live site found
     ONE dead person address; asking the frozen ledger which of its keys no longer
     name a row in the register found TWENTY-TWO, of which FIVE had neither a page
     nor a redirect. The ledger is keyed by NAME, so every rename that touches a
     name strands its key and mints a fresh slug with a -2 suffix - the hazard its
     own _why calls "the fault this file exists to prevent, merely made rarer".
     Two of these had been dead since 23 September. No gate could see any of them:
     check-links only follows links that still exist, and nothing linked here. */
  '/people/emilia-lerena-vega': `${BASE}/people/emilia-lerena-vega-2/`,
  '/people/vicenta-lerena-vega': `${BASE}/people/vicenta-lerena-vega-2/`,
  '/people/domingo-razzetti': `${BASE}/people/domingo-razzetti-2/`,
  '/people/josefina-bertoglio': `${BASE}/people/josefina-bertoglio-2/`,
  /* This one was minted and withdrawn inside a single day, when the Artigas
     death turned out to be a Montevideo death and the row was folded into the
     man it duplicated. It was deployed in between, so it is a promise too. */
  '/people/pedro-a-lerena': `${BASE}/people/pedro-lerena-vega-2/`,

  /* 12 October 2026, and a smaller version of the same mistake. Pedro LERENA Vega
     was renamed when the census behind him turned out to be the padron of 1850
     rather than c.1833, moving his birth estimate from c.1817 to c.1834. The
     parenthetical is stripped from the slug, so this should have been a free
     rename - but the deduped slug moved to pedro-lerena-vega-2 anyway, and
     /people/pedro-lerena-vega/ had been published and live that morning. Nothing
     linked to it, so no gate caught it; it was found by walking the new domain
     page by page. A published address outlives the reason it was minted. */
  '/people/pedro-lerena-vega': `${BASE}/people/pedro-lerena-vega-2/`,

  /* 5 November 2026. The row 'Rodolfo Bernardo Lerena (father, Trinidad 1918)' and the row of Rodolfo B. Lerena Cardozo were one man (the baptisms of 1918 and 1919, read at the plate on 1 November 2026, write his name Rodolfo Bernardo Lerena with his wife Maria Luisa Caballero and his parents Bernabe and Florinda Cardoso). MERGED. */
  '/people/rodolfo-bernardo-lerena': `${BASE}/people/rodolfo-b-lerena-cardozo/`,

  /* 5 November 2026. A row for the 1969 death of Alberto Medardo Rodriguez Lerena was minted for a few minutes and withdrawn: he is the Alberto Madardo of the Flores birth act of 8 June 1921 (same birth date, same parents), already held. The death went into that row. */
  '/people/a-m-rodriguez-lerena': `${BASE}/people/alberto-m-rodriguez-lerena/`,

  /* 3 November 2026. 'Ademar' (twenty-six in 1912, the Ademar of his father's death act) and 'Miguel Abdemar' (the baptism of 1886) were one man: his own death act of 30 July 1948 calls him ADEMAR MIGUEL, son of Cipriano Lerena and Laureana Beloqui, husband of Maria Blanca Gau. MERGED. */
  '/people/ademar-lerena-beloqui': `${BASE}/people/miguel-abdemar-lerena-beloqui/`,
  /* 3 November 2026. 'A. C. Lerena (m. Blanca Rodriguez)' and the index row 'Angel Custodio Lerena Cardozo (1934-1955)' are one man with the Angel Custodio Carmelo of 1889 (probable): his death act of 16 October 1955 names his parents Doroteo and Isidora Cardozo and his wife Blanca Rodriguez; the index's 1934 was a mistake. */
  '/people/a-c-lerena': `${BASE}/people/angel-custodio-carmelo-lerena-cardozo/`,
  '/people/angel-custodio-lerena-cardozo': `${BASE}/people/angel-custodio-carmelo-lerena-cardozo/`,
  '/people/salvador-lorena': `${BASE}/people/salvador-lerena/`,
  /* 26 October 2026. 'Alejandro F. Lerena' and 'Natalia Lerena', held from the Trinidad index since 11 October as the parents of Aurora Lerena, were not two people: the baptism of 3 September 1891 names her parents Alejandro and Severa Fernandez. The first is Alejandro Florencio, the younger; the second is Natalia Lerena, wife of Manuel Vaquero, who is Aurora's mother-in-law. MERGED. */
  '/people/alejandro-f-lerena': `${BASE}/people/alejandro-lerena-2/`,
  '/people/natalia-lerena': `${BASE}/people/natalia-lerena-2/`,
  /* 26 October 2026. The elder Bernabe drawn at the apex of the 1911 dispensation diagram, published since September as a person of his own, is the Bernabe of Trinidad who married Casimira Pelaez: the 1889 double wedding names the father of Maria Lerena, who married Eliseo Cardozo. MERGED. */
  '/people/bernabe-lerena-3': `${BASE}/people/bernabe-lerena/`,
  /* 26 October 2026. Isaac Filomeno LERENA Fernandez, baptised at San Jose in June 1845, was published for a day as a separate person;
     the Trinidad baptism of his son in 1880 names his parents, and he is the Ysaac LERENA of Trinidad already held. MERGED. */
  '/people/isaac-filomeno-lerena-fernandez': `${BASE}/people/ysaac-lerena/`,

  '/gaps': `${BASE}/open-questions/#may-never-close`,
  '/photograph-these': `${BASE}/errands/#photographs`,

  /* 11 October 2026. A surname read as ZALSAMENDI for three weeks is ZALDUONDO on
     both plates, and "Amelia LERENA" is ANGELICA MARIA LERENA VILLADEMOROS. Five
     person pages changed address or were merged away. THEIR OLD ADDRESSES WERE
     PUBLISHED, so they stay alive and land on the same human being. The slug
     ledger keeps the dead slugs rather than deleting them; this is where they go.
     See data/corrections.tsv and /uruguay/#s-zalduondo. */
  '/people/eduardo-zalsamendi': `${BASE}/people/eduardo-zalduondo/`,
  '/people/juan-zalsamendi': `${BASE}/people/juan-zalduondo/`,
  '/people/dolores-pou-de-zalsamendi': `${BASE}/people/dolores-pou-de-zalduondo/`,
  '/people/maria-margarita-zalsamendi-lerena': `${BASE}/people/maria-margarita-luisa-zalduondo-lerena/`,
  /* 12 October 2026, the same day. The 1906 Trinidad marriage act gives the bride's
     mother as "Dona ANDREA ETCHEBERSE" - the surname broken across the opening - and the
     index gave her the FATHER'S surname instead. The groom is ETCHEBERSE on the act and
     ECHEBERSE in the index. Both renamed to the act. */
  '/people/andrea-lerena': `${BASE}/people/dona-andrea-echeverry/`,
  /* 26 October 2026. The index's Vitaliano Lerena and Andrea Etcheberse (the 1906 marriage act of
     their daughter) are Vitalino Lerena and Dona Andrea Echeverry, whose burial of 15 May 1883 names
     the same wife; the two rows were merged. */
  '/people/vitaliano-lerena': `${BASE}/people/vitalino-lerena/`,
  '/people/andrea-etcheberse': `${BASE}/people/dona-andrea-echeverry/`,
  '/people/antonio-echeberse': `${BASE}/people/antonio-etcheberse/`,

  /* 12 October 2026. An index turned "esclava de D.n Alejandro Lerena" into a marriage.
     The plate says Barbara was an enslaved woman in his household and her son Carmelo
     Anselmo was hijo natural with no father named; neither carried the surname. All three
     rows renamed to what the act says. See data/corrections.tsv. */
  '/people/barbara-lerena': `${BASE}/people/barbara/`,
  '/people/alejandro-lerena-3': `${BASE}/people/don-alejandro-lerena/`,
  '/people/carmelo-anselmo-lerena': `${BASE}/people/carmelo-anselmo/`,

  /* 11 October 2026, later the same day. Two rows for Eduardo Lerena proved to be one
     man when the Canelones marriage act named the bride's parents - the same couple who
     stood godparents to his daughter in Argentina the following year. Merged. */
  '/people/eduardo-lerena-2': `${BASE}/people/eduardo-lerena/`,

  /* 11 October 2026. ROZZETTI is RAZZETTI: the index of the 1921 baptism spells the
     mother one way and the act spells her the other, twice on one line, in a clear hand.
     Both addresses were published. See data/corrections.tsv. */
  '/people/maria-mercedes-rozzetti': `${BASE}/people/maria-mercedes-razzetti/`,
  '/people/ana-maria-lerena-rozzetti': `${BASE}/people/ana-maria-lerena-razzetti/`,

  /* 11 October 2026, found by a site-wide audit. The 1840 Catedral act was quoted on
     this archive's own page with the grandfather's forename in SQUARE BRACKETS -
     "Nieto pat[erno de D. Domingo] RODRIG.z" - supplied by the reader because the CHILD
     is called Domingo. The plate says JOAQUIN. So a man was published for three weeks
     who never existed, and his wife was published twice under two names. Both addresses
     were live and both now land on the people the act actually names.
     See data/corrections.tsv. */
  '/people/don-domingo-rodriguez': `${BASE}/people/mayor-don-joaquin-ruiz-de-carvallo/`,
  '/people/dona-juana-del-espiritu-santo': `${BASE}/people/dona-juana-suarez/`,

  /* NOT a rename but a MERGE: she and Angelica are one woman, argued on her row. */
  '/people/amelia-lerena': `${BASE}/people/angelica-maria-lerena-villademoros/`,

  /* 8 November 2026. A MERGE: the Trinidad christening of 24 April 1870, held from the index
     alone as 'Nemecio Ramon LERENA (b.1870)', was opened and read at the plate; it gives a birth
     of 19 December 1869 to the same parents and is the man of Salto and Concordia. */
  '/people/nemecio-ramon-lerena': `${BASE}/people/ramon-lerena-3/`,
  /* 12 November 2026. Two San Francisco de Asis burial rows (1872 and 1914) were renamed within hours of
     being minted, so that words describing the act sit inside the brackets (they had been read as given
     names by the linking standard). The addresses they briefly had point at the same two people. */
  '/people/dona-dominga-lerena-widow-of-don-antonio-carballo': `${BASE}/people/dona-dominga-lerena/`,
  '/people/dona-justiniana-written-lenguas-de-lerena': `${BASE}/people/dona-justiniana/`,
  '/people/justiniana-lenguas-de-lerena': `${BASE}/people/dona-justiniana/`,
};

export default defineConfig({
  site: 'https://lerena.defranceski.com',
  base: '/',
  /* WHY outDir IS A VARIABLE, and why the default must stay 'dist'.
     Several sessions build this estate at once, and `astro build` EMPTIES its
     outDir before it refills it — so one session's build wipes the tree
     another session's gates are reading, and the gates report a torrent of
     absences that are simply not copied yet. The kit's tools all honour
     ARCHIVE_OUT and, when they refuse a shared build, print «build to a
     directory of your own: ARCHIVE_OUT=...» as the way out. WITHOUT THIS LINE
     THAT HATCH CANNOT BE TAKEN: the variable redirected every reader and
     nothing that writes. Found 27 September 2026, after the kit had been
     printing that advice for four days.
     THE DEFAULT MUST STAY 'dist' — .github/workflows uploads `path: site/dist`,
     so changing it here would publish nothing. */
  outDir: process.env.ARCHIVE_OUT || 'dist',

  build: { format: 'directory' },
  redirects,
});
