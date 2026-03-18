#!/usr/bin/env python3
"""
Generate static skill detail pages at docs/skill/{slug}.html.
Each page has unique meta tags for SEO and renders the full skill detail.
On the skills.html page, these load as modals via JS interception.

Usage:
    python3 scripts/generate-skill-pages.py
"""

import json
import os
import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"
SKILLS_DIR = Path(__file__).parent.parent / "skills"
CATALOG_PATH = DOCS_DIR / "catalog.json"
OUTPUT_DIR = DOCS_DIR / "skill"

GA4_ID = "G-00XHYRHCX4"
BASE_URL = "https://thatrebeccarae.github.io/claude-marketing"
REPO_URL = "https://github.com/thatrebeccarae/claude-marketing"


def extract_skill_body(slug: str) -> str:
    """Extract the markdown body after frontmatter, skip title and install section."""
    skill_md = SKILLS_DIR / slug / "SKILL.md"
    if not skill_md.exists():
        return ""

    content = skill_md.read_text()
    # Strip frontmatter
    body = re.sub(r"^---\n.*?\n---\n*", "", content, flags=re.DOTALL)
    # Skip H1 title
    body = re.sub(r"^#[^#].*\n*", "", body)
    # Skip install section
    body = re.sub(r"^## Install\n```.*?```\n*", "", body, flags=re.DOTALL)
    return body.strip()


def md_to_html_simple(md: str) -> str:
    """Minimal markdown to HTML conversion for skill body content."""
    lines = md.split("\n")
    html_lines = []
    in_list = False
    in_code = False
    code_block = []

    for line in lines:
        # Code blocks
        if line.startswith("```"):
            if in_code:
                html_lines.append('<pre><code>' + escape_html('\n'.join(code_block)) + '</code></pre>')
                code_block = []
                in_code = False
            else:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                in_code = True
            continue

        if in_code:
            code_block.append(line)
            continue

        # Headers
        if line.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<h3>{escape_html(line[4:])}</h3>')
            continue
        if line.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<h2>{escape_html(line[3:])}</h2>')
            continue

        # List items
        if line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            # Handle bold in list items
            item = escape_html(line[2:])
            item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
            html_lines.append(f"<li>{item}</li>")
            continue

        # Blockquotes
        if line.startswith("> "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            quote = escape_html(line[2:])
            quote = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', quote)
            html_lines.append(f'<blockquote>{quote}</blockquote>')
            continue

        # Empty line
        if not line.strip():
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        # Paragraph
        if in_list:
            html_lines.append("</ul>")
            in_list = False
        text = escape_html(line)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        html_lines.append(f"<p>{text}</p>")

    if in_list:
        html_lines.append("</ul>")
    if in_code:
        html_lines.append('<pre><code>' + escape_html('\n'.join(code_block)) + '</code></pre>')

    return "\n".join(html_lines)


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def generate_page(skill: dict) -> str:
    slug = skill["slug"]
    name = skill["name"]
    desc = skill["description"]
    category = skill.get("category_label", skill.get("category", ""))
    tested = skill.get("tested", "")
    tested_with = skill.get("tested_with", "")
    install = skill.get("install_command", f"git clone {REPO_URL}.git && cp -r claude-marketing/skills/{slug} ~/.claude/skills/")
    capabilities = skill.get("capabilities", [])

    # Get the full skill body
    body_md = extract_skill_body(slug)
    body_html = md_to_html_simple(body_md) if body_md else ""

    tested_line = ""
    if tested:
        tested_line = f"Tested {tested}"
        if tested_with:
            tested_line += f" &middot; {escape_html(tested_with)}"

    caps_html = ""
    if capabilities:
        caps_items = "".join(f"<li>{escape_html(c)}</li>" for c in capabilities)
        caps_html = f'<div class="detail-capabilities"><h2>Capabilities</h2><ul>{caps_items}</ul></div>'

    source_links = f'''<div class="detail-sources">
<h2>Source Files</h2>
<div class="detail-source-links">
<a href="{REPO_URL}/tree/main/skills/{slug}/SKILL.md" target="_blank" rel="noopener">SKILL.md</a>
<a href="{REPO_URL}/tree/main/skills/{slug}/REFERENCE.md" target="_blank" rel="noopener">REFERENCE.md</a>
<a href="{REPO_URL}/tree/main/skills/{slug}/EXAMPLES.md" target="_blank" rel="noopener">EXAMPLES.md</a>
</div>
</div>'''

    return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape_html(name)} — claude-marketing</title>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA4_ID}');
</script>
<meta name="description" content="{escape_html(desc[:160])}">
<meta property="og:title" content="{escape_html(name)} — claude-marketing">
<meta property="og:description" content="{escape_html(desc[:200])}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{escape_html(name)} — claude-marketing">
<meta name="twitter:description" content="{escape_html(desc[:200])}">
<link rel="canonical" href="{BASE_URL}/skill/{slug}.html">
<link href="https://api.fontshare.com/v2/css?f[]=switzer@300,400,500,600,700&display=swap" rel="stylesheet">
<style>
@font-face {{
  font-family: 'PP Editorial New';
  src: url('../fonts/PPEditorialNew-Ultralight.woff2') format('woff2');
  font-weight: 200;
  font-style: normal;
  font-display: swap;
}}
@font-face {{
  font-family: 'PP Editorial New';
  src: url('../fonts/PPEditorialNew-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}}
@font-face {{
  font-family: 'Cartograph CF';
  src: url('../fonts/CartographCF-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}}

*, *::before, *::after {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

:root {{
  --accent: #5B5F8D;
  --black: #000000;
  --white: #ffffff;
  --ease: cubic-bezier(0.215, 0.61, 0.355, 1);
}}

html {{
  background: #000000;
  color: #ffffff;
}}

body {{
  font-family: 'Switzer', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: clamp(15px, 1.1vw, 17px);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  max-width: 100vw;
  overflow-x: hidden;
}}

a {{ color: inherit; text-decoration: none; }}

.detail-page {{
  max-width: 720px;
  margin: 0 auto;
  padding: 120px clamp(20px, 5vw, 40px) 80px;
}}

.detail-back {{
  font-family: 'Cartograph CF', monospace;
  font-size: 0.8rem;
  text-transform: uppercase;
  opacity: 0.5;
  transition: opacity 0.2s var(--ease);
  display: inline-block;
  margin-bottom: 2rem;
}}
.detail-back:hover {{ opacity: 1; }}

.detail-name {{
  font-family: 'PP Editorial New', 'Georgia', serif;
  font-size: clamp(2rem, 4vw, 3.5rem);
  font-weight: 200;
  line-height: 1.15;
  letter-spacing: -0.014em;
  margin-bottom: 0.5rem;
}}

.detail-category {{
  font-family: 'Cartograph CF', monospace;
  font-size: 0.8rem;
  text-transform: uppercase;
  opacity: 0.5;
  letter-spacing: 0.04em;
  margin-bottom: 2rem;
}}

.detail-desc {{
  font-size: 1.1rem;
  font-weight: 300;
  line-height: 1.65;
  margin-bottom: 2.5rem;
  opacity: 0.85;
}}

.detail-install {{
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin-bottom: 2.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}}

.detail-install code {{
  font-family: 'Cartograph CF', monospace;
  font-size: 0.75rem;
  opacity: 0.6;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}}

.detail-install .copy-btn {{
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  opacity: 0.5;
  transition: opacity 0.2s var(--ease);
  color: #ffffff;
  flex-shrink: 0;
}}
.detail-install .copy-btn:hover {{ opacity: 0.8; }}
.detail-install .copy-btn.copied {{ opacity: 1; color: #4ade80; }}

.detail-tested {{
  font-family: 'Cartograph CF', monospace;
  font-size: 0.75rem;
  text-transform: uppercase;
  opacity: 0.4;
  margin-bottom: 2.5rem;
}}

.detail-capabilities h2,
.detail-sources h2,
.detail-body h2 {{
  font-size: 1.1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  margin-top: 2.5rem;
}}

.detail-capabilities ul {{
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}}

.detail-capabilities li {{
  font-family: 'Cartograph CF', monospace;
  font-size: 0.75rem;
  text-transform: uppercase;
  padding: 0.4rem 0.8rem;
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 4px;
}}

.detail-source-links {{
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}}

.detail-source-links a {{
  font-family: 'Cartograph CF', monospace;
  font-size: 0.8rem;
  text-transform: uppercase;
  padding: 0.5rem 1rem;
  border: 1px solid #ffffff;
  border-radius: 45px;
  transition: background 0.2s var(--ease), color 0.2s var(--ease);
}}
.detail-source-links a:hover {{
  background: #ffffff;
  color: #000000;
}}

.detail-body {{
  margin-top: 2.5rem;
  border-top: 1px solid rgba(255,255,255,0.1);
  padding-top: 2rem;
}}

.detail-body h2 {{
  font-family: 'Switzer', sans-serif;
}}

.detail-body h3 {{
  font-size: 1rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}}

.detail-body p {{
  margin-bottom: 1rem;
  opacity: 0.85;
  line-height: 1.65;
}}

.detail-body ul {{
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}}

.detail-body li {{
  margin-bottom: 0.35rem;
  opacity: 0.85;
  line-height: 1.55;
}}

.detail-body pre {{
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  overflow-x: auto;
}}

.detail-body code {{
  font-family: 'Cartograph CF', monospace;
  font-size: 0.85rem;
}}

.detail-body blockquote {{
  border-left: 2px solid rgba(255,255,255,0.2);
  padding-left: 1rem;
  margin-bottom: 1rem;
  opacity: 0.7;
  font-style: italic;
}}

@media (max-width: 700px) {{
  .detail-page {{
    padding: 100px 20px 60px;
  }}
  .detail-source-links {{
    flex-wrap: wrap;
  }}
}}
</style>
</head>
<body>
<div class="detail-page" data-pagefind-body>
  <a href="../skills.html" class="detail-back">&larr; Back to skills</a>
  <h1 class="detail-name">{escape_html(name)}</h1>
  <div class="detail-category">{escape_html(category)}</div>
  <p class="detail-desc">{escape_html(desc)}</p>
  <div class="detail-install">
    <code>{escape_html(install)}</code>
    <button class="copy-btn" data-copy="{escape_html(install)}" title="Copy install command" onclick="copyInstall(this)">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
    </button>
  </div>
  {f'<div class="detail-tested">{tested_line}</div>' if tested_line else ''}
  {caps_html}
  {source_links}
  {f'<div class="detail-body">{body_html}</div>' if body_html else ''}
</div>
<script>
function copyInstall(btn) {{
  var text = btn.getAttribute('data-copy');
  navigator.clipboard.writeText(text).then(function() {{
    btn.classList.add('copied');
    btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
    setTimeout(function() {{
      btn.classList.remove('copied');
      btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
    }}, 2000);
  }});
}}
</script>
</body>
</html>'''


def main():
    with open(CATALOG_PATH) as f:
        catalog = json.load(f)

    skills = catalog.get("skills", [])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for skill in skills:
        slug = skill["slug"]
        html = generate_page(skill)
        output_path = OUTPUT_DIR / f"{slug}.html"
        output_path.write_text(html)

    print(f"Generated {len(skills)} skill detail pages in docs/skill/")
    for skill in skills:
        print(f"  docs/skill/{skill['slug']}.html")


if __name__ == "__main__":
    main()
