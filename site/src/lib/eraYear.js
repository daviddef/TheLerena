/* The year a birth can honestly be given to an "at the time" note (kit/docs/era-notes.md), for THIS archive.
 *
 * The register's born_est is often an ESTIMATE: a year worked back from an age on a census, a ship list or a death entry, and printed on the page
 * as a bare year. A full date ("1882-02-22") comes from an act and is taken as it stands. A bare year is taken only where NO era boundary of
 * the place's region lies within ESTIMATE_YEARS of it, so that the note is true for any year the estimate could stand for. The kit does not
 * know this; it is stricter than the kit and never looser. tools/check-era-expect.py holds the built pages to the same rule, written
 * independently in Python.
 */
import { eraAt, plainYear, fold } from "@daviddef/archive-kit/lib/era.js";

export const ESTIMATE_YEARS = 5;

const own = (o, k) => o != null && typeof o === "object" && Object.prototype.hasOwnProperty.call(o, k);

/* Every year at which the region's ground changes hands, kept eras and refused eras alike (a refused era is still a change). */
export function boundaries(snap, region) {
  const out = new Set();
  const eras = own(snap.regions, region) && Array.isArray(snap.regions[region]) ? snap.regions[region] : [];
  for (const e of eras) { if (Number.isInteger(e.from)) out.add(e.from); if (Number.isInteger(e.to)) out.add(e.to); }
  for (const d of snap.dropped || []) {
    if (d.region !== region) continue;
    if (Number.isInteger(d.from)) out.add(d.from);
    if (Number.isInteger(d.to)) out.add(d.to);
  }
  return out;
}

/* The note for a birth, or null. `born` is the text the page prints in the Born row. */
export function birthEra(snap, place, born, estimate = ESTIMATE_YEARS) {
  const date = String(born == null ? "" : born).trim();
  const m = /^(\d{4})/.exec(date);
  const year = plainYear(date, m ? Number(m[1]) : null);
  if (year === null) return null;
  if (/^\d{4}$/.test(date)) {
    const region = snap && snap.places ? snap.places[fold(place)] : null;
    if (typeof region === "string") {
      for (const b of boundaries(snap, region)) if (b > year - estimate && b <= year + estimate) return null;
    }
  }
  return eraAt(snap, place, year);
}
