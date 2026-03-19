# llms.txt Generator — Reference

## llms.txt Specification Format

The specification (from [llmstxt.org](https://llmstxt.org)) defines a simple markdown structure:

```markdown
# Project Name

> Brief project description in 2-3 sentences. What it does, who it is for,
> and its primary value proposition.

## Section Name

- [Page Title](url-or-path): One-line description of what this page covers
- [Page Title](url-or-path): One-line description of what this page covers
```

### Format Rules

1. **Title**: Single H1 with the project name
2. **Description**: Blockquote immediately after the title. 2-3 sentences. Answers: what is this, who uses it, what problem does it solve.
3. **Sections**: H2 headings grouping related content. Flat structure — no H3 nesting.
4. **Items**: Unordered list with markdown link, colon, one-line description
5. **Plain markdown**: No HTML, no frontmatter, no metadata beyond the content itself

## llms-full.txt Format

The expanded companion inlines actual page content so an LLM can consume the entire project in one pass. Use H3 headings for each inlined page under H2 section headings.

- **Generate when**: Small/mid-size projects (~50K tokens total docs), or when primary goal is LLM comprehension
- **Skip when**: Large doc sites (>100 pages), frequently changing docs, or docs already well-structured individually

## Priority Ranking Criteria

| Priority | Content Types | Rationale |
|----------|-------------|-----------|
| **P0** | README, Getting Started, API Reference, Install guide | Entry points — identity, first action, core contract |
| **P1** | Tutorials, Guides, Architecture, Config reference, Migration guides | Deeper understanding — workflows, design, upgrades |
| **P2** | CHANGELOG, CONTRIBUTING, FAQ, Security policy, License, Roadmap | Supporting context — history, community, compliance |

**Exclude**: Auto-generated API docs with no narrative, internal dev notes, draft RFCs, test fixtures, duplicate content.

## Writing Effective Descriptions

| Guideline | Good | Bad |
|-----------|------|-----|
| Action-oriented | "How to deploy to production with Docker" | "Deployment documentation" |
| Specific | "Configure OAuth2 with Google, GitHub, and SAML" | "Authentication setup" |
| User-focused | "Troubleshoot common connection errors" | "Error reference" |
| Concise | One line, under 100 characters | Multi-sentence explanations |

### Description Patterns by Content Type

| Type | Pattern |
|------|---------|
| Getting started | "Install [project] and run your first [action] in under 5 minutes" |
| API reference | "Complete API reference with endpoints, parameters, and response schemas" |
| Tutorial | "Build a [thing] using [feature] — step-by-step walkthrough" |
| Config reference | "All configuration options with defaults, types, and examples" |
| Migration guide | "Upgrade from v[X] to v[Y] — breaking changes and migration steps" |
| Contributing | "How to contribute — development setup, PR process, and code standards" |

## File Placement

**Repository**: Place `llms.txt` in the repo root alongside README.md.

**Hosted docs**: Serve at the site root (`https://docs.example.com/llms.txt`).

| Platform | Location |
|----------|---------|
| GitHub Pages | Root of source branch |
| Docusaurus | `static/llms.txt` |
| MkDocs | `docs/llms.txt` with extra config |
| Next.js | `public/llms.txt` |
| Hugo | `static/llms.txt` |

Optionally reference in robots.txt: `LLMs-Txt: https://example.com/llms.txt`

## How AI Answer Engines Use llms.txt

1. **RAG retrieval**: Curated index helps AI identify relevant pages, reducing hallucination
2. **Content mapping**: Section structure builds a mental model without reading every page
3. **Citation sourcing**: Pre-written descriptions enable accurate citations
4. **Context efficiency**: Full project understanding in a fraction of the tokens vs crawling

## Auto-Regeneration with GitHub Actions

The [demodrive-ai/llms-txt-action](https://github.com/demodrive-ai/llms-txt-action) GitHub Action auto-regenerates llms.txt on push or schedule:

```yaml
name: Update llms.txt
on:
  push:
    branches: [main]
    paths: ['docs/**', 'README.md']
  schedule:
    - cron: '0 6 * * 1'  # weekly Monday 6am

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: demodrive-ai/llms-txt-action@v1
        with:
          output: llms.txt
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: regenerate llms.txt"
```

Auto-generated files benefit from manual curation. The action provides a starting point, but hand-tuned descriptions and section organization will outperform fully automated output.
