# repo-scaffold


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

Scan the top-level directory structure and generate a CODEOWNERS file. Map directories to the repo owner by default. Add comments explaining how to customize.

#### 4f. .editorconfig

Generate settings appropriate to the detected project type:
- Indent style and size
- End-of-line character
- Trim trailing whitespace
- Insert final newline
- Charset (utf-8)

#### 4g. .github/ISSUE_TEMPLATE/bug-report.yml

Generate a YAML form-based bug report template with fields: description, steps to reproduce, expected behavior, actual behavior, environment, and optional screenshots. See REFERENCE.md for YAML form spec.

#### 4h. .github/ISSUE_TEMPLATE/feature-request.yml

Generate a YAML form-based feature request template with fields: problem statement, proposed solution, alternatives considered, and additional context.

#### 4i. .github/pull_request_template.md

Generate a PR template with sections: summary of changes, type of change (checkboxes), testing performed, and checklist.

#### 4j. .github/workflows/ci.yml

Generate a CI skeleton for GitHub Actions (unless `--ci none`). Include:
- Trigger on push to main and pull requests
- Language-appropriate setup step
- Lint step (ESLint, ruff, clippy, golangci-lint)
- Test step (language-appropriate test runner)
- Placeholder comments for additional steps

#### 4k. Optional: Safety Files (when --public)

When `--public` is passed, also generate:
- `.public-repo` — Empty marker file indicating the repo is public
- `.pii-allowlist` — One regex per line; starts with a comment header explaining usage
- `.commit-msg-blocklist` — One term per line; starts with a comment header and common defaults

### Step 5: Present Plan

Before writing any files, present the full list of files to be created with a one-line description of each. Show which files were skipped due to conflicts. Ask the user to confirm before proceeding.

### Step 6: Write Files

Write all confirmed files. Report each file as it is written.

### Step 7: Summary

Print a summary table:
- Files created (with paths)
- Files skipped (with reason)
- Suggested next steps (e.g., review CODEOWNERS, customize CONTRIBUTING.md, add secrets to CI)

## Key Principles

1. **Never overwrite existing files.** Always scan first, flag conflicts, and ask.
2. **Always ask before writing.** Present the plan and get explicit confirmation.
3. **Language-appropriate defaults.** Detect the project type and tailor every template.
4. **Minimal but complete.** Generate the standard set every well-maintained repo needs, nothing more.
5. **Composable.** Each file stands alone. Re-run the skill later to add missing files without disrupting existing ones.

## References

- [REFERENCE.md](REFERENCE.md) — License comparison, .gitignore patterns, YAML template spec, CI skeletons, CODEOWNERS syntax, .editorconfig settings, SECURITY.md and CONTRIBUTING.md templates
- [EXAMPLES.md](EXAMPLES.md) — Worked examples for Node.js, Python, and public repo scaffolding

---

# Repo Scaffold Reference

Detailed templates, patterns, and specifications used by the repo-scaffold skill.

## License Comparison

| License | Permissions | Conditions | Limitations |
|---------|------------|------------|-------------|
| **MIT** | Commercial use, modification, distribution, private use | License and copyright notice | No liability, no warranty |
| **Apache-2.0** | Commercial use, modification, distribution, patent use, private use | License and copyright notice, state changes, include NOTICE file | No liability, no warranty, no trademark use |
| **ISC** | Commercial use, modification, distribution, private use | License and copyright notice | No liability, no warranty |
| **GPL-3.0** | Commercial use, modification, distribution, patent use, private use | Disclose source, license and copyright notice, same license, state changes | No liability, no warranty |
| **BSD-2-Clause** | Commercial use, modification, distribution, private use | License and copyright notice | No liability, no warranty |

### When to Choose

- **MIT** — Maximum permissiveness, widest adoption. Good default.
- **Apache-2.0** — Like MIT but with explicit patent grant. Preferred for enterprise/corporate projects.
- **ISC** — Functionally identical to MIT with simpler language. Common in Node.js ecosystem.
- **GPL-3.0** — Copyleft. Derivatives must also be GPL. Use when openness is non-negotiable.
- **BSD-2-Clause** — Similar to MIT. Common in BSD/C ecosystems.

### MIT License Template

```text
MIT License

Copyright (c) {year} {fullname}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## .gitignore Patterns by Language

### Common (always include)

```gitignore
# OS
.DS_Store
Thumbs.db
Desktop.ini

# Editors
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local
.env.*.local
```

### Node.js

```gitignore
node_modules/
dist/
build/
coverage/
.next/
.nuxt/
*.tsbuildinfo
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.yarn/cache
.yarn/unplugged
.pnp.*
```

### Python

```gitignore
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.eggs/
*.egg
.venv/
venv/
env/
.pytest_cache/
.mypy_cache/
.ruff_cache/
htmlcov/
.coverage
.coverage.*
```

### Rust

```gitignore
/target/
**/*.rs.bk
Cargo.lock
```

Note: Include `Cargo.lock` in .gitignore for libraries, but commit it for binaries/applications.

### Go

```gitignore
/bin/
/vendor/
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
go.work
```

## YAML Issue Template Format

GitHub YAML form-based issue templates use the following structure:

```yaml
name: "Template Name"
description: "One-line description shown in the template picker"
title: "[PREFIX]: "
labels: ["label1", "label2"]
assignees:
  - username
body:
  - type: markdown
    attributes:
      value: |
        Markdown content shown as static text.

  - type: input
    id: field-id
    attributes:
      label: "Field Label"
      description: "Help text"
      placeholder: "Placeholder text"
    validations:
      required: true

  - type: textarea
    id: field-id
    attributes:
      label: "Field Label"
      description: "Help text"
      placeholder: "Placeholder text"
      render: shell
    validations:
      required: false

  - type: dropdown
    id: field-id
    attributes:
      label: "Field Label"
      description: "Help text"
      options:
        - "Option 1"
        - "Option 2"
    validations:
      required: true

  - type: checkboxes
    id: field-id
    attributes:
      label: "Field Label"
      options:
        - label: "Checkbox option"
          required: true
```

### Available Field Types

| Type | Description | Key Attributes |
|------|-------------|---------------|
| `markdown` | Static text (not submitted) | `value` |
| `input` | Single-line text | `label`, `description`, `placeholder` |
| `textarea` | Multi-line text | `label`, `description`, `placeholder`, `render` |
| `dropdown` | Select menu | `label`, `options`, `multiple` (v2) |
| `checkboxes` | Checkbox list | `label`, `options[].label`, `options[].required` |

### Bug Report Template

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
title: "[Bug]: "
labels: ["bug", "triage"]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear description of the bug.
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Minimal steps to reproduce the behavior.
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should have happened?
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened?
    validations:
      required: true

  - type: input
    id: environment
    attributes:
      label: Environment
      description: "OS, runtime version, browser, etc."
      placeholder: "macOS 15, Node 22, Chrome 130"
    validations:
      required: false

  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots / Logs
      description: If applicable, add screenshots or log output.
      render: shell
    validations:
      required: false
```

### Feature Request Template

```yaml
name: Feature Request
description: Suggest a new feature or improvement
title: "[Feature]: "
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: What problem does this feature solve?
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: Describe the solution you would like.
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Other approaches you have considered.
    validations:
      required: false

  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Any other context, mockups, or references.
    validations:
      required: false
```

## GitHub Actions CI Skeletons

### Node.js

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm test
```

### Python

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: pytest
```

### Rust

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt
      - run: cargo fmt --check
      - run: cargo clippy -- -D warnings
      - run: cargo test
```

### Go

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
      - uses: golangci/golangci-lint-action@v6
      - run: go test ./...
```

## CODEOWNERS Syntax

```text
# Default owner for everything
* @owner

# Directory-specific owners
/src/ @owner
/docs/ @owner
/tests/ @owner
/.github/ @owner

# File-type owners
*.js @owner
*.py @owner
```

Rules:
- Later rules take precedence over earlier rules
- Paths are relative to the repo root
- Use `@username`, `@org/team-name`, or `email@example.com`
- One owner entry per line
- Lines starting with `#` are comments

## .editorconfig Settings

### Node.js / JavaScript / TypeScript

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.{yml,yaml}]
indent_size = 2
```

### Python

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.{yml,yaml}]
indent_size = 2

[Makefile]
indent_style = tab
```

### Rust

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.toml]
indent_size = 2
```

### Go

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = tab
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.{yml,yaml}]
indent_size = 2
```

## SECURITY.md Template

```markdown
# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest  | Yes       |

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

To report a vulnerability, email **security@example.com** with:

1. Description of the vulnerability
2. Steps to reproduce
3. Impact assessment
4. Any suggested fixes (optional)

### What to Expect

- **Acknowledgment** within 48 hours
- **Initial assessment** within 5 business days
- **Resolution timeline** communicated after assessment
- **Credit** in the release notes (unless you prefer anonymity)

We follow responsible disclosure. Please allow us reasonable time to address the issue before any public disclosure.
```

## CONTRIBUTING.md Template

```markdown
# Contributing

Thank you for your interest in contributing. This guide covers the process for submitting changes.

## Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create a branch** from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
4. **Make your changes** and commit
5. **Push** to your fork and open a **Pull Request**

## Branch Naming

| Prefix | Purpose |
|--------|---------|
| `feat/` | New feature |
| `fix/` | Bug fix |
| `docs/` | Documentation only |
| `refactor/` | Code change that neither fixes a bug nor adds a feature |
| `test/` | Adding or updating tests |
| `chore/` | Maintenance (deps, CI, tooling) |

## Commit Messages

Write clear, concise commit messages. Use the imperative mood:
- "Add search endpoint" (not "Added" or "Adds")
- "Fix null pointer on empty input"
- "Update README with install instructions"

## Code Style

Follow the existing code style. The project uses automated linting — run the linter locally before submitting:

```bash
# Check the project's package.json, Makefile, or Cargo.toml for the lint command
```

## Pull Request Checklist

- [ ] Branch is up to date with `main`
- [ ] Code passes linting and tests
- [ ] New code has tests where appropriate
- [ ] Documentation updated if behavior changed
- [ ] PR description explains the "why" not just the "what"

## Code of Conduct

Be respectful. Harassment, discrimination, and bad-faith behavior will not be tolerated.
```

## PR Template

```markdown
## Summary

<!-- What does this PR do and why? -->

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Refactor
- [ ] Chore (deps, CI, tooling)

## Testing

<!-- How was this tested? -->

## Checklist

- [ ] Tests pass locally
- [ ] Linting passes
- [ ] Documentation updated (if applicable)
- [ ] No breaking changes (or clearly documented)
```

## Safety Files

### .public-repo

Empty file. Its presence marks the repository as public for tooling that distinguishes between public and private repos.

### .pii-allowlist

```text
# PII Allowlist
# One regex per line. Matches are exempt from the PII pre-commit scan.
# Example: ^docs/examples/.*\.md$
```

### .commit-msg-blocklist

```text
# Commit Message Blocklist
# One term per line. These terms must never appear in commit messages.
# Case-insensitive matching.
# Add internal project names, client names, or sensitive terms below.
```
