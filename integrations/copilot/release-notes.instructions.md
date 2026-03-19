Generate changelog entries and GitHub releases from git history. Categorizes commits into features, fixes, breaking changes, and docs. Supports conventional commits, PR-based grouping, and semantic versioning. Creates formatted CHANGELOG.md entries and GitHub releases.


# release-notes

Generate changelog entries and GitHub releases from git history.

## When to Use

- **Cutting a release**: You have commits ready to ship and need a changelog entry and/or GitHub release.
- **Monthly changelog update**: You maintain a regular changelog cadence and need to capture everything since the last entry.
- **Retroactive changelog**: An existing project has no CHANGELOG.md and you want to generate one from the full git history.

## Usage

### Generate a changelog entry

```
/release-notes changelog [repo-path]
```

Reads commits since the last tag, categorizes them, and prepends a new entry to CHANGELOG.md.

### Create a changelog entry and GitHub release

```
/release-notes release [repo-path] [version]
```

Does everything `changelog` does, then creates a GitHub release via `gh release create`. If `version` is omitted, a version is suggested based on the changes detected.

### Retroactively generate a full changelog

```
/release-notes init [repo-path]
```

Walks the entire tag history (or full commit history if untagged) and generates a complete CHANGELOG.md from scratch.

## Procedure

### Step 1 — Find the last tag or release

Run `git describe --tags --abbrev=0` to find the most recent tag. If no tags exist, use the initial commit as the starting point. Cross-reference with `gh release list --limit 1` to check for GitHub releases that may differ from local tags.

### Step 2 — Collect commits since last tag

```bash
git log <last-tag>..HEAD --pretty=format:"%H %s" --no-merges
```

Parse each commit message for conventional commit prefixes (`type(scope): description`). Record the raw message for commits that do not follow conventional format.

### Step 3 — Check merged PRs

```bash
gh pr list --state merged --search "merged:>YYYY-MM-DD" --json number,title,labels,mergedAt --limit 200
```

Use the date of the last tag as the cutoff. Cross-reference PR titles with commit messages to avoid duplicates. PR titles often provide cleaner descriptions than commit messages — prefer the PR title when a commit is associated with a merged PR.

### Step 4 — Categorize changes

Map each commit or PR to a changelog category:

| Prefix / Signal | Category |
|---|---|
| `feat`, `feature` | **Added** |
| `fix` | **Fixed** |
| `BREAKING CHANGE` in body or `!` suffix (e.g., `feat!:`) | **Breaking Changes** |
| `docs` | **Documentation** |
| `refactor`, `perf` | **Changed** |
| `chore`, `ci`, `build` | **Maintenance** |
| `deprecate` | **Deprecated** |
| `remove` | **Removed** |
| `security` | **Security** |

**When conventional commits are not used**: Analyze commit message content to infer categories. Look for keywords like "add", "fix", "remove", "update", "refactor", "document". Group ambiguous commits under **Changed** and flag them for human review.

### Step 5 — Suggest version bump

Apply semantic versioning rules:

- **Major** bump if any Breaking Changes are present.
- **Minor** bump if any Added entries exist and no breaking changes.
- **Patch** bump if only Fixed, Changed, or Maintenance entries.

Present the suggestion with reasoning. The human decides the final version.

### Step 6 — Format the changelog entry


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
