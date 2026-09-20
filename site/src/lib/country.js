/* Which country a place belongs to, in today's borders.
 *
 * WHY THIS IS A FILE AND NOT NINE HAND-TYPED PILLS. On 14 September 2026 the Taylor page
 * carried its ten siblings as a hardcoded array duplicating taylor-line.tsv, the TSV gained
 * five husbands' names, and the page went on saying "m. Dalling" for days. Anything written
 * out by hand in more than one place drifts. The tree pages all ask the same question of the
 * same strings, so they ask it here.
 *
 * TWO TRAPS THIS FAMILY SETS, AND BOTH ARE LIVE IN THE DATA:
 *
 *   1. ROSARIO IS TWO TOWNS. "Rosario, Santa Fe" is the Argentine city Pablo Armando was born
 *      in. "Rosario, Colonia" and "Rosario / Colla, Colonia" are a town in URUGUAY, and the
 *      register holds people from both. A substring match on "rosario" gets one of them wrong
 *      every time, so Colonia is tested BEFORE Santa Fe.
 *
 *   2. CORDOBA IS AMBIGUOUS AND MUST STAY THAT WAY. Sancho Llerena is "natural de Cordova la
 *      Llana" and the archive has never settled whether that is Andalusia or the Argentine
 *      Cordoba - it is one of the open questions. "Cordoba, Argentina" is explicit and safe;
 *      bare "Cordoba" returns NULL rather than picking a side. A pill is an assertion, and
 *      this archive does not assert that one.
 *
 * ANACHRONISM, ADMITTED. These are modern countries. Canelones in 1791 was the Banda Oriental
 * of the Spanish empire and Uruguay did not exist for another thirty-seven years. The pages
 * that render these say so in their legend rather than letting a pill quietly claim it.
 */

export const COUNTRIES = {
  uy: "Uruguay",
  ar: "Argentina",
  za: "South Africa",
  en: "England",
  es: "Spain",
  br: "Brazil",
  it: "Italy",
  pe: "Peru",
};

/* Ordered. First match wins, so the specific sits above the general. */
const RULES = [
  // --- the Rosario split, before anything matches bare "rosario" ---
  [/\bcolonia\b|\bcolla\b/i, "uy"],
  [/rosario\s*[,/]?\s*santa\s*fe|santa\s*fe/i, "ar"],

  // --- Uruguay ---
  [/montevideo|canelones|trinidad|flores|maldonado|salto|paysandu|florida|cerro\s*largo|san\s*jos[eé]|cord[oó]n|uruguay|banda\s*oriental|estado\s*oriental|r\.?\s*oriental/i, "uy"],

  // --- Argentina ---
  [/buenos\s*aires|entre\s*r[ií]os|gualeguaych|tucum[aá]n|mendoza|corrientes|jujuy|catamarca|santa\s*cruz|chacabuco|recoleta|capital\s*federal|misiones|cayasta|garay|c[oó]rdoba,\s*argentina|argentin/i, "ar"],

  // --- South Africa. "Cape Colony" and "Cape Province" are the same place under earlier
  //     names and are in this register; they belong on the modern country like everything else.
  [/cape\s*town|cape\s*colony|cape\s*province|newlands|wynberg|johannesburg|germiston|pretoria|transvaal|natal|south\s*africa/i, "za"],

  // --- England ---
  [/northam|bideford|devon|braunton|westleigh|appledore|london|suffolk|worlingworth|england/i, "en"],

  // --- Spain ---
  [/asturias|andalusia|andaluz|logro[nñ]o|sevilla|seville|madrid|zaragoza|llerena|spain|espa[nñ]a/i, "es"],

  // --- the rest of the crossings this register holds ---
  [/pernambuco|brazil|brasil/i, "br"],
  [/\blima\b|peru/i, "pe"],
  [/\bitaly\b|italia/i, "it"],
];

/* Places that look decidable and are not. Tested before the rules, and they win. */
const AMBIGUOUS = [
  /^\s*c[oó]rdoba\s*$/i,          // Andalusia or Argentina - an open question here
  /^\s*c[oó]rdova\s+la\s+llana/i, // Sancho's own phrase, same question
  /^\s*rosario\s*$/i,             // Santa Fe in Argentina, or Colonia in Uruguay - see above
];

/** The two-letter code for a place string, or null when it cannot be said. */
export function countryOf(place) {
  const s = String(place ?? "").trim();
  if (!s || s === "-") return null;
  if (AMBIGUOUS.some((re) => re.test(s))) return null;
  for (const [re, code] of RULES) if (re.test(s)) return code;
  return null;
}

/** Codes for several places at once, de-duplicated, in the order given. */
export function countriesOf(...places) {
  const out = [];
  for (const p of places) {
    const c = countryOf(p);
    if (c && !out.includes(c)) out.push(c);
  }
  return out;
}

/** One pill, as an HTML string. Used where a component only accepts markup. */
export function pill(code) {
  return COUNTRIES[code]
    ? `<span class="tag place ${code}">${COUNTRIES[code]}</span>`
    : "";
}

/** Several pills, space separated. Returns "" when nothing is known. */
export function pills(codes) {
  return (codes || []).map(pill).filter(Boolean).join(" ");
}
