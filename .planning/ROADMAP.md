# Roadmap: Claude Code Skills

## Overview

Build a public catalog of tested Claude Code skills organized by marketing workflow, complete with a static companion website that lets non-technical marketers discover and install skills without navigating a GitHub repo. The work proceeds in three phases: establish the repo structure and metadata schema that everything depends on, produce public-ready skills with complete documentation, then generate the static site and CI/CD pipeline from that content.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Foundation** - Repo structure, metadata schema, workflow taxonomy, and root documentation
- [ ] **Phase 2: Skills** - Public-ready skills with standardized docs, quality signals, and install commands
- [ ] **Phase 3: Site** - Static catalog site with category browsing, search, and automated CI/CD deployment

## Phase Details

### Phase 1: Foundation
**Goal**: The repo is publicly presentable with a finalized structure, metadata schema, and root documentation — every downstream component (collector script, Astro site, skill docs) builds against decisions made here.
**Depends on**: Nothing (first phase)
**Requirements**: REPO-01, REPO-02, REPO-03, REPO-04, REPO-05
**Success Criteria** (what must be TRUE):
  1. Skills are organized into workflow-based directories (auditing/, reporting/, campaign-management/, etc.) and existing skills exist at their new paths without breaking existing setup scripts
  2. Every skill directory contains a meta.yaml sidecar with fields: category, tags, complexity, platforms, prerequisites — and a finalized schema document defines all valid values
  3. A per-skill documentation template (SKILL-TEMPLATE.md) exists with enforced sections: what it does, prerequisites, install command, usage examples, last-tested date, non-technical guide
  4. The root README serves as a navigation hub with category index, install instructions, and a contribution guide stub
  5. CHANGELOG.md exists and is seeded with the initial catalog entry
**Plans**: TBD

Plans:
- [ ] 01-01: Audit existing repo, decide workflow taxonomy, restructure directories
- [ ] 01-02: Define and document meta.yaml schema; write per-skill documentation template
- [ ] 01-03: Write polished root README and seed CHANGELOG.md

### Phase 2: Skills
**Goal**: The catalog contains 5-10 public-ready skills that non-technical marketers can install and use, each with complete documentation, a tested quality signal, and a copy-paste install command.
**Depends on**: Phase 1
**Requirements**: SKIL-01, SKIL-02, SKIL-03, SKIL-04
**Success Criteria** (what must be TRUE):
  1. At least 5 skills exist across different workflow categories, each rebuilt or documented to the Phase 1 template standard
  2. Every skill displays a tested quality signal (e.g., "Last tested: YYYY-MM-DD with Claude Code vX.X") visible in both the README and meta.yaml
  3. Every skill README contains a copy-paste one-liner install command that works on a clean machine
  4. At least one skill has been validated end-to-end by a non-technical person following only the written setup guide — and they succeeded
**Plans**: TBD

Plans:
- [ ] 02-01: Migrate and rebuild existing skills (Klaviyo pack, LinkedIn viz, pro deck builder) to public-ready standard
- [ ] 02-02: Create 2-4 new skills in underrepresented workflow categories; validate non-technical install docs

### Phase 3: Site
**Goal**: A static companion website is live at GitHub Pages, auto-generated from repo content, with a browsable skill catalog, category filtering, full-text search, and per-skill detail pages — deployed automatically on every push to main.
**Depends on**: Phase 2
**Requirements**: SITE-01, SITE-02, SITE-03, SITE-04, CICD-01, CICD-02
**Success Criteria** (what must be TRUE):
  1. A non-technical marketer can browse skills by workflow category on the website without touching the GitHub repo
  2. A visitor can search for a skill by keyword (e.g., "email" or "reporting") and get relevant results — powered by Pagefind, with no server required
  3. Each skill has a detail page showing description, prerequisites, install command, usage examples, and last-tested date — all rendered from meta.yaml and SKILL.md, never manually edited on the site
  4. Pushing a commit to main triggers a GitHub Actions workflow that runs the metadata collector, builds the Astro site, indexes with Pagefind, and deploys to GitHub Pages — with no manual steps
**Plans**: TBD

Plans:
- [ ] 03-01: Build collect-metadata.py script and generate catalog.json from repo content
- [ ] 03-02: Build Astro + Starlight site consuming catalog.json; implement category pages and per-skill detail pages
- [ ] 03-03: Add Pagefind search indexing and wire up GitHub Actions CI/CD for auto-deploy to GitHub Pages

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 0/3 | Not started | - |
| 2. Skills | 0/2 | Not started | - |
| 3. Site | 0/3 | Not started | - |
