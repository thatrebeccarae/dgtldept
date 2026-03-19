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
