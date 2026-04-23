# GitHub README — Reference

Technical data, templates, and patterns for the github-readme skill.

---

## Badge URL Patterns

All badges use shields.io. Default style is `style=for-the-badge`. Append `&style=flat` for inline/compact use.

### Repository Badges

```markdown
<!-- GitHub stars -->
[![Stars](https://img.shields.io/github/stars/{owner}/{repo}?style=for-the-badge&logo=github&color=121011)](https://github.com/{owner}/{repo}/stargazers)

<!-- License (auto-detect from repo) -->
[![License](https://img.shields.io/github/license/{owner}/{repo}?style=for-the-badge&labelColor=353535)](LICENSE)

<!-- License (hardcoded MIT) -->
[![License](https://img.shields.io/badge/License-MIT-555?style=for-the-badge&labelColor=353535)](LICENSE)

<!-- Build status (GitHub Actions) -->
[![Build](https://img.shields.io/github/actions/workflow/status/{owner}/{repo}/{workflow}.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/{owner}/{repo}/actions)

<!-- Last commit -->
[![Last Commit](https://img.shields.io/github/last-commit/{owner}/{repo}?style=for-the-badge)](https://github.com/{owner}/{repo}/commits)

<!-- npm version -->
[![npm](https://img.shields.io/npm/v/{package}?style=for-the-badge&logo=npm&logoColor=white)](https://npmjs.com/package/{package})

<!-- PyPI version -->
[![PyPI](https://img.shields.io/pypi/v/{package}?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/{package})

<!-- crates.io version -->
[![Crates.io](https://img.shields.io/crates/v/{crate}?style=for-the-badge&logo=rust&logoColor=white)](https://crates.io/crates/{crate})

<!-- Docker pulls -->
[![Docker](https://img.shields.io/docker/pulls/{owner}/{image}?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/{owner}/{image})

<!-- Coverage (Codecov) -->
[![Coverage](https://img.shields.io/codecov/c/github/{owner}/{repo}?style=for-the-badge&logo=codecov&logoColor=white)](https://codecov.io/gh/{owner}/{repo})

<!-- npm downloads -->
[![Downloads](https://img.shields.io/npm/dm/{package}?style=for-the-badge)](https://npmjs.com/package/{package})
```

### Tech Stack Badges

Pattern: brand color on LEFT (`labelColor`), gray `#555` on RIGHT.

```markdown
<!-- TypeScript -->
[![TypeScript](https://img.shields.io/badge/TypeScript-ESM-555?style=for-the-badge&labelColor=007ACC&logo=typescript&logoColor=white)](#)

<!-- Node.js -->
[![Node](https://img.shields.io/badge/Node-%3E%3D22-555?style=for-the-badge&labelColor=6DA55F&logo=node.js&logoColor=white)](#)

<!-- Python -->
[![Python](https://img.shields.io/badge/Python-3.11+-555?style=for-the-badge&labelColor=3670A0&logo=python&logoColor=ffdd54)](https://python.org)

<!-- Rust -->
[![Rust](https://img.shields.io/badge/Rust-2021-555?style=for-the-badge&labelColor=000000&logo=rust&logoColor=white)](https://rust-lang.org)

<!-- Go -->
[![Go](https://img.shields.io/badge/Go-1.22+-555?style=for-the-badge&labelColor=00ADD8&logo=go&logoColor=white)](https://go.dev)

<!-- React -->
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&labelColor=20232a&logo=react&logoColor=61DAFB)](https://react.dev)

<!-- Vue -->
[![Vue](https://img.shields.io/badge/Vue-3.x-555?style=for-the-badge&labelColor=4FC08D&logo=vue.js&logoColor=white)](https://vuejs.org)

<!-- Next.js -->
[![Next.js](https://img.shields.io/badge/Next.js-15-555?style=for-the-badge&labelColor=000000&logo=next.js&logoColor=white)](https://nextjs.org)

<!-- Docker -->
[![Docker](https://img.shields.io/badge/Docker-Compose-555?style=for-the-badge&labelColor=2496ED&logo=docker&logoColor=white)](https://docker.com)

<!-- Tauri -->
[![Tauri](https://img.shields.io/badge/Tauri-v2-555?style=for-the-badge&labelColor=24C8DB&logo=tauri&logoColor=white)](https://v2.tauri.app)

<!-- Claude Code -->
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skills-555?style=for-the-badge&labelColor=D97757&logo=claude&logoColor=white)](https://docs.anthropic.com/en/docs/claude-code)

<!-- Tailwind CSS -->
[![Tailwind](https://img.shields.io/badge/Tailwind-v4-555?style=for-the-badge&labelColor=06B6D4&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)

<!-- Prisma -->
[![Prisma](https://img.shields.io/badge/Prisma-ORM-555?style=for-the-badge&labelColor=2D3748&logo=prisma&logoColor=white)](https://prisma.io)

<!-- PostgreSQL -->
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-555?style=for-the-badge&labelColor=4169E1&logo=postgresql&logoColor=white)](https://postgresql.org)

<!-- SQLite -->
[![SQLite](https://img.shields.io/badge/SQLite-WAL-555?style=for-the-badge&labelColor=003B57&logo=sqlite&logoColor=white)](https://sqlite.org)

<!-- n8n -->
[![n8n](https://img.shields.io/badge/n8n-Workflows-555?style=for-the-badge&labelColor=EA4B71&logo=n8n&logoColor=white)](https://n8n.io)

<!-- Framer -->
[![Framer](https://img.shields.io/badge/Framer-Components-555?style=for-the-badge&labelColor=000000&logo=framer&logoColor=0055FF)](https://framer.com)
```

### Social Badges (flagship repos only)

```markdown
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Rebecca%20Rae%20Barton-555?style=for-the-badge&labelColor=0077B5&logo=linkedin&logoColor=white)](https://linkedin.com/in/rebeccaraebarton)
[![X](https://img.shields.io/badge/X-@rebeccarae-555?style=for-the-badge&labelColor=000000&logo=x&logoColor=white)](https://x.com/rebeccarae)
```

### Clone Badge

```markdown
[![Clone](https://img.shields.io/badge/Clone-git%20clone-555?style=for-the-badge&labelColor=F05033&logo=git&logoColor=white)](https://github.com/{owner}/{repo})
```

---

## Section Templates

### Title Block (Hero)

```markdown
<div align="center">

# Project Name

**One-line description under 120 characters stating what this does.**

[![Badge](url)](#) [![Badge](url)](#) [![Stars](url)](#) [![License](url)](#)

<br>

```bash
git clone https://github.com/{owner}/{repo}.git
```

<br>

<!-- Screenshot or demo (width="760") -->

<br><br>

[Why I Built This](#why-i-built-this) · [Getting Started](#getting-started) · [Features](#features) · [License](#license)

</div>

---
```

### Features List

```markdown
## Features

**Category One**
- **Feature name** — What it does and why it matters
- **Feature name** — What it does and why it matters

**Category Two**
- **Feature name** — What it does and why it matters
```

### Installation

```markdown
## Getting Started

### Prerequisites

- Node.js >= 22
- npm >= 10

### Install

```bash
# npm
npm install {package}

# yarn
yarn add {package}

# pnpm
pnpm add {package}
```

```bash
# pip
pip install {package}

# uv
uv add {package}
```

```bash
# cargo
cargo install {crate}
```

```bash
# go
go install github.com/{owner}/{repo}@latest
```

```bash
# git clone
git clone https://github.com/{owner}/{repo}.git
cd {repo}
npm install
```
```

### Quick Start

```markdown
## Quick Start

```typescript
import { Client } from "{package}";

const client = new Client({ apiKey: process.env.API_KEY });
const result = await client.doSomething({ input: "value" });
console.log(result);
```
```

### CLI Commands Table

```markdown
## Commands

| Command | Description |
|---------|-------------|
| `tool init [name]` | Initialize a new project |
| `tool build` | Build for production |
| `tool dev` | Start dev server with hot reload |
| `tool test` | Run test suite |
| `tool lint` | Lint and format |

### `tool init`

```bash
tool init [project-name] [--template <name>] [--no-git]
```

**Options:**
| Flag | Default | Description |
|------|---------|-------------|
| `--template` | `basic` | Starter template |
| `--no-git` | `false` | Skip git initialization |
```

### API Reference (Expandable)

```markdown
## API Reference

<details>
<summary><code>GET /v1/resources</code> — List all resources</summary>

**Parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | integer | No | Max results (default: 20) |
| `offset` | integer | No | Pagination offset |

**Response:**

```json
{
  "data": [],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

</details>

<details>
<summary><code>POST /v1/resources</code> — Create a resource</summary>

**Body:**

```json
{
  "name": "string (required)",
  "type": "string"
}
```

**Response:** `201 Created`

</details>
```

### Environment Variables Table

```markdown
## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_KEY` | Yes | -- | API key from dashboard |
| `PORT` | No | `3000` | Server port |
| `LOG_LEVEL` | No | `info` | `debug`, `info`, `warn`, `error` |
| `DATABASE_URL` | Yes | -- | PostgreSQL connection string |

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```
```

### Architecture Overview

```markdown
## Architecture

```
repo/
├── src/
│   ├── core/          # Core business logic
│   ├── api/           # API routes and handlers
│   ├── lib/           # Shared utilities
│   └── index.ts       # Entry point
├── config/            # Configuration files
├── scripts/           # Build and deploy scripts
└── tests/             # Test suites
```

Brief explanation of data flow or key design decisions (2-3 sentences).
```

### Contributing

```markdown
## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/thing`)
3. Commit changes (`git commit -m 'Add thing'`)
4. Push (`git push origin feature/thing`)
5. Open a Pull Request
```

### License

```markdown
## License

MIT -- see [LICENSE](LICENSE) for details.
```

---

## Project Type Detection Signals

| Signal | Detected Type |
|--------|---------------|
| `bin` field in package.json | CLI tool |
| `exports` or `main` in package.json (no `bin`) | Library/SDK |
| `skills/` dir with SKILL.md files | Skill pack / collection |
| `templates/` dir with multiple template files | Collection / marketplace |
| `next.config.*` or `nuxt.config.*` | Web app (SSR) |
| `vite.config.*` or `webpack.config.*` | Web app (SPA) |
| `app/` or `pages/` dir + framework config | Web app |
| `routes/` or `openapi.yaml`/`swagger.json` | API service |
| `packages/` dir or `workspaces` in package.json | Monorepo |
| `Dockerfile` + `docker-compose.yml` (no app src) | Infrastructure / ops |
| `src-tauri/` or `tauri.conf.json` | Desktop app (Tauri) |
| `pyproject.toml` with `[project.scripts]` | Python CLI |
| `pyproject.toml` with `[project]` (no scripts) | Python library |
| `Cargo.toml` with `[[bin]]` | Rust CLI |
| `Cargo.toml` with `[lib]` | Rust library |
| `go.mod` + `main.go` at root | Go CLI |
| `go.mod` + no `main.go` at root | Go library |
| `.github/actions/` or `action.yml` | GitHub Action |
| `serverless.yml` or `sam-template.yaml` | Serverless function |

---

## Audit Scoring Rubric

Total: 100 points. Each category is weighted and scored independently.

| Category | Weight | Score 0 | Score 50 | Score 100 |
|----------|--------|---------|----------|-----------|
| **Description** | 15% | No description or generic placeholder | Description exists but vague or over 120 chars | Clear one-liner, explains what + who, under 120 chars |
| **Installation** | 20% | No install instructions | Install steps exist but missing prerequisites or package name wrong | Working install command, prerequisites with versions, copy-pasteable |
| **Usage/Examples** | 20% | No code examples | Examples exist but incomplete or use placeholder values | Working examples covering primary use case, syntactically valid |
| **Badges** | 10% | No badges | Some badges but broken URLs or inconsistent style | Relevant badges, all resolve, consistent `for-the-badge` style |
| **Structure** | 15% | Missing multiple required sections | Sections present but wrong order or names | All required sections, correct order, template-compliant names |
| **Completeness** | 10% | Placeholder text remaining, TODO markers | Most sections filled but some thin | All sections substantive, no placeholders, no TODO markers |
| **Freshness** | 10% | Stale version numbers, references removed features | Mostly current, minor drift | Version numbers current, all references accurate, badges valid |

**Scoring formula:** `sum(category_score * weight)` rounded to nearest integer.

**Grade thresholds:**
- 90-100: Excellent -- no action needed
- 70-89: Good -- minor improvements recommended
- 50-69: Needs work -- several sections require attention
- Below 50: Poor -- consider running generate mode

---

## Discoverability Reference

### GitHub Search Ranking Factors

Priority order for how GitHub search weights content:

1. **Repository name** — exact and partial matches rank highest
2. **Description** — the `About` field on the repo page
3. **Topics** — tagged topics visible below description
4. **README content** — full-text indexed but lowest weight

### Topic Best Practices

- Use lowercase, hyphenated terms (`cli-tool`, not `CLI Tool`)
- Prefer single-concept topics (`typescript`, `readme-generator`)
- Max 20 topics per repo (GitHub hard limit)
- Include: language, framework, domain, use-case
- Avoid: generic terms (`awesome`, `tool`), version numbers, duplicating the repo name

### Social Preview Image

- Dimensions: **1280 x 640 px** (2:1 ratio)
- Format: PNG or JPG, under 1MB
- Set via repo Settings > Social Preview
- Should include: project name, one-line description, visual identity
- Avoid: small text, busy backgrounds, screenshots at low resolution

### llms.txt Specification

A `llms.txt` file tells LLMs what a project does and how to use it.

- **Location:** repo root (`/llms.txt`)
- **Format:** plain text, structured sections
- **Sections:** Title, Description, Quick Start, API surface, Key concepts
- **Purpose:** LLM-optimized alternative to README -- dense, no marketing, no images
- **Spec:** https://llmstxt.org
- Also generate `llms-full.txt` for comprehensive reference if project is complex

### AEO (Answer Engine Optimization) Patterns

Structure README content so AI assistants and search engines can extract direct answers:

- **Semantic headings:** Use descriptive H2/H3 that match common questions (`## Installation`, `## How It Works`, not `## Section 3`)
- **Direct answers first:** Lead each section with a 1-2 sentence summary before details
- **Cited data points:** Include specific numbers, versions, benchmarks where relevant
- **Definition patterns:** "X is a Y that does Z" in the first paragraph
- **Comparison-friendly:** When relevant, name alternatives and state differentiators
- **Structured data:** Tables and lists over prose for reference material

---

## PII/Infrastructure Scrub Patterns

Regex patterns for detecting common leaks. Run against all generated README text before writing.

### Email Addresses

```regex
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

Allowlist: `noreply@github.com`, `action@github.com`, `example.com` domain.

### IP Addresses (RFC 1918 Private Ranges)

```regex
# 10.x.x.x
10\.\d{1,3}\.\d{1,3}\.\d{1,3}

# 172.16-31.x.x
172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}

# 192.168.x.x
192\.168\.\d{1,3}\.\d{1,3}

# Tailscale (100.x.x.x CGNAT range)
100\.(6[4-9]|[7-9]\d|1[0-2]\d)\.\d{1,3}\.\d{1,3}
```

### API Keys and Tokens

```regex
# AWS access key
AKIA[0-9A-Z]{16}

# AWS secret key (generic 40-char base64)
[A-Za-z0-9/+=]{40}

# GitHub token (classic and fine-grained)
gh[ps]_[A-Za-z0-9_]{36,}
github_pat_[A-Za-z0-9_]{22,}

# Slack token
xox[bpors]-[A-Za-z0-9-]+

# Slack webhook
hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+

# Generic bearer/API key patterns
(sk|pk|api|key|token|secret|password)[_-]?[A-Za-z0-9]{20,}

# OpenAI
sk-[A-Za-z0-9]{48}

# Anthropic
sk-ant-[A-Za-z0-9-]{40,}
```

### Internal Hostnames

```regex
# Specific known hostnames (case-insensitive) — replace with your own
(?i)\b(internal-host-a|internal-host-b)\b

# Generic internal hostname patterns
\b[a-z]+-?(dev|staging|internal|local)\.[a-z]+\.(local|internal|lan)\b
```

### Private Key Material

```regex
-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----
```

### File Paths Containing Usernames

```regex
# macOS home directories
/Users/[a-zA-Z][a-zA-Z0-9._-]+/

# Linux home directories
/home/[a-zA-Z][a-zA-Z0-9._-]+/

# Windows user directories
C:\\Users\\[a-zA-Z][a-zA-Z0-9._-]+\\
```

### Client Names and Internal References

```regex
# Replace with your client names and internal codenames
(?i)\b(client-name-a|client-name-b|project-codename)\b
```

### Device Identifiers

```regex
\b[A-Z]{5,8}\b  # Serial-like patterns (review matches manually)
```

---

## Voice Calibration Matrix

Adapt tone and structure based on detected project type.

| Type | Tone | Lead With | Avoid |
|------|------|-----------|-------|
| **CLI tool** | Direct, efficient | What it does + install command | Backstory, philosophy |
| **Library/SDK** | Technical, precise | Import statement + API surface | Marketing language, superlatives |
| **Collection/marketplace** | Catalog, organized | What's inside + how to browse/install | Personal narrative, long intros |
| **Web app** | Demo-focused, visual | Screenshot + try-it link | Implementation details upfront |
| **API service** | Reference-oriented | Base URL + auth + first request | Narrative prose, lengthy motivation |
| **Personal project** | Conversational, first-person | Why I built this + the problem | Corporate tone, passive voice |
| **GitHub Action** | Integration-focused | Usage YAML snippet | Architecture deep-dives |
| **Monorepo** | Navigational, structured | Package table + what each does | Treating it like a single project |
| **Desktop app** | User-focused | Download link + screenshot | Build-from-source as primary path |
| **Infrastructure** | Ops-oriented | Requirements + deploy command | End-user language |

### Voice Examples by Type

**CLI tool** -- lead sentence:
> `{tool}` finds unused dependencies in your Node.js project and removes them.

**Library** -- lead sentence:
> A TypeScript client for the {service} API with full type safety and automatic retry.

**Collection** -- lead sentence:
> 55 Claude Code skills for content marketing, developer tools, and design workflows.

**Personal project** -- lead sentence:
> I needed a way to track time without leaving the terminal, so I built one.

---
