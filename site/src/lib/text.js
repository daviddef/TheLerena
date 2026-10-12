/* The TSVs mark emphasis as *** like this ***. Nothing used to convert it, so 362 literal
   asterisks were rendering to readers across 38 pages. Convert at render time rather than
   editing the data: the asterisks are readable in the TSV, which is the point of the TSV.

   Returns an HTML string, so callers must use set:html. Everything is escaped first, so
   the data can never inject markup - only the *** markers become tags. */

const ESC = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };

export function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ESC[c]);
}

/* FamilySearch arks are written bare in the TSVs - 3:1:3QHK-MQL4-NQWN for an image,
   1:1:6TH8-DVXH for an index entry. They are the archive's citations, and for a long time
   they rendered as dead text: 72 arks across the site, 11 of them clickable. A citation the
   reader cannot follow is doing only half its job. The NAAN is always 61903.

   Runs AFTER emph() so it only ever sees escaped text plus <strong> tags - there are no
   arks inside attributes at that point, so this cannot corrupt markup it has itself made. */
const ARK = /\b([0-9]:[0-9]:[A-Z0-9]{4,}(?:-[A-Z0-9]+)*)\b/g;

export function arkify(html) {
  return String(html ?? "").replace(
    ARK,
    '<a class="ark" href="https://www.familysearch.org/ark:/61903/$1" rel="noopener">$1</a>'
  );
}

export function emph(s) {
  return arkify(esc(s).replace(/\*\*\*\s*(.+?)\s*\*\*\*/gs, "<strong>$1</strong>"));
}

/* For places that want the text with no markup at all - a title attribute, a meta
   description, the search index. */
export function plain(s) {
  return String(s ?? "").replace(/\*\*\*\s*(.+?)\s*\*\*\*/gs, "$1");
}

/* A SHORT LEAD FROM A LONG NOTE, for the line under a page title.
   A person page used to pass the WHOLE note as its dek and then print the same note again under
   "What is known". 588 of 692 people have a note over 160 characters, 112 of them over 1,500 and
   the longest 21,547, so most pages opened with a wall of unemphasised text that the page then
   repeated. Found on 13 October 2026 by looking at a rendered page rather than measuring one -
   no width or overflow check could have seen it.
   Takes the first sentence if it is a sensible length, else cuts at a word boundary. Notes of
   160 characters or fewer are returned whole, which is exactly what they were before. The full
   note is never lost: it is still printed, with its emphasis, in its own section. */
export function lead(s, max = 230) {
  const t = plain(s).replace(/\s+/g, " ").trim();
  if (t.length <= 160) return t;
  // A full stop is NOT a sentence end after an honorific/abbreviation ("Dr. Bordoni", "D. Pedro",
  // "No. 353") or after a lone capital, which is an initial ("Pedro A. Lerena"). Without this the
  // first version cut six pages off mid-name: "...named by the cura Dr."
  const re = /(?<!\b(?:Dr|Dra|Dn|Dna|D|Sr|Sra|St|Sta|No|Nos|Mr|Mrs|Fr|Don|Dona|Gral|Cap|Exmo|Ilmo|Rev|Vda|vs|cf|ca|c|fl|ff|ark|fol|p|pp|b|d|m|s))(?<!\b[A-Z])[.!?](?=\s+[A-Z"'(\u201c*])/g;
  let m;
  while ((m = re.exec(t))) {
    const end = m.index + 1;
    if (end > max) break;
    if (end >= 50) return t.slice(0, end);
  }
  const cut = t.slice(0, max);
  const sp = cut.lastIndexOf(" ");
  return cut.slice(0, sp > 100 ? sp : max).replace(/[,;:\s]+$/, "") + "\u2026";
}
