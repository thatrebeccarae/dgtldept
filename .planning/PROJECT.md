# Claude Code Skills

## What This Is

A public repository of tested, validated Claude Code skills and agents designed for marketing teams. Skills are organized by workflow (auditing, reporting, campaign management, etc.) so marketers can find tools that match what they're trying to do. Accompanied by a static companion website for browsing, filtering, and installation guides.

## Core Value

Marketing team members — from technical ops to non-technical practitioners — can discover, install, and use Claude Code skills that genuinely accelerate their workflows, with confidence that each skill has been personally tested in real work.

## Requirements

### Validated

- ✓ Klaviyo skill pack (analyst + developer + Shopify + GA4 + Looker Studio) — existing
- ✓ LinkedIn data visualization skill — existing
- ✓ Pro deck builder skill — existing
- ✓ Setup scripts for skill pack installation — existing

### Active

- [ ] Workflow-based repo organization (auditing/, reporting/, campaign-management/, etc.)
- [ ] Polished root README with clear navigation, install instructions, and contribution guide
- [ ] Per-skill documentation template (what it does, prerequisites, setup, usage examples)
- [ ] 5-10 public-ready skills across different workflow categories
- [ ] Skill metadata schema (tags, platforms, complexity level, prerequisites)
- [ ] Static companion website auto-generated from repo structure
- [ ] Website with browsable catalog, category filtering, and install guides
- [ ] Non-technical-friendly setup documentation for each skill

### Out of Scope

- Dynamic web app with auth/accounts — this is a static catalog, not a SaaS product
- Automated testing/CI for skills — validation is manual (Rebecca tests in real work)
- Community contributions in v1 — curated collection first, open contributions later
- Skill runtime/hosting — skills run in user's Claude Code environment, not hosted
- Private/proprietary skills — only publicly shareable, platform-generic skills

## Context

- Existing repo has skill packs (Klaviyo bundle) and individual skills (LinkedIn data viz, pro deck builder) that work but weren't built for public consumption
- Existing skills stay as-is for now, get hardened for public consumption later as needed
- Skills are rebuilt for public use — cleaner, better documented, more generic than private versions
- Discovery happens through multiple channels: repo browsing, companion website, and social content (LinkedIn, Substack, Twitter, TikTok) driving traffic back
- Target audience ranges from CLI-comfortable marketing ops to non-technical marketers who need hand-holding
- Rebecca personally tests every skill in real client/project work before publishing — she is the quality gate

## Constraints

- **Public repo**: Everything committed must be safe for public consumption — no API keys, client names, or proprietary config
- **Audience range**: Documentation must serve both technical and non-technical marketers
- **Static site**: Companion website must be auto-generated from repo content (no separate CMS or manual updates)
- **Existing content**: Current skills/packs remain in place; restructuring must not break them

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Organize skills by workflow, not platform | Matches how marketers think ("I need to audit") rather than tool-centric browsing | — Pending |
| Static site generated from repo | Single source of truth, no sync issues between repo and website | — Pending |
| Rebuild skills for public rather than publishing private ones | Private skills have personal config, shortcuts, and assumptions that won't work for others | — Pending |
| Keep existing skills as-is initially | They work; focus energy on repo structure and new skills first | — Pending |

---
*Last updated: 2026-02-19 after initialization*
