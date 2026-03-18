---
name: microsoft-ads
description: Microsoft Advertising (Bing Ads) platform expertise. Audit campaigns, keywords, audiences, and UET tracking. Use when the user asks about Microsoft Ads, Bing Ads, search advertising on Microsoft, LinkedIn audience targeting, or Performance Max campaigns on Microsoft.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: paid-media
  domain: microsoft-ads
  updated: 2026-03-11
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Microsoft Advertising (Bing Ads)

Expert-level guidance for Microsoft Advertising — auditing, building, and optimizing search, shopping, audience, and Performance Max campaigns.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/microsoft-ads ~/.claude/skills/
```

## Core Capabilities

### Campaign Auditing & Optimization
- Audit account structure, campaign settings, bid strategies, and budget allocation
- Review keyword match types, negative keywords, and search term reports
- Analyze quality scores and ad relevance
- Identify wasted spend and missed opportunity gaps

### Campaign Types
- **Search** — Text ads on Bing, Yahoo, DuckDuckGo, and partner sites
- **Shopping** — Product ads from Microsoft Merchant Center feed
- **Audience** — Native display ads on Microsoft Audience Network (MSN, Outlook, Edge)
- **Performance Max** — Automated cross-format campaigns (search, shopping, audience, display)
- **App Install** — Mobile app promotion campaigns
- **Dynamic Search** — Auto-generated ads from website content

### Audience Targeting
- **LinkedIn Profile Targeting** (Microsoft-exclusive) — Target by company, industry, job function
- In-market audiences, custom audiences, remarketing lists
- Customer match (email upload), similar audiences
- Combined audiences with AND/OR logic

### Tracking & Attribution
- UET (Universal Event Tracking) tag setup and validation
- Conversion goals: URL, event, duration, pages per visit, app install
- Offline conversion import (GCLID-based)
- Multi-touch attribution models
- Microsoft Clarity integration for session recordings

### Import & Sync
- Google Ads import (campaigns, keywords, ads, extensions)
- Scheduled sync from Google Ads (daily/weekly auto-import)
- Differences to watch: audience targeting, bid modifiers, ad formats, extensions

## Key Benchmarks

| Metric | Good | Great | Warning |
|--------|------|-------|---------|
| Search CTR | 3-5% | 6%+ | <2% |
| Search CPC | Typically 30-40% lower than Google Ads | — | Higher than Google |
| Conversion Rate | 3-5% | 6%+ | <2% |
| Quality Score | 7-8 | 9-10 | <6 |
| Impression Share | 60-70% | 80%+ | <40% |
| Search Term Relevance | 80%+ relevant | 90%+ | <60% |

## Microsoft Ads vs Google Ads

| Feature | Microsoft Ads | Google Ads |
|---------|--------------|------------|
| Search Volume | ~10-15% of Google | Dominant |
| Avg CPC | 30-40% lower | Higher |
| Audience | Older, higher income, desktop-heavy | Broader |
| Unique Targeting | LinkedIn Profile Targeting | None |
| Import | One-click from Google Ads | N/A |
| Shopping | Merchant Center (separate from Google) | Google Merchant Center |
| Performance Max | Available (newer) | More mature |

## Account Structure Best Practices

```
Account
├── Brand Search Campaign (Exact + Phrase)
│   ├── Brand Terms Ad Group
│   └── Brand + Product Ad Groups
├── Non-Brand Search Campaign (by theme)
│   ├── [Product/Service Category] Ad Groups
│   └── [High-Intent Keywords] Ad Groups
├── Shopping Campaign
│   ├── Priority: High (top products)
│   ├── Priority: Medium (categories)
│   └── Priority: Low (catch-all)
├── Audience Campaign (Audience Network)
│   ├── Remarketing
│   ├── In-Market
│   └── LinkedIn Targeting
├── Competitor Campaign (optional)
│   └── Competitor Brand Terms
└── Performance Max Campaign
    └── Asset Groups by theme
```

## Workflow: Full Account Audit

When asked to audit a Microsoft Ads account:

1. **Account Settings** — Conversion tracking (UET), attribution model, auto-tagging, time zone
2. **Campaign Structure** — Organization, naming conventions, budget distribution
3. **Keyword Analysis** — Match types, quality scores, search term relevance, negative keyword coverage
4. **Ad Copy Review** — RSA asset quality, ad extensions (sitelinks, callouts, structured snippets)
5. **Bid Strategy** — Manual vs automated, target CPA/ROAS, portfolio strategies
6. **Audience Targeting** — Remarketing lists, LinkedIn targeting, in-market audiences
7. **Shopping Feed** — Product data quality, feed errors, competitive pricing
8. **Budget Analysis** — Budget pacing, lost impression share (budget vs rank)
9. **Google Ads Sync** — Import freshness, divergence from Google, Microsoft-specific optimizations
10. **Recommendations** — Prioritized by expected ROAS impact

## How to Use This Skill

Ask me questions like:
- "Audit my Microsoft Ads account structure"
- "Help me set up LinkedIn Profile Targeting"
- "My Google Ads import isn't performing well on Microsoft — what should I change?"
- "Design a Shopping campaign structure for my product catalog"
- "What Microsoft-specific optimizations should I make beyond the Google import?"
- "Help me set up UET tracking and conversion goals"
- "Plan a Performance Max campaign on Microsoft"

For detailed Microsoft Ads API reference, UET implementation, and advanced configurations, see [REFERENCE.md](REFERENCE.md).

## Hard Rules

These constraints must never be violated in recommendations:

1. **UET tag must be verified and firing** before any optimization recommendations.
2. **Auto-tagging (MSCLKID) must be enabled** — without it, conversion tracking and analytics break.
3. **Brand syndication must be excluded** from brand campaigns — syndication network delivers low-quality traffic for brand terms.
4. **Google imports must be reviewed and adjusted** — raw imports without Microsoft-specific optimization waste the CPC advantage.
5. **Microsoft search terms must be reviewed independently** — different query patterns than Google, Google-imported negatives are insufficient.
6. **LinkedIn Profile Targeting must be tested** for any B2B account — it is Microsoft's unique differentiator.

## Scored Audit

When performing an account audit, load `skills/shared/scoring-system.md` for the weighted scoring algorithm and `CHECKS.md` for the 30-check Microsoft Ads audit checklist. Produce a health score (0-100, grade A-F) with Quick Wins and a prioritized action plan.
