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
