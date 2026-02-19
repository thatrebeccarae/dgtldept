# Architecture Research

**Domain:** Developer tooling catalog with auto-generated static site
**Researched:** 2026-02-19
**Confidence:** HIGH (Astro docs, official SKILL.md spec, Pagefind docs) / MEDIUM (directory structure patterns, build ordering)

---

## Standard Architecture

### System Overview

This system has two distinct layers that must coexist: the **installable skills layer** (files Claude Code users copy to their machines) and the **catalog site layer** (a static website generated from those same files at build time). The single source of truth is the repo.

```
┌──────────────────────────────────────────────────────────────┐
│                     GitHub Repository                         │
│                                                               │
│  skills/          skill-packs/         site/                  │
│  ┌────────────┐   ┌──────────────┐    ┌──────────────────┐   │
│  │ SKILL.md   │   │ SKILL.md     │    │  src/content/    │   │
│  │ REFERENCE  │   │ README.md    │    │  (symlinks or    │   │
│  │ scripts/   │   │ scripts/     │    │   build copy)    │   │
│  │ templates/ │   │ *.env.example│    └────────┬─────────┘   │
│  │ meta.yaml  │   │ meta.yaml    │             │             │
│  └────────────┘   └──────────────┘             │             │
│        │                 │                      │             │
│        └────────┬────────┘                      │             │
│                 │                               │             │
│            SKILL.md + meta.yaml ───────────────►│             │
│            (single source of truth)             │             │
└─────────────────────────────────────────────────┼────────────┘
                                                  │
                                                  ▼
┌──────────────────────────────────────────────────────────────┐
│                    Build Pipeline (CI)                        │
│                                                               │
│  1. collect-metadata.py                                       │
│     Reads SKILL.md + meta.yaml from all skills/skill-packs   │
│     Outputs catalog.json (normalized skill registry)          │
│                                                               │
│  2. astro build                                               │
│     Reads catalog.json via Content Layer                      │
│     Renders catalog index, category pages, skill detail pages │
│     Outputs dist/ (static HTML/CSS/JS)                        │
│                                                               │
│  3. pagefind --site dist/                                      │
│     Indexes rendered HTML                                      │
│     Outputs dist/pagefind/ (search index bundles)             │
│                                                               │
│  4. deploy to GitHub Pages                                     │
└──────────────────────────────────────────────────────────────┘
                          │
                          ▼
             ┌────────────────────────┐
             │   Static Catalog Site  │
             │   (GitHub Pages)       │
             │                        │
             │  /                     │
             │  /skills/[slug]        │
             │  /category/[name]      │
             │  /search               │
             └────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Communicates With |
|-----------|----------------|-------------------|
| `SKILL.md` (per skill) | Claude Code entry point; name + description only per official spec | Claude Code runtime, build pipeline (read-only) |
| `meta.yaml` (per skill) | Extended catalog metadata: category, tags, complexity, prerequisites, platforms | Build pipeline only; not read by Claude |
| `collect-metadata.py` | Walks repo, merges SKILL.md frontmatter + meta.yaml, outputs catalog.json | Reads skills/ and skill-packs/; writes catalog.json to site/src/data/ |
| `catalog.json` | Normalized registry of all skills (name, slug, category, tags, description, complexity, install path, platforms) | Consumed by Astro Content Layer |
| Astro site (`site/`) | Renders catalog index, category pages, skill detail pages from catalog.json | Reads catalog.json; outputs dist/ |
| Pagefind | Indexes rendered HTML at build time; serves search at runtime with no server | Runs after astro build; adds dist/pagefind/ bundle |
| GitHub Actions workflow | Orchestrates: collect → build → index → deploy | Triggers on push to main |

---

## Recommended Project Structure

The current repo puts all installable skill content at the root. The site needs to be a separate directory that does NOT get installed by users. A `site/` subdirectory keeps the two concerns cleanly separated.

```
claude-code-skills/
│
├── skills/                          # Individual installable skills (unchanged for users)
│   └── {skill-name}/
│       ├── SKILL.md                 # Claude Code entry point (name + description only)
│       ├── meta.yaml                # Catalog metadata (category, tags, complexity, etc.)
│       ├── REFERENCE.md
│       ├── scripts/
│       ├── templates/
│       └── assets/
│
├── skill-packs/                     # Skill bundles (unchanged for users)
│   └── {pack-name}/
│       ├── README.md
│       ├── meta.yaml                # Pack-level catalog metadata
│       ├── scripts/setup.py
│       └── {skill-name}/
│           ├── SKILL.md
│           ├── meta.yaml            # Skill-level catalog metadata within pack
│           └── ...
│
├── site/                            # Static catalog site (not installed by users)
│   ├── astro.config.ts
│   ├── package.json
│   ├── src/
│   │   ├── content.config.ts        # Astro Content Layer schema definition
│   │   ├── data/
│   │   │   └── catalog.json         # Generated by collect-metadata.py (gitignored or committed)
│   │   ├── pages/
│   │   │   ├── index.astro          # Catalog home — all skills, filter controls
│   │   │   ├── skills/
│   │   │   │   └── [slug].astro     # Dynamic per-skill detail page
│   │   │   └── category/
│   │   │       └── [name].astro     # Dynamic per-category listing page
│   │   ├── components/
│   │   │   ├── SkillCard.astro
│   │   │   ├── CategoryFilter.astro
│   │   │   └── SearchBar.astro
│   │   └── layouts/
│   │       └── Layout.astro
│   └── public/
│       └── (static assets: favicon, OG images)
│
├── scripts/                         # Repo-level utilities (not skill scripts)
│   └── collect-metadata.py          # Walks skills/ + skill-packs/, outputs catalog.json
│
├── .github/
│   └── workflows/
│       └── deploy-site.yml          # CI: collect → build → pagefind → deploy
│
├── README.md
└── .planning/
```

### Structure Rationale

- **`site/` isolation:** Users copy skills from `skills/` and `skill-packs/`. They never touch `site/`. This avoids confusion and keeps npm/node out of the skill installation path.
- **`meta.yaml` per skill, separate from `SKILL.md`:** The official SKILL.md spec (confirmed at agentskills.io/specification and anthropics/skills) only allows `name`, `description`, `license`, `allowed-tools`, and `metadata` in SKILL.md frontmatter. Adding custom catalog fields causes validation errors in Claude Code. A separate `meta.yaml` sidesteps this constraint cleanly.
- **`collect-metadata.py` as adapter:** This script is the single place that knows about both the skill file structure and the site's data format. If either changes, only this script needs updating.
- **`catalog.json` as intermediate artifact:** Decouples the metadata collection step from the Astro build. The JSON file can be inspected, diffed, and validated independently.

---

## Architectural Patterns

### Pattern 1: Sidecar Metadata File

**What:** Every skill has a `SKILL.md` (for Claude Code) and a `meta.yaml` (for the catalog). They live in the same directory but serve different consumers.

**When to use:** When the consumer of content (Claude Code) has a strict schema that can't accommodate extra fields.

**Trade-offs:**
- Pro: No contamination of functional files with catalog concerns. SKILL.md stays valid per spec.
- Pro: meta.yaml can evolve independently as catalog needs change.
- Con: Two files to maintain per skill. Requires discipline to keep them in sync.
- Con: A skill without a meta.yaml is silently excluded from the catalog unless the collector treats absence as an error.

**Example meta.yaml:**
```yaml
category: auditing
tags:
  - linkedin
  - data-viz
  - analytics
complexity: intermediate
platforms:
  - all
prerequisites:
  - python 3.9+
  - linkedin data export
install_path: skills/linkedin-data-viz
pack: null
featured: false
```

### Pattern 2: Two-Step Build (Collect Then Render)

**What:** The build pipeline runs in two explicit phases: (1) a Python script that collects and normalizes metadata into a JSON file, and (2) Astro that consumes that JSON to render pages.

**When to use:** When source content is spread across a non-standard directory layout that a generic SSG loader can't traverse on its own.

**Trade-offs:**
- Pro: Each step is testable independently. The collector can be run locally and the output inspected.
- Pro: If the site framework changes (Astro → Hugo), only the Astro step changes; the collector stays.
- Con: One extra artifact (catalog.json) to manage.
- Con: The collector must be kept in sync with changes to the skills directory structure.

### Pattern 3: Post-Build Search Indexing with Pagefind

**What:** Run `pagefind --site dist/` after `astro build` completes. Pagefind reads the rendered HTML, builds a static search index, and writes it into `dist/pagefind/`. No server required.

**When to use:** Always for a static site catalog — it's the correct pattern for 2025. Avoid client-side JS search (Fuse.js, lunr) for anything over ~200 entries.

**Trade-offs:**
- Pro: Zero infrastructure. Search index lives alongside static files.
- Pro: Pagefind indexes rendered HTML, so search results reflect what the user actually sees.
- Con: Search index is built from HTML, not from raw metadata. Metadata fields not rendered on the page are not searchable.
- Con: Requires an extra build step and ordering: astro build MUST finish before pagefind runs.

---

## Data Flow

### Build-Time Data Flow (repo → site)

```
skills/*/SKILL.md              ─┐
skills/*/meta.yaml             ─┤
skill-packs/*/meta.yaml        ─┤─► collect-metadata.py ─► catalog.json
skill-packs/*/*/SKILL.md       ─┤
skill-packs/*/*/meta.yaml      ─┘

catalog.json ─► Astro Content Layer (content.config.ts schema + Zod validation)
             ─► getCollection("skills") in pages/index.astro
             ─► getStaticPaths() in pages/skills/[slug].astro ─► /skills/{slug}.html
             ─► getStaticPaths() in pages/category/[name].astro ─► /category/{name}.html

dist/ (rendered HTML) ─► pagefind --site dist/ ─► dist/pagefind/ (search index)

dist/ + dist/pagefind/ ─► GitHub Pages deployment
```

### Runtime Data Flow (user → site)

```
User visits /                    ─► index.astro (all skills, category filter)
User clicks category filter      ─► client-side JS filters SkillCard components
                                    (no server round-trip — all cards pre-rendered)

User types in search             ─► Pagefind JS client queries dist/pagefind/ index
                                 ─► Returns matching skill pages
                                 ─► Renders results inline (no server)

User visits /skills/linkedin-data-viz  ─► pre-rendered static page
                                       ─► Shows: description, category, tags,
                                          complexity, prerequisites, install command
```

### Key Data Flows

1. **Metadata propagation:** SKILL.md name+description + meta.yaml category/tags/complexity → catalog.json entry → Astro page props → rendered HTML → Pagefind index → search results
2. **Install command generation:** `install_path` in meta.yaml + skill slug → Astro renders `cp -r {install_path} ~/.claude/skills/` as a copyable code block on the detail page — no manual maintenance of install docs
3. **Category filtering:** Tags and category in catalog.json → Astro renders data attributes on SkillCard HTML elements → client-side JS reads data attributes to filter without a page reload

---

## Suggested Build Order

Dependencies determine order. Nothing can be skipped.

| Step | Action | Depends On | Output |
|------|--------|------------|--------|
| 1 | Define `meta.yaml` schema | Product decision: what metadata fields matter | Schema doc / example file |
| 2 | Write `collect-metadata.py` | meta.yaml schema, skills/ directory structure | `catalog.json` |
| 3 | Define Astro content schema (`content.config.ts`) | `catalog.json` shape | TypeScript types for skills |
| 4 | Build Astro index and detail pages | Content schema, `getCollection()` | Static HTML pages |
| 5 | Build category filter UI | Index page structure | Filter component |
| 6 | Run Pagefind after build | Rendered HTML in dist/ | Search index |
| 7 | Wire GitHub Actions workflow | All of the above | Automated CI/CD |
| 8 | Add skills to repo with meta.yaml | meta.yaml schema defined | Catalog grows |

**Phase ordering rationale:**
- Steps 1–3 must happen before anything renders. The schema is the foundation.
- Steps 4–5 can happen in parallel once the schema exists.
- Step 6 (Pagefind) must always run after Step 4 (astro build). Running it before produces an empty or stale index.
- Step 7 automates what you've validated manually in steps 1–6. Wire CI after the pipeline works locally.
- Step 8 is ongoing — every new skill needs a `meta.yaml` or the collector should fail loudly.

---

## Anti-Patterns

### Anti-Pattern 1: Extended Frontmatter in SKILL.md

**What people do:** Add `category:`, `tags:`, `complexity:` directly to SKILL.md YAML frontmatter alongside `name` and `description`.

**Why it's wrong:** The official SKILL.md specification (confirmed at agentskills.io and anthropics/skills) only allows `name`, `description`, `license`, `allowed-tools`, and `metadata`. Custom fields cause Claude Code validation errors and may break skill loading in future Claude versions.

**Do this instead:** Sidecar `meta.yaml` in the same directory. The collector merges both sources; SKILL.md stays spec-compliant.

### Anti-Pattern 2: Astro Reads Skills Directly Without a Collection Step

**What people do:** Point Astro's glob loader directly at `skills/*/SKILL.md` and `skill-packs/*/*/SKILL.md` using a wildcard pattern, skip the collection script.

**Why it's wrong:** The skills directory layout is irregular (two levels: individual skills and pack skills). A glob pattern that handles both cases becomes fragile and breaks when new levels are added. More critically, Astro's glob loader reads frontmatter only — it can't merge data from `meta.yaml` sidecars. You lose the sidecar pattern entirely.

**Do this instead:** Keep the two-step build. The Python collector handles path complexity; Astro gets a clean, normalized JSON file.

### Anti-Pattern 3: Running Pagefind Before Astro Build

**What people do:** Order the CI steps as: pagefind → astro build → deploy.

**Why it's wrong:** Pagefind indexes the HTML in `dist/`. If `dist/` doesn't exist yet (or contains a stale previous build), the search index is empty or wrong.

**Do this instead:** `astro build && pagefind --site dist && deploy`. Always in that order.

### Anti-Pattern 4: Client-Side JS Filtering Fetches catalog.json at Runtime

**What people do:** Ship the raw `catalog.json` as a public asset, then have the search/filter UI fetch it via `fetch('/catalog.json')` and filter in JavaScript.

**Why it's wrong:** For a catalog of 50–200 skills, this works but is unnecessary complexity. For a public static site, it also means all catalog metadata (including any internal notes) is exposed directly as JSON, not just what's rendered.

**Do this instead:** Pre-render all skill cards in the index page HTML with data attributes (`data-category`, `data-tags`, `data-complexity`). Client-side filter JS reads `dataset` attributes on existing DOM elements — no fetch required, no extra payload, works offline.

---

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| GitHub Pages | Astro's `withastro/action` GitHub Action builds and deploys `dist/` automatically | Set `site` in astro.config.ts to the GitHub Pages URL; set `base` if deploying to a sub-path like /claude-code-skills |
| Pagefind | CLI run post-build: `pagefind --site dist/` | Add `astro-pagefind` npm package for local dev; run CLI in CI |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| `skills/` + `skill-packs/` ↔ `collect-metadata.py` | Filesystem reads (SKILL.md, meta.yaml) | Collector is read-only; never writes to skills directories |
| `collect-metadata.py` ↔ `site/src/data/` | Writes `catalog.json` | catalog.json can be committed to repo or generated fresh in CI — both work; CI-generated avoids stale data |
| `site/` ↔ Astro build | Astro reads `catalog.json` via content.config.ts, builds dist/ | Astro never reads from `skills/` directly |
| Astro dist/ ↔ Pagefind | Pagefind reads HTML files in dist/ | Pagefind output goes back into dist/pagefind/ — both then deploy together |

---

## Scalability Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 1–50 skills | Current pattern is sufficient. All page rendering at build time, all filtering in client JS on DOM attributes. |
| 50–200 skills | Pagefind handles search well at this scale. Client-side filter on pre-rendered cards still fast. Consider adding a dedicated search page. |
| 200+ skills | Pagefind still works (it's designed for large sites). Client-side DOM filter may feel sluggish at 200+ visible cards — add server-side pre-filtering via URL query params and Astro's static path generation. |

**First bottleneck:** Build time for Astro if skills grow to hundreds. Mitigation: Astro 5 Content Layer caches between builds — incremental builds are fast even for large collections.

**Second bottleneck:** catalog.json becomes large and slow to parse if skills grow to thousands (not a realistic near-term concern for this project).

---

## Sources

- Astro Content Collections docs: [https://docs.astro.build/en/guides/content-collections/](https://docs.astro.build/en/guides/content-collections/) — HIGH confidence
- Astro 5 Content Layer announcement: [https://astro.build/blog/content-layer-deep-dive/](https://astro.build/blog/content-layer-deep-dive/) — HIGH confidence
- Pagefind static search: [https://pagefind.app/](https://pagefind.app/) — HIGH confidence
- astro-pagefind integration: [https://github.com/shishkin/astro-pagefind](https://github.com/shishkin/astro-pagefind) — HIGH confidence
- Official SKILL.md spec (agentskills.io): [https://agentskills.io/specification](https://agentskills.io/specification) — HIGH confidence (confirmed allowed fields)
- Anthropics/skills GitHub repo issue confirming validation on frontmatter fields: [https://github.com/anthropics/skills/issues/37](https://github.com/anthropics/skills/issues/37) — HIGH confidence
- withastro/action GitHub Action: [https://github.com/withastro/action](https://github.com/withastro/action) — HIGH confidence
- Skills Hub example (Astro catalog from skills.json): [https://samueltauil.github.io/github-copilot/open-source/developer-tools/2026/02/06/skills-hub-curated-catalog-discovering-installing-ai-coding-skills.html](https://samueltauil.github.io/github-copilot/open-source/developer-tools/2026/02/06/skills-hub-curated-catalog-discovering-installing-ai-coding-skills.html) — MEDIUM confidence (blog post, not official docs)
- Astro GitHub Pages deployment guide: [https://docs.astro.build/en/guides/deploy/github/](https://docs.astro.build/en/guides/deploy/github/) — HIGH confidence

---

*Architecture research for: Claude Code Skills catalog with auto-generated static site*
*Researched: 2026-02-19*
