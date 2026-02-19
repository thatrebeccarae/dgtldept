# Requirements: Claude Code Skills

**Defined:** 2026-02-19
**Core Value:** Marketing team members can discover, install, and use tested Claude Code skills that accelerate their workflows

## v1 Requirements

### Repo Structure

- [ ] **REPO-01**: Skills organized into workflow-based directories (auditing/, reporting/, campaign-management/, etc.)
- [ ] **REPO-02**: Sidecar meta.yaml per skill with structured metadata (category, tags, complexity, platforms, prerequisites)
- [ ] **REPO-03**: Standardized per-skill documentation template (what it does, prerequisites, setup, usage examples, non-technical guide)
- [ ] **REPO-04**: Polished root README with navigation hub, install instructions, category index, and contribution guide
- [ ] **REPO-05**: CHANGELOG tracking additions and changes to the skill catalog

### Skill Content

- [ ] **SKIL-01**: 5-10 public-ready skills rebuilt/documented across workflow categories
- [ ] **SKIL-02**: Tested badge / quality signal indicating each skill has been personally validated
- [ ] **SKIL-03**: Copy-paste one-liner install command for each skill
- [ ] **SKIL-04**: Non-technical step-by-step setup guides for marketers who aren't CLI-comfortable

### Companion Website

- [ ] **SITE-01**: Astro/Starlight static site auto-generated from repo content
- [ ] **SITE-02**: Browsable skill catalog with category/workflow filtering
- [ ] **SITE-03**: Built-in full-text search via Pagefind
- [ ] **SITE-04**: Per-skill detail pages with description, install, usage, prerequisites

### CI/CD

- [ ] **CICD-01**: Python metadata collector script (walks repo, normalizes meta.yaml + SKILL.md into catalog.json)
- [ ] **CICD-02**: GitHub Actions workflow that auto-deploys site on push to main

## v2 Requirements

### Community

- **COMM-01**: Contribution guide for external skill submissions
- **COMM-02**: Skill request / wishlist mechanism (GitHub Issues template)

### Content

- **CONT-01**: Live demo links for applicable skills (e.g., LinkedIn data viz)
- **CONT-02**: Video walkthroughs for complex skills
- **CONT-03**: Decision guide for non-technical users ("which skill do I need?")

### Discovery

- **DISC-01**: Social sharing metadata (OpenGraph) for skill pages
- **DISC-02**: RSS feed for new skill additions

## Out of Scope

| Feature | Reason |
|---------|--------|
| User accounts / auth | Static catalog, not a SaaS platform |
| Rating / review system | Sparse data looks bad; quality gate is Rebecca's testing |
| Auto-aggregation of skills | SkillsMP's failure mode — low signal-to-noise |
| In-browser skill playground | Enormous complexity, skills run in user's Claude Code |
| Automated CI testing for skills | Skills call live APIs; manual testing is the quality gate |
| Backend / database | Static site only — no server infrastructure |
| Version pinning infrastructure | Premature; catalog is small enough for manual management |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| REPO-01 | — | Pending |
| REPO-02 | — | Pending |
| REPO-03 | — | Pending |
| REPO-04 | — | Pending |
| REPO-05 | — | Pending |
| SKIL-01 | — | Pending |
| SKIL-02 | — | Pending |
| SKIL-03 | — | Pending |
| SKIL-04 | — | Pending |
| SITE-01 | — | Pending |
| SITE-02 | — | Pending |
| SITE-03 | — | Pending |
| SITE-04 | — | Pending |
| CICD-01 | — | Pending |
| CICD-02 | — | Pending |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 0
- Unmapped: 15

---
*Requirements defined: 2026-02-19*
*Last updated: 2026-02-19 after initial definition*
