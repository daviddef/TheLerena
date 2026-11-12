/* THE RESEARCH MENU: one list, read by the header menu (layouts/Base.astro), the drawer, the hub page /research/ and the two group
   pages. 12 November 2026 (the research-menu trial, wave 2, after the Defranceski archive): "Evidence" and "Investigations" became
   one "Research" menu with three groups. Nothing is renamed or removed: every item keeps the address it had, and the labels of the
   eight pages the estate's Evidence canon names (kit data/evidence-menu.json) are unchanged. `asks` is the canon's question for
   those pages. This archive's Roadmap goes with the To do group (it ranks the routes still to be worked); Hypotheses and the
   papers in the house are deep dives under Sources & method. */
export const RESEARCH = [
  { id: "to-do", head: "To do", href: "/research/to-do/",
    dek: "What is not known yet, what has been asked of other people, what is being worked on, and which routes come next.",
    items: [
      { href: "/open-questions/", label: "Open Questions", asks: "What is not known, and what would settle it?" },
      { href: "/errands/", label: "Errands", asks: "What has been asked of other people, or needs someone standing in a place?" },
      { href: "/worklist/", label: "The work list", asks: "What is being done, by whom, since when?" },
      { href: "/roadmap/", label: "Roadmap", asks: "Which routes are finished, which are live, and which need a person rather than a search?" },
    ] },
  { id: "whats-new", head: "What's new", href: "/whats-new/",
    dek: "What was read, found and taken back lately, newest first, and the same record in full.",
    items: [
      { href: "/searched/", label: "What Has Been Read", asks: "What was looked at, and what did it not turn up?" },
      { href: "/corrections/", label: "Corrections", asks: "What did this archive get wrong?" },
      { href: "/changes/", label: "What changed", asks: "What happened, most recent first?" },
    ] },
  { id: "sources-and-method", head: "Sources & method", href: "/research/sources-and-method/",
    dek: "What this archive stands on, how it reads a register, and the long studies that sit beside them.",
    items: [
      { href: "/sources/", label: "Sources", asks: "What does this stand on, and where do I check?" },
      { href: "/method/", label: "Method", asks: "What would make you believe or not believe this?" },
      { sub: "Deep dives", id: "deep-dives",
        note: "Long studies, each of one proposition or one set of papers. They are linked from the Sources page too.",
        items: [
          { href: "/hypotheses/", label: "Hypotheses" },
          { href: "/family-papers/", label: "The papers in the house" },
        ] },
    ] },
];
/* the header menu's shape: [group, ...] with { head, href, items: [[href, label] | { sub }] } */
export const navGroups = RESEARCH.map((g) => ({
  head: g.head, href: g.href,
  items: g.items.flatMap((x) => x.sub ? [{ sub: x.sub }, ...x.items.map((y) => [y.href, y.label])] : [[x.href, x.label]]),
}));
