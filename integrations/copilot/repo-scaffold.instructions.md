Initialize GitHub repositories with standard files and configuration. Generates LICENSE, CONTRIBUTING.md, SECURITY.md, issue/PR templates, CI config, and .gitignore. Detects project type and adapts templates accordingly.


# Repo Scaffold

Initialize GitHub repositories with standard files and configuration. This skill generates LICENSE, CONTRIBUTING.md, SECURITY.md, CODEOWNERS, .gitignore, .editorconfig, YAML-based issue templates, PR template, CI config skeleton, and optional safety files. It detects project type from existing files and adapts all templates accordingly.

## When to Use

This skill should be used when:
- Setting up a new GitHub repository from scratch
- Adding missing standard files to an existing repository
- Standardizing repository configuration across projects
- Preparing a private repo for open-source release

## Usage

```
/repo-scaffold [repo-path] [--license MIT|Apache-2.0|ISC] [--public] [--ci github-actions|none]
```

| Flag | Default | Description |
|------|---------|-------------|
| `repo-path` | `.` (cwd) | Path to the git repository root |
| `--license` | `MIT` | License type (MIT, Apache-2.0, ISC, GPL-3.0, BSD-2-Clause) |
| `--public` | off | Include `.public-repo`, `.pii-allowlist`, `.commit-msg-blocklist` |
| `--ci` | `github-actions` | CI provider skeleton (`github-actions` or `none`) |

## Procedure

### Step 1: Validate Repo Path

Confirm the target path is an initialized git repository (contains `.git/`). If not, halt and inform the user. Never run `git init` without explicit permission.

### Step 2: Scan Existing Files

Inventory the repo root and `.github/` directory for any files this skill would generate. Build a conflict list. **Never overwrite existing files.** If conflicts exist, present them and ask which to skip or replace.

### Step 3: Detect Project Type

Identify the primary language and tooling by checking for marker files:

| Marker File | Project Type |
|-------------|-------------|
| `package.json` | Node.js / JavaScript / TypeScript |
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| Multiple markers | Multi-language |
| None of the above | Generic |

If multiple markers are found, treat as multi-language and combine relevant patterns.

### Step 4: Generate Files

Generate each file with language-appropriate content. Refer to [REFERENCE.md](REFERENCE.md) for templates, patterns, and format specifications.

#### 4a. LICENSE

Prompt the user for license choice if `--license` was not provided. Default to MIT. Insert the current year and the repo owner's name (from `git config user.name` or ask). See REFERENCE.md license comparison table for guidance.

#### 4b. .gitignore

Generate language-appropriate ignore patterns based on the detected project type. Combine patterns for multi-language repos. Always include OS-level ignores (`.DS_Store`, `Thumbs.db`) and editor ignores (`.vscode/`, `.idea/`).

#### 4c. CONTRIBUTING.md

Generate a fork-branch-PR contribution guide. Include:
- Fork and clone instructions
- Branch naming conventions (`feat/`, `fix/`, `docs/`)
- Code style notes (link to linter config if detected)
- Commit message format
- PR checklist

#### 4d. SECURITY.md

Generate a security policy with:
- Supported versions table (populate from package version if detectable)
- Vulnerability reporting instructions (email-based, not public issues)
- Response timeline expectations

#### 4e. CODEOWNERS


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
