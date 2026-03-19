# utm-attribution-strategy


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

| Channel | Full UTM String |
|---------|----------------|
| Google Search Ad | `?utm_source=google&utm_medium=cpc&utm_campaign=[campaign]&utm_term=[keyword]&utm_content=[ad-group]` |
| Facebook Ad | `?utm_source=facebook&utm_medium=paid-social&utm_campaign=[campaign]&utm_content=[ad-name]` |
| LinkedIn Ad | `?utm_source=linkedin&utm_medium=paid-social&utm_campaign=[campaign]&utm_content=[creative-type]` |
| Email Newsletter | `?utm_source=newsletter&utm_medium=email&utm_campaign=[newsletter-name]-[date]&utm_content=[link-position]` |
| Organic LinkedIn Post | `?utm_source=linkedin&utm_medium=social&utm_campaign=[post-topic]` |
| Partner Referral | `?utm_source=partner-[name]&utm_medium=referral&utm_campaign=[initiative]` |

## Attribution Models

### Model Comparison

| Model | How It Works | Best For | Limitation |
|-------|-------------|----------|-----------|
| **Last Click** | 100% credit to last touchpoint | Short sales cycles, direct response | Ignores awareness/consideration |
| **First Click** | 100% credit to first touchpoint | Brand awareness measurement | Ignores conversion-driving touches |
| **Linear** | Equal credit to all touchpoints | Simple multi-touch view | Over-credits low-impact touches |
| **Time Decay** | More credit to recent touches | Long sales cycles with clear momentum | Under-values early awareness |
| **Position-Based** | 40% first, 40% last, 20% middle | Balanced view of full funnel | Arbitrary weight distribution |
| **Data-Driven** | ML-based credit allocation | Large datasets (1000+ conversions) | Black box, requires volume |

### GA4 Attribution

GA4 uses data-driven attribution by default. Key settings:
- **Reporting attribution model**: Set in Admin > Attribution Settings
- **Lookback window**: 30 days (click) / 7 days (view) default
- **Conversion paths**: Analyze in Advertising > Attribution > Conversion Paths

### Choosing a Model

```
Sales cycle < 7 days → Last Click or Data-Driven
Sales cycle 7-30 days → Position-Based or Data-Driven
Sales cycle > 30 days → Time Decay or Data-Driven
Brand awareness focus → First Click
Performance marketing focus → Last Click
Balanced view needed → Position-Based
1000+ monthly conversions → Data-Driven (always)
```

## UTM Audit Checklist

- [ ] All paid campaigns have UTM parameters
- [ ] Naming convention documented and shared with team
- [ ] No mixed case (utm_source=Google vs google)
- [ ] No spaces in parameter values (use hyphens)
- [ ] utm_medium values align with GA4 default channel groupings
- [ ] Internal links do NOT have UTM parameters (breaks attribution)
- [ ] UTM parameters are on the landing page URL, not post-redirect
- [ ] No PII in UTM parameters (names, emails, account IDs)
- [ ] Short URLs / link shorteners preserve UTM parameters
- [ ] Redirects preserve UTM parameters (302s can strip them)

## Common Mistakes

1. **UTMs on internal links** — breaks session attribution, inflates source counts
2. **Inconsistent naming** — `Facebook` vs `facebook` vs `fb` creates 3 separate sources
3. **Missing utm_medium** — traffic falls into "(other)" channel grouping
4. **Non-standard utm_medium values** — use GA4 recognized values for proper channel grouping
5. **UTMs on organic search results** — Google auto-tags organic; adding UTMs creates duplicate sources
6. **PII in UTM parameters** — email addresses or user IDs in URLs violate privacy policies
7. **Forgetting post-click tracking** — UTMs track the click, not what happens after

## Integration with Other Skills

- **google-analytics** — UTM data flows into GA4 for analysis
- **google-ads** — Google auto-tags with gclid; UTMs are supplementary
- **facebook-ads** — Meta auto-tags with fbclid; UTMs needed for GA4 attribution
- **linkedin-ads** — LinkedIn requires manual UTM configuration
- **tiktok-ads** — TikTok requires manual UTM configuration
