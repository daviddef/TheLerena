/* The anchor of each correction on /corrections/ (kit docs/corrections.md, 17 November 2026): c-<day>-<hash of the headline>, from the kit's own
   corrIdMap over the rows in FILE order. /whats-new/ (src/lib/pulse.js hands buildPulse the same rows) links a "Corrected" card to it; the page
   puts it on the entry; a person page links a day to the day's FIRST entry (dayAnchor), because the day heading carries no id of its own. */
import { corrIdMap } from "@daviddef/archive-kit/lib/corrections.js";
import rows from "../data/corrections.json";

export const corrections = rows;
export const ids = corrIdMap(rows);
export const dayAnchor = (date) => {
  const r = rows.find((x) => x.date === date);
  return r ? ids.get(r) : "";
};
