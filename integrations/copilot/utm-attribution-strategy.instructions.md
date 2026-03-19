UTM parameter strategy, campaign tracking, and marketing attribution modeling. Build consistent UTM taxonomies, configure attribution models, measure cross-channel performance, and connect marketing spend to revenue. Use when the user asks about UTM parameters, campaign tracking, attribution models, marketing measurement, or cross-channel analytics.


# UTM & Attribution Strategy

Campaign tracking with UTM parameters and marketing attribution modeling.

## UTM Parameter Reference

### The 5 Standard UTM Parameters

| Parameter | Purpose | Required | Example |
|-----------|---------|----------|---------|
| `utm_source` | Where traffic comes from | Yes | google, linkedin, newsletter |
| `utm_medium` | Marketing medium/channel | Yes | cpc, email, social, referral |
| `utm_campaign` | Campaign name | Yes | spring-sale, product-launch-q1 |
| `utm_term` | Paid keyword (search ads) | No | email+marketing+software |
| `utm_content` | Differentiate ad variants | No | cta-button, sidebar-banner, video-ad |

### UTM Naming Convention

**Rules:**
- All lowercase (Google Analytics is case-sensitive)
- Use hyphens (`-`) as word separators, never spaces or underscores
- Be descriptive but concise
- Use consistent vocabulary across all teams
- Document your taxonomy and enforce it

### Recommended Taxonomy

#### utm_source

| Value | When to Use |
|-------|------------|
| `google` | Google Ads, Google organic |
| `facebook` | Meta/Facebook ads and organic |
| `instagram` | Instagram ads and organic |
| `linkedin` | LinkedIn ads and organic |
| `tiktok` | TikTok ads |
| `twitter` | Twitter/X |
| `youtube` | YouTube ads and organic |
| `bing` | Microsoft/Bing ads |
| `newsletter` | Your email newsletter |
| `email` | Transactional or one-off emails |
| `partner-[name]` | Partner/affiliate traffic |
| `podcast-[name]` | Podcast mentions |

#### utm_medium

| Value | When to Use |
|-------|------------|
| `cpc` | Paid search (cost per click) |
| `paid-social` | Paid social media |
| `social` | Organic social media |
| `email` | Email marketing |
| `referral` | Partner/affiliate referrals |
| `display` | Display/banner ads |
| `video` | Video ads (pre-roll, in-stream) |
| `retargeting` | Retargeting/remarketing |
| `influencer` | Influencer partnerships |
| `organic` | Organic search (usually auto-tagged) |
| `direct` | Direct traffic (usually auto-tagged) |

#### utm_campaign

**Pattern:** `[initiative]-[audience]-[date]`

Examples:
- `spring-sale-2026`
- `product-launch-enterprise-q1`
- `webinar-seo-masterclass-mar2026`
- `blog-weekly-digest-w12`
- `retarget-cart-abandoners-mar`

#### utm_content

**Pattern:** `[format]-[variant]-[placement]`

Examples:
- `video-testimonial-feed`
- `carousel-product-stories`
- `cta-start-trial-hero`
- `banner-logo-sidebar`
- `text-ad-headline-v2`

## UTM Builder

### URL Structure

```
https://example.com/landing-page?utm_source=linkedin&utm_medium=paid-social&utm_campaign=product-launch-q1&utm_content=video-demo-feed
```

### Common UTM Templates


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
