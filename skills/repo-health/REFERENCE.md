# Repo Health Reference

Technical reference for the repo-health skill. Scoring rubrics, standard file descriptions, API endpoints, and templates.

## Standard Files Checklist

| File | Purpose | Notes |
|------|---------|-------|
| `LICENSE` | Legal terms for use, modification, distribution | MIT is the most common for open source. Required for public repos. GitHub will not display a license badge without this file. |
| `README.md` | First thing visitors see. Project description, setup, usage. | Should be substantive (50+ lines for public repos). See `/github:readme` for deep auditing. |
| `.gitignore` | Prevents tracking of build artifacts, dependencies, secrets | Language-specific. See common entries below. |
| `SECURITY.md` | How to report vulnerabilities | GitHub surfaces this in the Security tab. Critical for public repos accepting contributions. |
| `CONTRIBUTING.md` | Contribution guidelines: how to fork, branch, submit PRs | GitHub links to this from the "New Issue" and "New PR" pages. |
| `CODEOWNERS` | Auto-assigns reviewers to PRs based on file paths | Lives at repo root or `.github/CODEOWNERS`. Requires branch protection to enforce. |
| `.editorconfig` | Consistent formatting across editors (indent style, line endings) | Supported natively by most editors. Prevents whitespace-only diffs. |
| `CODE_OF_CONDUCT.md` | Community behavior expectations | Contributor Covenant v2.1 is the standard. GitHub surfaces this in the community profile. |
| `CHANGELOG.md` | Human-readable list of notable changes per version | Follow [Keep a Changelog](https://keepachangelog.com/) format. |
| `.github/pull_request_template.md` | Default body text when opening a PR | Can include checklists, testing instructions, link to issues. |
| `.github/ISSUE_TEMPLATE/` | Structured issue forms (bug report, feature request) | YAML form-based templates are preferred over freeform markdown. |

## GitHub API Endpoints

These are used via `gh api` to check repo configuration.

### Repo Metadata
```bash
gh repo view --json description,repositoryTopics,hasWikiEnabled,defaultBranchRef,homepageUrl
```
Returns: description (string), repositoryTopics (array of {name}), defaultBranchRef.name (string), homepageUrl (string).

### Branch Protection
```bash
gh api repos/{owner}/{repo}/branches/main/protection
```
Returns 200 if protection is enabled, 404 if not. Requires admin access to read.

### Repository Details (Social Preview)
```bash
gh api repos/{owner}/{repo} --jq '.has_pages, .open_issues_count, .has_projects'
```

### Topics (Set)
```bash
gh repo edit --add-topic "topic1" --add-topic "topic2"
```

### Description (Set)
```bash
gh repo edit --description "Your description here"
```

## Scoring Rubric

### Standard Files (30% weight)

| Score | Criteria |
|-------|----------|
| 100 | All files present: LICENSE, .gitignore, SECURITY.md, CONTRIBUTING.md, CODEOWNERS, .editorconfig, PR template, issue templates, CHANGELOG, CODE_OF_CONDUCT |
| 80 | All required files present (LICENSE, .gitignore, SECURITY.md, CONTRIBUTING.md). Missing only recommended files. |
| 60 | LICENSE and .gitignore present. Missing 1-2 required files. |
| 40 | LICENSE or .gitignore present but not both. Multiple required files missing. |
| 20 | Only .gitignore present, no LICENSE. |
| 0 | Neither LICENSE nor .gitignore present. |

For private repos: only README.md and .gitignore are scored. All others are informational.

### GitHub Config (15% weight)

| Score | Criteria |
|-------|----------|
| 100 | Description set, 3+ topics, default branch is `main`, branch protection enabled |
| 75 | Description set, 1-2 topics, default branch is `main`, no branch protection |
| 50 | Description set, no topics, default branch is `main` |
| 25 | Description set, other issues |
| 0 | No description set |

### Documentation (25% weight)

| Score | Criteria |
|-------|----------|
| 100 | README 50+ lines with description, install instructions, license reference. CHANGELOG present and current (updated within 90 days). |
| 80 | README 50+ lines with description and install instructions. CHANGELOG present but stale. |
| 60 | README exists with description. Missing install instructions or license reference. No CHANGELOG. |
| 40 | README exists but is thin (< 50 lines) or missing key sections. |
| 20 | README exists but is a stub (< 10 lines). |
| 0 | No README. |

### Code Hygiene (20% weight)

| Score | Criteria |
|-------|----------|
| 100 | No tracked secrets, no stale branches, no large binaries (or LFS configured), lockfile present. |
| 80 | No tracked secrets, 1-3 stale branches, no large binaries. |
| 60 | No tracked secrets, 4-10 stale branches or 1-2 large binaries without LFS. |
| 40 | Minor issues: missing lockfile, many stale branches. No tracked secrets. |
| 20 | Tracked secrets (.env files) found OR large binaries without LFS. |
| 0 | Multiple critical hygiene failures (tracked secrets AND large binaries AND many stale branches). |

### Community (10% weight)

| Score | Criteria |
|-------|----------|
| 100 | CODE_OF_CONDUCT, CONTRIBUTING.md, issue templates (YAML form-based), PR template all present. |
| 75 | 3 of 4 community files present. |
| 50 | 2 of 4 community files present. |
| 25 | 1 of 4 community files present. |
| 0 | No community files. |

## Branch Protection Recommended Settings

For public repos, recommend these settings via `gh api`:

```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": []
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

Key settings explained:
- **Require PR reviews (1+)**: Prevents direct pushes to main
- **Dismiss stale reviews**: Re-request review when new commits are pushed
- **No force pushes**: Protects commit history
- **No branch deletion**: Prevents accidental deletion of main
- **Strict status checks**: Branch must be up to date before merging

For solo developers, a lighter config is acceptable:
- Require PR reviews: 0 (self-merge is fine)
- No force pushes: enabled
- No branch deletion: enabled
- Status checks: optional

## Issue Template Format (YAML Form-Based)

### Bug Report: `.github/ISSUE_TEMPLATE/bug_report.yml`

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
title: "[Bug]: "
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: "Thanks for reporting a bug. Please fill out the sections below."
  - type: textarea
    id: description
    attributes:
      label: Describe the bug
      description: A clear description of the unexpected behavior.
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      description: How can we reproduce this?
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      description: What did you expect to happen?
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: Version
      description: What version are you using?
    validations:
      required: false
  - type: textarea
    id: context
    attributes:
      label: Additional context
      description: Any other information (screenshots, logs, environment).
    validations:
      required: false
```

### Feature Request: `.github/ISSUE_TEMPLATE/feature_request.yml`

```yaml
name: Feature Request
description: Suggest a new feature or improvement
title: "[Feature]: "
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem or motivation
      description: What problem does this solve? Why do you need it?
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: Proposed solution
      description: How would you like this to work?
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
      description: Any workarounds or alternative approaches you've tried?
    validations:
      required: false
```

## PR Template Format

### `.github/pull_request_template.md`

```markdown
## Summary

<!-- What does this PR do? Link to related issue(s). -->

## Changes

-

## Testing

- [ ] Tests pass locally
- [ ] Manual testing completed
- [ ] No regressions observed

## Notes

<!-- Anything reviewers should know? -->
```

## Common .gitignore Entries by Language

### Node.js / TypeScript
```
node_modules/
dist/
build/
.env
.env.*
*.log
.DS_Store
coverage/
.turbo/
.next/
```

### Python
```
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.env
.venv/
venv/
.pytest_cache/
.mypy_cache/
*.egg
```

### Rust
```
target/
Cargo.lock  # for libraries only; commit for binaries
*.pdb
```

### Go
```
bin/
vendor/  # if using go modules
*.exe
*.test
```

### Universal (always include)
```
.DS_Store
Thumbs.db
*.swp
*.swo
*~
.idea/
.vscode/
*.env
*.env.*
```
