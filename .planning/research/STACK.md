# Stack Research

**Domain:** Public developer tooling catalog with auto-generated static companion website
**Researched:** 2026-02-19
**Confidence:** MEDIUM — core framework and search decisions verified via official docs and release notes; some compatibility nuances flagged as needing active monitoring

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Astro | 5.17+ (current as of Jan 2026) | Static site framework | Islands architecture means zero JS shipped by default — ideal for a catalog where performance matters for non-technical visitors. Content Layer API (introduced v5.0) was purpose-built for file-based content sourcing, which maps directly to reading SKILL.md and README.md files from the repo. File-based routing and `getStaticPaths()` auto-generate pages from collections without manual configuration. |
| Starlight (Astro integration) | 0.37.6 (current, Jan 2026; Astro 5 compatible) | Documentation/catalog theme on top of Astro | Ships with navigation, dark mode, accessible typography, category grouping, mobile nav, and Pagefind search out of the box — no building these from scratch. Its plugin ecosystem is active (Tags plugin, Telescope fuzzy-search plugin available). Initial Astro 5 compatibility issues (around v0.30) were resolved; 0.37.x confirmed working with Astro 5. |
| Pagefind | 1.4.0 (current) | Client-side static full-text search | Runs entirely at build time. Zero server required. Searches title metadata by default, with ranking that weights title matches higher. Ships as a UI widget that Starlight integrates automatically — no config needed. Binary indexed at build, lightweight JS bundle at runtime. |
| Zod | Bundled with Astro content collections | Frontmatter schema validation | Astro 5 Content Layer API uses Zod natively for schema enforcement. Validation happens at build time, not runtime — broken frontmatter fails the build cleanly rather than silently rendering bad pages. IDE autocomplete comes for free. No separate install required. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `@astrojs/mdx` | Bundled with Astro | MDX support for skill pages needing interactive components | Only if skill pages need embedded interactive examples. For pure documentation catalogs, plain Markdown is sufficient. |
| `astro-icon` | Latest | Icon support for category labels, badge chips, complexity indicators | When adding visual metadata indicators to catalog cards (e.g., complexity level, platform tags). |
| `sharp` | Bundled with Astro | Image optimization | Needed if adding screenshots or preview images to skill cards. Auto-invoked by Astro's `<Image>` component. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| Node.js | Runtime for Astro build | v22 is the current default in the official `withastro/action` GitHub Action. Match locally. |
| `withastro/action` GitHub Action | Official Astro GitHub Action for CI/CD deploy | v5 of the action. Configured with `actions/checkout@v4`, `withastro/action@v5`, `actions/deploy-pages@v4`. Produces a two-job workflow: build then deploy. |
| GitHub Pages | Static hosting | Free, unlimited bandwidth on public repos. Direct integration with `withastro/action`. Requires `site` config in `astro.config.mjs` set to the GitHub Pages URL. No cold starts, no usage caps, no build minute quotas to worry about. Best fit given the repo already lives on GitHub. |

---

## Installation

```bash
# Scaffold a new Starlight project (recommended — includes Astro + Starlight wired together)
npm create astro@latest -- --template starlight

# If adding to existing Astro project
npx astro add starlight

# Dev server
npm run dev

# Build
npm run build

# Preview built output locally
npm run preview
```

**Note:** Pagefind is included and auto-configured by Starlight. Zod is included with Astro. No additional search or schema installs needed.

---

## Frontmatter Schema Design

The companion site auto-generates from repo Markdown files. Astro's Content Layer glob loader reads existing `SKILL.md` and README files, but those files currently use inconsistent or minimal frontmatter. The site's schema should be defined in Astro's `src/content.config.ts` and validated at build time.

**Recommended skill frontmatter schema:**

```typescript
// src/content.config.ts
import { z, defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { glob } from 'astro/loaders';

const skills = defineCollection({
  loader: glob({ pattern: '**/SKILL.md', base: '../../skills' }),
  schema: z.object({
    name: z.string(),
    description: z.string(),
    workflow: z.enum([
      'auditing',
      'reporting',
      'campaign-management',
      'content',
      'analytics',
      'data-viz',
    ]),
    platforms: z.array(z.string()).default([]),
    complexity: z.enum(['beginner', 'intermediate', 'advanced']).default('intermediate'),
    prerequisites: z.array(z.string()).default([]),
    version: z.string().optional(),
    tested: z.boolean().default(false),
  }),
});
```

**Why this schema:**
- `workflow` is an enum, not freeform string — prevents "Auditing" vs "auditing" inconsistency
- `complexity` is explicit — lets non-technical marketers filter before reading further
- `prerequisites` is an array — enables "what do I need first?" filtering
- `tested` boolean — reflects the project's quality gate (Rebecca-tested) explicitly in the data
- Build-time validation means a missing or misspelled field is caught before deploy, not discovered in production

---

## Alternatives Considered

| Recommended | Alternative | Why Not |
|-------------|-------------|---------|
| Astro + Starlight | Docusaurus 3.9 | Docusaurus is React-based and ships more JavaScript by default. Its documentation use case is optimized for large API reference sites with versioning — overkill for a focused catalog. React adds complexity and weight for a site that's primarily static content cards. Meta-maintained, which creates risk of priority drift. |
| Astro + Starlight | VitePress | Vue ecosystem — introduces Vue as a dependency when the repo has no existing Vue. Strong for Vue project docs but no native advantage here. Less plugin ecosystem than Starlight for docs-specific features. |
| Astro + Starlight | MkDocs (Python) | Python-based. The repo already has Python scripts, but mixing Python tooling for site generation creates two distinct build pipelines. MkDocs Material is excellent for Python projects but creates a non-standard deploy setup for a primarily Markdown/Node.js ecosystem. |
| Astro + Starlight | Eleventy | Maximum flexibility, zero opinions. For this use case that's a liability — Starlight ships everything needed out of the box. Eleventy would require building search, nav, dark mode, and mobile layout from scratch. |
| Astro + Starlight | Jekyll | Ruby ecosystem, aging toolchain. GitHub Pages defaults to Jekyll but it's no longer the standard for new projects. Slower builds, less active ecosystem in 2025/2026. |
| Pagefind | Algolia DocSearch | Algolia requires ongoing account management, rate limits, and API key rotation. For a public repo catalog with no backend, Pagefind's fully static approach eliminates all operational concerns. DocSearch's new AI search feature (v4) is compelling but not warranted for a catalog of 10–50 skills. |
| Pagefind | Lunr.js | Lunr builds its index in the browser at runtime — worse initial load performance. Pagefind builds the index at compile time and ships it as binary chunks loaded on demand. |
| GitHub Pages | Cloudflare Pages | Both are viable. Cloudflare Pages has unlimited bandwidth and faster CDN globally. GitHub Pages chosen because the repo is already on GitHub, the official `withastro/action` is a one-config deployment, and Cloudflare adds an account/DNS management surface that isn't needed for this project's scale. |
| GitHub Pages | Netlify | Netlify's 100GB/month bandwidth limit and 300 build minutes/month are constrained for a public repo that could get traffic spikes. GitHub Pages has no such caps on public repos. Netlify's DX is excellent but the caps are a risk. |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Next.js | Server-side rendering framework — wrong tool for a static catalog. Adds Node.js server dependency, complex deployment, and SSR overhead with no benefit for static content. Common mistake on "it's React" projects. | Astro |
| Gatsby | Peaked circa 2021. Dramatically slowed development post-Netlify acquisition. Build times are notoriously slow for content-heavy sites, GraphQL data layer adds unnecessary complexity for a file-based catalog. | Astro |
| Hugo | Go-based, extremely fast builds. No native TypeScript schema validation — frontmatter validation is convention-only. Templating syntax (Go templates) is cryptic compared to Astro's JSX-adjacent `.astro` component format. Wrong tradeoff when build speed isn't the bottleneck. | Astro |
| Custom Python script to generate HTML | Tempting given existing Python scripts in the repo. Creates an unmaintainable bespoke build system with no community, no search, no accessible navigation, and no component model. The existing Python scripts are skill runners, not site builders — don't conflate them. | Astro + Starlight |
| Client-side JavaScript catalog (React SPA) | Requires JavaScript to be enabled for any content to render. Kills SEO, kills non-technical accessibility. Wrong architecture for a catalog that should be dead-simple to browse. | Astro (zero JS by default) |
| Separate CMS (Contentful, Notion, etc.) | PROJECT.md explicitly states: static site must be auto-generated from repo content — no separate CMS or manual updates. A CMS breaks the single source of truth. | Astro content collections reading from repo files |

---

## Stack Patterns by Variant

**If the site stays small (< 50 skills):**
- Use Starlight's built-in sidebar navigation for browsing by workflow category
- No additional catalog page needed — Starlight's docs structure handles it
- Pagefind search covers discoverability completely

**If the catalog grows large (50+ skills):**
- Add a custom catalog index page (`src/pages/catalog.astro`) with client-side filter chips
- Filter chips use Astro's View Transitions and minimal Alpine.js or vanilla JS for tag filtering
- Pagefind continues handling full-text search

**If non-technical marketers are the primary entry point:**
- Prioritize the "Getting Started" section using Starlight's `banner` component per skill
- Add a complexity filter on the catalog index (beginner / intermediate / advanced)
- Consider a dedicated "Quick Start" collection separate from the full skills catalog

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| `@astrojs/starlight@0.37.6` | `astro@5.x` | Astro 5 compatibility resolved as of Starlight ~0.30.x. Initial 0.30.0 had issues; subsequent patches fixed them. Verify `peerDependencies` on install. |
| `pagefind@1.4.0` | Starlight 0.37.x | Starlight bundles Pagefind automatically; do not install Pagefind separately in a Starlight project — version conflicts can occur. |
| `node` | v22 LTS | Matches `withastro/action@v5` default. Node 18 dropped in Docusaurus 3.9 (for reference); stay on v22 for longevity. |
| `withastro/action@v5` | GitHub Pages | Requires Pages source set to "GitHub Actions" in repo settings (not "Deploy from branch"). |

---

## Sources

- Astro 5.17 release: https://astro.build/blog/whats-new-january-2026/ — MEDIUM confidence (WebSearch verified)
- Starlight 0.37.6 release, Astro 5 compatibility: https://github.com/withastro/starlight/releases — MEDIUM confidence (WebSearch verified; Astro 5 compat confirmed from multiple sources noting resolution of initial 0.30.x issues)
- Pagefind 1.4.0 current version: https://www.npmjs.com/package/pagefind — MEDIUM confidence (WebSearch verified)
- Starlight site search docs (Pagefind built-in): https://starlight.astro.build/guides/site-search/ — HIGH confidence (official Astro docs)
- Astro Content Collections + Zod: https://docs.astro.build/en/guides/content-collections/ — HIGH confidence (official Astro docs)
- Astro Content Layer API deep dive: https://astro.build/blog/content-layer-deep-dive/ — HIGH confidence (official Astro blog)
- `withastro/action` GitHub Action: https://github.com/withastro/action — HIGH confidence (official Astro org)
- GitHub Pages vs Cloudflare Pages hosting comparison: https://www.freetiers.com/blog/github-pages-vs-cloudflare-pages-comparison — MEDIUM confidence (WebSearch, cross-referenced with Netlify/GH Pages official docs)
- Docusaurus 3.9 (AI search, Node 18 drop): https://www.infoq.com/news/2025/10/docusaurus-3-9-ai-search/ — MEDIUM confidence (WebSearch)
- VitePress vs Docusaurus vs MkDocs comparison 2025: https://okidoki.dev/documentation-generator-comparison — LOW confidence (single source, use for directional context only)

---

## Confidence Notes

- **Starlight + Astro 5 compatibility:** Multiple sources confirm resolution of the initial Astro 5 incompatibility. The exact version where it was fully resolved is ambiguous from search results alone (references to ~0.30.x patches). Verify with `npm create astro@latest -- --template starlight` before committing to this stack — the scaffold will pull the current compatible pair. MEDIUM confidence.
- **Pagefind version:** 1.4.0 confirmed via npm. Do not install as a separate dep in Starlight projects — it's bundled. LOW-to-MEDIUM confidence on exact internal bundled version; check Starlight changelog for their specific Pagefind pin.
- **GitHub Actions workflow syntax:** `actions/checkout@v4`, `withastro/action@v5`, `actions/deploy-pages@v4` are the current major versions per official Astro docs. These version pin frequently — check the official Astro deploy guide at build time. HIGH confidence on the approach, MEDIUM on exact action versions.

---
*Stack research for: Public Claude Code skills catalog with auto-generated static companion website*
*Researched: 2026-02-19*
