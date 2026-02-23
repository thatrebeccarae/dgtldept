# Feature Research

**Domain:** Developer tooling catalog / skill registry / companion static site
**Researched:** 2026-02-19
**Confidence:** MEDIUM-HIGH (catalog features from direct observation; audience-specific differentiators from synthesis; LOW-confidence assertions flagged inline)

---

## Context: What This Is

A public GitHub repo of tested Claude Code skills, organized by marketing workflow. Two surfaces:

1. **The repo itself** — installation, documentation, contribution
2. **A companion static site** — discovery, positioning, non-technical audience

The audience spans a spectrum: technical ops who clone and hack vs. non-technical marketers who need proof it works before touching a terminal. Features must serve both ends without collapsing toward either.

---

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete or untrustworthy.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Per-skill README/documentation | Every plugin catalog (VS Code, Obsidian, Raycast, npm) surfaces a description, what it does, prerequisites, and installation steps. Absent = abandoned project signal. | LOW | Already partially exists in dtc-skill-pack. Needs standardization into a repeatable template. |
| Copy-paste install command | Users won't read setup prose. They scan for the bash block. Homebrew, npm, Raycast all lead with one-liner. | LOW | Exists for Klaviyo pack. Needs to exist per-skill in catalog. |
| Clear prerequisites section | What do I need before this works? API keys, tools, Claude Code version. Without this, first-run failures kill adoption. | LOW | Exists in Klaviyo pack. Not systematized across skills. |
| Example prompts / use-case demos | VS Code marketplace, Raycast store, and Obsidian plugin browser all show what the extension actually does through examples. Critical for non-technical audiences who cannot reverse-engineer capability from a description. | LOW | Exists in Klaviyo pack (strong). LinkedIn Data Viz has live demo. Needs to be table stakes for every skill. |
| Platform/compatibility signal | "Works with Claude Code" + version or date last tested. Users need confidence the skill is not stale. | LOW | Not currently present. npm shows this via maintenance score; VS Code shows last updated date. |
| License statement | MIT or equivalent. Necessary for professional/enterprise use. Absence signals amateur project. | LOW | MIT present at root level. Should be visible per-skill. |
| Source repo link (from static site) | Any static site catalog must link back to the authoritative source. Raycast store, VS Code marketplace all deep-link to GitHub. | LOW | Trivial to implement; must be deliberate. |
| Search / browse by category | The primary navigation pattern across all catalogs surveyed (VS Code, Obsidian, Raycast, SkillsMP, npm). Without it, the catalog is a flat list that does not scale past ~10 entries. | MEDIUM | Categories exist implicitly (auditing, reporting, campaign management). Need to be explicit navigation. |
| Security disclosure | What access does this skill need? Marketing teams dealing with client data need this. API keys handled how? Absence is a blocker for any enterprise-adjacent user. | LOW | Root README mentions security. Needs to surface per-skill. |
| Changelog / last updated | npm, VS Code, Homebrew all expose recency. Stale tools get abandoned. Non-technical users read "updated 2 years ago" as "broken." | LOW | Not present. Needs to be in per-skill frontmatter or doc header. |

### Differentiators (Competitive Advantage)

Features that set this catalog apart from SkillsMP (96K+ low-signal skills), awesome-lists (link dumps), and Anthropic's own example repo. Not required, but where the project wins.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Workflow-first organization (not tool-first) | Every other skill catalog organizes by tool type (git, testing, code review). This organizes by marketing workflow: auditing, reporting, campaign management. A non-technical marketer searching "how do I audit my Klaviyo flows" finds what they need without knowing what a "skill" is. | MEDIUM | Requires deliberate information architecture. The category structure is the differentiator. |
| Tested badge / quality gate | SkillsMP's documented criticism is low signal-to-noise ratio with no quality control. A "tested on [date] with [Claude version]" indicator on each skill is a meaningful differentiator. Source: Medium article on SkillsMP noted "lack of quality control and low signal-to-noise ratio means you need to be a sophisticated developer who can vet skills yourself." [MEDIUM confidence — secondary source] | LOW | Requires a testing ritual, not infrastructure. The badge is a markdown line in the skill doc. The discipline is the work. |
| Skill pack concept (grouped, connected skills) | SkillsMP, awesome-claude-code, and other catalogs treat skills as atomic units. The dtc-skill-pack demonstrates that connected skill groups (analyst + developer + GA4 + Shopify + Looker Studio + deck builder) are more valuable than individual skills for workflow-complete use cases. This is a structural differentiator. | MEDIUM | Already exists as the core product shape. The catalog must foreground this as intentional design, not happenstance. |
| Non-technical onboarding path | SkillsMP and awesome-claude-code assume developer-level comfort. The setup wizard (scripts/setup.py) in the Klaviyo pack is already differentiated. Making this pattern systematic — wizard OR copy-paste OR manual, clearly tiered — serves the non-technical marketer audience that no competitor explicitly targets. | MEDIUM | Pattern exists. Needs documentation as a design principle, not just an implementation detail. |
| Live demo links | The LinkedIn Data Viz demo is the only external-facing proof of output in any Claude Code skill catalog surveyed. No competitor provides this. For non-technical users, "see what it produces" is more compelling than "read what it does." | MEDIUM | Requires hosted outputs. LinkedIn Data Viz already does this via GitHub Pages. Should be a standard optional field in per-skill docs: "See example output: [link]". |
| Marketing-specific benchmark context | The Klaviyo analyst skill references industry benchmarks (e.g., abandoned cart flow click rate norms). No general-purpose skill catalog can do this. Domain specificity is the moat. Documenting what good looks like (benchmarks, typical outputs) is a differentiator. | LOW | Already embedded in skill content. Should be surfaced in catalog metadata. |
| Companion static site for non-technical discovery | GitHub is a technical interface. A static site with plain-English workflow descriptions, screenshots of outputs, and a "which skill do I need?" guide serves marketers who will never clone a repo. No current Claude Code skill catalog has a companion site targeting non-technical users. | HIGH | This is the highest-complexity differentiator. Worth it if the audience is real. Astro or Hugo is appropriate. |
| Contribution guide with quality standards | awesome-claude-code accepts community submissions via CSV with minimal quality bar. A clear standard (tested, documented, example prompts, security disclosure) raises the bar and protects catalog quality. This is a differentiator via curation discipline. | LOW | Needs writing; no code required. |

### Anti-Features (Deliberately NOT Build)

Features that seem reasonable but create problems for this specific project. Documented to prevent scope creep.

| Anti-Feature | Why Requested | Why Problematic | What to Do Instead |
|--------------|---------------|-----------------|-------------------|
| Rating/review system | npm, VS Code, Obsidian all have ratings. Seems like table stakes. | With a small catalog and niche audience, ratings will be sparse and meaningless. Zero ratings look worse than no rating system. SkillsMP tried popularity-based ranking and produced a low-signal experience. | Surface "tested on" dates and explicit quality statements from the author. Curated quality beats crowd-sourced signal when volume is low. |
| Auto-aggregation of community skills | SkillsMP has 96K+ skills via automated GitHub scraping. More seems better. | Signal-to-noise destruction. SkillsMP is documented as overwhelming with poor filtering. The value proposition of this catalog is tested, opinionated skills for marketing teams. Auto-aggregation destroys that. | Deliberate curation. Accept contributions via PR with quality gate, not automated scraping. |
| Version pinning / dependency management system | Developer tool registries like Homebrew manage dependencies. Seems professional. | Claude Code skills are markdown + scripts. There is no package dependency graph to manage. Building version management infrastructure before the problem exists is pure overhead. | Use "last tested with Claude Code [date]" in per-skill frontmatter. That is the entire maintenance signal needed. |
| User accounts / saved skills / favorites | Personalization features (favorites, installed tracking). | Static site + GitHub repo does not need a backend. Adding accounts requires auth, database, session management. | Rely on GitHub stars for save-to-later behavior. Lean into GitHub's existing social infrastructure. |
| In-browser skill runner / playground | "Try it without installing" interactive sandbox. | Claude Code skills require Claude Code. There is no web-based runtime. Simulating one is misleading and would require building a proxy to the Claude API — massive scope creep. | Use live demo links to real outputs (HTML pages, screenshots) to show what skills produce, without faking interactivity. |
| Automated skill testing CI pipeline | Automated regression tests that run skills against Claude API in CI. | Requires API credits per test run, non-deterministic outputs, and complex harnesses for skills that interact with third-party APIs (Klaviyo, GA4, Shopify). Cost-prohibitive and fragile at this stage. | Manual testing ritual with a checklist before publishing. Document test date and Claude version. Automate linting of SKILL.md frontmatter structure only — that part is deterministic. |
| Complex tagging taxonomy | Faceted search with 50+ tags (like VS Code marketplace). | With a small catalog, faceted tags create navigation overhead without payoff. Complex taxonomies decay when not maintained. | Three to five top-level workflow categories maximum. Flat is fine until there are 50+ skills. |
| SEO content farm pages | Auto-generating landing pages for every permutation of "Claude Code skill for [tool]" to capture organic search. | Creates maintenance burden, dilutes brand, positions the project as low-quality content rather than curated tooling. The audience discovers via repo and social, not organic search. | Invest in depth over breadth. One excellent page per skill beats ten thin pages. |

---

## Feature Dependencies

```
[Static site]
    └── requires --> [Per-skill documentation template]
                         └── requires --> [Standardized frontmatter fields]
                                              (name, description, platforms, prerequisites,
                                               last-tested, example-prompts, demo-link)

[Category navigation]
    └── requires --> [Workflow-first taxonomy defined]
                         (auditing, reporting, campaign-management, presentation)

[Tested badge / quality gate]
    └── requires --> [Testing ritual documented]
                         └── enhances --> [Contribution guide]

[Live demo links]
    └── requires --> [Hosted output artifacts]
                         (GitHub Pages or static hosting for HTML outputs)

[Skill pack concept foregrounded]
    └── enhances --> [Per-skill documentation]
    └── enhances --> [Workflow-first navigation]

[Non-technical onboarding path]
    └── requires --> [Per-skill setup instructions tiered by user type]
    └── enhances --> [Static site companion]

[Setup wizard pattern]
    └── enhances --> [Non-technical onboarding path]
    └── conflicts with --> [one-liner install only]
        (wizards are good for complex multi-API setups; one-liners for simple skills;
         design both paths and let skill complexity determine which applies)
```

### Dependency Notes

- **Static site requires per-skill docs template first.** You cannot build a catalog site before knowing what data each skill exposes. Define the template, then build the site against it. Reversing this order means rebuilding site structure after the template is finalized.
- **Category navigation requires taxonomy decision first.** The information architecture decision (workflow-first vs. tool-first vs. audience-first) must be made before any site or catalog structure is built. Changing categories later breaks URLs and navigation.
- **Tested badge requires discipline, not infrastructure.** The dependency is a ritual and a checklist, not code. Low effort to establish, high cost to skip.
- **Live demo conflicts with setup wizard for some skills.** Skills that produce file outputs (HTML visualizations, PowerPoint decks) can have demos. Skills that operate on user's live platform data (Klaviyo, GA4) cannot expose live demos without credentials. Design the demo link field as optional.

---

## MVP Definition

### Launch With (v1)

Minimum viable catalog — what is needed to make the public-facing layer credible.

- [ ] **Per-skill documentation template** — Standardized fields: name, one-liner description, what it produces, prerequisites, install command, 3-5 example prompts, last-tested date, demo link (optional). Without this, the catalog is inconsistent and untrustworthy.
- [ ] **Workflow-first category taxonomy** — Define and document 3-5 top-level workflow categories before building any navigation. This is an information architecture decision, not a writing task.
- [ ] **Static site with category browsing** — Even a minimal Astro or Hugo site with category pages and per-skill pages beats a flat GitHub README for non-technical discovery.
- [ ] **Tested quality signal per skill** — A simple "Last tested: [date] with Claude Code [version]" line in each skill doc. The ritual that produces this is the real work.
- [ ] **Copy-paste install commands per skill** — Standardized across all skills. Currently inconsistent between LinkedIn Data Viz and Klaviyo pack.

### Add After Validation (v1.x)

Features to add once the catalog structure is working and user behavior is observable.

- [ ] **Live demo links** — Add to skills that produce file outputs once the static site is live and can host them. Trigger: first external user feedback asking "what does it look like?"
- [ ] **Contribution guide with quality standards** — Once structure is proven and external contributions start arriving. Trigger: first unsolicited PR.
- [ ] **Search within static site** — Add when catalog exceeds 15-20 skills and category browsing feels insufficient. Trigger: observable user difficulty finding specific skills.
- [ ] **"Which skill do I need?" guide** — Plain-English decision tree for non-technical marketers. Trigger: repeated questions in GitHub issues or social about where to start.

### Future Consideration (v2+)

Features to defer until the catalog has validated its audience and value proposition.

- [ ] **Setup wizard generalization** — Extending the scripts/setup.py pattern to all skills, not just Klaviyo. High effort; defer until complexity of new skills warrants it.
- [ ] **Marketing-specific benchmark library** — A separate reference resource documenting industry benchmarks for email, SMS, analytics. Valuable but scope-expanding.
- [ ] **SKILL.md frontmatter linting in CI** — GitHub Actions validation of required frontmatter fields on PR. Worthwhile once contribution volume makes manual review slow. Deterministic and cheap to run; just not urgent at low volume.

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Per-skill documentation template | HIGH | LOW | P1 |
| Copy-paste install commands | HIGH | LOW | P1 |
| Workflow-first taxonomy | HIGH | LOW | P1 |
| Tested quality signal | HIGH | LOW | P1 |
| Static site with category browsing | HIGH | MEDIUM | P1 |
| Example prompts per skill | HIGH | LOW | P1 |
| Live demo links | HIGH | MEDIUM | P2 |
| Non-technical onboarding guide | MEDIUM | LOW | P2 |
| Search within static site | MEDIUM | MEDIUM | P2 |
| Contribution guide | MEDIUM | LOW | P2 |
| Setup wizard generalization | MEDIUM | HIGH | P3 |
| Benchmark library | LOW | HIGH | P3 |
| SKILL.md linting CI | LOW | MEDIUM | P3 |

**Priority key:**
- P1: Must have for launch — catalog is not credible without these
- P2: Should have, add when structure is proven
- P3: Nice to have, future consideration

---

## Competitor Feature Analysis

| Feature | SkillsMP (96K+ skills, auto-aggregated) | awesome-claude-code (curated link list) | Anthropic official skills repo | Our Approach |
|---------|------------------------------------------|-----------------------------------------|-------------------------------|--------------|
| Quality signal | Install-count ranking only; criticized as low-signal | Human-curated list, no explicit testing | Official provenance only | Tested badge + date; manual curation |
| Organization | Category filter (broad) | Category sections in README | Flat list | Workflow-first categories (auditing, reporting, campaign mgmt) |
| Non-technical audience | Not targeted | Not targeted | Not targeted | Primary audience for static site |
| Skill packs (grouped skills) | Individual skills only | Individual items only | Individual skills | Explicit skill pack as a first-class concept |
| Live demos | None found | None | None | Per-skill demo links (HTML outputs, screenshots) |
| Setup wizard | None | None | None | Pattern established in Klaviyo pack; to be systematized |
| Marketing-domain specificity | Generic | Generic | Generic | Explicit DTC/marketing focus with benchmark context |
| Static site companion | SkillsMP is a site (but for all domains) | GitHub README only | GitHub README only | Companion site targeting non-technical marketing discovery |

---

## Sources

- [SkillsMP — Agent Skills Marketplace](https://skillsmp.com) — Direct observation of catalog features, category structure, quality signal approach. Confidence: MEDIUM (WebSearch verified; site observed via search snippets, not direct fetch).
- [SkillsMP: 87,427+ Claude Code Skills Directory — Medium](https://medium.com/ai-software-engineer/skillsmp-this-87-427-claude-code-skills-directory-just-exploded-but-with-one-annoying-problem-ec4af66b78cb) — Documented criticism of signal-to-noise ratio and quality control gap. Confidence: MEDIUM (secondary source; corroborated by vibecoding.app review).
- [Skills.sh Review (2026) — Vibe Coding](https://vibecoding.app/blog/skills-sh-review) — Comparative review noting quality control and filtering differences across skills directories. Confidence: MEDIUM.
- [awesome-claude-code — GitHub](https://github.com/hesreallyhim/awesome-claude-code) — Structure: CSV source of truth, auto-generated README, categories.yaml, minimal quality gate. Confidence: HIGH (direct repo observation).
- [Extend Claude with skills — Claude Code official docs](https://code.claude.com/docs/en/skills) — SKILL.md frontmatter fields, name/description validation rules, user-invocable vs. disable-model-invocation flags. Confidence: HIGH (official Anthropic documentation).
- [VS Code Extension Marketplace — Microsoft official docs](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace) — Per-extension page features: description, install count, 5-star rating, README, changelog, feature contributions, dependencies, publisher. Confidence: HIGH (official documentation).
- [Obsidian Plugin Stats — obsidianstats.com](https://www.obsidianstats.com) — Ratings, reviews, trending calculation via z-score on daily downloads, tag-based filtering. Confidence: MEDIUM (third-party stats site, not official Obsidian; patterns consistent with Obsidian's community plugin design).
- [npm Search Experience Updates — Socket.dev](https://socket.dev/blog/npm-updates-search-experience) — npm retiring popularity/quality/maintenance scoring in favor of objective sorting. Quality signals historically included: README presence, tests, up-to-date dependencies, release frequency. Confidence: HIGH (news source covering official npm change).
- [Homebrew Taps — official docs](https://docs.brew.sh/Taps) — Formula structure: formula_renames.json, Casks directory, cmd subdirectory. Metadata: URL, checksum, dependencies, build instructions. Confidence: HIGH (official Homebrew documentation).
- [Raycast — Prepare an Extension for Store](https://developers.raycast.com/basics/prepare-an-extension-for-store) — Screenshots (max 6), categories, extension details screen. Confidence: HIGH (official Raycast developer documentation).
- [Existing repo — dtc-skill-pack README](https://github.com/thatrebeccarae/claude-code-skills/blob/main/skill-packs/dtc-skill-pack/README.md) — Direct read of existing skill pack structure. Confidence: HIGH (primary source).

---

*Feature research for: Claude Code Skills public catalog + companion static site*
*Researched: 2026-02-19*
*Researcher: gsd-project-researcher agent*
