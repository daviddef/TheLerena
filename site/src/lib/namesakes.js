/* The people who share a name, as the pages draw them (see namesets.js for which people, and why).
   Each entry is what the old /who/<name>/ page showed beside a bearer, and nothing more: the name, the life span and the birthplace of
   a person who has died, and for a living person only the name and the town and country (no life, no birthplace string). */
import people from "../data/people.json";
import { nameSets, othersOf, byAge, firstBearer, isShared, nameKey, slugify, SECTION_ID } from "./namesets.js";
import { u } from "./url.js";

export const SETS = nameSets(people);
export { SECTION_ID, slugify, isShared, nameKey, byAge };

/* this register writes «-» for «not known» */
const said = (v) => { const t = String(v ?? "").trim(); return t && t !== "-" && t !== "?" ? t : ""; };

export const entry = (q) => q.living === true
  ? { name: q.name, slug: q.slug, href: u(`/people/${q.slug}/`), life: "", where: [q.town, q.country].filter(Boolean).join(", "), living: true }
  : { name: q.name, slug: q.slug, href: u(`/people/${q.slug}/`), life: [said(q.born), said(q.died)].filter(Boolean).join(" – "), where: said(q.birthplace), living: false };

/* the other people of p's name, oldest first: [] when nobody shares it */
export const othersFor = (p) => othersOf(p, SETS).map(entry);

export const firstOf = (set) => firstBearer(set);
