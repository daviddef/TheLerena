/* WHO SHARES A NAME (one page per person; 23 November 2026).
 *
 * Until now a NAME had a page of its own, /who/<name>/ ("Everyone in this archive called ...", one entry for a name one person
 * bears, a list for a name several bear), beside the PERSON's page at /people/<slug>/. David's rule: one page per person, and
 * each person's page links to the other people who carry the same name. The name pages are gone; their addresses redirect
 * (astro.config.mjs reads whoRedirects below) and this file is the one place that says which people share a name.
 *
 * THE SET IS THE ONE THE NAME PAGES USED, moved here unchanged in what it counts: every row of people.json with a name and a slug,
 * keyed on the slug of its whole register name (accents and case folded, the editorial bracket and all: "Pedro LERENA (b.1834)" and
 * "Pedro LERENA (b.1875)" are two names, as they were two name pages). So the people listed under "Others of the same name" are
 * exactly the people /who/ listed. On 23 November 2026 that is NOBODY: the register writes a different whole name for every person
 * (a bracket, a second given name, an initial tells two Pedros apart), so no name is borne by two of its rows. The section, the
 * redirects and the gate are all in place for the day two rows read the same. If David wants "same name" to mean the name before the
 * bracket, `nameKey` is the one line to change (the gate, the index and the redirects all read it).
 *
 * PURE: no imports, so astro.config.mjs can use it (it reads the JSON itself) and so can the pages.
 */
export const slugify = (s) => String(s ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "")
  .replace(/[^A-Za-z0-9]+/g, "-").replace(/^-+|-+$/g, "").toLowerCase();

/* the key a name page had: the slug of the whole register name */
export const nameKey = (p) => slugify(p.name);

/* @param people  people.json (an array of rows)
   @returns Map key -> { key, name, people } in people.json order, only for rows that had a name page (a name and a slug). */
export function nameSets(people) {
  const by = new Map();
  for (const p of people) {
    if (!p || !p.name || !p.slug) continue;
    const k = nameKey(p);
    if (!k) continue;
    if (!by.has(k)) by.set(k, { key: k, name: p.name, people: [] });
    by.get(k).people.push(p);
  }
  return by;
}

/* the first four-digit year of a date as the register writes it ("1882-02-22", "c.1815", "1842c"), or null */
export const yearIn = (v) => { const m = /(?<!\d)(1[0-9]{3}|20[0-9]{2})(?!\d)/.exec(String(v ?? "")); return m ? Number(m[1]) : null; };
const yearOf = (p) => yearIn(p.born);

/* oldest first (the first four-digit year of `born`), those with no year after, then slug order */
export const byAge = (a, b) => (yearOf(a) ?? 99999) - (yearOf(b) ?? 99999) || (a.slug < b.slug ? -1 : a.slug > b.slug ? 1 : 0);

/* THE FIRST BEARER of a set: the one a shared name's old address lands on. A bearer who is not living comes first (the page a
   search engine may show), then the earliest born, and a bearer with no year after those with one, then slug order. */
export function firstBearer(set) {
  const rank = (p) => [p.living === true ? 1 : 0, yearOf(p) ?? 99999, p.slug];
  return [...set.people].sort((a, b) => {
    const x = rank(a), y = rank(b);
    return x[0] - y[0] || x[1] - y[1] || (x[2] < y[2] ? -1 : x[2] > y[2] ? 1 : 0);
  })[0];
}

/* a set is SHARED when more than one person bears the name */
export const isShared = (set) => set.people.length > 1;

export const SECTION_ID = "others-of-this-name";

/* the old address of every name page -> where it goes now
   a name one person bears -> that person's page; a shared name -> its first bearer's page at the "Others of this name" section */
export function whoRedirects(people, base = "") {
  const out = {};
  for (const [key, set] of nameSets(people)) {
    const to = firstBearer(set);
    out[`/who/${key}`] = `${base}/people/${to.slug}/` + (isShared(set) ? `#${SECTION_ID}` : "");
  }
  return out;
}

/* the people who bear the same name as p, other than p: oldest first, then slug order; [] when nobody shares it */
export function othersOf(p, sets) {
  const set = sets.get(nameKey(p));
  return set ? set.people.filter((q) => q !== p && q.slug !== p.slug).sort(byAge) : [];
}
