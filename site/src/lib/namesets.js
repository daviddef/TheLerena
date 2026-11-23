/* WHO SHARES A NAME (one page per person; 23 November 2026).
 *
 * Until now a NAME had a page of its own, /who/<name>/ ("Everyone in this archive called ...", one entry for a name one person
 * bears, a list for a name several bear), beside the PERSON's page at /people/<slug>/. David's rule: one page per person, and
 * each person's page links to the other people who carry the same name. The name pages are gone; their addresses redirect
 * (astro.config.mjs reads whoRedirects below) and this file is the one place that says which people share a name.
 *
 * WHAT "THE SAME NAME" MEANS (David, 23 November 2026, second step). The register writes a bracket after a name to tell its people
 * apart or to say what it knows of them ("Gilberto LERENA (b.1879, arr. 1928)", "Eduardo LERENA (godfather, Cordon 1900-02)",
 * "Gilberto LERENA (Gilberto Justiniano LERENA LENGUAS)"). Two rows whose names are the same once the bracket is dropped are
 * namesakes: `nameKey` is the slug of the name before its first "(", accents and case folded, so 1,537 people fall in 1,458 names and
 * 60 of those are borne by more than one row (139 people). A square bracket "[infant]" is part of the name and stays. A bracket
 * can say that two rows are two people (the elder / the younger) or leave it open that they are one man (a godfather and a groom): the
 * page says "They are different people: this archive does not join two of them without a record that says to", and joins none.
 *
 * THE OLD ADDRESSES. /who/<name>/ was keyed on the WHOLE register name, bracket and all (`oldKey`), so all 1,537 of those keys still
 * answer. A key that carries a bracket named one row, so it goes to that person's page (at #others-of-this-name when the page
 * lists others). A key that is the bare name of a shared set (nobody wrote a bracket) is a shared name's address: it goes to the
 * FIRST bearer's page at #others-of-this-name (not living, earliest born, then slug order).
 *
 * PURE: no imports, so astro.config.mjs can use it (it reads the JSON itself) and so can the pages.
 */
export const slugify = (s) => String(s ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "")
  .replace(/[^A-Za-z0-9]+/g, "-").replace(/^-+|-+$/g, "").toLowerCase();

/* the key an old name page had: the slug of the whole register name, bracket and all */
export const oldKey = (p) => slugify(p.name);

/* the key of the NAME: the register name before its first "(" (a name that is only a bracket keeps the whole), accents and case folded */
export const bareName = (p) => String(p.name ?? "").replace(/\s*\(.*$/s, "").trim() || String(p.name ?? "");
export const nameKey = (p) => slugify(bareName(p)) || oldKey(p);

/* @param people  people.json (an array of rows)
   @returns Map key -> { key, name, people } in people.json order, only for rows that had a name page (a name and a slug); `name` is the first bearer's register name, `bare` the same before its bracket. */
export function nameSets(people) {
  const by = new Map();
  for (const p of people) {
    if (!p || !p.name || !p.slug) continue;
    const k = nameKey(p);
    if (!k) continue;
    if (!by.has(k)) by.set(k, { key: k, name: p.name, bare: bareName(p), people: [] });
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

/* a set is SHARED when more than one person bears the name (before the bracket) */
export const isShared = (set) => set.people.length > 1;

export const SECTION_ID = "others-of-this-name";

/* the old address of every name page -> where it goes now (see the head of this file). One entry per old key (the whole register name). */
export function whoRedirects(people, base = "") {
  const sets = nameSets(people);
  const out = {};
  for (const p of people) {
    if (!p || !p.name || !p.slug) continue;
    const key = oldKey(p), set = sets.get(nameKey(p));
    const bare = key === set.key && isShared(set);          // the address of a shared NAME, written without a bracket
    const to = bare ? firstBearer(set) : p;
    out[`/who/${key}`] = `${base}/people/${to.slug}/` + (isShared(set) && to.living !== true ? `#${SECTION_ID}` : "");
  }
  return out;
}

/* the people who bear the same name as p, other than p: oldest first, then slug order; [] when nobody shares it */
export function othersOf(p, sets) {
  const set = sets.get(nameKey(p));
  return set ? set.people.filter((q) => q !== p && q.slug !== p.slug).sort(byAge) : [];
}
