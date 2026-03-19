# GitHub README — Examples

---

## Example 1: Generate README for a TypeScript CLI Tool

**Prompt:**
> Generate a README for this repo. It's a CLI tool for bulk-renaming files with regex patterns.

**Expected output:** Title + badges (TypeScript, Node.js >=18, MIT license, GitHub stars), one-line description, and these sections:

- **Why I Built This** — Skill asks user for motivation, never fabricates
- **Getting Started** — Prerequisites (Node >= 18), `npm install -g rename-cli`
- **Commands** — Table format:

| Command | Description |
|---------|-------------|
| `rename match <pattern>` | Preview files matching the regex |
| `rename apply <pattern> <replacement>` | Rename all matched files |
| `rename undo` | Revert last rename operation |

- **Configuration** — `.renamerc` options
- **Contributing** — Fork/branch/PR instructions
- **License** — MIT

Professional voice. No emojis in prose. No "Why I Built This" fabrication. `for-the-badge` style on all badges.

---

## Example 2: Generate README for a Python Library

**Prompt:**
> Generate a README for this Python library that provides rate-limiting decorators for async functions.

**Expected output:** Title + badges (Python 3.11+, PyPI version, MIT license, stars), then:

- **Why I Built This** — User-provided
- **Getting Started** — `pip install ratelimit-async` / `poetry add ratelimit-async`
- **Quick Start** — Working code example:
```python
from ratelimit_async import limit

@limit(calls=10, period=60)
async def fetch_data(url: str) -> dict:
    ...
```
- **API Reference** — Function signatures with parameter docs:
  - `@limit(calls, period, strategy="sliding_window")` — params, types, defaults
  - `@limit_concurrent(max_concurrent)` — concurrency cap
  - `RateLimitExceeded` — exception class
- **Contributing** / **License**

Technical voice. Function signatures are exact. Install commands cover pip and poetry.

---

## Example 3: Generate README for a Skill/Template Collection

**Prompt:**
> Generate a README for this repo. It contains 30+ Claude Code skills for marketing.

**Expected output:** Title + badges (Claude Code, MIT, stars, LinkedIn, X — social badges because user confirms flagship), then:

- **Why I Built This** — User-provided
- **Quick Start** — Clone, copy to `~/.claude/skills/`, invoke with `/skill-name`
- **Skills Catalog** — Categorized tables (not a flat list):

| Skill | Description |
|-------|-------------|
| `gcd-producer` | Generate content drafts from briefs |
| `github-readme` | Generate, audit, or update repo READMEs |
| `research-analyst` | Deep research briefs with source synthesis |

- **How Skills Work** — SKILL.md structure, tool access
- **Composing Skills** — Chaining workflows (research -> produce -> review)
- **Configuration** / **Contributing** / **License**

Catalog voice — organized, browsable. Skills grouped by category with tables.

---

## Example 4: Audit an Existing README

**Prompt:**
> Audit the README for this repo.

**Expected output (read-only, no files modified):**

```
=== README Audit: rename-cli ===
Score: 68/100

  Description:   12/15 — Clear but doesn't mention target audience
  Installation:  15/20 — npm command works but missing prerequisites
  Usage:          8/20 — No code examples, only text description
  Badges:         5/10 — License badge missing, npm badge stale
  Structure:     10/15 — Good order but missing Contributing section
  Completeness:   8/10
  Freshness:     10/10

FAIL:
  - Required badge missing: License
  - npm badge URL returns 404 (package name mismatch)
  - No Contributing section (public repo)

WARN:
  - Badge style inconsistent (mixing flat and for-the-badge)
  - "Install" should be "Getting Started"
  - One paragraph exceeds 4 sentences

Discoverability:
  - Repo description empty — add: "Bulk-rename files with regex patterns"
  - No topics — suggest: typescript, cli, file-rename, regex
  - No social preview image

Suggested fixes:
  - Add: [![License: MIT](https://img.shields.io/github/license/...)]
  - Fix npm badge package name: "rename-cli" not "rename"
  - Add Contributing section with fork/branch/PR instructions
```

Scored with category breakdown per REFERENCE.md rubric. Includes discoverability audit for repo metadata (description, topics, social preview).

---

## Example 5: Update README After Adding Features

**Prompt:**
> Update the README. We added a --dry-run flag and dropped Node 16 support.

**Expected output — diff-style preview:**

```
=== README Update Plan: rename-cli ===
5 changes proposed:

1. [BADGE] Node.js version
   - Node.js-%3E%3D16
   + Node.js-%3E%3D18

2. [SECTION] Commands table — add --dry-run
   + | `rename apply --dry-run` | Preview renames without executing |

3. [SECTION] Getting Started — prerequisites
   - Node.js >= 16
   + Node.js >= 18

4. [STRUCTURE] Nav anchors missing Configuration link

5. [VOICE] Hedge language in Why I Built This
   - "This might be useful if you need to..."
   + "I built this because renaming files in bulk shouldn't require..."

Apply all changes? [y/N/select]
```

User responds `select 1,2,3` — applies badge update, new command row, and prerequisites only. Skips nav anchors and voice rewrite.

```
=== README Updated: rename-cli ===
Changes applied: 3 of 5
PII/Infra scrub: PASS
Updated: /path/to/repo/README.md
```

Selective apply lets user accept feature updates while deferring style fixes. PII scrub runs on final output regardless.
