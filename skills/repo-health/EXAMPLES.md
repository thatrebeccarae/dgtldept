# Repo Health Examples

Practical examples showing repo-health audit output for different scenarios.

## Example 1: New Public Repo (Low Score)

**User Request**: `/repo-health ~/Popoloto/Repos.nosync/my-new-tool`

A freshly created public repo with only source code committed. No standard files, no GitHub configuration.

**Output**:
```
=== Repo Health Report: my-new-tool ===
Visibility: public
Overall Score: 22/100 (Grade: F)

--- Standard Files (30%) --- Score: 20/100
  [PASS] .gitignore
  [MISS] LICENSE
  [MISS] SECURITY.md
  [MISS] CONTRIBUTING.md
  [MISS] CODEOWNERS
  [MISS] .editorconfig
  [MISS] .github/pull_request_template.md
  [MISS] .github/ISSUE_TEMPLATE/
  [MISS] CHANGELOG.md
  [MISS] CODE_OF_CONDUCT.md

--- GitHub Config (15%) --- Score: 0/100
  [FAIL] Description: not set
  [FAIL] Topics: none set
  [PASS] Default branch: main
  [FAIL] Branch protection: not enabled

--- Documentation (25%) --- Score: 20/100
  [PASS] README.md (8 lines)
  [WARN] README is a stub (< 10 lines)
  [WARN] No install/setup instructions found
  [WARN] No license reference in README
  [MISS] CHANGELOG.md

--- Code Hygiene (20%) --- Score: 60/100
  [PASS] No tracked .env files
  [PASS] No large binary files tracked
  [WARN] No package-lock.json (package.json exists)
  [PASS] No stale branches

--- Community (10%) --- Score: 0/100
  [MISS] CODE_OF_CONDUCT.md
  [MISS] CONTRIBUTING.md
  [MISS] Issue templates
  [MISS] PR template

=== Prioritized Fixes ===
1. [HIGH] Add LICENSE — legally required for open-source distribution. MIT recommended.
2. [HIGH] Add SECURITY.md — required for public repos accepting contributions.
3. [HIGH] Set repository description — currently empty.
4. [HIGH] Add 3+ repository topics — improves discoverability.
5. [MED]  Expand README.md — add project description, install instructions, usage examples.
6. [MED]  Add CONTRIBUTING.md — guides external contributors on your workflow.
7. [MED]  Enable branch protection on main — prevents accidental force pushes.
8. [MED]  Add CHANGELOG.md — track releases for users.
9. [LOW]  Add .editorconfig — ensures consistent formatting across contributors.
10.[LOW]  Add CODE_OF_CONDUCT.md — signals a welcoming community.
11.[LOW]  Add issue templates — structured bug reports and feature requests.
12.[LOW]  Add PR template — consistent pull request descriptions.
13.[LOW]  Commit package-lock.json — ensures reproducible installs.

Run /repo-health ~/Popoloto/Repos.nosync/my-new-tool --fix to auto-generate missing files.
```

## Example 2: Mature Public Repo (High Score)

**User Request**: `/repo-health ~/Popoloto/Repos.nosync/aouda`

A well-maintained public repo with most standard files in place.

**Output**:
```
=== Repo Health Report: aouda ===
Visibility: public
Overall Score: 85/100 (Grade: B)

--- Standard Files (30%) --- Score: 80/100
  [PASS] .gitignore
  [PASS] LICENSE (MIT)
  [PASS] SECURITY.md
  [PASS] CONTRIBUTING.md
  [MISS] CODEOWNERS
  [PASS] .editorconfig
  [PASS] .github/pull_request_template.md
  [PASS] .github/ISSUE_TEMPLATE/ (2 templates)
  [MISS] CHANGELOG.md
  [PASS] CODE_OF_CONDUCT.md

--- GitHub Config (15%) --- Score: 100/100
  [PASS] Description: "Autonomous AI agent with taste, memory, and goals"
  [PASS] Topics: ai-agent, typescript, autonomous, llm (4 topics)
  [PASS] Default branch: main
  [PASS] Branch protection: enabled (1 review required)

--- Documentation (25%) --- Score: 80/100
  [PASS] README.md (187 lines)
  [PASS] Has project description
  [PASS] Has install/setup instructions
  [PASS] Has license reference
  [MISS] CHANGELOG.md
  [WARN] README has no "Why I Built This" section (run /github:readme audit for details)

--- Code Hygiene (20%) --- Score: 80/100
  [PASS] No tracked .env files
  [PASS] No large binary files tracked
  [PASS] package-lock.json present
  [WARN] 2 stale branches: feature/old-plugin (4 months), experiment/v1-api (6 months)

--- Community (10%) --- Score: 100/100
  [PASS] CODE_OF_CONDUCT.md
  [PASS] CONTRIBUTING.md
  [PASS] Issue templates (bug_report.yml, feature_request.yml)
  [PASS] PR template

=== Prioritized Fixes ===
1. [MED]  Add CHANGELOG.md — no changelog found. Start with current version.
2. [MED]  Add CODEOWNERS — auto-assign PR reviewers by file path.
3. [LOW]  Clean up 2 stale branches (feature/old-plugin, experiment/v1-api).
```

## Example 3: Pre-Open-Source Audit (Private to Public)

**User Request**: `/repo-health ~/Popoloto/Repos.nosync/clawclip-build`

Auditing a private repo before making it public. The report highlights everything that needs to be added.

**Output**:
```
=== Repo Health Report: clawclip-build ===
Visibility: private
Overall Score: 58/100 (Grade: F)

NOTE: This repo is currently private. Scoring below uses PUBLIC repo
standards since you indicated you are preparing to open-source it.
Re-run without the public flag to see private-only scoring.

--- Standard Files (30%) --- Score: 40/100
  [PASS] .gitignore
  [PASS] README.md
  [MISS] LICENSE — REQUIRED before open-sourcing
  [MISS] SECURITY.md — REQUIRED before open-sourcing
  [MISS] CONTRIBUTING.md
  [MISS] CODEOWNERS
  [PASS] .editorconfig
  [MISS] .github/pull_request_template.md
  [MISS] .github/ISSUE_TEMPLATE/
  [MISS] CHANGELOG.md
  [MISS] CODE_OF_CONDUCT.md

--- GitHub Config (15%) --- Score: 50/100
  [PASS] Description: "AI-powered project management for Claude Code agents"
  [FAIL] Topics: none set
  [PASS] Default branch: main
  [FAIL] Branch protection: not enabled

--- Documentation (25%) --- Score: 60/100
  [PASS] README.md (94 lines)
  [PASS] Has project description
  [PASS] Has install/setup instructions
  [WARN] No license reference in README (LICENSE file also missing)
  [MISS] CHANGELOG.md

--- Code Hygiene (20%) --- Score: 60/100
  [PASS] No large binary files tracked
  [PASS] package-lock.json present
  [WARN] 5 stale branches (>90 days)
  [FAIL] Tracked .env file: .env.example — review contents before open-sourcing

--- Community (10%) --- Score: 25/100
  [PASS] CONTRIBUTING.md — wait, this is missing
  [MISS] CODE_OF_CONDUCT.md
  [MISS] CONTRIBUTING.md
  [MISS] Issue templates
  [MISS] PR template

=== Pre-Open-Source Checklist ===

MUST DO before making public:
1. [HIGH] Add LICENSE — cannot open-source without one. MIT recommended.
2. [HIGH] Add SECURITY.md — vulnerability reporting process for contributors.
3. [HIGH] Review .env.example — ensure no real credentials, only placeholder values.
4. [HIGH] Run /safe-push scan — check all commit history for PII, secrets, infra details.
5. [HIGH] Set repository topics — add 3+ for discoverability.

SHOULD DO before making public:
6. [MED]  Add CONTRIBUTING.md — tell contributors how to participate.
7. [MED]  Add CHANGELOG.md — document what shipped in each version.
8. [MED]  Enable branch protection on main — prevent accidental force pushes.
9. [MED]  Add PR template — standardize pull request descriptions.
10.[MED]  Add issue templates — structured bug reports and feature requests.

NICE TO HAVE:
11.[LOW]  Add CODE_OF_CONDUCT.md — Contributor Covenant v2.1.
12.[LOW]  Add CODEOWNERS — auto-assign reviewers.
13.[LOW]  Clean up 5 stale branches before going public.

Run /repo-health ~/Popoloto/Repos.nosync/clawclip-build --fix to auto-generate missing files.
```

The pre-open-source audit adds a dedicated checklist section that separates "must do" (legal/security blockers) from "should do" (quality) and "nice to have" (polish). It also flags the need to run `/safe-push` to scan commit history for leaked secrets before the repo becomes publicly visible.
