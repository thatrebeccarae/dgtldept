---
name: google-ads
description: Google Ads platform expertise. Audit campaigns, keywords, audiences, bidding, and conversion tracking. Use when the user asks about Google Ads, PPC, search advertising, Performance Max, Shopping ads, display campaigns, YouTube ads, or paid search optimization.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: paid-media
  domain: google-ads
  updated: 2026-03-11
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Google Ads

Expert-level guidance for Google Ads — auditing, building, and optimizing search, shopping, display, video, Performance Max, and demand gen campaigns.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/google-ads ~/.claude/skills/
```

## Core Capabilities

### Campaign Auditing & Optimization
- Full account audit covering structure, settings, bidding, keywords, ads, and tracking
- Quality Score optimization (expected CTR, ad relevance, landing page experience)
- Search term analysis and negative keyword management
- Budget allocation and pacing optimization
- Wasted spend identification and elimination

### Campaign Types
- **Search** — Text ads on Google Search and Search Partners
- **Shopping** — Product Listing Ads from Google Merchant Center
- **Performance Max** — AI-driven cross-channel (Search, Shopping, Display, YouTube, Discover, Gmail, Maps)
- **Display** — Banner/responsive ads across Google Display Network (3M+ sites)
- **Video** — YouTube ads (in-stream, bumper, discovery, shorts)
- **Demand Gen** — Visual-first ads on YouTube, Discover, Gmail
- **App** — App install and engagement campaigns

### Bidding Strategies
- **Manual CPC / Enhanced CPC** — Direct control, good for learning phases
- **Target CPA** — Optimize for cost per conversion
- **Target ROAS** — Optimize for return on ad spend
- **Maximize Conversions / Maximize Conversion Value** — Spend full budget optimally
- **Target Impression Share** — Competitive visibility
- Portfolio bid strategies for cross-campaign optimization

### Audience Strategy
- First-party data: Customer Match, website visitors, app users
- Google audiences: In-market, affinity, detailed demographics, life events
- Custom audiences (by keywords, URLs, apps)
- Remarketing lists for Search Ads (RLSA)
- Optimized targeting vs observation mode
- Audience signals for Performance Max

### Tracking & Measurement
- Google Tag (gtag.js) / Google Tag Manager implementation
- Conversion actions: website, phone calls, app, import, store visits
- Enhanced conversions (first-party data matching)
- Offline conversion import (GCLID / enhanced conversions for leads)
- Google Ads Data Hub and GA4 integration
- Attribution models: data-driven (default), last-click, cross-channel

## Key Benchmarks

| Metric | Good | Great | Warning |
|--------|------|-------|---------|
| Search CTR | 4-6% | 8%+ | <3% |
| Search CPC | Industry dependent | Below industry avg | Rising trend |
| Search Conv Rate | 3-5% | 7%+ | <2% |
| Quality Score | 7-8 | 9-10 | <6 |
| Impression Share (Brand) | 90%+ | 95%+ | <80% |
| Impression Share (Non-Brand) | 40-60% | 70%+ | <30% |
| PMax ROAS | 3-4x | 6x+ | <2x |
| Display CTR | 0.5-1% | 1.5%+ | <0.3% |
| YouTube View Rate | 15-25% | 30%+ | <10% |

## Account Structure Best Practices

```
Account
├── Brand Search (Exact + Phrase match)
│   ├── Pure Brand
│   └── Brand + Product/Service modifiers
├── Non-Brand Search (by theme/intent)
│   ├── High-Intent / Bottom-Funnel keywords
│   ├── Mid-Funnel / Consideration keywords
│   └── Category / Broad keywords
├── Competitor Search (optional)
│   └── Competitor brand terms
├── Shopping (Standard)
│   ├── Top Performers (high priority)
│   ├── Category groups (medium priority)
│   └── Catch-All (low priority)
├── Performance Max
│   ├── Asset Groups by product category or audience theme
│   └── Audience signals per group
├── Display (if separate from PMax)
│   ├── Remarketing
│   └── Prospecting (in-market / custom)
├── YouTube / Video
│   ├── Brand awareness (bumper, in-stream)
│   └── Action / conversions (in-feed, in-stream)
└── Demand Gen
    └── Visual-first prospecting
```

## Workflow: Full Account Audit

When asked to audit a Google Ads account:

1. **Conversion Tracking** — Verify Google Tag, conversion actions, enhanced conversions, attribution model
2. **Account Structure** — Campaign organization, naming conventions, settings consistency
3. **Budget & Bidding** — Allocation across campaigns, bid strategy alignment with goals, target efficiency
4. **Keyword Strategy** — Match types, Quality Scores, search term relevance, negative keyword lists
5. **Ad Copy** — RSA asset quality (headlines, descriptions), pin usage, ad strength, extensions
6. **Shopping / Merchant Center** — Feed quality, disapprovals, competitive metrics, listing groups
7. **Performance Max** — Asset group quality, audience signals, URL expansion settings, cannibalizing Search
8. **Audiences** — First-party lists, remarketing, Customer Match, observation vs targeting
9. **Landing Pages** — Load speed, message match, conversion rate by landing page
10. **Competitive Landscape** — Auction insights, impression share losses (budget vs rank)
11. **Recommendations** — Prioritized by expected revenue impact with effort estimate

## Performance Max Guidance

PMax-specific audit checklist:
- Asset group organization (themes, not catch-all)
- All asset types provided (text, image, video, logo)
- Audience signals configured (not left empty)
- URL expansion settings reviewed (exclude irrelevant pages)
- Search themes added for intent signals
- Brand exclusions applied
- Not cannibalizing high-performing standard Shopping/Search campaigns
- Conversion goals aligned (avoid mixing lead gen and ecommerce)

## How to Use This Skill

Ask me questions like:
- "Audit my Google Ads account and find wasted spend"
- "My Quality Scores are low — help me diagnose and fix"
- "Design a Performance Max campaign structure for my ecommerce store"
- "Should I use Target CPA or Target ROAS?"
- "Help me build a negative keyword strategy"
- "My CPA is increasing — what should I investigate?"
- "Plan a YouTube advertising strategy for brand awareness"
- "Review my Google Merchant Center feed for issues"

For detailed Google Ads API reference, script templates, and advanced configurations, see [REFERENCE.md](REFERENCE.md).

## Hard Rules

These constraints must never be violated in recommendations:

1. **Never recommend Broad Match without Smart Bidding.** Broad Match + Manual CPC = uncontrolled spend.
2. **3x Kill Rule:** Flag any campaign/ad group with CPA >3x target for immediate pause or restructuring.
3. **Enhanced Conversions must be recommended** if not already active. Foundation for data quality.
4. **Consent Mode v2 required** for any account serving EU/EEA traffic.
5. **Negative keyword lists required** — minimum 3 themed lists (Competitor, Jobs, Free, Irrelevant).
6. **Never recommend edits during active learning phase** — wait for learning to complete or reset intentionally.
7. **Brand and non-brand must be separated** into distinct campaigns with independent budgets and bidding.
8. **PMax must have brand exclusions** when a brand Search campaign exists.

## Scored Audit

When performing an account audit, load `skills/shared/scoring-system.md` for the weighted scoring algorithm and `CHECKS.md` for the 74-check Google Ads audit checklist. Produce a health score (0-100, grade A-F) with Quick Wins and a prioritized action plan.
