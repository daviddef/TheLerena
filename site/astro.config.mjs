import { defineConfig } from 'astro/config';

// GitHub Pages project site. Change `base` to '/' and `site` to the domain
// if this ever moves to a custom domain.
/* 9 October 2026. Two pages folded into pages that do the same job; their published
   addresses stay alive and land on the section that now holds them. */
const BASE = '/TheLerena';
const redirects = {
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
  /* NOT a rename but a MERGE: she and Angelica are one woman, argued on her row. */
  '/people/amelia-lerena': `${BASE}/people/angelica-maria-lerena-villademoros/`,
};

export default defineConfig({
  site: 'https://daviddef.github.io',
  base: '/TheLerena',
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
