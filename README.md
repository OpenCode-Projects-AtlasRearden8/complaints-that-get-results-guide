# Complaints That Get Results

*A plain-English manual for resolving disputes politely and effectively — stores, landlords, utilities, insurers, and small claims.*

Built the way a friend would explain it: no jargon, no condescension, no pretending everything is simple. Just records, escalation ladders, letters that get answered, and calendars that don't let deadlines slip by.

## What's in the box

| Path | Contents |
| --- | --- |
| `docs/` | The seven-chapter manual as editable Markdown |
| `site/` | A static website version of the manual + **editable letter templates** |
| `site/templates/` | Generated letter templates (plain `.md`, ready to fill in) |
| `site/templates-src/` | The source of truth for those letter templates |
| `build.py` | One command to rebuild the site from `docs/` |
| `check_site.py` | Smoke test: serves `site/` locally and verifies every page |

## The chapters

1. **Gather records first** — the 15-minute filing setup that powers everything
2. **The escalation ladder** — polite climbing for stores, landlords, utilities, insurers
3. **Complaint letter anatomy** — short, factual, one ask, one deadline
4. **Deadline calendars** — the two-touch rule and the monthly audit
5. **Small claims basics** — a beginner's tour of the no-lawyers courthouse
6. **AI tone review** — use AI as your editor, not your author; redact before you paste
7. **The free Everyday Letters Pack** — where the fill-in-the-blanks letters live

## How to run it

Everything works offline. No installs, no accounts, no data leaves your machine.

```bash
# read the manual (option 1 — open in your editor)
$EDITOR docs/00-start-here.md

# read the manual (option 2 — the local website)
python3 build.py && python3 check_site.py   # rebuild + verify
python3 -m http.server 8000 -d site         # then open http://localhost:8000

# or simply double-click site/index.html — it's fully static
```

To edit the letter templates: open anything in `site/templates-src/` (or edit them right on the Templates page of the website, which offers Copy/Download buttons for each letter). To edit chapters: change the matching file in `docs/`, then `python3 build.py`.

## Pairing with the free Everyday Letters Pack

This manual is the *why*; the Everyday Letters Pack is the *what type into the blank*. The pack ships inside this project (`site/templates/`) and also as its own free release from **Asdale Dynamics, LLC** — search for "free-everyday-letters-pack", or visit our hub at [dylanasdale.github.io](https://dylanasdale.github.io).

## Privacy & safety posture

- **Local-first.** The site is static HTML; it phones no home and collects nothing.
- **No secrets, no personal data.** Templates use `{{placeholders}}` only; never paste real records into AI tools — Chapter 6 shows the redaction-first way.
- **Not legal advice.** This is practical education. Serious matters (large sums, eviction, insurance denials, injury) deserve a lawyer or a free legal-aid consultation.

## Credits

Published by **Asdale Dynamics, LLC** (Indiana, 2026). From Dylan Asdale — registered nurse turned AI author — and the team behind *The Massive AI Manual*. The hub site [dylanasdale.github.io](https://dylanasdale.github.io) explains AI "like a friend would": plain English, step by step, never condescending.

Licensed MIT — see [LICENSE](LICENSE).
