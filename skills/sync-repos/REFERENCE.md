# Sync Repos Reference

## sync-public.sh Template

Rsync-based sync script. Source `sync-public.conf` for configuration.

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=sync-public.conf
source "${SCRIPT_DIR}/sync-public.conf"

# -- Helpers -----------------------------------------------------------
log()  { echo "[sync] $*"; }
warn() { echo "[sync] WARNING: $*" >&2; }
die()  { echo "[sync] ERROR: $*" >&2; exit 1; }

# -- Validate ----------------------------------------------------------
[[ -d "${SOURCE_DIR}/.git" ]] || die "SOURCE_DIR is not a git repo: ${SOURCE_DIR}"
[[ -d "${TARGET_DIR}/.git" ]] || die "TARGET_DIR is not a git repo: ${TARGET_DIR}"
log "Source: ${SOURCE_DIR}"
log "Target: ${TARGET_DIR}"

# -- Prepare target ----------------------------------------------------
mkdir -p "${TARGET_DIR}"

# -- Clean stale untracked files ---------------------------------------
if [[ -d "${TARGET_DIR}/.git" ]]; then
  log "Cleaning stale untracked files from target..."
  (cd "${TARGET_DIR}" && git clean -fd --exclude=node_modules) || warn "git clean failed"
fi

# -- Build rsync exclude list ------------------------------------------
RSYNC_EXCLUDES=()
for p in "${EXCLUDE_PATHS[@]+"${EXCLUDE_PATHS[@]}"}"; do
  RSYNC_EXCLUDES+=(--exclude "$p")
done

# -- Copy files --------------------------------------------------------
log "Copying files..."
rsync -a --delete-excluded \
  "${RSYNC_EXCLUDES[@]+"${RSYNC_EXCLUDES[@]}"}" \
  "${SOURCE_DIR}/" "${TARGET_DIR}/"

# -- Verify: check for personal data leaks -----------------------------
log "Checking for personal data leaks..."
LEAKS=0
# Add project-specific patterns to this array
LEAK_PATTERNS=()

for pattern in "${LEAK_PATTERNS[@]+"${LEAK_PATTERNS[@]}"}"; do
  MATCHES=$(grep -rE "$pattern" "${TARGET_DIR}" \
    --include='*.ts' --include='*.js' --include='*.json' \
    --include='*.md' --include='*.sh' --include='*.yaml' \
    --include='*.yml' --include='*.toml' --include='*.py' \
    2>/dev/null || true)
  if [[ -n "$MATCHES" ]]; then
    echo "  LEAK: '$pattern' found:"
    echo "$MATCHES" | head -5
    LEAKS=$((LEAKS + 1))
  fi
done

if [[ "$LEAKS" -gt 0 ]]; then
  die "$LEAKS personal data pattern(s) found in public repo — aborting"
fi
log "Clean — no personal data leaks detected"

# -- Summary -----------------------------------------------------------
FILE_COUNT=$(find "${TARGET_DIR}" -type f ! -path '*/.git/*' ! -path '*/node_modules/*' | wc -l | tr -d ' ')
log "Done. ${FILE_COUNT} files synced to ${TARGET_DIR}"
```

## sync-public.conf Template

```bash
# sync-public.conf — Configuration for sync-public.sh
# Source this file; do not execute directly.

SOURCE_DIR="${SOURCE_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
TARGET_DIR="${TARGET_DIR:-$(dirname "$SOURCE_DIR")/PUBLIC_REPO_NAME}"

PACKAGE_NAME="${PACKAGE_NAME:-my-project}"

# Files/directories to EXCLUDE from sync (relative to SOURCE_DIR)
EXCLUDE_PATHS=(
  ".git/"
  ".env"
  ".env.*"
  "!.env.example"
  ".planning/"
  ".claude/"
  "CLAUDE_CONTEXT.md"
  "data/"
  "dist/"
  "node_modules/"
  "*.pem"
  "*.key"
  "*.plist"
  "briefs/"
  "scripts/sync-public.sh"
  "scripts/sync-public.conf"
)

# Directories in TARGET_DIR to preserve (not deleted during clean step)
PRESERVE_PATHS=(
  ".git"
  "node_modules"
  "README.md"
  "LICENSE"
  "CONTRIBUTING.md"
  "SECURITY.md"
  "CHANGELOG.md"
  ".github"
)
```

## Common Exclusion Patterns by Project Type

### Node.js / TypeScript
```
node_modules/  dist/  .env  .env.*  *.pem  *.key  data/
.planning/  .claude/  CLAUDE_CONTEXT.md  briefs/
scripts/sync-public.*  config/soul.md  *.plist
```

### Python
```
__pycache__/  *.pyc  .venv/  venv/  .env  .env.*
*.pem  *.key  data/  .planning/  .claude/
CLAUDE_CONTEXT.md  scripts/sync-public.*
```

### Rust
```
target/  .env  .env.*  *.pem  *.key  data/
.planning/  .claude/  CLAUDE_CONTEXT.md
scripts/sync-public.*
```

### General (all projects)
```
.git/  .DS_Store  *.log  .syncthing.*.tmp
```

## Git-Based Sync Alternative

For projects where rsync is too coarse, use `git format-patch` / `git am` to replay commits selectively.

```bash
# In the dev repo: export patches since last sync tag
git format-patch last-sync-tag..HEAD --output-directory /tmp/patches/

# In the public repo: apply patches
git am /tmp/patches/*.patch

# Tag the sync point in dev
git tag -a "sync-$(date +%Y%m%d)" -m "Synced to public"
```

Limitations: requires commit-level discipline (no commits that mix public and private content). Best for projects with clean commit hygiene. The rsync approach is more forgiving.

## Drift Detection Methods

### File hash comparison
```bash
# Generate sorted hash manifests for both repos
(cd "$DEV_REPO" && find . -type f ! -path './.git/*' ! -path './node_modules/*' \
  -exec sha256sum {} \; | sort) > /tmp/dev-manifest.txt

(cd "$PUBLIC_REPO" && find . -type f ! -path './.git/*' ! -path './node_modules/*' \
  -exec sha256sum {} \; | sort) > /tmp/public-manifest.txt

# Compare (filtering expected exclusions)
diff /tmp/dev-manifest.txt /tmp/public-manifest.txt
```

### Git log comparison
```bash
# Last commit timestamps
DEV_LAST=$(cd "$DEV_REPO" && git log -1 --format='%aI')
PUB_LAST=$(cd "$PUBLIC_REPO" && git log -1 --format='%aI')

# Commits in dev since public's last update
cd "$DEV_REPO" && git log --oneline --since="$PUB_LAST"
```

## PII Scan Patterns

Reused from the safe-push skill. Scan all text files in the public repo diff for:

| Category | Pattern Examples |
|----------|-----------------|
| Email addresses | `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` |
| Phone numbers | `\b\d{3}[-.]?\d{3}[-.]?\d{4}\b` |
| API keys/tokens | `(sk-[a-zA-Z0-9]{20,})`, `(xoxb-[a-zA-Z0-9-]+)`, `(ghp_[a-zA-Z0-9]{36})` |
| AWS keys | `AKIA[0-9A-Z]{16}` |
| Private IPs | `\b(10\.\|172\.(1[6-9]\|2[0-9]\|3[01])\.\|192\.168\.)\d+\.\d+\b` |
| Private keys | `-----BEGIN (RSA\|EC\|DSA)? ?PRIVATE KEY-----` |
| Generic secrets | `(password\|secret\|token\|apikey)\s*[:=]\s*['"][^'"]+['"]` (case-insensitive) |

Allowlist: if the public repo contains a `.pii-allowlist` file (one regex per line), matches are excluded from the scan.

## .syncignore File Format

Optional file at the dev repo root. Same syntax as `.gitignore`. Defines additional files to exclude from sync beyond the defaults in `sync-public.conf`.

```
# .syncignore — additional exclusions for public sync
# One pattern per line. Supports glob patterns.

# Internal docs
docs/internal/
ROADMAP-INTERNAL.md

# Test fixtures with real data
tests/fixtures/real-data/

# Draft content
*.draft.md
```

When both `.syncignore` and `sync-public.conf` exist, merge the exclusion lists (union). `.syncignore` is additive — it never removes exclusions from `sync-public.conf`.
