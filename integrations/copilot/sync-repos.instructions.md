Manage public/private repository pairs. Verify parity, detect drift, run sync scripts, and validate no sensitive data leaks to the public repo. Use for projects that maintain separate dev and public repositories.


# Sync Repos

Manage public/private repository pairs. Verify parity between a dev (private) repo and its public counterpart, detect drift, run sync scripts, validate results, and ensure no PII or secrets leak to the public side.

## When to Use

- Before pushing a public repo — verify the sync is clean and current
- After major dev work — check whether the public repo has drifted behind
- On a periodic cadence — weekly or before releases, catch unsynced changes early
- When setting up a new public/private repo pair for the first time

## Usage

- `/sync-repos check [dev-path] [public-path]` — Compare repos and report drift
- `/sync-repos sync [dev-path] [public-path]` — Run sync script and validate
- `/sync-repos setup [dev-path] [public-path]` — Create initial sync-public.sh and config

If paths are omitted, prompt the user for them. Look for `.syncignore` or `scripts/sync-public.conf` in the dev repo to auto-detect the pair.

## Procedure

### Check Mode

1. **Validate paths.** Confirm both paths exist and contain `.git/` directories. Abort with a clear message if either is not a git repo.

2. **Detect sync script.** Look for `scripts/sync-public.sh`, `scripts/sync-public.conf`, or `.syncignore` in the dev repo. Report whether a sync mechanism exists.

3. **Compare file lists.** Generate sorted file lists for both repos (excluding `.git/`, `node_modules/`, `dist/`). Categorize differences:
   - **Expected exclusions** — files matching known exclusion patterns (see Common Exclusion Patterns below) or listed in `.syncignore` / `sync-public.conf`
   - **Unexpected drift** — files present in dev but missing from public that are NOT in any exclusion list
   - **Diverged files** — files present in both repos but with different content (compare via `sha256sum` or `git hash-object`)
   - **Public-only files** — files in public but not in dev (legitimate: README, CONTRIBUTING, LICENSE, .github/)

4. **Check last sync timestamp.** If `scripts/sync-public.sh` exists, check its last execution time via the most recent commit in the public repo that matches a sync pattern. Compare against the latest commit in the dev repo.

5. **Report.** Present a summary table:
   - Sync script: found / not found
   - Files only in dev (expected): count
   - Files only in dev (unexpected): count + list
   - Diverged files: count + list
   - Public-only files: count + list
   - Estimated drift: number of dev commits since last sync
   - Recommendation: "in sync", "minor drift", or "sync needed"

### Sync Mode

1. **Run check first.** Execute the full check procedure above. If no drift is detected, report "already in sync" and stop.

2. **Locate sync script.** Look for `scripts/sync-public.sh` in the dev repo. If not found, ask the user whether to run setup mode to create one.

3. **Preview the sync.** Show what the sync script will do — files to copy, exclusions, text replacements. Require user confirmation before proceeding.

4. **Execute the sync script.** Run from the dev repo root:
   ```bash
   bash scripts/sync-public.sh
   ```
   Capture stdout and stderr. If the script exits non-zero, report the error and stop.


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
