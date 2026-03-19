Cross-repository dependency audit. Scans package manifests for outdated packages, security advisories, version conflicts, and license issues. Produces a prioritized update plan. Supports Node.js, Python, Rust, and Go projects.


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


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
