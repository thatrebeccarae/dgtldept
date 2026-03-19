Template-based page generation at scale for SEO. Data-driven content, internal linking architecture, and automated optimization for large-scale content operations. Use when the user asks about programmatic SEO, pSEO, scaled content, template pages, or automated page generation.


# Programmatic SEO

Generate thousands of targeted pages from data templates at scale.

## What Is Programmatic SEO

Creating large numbers of search-optimized pages from structured data + templates. Instead of writing each page manually, you define a template and populate it with data variations.

**Examples of successful pSEO:**
- Zapier: "[App A] + [App B] integrations" (25,000+ pages)
- Wise: "[Currency A] to [Currency B]" exchange rate pages
- NomadList: "[City] for digital nomads" with cost/weather/internet data
- Yelp: "[Business type] near [location]" listing pages
- Canva: "[Template type] templates" design pages

## Use Cases

| Pattern | Template | Data Source | Pages |
|---------|----------|------------|-------|
| Integration pages | "[Your product] + [Partner]" | Partner/integration list | 100-5,000 |
| Location pages | "[Service] in [City/State]" | Location database | 500-50,000 |
| Comparison pages | "[Your product] vs [Competitor]" | Competitor list | 20-200 |
| Glossary/definitions | "What is [Term]?" | Industry term database | 200-2,000 |
| Template/example pages | "[Type] template" or "[Type] examples" | Template library | 100-1,000 |
| Tool pages | "[Metric] calculator" | Calculator variations | 50-500 |
| Stats pages | "[Topic] statistics [Year]" | Data sources | 50-500 |

## Template Design

### Page Template Structure

```
[H1: Dynamic title with primary keyword]
[Intro paragraph: 2-3 sentences with entity-specific context]
[Key data section: structured data unique to this entity]
[Comparison or context section: how this entity relates to others]
[FAQ section: 3-5 entity-specific questions]
[Related pages: internal links to related entities]
[CTA: conversion action relevant to search intent]
```

### Quality Requirements

Every programmatic page MUST have:
1. **Unique title tag** — not just "[Entity] | Site Name"
2. **Unique meta description** — entity-specific, not templated
3. **Unique introductory content** — at least 2-3 sentences unique per page
4. **Unique data** — entity-specific numbers, facts, or comparisons
5. **Internal links** — contextual links to related pages and hub pages
6. **Schema markup** — appropriate structured data per page type

### Anti-Patterns (Google Will Penalize)

1. **Doorway pages** — thin pages with no unique value, just keyword variations
2. **Duplicate content** — same paragraph on every page with only entity name swapped
3. **No user value** — page exists for search engines, not humans
4. **Orphaned pages** — no internal links pointing to them
5. **Auto-generated gibberish** — AI-generated content without quality review

## Internal Linking Architecture

### Hub-and-Spoke Model

```
Hub page: "[Category] Guide" (high authority)
  └── Spoke 1: "[Entity A] in [Category]"
  └── Spoke 2: "[Entity B] in [Category]"
  └── Spoke 3: "[Entity C] in [Category]"
  (Each spoke links back to hub and to 3-5 related spokes)
```

### Cross-Linking Rules


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
