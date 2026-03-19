Generate and maintain llms.txt files for AI discoverability. Scans repos to create curated content maps that help AI answer engines surface your project accurately. Implements the llms.txt specification from Answer.AI.


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


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
