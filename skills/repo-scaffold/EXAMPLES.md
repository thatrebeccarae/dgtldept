# Repo Scaffold Examples

Practical examples of scaffolding repositories with different configurations.

## Example 1: New Node.js Project

**User Request**: "Scaffold my new Node.js project at ~/projects/my-api"

**Detected**: `package.json` found — Node.js project

**Plan Presented**:
```
Files to create:
  LICENSE ..................... MIT license (2026, Rebecca Rae Barton)
  .gitignore ................. Node.js + OS + editor patterns
  .editorconfig .............. 2-space indent, LF, UTF-8
  CONTRIBUTING.md ............ Fork/branch/PR guide
  SECURITY.md ................ Vulnerability reporting policy
  CODEOWNERS ................. Default owner: @thatrebeccarae
  .github/ISSUE_TEMPLATE/bug-report.yml ....... YAML form
  .github/ISSUE_TEMPLATE/feature-request.yml .. YAML form
  .github/pull_request_template.md ............ PR checklist
  .github/workflows/ci.yml .................... Node 20+22, lint + test

No conflicts found. Proceed? (y/n)
```

**Result**: 10 files created. The CI workflow includes `npm ci`, `npm run lint`, and `npm test` across Node 20 and 22. The .gitignore covers `node_modules/`, `dist/`, `.next/`, coverage output, and environment files.

**Suggested Next Steps**:
- Review CODEOWNERS and add team members
- Update SECURITY.md with your actual security contact email
- Add repository secrets for CI if needed
- Customize CONTRIBUTING.md code style section with your ESLint config

---

## Example 2: Existing Python Repo Missing Standard Files

**User Request**: "My Python repo at ~/projects/data-pipeline is missing standard files. Add what's missing."

**Detected**: `pyproject.toml` found — Python project

**Scan Results**:
```
Existing files (will skip):
  .gitignore ................. already exists
  LICENSE .................... already exists

Files to create:
  .editorconfig .............. 4-space indent, LF, UTF-8
  CONTRIBUTING.md ............ Fork/branch/PR guide
  SECURITY.md ................ Vulnerability reporting policy
  CODEOWNERS ................. Default owner from git config
  .github/ISSUE_TEMPLATE/bug-report.yml ....... YAML form
  .github/ISSUE_TEMPLATE/feature-request.yml .. YAML form
  .github/pull_request_template.md ............ PR checklist
  .github/workflows/ci.yml .................... Python 3.11-3.13, ruff + pytest

Skipped 2 files (already exist). Proceed with 8 new files? (y/n)
```

**Result**: 8 files created. The existing .gitignore and LICENSE are untouched. The CI workflow uses `ruff check .` for linting and `pytest` for testing across Python 3.11, 3.12, and 3.13. The .editorconfig uses 4-space indentation with a Makefile override for tabs.

**Suggested Next Steps**:
- Verify `pip install -e ".[dev]"` works with your pyproject.toml dev dependencies
- Add ruff and pytest to your dev dependencies if not already present
- Review the generated SECURITY.md supported versions table

---

## Example 3: Public Repo with Safety Files

**User Request**: "/repo-scaffold ~/projects/open-tool --license Apache-2.0 --public"

**Detected**: `package.json` + `Cargo.toml` found — Multi-language project (Node.js + Rust)

**Plan Presented**:
```
Files to create:
  LICENSE ..................... Apache 2.0 (2026, Rebecca Rae Barton)
  .gitignore ................. Node.js + Rust + OS + editor patterns
  .editorconfig .............. 2-space (JS/TS), 4-space (Rust), LF, UTF-8
  CONTRIBUTING.md ............ Fork/branch/PR guide
  SECURITY.md ................ Vulnerability reporting policy
  CODEOWNERS ................. Default owner: @thatrebeccarae
  .github/ISSUE_TEMPLATE/bug-report.yml ....... YAML form
  .github/ISSUE_TEMPLATE/feature-request.yml .. YAML form
  .github/pull_request_template.md ............ PR checklist
  .github/workflows/ci.yml .................... Node 22 + Rust stable, lint + test
  .public-repo ............... Public repo marker (empty)
  .pii-allowlist ............. PII scan exemption patterns
  .commit-msg-blocklist ...... Blocked terms for commit messages

No conflicts found. Proceed? (y/n)
```

**Result**: 13 files created. The .gitignore merges Node.js and Rust patterns. The CI workflow has two jobs: one for Node (npm ci, lint, test) and one for Rust (cargo fmt, clippy, test). The three safety files are in place for pre-commit hook integration.

**Suggested Next Steps**:
- Add sensitive terms to `.commit-msg-blocklist` (client names, internal codenames)
- Add path exemptions to `.pii-allowlist` if docs contain example emails or IPs
- Verify the `.public-repo` marker is detected by your pre-commit hooks
- Review the Apache 2.0 LICENSE and add a NOTICE file if required by dependencies
- Audit all existing commit messages before first public push
