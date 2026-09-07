#!/usr/bin/env python3
"""
Query NAAIRS - the South African National Archives index - from the command line.

NAAIRS is a legacy CGI application on plain HTTP (no HTTPS). Every page mints a
fresh session token which must be carried into the next request, so the whole
flow has to happen inside one process:

    sm300dl                      database selection, mints a token
    sm300gi?<tok>%26DB%3D<db>    the search form for one database
    POST sm300dr?<tok>           run the query
    sm30ddf0?<tok>               the full record details

Databases: RSAE (all repositories - the default), KABE Cape Town, TABE Transvaal,
NABE Pietermaritzburg, VABE Free State, TBDE Durban, TBEE Port Elizabeth,
SABE central government, GENE gravestones, MANE manuscripts.

Usage:
    python3 tools/naairs.py SURNAME [--db RSAE] [--out prefix]
"""
import sys, re, time, urllib.request, urllib.parse, http.cookiejar

BASE = "http://www.national.archsrch.gov.za/sm300cv/smws/"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


class Naairs:
    def __init__(self):
        cj = http.cookiejar.CookieJar()
        self.o = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        self.last = BASE

    def open(self, url, data=None, tries=3):
        url = urllib.parse.urljoin(BASE, url)
        hdr = {"User-Agent": UA, "Referer": self.last}
        body = None
        if data is not None:
            body = urllib.parse.urlencode(data).encode()
            hdr["Content-Type"] = "application/x-www-form-urlencoded"
        for n in range(tries):
            try:
                with self.o.open(urllib.request.Request(url, data=body, headers=hdr),
                                 timeout=120) as r:
                    html = r.read().decode("latin-1")
                self.last = url
                return html
            except Exception as e:
                if n == tries - 1:
                    raise
                time.sleep(3 * (n + 1))

    # -- flow -------------------------------------------------------------
    def search(self, term, db="RSAE"):
        sel = self.open("sm300dl")
        m = re.search(r'href=["\']?((?:sm300gi|SM200gi)\?[^"\'\s>]*' + db + r')', sel, re.I)
        if not m:
            raise SystemExit(f"!! database {db} not offered on the selection page")
        form = self.open(m.group(1))
        act = re.search(r'<form[^>]*action="([^"]+)"', form, re.I)
        if not act:
            raise SystemExit("!! no search form found")
        res = self.open(act.group(1),
                        {"VER": "HI", "K0000001": term, "btnSearch": "Search"})
        return res

    def details(self, results_html, count):
        """Fetch every hit by document number: sm30ddf0?<tok>&DN=000000NN&F=P"""
        m = re.search(r'href=["\']?(sm30ddf0\?[^"\'\s>]+)', results_html, re.I)
        if not m:
            return []
        first = self.open(m.group(1))
        tok = re.search(r'sm30ddf0\?([0-9A-Za-z]+)', first)
        pages = [first]
        if not tok:
            return pages
        for dn in range(2, count + 1):
            tk = re.search(r'sm30ddf0\?([0-9A-Za-z]+)', pages[-1])
            tk = tk.group(1) if tk else tok.group(1)
            pages.append(self.open(f"sm30ddf0?{tk}&DN={dn:08d}&F=P"))
        return pages


def strip(html):
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    h = re.sub(r"(?i)<br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</(tr|p|div|h[1-6]|table)>", "\n", h)
    h = re.sub(r"<[^>]+>", " ", h)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&#39;", "'"),
                 ("&quot;", '"'), ("&lt;", "<"), ("&gt;", ">")):
        h = h.replace(a, b)
    h = re.sub(r"[ \t]+", " ", h)
    return "\n".join(l.strip() for l in h.splitlines() if l.strip())


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    term = sys.argv[1]
    db = sys.argv[sys.argv.index("--db") + 1] if "--db" in sys.argv else "RSAE"
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None

    n = Naairs()
    res = n.search(term, db)
    hits = re.search(r"located in\s*(\d+)\s*document", strip(res), re.I)
    print(f"# {term} / {db}: {hits.group(1) if hits else '?'} documents", file=sys.stderr)

    count = int(hits.group(1)) if hits else 0
    if not count:
        print(strip(res)); return
    pages = n.details(res, count)
    if out:
        for i, p in enumerate(pages, 1):
            open(f"{out}.{i}.html", "w", encoding="utf-8").write(p)
        print(f"# raw -> {out}.*.html ({len(pages)} page(s))", file=sys.stderr)
    for p in pages:
        print(strip(p))


if __name__ == "__main__":
    main()
