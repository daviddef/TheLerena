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

  '/people/salvador-lorena': `${BASE}/people/salvador-lerena/`,
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
  '/people/andrea-lerena': `${BASE}/people/andrea-etcheberse/`,
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
