Generate, audit, or update GitHub READMEs with project-type-aware structure, voice calibration, and SEO/AEO discoverability guidance. Three modes: generate (new), audit (check existing), update (patch). Detects repo type and adapts sections, tone, and badges accordingly.


# GitHub README Generator

Generate, audit, or update repository READMEs with project-type detection, voice calibration, discoverability guidance, and scored quality audits.

## When to Use

- Starting a new public repo and need a solid README from scratch
- Auditing an existing README for quality, discoverability, and security issues
- Updating a README after the repo has evolved (new deps, features, structure)
- Preparing a repo for public release and want discoverability optimized

## Modes

```
/github:readme generate [repo-path]   # Scan repo, detect type, generate README
/github:readme audit [repo-path]      # Score existing README (read-only, 0-100)
/github:readme update [repo-path]     # Re-scan, silent audit, patch with approval
```

Default `repo-path` is the current working directory if omitted.


## Step 0: Parse and Validate

Expect: `/github:readme {mode} [repo-path]`

1. **Extract mode** — `generate`, `audit`, or `update`. Any other value or missing → error with usage hint. STOP.
2. **Extract repo-path** — second argument, or current working directory if omitted.
3. **Validate** — confirm path exists, is a directory, and contains `.git`. If not → error. STOP.

Store `repo_path` (absolute) and `mode`.


## Step 1: Scan the Repo

Gather context by reading available files. Skip gracefully if a file does not exist.

**Package/config files** (tech stack detection):
- `package.json` — Node/TypeScript/React
- `Cargo.toml` — Rust
- `pyproject.toml`, `setup.py`, `requirements.txt` — Python
- `go.mod` — Go
- `tsconfig.json` — TypeScript confirmation
- `Dockerfile`, `docker-compose.yml` — containerization
- `Makefile`, `justfile` — build system
- `.github/workflows/` — CI/CD

**Directory structure:**
- Run `ls` at repo root for top-level layout
- Note: `src/`, `bin/`, `lib/`, `scripts/`, `docs/`, `tests/`, `skills/`, `templates/`, `plugins/`, `.github/`

**Existing docs:**
- `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`, `ARCHITECTURE.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `llms.txt`

**Git remote:**
- Run `git -C {repo_path} remote get-url origin`
- Extract `{owner}` and `{repo}` from the URL
- Determine public/private: `.public-repo` marker → public; `-dev` suffix or no marker → ask user


## Step 2: Detect Project Type

Classify the repo into exactly one type based on scan signals:

| Type | Signals |
|------|---------|
| **tool/CLI** | Has `bin` field in package.json, CLI entry points, man pages, command parsers (yargs, clap, cobra) |
| **library/SDK** | Has `main`/`exports`/`module` field, published to npm/PyPI/crates.io, no CLI entry |
| **collection/marketplace** | Contains multiple independent items: `skills/`, `templates/`, `plugins/`, `recipes/` directories with 3+ subdirectories |
| **web-app** | Has React/Vue/Svelte/Next/Nuxt, server framework (Express, FastAPI, Actix), deployment config (Vercel, Dockerfile) |
| **personal/experimental** | Small repo (<20 files), no package publishing config, no CI, no semver tags |

If ambiguous, ask the user to confirm. Store as `project_type`.


## Step 3: Discoverability Audit


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
