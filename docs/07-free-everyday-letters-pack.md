# Chapter 7 — The Free Everyday Letters Pack

> One sentence to remember: **Never start a letter from a blank page — start from a fill-in-the-blanks.**

---

## What the pack is

This manual pairs with a **free companion: the Everyday Letters Pack** — a set of ready-made, fill-in-the-blanks letter templates covering the disputes people actually have. Where this manual teaches *why* each sentence works, the pack gives you *the sentences*:

- Store: defective product refund/exchange request
- Store: wrong or missing order / delivery issue
- Landlord: written repair request + follow-up notice
- Utility: billing dispute / high-bill request for meter review
- Insurer: denial appeal (first appeal letter)
- Generic: negative replies, deadline reminders, and the "escalation notice" stair-step letters
- Small-claims: the pre-filing final-demand letter that often settles the case outright

Every template ships as **plain text and Markdown**, so it works in Notepad, Google Docs, Word, or a phone — no special software, no account.

## Where to get it

The templates are also included in this project's `site/templates/` folder (see below), and a standalone copy of the pack is published by Asdale Dynamics, LLC — search for **"free-everyday-letters-pack"** on your code-hosting site of choice, or visit the hub at [dylanasdale.github.io](https://dylanasdale.github.io).

Locally in this repo, the editable versions live in:

```
site/templates/
├── letter-store-defect.md / .html
├── letter-landlord-repair.md / .html
├── letter-utility-billing.md / .html
├── letter-insurer-appeal.md / .html
└── letter-general-escalation.md / .html
```

The `.md` versions are the ones you'll usually copy. The `.html` versions are the same letters wrapped so the site can show them — edit either; the structure matches.

## How a template is built (the anatomy, hidden in the blanks)

The book's Chapter 3 anatomy maps onto every template:

| Anatomy piece | In the template |
| --- | --- |
| Headline/date/ref | The `To / From / Re:` block with `{{REF}}` slots |
| One-sentence summary | The "On `<date>`, I `<did what>`…" first line |
| Facts | Numbered `FACT 1..3` slots with photo/attachment references |
| The ask | `REMEDY REQUEST:` — exactly one sentence |
| The deadline | `Please reply by {{DATE}}` — pre-formatted as +14 days |
| The next step | The calm escalation line, already worded |
| Closing | A warm one-liner, plus your contact block |

Fill in the `{{slug}}` slots; delete any brackets that DON'T apply. Then run the Chapter 6 AI tone review on your cleaned copy.

## The 5-minute workflow

1. **Pick the template** that matches your ladder rung (Chapter 2 told you which).
2. **Copy it** into `04-letters-sent/` as `letter-03-corporate-2026-03-04.md`.
3. **Fill the slots,** keeping the letter to one page.
4. **Redact + tone review** (Chapter 6).
5. **Send** (email + printed copy for anything high-stakes), **log it** in `00-log.md`, **set the two calendar touches** (Chapter 4).

## Why templates work better than "writing from scratch"

- You can't forget the deadline if the deadline is already in the template.
- You can't let the angry paragraph grow if there's no slot for it.
- They *should be* edited — strike anything that doesn't fit, and your edit is always faster than composing.

## Practice once before you need it

Fill one template for a problem you've already resolved (that time the streaming service charged twice, maybe). You'll learn the slots in five minutes, and when a real dispute shows up, you'll reach for the folder instead of the worry spiral. That's the whole point of this manual.

---

*Previous: [Chapter 6 — AI Tone Review](06-ai-tone-review.md) · Back to [Start Here](00-start-here.md)*
