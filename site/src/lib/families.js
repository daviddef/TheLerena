/* THE FAMILY PAGES, worked out from the register.   17 October 2026.

   /families/ and /families/<slug>/ are BUILT, not written. data/families.tsv says which spellings count as one
   name and where this archive has already written the family up; everything else on a family page - who carries
   the name, where, between which years, how the archive knows them, which other families they are joined to - is
   worked out here from site/src/data/people.json, the same file every person page is built from. A count on a
   family page therefore cannot drift from the register, and nothing is claimed about a family that the register
   does not hold.

   WHO IS COUNTED. Never a living person, and never a person held out of publication (people.json `noindex`):
   the filter below runs before anything is counted, listed or linked, so a family page makes nobody easier to find
   than their own page does. tools/check-families.py checks the BUILT pages against the same rule independently.

   WHAT "CARRIES THE NAME" MEANS. The register writes the surname in capitals, and a Spanish second surname in
   ordinary case straight after it: "Maria Margarita Luisa ZALDUONDO Lerena" carries Zalduondo and Lerena. A middle
   name does not count ("Isabella Temple TAYLOR" is a Taylor, not a Temple), and neither does anything inside
   brackets, which is where the register keeps a relative's name ("... (m. Eduardo Avelino Zalduando 1927)").
   A name with no capitals at all ("Catherine Mary Sophia Booyzen") is read by its last word.

   NOTHING IS FOLDED except by data/families.tsv, and that file folds only what the archive has already decided. */

import people from "../data/people.json";
import fams from "../data/families.json";
import places from "../data/places.json";

export const fold = (s) =>
  String(s ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

const strip = (n) => String(n ?? "").replace(/\([^)]*\)/g, " ");
const CAPS = /^[A-ZÁÉÍÓÚÑ]{3,}$/;
const TITLE = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+$/;

/* the surname words of a register name, folded, as above */
export function surnameWords(name) {
  const words = strip(name).split(/\s+/).filter(Boolean);
  let lastCaps = -1;
  words.forEach((w, i) => { if (CAPS.test(w)) lastCaps = i; });
  const out = [];
  if (lastCaps < 0) {
    const last = words[words.length - 1];
    if (last && TITLE.test(last)) out.push(last);
    return out;
  }
  words.forEach((w) => { if (CAPS.test(w)) out.push(w); });
  for (let i = lastCaps + 1; i < words.length && TITLE.test(words[i]); i++) out.push(words[i]);
  return out;
}

/* a person who may appear on a family page at all */
export const listable = (p) => !!p && !p.living && !p.noindex && !!p.slug;

const BY_SLUG = new Map(people.map((p) => [p.slug, p]));
export const personBySlug = (s) => BY_SLUG.get(s);

const yearsOf = (p) =>
  [...`${p.born || ""} ${p.died || ""}`.matchAll(/\b(1[5-9]\d\d|20\d\d)\b/g)].map((m) => Number(m[1]));
const bornYear = (p) => (String(p.born || "").match(/\b(1[5-9]\d\d|20\d\d)\b/) || [])[1] || "";

export const STATUS = {
  connected: "Connected to the line",
  high: "Unplaced · high interest",
  interest: "Unplaced · of interest",
  unplaced: "Unplaced",
  excluded: "Excluded",
};

/* the spellings of the surname itself that the archive has seen written (data/name-variants.tsv) */
const NAME_FORMS = new Set(["lerena", "llerena", "serena", "gerena", "perena", "lorena", "leresa",
  "larena", "lerina", "lerrena", "levena", "herencia"]);

const famList = fams.map((f) => ({
  ...f,
  tokens: new Set(f.forms.split("|").map(fold)),
  read: String(f.read || "").split("|").filter(Boolean).map((x) => {
    const [label, href] = x.split("~");
    return { label, href };
  }),
}));
export const families = famList;

/* surname word -> where the archive writes that family up */
const DOORS = new Map();
for (const f of famList) for (const t of f.tokens) DOORS.set(t, `/families/${f.slug}/`);
DOORS.set("taylor", "/taylor/");
export const doorFor = (token) => DOORS.get(token) || null;

const cap = (s) => (s ? s[0].toUpperCase() + s.slice(1) : s);

const placeName = new Map(places.map((x) => [x.slug, x.name]));

function bearersOf(tokens) {
  return people
    .filter((p) => listable(p) && surnameWords(p.name).some((w) => tokens.has(fold(w))))
    .sort((a, b) => (bornYear(a) || "9999").localeCompare(bornYear(b) || "9999") || a.name.localeCompare(b.name));
}

/* the relatives a person page draws, restricted to people who may be listed */
function relatives(p) {
  const out = [];
  const add = (node, kind) => { if (node && listable(BY_SLUG.get(node.slug))) out.push({ kind, node }); };
  add(p.father, "parent");
  add(p.mother, "parent");
  (p.spouses || []).forEach((n) => add(n, "spouse"));
  (p.children || []).forEach((n) => add(n, "child"));
  return out;
}

/* does a person's line of descent reach somebody on the direct line, through people who may be listed? */
function reachesLine(slug, seen = new Set(), depth = 0) {
  const p = BY_SLUG.get(slug);
  if (!listable(p) || seen.has(slug) || depth > 6) return false;
  seen.add(slug);
  if (p.isLine) return true;
  return (p.children || []).some((c) => reachesLine(c.slug, seen, depth + 1));
}

export function buildFamily(f) {
  const bearers = bearersOf(f.tokens);
  const slugs = new Set(bearers.map((p) => p.slug));

  /* spellings actually found, in the form the register writes them */
  const seenForms = new Map();
  for (const p of bearers) for (const w of surnameWords(p.name)) {
    if (f.tokens.has(fold(w))) seenForms.set(cap(w.toLowerCase()), (seenForms.get(cap(w.toLowerCase())) || 0) + 1);
  }
  const spellings = [...seenForms.entries()].sort((a, b) => b[1] - a[1]).map(([w]) => w);

  const yrs = bearers.flatMap(yearsOf);
  const span = yrs.length ? [Math.min(...yrs), Math.max(...yrs)] : null;
  const dated = bearers.filter((p) => yearsOf(p).length).length;

  const byStatus = {};
  for (const p of bearers) byStatus[p.status || "unplaced"] = (byStatus[p.status || "unplaced"] || 0) + 1;

  /* where: the place each person is filed under */
  const pl = new Map();
  for (const p of bearers) {
    const key = p.placeSlug || "";
    if (!key) continue;
    const e = pl.get(key) || { slug: key, name: placeName.get(key) || p.place || key, n: 0 };
    e.n++; pl.set(key, e);
  }
  const where = [...pl.values()].sort((a, b) => b.n - a.n || a.name.localeCompare(b.name));
  const unfiled = bearers.filter((p) => !p.placeSlug).length;

  /* how the archive knows the relationships drawn for these people */
  const seenEdge = new Set();
  let reg = 0, tree = 0;
  const conn = new Map();
  const couples = [];
  const coupleSeen = new Set();
  let alsoLerena = 0;
  for (const p of bearers) {
    if (surnameWords(p.name).some((w) => fold(w) === "lerena")) alsoLerena++;
    for (const { kind, node } of relatives(p)) {
      const key = [p.slug, node.slug].sort().join("|");
      if (!seenEdge.has(key)) {
        seenEdge.add(key);
        if (node.via === "tree") tree++; else reg++;
      }
      if (kind === "spouse" && !coupleSeen.has(key)) {
        coupleSeen.add(key);
        couples.push({ a: p, b: BY_SLUG.get(node.slug), note: node.note || "", via: node.via || "" });
      }
      const other = BY_SLUG.get(node.slug);
      if (slugs.has(other.slug)) continue;
      const toks = new Set(surnameWords(other.name).map(fold).filter((t) => !f.tokens.has(t)));
      let touchedNameForm = false;
      for (const t of toks) {
        if (NAME_FORMS.has(t)) { touchedNameForm = true; continue; }
        const e = conn.get(t) || { token: t, label: cap(t), who: new Set(), kinds: { spouse: 0, parent: 0, child: 0 } };
        if (!e.who.has(other.slug)) { e.who.add(other.slug); e.kinds[kind]++; }
        conn.set(t, e);
      }
      if (touchedNameForm) {
        const e = conn.get("lerena") || { token: "lerena", label: "Lerena", who: new Set(), kinds: { spouse: 0, parent: 0, child: 0 } };
        if (!e.who.has(other.slug)) { e.who.add(other.slug); e.kinds[kind]++; }
        conn.set("lerena", e);
      }
    }
  }
  /* one chip per family: the spellings of a name this archive counts as one (Brailey, Brayley) are merged */
  const merged = new Map();
  for (const e of conn.values()) {
    const href = e.token === "lerena" ? "/name/#s-variants" : doorFor(e.token);
    const fam = href && href.startsWith("/families/") ? famList.find((x) => href === `/families/${x.slug}/`) : null;
    const key = fam ? fam.slug : e.token;
    const m = merged.get(key) || { label: fam ? fam.name : e.label, href, who: new Set() };
    e.who.forEach((s) => m.who.add(s));
    merged.set(key, m);
  }
  const connections = [...merged.values()]
    .map((m) => ({ label: m.label, n: m.who.size, href: m.href }))
    .sort((a, b) => b.n - a.n || a.label.localeCompare(b.label));

  /* the direct line */
  const onLine = bearers.filter((p) => p.isLine);
  const ancestors = bearers.filter((p) => !p.isLine && reachesLine(p.slug));
  const marriedIn = bearers.filter((p) => !p.isLine && !ancestors.includes(p) &&
    (p.spouses || []).some((s) => BY_SLUG.get(s.slug)?.isLine && listable(BY_SLUG.get(s.slug))));

  return {
    fam: f, bearers, spellings, span, dated, byStatus, where, unfiled,
    reg, tree, edges: reg + tree, connections, couples, alsoLerena,
    onLine, ancestors, marriedIn,
  };
}

export const lifeOf = (p) => [p.born, p.died].filter((x) => x && x !== "-").join(" – ");
export const placeOf = (p) => (p.birthplace && p.birthplace !== "-" ? p.birthplace : p.where && p.where !== "-" ? p.where : "");
