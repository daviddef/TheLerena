/* What is new here, and the archive in numbers: the kit computes it at build time from this archive's own logs (kit/docs/whats-new.md).
   This file is the only Lerena-specific part: which JSON is which, and the one count no log holds. */
import { buildPulse } from "@daviddef/archive-kit/lib/pulse.js";
import { loadReceipts } from "@daviddef/archive-kit/lib/receipts.js";
import searched from "../data/searched.json";
import corrections from "../data/corrections.json";
import worklist from "../data/worklist.json";
import people from "../data/people.json";

export const pulse = buildPulse({
  searched, corrections, worklist,
  counts: { people: people.length },
  /* the Atlas's receipt for each search row (null on any failure: a build never fails because the Atlas is unreachable).
     searched.json is passed UNMAPPED, so a row's key on the page is the key the Atlas importer wrote. */
  receipts: await loadReceipts("lerena"),
});
