---
name: facebook-ads
description: Meta Ads (Facebook & Instagram) platform expertise. Audit campaigns, audiences, creative strategy, pixel tracking, and CAPI. Use when the user asks about Facebook Ads, Instagram Ads, Meta Ads, social media advertising, Advantage+ campaigns, or Meta pixel/CAPI setup.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: paid-media
  domain: meta-ads
  updated: 2026-03-11
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Meta Ads (Facebook & Instagram)

Expert-level guidance for Meta Ads — auditing, building, and optimizing campaigns across Facebook, Instagram, Messenger, and the Audience Network.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/facebook-ads ~/.claude/skills/
```

## Core Capabilities

### Campaign Auditing & Optimization
- Full account audit: structure, objectives, audiences, creative, tracking, attribution
- Identify creative fatigue, audience overlap, and budget inefficiencies
- Diagnose performance drops (iOS privacy, audience saturation, creative burnout)
- Advantage+ Shopping and Advantage+ Audience recommendations

### Campaign Objectives (Outcome-Based)
- **Awareness** — Reach, brand awareness, video views
- **Traffic** — Link clicks, landing page views
- **Engagement** — Post engagement, messages, conversions on-platform
- **Leads** — Instant Forms, Messenger, website lead gen
- **App Promotion** — App installs, app events
- **Sales** — Website conversions, catalog sales, Advantage+ Shopping

### Audience Strategy
- **Core Audiences** — Demographics, interests, behaviors, location
- **Custom Audiences** — Website (pixel/CAPI), customer list, app activity, video viewers, engagement
- **Lookalike Audiences** — 1-10% based on custom audience seed (value-based LALs preferred)
- **Advantage+ Audience** — Meta's AI-driven targeting (audience suggestions as signals, not constraints)
- **Broad targeting** — No interests/LAL, rely on creative + pixel data + Meta's ML

### Creative Strategy
- Ad format selection: single image, carousel, video, collection, Instant Experience
- Creative testing frameworks: concept testing vs iterative testing
- UGC (user-generated content) integration and creator whitelisting
- Dynamic Creative Optimization (DCO) vs manual A/B testing
- Creative fatigue signals and refresh cadence
- Platform-specific creative (Feed, Stories, Reels, Explore)

### Tracking & Attribution
- **Meta Pixel** — Standard events, custom events, microdata, aggregated event measurement
- **Conversions API (CAPI)** — Server-side tracking for privacy resilience
- **Aggregated Event Measurement (AEM)** — iOS 14.5+ handling, 8-event prioritization
- Attribution settings: 7-day click + 1-day view (default), 1-day click, 28-day click
- UTM parameter strategy for GA4 cross-reference
- Conversion lift studies and incrementality testing

## Key Benchmarks

| Metric | Good | Great | Warning |
|--------|------|-------|---------|
| CTR (Link Clicks) | 1-2% | 3%+ | <0.8% |
| CPC (Link Click) | $0.50-$1.50 | <$0.50 | >$2.00 |
| CPM | $8-$15 | <$8 | >$20 |
| Conversion Rate (Landing Page) | 3-5% | 8%+ | <2% |
| ROAS (ecommerce) | 3-4x | 6x+ | <2x |
| Cost Per Lead | Industry dependent | Below industry avg | Rising trend |
| Frequency (prospecting) | 1.5-2.5 | 1-1.5 | >3.5 |
| Frequency (retargeting) | 3-6 | 2-3 | >10 |
| Thumb-Stop Rate (video) | 25-35% | 40%+ | <20% |
| Hook Rate (3s video views %) | 30-40% | 50%+ | <25% |

## Campaign Structure (Modern Best Practice)

```
Ad Account
├── Advantage+ Shopping Campaign (ecommerce)
│   ├── Broad targeting (Meta AI optimizes)
│   ├── Existing customer budget cap (10-20%)
│   └── Mixed creative (image, video, UGC, carousel)
├── Prospecting Campaign (Conversions/Sales)
│   ├── Ad Set: Broad (no targeting, trust the pixel)
│   ├── Ad Set: Lookalike 1-3% (value-based)
│   └── Ad Set: Interest stacks (if needed)
├── Retargeting Campaign (Conversions/Sales)
│   ├── Ad Set: Website visitors 1-30 days
│   ├── Ad Set: Engaged (video viewers, IG/FB engaged)
│   └── Ad Set: Cart abandoners
├── Lead Gen Campaign (if applicable)
│   ├── Ad Set: Lookalikes of converters
│   └── Ad Set: Interest-based
└── Brand / Top-of-Funnel (optional)
    ├── Video Views (awareness content)
    └── Traffic (blog, resources)
```

**Modern trend**: Consolidate ad sets. Meta's algorithm performs better with fewer, broader ad sets and more creative diversity within each.

## Workflow: Full Account Audit

When asked to audit a Meta Ads account:

1. **Pixel & CAPI Health** — Event tracking, CAPI coverage, event match quality score, AEM config
2. **Account Structure** — Campaign consolidation, objective alignment, naming conventions
3. **Audience Strategy** — Overlap analysis, LAL seeds, audience size, Advantage+ adoption
4. **Creative Analysis** — Format mix, creative fatigue (frequency + declining CTR), testing velocity
5. **Budget & Bidding** — CBO vs ABO, budget allocation, bid strategy (lowest cost vs cost cap vs bid cap)
6. **Funnel Coverage** — Prospecting vs retargeting balance, exclusions between funnels
7. **Attribution** — Window settings, cross-platform reconciliation (vs GA4), CAPI deduplication
8. **Placement Optimization** — Advantage+ placements vs manual, creative per placement
9. **Shopping / Catalog** — Feed quality, product sets, dynamic ads setup
10. **Recommendations** — Prioritized with expected impact and creative direction

## Post-iOS 14.5 Best Practices

- Implement CAPI alongside pixel (aim for 90%+ event match quality)
- Prioritize 8 conversion events per domain in Events Manager
- Use value optimization when possible (Purchase over Add to Cart)
- Broader audiences outperform narrow (give Meta's ML room to optimize)
- UTM tracking + GA4 as secondary attribution source
- Creative is the new targeting — invest in creative testing over audience testing

## How to Use This Skill

Ask me questions like:
- "Audit my Facebook Ads account performance"
- "My ROAS is declining — what should I investigate?"
- "Help me set up Conversions API (CAPI)"
- "Design a creative testing framework for my brand"
- "Should I use Advantage+ Shopping or manual campaigns?"
- "Build a full-funnel campaign structure for my DTC brand"
- "My frequency is too high — how do I manage audience fatigue?"
- "Plan a lead gen campaign for B2B on Facebook/Instagram"

For detailed Meta Ads API reference, pixel implementation, and advanced configurations, see [REFERENCE.md](REFERENCE.md).

## Hard Rules

These constraints must never be violated in recommendations:

1. **Pixel + CAPI both required.** Post-iOS 14.5, browser-only tracking loses 30-40% of conversion data.
2. **Event deduplication must be active** (event_id matching) — without it, conversions are double-counted.
3. **Event Match Quality ≥8.0** for Purchase event. Below 6.0 is critical.
4. **Budget must be ≥5x target CPA per ad set** — below this, the algorithm cannot exit learning phase.
5. **Never recommend edits during active learning phase** — wait for ~50 conversions/week or intentional reset.
6. **Creative fatigue = action required.** CTR decline >20% over 14 days with frequency >3 = replace creative immediately.
7. **<30% of ad sets in Learning Limited** — above this threshold, consolidation is mandatory.
8. **Purchasers/converters must be excluded** from prospecting campaigns.
9. **Special Ad Categories must be declared** before campaign creation for Housing, Employment, Credit, and Financial Products.

## Scored Audit

When performing an account audit, load `skills/shared/scoring-system.md` for the weighted scoring algorithm and `CHECKS.md` for the 46-check Meta Ads audit checklist. Produce a health score (0-100, grade A-F) with Quick Wins and a prioritized action plan.
