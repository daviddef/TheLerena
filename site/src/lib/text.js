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
