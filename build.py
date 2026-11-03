#!/usr/bin/env python3
"""Build the static site for Complaints That Get Results.

Converts docs/*.md into site/*.html with the `markdown` package, generates the
editable-templates gallery from site/templates-src/*.md, copies templates and
LICENSE into the output tree, validates every page (tag balance + internal
links), and exits non-zero on any problem.

Usage: python3 build.py
"""

import re
import shutil
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit(
        "The 'markdown' package is required. Install it with: pip install markdown"
    )

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"
TEMPLATES_SRC = SITE / "templates-src"   # committed source (.md letters)
TEMPLATES_OUT = SITE / "templates"       # generated copies for delivery
ASSETS = SITE / "assets"

PAGE_MAP = {
    "00-start-here.md": "index.html",
    "01-gather-records-first.md": "gather-records.html",
    "02-escalation-ladder.md": "escalation-ladder.html",
    "03-complaint-letter-anatomy.md": "letter-anatomy.html",
    "04-deadline-calendars.md": "deadlines.html",
    "05-small-claims-basics.md": "small-claims.html",
    "06-ai-tone-review.md": "ai-tone-review.html",
    "07-free-everyday-letters-pack.md": "letters-pack.html",
}

NAV = [
    ("index.html", "Start here"),
    ("gather-records.html", "1 · Records"),
    ("escalation-ladder.html", "2 · Ladder"),
    ("letter-anatomy.html", "3 · Letters"),
    ("deadlines.html", "4 · Deadlines"),
    ("small-claims.html", "5 · Small claims"),
    ("ai-tone-review.html", "6 · AI review"),
    ("letters-pack.html", "7 · Letters pack"),
    ("templates.html", "Templates"),
]

FOOTNOTE_DISCLAIMER = (
    "Education, not legal advice. Results depend on your own records, your "
    "chosen jurisdiction and its published rules."
)


def esc(text: str) -> str:
    for old, new in (("&", "&amp;"), ("<", "&lt;"), (">", "&gt;")):
        text = text.replace(old, new)
    return text


def rewrite_links(html: str) -> str:
    """Point markdown-relative links at generated site pages."""

    def repl(match):
        target = match.group("target")
        if target.startswith(("http:", "https:", "mailto:", "tel:")):
            return match.group(0)
        base, _, anchor = target.partition("#")
        anchor = f"#{anchor}" if anchor else ""
        if base in PAGE_MAP:
            return f'href="{PAGE_MAP[base]}{anchor}"'
        if base.endswith("index.html"):
            return f'href="templates.html"'
        if base.endswith("LICENSE"):
            return 'href="LICENSE"'
        return match.group(0)

    return re.sub(r'href="(?P<target>[^"]+)"', repl, html)


def nav_html(active: str) -> str:
    links = "\n".join(
        f'<a href="{href}" class="nav-link{" active" if href == active else ""}">{label}</a>'
        for href, label in NAV
    )
    brand = '<a href="index.html" class="brand">Complaints That Get Results</a>'
    return f'<nav class="topnav">{brand}<div class="nav-links">{links}</div></nav>'


def shell(title: str, body: str, active: str, description: str) -> str:
    nav = nav_html(active)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<title>{title} — Complaints That Get Results</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
{nav}
<main class="page">{body}</main>
<footer class="site-footer">
  <div class="footer-inner">
    <p><strong>Complaints That Get Results</strong> — a plain-English dispute manual.</p>
    <p>{FOOTNOTE_DISCLAIMER}</p>
    <p>© 2026 Asdale Dynamics, LLC · <a href="LICENSE">MIT License</a> · paired with the free <a href="templates.html">Everyday Letters Pack</a></p>
  </div>
</footer>
</body>
</html>
"""


GALLERY_JS = """
<script>
function copyLetter(id, btn) {
  var box = document.getElementById(id);
  navigator.clipboard.writeText(box.value).then(function () {
    btn.textContent = 'Copied!';
    setTimeout(function () { btn.textContent = 'Copy'; }, 1500);
  });
}
function downloadLetter(id, name) {
  var text = document.getElementById(id).value;
  var blob = new Blob([text], { type: 'text/markdown' });
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  URL.revokeObjectURL(a.href);
}
</script>
"""


def split_usage(body: str):
    """Everything before the fence = usage note; inside the fence = the letter."""
    note_lines, letter_lines, in_letter = [], [], False
    for line in body.splitlines():
        stripped = line.strip()
        if not in_letter and stripped.startswith("```"):
            in_letter = True
            continue
        if in_letter and stripped == "```":
            continue
        (letter_lines if in_letter else note_lines).append(line)
    return "\n".join(note_lines).strip(), "\n".join(letter_lines).strip()


INTRO_MD = """## How to use one

1. Pick the letter that matches your Chapter 2 escalation rung.
2. Edit it below (or open the raw `.md` file), then save a copy in your dispute folder's `04-letters-sent/` folder.
3. Redact personal details first, then run the AI tone review from [Chapter 6](ai-tone-review.html).
4. Send it, log it in `00-log.md`, and set the two calendar reminders from [Chapter 4](deadlines.html).
"""


def build_templates_page() -> str:
    sections = []
    for md_path in sorted(TEMPLATES_SRC.glob("*.md")):
        slug = md_path.stem
        raw = md_path.read_text(encoding="utf-8")
        title = raw.splitlines()[0].lstrip("# ").strip()
        usage_note, letter = split_usage(raw.split("\n", 1)[1])
        note_html = markdown.markdown(usage_note, extensions=["tables"])
        sections.append(
            f"""<section class="template-card" id="{slug}">
<h2>{title}</h2>
<div class="template-note">{note_html}</div>
<textarea id="{slug}" name="{slug}" spellcheck="false" rows="30" aria-label="Editable {title}">{esc(letter.strip())}</textarea>
<div class="template-actions">
<button class="btn" type="button" onclick="copyLetter('{slug}', this)">Copy</button>
<button class="btn" type="button" onclick="downloadLetter('{slug}', '{slug}.md')" download>Download .md</button>
<span class="raw-link-code"><code>site/templates-src/{slug}.md</code></span>
</div>
</section>"""
        )
    intro_html = markdown.markdown(INTRO_MD, extensions=["tables"])
    body = f"""<header class="page-header">
<p class="kicker">The free Everyday Letters Pack — five fill-in-the-blanks letters</p>
<h1>Letter Templates</h1>
<p class="lede">Editable right in this page, plus raw files in <code>site/templates-src/</code>.
Fill every slot, delete what doesn't apply, then run the Chapter 6 redaction + tone review. Keep each letter to one page.</p>
</header>
{intro_html}
{''.join(sections)}{GALLERY_JS}"""
    return shell(
        "Templates",
        body,
        "templates.html",
        "Editable complaint letter templates — the free Everyday Letters Pack",
    )


def build_docs_pages() -> dict:
    pages = {}
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc"],
        output_format="html5",
    )
    for doc_name, page_name in PAGE_MAP.items():
        text = (DOCS / doc_name).read_text(encoding="utf-8")
        md.reset()
        html = md.convert(text)
        html = rewrite_links(html)
        first_heading = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        title = (
            re.sub(r"<[^>]+>", "", first_heading.group(1)).strip()
            if first_heading
            else doc_name
        )
        if page_name == "index.html":
            html = (
                '<header class="page-header"><p class="kicker">A plain-English, beginner-friendly manual from Asdale Dynamics, LLC</p>'
                '<h1>Complaints That Get Results</h1>'
                '<p class="lede">Polite, step-by-step dispute resolution for real people: records, escalation ladders, letters, deadlines, small claims, and safe AI tone review. Generated from <code>docs/</code> — the same chapters live there as editable Markdown.</p></header>\n'
                + html
            )
        pages[page_name] = shell(
            title, html, page_name, f"{title} — the plain-English dispute manual"
        )
    return pages


VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
TAG_PATTERN = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9-]*)([^>]*?)(/?)>")


def check_tag_balance(page_name: str, html: str) -> list:
    problems, stack = [], []
    for match in TAG_PATTERN.finditer(html):
        closing, tag, self_close = match.group(1), match.group(2).lower(), match.group(4)
        if self_close or (not closing and tag in VOID_TAGS):
            continue
        if closing:
            if not stack:
                problems.append(f"{page_name}: unmatched closing </{tag}>")
            elif stack[-1] == tag:
                stack.pop()
            elif tag in stack:
                problems.append(f"{page_name}: expected </{stack[-1]}>, got </{tag}>")
                while stack and stack.pop() != tag:
                    pass
            else:
                problems.append(f"{page_name}: stray closing </{tag}>")
        else:
            stack.append(tag)
    for tag in stack:
        problems.append(f"{page_name}: unclosed <{tag}>")
    return problems


def validate(pages: dict) -> list:
    problems = []
    known_files = set(pages) | {"assets/style.css", "LICENSE"}
    known_files.update(f"templates/{p.name}" for p in sorted(TEMPLATES_OUT.glob("*.md")))
    known_anchors = {
        name: set(re.findall(r'<[^>]+ id="([^"]+)"', html)) for name, html in pages.items()
    }
    for page_name, html in pages.items():
        for attr, target in re.findall(r'(href|src)="([^"]+)"', html):
            if target.startswith(("http:", "https:", "mailto:", "tel:")):
                continue
            path_part, _, anchor = target.partition("#")
            if not path_part:
                continue
            if path_part not in known_files:
                problems.append(f"{page_name}: link to unknown file '{path_part}'")
                continue
            if anchor and path_part in known_anchors and anchor not in known_anchors[path_part]:
                problems.append(f"{page_name}: broken anchor '{anchor}' in {path_part}")
        problems.extend(check_tag_balance(page_name, html))
    return problems


def write_output(pages: dict) -> None:
    for page_name, html in pages.items():
        (SITE / page_name).write_text(html, encoding="utf-8")
    if TEMPLATES_OUT.exists():
        shutil.rmtree(TEMPLATES_OUT)
    TEMPLATES_OUT.mkdir(parents=True)
    for src in sorted(TEMPLATES_SRC.glob("*.md")):
        shutil.copy2(src, TEMPLATES_OUT / src.name)
    license_src = ROOT / "LICENSE"
    if license_src.exists():
        shutil.copy2(license_src, SITE / "LICENSE")


def main() -> int:
    pages = build_docs_pages()
    pages["templates.html"] = build_templates_page()
    write_output(pages)
    problems = validate(pages)
    if problems:
        print(f"BUILD FAILED: {len(pages)} pages generated, {len(problems)} problem(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"BUILD OK: {len(pages)} pages generated in site/.")
    for name in sorted(pages):
        print(f"  site/{name}")
    check = ASSETS / "style.css"
    print(" Stylesheet: site/assets/style.css" if check.exists() else "WARNING: site/assets/style.css missing; pages will render unstyled.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
