# llms-txt


# llms.txt Generator

Generate and maintain llms.txt files that help AI answer engines surface your project accurately.

## When to Use

- Launching a new open-source project or documentation site
- Major documentation restructure or content overhaul
- Improving your project's visibility in AI search (ChatGPT, Perplexity, Google AI Overviews)
- Onboarding a project to AI-friendly discoverability standards
- Periodic refresh after significant repo changes

## What Is llms.txt

llms.txt is a plain-text markdown file placed in a project's root that gives LLMs a curated map of the project's most important content. Think of it as robots.txt for AI comprehension — instead of telling crawlers where they can go, it tells them what matters and how the project is organized.

The specification was proposed by Answer.AI and is documented at [llmstxt.org](https://llmstxt.org). Adoption is growing across developer tools, documentation sites, and open-source projects. Projects with an llms.txt are easier for AI to understand, cite, and recommend accurately.

## Usage

### `/llms-txt generate [repo-path]`

Scan a repository and generate a new llms.txt file. If no path is provided, uses the current working directory.

### `/llms-txt audit [repo-path]`

Check an existing llms.txt for completeness, broken links, stale descriptions, and missing high-priority content. Produces a report with specific recommendations.

### `/llms-txt update [repo-path]`

Refresh an existing llms.txt based on current repo state. Preserves manually curated descriptions while adding new content and removing references to deleted files.

## Procedure

### Step 1: Scan Repo Structure

Identify all documentation-relevant files in the repository:

- README.md (root and significant subdirectories)
- `docs/` directory and its contents
- API documentation (OpenAPI specs, API reference pages)
- Tutorials, guides, and getting-started content
- CHANGELOG.md, CONTRIBUTING.md, FAQ.md
- Architecture and design decision docs
- Configuration and deployment guides
- Example directories with their own READMEs

### Step 2: Prioritize Content

Rank discovered content by importance to an LLM trying to understand the project:

| Priority | Content Type | Why It Matters |
|----------|-------------|---------------|
| **P0** | README, Getting Started, API Reference | Entry points — what the project is and how to use it |
| **P1** | Tutorials, Guides, Architecture docs | Deeper understanding — how it works and common workflows |
| **P2** | CHANGELOG, CONTRIBUTING, FAQ, Config docs | Supporting context — history, community, troubleshooting |

### Step 3: Extract Metadata

For each content page, extract or write:

- **Title**: Clear, descriptive page title
- **URL or path**: Where to find the content (full URL for hosted docs, relative path for repo files)
- **Description**: One-line action-oriented summary of what the page covers

### Step 4: Generate llms.txt

Assemble the file following the specification format:

1. **Title line**: `# Project Name`
2. **Description block**: 2-3 sentence summary of what the project does, who it is for, and its primary use case
3. **Sections**: Group content logically (e.g., "Getting Started", "API", "Guides", "Community")
4. **Content items**: Each item is a markdown link with a colon-separated description

See REFERENCE.md for the exact format specification.

### Step 5: Optionally Generate llms-full.txt

For projects that benefit from it, generate an expanded version that inlines the actual content of key pages. This is useful for smaller projects where the full documentation fits in a single context window.

### Step 6: User Review

Present the generated llms.txt for review. Flag any decisions made during curation:

- Content that was excluded and why
- Descriptions that were inferred vs extracted from existing metadata
- Sections where additional documentation would improve AI discoverability

### Step 7: Write to Repo Root

Save `llms.txt` (and optionally `llms-full.txt`) to the repository root.

For projects with hosted documentation sites, also note the recommended placement for the hosted version (site root, e.g., `https://docs.example.com/llms.txt`).

## Hosted Docs and GitHub Pages

If the project has a documentation site (GitHub Pages, ReadTheDocs, Docusaurus, etc.):

- Generate llms.txt with full URLs pointing to the hosted docs, not repo file paths
- Place the file where it will be served at `https://yourdomain.com/llms.txt`
- For GitHub Pages: add llms.txt to the docs source directory so it deploys automatically
- Consider adding llms.txt to your sitemap or linking it from robots.txt

## Key Principles

1. **Curate, don't dump.** An llms.txt that lists every file in the repo is worse than useless. Select the 10-30 most important pages that give an LLM the clearest picture of the project.
2. **Prioritize entry points.** The first few items should answer: what is this, who is it for, and how do I start?
3. **Keep descriptions action-oriented.** "How to configure authentication for SSO providers" beats "Authentication configuration page."
4. **Match the reader's mental model.** Organize sections the way a newcomer would learn the project, not the way the repo is structured.
5. **Maintain freshness.** Stale llms.txt with broken links or outdated descriptions erodes trust. Run `/llms-txt audit` after major documentation changes.

## Integration with Other Skills

- **aeo-geo-optimizer** — llms.txt complements broader AI search optimization; use both for maximum AI discoverability
- **technical-seo-audit** — Ensure AI crawlers can access your docs before generating llms.txt
- **github-readme** — A strong README is the foundation of a good llms.txt; optimize it first

For the full specification format, priority ranking criteria, and placement guidance, see [REFERENCE.md](REFERENCE.md).

---

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
