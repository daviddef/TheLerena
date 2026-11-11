/* What is new here, and the archive in numbers: the kit computes it at build time from this archive's own logs (kit/docs/whats-new.md).
   This file is the only Lerena-specific part: which JSON is which, and the one count no log holds. */
import { buildPulse } from "@daviddef/archive-kit/lib/pulse.js";
import searched from "../data/searched.json";
import corrections from "../data/corrections.json";
import worklist from "../data/worklist.json";
import people from "../data/people.json";

export const pulse = buildPulse({
  searched, corrections, worklist,
  counts: { people: people.length },
});
