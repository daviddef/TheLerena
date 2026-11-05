/* The people of the register in the SHAPE the kit's story functions read (kit lib/personstory.js: byId[id] = { id, given, sur, sex, by, bye, dy, dye, bp, line,
   href, father, mother, kids[], spouse[], saidLiving }), built ONCE from people.json for every person page. Nothing is added: a living person has no
   years and no place here (people.json holds none), a relative people.json leaves out (held out) is not here, and the kit's own living rule decides how each
   is drawn (kit familyOf / famNode). The name is the register's, with its capitals folded and a bracketed qualifier left out (as the page's own header does). */
import people from "../data/people.json";
import { splitQualifier, displayName } from "@daviddef/archive-kit/lib/person.js";

const said = (v) => { const s = String(v == null ? "" : v).trim(); return s && s !== "-" && s !== "?" ? s : ""; };
const yearOf = (v) => { const m = /\b(1[0-9]\d\d|20\d\d|[5-9]\d\d)\b/.exec(said(v)); return m ? Number(m[1]) : null; };
const circa = (v) => /c/i.test(String(v || "")) && /\d{4}/.test(String(v || ""));

export const byId = (() => {
  const out = {};
  for (const q of people) {
    out[q.slug] = { id: q.slug, given: splitQualifier(displayName(q.name, {})).name, sur: "", sex: "",
      by: q.living ? null : yearOf(q.born), bye: !q.living && circa(q.born),
      dy: q.living ? null : yearOf(q.died), dye: !q.living && circa(q.died),
      bp: q.living ? "" : said(q.birthplace), line: q.isLine ? 0 : 1, href: `/people/${q.slug}/`,
      father: null, mother: null, kids: [], spouse: [], saidLiving: q.living === true };
  }
  for (const q of people) {
    const o = out[q.slug];
    if (q.father && out[q.father.slug]) o.father = q.father.slug;
    if (q.mother && out[q.mother.slug]) o.mother = q.mother.slug;
    o.kids = (q.children || []).map((c) => c.slug).filter((x) => out[x]);
    o.spouse = (q.spouses || []).map((c) => c.slug).filter((x) => out[x] && x !== q.slug);
  }
  return out;
})();
