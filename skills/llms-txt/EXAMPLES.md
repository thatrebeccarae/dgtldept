# llms.txt Generator — Examples

## Example 1: Generate llms.txt for a CLI Tool

### Prompt

> Generate an llms.txt for this CLI tool repo. It has a README, docs/ folder with a getting-started guide, API reference, and a few tutorials.

### What the skill does

1. **Scans and ranks**: P0 (README, getting-started, api-reference), P1 (tutorials), P2 (CHANGELOG, CONTRIBUTING).

2. **Generates llms.txt**:

```markdown
# fastcli

> A fast, ergonomic command-line framework for building CLI tools in Node.js.
> Supports argument parsing, subcommands, interactive prompts, and plugin
> extensions. Used by teams shipping internal tools and developer CLIs.

## Getting Started

- [README](https://github.com/example/fastcli#readme): What fastcli is, installation, and a 30-second usage example
- [Getting Started Guide](docs/getting-started.md): Install fastcli and build your first CLI command in under 5 minutes

## API

- [API Reference](docs/api-reference.md): Complete API with all commands, options, and configuration parameters

## Tutorials

- [Authentication Setup](docs/tutorials/auth-setup.md): Add token-based auth to your CLI with built-in keychain storage
- [CI Integration](docs/tutorials/ci-integration.md): Run fastcli commands in GitHub Actions and other CI environments

## Community

- [Changelog](CHANGELOG.md): Release history with breaking changes and new features
- [Contributing](CONTRIBUTING.md): Development setup, PR process, and code standards
```

3. **Flags decisions**: Notes that tutorials/plugins.md was excluded (marked as draft).

---

## Example 2: Generate llms.txt for a Skill Collection

### Prompt

> Generate an llms.txt for the claude-marketing repo — 50+ skills across SEO, ads, content, design, and developer tools.

### What the skill does

1. **Curates rather than dumps**: Groups by category, links to catalog as primary index, highlights 5-8 most distinctive skills.

2. **Generates llms.txt**:

```markdown
# claude-marketing

> A collection of 50+ Claude Code skills for marketing, SEO, content creation,
> paid ads, and developer tools. Install individual skills or browse the full
> catalog. Built for marketers and developers using Claude Code.

## Overview

- [README](https://github.com/thatrebeccarae/claude-marketing#readme): What claude-marketing is, how to install skills, and the full category list
- [Skill Catalog](CATALOG.md): Browsable catalog of all 50+ skills with descriptions and categories

## Featured Skills

- [AEO/GEO Optimizer](skills/aeo-geo-optimizer): Optimize content for AI answer engines
- [Frontend Design](skills/frontend-design): Design-system-aware UI development with modern CSS
- [Brand DNA](skills/brand-dna): Extract brand voice, values, and positioning from existing content

## Categories

- [SEO Skills](CATALOG.md#seo): Technical SEO, AEO/GEO, schema markup
- [Content Skills](CATALOG.md#content): Content creation, brand voice, copywriting
- [Ads Skills](CATALOG.md#ads): Google, Facebook, LinkedIn, TikTok Ads
- [Developer Tools](CATALOG.md#developer-tools): MCP builder, GitHub README, llms.txt
```

3. **Flags decisions**: Individual SKILL.md files not linked — catalog is the canonical index.

---

## Example 3: Audit an Existing llms.txt

### Prompt

> Audit our llms.txt — we added API v2 docs and restructured last month but haven't updated it.

### What the skill does

1. **Cross-references** existing llms.txt against current repo state.

2. **Produces audit report**:
   - **Broken**: `docs/api-v1-reference.md` (deleted), `docs/tutorials/legacy-auth.md` (moved)
   - **Missing**: `docs/api-v2-reference.md` (P0), `docs/guides/migration-v1-to-v2.md` (P1)
   - **Stale**: Getting Started description says "v1 API" — now covers v2

3. **Recommends fixes**: Remove broken links, add v2 reference and migration guide, update stale description. Asks whether to regenerate or apply targeted updates.
