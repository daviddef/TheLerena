/* THE WHOLE MENU, one list. 12 November 2026 (the menu regroup, PR A, MENU ONLY): the five menus other than Research became six
   (Start, Our line, People, Places & families, The name, Research). The header menu and the drawer (layouts/Base.astro) both read
   THIS list, so there is one place to change a label or move a page. No page was renamed, no address changed or retired and no
   page was written: every href below was already built, only its menu moved. Research is lib/research-menu.js (its shape unchanged).
     a menu is  [label, items]
     items     either a flat list of [href, label]            (a short menu: one column)
               or a list of groups { head, href?, items }   (a group is a column; `href` makes its heading a link; an item is [href, label])
   Where the old entries went:
     Start (10)          -> Home, The story, About stay; The trees, Our line drawn, The Timeline -> People > Drawn (Roots & Routes was in that list until 23 Nov 2026, when the page was removed);
                            The Atlas -> Places & families; What's new -> Research only (its group head, and the pulse button);
                            The DNA -> Research > Deep dives
     Our line (6)        -> The Name -> The name; The Lines -> Places & families; The Horses joins from "The work"
     The families (13)   -> the index (now the heading of the group), Taylor and Fernandez stay; the ten other family pages (Brayley, Temple, Pelaez, Gonzalez,
                            Lenguas, Cardozo, Juanico, Traibel, Alvarez, Larriera) leave the menu and are reached from /families/,
                            which links every one of them (proved in docs/menu-a-inventory.md)
     The work (6)        -> Argentina, Uruguay, South Africa -> Places & families; The Archives (naairs) and The British Archives ->
                            Research > Deep dives; The Horses -> Our line
     People & places (6) -> Blood relatives -> People > Drawn; Places -> Places & families
   THE FAMILY RULE (David, 12 Nov 2026, "own line first then A to Z"; Working Folder/Research Menu Rollout/family-menu-rule.md): a family
   entry is the bare surname; the heading of the group is the link to the /families/ index (so no sub-head repeats the label under it),
   then the archive's own line, then the other surnames A to Z (accents folded, particles ignored), then pages that are not a surname.
   This archive has no Lerena family page: its own line is TAYLOR (the family of Mary Septima Taylor, listed first at /families/), then Fernandez. The /families/ index itself lists Taylor, Brayley, Temple, Fernandez, Pelaez, Gonzalez,
   Lenguas, Cardozo, Juanico, Traibel, Alvarez, Larriera (not A to Z): reported, not changed.
   23 NOVEMBER 2026 (estate clean-up, David: "menus, do all"): People > Drawn is ONE link, to the hub /drawn/ (lib/drawn.js lists the five drawn pages with what
   each shows: Our line drawn, The trees, Blood relatives drawn, The Timeline, The Spine). The families group is "The families", whose first link is the hub
   "All the families" (/families/), then the archive's own line (Taylor) and Fernandez; every other family page is linked from that hub (docs/menu-reach.md).
   Roots & Routes is gone (Task A of the same clean-up). Research: its "Deep dives" heading opens /research/deep-dives/ (lib/research-menu.js).
   NOTE for the landing page at defranceski.com: it once read this archive's family labels to show its family pages. The menu now names
   three of them (the index, Taylor, Fernandez); every family page is still built at the address it had. */
import { navGroups } from "./research-menu.js";

export const MENU = [
  ["Start", [
    ["/", "Home"], ["/story/", "The story"], ["/about/", "About"],
  ]],
  ["Our line", [
    ["/direct-line/", "The Spine"], ["/estate/", "The Estate"], ["/passport/", "The Passport"], ["/enrolment-card/", "The Enrolment Card"],
    ["/horses/", "The Horses"],
  ]],
  ["People", [
    { head: "Lists", items: [
      ["/people/", "The People"], ["/who/", "Every Name"], ["/register/", "The Register"], ["/marriages/", "The Marriages"],
    ] },
    { head: "Drawn", href: "/drawn/", items: [] },
  ]],
  ["Places & families", [
    { head: "The families", items: [
      ["/families/", "All the families"], ["/taylor/", "Taylor"], ["/families/fernandez/", "Fernandez"],
    ] },
    { head: "Places", items: [
      ["/places/", "Places"], ["/atlas/", "The Atlas"], ["/lines/", "The Lines"], ["/argentina/", "Argentina"], ["/uruguay/", "Uruguay"],
      ["/south-africa/", "South Africa"],
    ] },
  ]],
  ["The name", [
    ["/name/", "The Name"],
  ]],
  ["Research", navGroups],
];
