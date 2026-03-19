# release-notes


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

Use [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format:

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Breaking Changes
- Description of breaking change (#PR)

### Added
- Description of new feature (#PR)

### Fixed
- Description of bug fix (#PR)

### Changed
- Description of refactor or improvement (#PR)

### Documentation
- Description of docs change (#PR)

### Maintenance
- Description of chore (#PR)
```

Omit empty categories. Order categories as shown above — Breaking Changes always first.

### Step 7 — Human review

Present the formatted entry and suggested version to the user. Wait for explicit approval before writing anything. Highlight any commits that were ambiguously categorized.

### Step 8 — Write to CHANGELOG.md

Prepend the new entry after the file header. Never overwrite or reorder existing entries. If CHANGELOG.md does not exist, create it with a standard header:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

### Step 9 — Optionally create GitHub release

Only when the user invoked `/release-notes release` or explicitly requests it:

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes "RELEASE_BODY"
```

Use the changelog entry as the release body. Never create a release without user confirmation.

## Key Principles

1. **Never auto-publish.** Every release and changelog write requires explicit human approval.
2. **Preserve existing entries.** Never modify, reorder, or delete previous changelog entries.
3. **Human-readable over machine-parseable.** Write descriptions that make sense to a person reading the changelog, not a parser. Prefer plain language over commit hashes.
4. **Attribute PRs and authors.** Include PR numbers as links. For multi-contributor projects, consider noting first-time contributors.
5. **When in doubt, ask.** If a commit is ambiguous, surface it to the user rather than guessing the category.

---

# release-notes — Reference

## Conventional Commits Specification

Conventional commits follow this structure:

```
type(scope): description

[optional body]

[optional footer(s)]
```

- **type**: Required. One of `feat`, `fix`, `docs`, `refactor`, `perf`, `chore`, `ci`, `build`, `test`, `style`, `deprecate`, `remove`, `security`.
- **scope**: Optional. A noun describing the section of the codebase (e.g., `parser`, `api`, `auth`).
- **description**: Required. A short summary in imperative mood ("add feature", not "added feature").
- **body**: Optional. Longer explanation of the change.
- **footer**: Optional. `BREAKING CHANGE: description` or `Refs: #123`.
- **`!` suffix**: Adding `!` after the type/scope (e.g., `feat!: remove v1 endpoints`) signals a breaking change without needing a footer.

## Keep a Changelog Format

Standard file structure:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] — 2026-03-19

### Added
- New feature description (#45)

### Fixed
- Bug fix description (#42)

## [1.1.0] — 2026-02-15

### Added
- Earlier feature (#30)

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/releases/tag/v1.1.0
```

### Category order

1. Breaking Changes
2. Deprecated
3. Removed
4. Security
5. Added
6. Fixed
7. Changed
8. Documentation
9. Maintenance

Omit empty categories.

## Semantic Versioning Rules

Given version `MAJOR.MINOR.PATCH`:

| Bump | When |
|---|---|
| **MAJOR** | Incompatible API changes, breaking changes, removed features |
| **MINOR** | New functionality added in a backward-compatible manner |
| **PATCH** | Backward-compatible bug fixes, documentation, refactors |

Pre-release versions: `1.0.0-alpha.1`, `1.0.0-beta.2`, `1.0.0-rc.1`.

The first stable release is `1.0.0`. Projects at `0.x.y` are considered unstable — any minor bump may contain breaking changes.

## Git Commands for Extracting History

### Find the latest tag

```bash
git describe --tags --abbrev=0
```

### List all tags sorted by version

```bash
git tag --sort=-v:refname
```

### Commits since last tag (excluding merges)

```bash
git log v1.1.0..HEAD --pretty=format:"%H|%s|%an|%ai" --no-merges
```

### Commits between two tags

```bash
git log v1.0.0..v1.1.0 --pretty=format:"%H|%s|%an|%ai" --no-merges
```

### Full commit history for init mode

```bash
git log --pretty=format:"%H|%s|%an|%ai" --no-merges --reverse
```

### Date of a specific tag

```bash
git log -1 --format=%ai v1.1.0
```

### Check if a tag exists

```bash
git tag -l "v1.2.0"
```

## gh CLI Commands for Releases

### List existing releases

```bash
gh release list --limit 10
```

### Create a release

```bash
gh release create v1.2.0 --title "v1.2.0" --notes "Release body here"
```

### Create a release from a specific tag

```bash
gh release create v1.2.0 --target main --title "v1.2.0" --notes-file RELEASE_NOTES.md
```

### Create a draft release (does not publish)

```bash
gh release create v1.2.0 --draft --title "v1.2.0" --notes "Draft release"
```

### Create a pre-release

```bash
gh release create v1.2.0-rc.1 --prerelease --title "v1.2.0-rc.1" --notes "Release candidate"
```

### List merged PRs since a date

```bash
gh pr list --state merged --search "merged:>2026-03-01" --json number,title,labels,mergedAt --limit 200
```

### Get PR details by number

```bash
gh pr view 42 --json title,body,labels,mergedAt,mergeCommit
```

## Version Comparison Patterns

### Parse the current version from a tag

```bash
latest_tag=$(git describe --tags --abbrev=0 2>/dev/null)
# Strip leading 'v' if present
version="${latest_tag#v}"
major=$(echo "$version" | cut -d. -f1)
minor=$(echo "$version" | cut -d. -f2)
patch=$(echo "$version" | cut -d. -f3)
```

### Compute next version

```
If breaking changes → (major+1).0.0
If new features    → major.(minor+1).0
If fixes only      → major.minor.(patch+1)
```

### Tag format conventions

Most projects use `v` prefix: `v1.2.0`. Some omit it: `1.2.0`. Match whatever convention the repo already uses. Check existing tags with `git tag -l` before creating a new one.
