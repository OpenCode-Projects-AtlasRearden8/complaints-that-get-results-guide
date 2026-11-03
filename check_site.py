#!/usr/bin/env python3
"""Smoke-test the built site: every page must serve HTTP 200 and contain
the stylesheet link, nav, and footer. Run `python3 build.py` first.
"""

import functools
import http.server
import socketserver
import sys
import threading
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"

PAGES = [
    "index.html",
    "gather-records.html",
    "escalation-ladder.html",
    "letter-anatomy.html",
    "deadlines.html",
    "small-claims.html",
    "ai-tone-review.html",
    "letters-pack.html",
    "templates.html",
]


def main() -> int:
    Handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(SITE)
    )

    with socketserver.TCPServer(("127.0.0.1", 0), Handler) as httpd:
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        failures = 0
        for page in PAGES:
            url = f"http://127.0.0.1:{port}/{page}"
            try:
                with urllib.request.urlopen(url, timeout=5) as resp:
                    body = resp.read().decode("utf-8")
                    problems = []
                    for needle in ("assets/style.css", "nav-link", "site-footer"):
                        if needle not in body:
                            problems.append(f"missing '{needle}'")
                    if f"href=\"{page}\"" not in body and page != "index.html":
                        problems.append("not linked from nav")
                    if problems:
                        failures += 1
                        print(f"FAIL {url}: {problems}")
                    else:
                        print(f"OK   {url}")
            except Exception as err:  # noqa: BLE001
                failures += 1
                print(f"FAIL {url}: {err}")
        httpd.shutdown()

    if failures:
        print(f"SITE CHECK FAILED: {failures} page(s) with problems.")
        return 1
    print("SITE CHECK OK: all pages serve and render intact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
