# Sync Repos Examples

## Example 1: Check Drift Between Dev and Public Repos

**User Request**: "Check if aouda-dev and aouda are in sync"

**Invocation**: `/sync-repos check ~/Popoloto/Repos.nosync/aouda-dev ~/Popoloto/Repos.nosync/aouda`

**Steps Taken**:
1. Validate both paths are git repos
2. Locate `scripts/sync-public.sh` and `scripts/sync-public.conf` in aouda-dev
3. Parse exclusion list from `sync-public.conf`
4. Generate file manifests for both repos, filtering exclusions
5. Compare file hashes for files present in both

**Sample Output**:
```
Sync Repos — Check Report
==========================

Dev repo:    ~/Popoloto/Repos.nosync/aouda-dev (142 files)
Public repo: ~/Popoloto/Repos.nosync/aouda (98 files)
Sync script: scripts/sync-public.sh (found)

Files only in dev (expected exclusions): 38
  .env, .planning/*, config/soul.md, data/*, briefs/*, ...

Files only in dev (UNEXPECTED): 3
  src/config/new-feature.ts
  src/plugins/experimental.ts
  tests/integration/new-feature.test.ts

Diverged files: 1
  src/agent/prompt.ts (dev: a3f8c2b, public: 91e4d0a)

Public-only files: 4
  README.md, LICENSE, CONTRIBUTING.md, .github/workflows/ci.yml

Dev commits since last sync: 7
Recommendation: SYNC NEEDED — 3 unexpected files missing from public, 1 file diverged
```

**Next Step**: User runs `/sync-repos sync` to bring public up to date.

## Example 2: Full Sync Workflow

**User Request**: "Sync ouras dev repo to public"

**Invocation**: `/sync-repos sync ~/Popoloto/Repos.nosync/v0-ouras-landing-page ~/Popoloto/Repos.nosync/ouras`

**Steps Taken**:
1. Run check (as in Example 1). Drift detected: 5 files diverged, 2 new files missing.
2. Locate `scripts/sync-public.sh` in dev repo.
3. Preview sync: "Will rsync 67 files, excluding 22 patterns. Text replacements: none configured."
4. User confirms.
5. Execute `bash scripts/sync-public.sh`. Script completes with exit code 0.
6. Run post-sync check — all files now match.
7. PII/secrets scan on public repo diff: scan all changed files for email addresses, API keys, private IPs, hostnames.

**Sample Output**:
```
Sync Repos — Sync Report
==========================

Sync script: scripts/sync-public.sh
Exit code: 0

Files synced: 69
Exclusions applied: 22 patterns
New files in public: 2
Updated files in public: 5

PII/Secrets Scan: CLEAN
  Scanned 7 changed files
  No email addresses, API keys, private IPs, or secrets detected

Post-sync check: IN SYNC
  All non-excluded files match between dev and public

Next step: Review changes in the public repo, then /safe-push when ready.
```

## Example 3: Set Up Sync for a New Repo Pair

**User Request**: "Set up sync between clawclip-build (dev) and clawclip (public)"

**Invocation**: `/sync-repos setup ~/Popoloto/Repos.nosync/clawclip-build ~/Popoloto/Repos.nosync/clawclip`

**Steps Taken**:
1. Confirm both paths exist and are git repos.
2. Scan clawclip-build for files that should not sync:
   - Found `.env` (secrets)
   - Found `data/` directory (SQLite databases)
   - Found `.claude/` directory (project config)
   - Found `.planning/` directory (internal docs)
   - Found `*.plist` files (macOS service config)
   - Parsed `.gitignore` for additional patterns
3. Generate `sync-public.conf` with detected exclusions.
4. Generate `sync-public.sh` from template.
5. Present both files for review.

**Sample Output**:
```
Sync Repos — Setup
====================

Dev repo:    ~/Popoloto/Repos.nosync/clawclip-build
Public repo: ~/Popoloto/Repos.nosync/clawclip

Detected exclusion patterns:
  .env, .env.*           (secrets)
  data/                  (SQLite databases)
  .claude/               (project config)
  .planning/             (internal docs)
  *.plist                (macOS service config)
  dist/                  (build output)
  node_modules/          (dependencies)
  scripts/sync-public.*  (sync infrastructure)
  CLAUDE_CONTEXT.md      (agent context)

Generated files:
  scripts/sync-public.conf  (exclusion config)
  scripts/sync-public.sh    (sync script)

Review the generated files above. Approve to write them to the dev repo.
```

**User approves. Files written**:
```
[sync-repos] Wrote scripts/sync-public.conf (18 exclusion patterns)
[sync-repos] Wrote scripts/sync-public.sh (chmod +x)
[sync-repos] Setup complete. Run /sync-repos sync to perform the first sync.
```

**Follow-up**: User runs `/sync-repos sync` to perform the initial sync, then `/safe-push` to push the public repo.
