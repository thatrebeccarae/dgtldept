#!/usr/bin/env python3
"""
Collect SKILL.md frontmatter from all skills into catalog.json.
No external dependencies — parses the simple YAML frontmatter manually.

Usage:
    python3 scripts/collect-metadata.py
    python3 scripts/collect-metadata.py --output docs/catalog.json
"""

import datetime
import json
import os
import re
import sys
from pathlib import Path


SKILLS_DIR = Path(__file__).parent.parent / "skills"
SKIP_DIRS = {"shared"}

# Category display names and order
CATEGORIES = {
    "paid-media": {"label": "Paid Media", "order": 1},
    "seo": {"label": "SEO & AI Search", "order": 2},
    "content": {"label": "Content", "order": 3},
    "growth": {"label": "Growth & Conversion", "order": 4},
    "strategy": {"label": "Strategy & Research", "order": 5},
    "email-lifecycle": {"label": "Email & Lifecycle", "order": 6},
    "analytics": {"label": "Analytics", "order": 7},
    "creative": {"label": "Creative & Design", "order": 8},
    "reporting": {"label": "Reporting & Deliverables", "order": 9},
    "devops": {"label": "DevOps", "order": 11},
}


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from --- delimited block. Handles one level of nesting."""
    match = re.match(r"^---\n(.*?\n)---", content, re.DOTALL)
    if not match:
        return {}

    result = {}
    current_parent = None

    for line in match.group(1).strip().splitlines():
        # Nested key (2-space indent)
        if line.startswith("  ") and current_parent is not None:
            key, _, value = line.strip().partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            result[current_parent][key] = value
        # Parent key with no value (start of nested block)
        elif ":" in line and line.split(":", 1)[1].strip() == "":
            current_parent = line.split(":", 1)[0].strip()
            result[current_parent] = {}
        # Simple key: value
        elif ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            result[key] = value
            current_parent = None

    return result


def extract_first_paragraph(content: str) -> str:
    """Extract the first non-heading paragraph after frontmatter as the summary."""
    # Strip frontmatter
    body = re.sub(r"^---\n.*?\n---\n*", "", content, flags=re.DOTALL)
    # Skip the H1 title
    body = re.sub(r"^#[^#].*\n*", "", body)
    # Skip install section if it comes first
    body = re.sub(r"^## Install\n```.*?```\n*", "", body, flags=re.DOTALL)
    # Get first non-empty paragraph
    for para in body.split("\n\n"):
        para = para.strip()
        if para and not para.startswith("#") and not para.startswith(">") and not para.startswith("```"):
            return para
    return ""


def extract_capabilities(content: str) -> list:
    """Extract H3 section names under Core Capabilities or similar."""
    caps = []
    in_capabilities = False
    for line in content.splitlines():
        if re.match(r"^## (Core Capabilities|Capabilities|Design Thinking|Key Features)", line):
            in_capabilities = True
            continue
        if in_capabilities and line.startswith("## "):
            break
        if in_capabilities and line.startswith("### "):
            cap = line.lstrip("# ").strip()
            # Remove numbering like "1. "
            cap = re.sub(r"^\d+\.\s*", "", cap)
            caps.append(cap)
    return caps


def collect_skills() -> list:
    """Walk skills/ and collect metadata from each SKILL.md."""
    skills = []

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name in SKIP_DIRS:
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text()
        fm = parse_frontmatter(content)
        meta = fm.get("metadata", {})

        category_key = meta.get("category", "uncategorized")
        category_info = CATEGORIES.get(category_key, {"label": category_key, "order": 99})

        skill = {
            "slug": skill_dir.name,
            "name": fm.get("name", skill_dir.name),
            "description": fm.get("description", ""),
            "summary": extract_first_paragraph(content),
            "category": category_key,
            "category_label": category_info["label"],
            "category_order": category_info["order"],
            "domain": meta.get("domain", ""),
            "version": meta.get("version", ""),
            "updated": meta.get("updated", ""),
            "tested": meta.get("tested", ""),
            "tested_with": meta.get("tested_with", ""),
            "capabilities": extract_capabilities(content),
            "has_scripts": (skill_dir / "scripts").is_dir(),
            "has_reference": (skill_dir / "REFERENCE.md").exists(),
            "has_examples": (skill_dir / "EXAMPLES.md").exists(),
            "install_command": f"git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/{skill_dir.name} ~/.claude/skills/",
        }

        skills.append(skill)

    # Sort by category order, then name
    skills.sort(key=lambda s: (s["category_order"], s["name"]))

    return skills


def build_catalog(skills: list) -> dict:
    """Build the full catalog structure."""
    # Group by category
    categories = {}
    for skill in skills:
        cat = skill["category"]
        if cat not in categories:
            categories[cat] = {
                "key": cat,
                "label": skill["category_label"],
                "order": skill["category_order"],
                "skills": [],
            }
        categories[cat]["skills"].append(skill)

    return {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "total_skills": len(skills),
        "total_categories": len(categories),
        "categories": sorted(categories.values(), key=lambda c: c["order"]),
        "skills": skills,
    }


def main():
    output_path = "docs/catalog.json"
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    skills = collect_skills()
    catalog = build_catalog(skills)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(catalog, indent=2) + "\n")

    print(f"Collected {catalog['total_skills']} skills across {catalog['total_categories']} categories")
    print(f"Written to {output_path}")

    # Summary
    for cat in catalog["categories"]:
        print(f"  {cat['label']}: {len(cat['skills'])} skills")


if __name__ == "__main__":
    main()
