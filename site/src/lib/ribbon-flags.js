/* The mini flags on the ribbon cards (27 October 2026; kit docs/ribbon-flags.md). src/data/ribbon-flags.json holds each card's
   flags by position, made by tools/build-ribbon-flags.py with the kit's own generator (see that tool for why they are not written
   into story.json and family-lines.json). These two functions put them on copies of the cards as a page draws them; the kit's
   StoryRibbon and FamilyRibbon then draw `card.flags` as they would anywhere. A flag whose place is not the one its card prints on
   that line (the file is stale) stops the build rather than drawing a flag over the wrong place. */
import flags from "../data/ribbon-flags.json";

const LINE = { from: "origin", at: "atPlace", spouse: "spouseOrigin" };
const placeOf = (card, line) => String(card[LINE[line]] || "").trim().replace(/^of\s+/, "");

function onCards(cards, list, where) {
  if (!list) return cards;
  if (list.length !== cards.length) throw new Error(`ribbon-flags.json: ${where} has ${list.length} entries for ${cards.length} cards; run python3 tools/build-ribbon-flags.py`);
  return cards.map((c, i) => {
    const fl = list[i];
    if (!fl || !fl.length) return c;
    for (const f of fl) {
      if (placeOf(c, f.line) !== f.place) throw new Error(`ribbon-flags.json: ${where} card ${i + 1} ${f.line} is not ${f.place}; run python3 tools/build-ribbon-flags.py`);
    }
    return { ...c, flags: fl };
  });
}

/* the story (story.json) with each ribbon card's flags */
export function storyWithFlags(book) {
  return { ...book, ribbon: { ...book.ribbon, cards: onCards(book.ribbon?.cards || [], flags.story, "the story") } };
}

/* one family of family-lines.json with each card's flags */
export function familyWithFlags(fam) {
  if (!fam) return fam;
  return { ...fam, cards: onCards(fam.cards || [], flags.families?.[fam.id], `family ${fam.id}`) };
}
