# Project Research Summary

**Project:** Claude Code Skills — Public Catalog + Companion Static Site
**Domain:** Developer tooling catalog / open-source Claude Code skill registry
**Researched:** 2026-02-19
**Confidence:** MEDIUM

## Executive Summary

This project is a public catalog of tested Claude Code skills organized by marketing workflow, with a companion static site targeting non-technical marketers who would never navigate a GitHub repo directly. Experts building this type of catalog in 2025/2026 converge on Astro + Starlight as the correct framework: islands architecture ships zero JS by default, the Content Layer API was built for file-based content sourcing, and Starlight provides navigation, dark mode, search, and mobile layout out of the box — eliminating weeks of bespoke UI work. The build pipeline follows a two-step pattern: a Python collector normalizes skill metadata into a `catalog.json` intermediate artifact, then Astro consumes that to render static pages. Pagefind runs post-build for zero-server search indexing. GitHub Pages handles hosting with the official `withastro/action` in a two-job CI workflow.

The recommended approach prioritizes schema-first development over site-first development. Every downstream deliverable — the static site, the catalog navigation, the search index, the quality badge — depends on a finalized `meta.yaml` sidecar schema per skill. The SKILL.md spec (confirmed against official Anthropic documentation) only permits `name`, `description`, `license`, `allowed-tools`, and `metadata` fields. All catalog-specific metadata must live in a `meta.yaml` sidecar to avoid Claude Code validation errors. This constraint shapes the entire architecture: the collector merges both sources, Astro sees only normalized JSON, and SKILL.md files remain spec-compliant. The information architecture decision — organizing by marketing workflow rather than by tool name — is the project's primary competitive differentiator and must be finalized before any navigation or URL structure is built.

Critical risks fall into two categories. First, documentation drift: the companion site must be regenerated entirely from repo source files — any manually edited site copy creates parallel maintenance burden that diverges within weeks. Second, scope creep into platform building: user accounts, automated CI testing of skills, submission portals, and search APIs are all anti-features for v1 that appear reasonable in isolation. The out-of-scope line is "if it requires server-side code, a database, or auth, it defers to v2." A third risk specific to this platform is Claude Code's context budget limit (~16,000 characters for skill descriptions). SKILL.md files over 500 lines and skill packs with more than 5-6 densely-described skills silently crowd out other skills from Claude's awareness — users install a pack expecting 8 skills to respond and only 5 do.

## Key Findings

### Recommended Stack

Astro 5.17 + Starlight 0.37.6 is the recommended foundation. Astro 5 compatibility with Starlight was a documented issue through ~0.30.x but is resolved in 0.37.x. Node.js v22 LTS matches the official `withastro/action@v5` default. Zod schema validation is bundled with Astro's Content Layer — no separate install. Pagefind 1.4.0 is bundled by Starlight and must NOT be installed separately to avoid version conflicts. GitHub Pages is chosen over Cloudflare Pages or Netlify because the repo is already on GitHub, the official action provides one-config deployment, and GitHub Pages has no bandwidth or build-minute caps for public repos.

**Core technologies:**
- **Astro 5.17+**: Static site framework — zero JS shipped by default; Content Layer API reads file-based content collections; `getStaticPaths()` auto-generates skill pages
- **Starlight 0.37.6**: Documentation theme on Astro — ships navigation, dark mode, accessible typography, mobile nav, and Pagefind search with no configuration
- **Pagefind 1.4.0**: Static full-text search — build-time indexed, zero server required, bundled by Starlight automatically
- **Zod**: Frontmatter schema validation — bundled with Astro, validates at build time so broken metadata fails the build rather than silently rendering bad pages
- **GitHub Pages + `withastro/action@v5`**: Free static hosting with official CI/CD integration; requires Pages source set to "GitHub Actions" in repo settings

See `.planning/research/STACK.md` for full alternatives analysis and version compatibility notes.

### Expected Features

The feature landscape splits clearly between the repo surface (for technical operators who clone and configure) and the companion site surface (for non-technical marketers who need proof before touching a terminal). No competitor — SkillsMP, awesome-claude-code, or Anthropic's official repo — targets the non-technical marketing audience. That gap is the moat.

**Must have (table stakes):**
- Per-skill documentation template with standardized fields (name, one-liner, prerequisites, install command, 3-5 example prompts, last-tested date)
- Copy-paste install commands per skill — users scan for the bash block; prose is skipped
- Workflow-first category taxonomy (auditing, reporting, campaign management, presentation) — defined before any navigation is built
- Tested quality signal per skill ("Last tested: [date] with Claude Code [version]") — the discipline is the differentiator, not the infrastructure
- Static site with category browsing — even minimal beats a flat README for non-technical discovery
- Example prompts per skill — non-technical users cannot reverse-engineer capability from descriptions

**Should have (competitive differentiators):**
- Skill pack concept foregrounded as intentional design (not individual atomic skills like every competitor)
- Live demo links for skills that produce file outputs (HTML visualizations, decks)
- Non-technical onboarding guide with tiered paths (wizard / copy-paste / manual based on skill complexity)
- Search within static site (Pagefind, add when catalog exceeds 15-20 skills)
- Contribution guide with documented quality standards

**Defer (v2+):**
- Setup wizard generalization beyond Klaviyo pack
- Marketing-specific benchmark library
- SKILL.md frontmatter linting in CI
- Community submission portal / review queue
- Rating or review system (sparse at low catalog volume; "tested on" dates are more credible)

See `.planning/research/FEATURES.md` for full competitor analysis and prioritization matrix.

### Architecture Approach

The system has two coexisting layers that must never collapse into each other: the installable skills layer (files users copy to `~/.claude/skills/`) and the catalog site layer (a static website generated from those same files). The single source of truth is the repo. The build pipeline runs in four ordered steps: (1) `collect-metadata.py` walks `skills/` and `skill-packs/`, merges SKILL.md frontmatter with `meta.yaml` sidecars, and outputs `catalog.json`; (2) `astro build` consumes `catalog.json` via the Content Layer and renders the catalog index, category pages, and skill detail pages; (3) `pagefind --site dist/` indexes the rendered HTML; (4) GitHub Actions deploys `dist/` to GitHub Pages. This ordering is non-negotiable — Pagefind must run after Astro build; the collection step must run before Astro.

**Major components:**
1. **`SKILL.md` per skill** — Claude Code entry point; spec-compliant with name + description only; read-only by build pipeline
2. **`meta.yaml` per skill** — Sidecar file with catalog metadata (category, tags, complexity, prerequisites, platforms, install path); not read by Claude Code
3. **`collect-metadata.py`** — Adapter script that merges SKILL.md frontmatter + meta.yaml into normalized `catalog.json`; single place that knows both file structures
4. **`catalog.json`** — Intermediate artifact; decouples collection from rendering; inspectable and diffable independently
5. **Astro site (`site/` subdirectory)** — Isolated from installable skill content; renders catalog index, per-category pages, and per-skill detail pages
6. **Pagefind** — Post-build search indexing; indexes rendered HTML into `dist/pagefind/` bundles; no server required
7. **GitHub Actions workflow** — Orchestrates collect → build → index → deploy on push to main

See `.planning/research/ARCHITECTURE.md` for full data flow diagrams, anti-patterns, and scalability thresholds.

### Critical Pitfalls

1. **Documentation drift between repo and site** — All user-visible content must live in SKILL.md and meta.yaml files. The site renders from structured metadata verbatim. Any manually edited site copy begins drifting from day one. Prevention: if the site cannot be fully regenerated from repo content alone, the build fails.

2. **Breaking existing skills during restructure** — Directory restructuring changes file paths. Existing setup scripts in the Klaviyo pack, LinkedIn viz, and pro deck builder have hardcoded paths that silently fail after a move. Prevention: audit all path references before restructuring; create stub redirects at old paths; tag old structure as v0.x before creating new layout.

3. **Scope creep into platform building** — User accounts, automated CI skill testing, submission portals, and search APIs all appear reasonable in isolation but collectively convert a catalog project into a platform maintenance burden. Prevention: the static site constraint is the gate — if a feature requires server-side code, a database, or auth, it defers to v2. Re-affirm this at every phase.

4. **Install friction killing non-technical adoption** — Skills written from a builder's mental model (assumes dotfile knowledge, terminal comfort, path awareness) are incomprehensible to the target non-technical marketing audience. 34.7% of developers abandon a tool if setup is difficult; the threshold is lower for non-technical users. Prevention: every skill README must have a "Prerequisites" section and a "What you'll see" example; validate install docs with an actual non-technical person.

5. **Context budget overload from over-bundling skills** — Claude Code loads skill descriptions into context with a ~16,000 character budget. Skills beyond the budget are silently excluded. Prevention: SKILL.md files must stay under 500 lines; description frontmatter must be one to two sentences; skill packs should not exceed 5-6 bundled skills; verify with `/context` after installing a full pack.

See `.planning/research/PITFALLS.md` for full recovery strategies and a "looks done but isn't" verification checklist.

## Implications for Roadmap

Based on combined research, the build order is dictated by a hard dependency chain: schema must exist before collection can run, collection must run before Astro can render, Astro must render before Pagefind can index. This maps naturally to four phases.

### Phase 1: Foundation — Schema, Structure, and Safety
**Rationale:** Everything downstream depends on the metadata schema and repo structure decisions made here. The pitfall research is unambiguous: "skip frontmatter metadata schema for first few skills" is listed as "never acceptable." The restructure risk (breaking existing skills) and the public data safety audit also belong here — both must be resolved before public launch.
**Delivers:** Finalized `meta.yaml` schema; SKILL.md authoring constraints documented (500-line limit, 2-sentence description); repo directory structure with `site/` isolation; CHANGELOG.md established; all existing setup scripts audited and updated for new paths; every committed file scrubbed for private data; workflow-first category taxonomy decided (auditing, reporting, campaign management, presentation).
**Addresses:** Per-skill documentation template (fields defined here), workflow-first taxonomy, tested quality signal (ritual documented here)
**Avoids:** Documentation drift (SSOT contract established), breaking existing skills during restructure, context budget overload, private data in public commits

### Phase 2: Content — Per-Skill Documentation
**Rationale:** The static site cannot be built credibly before the skill documentation is standardized. Building the site against inconsistent docs means rebuilding it after docs are finalized. Features research confirms the dependency explicitly: "static site requires per-skill docs template first."
**Delivers:** Per-skill README template with enforced sections (Prerequisites, Install command, Example prompts, What you'll see, Last tested date, Demo link field); all existing skills migrated to template; copy-paste install commands standardized across skills; complexity ratings (Beginner/Intermediate/Advanced) applied; non-technical install validation done for at least one skill.
**Addresses:** Table stakes features (copy-paste install, prerequisites, example prompts, changelog/last-updated), non-technical onboarding path
**Avoids:** Install friction killing non-technical adoption, skill docs written for builders not users

### Phase 3: Site — Static Catalog with Category Browsing
**Rationale:** Site builds against the normalized `catalog.json` produced by the collection script. Schema is finalized (Phase 1), docs are standardized (Phase 2), so Astro has clean input data. Building in this order means no retroactive page restructuring.
**Delivers:** `collect-metadata.py` script; `catalog.json` generation; Astro + Starlight site in `site/` subdirectory; catalog index page with pre-rendered skill cards and data attributes for client-side filtering; per-skill detail pages at `/skills/[slug]`; per-category pages at `/category/[name]`; Pagefind search index; GitHub Actions CI/CD workflow (`withastro/action@v5`); deployed to GitHub Pages.
**Uses:** Astro 5.17, Starlight 0.37.6, Pagefind 1.4.0, Zod, Node 22, `withastro/action@v5`
**Implements:** Two-step build (collect then render), sidecar metadata pattern, post-build search indexing, data-attribute filtering (no fetch at runtime)
**Avoids:** Extending SKILL.md frontmatter beyond spec (use meta.yaml instead), Astro reading skills directly without collector, Pagefind running before Astro build, client-side fetch of catalog.json at runtime

### Phase 4: Polish — Differentiators and Discovery
**Rationale:** Once the catalog is live and the structure is validated with real users, add the features that make it competitive: live demo links for skills with file outputs, a non-technical "which skill do I need?" guide, and a contribution quality standard. These are P2 features that require the site to be working first.
**Delivers:** Live demo links added to qualifying skills (HTML output skills first); "Which skill do I need?" plain-English decision guide; contribution guide with quality standards and testing ritual; search within static site validated at current skill count; optional: skill pack landing pages foregrounding the grouped-skill concept.
**Addresses:** Live demo links (P2), non-technical onboarding guide (P2), contribution guide (P2), skill pack concept foregrounded as design

### Phase Ordering Rationale

- Schema before site: every downstream component (collector, Astro content schema, search index, category navigation) is built against the metadata schema. Changing the schema after Phase 3 requires updating four components simultaneously.
- Docs before site: the site renders what the docs contain. Standardizing docs first means the site structure is built for accurate, complete content rather than retrofitted.
- Site before polish: live demo links need hosted outputs; the contribution guide needs a working catalog to describe; the "which skill" guide needs real skills to reference.
- Repo restructure in Phase 1: brownfield restructure risk is highest here. Doing it first, before any site code references skill paths, keeps the blast radius small.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3 (Static Site Build):** The two-step build pipeline (Python collector + Astro) is documented in research but specific implementation details around glob patterns, Astro Content Layer JSON source configuration, and Pagefind custom attribute indexing will benefit from targeted research before implementation begins.
- **Phase 1 (SKILL.md spec validation):** The official SKILL.md frontmatter field list is confirmed from `agentskills.io/specification` and a GitHub issue, but the exact behavior of the `metadata` field (whether nested custom keys under `metadata:` are permitted) should be verified before finalizing the sidecar vs. inline decision.

Phases with standard patterns (skip research-phase):
- **Phase 2 (Per-skill documentation):** This is a writing and templating task. Patterns are clear and well-established; no technical unknowns.
- **Phase 4 (Polish):** Adding demo links and contribution guides are content tasks. Astro patterns for these are fully covered in Phase 3 research.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | MEDIUM | Astro + Starlight core confirmed via official docs and release notes. Starlight + Astro 5 compatibility resolved in 0.37.x but exact version of resolution is ambiguous; verify with `npm create astro@latest -- --template starlight` before committing. Pagefind version inside Starlight bundle not pinned in research — check Starlight changelog. |
| Features | MEDIUM-HIGH | Table stakes features verified against direct observation of VS Code, Obsidian, Raycast, npm, and Homebrew catalogs. Differentiators are synthesis-level conclusions. SkillsMP quality gap corroborated by multiple secondary sources. |
| Architecture | HIGH | Two-step build pattern, sidecar meta.yaml, Pagefind post-build indexing, and GitHub Pages deployment are all confirmed against official Astro, Pagefind, and GitHub documentation. SKILL.md spec field validation confirmed via Anthropic's skills repo issue tracker. |
| Pitfalls | MEDIUM-HIGH | Context budget limit confirmed via official Claude Code docs. Install friction abandonment rate (34.7%) from a single primary source. Documentation drift and scope creep patterns corroborated by IDP and open-source service catalog literature. |

**Overall confidence:** MEDIUM

### Gaps to Address

- **`metadata:` field behavior in SKILL.md:** The spec allows a `metadata` key in SKILL.md frontmatter. It's unclear whether arbitrary nested keys under `metadata:` are permitted (which would eliminate the need for a sidecar `meta.yaml`). Verify against `agentskills.io/specification` and test during Phase 1 before finalizing the architecture pattern. If nested metadata keys work, the sidecar approach may be unnecessary complexity.
- **Starlight + Astro 5 exact compatibility version:** Research cites "~0.30.x" as the range where Astro 5 issues were resolved but does not pin the exact version. Run `npm create astro@latest -- --template starlight` at Phase 3 start to confirm current compatible pair.
- **Existing skill count and directory structure:** Research assumes ~5-15 skills based on known Klaviyo pack + LinkedIn viz + pro deck builder. The actual file tree and setup script path inventory has not been enumerated. Phase 1 must begin with a full audit.
- **Non-technical user testing:** The install friction pitfall recommends testing docs with an actual non-technical person. No such test has been done yet. Phase 2 must include this as a gate before skills are considered "done."

## Sources

### Primary (HIGH confidence)
- Astro 5 Content Collections docs — https://docs.astro.build/en/guides/content-collections/
- Astro 5 Content Layer deep dive — https://astro.build/blog/content-layer-deep-dive/
- Starlight official docs — https://starlight.astro.build/
- Pagefind documentation — https://pagefind.app/
- Official SKILL.md specification — https://agentskills.io/specification
- Anthropic/skills GitHub repo issue #37 (frontmatter validation) — https://github.com/anthropics/skills/issues/37
- Extend Claude with skills — Claude Code official docs — https://code.claude.com/docs/en/skills
- withastro/action GitHub Action — https://github.com/withastro/action
- Astro GitHub Pages deployment guide — https://docs.astro.build/en/guides/deploy/github/
- VS Code Extension Marketplace docs — https://code.visualstudio.com/docs/configure/extensions/extension-marketplace
- Raycast prepare extension for store — https://developers.raycast.com/basics/prepare-an-extension-for-store
- Homebrew Taps official docs — https://docs.brew.sh/Taps

### Secondary (MEDIUM confidence)
- Starlight 0.37.6 release notes — https://github.com/withastro/starlight/releases
- Astro 5.17 release — https://astro.build/blog/whats-new-january-2026/
- SkillsMP review (signal-to-noise criticism) — https://medium.com/ai-software-engineer/skillsmp-this-87-427-claude-code-skills-directory-just-exploded-but-with-one-annoying-problem-ec4af66b78cb
- awesome-claude-code repo (structure observation) — https://github.com/hesreallyhim/awesome-claude-code
- IDP implementation pitfalls (scope creep patterns) — https://securityboulevard.com/2025/12/7-common-idp-implementation-pitfalls-and-how-to-avoid-them/
- Tool adoption abandonment rate study — https://www.catchyagency.com/post/what-202-open-source-developers-taught-us-about-tool-adoption
- Open source service catalogs and metadata drift — https://www.port.io/blog/open-source-service-catalogs
- npm search experience and quality signals — https://socket.dev/blog/npm-updates-search-experience
- Obsidian plugin stats — https://www.obsidianstats.com

### Tertiary (LOW confidence)
- VitePress vs. Docusaurus vs. MkDocs comparison 2025 — https://okidoki.dev/documentation-generator-comparison (single source; directional only)
- Skills Hub Astro catalog example — blog post, not official docs
- Claude Code troubleshooting — https://claudelog.com/troubleshooting/ (community, not official)

---
*Research completed: 2026-02-19*
*Ready for roadmap: yes*
