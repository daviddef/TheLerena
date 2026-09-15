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


---

## Home Affairs certificates — the rule, and where it came from (added 15 September 2026)

**Do not draft another letter asking the South African Department of Home Affairs for a certificate
by email. It is not a mechanism that exists.**

Source: **Heather MacAlister, Ancestors Research South Africa**, `heather@ancestors.co.za`, to David
on **11 May 2020**, in the Lerena/Booyzen thread (Gmail `1720deb1fca8f731`):

> … abridged, unabridged or vault can only be applied for **in person (only)** at any Department of
> Home Affairs. If the person applying for it is not for them then **only immediate family members
> can apply**. Home Affairs no longer allows 3rd party applications so I cannot do it on your behalf
> and any company that offers this service offers an illegal service … If, however you live overseas
> you can then apply through the **South African Embassy or Consulate in your country of residence**.

**Three things follow, and they apply to BOTH archives:**

1. The route for an applicant in Australia is the **South African High Commission, Canberra**.
2. **Nobody can be paid to do it for you.** Any service offering to obtain SA certificates as a third
   party is, on this account, offering something it is not allowed to do. That is a caution for the
   Pretoria researcher brief too: estate files and court files at the National Archives are fine;
   Home Affairs certificates are not.
3. **Eligibility is the real constraint, not the fee.** For an old record it turns on who counts as
   immediate family, and in the Luwinski archive that question has a living answer. See work-list
   row 22 and request 15.

*This entry exists because the same mistake was one draft away from being made a fourth time.*


---

## SANDF Documentation Centre — already written to, and one address is dead (15 September 2026)

**BOTH archives want this office.** The Lerena/Booyzen side wrote first.

- **9 September 2026** — David wrote about the **BOOYZEN/BOOYSEN** family, UDF service and a
  military pension (Gmail `1a085121bd59a4a2`). **No reply as at 15 September.**
- **15 September 2026** — request 16 drafted in the Luwinski archive about **Leonard Aubrey Robert
  Wear**, a different man entirely. It opens by naming the earlier letter, because two cold emails
  from one person in six days is how the Xaba duplication happened.

**The address most of the internet gives you is dead.**

- `sandfdoc@mweb.co.za` — **BOUNCED**, `550 5.7.1 Relay access denied`. Still the address quoted in
  almost every guide to South African military research. **Do not use it.**
- `archive@dod.mil.za` — **use this one.** MX verified: `mail1.dod.mil.za`.

**And the Centre has moved.** The widely published *Schweikert Building, 20 Visagie Street, Pretoria*
is stale. Current: **42 Saturnus Road, Irene, Pretoria 0157**; postal **DoD Archives, Private Bag
X289, Pretoria 0001**; +27 12 670 8127; **closed Mondays and Fridays**.

*Fourth bad address of this project, and the first one caught before sending rather than after.*

## Church of the Immaculate Conception, Rosebank (15 September 2026)

`Info@rosebankcatholicchurch.co.za` — MX verified (Microsoft 365). 16 Keyes Avenue, Rosebank 2196;
011 788 5226/7; office Monday–Friday 09h00–15h00, **closed weekends**. Parish established **1936**;
parish priest listed as Fr Donald McLoughlin. Request 17. Fallback if the registers were deposited
centrally: the **Archdiocese of Johannesburg**, `catholicjhb.org.za` (MX verified) — **confirm the
chancery address on the day rather than guessing it.**


---

## The address procedure, rewritten — 15 September 2026

**The old rule was "MX check before sending any email". It has now been audited against every
address this project has used, and it is nearly worthless as a primary test.**

Twenty-six addresses were re-resolved. Six have failed in practice. **MX caught one of the six.**

| Address | MX says | What actually happened |
|---|---|---|
| `ahm@mail.exercito.pt` | **no MX** | NXDOMAIN bounce — **caught** |
| `sandfdoc@mweb.co.za` | live MX | `550 relay access denied` — missed |
| `enquiries@dac.gov.za` | live MX | NXDOMAIN bounce from DSAC's own gateway — missed |
| `enquiries@dac.gov.za` (earlier) | live MX | department renamed **DAC → DSAC** — missed |
| `NMphetshwa@justice.gov.za` | live MX | the person had left the section — missed |
| SANDF, Visagie Street | live MX | the office had **moved to Irene** — missed |

**And here is why MX can never catch the commonest failure.** `dac.gov.za` and `dsac.gov.za`
resolve to **the same mail gateway** — `za-smtp-inbound-1.mimecast.co.za`. The dead old domain
therefore keeps a perfectly valid MX record, mail is accepted by the shared gateway, and the
rejection happens *inside*, where a DNS check cannot see it. *A live MX record proves a mail server
answers for the domain. It proves nothing about the department, the office or the person.*

### The replacement, in order of what actually catches things

1. **Search the sent mail first.** For prior contact *and* for prior bounces to that domain. This
   has caught three separate failures: the Xaba duplication, the SANDF duplication, and the dead
   mweb address that was about to be reused.
2. **Prefer an address the institution itself gave you.** A referral beats a directory entry every
   time — `arqgex@exercito.pt` came from the ADN and answered within the hour, twice.
3. **Check the institution still exists under that name, and at that address.** DAC became DSAC;
   the SANDF Documentation Centre left Visagie Street for Irene. A published guide can be a decade
   stale and still rank first in a search.
4. **MX last**, and only to catch a mistyped subdomain. One in six.
5. **Watch for a bounce for a day afterwards** — and record an auto-acknowledgement as *delivery
   evidence, not an answer*. See `/letters/`.

*Applies to both archives.*
