# STATUS.md

Last updated: 2026-11-03

## What was built

**Complaints That Get Results** — a beginner-friendly manual for resolving disputes politely and effectively, published as both Markdown chapters and a fully offline static website, with editable complaint-letter templates. © Asdale Dynamics, LLC.

| Piece | Detail |
| --- | --- |
| `docs/00-start-here.md` | Roadmap, how-to-use, what this is/isn't |
| `docs/01-gather-records-first.md` | The 15-minute dispute-filing system + timeline log |
| `docs/02-escalation-ladder.md` | Polite escalation ladder for stores, landlords, utilities, insurers |
| `docs/03-complaint-letter-anatomy.md` | Complaint letter anatomy + one-page template + tone killers |
| `docs/04-deadline-calendars.md` | Four clocks, two-touch rule, monthly audit, blank deadline template |
| `docs/05-small-claims-basics.md` | Beginner's overview of small claims (education, not a filing kit) |
| `docs/06-ai-tone-review.md` | Redact-first AI tone review with copy-paste prompt + hard rules |
| `docs/07-free-everyday-letters-pack.md` | Pairing guide for the free Everyday Letters Pack |
| `site/templates-src/` | 5 editable letter templates (source of truth): store defect, landlord repair, utility billing, insurer appeal, general escalation |
| `site/` | Static HTML manual (9 pages), editable in-browser template gallery with Copy/Download buttons, stylesheet |
| `build.py` | Rebuilds `site/*.html` from `docs/` via Python `markdown`; validates tag balance and every internal link; non-zero exit on failure |
| `check_site.py` | Serves `site/` locally and verifies all 9 pages return 200 with intact nav/footer |
| `LICENSE` | MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC` |
| `README.md` | Setup + credits to Asdale Dynamics, LLC |

## How to run it

```bash
# Rebuild the website from docs/ + templates (requires: pip install markdown)
python3 build.py

# Verify: syntax/link check (inside build) + live smoke test of every page
python3 check_site.py

# Read it
python3 -m http.server 8000 -d site    # then open http://localhost:8000
# ... or simply open site/index.html in a browser; everything is static/offline
```

## Verification results

All commands run successfully on 2026-11-03:

- `python3 -m py_compile build.py check_site.py` — OK
- `python3 build.py` — exit 0; prints `BUILD OK: 9 pages generated in site/`; internal validators confirm tag balance and that no page links to a missing file or broken anchor
- `python3 check_site.py` — exit 0; prints `SITE CHECK OK: all pages serve and render intact.` (9/9 pages, HTTP 200)
- Secret/personal-data scan (grep for keys, tokens, passwords, SSN patterns) — clean; templates contain `{{placeholders}}` only
- CJK/stray-character scan over docs, templates, generated HTML — clean
- LICENSE copyright line verified: `Copyright (c) 2026 Asdale Dynamics, LLC`
- No remote, no push, no publishing; committed locally only

## Known gaps / future work

- **Jurisdiction specificity:** the manual deliberately avoids naming statutes, claim caps, or state-by-state deadlines; a future "local rules finder" page with plain-language summaries per state/province would be a natural companion (researched per jurisdiction, kept education-only).
- **Template coverage:** five letters ship today; natural additions: chargeback request letter, car-dealer issue, deposit-return follow-up, "deadline missed" recovery letter.
- **Templates gallery niceties:** the Copy/Download buttons use the browser clipboard/download APIs; a plain "select all" fallback works everywhere but the buttons degrade silently on very old browsers.
- **No search:** site is static; a tiny client-side index (hand-rolled, no CDN) could be added later.
- **Print/PDF:** no bundled PDF export; `docs/*.md` print fine from any editor.
- **Everyday Letters Pack distribution:** the companion "free-everyday-letters-pack" release page is referenced in docs; here it ships inline via `site/templates/`. Coordinate links when that pack publishes separately.
- Markdown version locked to the standard `markdown` PyPI package (tables + fenced code extensions); any future Python ABI change just needs `pip install markdown`.
