# dep-audit


# Dependency Audit

Cross-repository dependency audit. Scans package manifests (package.json, pyproject.toml, Cargo.toml, go.mod) for outdated packages, security advisories, version conflicts between repos, and license compatibility issues. Produces a prioritized update plan.

## When to Use

- **Monthly hygiene**: Run on a cadence to catch dependency drift before it compounds
- **Before releases**: Verify no known vulnerabilities ship to production
- **Security incidents**: When a CVE drops, quickly assess exposure across all repos
- **Onboarding new repos**: Baseline the dependency health of a repo you're inheriting or adopting

## Usage

- `/dep-audit [repo-path]` — audit a single repository
- `/dep-audit [repo-path1] [repo-path2] ...` — cross-repo audit (enables version conflict detection)

## Procedure

### 1. Detect Package Managers

Scan the target repo(s) for manifest files:

| Manager | Manifest | Lock File |
|---------|----------|-----------|
| npm | `package.json` | `package-lock.json` |
| yarn | `package.json` | `yarn.lock` |
| pnpm | `package.json` | `pnpm-lock.yaml` |
| pip | `requirements.txt`, `setup.py`, `setup.cfg` | `requirements.txt` (pinned) |
| poetry | `pyproject.toml` (has `[tool.poetry]`) | `poetry.lock` |
| uv | `pyproject.toml` (has `[tool.uv]`) | `uv.lock` |
| cargo | `Cargo.toml` | `Cargo.lock` |
| go mod | `go.mod` | `go.sum` |

```bash
# Detect which manifests exist
ls package.json pyproject.toml Cargo.toml go.mod requirements.txt 2>/dev/null
# Detect lock files
ls package-lock.json yarn.lock pnpm-lock.yaml poetry.lock uv.lock Cargo.lock go.sum 2>/dev/null
```

If multiple ecosystems are present (e.g., a monorepo with Node.js frontend and Go backend), audit each independently and merge results.

### 2. Parse Manifests and Lock Files

Read the manifest to identify declared dependencies (direct) and the lock file for resolved versions (transitive). Distinguish between:
- **Production dependencies** (`dependencies`, `[dependencies]`, main requires)
- **Development dependencies** (`devDependencies`, `[dev-dependencies]`, extras)

### 3. Check for Outdated Packages

Query the registry for latest versions and categorize the delta:

```bash
# Node.js
npm outdated --json

# Python (pip)
pip list --outdated --format=json

# Python (poetry)
poetry show --outdated

# Rust
cargo outdated --format json  # requires cargo-outdated

# Go
go list -m -u all
```

Categorize each outdated package:
- **Patch update** (e.g., 2.3.1 -> 2.3.4): Safe, usually bug fixes
- **Minor update** (e.g., 2.3.1 -> 2.5.0): New features, should be backward-compatible
- **Major update** (e.g., 2.3.1 -> 3.0.0): Breaking changes likely, needs migration review

### 4. Check for Security Advisories

Run ecosystem-native audit tools:

```bash
# Node.js
npm audit --json

# Python
pip-audit --format=json  # or: safety check

# Rust
cargo audit --json  # requires cargo-audit

# Go
govulncheck ./...
```

Parse severity from results:
- **Critical**: Remote code execution, authentication bypass, data exfiltration
- **High**: Privilege escalation, significant data exposure
- **Medium**: DoS potential, limited data exposure
- **Low**: Information disclosure, minor issues

### 5. Cross-Repo Analysis (Multiple Repos)

When auditing two or more repos, compare dependency versions:

- **Version conflicts**: Same package at different versions across repos (e.g., `axios@0.27.2` in repo A, `axios@1.6.2` in repo B)
- **Shared dependencies**: Packages used by multiple repos that could be aligned to a single version
- **Divergent major versions**: Flag these as highest priority — they indicate repos drifting apart

Present a conflict table showing package, version per repo, and recommended target version.

### 6. License Scan

Check dependency licenses against compatibility rules:

```bash
# Node.js
npx license-checker --json

# Python
pip-licenses --format=json

# Rust
cargo license --json  # requires cargo-license

# Go
go-licenses report ./...  # requires go-licenses
```

Flag issues:
- **Copyleft in permissive projects**: GPL/AGPL dependencies in MIT/Apache-licensed projects
- **Unknown or missing licenses**: Dependencies with no license metadata
- **Non-OSI-approved licenses**: Custom or restrictive licenses
- **License conflicts**: Incompatible license combinations (e.g., GPLv2-only with Apache-2.0)

### 7. Generate Update Plan

Prioritize all findings into a single ordered list:

1. **Critical security advisories** — fix immediately
2. **High security advisories** — fix this sprint
3. **License violations** — assess and remediate
4. **Major outdated (with known issues)** — plan migration
5. **Cross-repo version conflicts** — align versions
6. **Minor outdated** — batch update
7. **Patch outdated** — batch update

Group related updates together:
- All `@types/*` packages in one PR
- All packages from the same org (e.g., `@babel/*`)
- Peer dependency chains that must move together

Note breaking change risks for any major update. Link to migration guides where available.

### 8. Report

Produce a severity-coded summary table:

| Priority | Package | Current | Latest | Type | Severity | Repos Affected | Action |
|----------|---------|---------|--------|------|----------|---------------|--------|
| 1 | lodash | 4.17.19 | 4.17.21 | patch | CRITICAL (CVE-2021-23337) | repo-a, repo-b | Update immediately |
| 2 | express | 4.17.1 | 4.21.2 | minor | HIGH (CVE-2024-29041) | repo-a | Update this sprint |
| 3 | webpack | 4.46.0 | 5.94.0 | major | MEDIUM (outdated) | repo-a | Plan migration |
| ... | | | | | | | |

Follow with:
- Total dependency count (direct / transitive) per repo
- Security summary: X critical, Y high, Z medium, W low
- Outdated summary: X major, Y minor, Z patch
- License summary: X flagged, Y clean
- Cross-repo conflicts: X packages with version divergence

## Key Principles

1. **Never auto-update.** This skill audits and recommends. The human decides what to update and when. Automated updates can introduce breaking changes, especially for major versions.
2. **Security first.** Critical and high-severity vulnerabilities always top the priority list, regardless of how old other dependencies are.
3. **Group related updates.** Updating `react` without updating `react-dom` creates version mismatches. Always identify peer dependency chains.
4. **Context matters.** A major version bump on a dev-only dependency (e.g., `eslint`) is lower risk than a patch on a production runtime dependency with a CVE.
5. **Lock files are truth.** Always read the lock file for actual resolved versions, not just the range specifier in the manifest.
6. **Don't chase latest for its own sake.** If a dependency is working, stable, and has no advisories, "outdated" is not the same as "broken."

## How to Use This Skill

Ask:
- "Audit the dependencies in ~/Repos/my-app"
- "Compare dependency versions across these three repos"
- "Are there any security vulnerabilities in this project?"
- "Check for license issues before we open-source this repo"
- "Build me an update plan for everything that's behind"

For command reference, license compatibility details, and false positive handling, see [REFERENCE.md](REFERENCE.md).
For worked examples, see [EXAMPLES.md](EXAMPLES.md).

---

# Dependency Audit Reference

## Package Manager Commands

### Checking Outdated Packages

| Ecosystem | Command | Output |
|-----------|---------|--------|
| npm | `npm outdated --json` | Current, wanted, latest per package |
| yarn | `yarn outdated --json` | Same as npm but yarn format |
| pnpm | `pnpm outdated --format json` | Same structure |
| pip | `pip list --outdated --format=json` | Installed vs latest |
| poetry | `poetry show --outdated` | Table of outdated packages |
| uv | `uv pip list --outdated` | Installed vs latest |
| cargo | `cargo outdated --format json` | Requires `cargo-outdated` crate |
| go | `go list -m -u all` | Lists modules with available updates |

### Security Audit Commands

| Ecosystem | Command | Notes |
|-----------|---------|-------|
| npm | `npm audit --json` | Uses GitHub Advisory Database |
| npm | `npm audit --audit-level=critical` | Filter by severity |
| pip | `pip-audit --format=json` | Uses OSV database. Install: `pip install pip-audit` |
| pip | `safety check --json` | Uses Safety DB (requires API key for full access) |
| cargo | `cargo audit --json` | Uses RustSec Advisory DB. Install: `cargo install cargo-audit` |
| go | `govulncheck ./...` | Uses Go Vulnerability Database. Install: `go install golang.org/x/vuln/cmd/govulncheck@latest` |

### License Checking Commands

| Ecosystem | Command | Notes |
|-----------|---------|-------|
| npm | `npx license-checker --json` | All deps with licenses |
| npm | `npx license-checker --failOn "GPL-3.0"` | Fail on specific licenses |
| pip | `pip-licenses --format=json` | Install: `pip install pip-licenses` |
| cargo | `cargo license --json` | Install: `cargo install cargo-license` |
| go | `go-licenses report ./...` | Install: `go install github.com/google/go-licenses@latest` |

## Lock File Locations

| Package Manager | Lock File | Notes |
|----------------|-----------|-------|
| npm | `package-lock.json` | JSON, contains resolved versions and integrity hashes |
| yarn (classic) | `yarn.lock` | Custom format, not JSON |
| yarn (berry) | `yarn.lock` | YAML-ish format |
| pnpm | `pnpm-lock.yaml` | YAML |
| pip (pinned) | `requirements.txt` | Only if pinned with `==` |
| pip-tools | `requirements.txt` (generated) | From `requirements.in` |
| poetry | `poetry.lock` | TOML-like |
| uv | `uv.lock` | TOML |
| cargo | `Cargo.lock` | TOML |
| go | `go.sum` | Checksums, not versions — use `go.mod` for direct deps |

## Common License Types and Compatibility

### Permissive Licenses (low restriction)

| License | Can use in proprietary? | Can sublicense? | Attribution required? |
|---------|------------------------|----------------|----------------------|
| MIT | Yes | Yes | Yes |
| Apache-2.0 | Yes | Yes | Yes + NOTICE file |
| BSD-2-Clause | Yes | Yes | Yes |
| BSD-3-Clause | Yes | Yes | Yes (no endorsement) |
| ISC | Yes | Yes | Yes |
| Unlicense | Yes | Yes | No |

### Copyleft Licenses (viral, higher restriction)

| License | Derivative must be same license? | Can use in proprietary? | Network trigger? |
|---------|--------------------------------|------------------------|-----------------|
| GPL-2.0 | Yes | No (if distributed) | No |
| GPL-3.0 | Yes | No (if distributed) | No |
| LGPL-2.1 | Only modifications to the library | Yes (if dynamically linked) | No |
| LGPL-3.0 | Only modifications to the library | Yes (if dynamically linked) | No |
| AGPL-3.0 | Yes | No (even SaaS) | Yes |
| MPL-2.0 | File-level copyleft | Yes (unmodified files) | No |

### Compatibility Matrix (can A include B?)

| Project License \ Dep License | MIT | Apache-2.0 | GPL-2.0 | GPL-3.0 | AGPL-3.0 | LGPL |
|-------------------------------|-----|------------|---------|---------|----------|------|
| MIT | OK | OK | NO | NO | NO | OK* |
| Apache-2.0 | OK | OK | NO | NO | NO | OK* |
| GPL-2.0 | OK | NO** | OK | NO | NO | OK |
| GPL-3.0 | OK | OK | OK | OK | NO | OK |
| AGPL-3.0 | OK | OK | OK | OK | OK | OK |

\* LGPL is OK if the dependency is dynamically linked (standard for most package managers).
\** Apache-2.0 has patent clauses incompatible with GPL-2.0-only (but compatible with GPL-2.0-or-later and GPL-3.0).

### Licenses to Flag

- **AGPL-3.0**: Network copyleft. If you use it in a SaaS product, your entire codebase must be AGPL. Almost always a blocker for proprietary projects.
- **GPL-2.0 / GPL-3.0**: Copyleft. If you distribute the software, derivative works must use the same license.
- **SSPL**: MongoDB's Server Side Public License. Not OSI-approved. Treat as proprietary-restrictive.
- **BSL**: Business Source License. Time-delayed open source. Restrictions during the change period.
- **No license / UNLICENSED**: No license means all rights reserved by default. Cannot legally use.
- **Custom / Unknown**: Requires manual legal review.

## Severity Scoring Criteria

### Security Advisories

| Severity | CVSS Score | Criteria | SLA |
|----------|-----------|---------|-----|
| Critical | 9.0-10.0 | RCE, auth bypass, full data access, wormable | Fix immediately (same day) |
| High | 7.0-8.9 | Privilege escalation, significant data exposure, partial RCE with conditions | Fix this sprint |
| Medium | 4.0-6.9 | DoS, limited data exposure, requires user interaction | Plan for next cycle |
| Low | 0.1-3.9 | Information disclosure, theoretical attacks, minimal impact | Track, batch with other updates |

### Outdated Packages (no advisory)

| Category | Risk Level | Guidance |
|----------|-----------|---------|
| Major, 2+ versions behind | High | Accumulating migration debt. Plan upgrade. |
| Major, 1 version behind | Medium | Review changelog for breaking changes. Schedule. |
| Minor, 5+ versions behind | Medium | Likely missing perf/security improvements. |
| Minor, 1-4 versions behind | Low | Update opportunistically. |
| Patch, any amount behind | Low | Safe to batch update. |

## Dependabot vs Renovate

For automating dependency updates after the initial audit:

| Feature | Dependabot | Renovate |
|---------|-----------|----------|
| Hosting | GitHub-native | Self-hosted or Mend cloud |
| Config | `.github/dependabot.yml` | `renovate.json` |
| Grouping PRs | Limited (v2 groups) | Excellent (regex, package rules) |
| Monorepo support | Basic | Strong |
| Auto-merge | Via GitHub Actions | Built-in |
| Schedule control | Weekly/monthly | Cron expressions |
| Ecosystems | npm, pip, cargo, go, docker, etc. | Same + more (gradle, nuget, etc.) |
| License checks | No | Via `allowedLicenses` config |
| Changelog in PR | Yes | Yes (more detailed) |

**Recommendation**: Renovate for repos that need grouped PRs, complex schedules, or monorepo support. Dependabot for simple repos that want zero config on GitHub.

## Common False Positives

### npm audit

| False Positive | Why | How to Handle |
|----------------|-----|--------------|
| Advisory in devDependency only | No production exposure | Verify with `npm audit --omit=dev`. Suppress if dev-only. |
| Prototype pollution in deep transitive dep | Often requires specific call patterns that your code doesn't use | Check if the vulnerable function is reachable from your code. |
| ReDoS in a parser you don't use | Transitive dep pulls in vulnerable regex | If the parser is never invoked, document and suppress. |
| Advisory fixed in later version but lock file pins old | Lock file hasn't been refreshed | Run `npm update <package>` to pull the fix without a major bump. |

### pip-audit / safety

| False Positive | Why | How to Handle |
|----------------|-----|--------------|
| Advisory for a feature you don't use | e.g., XML parsing vuln but you only use JSON | Document the exclusion with rationale. |
| Withdrawn CVE | CVE was disputed or revoked | Check NVD status. Suppress if withdrawn. |
| OS-packaged Python library | System Python has different version than pip reports | Verify actual installed version matches. |

### cargo audit

| False Positive | Why | How to Handle |
|----------------|-----|--------------|
| Unmaintained crate advisory | `cargo audit` flags unmaintained crates as informational | Assess if a maintained fork exists. Not a security issue per se. |
| Advisory in optional feature not enabled | Crate compiled without the vulnerable feature flag | Verify with `cargo tree -f '{p} {f}'`. |

### govulncheck

| False Positive | Why | How to Handle |
|----------------|-----|--------------|
| Vulnerability in imported but unused function | `govulncheck` traces call graphs but may over-approximate | Check if the flagged symbol is reachable. govulncheck is already conservative — if it flags it, likely real. |

## Useful One-Liners

```bash
# Count total direct dependencies (Node.js)
jq '.dependencies | length' package.json

# Count total resolved packages (Node.js)
jq '.packages | length' package-lock.json

# List all direct deps with versions (Python/poetry)
grep -A1 '^\[tool.poetry.dependencies\]' pyproject.toml

# Find duplicate packages at different versions (Node.js)
npm ls --all 2>/dev/null | grep 'deduped' | wc -l

# Show dependency tree for a specific package
npm ls <package-name>
cargo tree -p <crate-name>
go mod graph | grep <module-name>

# Check if a specific CVE affects you (npm)
npm audit --json | jq '.vulnerabilities | to_entries[] | select(.value.via[].url | test("CVE-XXXX-XXXXX"))'
```
