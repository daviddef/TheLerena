/* The TSVs mark emphasis as *** like this ***. Nothing used to convert it, so 362 literal
   asterisks were rendering to readers across 38 pages. Convert at render time rather than
   editing the data: the asterisks are readable in the TSV, which is the point of the TSV.

   Returns an HTML string, so callers must use set:html. Everything is escaped first, so
   the data can never inject markup - only the *** markers become tags. */

const ESC = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };

export function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ESC[c]);
}

export function emph(s) {
  return esc(s).replace(/\*\*\*\s*(.+?)\s*\*\*\*/gs, "<strong>$1</strong>");
}

/* For places that want the text with no markup at all - a title attribute, a meta
   description, the search index. */
export function plain(s) {
  return String(s ?? "").replace(/\*\*\*\s*(.+?)\s*\*\*\*/gs, "$1");
}
