# Shared across both archives — read this before writing to anybody

**Two archives, one mailbox.** *The Luwinski Family* and *The Lerena / Booyzen Family* are
separate projects with separate sites and separate notes, but they share:

- one email account — **david.defranceski@gmail.com**
- one National Archives of South Africa
- one Reading Room contact
- one private researcher
- and, increasingly, one set of South African tools

**On 15 September 2026 that cost a duplicated letter.** The Luwinski session wrote to the
National Archives without knowing the Lerena session had written three days earlier, been
answered, replied to, and already engaged the researcher the archives recommended. It cc'd a
woman who had been thanked fourteen hours before, about a different family.

> ## THE RULE
> **Before writing to any institution, search the sent mail.** One query. It would have caught
> all three of that day's problems at once.

---

## Shared contacts, and their live state

| Who | Address | State |
|---|---|---|
| **National Archives (NARSSA), Pretoria — general** | `Enquiries2@dsac.gov.za` | **Live. Answers.** Used 12 Sep, answered 14 Sep. |
| **Ms Mavis Xaba**, Archivist Assistant, Reading Room | `mavisx@dsac.gov.za` | **Live, helpful, fast.** Already written to twice. Do not open a third thread. |
| Nontembeko Matika | `nontembekom@dsac.gov.za` | cc'd 12 Sep |
| **Private researcher** (referred by Ms Xaba) | `digitalphoto@icon.co.za` | **Commissioned 14 Sep** for six Booyzen MHG files. Paid work. |
| ~~National Archives, old domain~~ | ~~`enquiries@dac.gov.za`~~ | **DEAD DOOR.** Department renamed DAC → DSAC. Live MX, no bounce, nobody listening. |
| Master of the High Court, **Cape Town** — files ending 1 | `DKeyster@justice.gov.za` | Live. Auto-reply diverts only *appointment* queries. |
| Master of the High Court, Cape Town — Assistant Master | ~~`NMphetshwa@justice.gov.za`~~ | **Has left the Deceased Estates section.** |
| Master of the High Court, **Johannesburg** — files ending 4 | Ms Morwanki Sello | Used for estate 12294/2023 |
| ~~Masters Johannesburg general~~ | ~~`MastersJohannesburg@justice.gov.za`~~ | **NOT IN USE** — the department's own PDF says so in capitals. |
| Arquivo Histórico Militar, Lisbon | `ahm@exercito.pt` | Live, acknowledged in nine minutes |
| ~~Arquivo Histórico Militar~~ | ~~`ahm@mail.exercito.pt`~~ | **BOUNCED.** Domain does not exist. |

## Constraints that apply to both archives

1. **MHG estate files at the National Archives are BOUND** and cannot be scanned or emailed.
   *— Ms Mavis Xaba, 14 September 2026.* The "just send me the J294" framing does not work
   there. It **does** work at the Master's offices, which hold live files rather than bound
   archive volumes.
2. **A live MX record proves a domain exists, not that anybody is listening.** Check that an
   address has demonstrably answered a human being.
3. **Read the source document, not a summary of it** — and then check the source document is
   not itself out of date. `reposit.htm` passed every test and was still wrong.

## Shared tools worth knowing in both projects

- **gazettes.africa** — free, full-text, to 2026. Estate notices (Form J193) give date of
  birth, identity number, address, date of death, surviving spouse and executor.
  **Modern notices put the SURNAME FIRST** — search `"GILLIAN AGNES LOUISA"`, not
  `"Gillian Agnes Louisa Nel"`. The site is Cloudflare-protected but the PDFs are open at
  `archive.gazettes.africa/archive/za/<year>/<slug>.pdf` — fetch, `pdftotext -layout`, grep.
- **gendatabase.com** — indexes South African women under their **MAIDEN** name, which nothing
  else does. `/search-results.php?firstname=&surname=X` carries a `SID`; then
  `/search/api.php?action=page&sid=<SID>&offset=N` returns clean JSON.
  **Its terms forbid republishing without written permission.**
- **NAAIRS** — `national.archsrch.gov.za`, free, session-chained forms. Estate and court files.
