# Pitfalls Research

**Domain:** Public developer tooling catalog / open-source Claude Code skill registry
**Researched:** 2026-02-19
**Confidence:** MEDIUM-HIGH — Claude Code skills platform verified against official docs (code.claude.com); catalog/registry pitfalls verified across multiple community sources

---

## Critical Pitfalls

### Pitfall 1: Documentation Drift Between Repo and Companion Site

**What goes wrong:**
The static companion site is generated from repo content at build time. When skills are updated in the repo but the site isn't rebuilt, or when site copy is manually edited separately from the source SKILL.md files, the two fall out of sync. Users following install instructions on the website get directions that no longer match the actual skill files. This is the "documentation drift" failure mode that plagues most developer tool catalogs.

**Why it happens:**
Teams add a manual "polish" step to site content — rewriting descriptions, adding screenshots, tweaking install steps. These edits happen in the site layer, not the source. Within weeks, the site is a separate document with its own stale facts.

**How to avoid:**
- Enforce a strict single source of truth: all user-visible content lives in SKILL.md and README.md files in the repo. The site renders these files verbatim or via structured metadata — never manually edited copy.
- Every skill must have a metadata frontmatter block (name, description, prerequisites, complexity, tags) that the static generator uses directly. No parallel content.
- Add a build check: if the site cannot be fully regenerated from repo content alone, the build fails.

**Warning signs:**
- Anyone edits site content in the site layer (not the repo)
- Site has more descriptive text than the corresponding SKILL.md
- You find yourself "updating the website" as a separate task from updating the skill

**Phase to address:**
Phase 1 (repo structure and schema) — establish the metadata schema before any site generation begins. Locking the SSOT contract early prevents the "we'll fix it later" drift.

---

### Pitfall 2: Breaking Existing Skills During Restructure

**What goes wrong:**
The repo restructure (moving from flat skills/ layout to workflow-based organization) changes file paths. Anyone who installed a skill by cloning the repo and pointing to its path now has a broken reference. Existing skill pack setup scripts that hardcode paths silently fail after the move. The original Klaviyo skill pack, LinkedIn viz skill, and pro deck builder are all at risk.

**Why it happens:**
Brownfield restructures optimistically assume "nobody has the old paths memorized" — but in a public repo, even a handful of users who starred it and cloned it three months ago will have old paths. More importantly, your own existing setup scripts have hardcoded paths.

**How to avoid:**
- Audit every existing script and SKILL.md for hardcoded paths before restructuring.
- Create redirect/alias files at old paths that point to new locations (or at minimum a README.md stub explaining the move).
- Version the restructure as a breaking change: tag the old structure as v0.x before creating the new layout, so old clone references still work.
- Document migration steps in CHANGELOG.md with explicit before/after path mappings.

**Warning signs:**
- You start renaming directories without checking existing setup scripts first
- No CHANGELOG.md exists at time of restructure
- Setup scripts use absolute or relative paths to skill files rather than reading from a config

**Phase to address:**
Phase 1 (repo restructure) — the restructure phase itself is the moment of maximum breaking-change risk. Compatibility checking must be a gate, not an afterthought.

---

### Pitfall 3: Scope Creep Into Platform Building

**What goes wrong:**
The project starts as a curated catalog of skills. Then comes: "we should have a search API," "we need user accounts to save favorites," "we need automated skill testing in CI," "we need a submission portal for community contributions." Each addition seems reasonable in isolation. Six months in, you're building and maintaining a platform instead of shipping skills. The skills catalog — the actual product — stagnates while infrastructure expands.

**Why it happens:**
This is the most documented anti-pattern in developer platform engineering. The IDP (Internal Developer Platform) community has named it explicitly: teams treat platforms as infrastructure projects rather than products, and scope expands because "it would be nice to have" beats "this serves users." With a static catalog + companion site, every dynamic feature request is a scope explosion.

**How to avoid:**
- The out-of-scope list in PROJECT.md is the primary defense. Enforce it explicitly.
- Static site constraint is non-negotiable: if a feature requires server-side code, an API, or a database, it's out of scope for v1.
- Community contributions deferred to v2 is a hard line. The submission portal, review queue, and contribution guide are a separate milestone.
- Every new idea goes on a backlog with explicit "not before v2" labels.

**Warning signs:**
- Any PR or task that adds server-side infrastructure
- Discussion of "automated skill validation" or "CI testing for skills"
- "We should let people submit skills" before v1 is shipped
- The companion site gains features not in the original static site spec

**Phase to address:**
Every phase — this pitfall has no natural endpoint. The scope constraint needs to be actively re-affirmed at the start of each phase.

---

### Pitfall 4: Install Friction Killing Non-Technical Adoption

**What goes wrong:**
34.7% of developers abandon a tool if setup is difficult. For non-technical marketers, the threshold is lower and the tolerance for ambiguity is near zero. Skills with unclear prerequisites, multi-step install processes, or "you should know what a dotfile is" assumptions will be ignored by the target audience. The skills may work perfectly — and nobody uses them.

**Why it happens:**
Skills are built by someone who already has Claude Code installed, understands ~/.claude/skills/, and has a working terminal. Documentation written from that mental model is incomprehensible to someone whose version of "technical" is "I've heard of git." The gap between builder context and user context is invisible to the builder.

**How to avoid:**
- Every skill needs a per-skill README with a non-technical-friendly install section written for someone who has never used a terminal.
- Define the prerequisite stack explicitly (Claude Code installed, subscription level, OS requirements) before any install steps.
- Use the complexity metadata field to help users self-select: "Beginner / Intermediate / Advanced" with honest descriptions of what each requires.
- Test install docs with an actual non-technical person before publishing a skill. If they get stuck, the docs are wrong — the user is not.
- The companion website's primary job is reducing install friction: step-by-step guides with screenshots, copy-paste commands, and "what you'll need first" sections.

**Warning signs:**
- Install docs start with "clone the repo to ~/.claude/skills/" without explaining what that means
- Prerequisites are listed without versions or links
- "Technical" users review install docs but non-technical users never do
- Skills are published with placeholder docs ("TBD" or "see SKILL.md for details")

**Phase to address:**
Phase 2 (per-skill documentation template) — the doc template itself must enforce the non-technical section. If the template doesn't require it, it won't get written.

---

### Pitfall 5: Context Budget Overload From Over-Bundling Skills

**What goes wrong:**
Claude Code loads skill descriptions into context to know what's available. The budget is 2% of the context window (approximately 16,000 characters fallback). Skill packs that bundle many skills together — or skills with verbose SKILL.md files — silently hit this limit. Skills beyond the budget are excluded from Claude's awareness without clear user feedback. Users install a skill pack expecting 8 skills to work and only 5 respond.

**Why it happens:**
The context budget limit is not surfaced prominently to skill authors. Authors optimize SKILL.md for clarity and completeness — longer descriptions, detailed examples, multi-step instructions — without knowing they're contributing to a shared budget problem. Skill packs (bundling related skills together) are particularly high-risk.

**How to avoid:**
- Keep SKILL.md files under 500 lines (Anthropic's documented recommendation).
- Use supporting files for detail: move examples, reference docs, and scripts out of SKILL.md and into skill subdirectories, referenced from SKILL.md.
- The description frontmatter field should be one or two sentences, not a paragraph — it's always in context, even when the skill isn't active.
- Document the context budget constraint in the skill authoring guide for this repo.
- For skill packs, test the full pack installed simultaneously and run /context to verify no skills are excluded.

**Warning signs:**
- SKILL.md files exceeding 500 lines
- Skill descriptions in frontmatter longer than two sentences
- Skill packs with more than 5-6 bundled skills
- Users report that some skills "don't respond" despite installation

**Phase to address:**
Phase 1 (skill metadata schema) — bake the length constraints into the SKILL.md template so authors hit the guardrails during authoring, not after publication.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Skip frontmatter metadata schema for first few skills | Ship faster | Skills can't be filtered, indexed, or queried by the static site generator — requires retroactive migration | Never; schema should be defined before any skill is published |
| Write skill docs for technical users only | Faster to write | Non-technical audience excluded; install support burden increases | Never for this project's stated audience range |
| Hardcode install paths in setup scripts | Works immediately | Breaks on repo restructure; brittle across OS environments | Never |
| Manually duplicate content between repo and website | Quick customization of site copy | Drift begins immediately; maintenance doubles | Never; SSOT is non-negotiable |
| Defer CHANGELOG.md until "things are stable" | Save time | No migration path for early adopters when restructure happens | Never for a public repo |
| Use `disable-model-invocation: false` on all skills by default | Skills trigger automatically | Skills with side effects or external API calls fire unexpectedly; user trust damage | Only for pure reference/knowledge skills with no side effects |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Static site generator reading SKILL.md | Parse markdown as free text and display verbatim | Define a strict YAML frontmatter schema; generate site from structured metadata + render markdown body separately |
| GitHub Actions for site build | Build only on main branch push | Build and preview on PRs too, so authors can verify site output before merge |
| Existing setup scripts (Klaviyo pack, LinkedIn viz) | Assume paths are stable during restructure | Inventory all path references in scripts before restructuring; update atomically |
| Claude Code skills installation | Assume ~/.claude/skills/ exists on user machines | Installation docs must include directory creation step; don't assume any dotfiles exist |
| Supporting files in skill directories | Reference files with absolute paths | Use relative paths from SKILL.md; skills are intended to be portable |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Too many skills in one pack | Some skills don't respond; /context shows excluded skills | Keep packs focused; stay under context budget; use supporting files for bulk content | At approximately 8+ densely-described skills in a single install set |
| Verbose SKILL.md descriptions | Context fills up faster than expected; unrelated skills get crowded out | Strict line limit (500); move detail to supporting files | As soon as description frontmatter exceeds 2-3 sentences per skill |
| Static site built from free-form markdown | Site content drifts from repo; metadata inconsistent | Enforce YAML frontmatter schema; site generator parses schema fields | First time someone edits site content without updating SKILL.md |
| No skill versioning scheme | Users can't know if an installed skill is current | Define a version field in frontmatter from day one; document in CHANGELOG.md | First significant skill update — users can't self-diagnose "am I on the latest version?" |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Organizing catalog by platform (Klaviyo, GA4, etc.) rather than workflow | Marketers who don't know tool names can't find relevant skills | Organize by workflow (auditing, reporting, campaign management) matching how marketers think about their jobs |
| One giant README with all skills listed | Users skim, miss relevant skills, give up | Companion website with category filtering; skill-level pages with focused information |
| Technical prerequisites buried in install steps | Non-technical users hit blockers mid-install with no recovery path | Prerequisites section at the very top, before any steps; link to how to get each prerequisite |
| No complexity/difficulty signal on skills | Users attempt advanced skills without readiness | Complexity metadata (Beginner / Intermediate / Advanced) with honest definition of what each requires |
| Blank install instructions for published skills | Users have nothing to go on; trust erodes | Skills gate on documentation completeness before publication — "TBD" docs block publication |
| No "what this does" example output | Users can't evaluate if a skill is worth installing | Each skill README includes one concrete example: input context + what Claude produces |

---

## "Looks Done But Isn't" Checklist

- [ ] **Skill restructure complete:** Verify every existing setup script path still resolves after directory changes — don't assume, test each one
- [ ] **Skill documentation:** "Written" is not the same as "tested with a non-technical user" — verify docs with someone who isn't you
- [ ] **Static site generation:** Confirm the site can be fully rebuilt from scratch from repo content only, with no manual edits required
- [ ] **Context budget:** Install all skills in a pack simultaneously and run /context to verify none are silently excluded
- [ ] **Public safety:** Every committed file must be scrubbed for API keys, client names, proprietary config, and private paths — git history check too, not just HEAD
- [ ] **Metadata schema:** Check that every skill has the full required frontmatter fields; partial metadata breaks site generation or filtering
- [ ] **Companion site discoverability:** Verify skills are findable by workflow category, not just by name — someone shouldn't need to know a skill exists to find it

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Documentation drift (site vs. repo) | HIGH | Audit every site page against its source SKILL.md; decide canonical version; rebuild site from canonical source; enforce SSOT going forward |
| Broken paths from restructure | MEDIUM | Identify all affected paths via git history; create stub redirects at old paths; notify anyone who starred/forked; update CHANGELOG |
| Scope creep into platform | HIGH | Stop all non-catalog work; re-establish out-of-scope list; move in-progress platform features to a v2 milestone; ship the static catalog |
| Install friction causing abandonment | MEDIUM | Rewrite install docs from scratch using non-technical user as test subject; add companion site install guides before re-promoting |
| Context budget overload | LOW-MEDIUM | Identify verbose SKILL.md files; move supporting content to subdirectory files; test again with /context; redocument best practices |
| Public exposure of private data | CRITICAL | Remove from git history (git filter-branch or BFQ); rotate any exposed credentials immediately; audit all other committed files |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Documentation drift (repo vs. site) | Phase 1: Metadata schema and SSOT contract | Can the site regenerate from scratch without any manual edits? |
| Breaking existing skills during restructure | Phase 1: Repo restructure | Do all existing setup scripts still execute without errors? |
| Scope creep into platform building | Every phase (ongoing gate) | Does the PR/task require server-side code, a database, or auth? If yes, defer to v2 |
| Install friction for non-technical users | Phase 2: Per-skill doc template | Can a non-technical person install a skill using only the documentation? |
| Context budget overload | Phase 1: Skill metadata schema + templates | Does /context show all skills present after installing a full pack? |
| Skill docs written for builders, not users | Phase 2: Per-skill doc template | Is there a "Prerequisites" section and a "What you'll see" example in every skill README? |
| Private data in public commits | Phase 1: Before first public push | Has every file been audited for API keys, client names, and private paths — including git history? |
| Missing version scheme | Phase 1: Metadata schema | Does every skill have a version field in frontmatter? Is there a CHANGELOG? |

---

## Sources

- [Extend Claude with skills — official Claude Code docs](https://code.claude.com/docs/en/skills) — HIGH confidence; authoritative source for Claude Code skill mechanics, context budget limits, frontmatter schema, and installation paths (verified February 2026)
- [Claude Skills vs Prompt Libraries 2025: Maintainability & Versioning](https://skywork.ai/blog/ai-agent/claude-skills-vs-prompt-libraries-2025-comparison/) — MEDIUM confidence; covers versioning and rollback challenges
- [7 Common IDP Implementation Pitfalls](https://securityboulevard.com/2025/12/7-common-idp-implementation-pitfalls-and-how-to-avoid-them/) — MEDIUM confidence; scope creep, over-engineering, and adoption failure patterns in developer tool platforms
- [What 202 Open Source Developers Taught Us About Tool Adoption](https://www.catchyagency.com/post/what-202-open-source-developers-taught-us-about-tool-adoption) — MEDIUM confidence; 34.7% abandonment rate for difficult setup; five-minute benchmark
- [9 Platform Engineering Anti-Patterns That Kill Adoption](https://jellyfish.co/library/platform-engineering/anti-patterns/) — MEDIUM confidence; platform-as-infrastructure vs. platform-as-product failure mode
- [awesome-claude-skills GitHub repositories](https://github.com/travisvn/awesome-claude-skills) — LOW-MEDIUM confidence; community patterns in how skill catalogs are structured and where they encounter problems
- [Build a Governed AI Prompt Library for Marketing Teams — Everworker](https://everworker.ai/blog/governed_ai_prompt_library_marketing) — MEDIUM confidence; governance and discoverability patterns for non-technical marketing audiences
- [How open source service catalogs changed in 2025 — Port.io](https://www.port.io/blog/open-source-service-catalogs) — MEDIUM confidence; manual-update burden and metadata drift in catalog projects
- [Claude Code Troubleshooting Guide — ClaudeLog](https://claudelog.com/troubleshooting/) — LOW-MEDIUM confidence; installation and path issue patterns

---
*Pitfalls research for: Public Claude Code skills catalog for marketing teams*
*Researched: 2026-02-19*
