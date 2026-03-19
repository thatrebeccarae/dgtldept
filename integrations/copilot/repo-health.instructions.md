One-command GitHub repository health audit. Checks for missing standard files, GitHub configuration, branch protection, documentation quality, and code hygiene. Produces a scored health report with prioritized fix recommendations.


# Repo Health

One-command health audit for GitHub repositories. Produces a scored report with prioritized fix recommendations.

## When to Use

- Setting up a new repo and want to make sure nothing is missing
- Periodic health checks on active repositories
- Before open-sourcing a private repo (what needs to be added?)
- Onboarding onto an unfamiliar repo to assess its state
- Pre-release hygiene sweep

## How to Use

```
/repo-health [repo-path]        # Full audit with scored report
/repo-health [repo-path] --fix  # Audit + generate missing files
```

Default `repo-path` is the current working directory if omitted.


## Procedure

Execute each step in order. Do not skip steps.

### Step 1: Validate Repo Path

1. If `repo-path` is provided, resolve to absolute path. If omitted, use current working directory.
2. Confirm the path exists and is a directory.
3. Confirm it contains a `.git` directory (is a git repo).

If validation fails:
```
Error: {repo-path} is not a git repository.
Provide a path to a git repo or run from within one.
```
STOP.

### Step 2: Detect Public/Private

Determine repo visibility:
1. Check for `.public-repo` marker file at repo root -> public
2. Check if "public" appears in the remote URL -> public
3. Run `gh repo view --json isPrivate -q '.isPrivate'` if `gh` is available -> use result
4. If none of the above resolve it -> ask the user

Store as `repo_visibility` (public or private). Public repos are held to a stricter standard in scoring.

### Step 3: File Presence Checks

Check for each standard file. Track result as PRESENT or MISSING.

| File | Required (Public) | Required (Private) |
|------|-------------------|--------------------|
| `LICENSE` | Yes | No |
| `README.md` | Yes | Yes |
| `.gitignore` | Yes | Yes |
| `SECURITY.md` | Yes | No |
| `CONTRIBUTING.md` | Yes | No |
| `CODEOWNERS` | Recommended | No |
| `.editorconfig` | Recommended | Recommended |
| `.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE.md` | Recommended | No |
| `.github/ISSUE_TEMPLATE/` directory (or `.github/ISSUE_TEMPLATE.md`) | Recommended | No |
| `CHANGELOG.md` | Recommended | No |
| `CODE_OF_CONDUCT.md` | Recommended (public) | No |

### Step 4: GitHub Configuration Checks

Use `gh` CLI to query repo metadata. If `gh` is not available, skip this category and note it in the report.

```bash
gh repo view --json description,repositoryTopics,hasWikiEnabled,defaultBranchRef,homepageUrl
```

Check each item. Track as PASS or FAIL.

| Check | Criteria |
|-------|----------|
| Description set | `description` is non-empty |
| Topics set | `repositoryTopics` has at least 3 topics |
| Homepage URL | `homepageUrl` is set (if project has a site) |
| Default branch name | `defaultBranchRef.name` is `main` (not `master`) |
| Branch protection | `gh api repos/{owner}/{repo}/branches/main/protection` returns 200 (public repos only) |
| Social preview | `gh api repos/{owner}/{repo}` and check for custom Open Graph image (informational only) |

### Step 5: Documentation Quality


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
