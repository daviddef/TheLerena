#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give the citations on the narrative pages their links to the records (the linking standard's L3) and put a held scan beside the
passage that relies on it (L4). A build step that runs on the BUILT pages after the names are linked, before the standard's gate.

    python3 ../tools/link-records.py                  # from site/: rewrite site/dist
    python3 ../tools/link-records.py --check          # change nothing; print what a run would do
    python3 ../tools/link-records.py --report FILE    # also write every change, with its passage, to FILE (names appear: private)

WHY A PASS AND NOT A COMPONENT IN EVERY PAGE. The citations sit in 785 KB of hand-written pages and in dozens of TSVs rendered through
emph(); wrapping each with <Rec> would mean editing research prose in a hundred places. The kit's Rec draws one tag (see
kit/components/Rec.astro); this pass draws the SAME tag from the SAME table (site/src/data/records.json, made by tools/build-records.py from
committed data), so the words of the citation become the link and nothing is reworded. A new passage written with <Rec> directly
(src/components/Rec.astro) is equally fine: this pass skips a passage that already carries a record link.

THREE SOURCES OF CHANGE, none of which invents an address:
  1. a DGS or film number in a passage (with an image number when the table holds that image's ark) -> the film's row or the image's ark
     row, only for a number the table holds;
  2. data/record-links.tsv, an editorial table: page, how the passage begins, the exact words, and the record (a table id), or `exempt:`
     and a reason (a passage that cites nothing a reader could be sent to: a negative search, a record with no public address held,
     a note on the tool), or `thumb:` and a plate id (the held scan beside the passage that relies on it). A row whose passage or words
     cannot be found changes nothing and is counted ("rows that matched nothing"): the standard's ratchet is what holds the number.
  3. nothing else.
A link is not drawn for a record the table flags `living` or `hold` (none is made). Text inside an existing link is never touched; the
words are linked once per passage. Prints counts only.
"""
import argparse, html, json, pathlib, re, sys, unicodedata

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = ROOT / "site"
RECORDS = SITE / "src" / "data" / "records.json"
LINKS = ROOT / "data" / "record-links.tsv"
STANDARD = SITE / "standard.json"

TOKEN = re.compile(r"<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<[^>]+>|[^<]+", re.S | re.I)
TAG = re.compile(r"<(/?)([A-Za-z][A-Za-z0-9-]*)([^>]*?)(/?)>", re.S)
BLOCKS = {"p", "li", "dd", "dt", "td", "th", "blockquote", "figcaption"}
VOID = {"br", "hr", "img", "input", "meta", "link", "source", "area", "base", "col", "embed", "param", "track", "wbr"}
CLOSERS = {"p": {"p"}, "li": {"li"}, "dd": {"dd", "dt"}, "dt": {"dd", "dt"}, "td": {"td", "th"}, "th": {"td", "th"}}
FILM_REF = re.compile(r"\b(?:film|DGS|microfilm)\s*(?:no\.?\s*)?0*(\d{6,9})\b(?:\s*[,(]?\s*(?:items?\s*\d+(?:\s*[-–]\s*\d+)?\s*,?\s*)?(?:images?|img|frames?)\s*(?:no\.?\s*)?0*(\d+))?", re.I)
BREAK = re.compile(r"</?(?:br|p|div|li|td|th|tr|dd|dt|ul|ol|table|blockquote|figure|figcaption|h[1-6])\b", re.I)
ENT = re.compile(r"&(?:#\d+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);")


def squash(s):
    return " ".join(s.replace("\xa0", " ").split())


def esc_attr(s):
    return html.escape(s, quote=True)


class Page:
    """A built page as tokens, with its passages (blocks) found and its record links known."""

    def __init__(self, text):
        self.tok = TOKEN.findall(text) if text else []
        self.repl = {}                               # token index -> its new text (self.tok stays the page as built)
        self.blocks = []
        self._scan()

    def _scan(self):
        stack = []                                   # [name, token index, block or None, in_main]
        open_blocks = []
        in_main = 0
        for i, t in enumerate(self.tok):
            if not t.startswith("<") or t.startswith("<!--") or re.match(r"<(script|style)\b", t, re.I):
                if in_main:
                    for b in open_blocks:
                        b["text"].append(i)
                continue
            m = TAG.match(t)
            if not m:
                continue
            closing, name, attrs, selfc = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
            if not closing:
                if name in CLOSERS:
                    for k in range(len(stack) - 1, -1, -1):
                        if stack[k][0] in CLOSERS[name]:
                            self._pop(stack, open_blocks, k, i)
                            break
                        if stack[k][0] in ("ul", "ol", "table", "dl", "div", "section"):
                            break
                if name == "main":
                    in_main += 1
                if name in VOID or selfc:
                    if name == "a" or True:
                        pass
                    if in_main and name == "img":
                        pass
                    continue
                blk = None
                if name in BLOCKS and in_main:
                    blk = {"tag": name, "start": i, "end": None, "text": [], "links": [], "attrs": attrs}
                    self.blocks.append(blk)
                    open_blocks.append(blk)
                stack.append([name, i, blk])
                if name == "a" and in_main:
                    href = re.search(r'href\s*=\s*"([^"]*)"', attrs)
                    for b in open_blocks:
                        b["links"].append((html.unescape(href.group(1)) if href else "", "data-cite" in attrs or "data-rec" in attrs, i))
            else:
                for k in range(len(stack) - 1, -1, -1):
                    if stack[k][0] == name:
                        self._pop(stack, open_blocks, k, i)
                        break
                if name == "main" and in_main:
                    in_main -= 1

    @staticmethod
    def _pop(stack, open_blocks, k, i):
        while len(stack) > k:
            f = stack.pop()
            if f[2] is not None:
                f[2]["end"] = i
                if f[2] in open_blocks:
                    open_blocks.remove(f[2])

    def text_of(self, b):
        parts = []
        for i in range(b["start"] + 1, (b["end"] if b["end"] is not None else len(self.tok))):
            t = self.tok[i]
            if not t.startswith("<"):
                parts.append(t)
            elif BREAK.match(t):
                parts.append(" ")
        return squash(html.unescape("".join(parts)))

    def in_anchor(self, i):
        depth = 0
        for j in range(i - 1, -1, -1):
            t = self.tok[j]
            m = TAG.match(t) if t.startswith("<") else None
            if m and m.group(2).lower() == "a":
                if m.group(1):
                    depth += 1
                else:
                    if depth == 0:
                        return True
                    depth -= 1
        return False

    def text(self):
        return "".join(self.repl.get(i, t) for i, t in enumerate(self.tok))

    def put(self, i, new):
        self.repl[i] = new


def raw_find(raw, phrase, start=0):
    """Find `phrase` (plain text) in `raw` (HTML text with entities). Returns (raw_start, raw_end) or None."""
    plain, idx = [], []
    pos = 0
    for m in ENT.finditer(raw):
        for k in range(pos, m.start()):
            plain.append(raw[k]); idx.append((k, k + 1))
        ch = html.unescape(m.group(0))
        for c in ch:
            plain.append(c); idx.append((m.start(), m.end()))
        pos = m.end()
    for k in range(pos, len(raw)):
        plain.append(raw[k]); idx.append((k, k + 1))
    s = "".join(plain).replace("\xa0", " ")
    j = s.find(phrase, start)
    if j < 0:
        return None
    return idx[j][0], idx[j + len(phrase) - 1][1]


def link_html(rec, words):
    attrs = ' class="lk-rec" href="%s" data-rec="%s" data-cite' % (esc_attr(rec["url"]), esc_attr(rec["id"]))
    if rec.get("kind"):
        attrs += ' data-kind="%s"' % esc_attr(rec["kind"])
    if rec.get("label"):
        attrs += ' title="%s"' % esc_attr(rec["label"])
    if rec["url"].startswith(("http://", "https://")):
        attrs += ' rel="noopener"'
    return "<a%s>%s</a>" % (attrs, words)


def figure_html(rec, first):
    base = rec["plate"]
    ident = ' id="plate-%s"' % esc_attr(rec["id"][len("plate-"):] if rec["id"].startswith("plate-") else rec["id"]) if first else ""
    dims = (' width="%d" height="%d"' % (rec["w"], rec["h"])) if rec.get("w") and rec.get("h") else ""
    src = "/docs/" + base
    cap = link_html(rec, html.escape(rec["label"]))
    return ('<figure class="rec-fig"%s><a class="rec-fig-img" href="%s"><img src="%s" alt="%s"%s loading="lazy" decoding="async"></a>'
            "<figcaption>%s</figcaption></figure>") % (ident, esc_attr(src), esc_attr(src), esc_attr(rec["label"]), dims, cap)


def _chars(page, b):
    """The block's text as (char, token index, raw start, raw end), entities decoded and every run of white space one space."""
    out = []
    last_space = True
    for i in range(b["start"] + 1, (b["end"] if b["end"] is not None else len(page.tok))):
        t = page.tok[i]
        if t.startswith("<"):
            if BREAK.match(t):
                last_space = _push(out, " ", i, 0, 0, last_space)
            continue
        pos = 0
        for m in ENT.finditer(t):
            for k in range(pos, m.start()):
                last_space = _push(out, t[k], i, k, k + 1, last_space)
            for c in html.unescape(m.group(0)):
                last_space = _push(out, c, i, m.start(), m.end(), last_space)
            pos = m.end()
        for k in range(pos, len(t)):
            last_space = _push(out, t[k], i, k, k + 1, last_space)
    return out


def _push(out, c, i, a, z, last_space):
    if c in " \t\r\n\xa0":
        if last_space:
            if out:
                out[-1] = (out[-1][0], out[-1][1], out[-1][2], z) if out[-1][0] == " " and out[-1][1] == i else out[-1]
            return True
        out.append((" ", i, a, z))
        return True
    out.append((c, i, a, z))
    return False


def wrap_in_block(page, b, phrase, rec, taken):
    """Link the first occurrence of `phrase` inside block b (not inside a link, the words spread over inline tags if need be) to
    rec. True when done."""
    ch = _chars(page, b)
    plain = "".join(c[0].lower() if len(c[0].lower()) == 1 else c[0] for c in ch)
    want = " ".join(phrase.replace("\xa0", " ").split()).lower()
    start = 0
    while True:
        j = plain.find(want, start)
        if j < 0:
            return False
        first, last = ch[j], ch[j + len(want) - 1]
        i0, i1 = first[1], last[1]
        ok = not (page.in_anchor(i0) or any(k in taken for k in range(i0, i1 + 1)))
        if ok and i1 > i0:
            depth = 0                                   # the tags inside the words must open and close inside them
            for k in range(i0 + 1, i1):
                t = page.tok[k]
                m = TAG.match(t) if t.startswith("<") else None
                if not m or m.group(4) or m.group(2).lower() in VOID:
                    continue
                if m.group(2).lower() == "a":
                    ok = False
                    break
                depth += -1 if m.group(1) else 1
                if depth < 0:
                    ok = False
                    break
            ok = ok and depth == 0
        if ok:
            op = link_html(rec, "").rsplit("</a>", 1)[0]
            if i0 == i1:
                t = page.repl.get(i0, page.tok[i0])
                a_, z_ = first[2], last[3]
                page.put(i0, t[:a_] + op + t[a_:z_] + "</a>" + t[z_:])
            else:
                t0 = page.repl.get(i0, page.tok[i0])
                page.put(i0, t0[:first[2]] + op + t0[first[2]:])
                t1 = page.repl.get(i1, page.tok[i1])
                page.put(i1, t1[:last[3]] + "</a>" + t1[last[3]:])
            for k in range(i0, i1 + 1):
                taken.add(k)
            return True
        start = j + 1


def load_standard_pages():
    d = json.loads(STANDARD.read_text(encoding="utf-8"))
    return [p for p in d["include"] if p not in set(d.get("exclude") or [])]


def load_rows():
    rows = []
    if not LINKS.exists():
        return rows
    for n, line in enumerate(LINKS.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#") or line.startswith("page\t"):
            continue
        c = (line.split("\t") + [""] * 6)[:6]
        page, start, nth, phrase, target, note = [x.strip() if i != 1 else x for i, x in enumerate(c)]
        rows.append({"n": n, "page": page, "start": start.strip(), "nth": int(nth or 1), "phrase": phrase, "target": target, "note": note})
    return rows


def dist_path(dist, url):
    return dist / url.strip("/") / "index.html"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dist", default="dist")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report")
    a = ap.parse_args(argv)
    dist = SITE / a.dist
    table = {r["id"]: r for r in json.loads(RECORDS.read_text(encoding="utf-8"))["records"]}
    by_key = {}
    for r in table.values():
        for k in r.get("key", []):
            by_key[(r["kind"], k)] = r
    rows = load_rows()
    stats = {"film or image links": 0, "linked from the table": 0, "exempted with a reason": 0, "scans placed": 0,
             "rows that matched nothing": 0, "pages changed": 0}
    report = []
    pages = load_standard_pages()
    first_fig = set()
    for url in pages:
        p = dist_path(dist, url)
        if not p.exists():
            print("link-records: %s is not built" % url)
            return 2
        page = Page(p.read_text(encoding="utf-8"))
        changed = False
        taken = set()
        figs = {}                                    # block end token -> html
        # 1. curated rows
        for r in [x for x in rows if x["page"] == url]:
            short = len(r["start"]) < 60                  # a whole short passage is matched whole, a long one by how it begins
            cands = [b for b in page.blocks if (page.text_of(b) == r["start"] if short else page.text_of(b).startswith(r["start"]))]
            # prefer the innermost block when nested blocks both start with the text
            cands = [b for b in cands if not any(o is not b and o["start"] > b["start"] and (o["end"] or 0) <= (b["end"] or 0) and page.text_of(o).startswith(r["start"]) for o in cands)]
            if len(cands) < r["nth"]:
                stats["rows that matched nothing"] += 1
                report.append("UNMATCHED passage\t%s\tline %d" % (url, r["n"]))
                continue
            b = cands[r["nth"] - 1]
            tgt = r["target"]
            if tgt.startswith("exempt:"):
                reason = tgt[len("exempt:"):].strip()
                if len(reason) < 12:
                    print("link-records: data/record-links.tsv line %d: an exemption needs a reason of 12+ characters" % r["n"])
                    return 2
                t = page.repl.get(b["start"], page.tok[b["start"]])
                if "data-cite-exempt" not in t:
                    page.put(b["start"], t[:-1] + ' data-cite-exempt="%s">' % esc_attr(reason))
                    stats["exempted with a reason"] += 1
                    changed = True
            elif tgt.startswith("thumb:"):
                rec = table.get(tgt[len("thumb:"):].strip())
                if rec is None or rec.get("kind") != "plate" or rec.get("show") is not True or rec.get("living") or rec.get("hold"):
                    stats["rows that matched nothing"] += 1
                    continue
                figs.setdefault(b["end"], []).append((rec, b))
            else:
                rec = table.get(tgt)
                if rec is None or rec.get("living") or rec.get("hold") or not r["phrase"]:
                    stats["rows that matched nothing"] += 1
                    report.append("UNMATCHED record\t%s\tline %d" % (url, r["n"]))
                    continue
                if wrap_in_block(page, b, r["phrase"], rec, taken):
                    stats["linked from the table"] += 1
                    changed = True
                    report.append("%s\t%s\t%s" % (url, rec["id"], r["phrase"]))
                else:
                    stats["rows that matched nothing"] += 1
                    report.append("UNMATCHED words\t%s\tline %d" % (url, r["n"]))
        # 2. a film or image number in a passage that carries no record link
        for b in page.blocks:
            if any(ok for _h, ok, _i in b["links"]) or any(h.startswith("https://www.familysearch.org/") for h, _o, _i in b["links"]):
                continue
            seen = set()
            for i in b["text"]:
                t = page.tok[i]
                if t.startswith("<") or page.in_anchor(i) or i in taken:
                    continue
                s = html.unescape(t)
                for m in FILM_REF.finditer(s):
                    f = int(m.group(1))
                    row = by_key.get(("film", str(f)))
                    if m.group(2):
                        row = by_key.get(("ark", "%d/%d" % (f, int(m.group(2))))) or row
                    if row is None or row["id"] in seen or len(seen) >= 3:
                        continue
                    r_ = raw_find(t, m.group(0))
                    if not r_:
                        continue
                    seen.add(row["id"])
                    za, zz = r_
                    page.put(i, t[:za] + link_html(row, t[za:zz]) + t[zz:])
                    taken.add(i)
                    stats["film or image links"] += 1
                    changed = True
                    report.append("%s\t%s\t%s" % (url, row["id"], m.group(0)))
                    break
        # 3. scans beside the passage (one per plate per section is enough; a repeat in the same block run is skipped)
        for end, lst in sorted(figs.items(), reverse=True):
            h = ""
            for rec, b in lst:
                key = (url, rec["id"], id(b))
                first = (url, rec["id"]) not in first_fig
                first_fig.add((url, rec["id"]))
                h += figure_html(rec, first)
                stats["scans placed"] += 1
                report.append("%s\t%s\tthumb" % (url, rec["id"]))
            blk = next(x for x in page.blocks if x["end"] == end)
            cur = page.repl.get(end, page.tok[end])
            page.put(end, cur + h if blk["tag"] in ("p", "blockquote", "figcaption") else h + cur)
            changed = True
        if changed:
            stats["pages changed"] += 1
            if not a.check:
                p.write_text(page.text(), encoding="utf-8")
    print("link-records: " + "; ".join("%d %s" % (v, k) for k, v in stats.items()))
    if a.report:
        pathlib.Path(a.report).write_text("\n".join(report) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
