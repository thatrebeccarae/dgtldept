---
name: brand-dna
description: "Extract brand identity from a website URL — voice, colors, typography, imagery, values, and target audience — into a structured brand-profile.json. The profile feeds downstream skills (seo-content-writer, email-composer, frontend-design, pro-deck-builder, cross-platform-audit) for brand-consistent output. Use when the user says brand DNA, brand profile, extract brand, analyze brand, brand voice, brand identity, brand colors, or brand style guide."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: strategy
  domain: brand-identity
  updated: 2026-03-16
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Brand DNA — Brand Identity Extractor

Extracts brand identity from a website and produces a structured `brand-profile.json` that other skills can consume for brand-consistent output.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/brand-dna ~/.claude/skills/
```

## Quick Reference

| Command | What It Does |
|---------|-------------|
| "Extract brand DNA from https://example.com" | Full extraction → `brand-profile.json` |
| "Quick brand profile for https://example.com" | Homepage-only extraction (faster, lower confidence) |

## Zero Dependencies

This skill uses only the WebFetch tool — no Python scripts, no Playwright, no external APIs. It works anywhere Claude Code runs.

## Extraction Process

### Step 1: Collect URL

If the user hasn't provided a URL, ask:
> "What website URL should I analyze? (e.g., https://yoursite.com)"

### Step 2: Fetch Pages

Use the **WebFetch tool** to retrieve page content. For each URL, request:
- All visible text content
- Full contents of `<style>` blocks
- Inline `style=` attributes
- `<meta>` tags (especially `og:image`, `description`)
- Google Fonts `@import` URLs
- Any `<link>` tags referencing external stylesheets

**Fetch order:**
1. **Homepage** (`<url>`)
2. **About page** — try `<url>/about`, then `/about-us`, then `/our-story`
3. **Product/Services page** — try `<url>/products`, then `/product`, then `/services`

**Quick mode:** If the user requests a quick extraction, fetch homepage only — skip pages 2 and 3.

If a secondary page returns 404 or redirects to homepage, continue with fewer pages and note reduced confidence.

### Step 3: Extract Brand Elements

#### Colors
- **Primary color:** Most prominent brand color from CSS `background-color` on `.hero`, `.btn-primary`, `header`, or `og:image` dominant color
- **Secondary colors:** Supporting palette from CTAs, accents, borders
- **Background/text:** `body` background-color and color
- **Forbidden:** Infer from brand positioning (e.g., competitor colors if identifiable)
- **Dark mode detection:** If body background is #333 or darker, swap background/text values

**CSS targets:** `background-color`, `color`, `border-color` on `body`, `header`, `.hero`, `.btn`, `.cta`, `h1`, `h2`

#### Typography
- **Google Fonts:** Extract from `@import url(https://fonts.googleapis.com/css2?family=...)` — parse font name from URL
- **CSS font-family:** Check `h1`, `h2`, `body`, `.headline` declarations
- **Fallback:** If no Google Fonts detected, set heading_font to `null` and body_font to `"system-ui"`

#### Voice (1-10 scale per axis)
Analyze hero headline, subheadline, about page intro, and CTA button text:

| Signal | Axis | Direction |
|--------|------|-----------|
| Uses "you/your" frequently | formal_casual | +2 toward casual |
| Technical jargon, industry terms | expert_accessible | -2 toward expert |
| Short punchy sentences (≤8 words) | bold_subtle | +2 toward bold |
| Data, stats, percentages in hero | rational_emotional | -2 toward rational |
| "Transform", "revolutionize", "disrupt" | traditional_innovative | +2 toward innovative |
| Customer testimonials lead | rational_emotional | +2 toward emotional |
| "Trusted by X companies", awards | traditional_innovative | -1 toward traditional |
| Humor, wordplay, casual phrasing | playful_serious | +2 toward playful |
| Formal language, third person | playful_serious | -2 toward serious |

Start each axis at 5 (neutral) and adjust based on signals found.

**Descriptors:** Choose 3-5 adjectives that capture the overall voice tone. These should complement the numerical scores, not repeat them.

#### Imagery
- **Style:** Professional photography, illustration, flat design, 3D renders, or mixed
- **Subjects:** What appears in hero images and product shots (people, products, abstract, data)
- **Composition:** Clean/minimal, busy/editorial, dark/dramatic, light/airy
- **Forbidden elements:** Infer from industry (healthcare → no unqualified medical claims imagery; B2B → no cheesy stock photos)

#### Aesthetic
- **Mood keywords:** 3 adjectives describing the visual mood (e.g., "trustworthy", "modern", "premium")
- **Texture:** minimal, textured, or mixed
- **Negative space:** generous, moderate, or dense

#### Brand Values
Extract from about page, mission statement, or footer. Look for repeated themes. Choose 3-5 core values.

#### Target Audience
Infer from copy, pricing signals, and positioning:
- **Age range:** Estimate from visual design, language complexity, and product type
- **Profession:** Who the product/service is for
- **Pain points:** What problems the brand addresses (from hero copy and feature descriptions)
- **Aspirations:** What the audience wants to achieve (from benefit-oriented copy)

### Step 4: Build brand-profile.json

Construct the JSON following the schema in REFERENCE.md precisely. Use `null` for any field that cannot be confidently extracted — never guess.

### Step 5: Write and Confirm

Write `brand-profile.json` to the current working directory.

Display a summary:
```
Brand DNA extracted → brand-profile.json

  Brand: [brand_name]
  Voice: [descriptor 1], [descriptor 2], [descriptor 3]
  Primary Color: [hex]
  Typography: [heading_font] / [body_font]
  Audience: [age_range], [profession]

This profile can be consumed by:
  - seo-content-writer (voice matching)
  - email-composer (tone calibration)
  - frontend-design (visual identity)
  - pro-deck-builder (brand colors/fonts)
  - cross-platform-audit (brand consistency checks)
```

## Limitations

- **Sparse sites:** <200 words of body text produce lower-confidence profiles. Note this in output.
- **SPA/React sites:** JavaScript-rendered content may not be fully captured by WebFetch. Note this if detected.
- **Multi-brand enterprises:** Creates one profile per URL. Run separately for each brand.
- **CSS-in-JS:** Modern React/Next.js sites may not have extractable CSS. Use og:image analysis as fallback.

## How to Use This Skill

Ask questions like:
- "Extract the brand DNA from https://example.com"
- "Build a brand profile for my client's website"
- "Analyze the brand voice and colors of https://competitor.com"
- "Quick brand profile — homepage only — for https://example.com"
- "What's the brand identity of this website?"
