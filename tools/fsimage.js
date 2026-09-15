/* Read any FamilySearch film image without the viewer, and without www.
 *
 * Paste this whole file into the browser console on ANY page of
 * sg30p0.familysearch.org (open a thumb_p200.jpg first - it is public and
 * needs no session). Then:
 *
 *     await __show(8166578, 2687);   // film, image  -> loads the mosaic
 *     __fit();                       // whole opening
 *     __view(430, 900, 1.15);        // page x, page y, scale
 *     await __sheet(8166573, 1438, 1470, 1);   // thumbnail contact sheet
 *     await __resolve('3:1:3Q9M-CS2Z-W45W');   // ark -> film and image
 *
 * WHY THIS EXISTS. The FamilySearch viewer renders an image in 30-60 seconds
 * in an automated browser and often not at all, and www.familysearch.org is
 * regularly behind an Error 15 block that takes down /search/ and ark: pages
 * together. The tile host is NOT behind that block. So this keeps working when
 * nothing else does - the 1791 marriage act was found this way while www was
 * returning Access Denied.
 *
 * THE ID. dgs:{film9}.{film9}_{image5} is accepted directly, so any image on
 * any film is addressable BY NUMBER: no ark, no viewer, no catalogue.
 * manifest.json converts an ark to that id and back.
 *
 * THREE TRAPS, EACH OF WHICH COST REAL TIME ON 15 SEPTEMBER 2026:
 *
 *  1. NEVER cache-bust a failed tile. Re-request the SAME url
 *     (i.removeAttribute('src'); i.src = u). Appending ?rt=... returns a
 *     DIFFERENT tile and silently scrambles the mosaic.
 *  2. Wait after naturalWidth>0 before screenshotting, or tiles render white.
 *  3. NEVER batch __view and the screenshot in one call. A CSS transform has
 *     not repainted when the screenshot is taken and you get the PREVIOUS
 *     view. Separate calls, every time.
 *
 * AND ONE RULE THAT IS NOT ABOUT CODE: do not read names at fit-width. On one
 * day this cost four misreadings - a chaplain as "Mendoza" who is BERROETA, a
 * slave-owner as "Llerena" who is FRANCISCO JUAREZ, a mother as "Rosalia
 * Illera" who is PETRONA ILLESCAS, and a year as 1836 that is 1830. Magnify
 * before believing, and magnify hardest when the reading is the one you hoped
 * for.
 */
const D = '/service/records/storage/deepzoomcloud/dz/v1/';

window.__id = (f, i) => {
  const p = String(f).padStart(9, '0');
  return `dgs:${p}.${p}_${String(i).padStart(5, '0')}`;
};

window.__resolve = async (ark) => {
  const r = await fetch(D + ark + '/manifest.json');
  if (r.status !== 200) return 'HTTP' + r.status;   // 403 = restricted, not absent
  const t = await r.text();
  return JSON.parse(t.slice(0, t.indexOf(',"streams"')) + '}').alternateId;
};

window.__exists = async (f, n) => {
  try { return (await fetch(D + window.__id(f, n) + '/manifest.json')).status === 200; }
  catch (e) { return false; }
};

/* Films can have GAPS. Probing three numbers and generalising is how this
   archive wrongly declared film 8166573 empty below image 1057, when images
   72-478 were sitting there. Step finely or binary-search both edges. */
window.__extent = async (f, lo, hi, step) => {
  const present = [];
  for (let n = lo; n <= hi; n += (step || 20)) if (await window.__exists(f, n)) present.push(n);
  return present;
};

window.__grid = async (id) => {
  const B = D + id + '/image_files';
  const ok = async (l, c, r) => {
    try { return (await fetch(`${B}/${l}/${c}_${r}.jpg`)).status === 200; } catch (e) { return false; }
  };
  let lvl = 0;
  for (const l of [14, 13, 12, 11, 10, 9, 8]) if (await ok(l, 0, 0)) { lvl = l; break; }
  if (!lvl) return null;
  let cols = 0, rows = 0;
  for (let c = 0; c < 40; c++) if (!await ok(lvl, c, 0)) { cols = c; break; }
  for (let r = 0; r < 40; r++) if (!await ok(lvl, 0, r)) { rows = r; break; }
  return { id, level: lvl, cols, rows };
};

window.__showId = async (id) => {
  const g = await window.__grid(id);
  if (!g) return { error: 'no tiles', id };
  const B = D + id + '/image_files/' + g.level;
  let h = '<head><style>html,body{margin:0;background:#222}table{border-collapse:collapse}'
        + 'td{padding:0;line-height:0}img{display:block}</style></head><body><table id=M>';
  for (let r = 0; r < g.rows; r++) {
    h += '<tr>';
    for (let c = 0; c < g.cols; c++) h += `<td><img data-u="${B}/${c}_${r}.jpg" src="${B}/${c}_${r}.jpg"></td>`;
    h += '</tr>';
  }
  /* documentElement.innerHTML, NOT document.write - an image document ends up
     with a null body and the mosaic vanishes. This also keeps window globals. */
  document.documentElement.innerHTML = h + '</table></body>';
  const imgs = [...document.images], sleep = ms => new Promise(r => setTimeout(r, ms));
  for (let p = 0; p < 6; p++) {
    await sleep(1200);
    const bad = imgs.filter(i => !(i.naturalWidth > 0));
    if (!bad.length) break;
    bad.forEach(i => { const u = i.dataset.u; i.removeAttribute('src'); i.src = u; });  // trap 1
  }
  await sleep(2500);                                                                     // trap 2
  const M = document.getElementById('M');
  return { ...g, missing: imgs.filter(i => !(i.naturalWidth > 0)).length, w: M.offsetWidth, h: M.offsetHeight };
};

window.__show = (film, img) => window.__showId(window.__id(film, img));

window.__view = (x, y, s) => {                                                           // trap 3
  const M = document.getElementById('M');
  M.style.transformOrigin = '0 0';
  M.style.transform = 'scale(' + s + ')';
  document.body.style.width = (M.offsetWidth * s) + 'px';
  document.body.style.height = (M.offsetHeight * s) + 'px';
  window.scrollTo(x * s, y * s);
  return { sx: scrollX, sy: scrollY };
};

window.__fit = () => {
  const M = document.getElementById('M');
  return window.__view(0, 0, (innerWidth - 4) / M.offsetWidth);
};

/* Thumbnails are PUBLIC - plain curl gets them, no session needed. A contact
   sheet is the cheapest way to find filming target boards, volume seams, blank
   leaves and near-blank expediente covers. It is how the informaciones reel was
   cut into volumes in a single screenshot. */
window.__sheet = async (film, from, to, step, wpx) => {
  let h = '<head><style>html,body{margin:0;background:#111;color:#0f0;font:10px monospace}'
        + 'div{display:inline-block;margin:1px;vertical-align:top}img{display:block;width:'
        + (wpx || 150) + 'px}</style></head><body>';
  const nums = [];
  for (let n = from; n <= to; n += step) nums.push(n);
  for (const n of nums) {
    const u = D + window.__id(film, n) + '/thumb_p200.jpg';
    h += `<div><img data-u="${u}" src="${u}"><span>${n}</span></div>`;
  }
  document.documentElement.innerHTML = h + '</body>';
  const imgs = [...document.images], sleep = ms => new Promise(r => setTimeout(r, ms));
  for (let p = 0; p < 5; p++) {
    await sleep(1200);
    const bad = imgs.filter(i => !(i.naturalWidth > 0));
    if (!bad.length) break;
    bad.forEach(i => { const u = i.dataset.u; i.removeAttribute('src'); i.src = u; });
  }
  await sleep(2000);
  return { n: nums.length, missing: imgs.filter(i => !(i.naturalWidth > 0)).length };
};
