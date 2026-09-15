/* People carrying the name, grouped by what this archive has decided about
   each — the status field, which is the same gate /marriages/ uses. */
import people from "../data/people.json";
const ORDER = [["connected","Connected to the line"],["high","Unplaced — high interest"],
  ["interest","Unplaced — of interest"],["unplaced","Unplaced"],
  ["excluded","Excluded — the name is coincidental"]];
const bySur = (list) => {
  const m = {};
  for (const p of list) (m[(p.surname || "—").trim()] ||= []).push(p);
  return Object.entries(m).map(([s, l]) => ({ surname: s, n: l.length }))
    .sort((a, b) => b.n - a.n);
};
export const chartGroups = ORDER.map(([k, label]) => ({
  key: k, label, families: bySur(people.filter((p) => (p.status || "unplaced") === k)),
})).filter((g) => g.families.length);
