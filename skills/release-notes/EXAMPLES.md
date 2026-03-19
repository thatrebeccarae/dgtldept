# release-notes — Examples

## Example 1: Generate changelog for a repo with conventional commits

**Input:**
```
/release-notes changelog
```

**Git history since last tag (v2.3.1):**
```
a1b2c3d feat(auth): add OAuth2 PKCE support (#112)
d4e5f6a fix(api): handle null response from upstream (#108)
f7a8b9c fix(ui): correct date picker timezone offset (#110)
c0d1e2f docs: update API authentication guide (#111)
3a4b5c6 chore: upgrade eslint to v9 (#109)
e7f8a9b feat!: remove deprecated /v1/users endpoint (#113)
```

**Generated changelog entry:**
```markdown
## [3.0.0] — 2026-03-19

### Breaking Changes
- Remove deprecated /v1/users endpoint (#113)

### Added
- Add OAuth2 PKCE support for auth flow (#112)

### Fixed
- Handle null response from upstream API (#108)
- Correct date picker timezone offset (#110)

### Documentation
- Update API authentication guide (#111)

### Maintenance
- Upgrade eslint to v9 (#109)
```

**Suggested version:** 3.0.0 (major bump due to breaking change). User confirms, entry is prepended to CHANGELOG.md.

---

## Example 2: Generate changelog for a repo without conventional commits

**Input:**
```
/release-notes changelog ~/projects/legacy-app
```

**Git history since last tag (v0.8.0):**
```
a1b2c3d Added dark mode toggle to settings page (#45)
d4e5f6a Fix crash when opening empty project (#41)
f7a8b9c Updated README with new screenshots
c0d1e2f Refactored database connection pooling
3a4b5c6 Bump dependencies
e7f8a9b Fixed typo in error message (#43)
```

**AI categorization (presented for review):**
```
Added:
  - "Added dark mode toggle" → Added (keyword: "Added")
Fixed:
  - "Fix crash when opening empty project" → Fixed (keyword: "Fix")
  - "Fixed typo in error message" → Fixed (keyword: "Fixed")
Changed:
  - "Refactored database connection pooling" → Changed (keyword: "Refactored")
Documentation:
  - "Updated README with new screenshots" → Documentation (keyword: "README")
Maintenance:
  - "Bump dependencies" → Maintenance (keyword: "Bump")
```

**Generated changelog entry:**
```markdown
## [0.9.0] — 2026-03-19

### Added
- Dark mode toggle in settings page (#45)

### Fixed
- Crash when opening empty project (#41)
- Typo in error message (#43)

### Changed
- Refactored database connection pooling

### Documentation
- Updated README with new screenshots

### Maintenance
- Bump dependencies
```

**Suggested version:** 0.9.0 (minor bump — new feature, no breaking changes).

---

## Example 3: Create a GitHub release with changelog entry

**Input:**
```
/release-notes release ~/projects/my-api v4.1.0
```

**Procedure:**
1. Commits collected and categorized (3 features, 2 fixes).
2. Changelog entry formatted and shown to user.
3. User approves.
4. Entry prepended to CHANGELOG.md.
5. GitHub release created:

```bash
gh release create v4.1.0 --title "v4.1.0" --notes "$(cat <<'EOF'
## What's New

### Added
- Batch endpoint for bulk operations (#201)
- Rate limiting with configurable thresholds (#198)
- Health check endpoint with dependency status (#195)

### Fixed
- Memory leak in WebSocket connection handler (#199)
- Incorrect pagination headers on empty results (#196)

**Full Changelog**: https://github.com/user/repo/compare/v4.0.0...v4.1.0
EOF
)"
```

Output: `https://github.com/user/repo/releases/tag/v4.1.0`

---

## Example 4: Retroactively generate changelog from full history

**Input:**
```
/release-notes init ~/projects/side-project
```

**Repo state:** 3 tags exist (`v0.1.0`, `v0.2.0`, `v1.0.0`), plus 8 untagged commits after `v1.0.0`.

**Procedure:**
1. Walk all tags in chronological order.
2. For each tag range, collect and categorize commits.
3. Generate entries for `v0.1.0`, `v0.2.0`, `v1.0.0`, and an `[Unreleased]` section.
4. Present the full CHANGELOG.md to the user for review.
5. On approval, write the file.

**Generated CHANGELOG.md:**
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- WebSocket support for real-time updates (#18)

### Fixed
- Connection timeout on slow networks (#17)

## [1.0.0] — 2026-01-15

### Breaking Changes
- New authentication required for all endpoints (#14)

### Added
- Full REST API (#12)
- User management (#13)

## [0.2.0] — 2025-11-20

### Added
- Database persistence (#8)
- Configuration file support (#7)

### Fixed
- Startup crash on missing env vars (#9)

## [0.1.0] — 2025-10-01

### Added
- Initial project setup
- Basic CLI interface (#1)
- Core processing engine (#2)

[Unreleased]: https://github.com/user/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/user/repo/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/user/repo/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/user/repo/releases/tag/v0.1.0
```

User reviews, requests moving one entry from Changed to Added, approves the corrected version, and the file is written.
