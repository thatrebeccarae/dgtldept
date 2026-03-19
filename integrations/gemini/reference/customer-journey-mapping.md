# customer-journey-mapping


# Customer Journey Mapping

Map, analyze, and optimize the full customer journey from first touch to advocacy.

## Journey Stages

| Stage | Customer Goal | Key Channels | Metrics |
|-------|-------------|-------------|---------|
| **Awareness** | Discover a solution exists | SEO, social, ads, PR, referral | Impressions, reach, brand searches |
| **Consideration** | Evaluate options | Blog, reviews, comparison, webinar | Time on site, pages/session, content downloads |
| **Decision** | Choose and purchase | Pricing page, demo, trial, sales | Conversion rate, CAC, time to close |
| **Onboarding** | Get initial value | Welcome email, docs, setup wizard | Activation rate, time to value, support tickets |
| **Retention** | Continue getting value | Product, email, success team | NRR, usage frequency, NPS |
| **Advocacy** | Recommend to others | Referral, review, community | NPS, referral rate, review count |

## Journey Map Template

For each stage, document:

```markdown
### [Stage Name]

**Customer goal:** What are they trying to accomplish?
**Emotional state:** How do they feel? (confident, anxious, frustrated, delighted)
**Touchpoints:**
- [Channel 1]: [Specific interaction]
- [Channel 2]: [Specific interaction]

**Pain points:**
- [What causes friction or frustration]

**Opportunities:**
- [How to improve the experience]

**Key metric:** [Primary measurement]
**Drop-off risk:** [What causes people to leave at this stage]
```

## Touchpoint Inventory

### Common B2B SaaS Touchpoints

| Stage | Touchpoint | Owner |
|-------|-----------|-------|
| Awareness | Google search result | SEO/Content |
| Awareness | LinkedIn ad | Paid Media |
| Awareness | Blog post | Content |
| Consideration | Product page | Marketing |
| Consideration | Case study | Marketing |
| Consideration | Demo request form | Marketing |
| Decision | Sales demo | Sales |
| Decision | Pricing page | Product/Marketing |
| Decision | Proposal/contract | Sales |
| Onboarding | Welcome email sequence | CRM/CS |
| Onboarding | Setup wizard | Product |
| Onboarding | First value moment | Product |
| Retention | Feature adoption email | Product/CRM |
| Retention | QBR/check-in | CS |
| Retention | Product updates | Product |
| Advocacy | NPS survey | CS |
| Advocacy | Referral program | Growth |
| Advocacy | Case study request | Marketing |

## Drop-Off Analysis

### Identifying Drop-Offs

1. **Quantitative:** GA4 funnel reports, cohort analysis, conversion tracking
2. **Qualitative:** Session recordings, user interviews, support ticket themes
3. **Survey:** Post-interaction surveys at each stage transition

### Common Drop-Off Points

| Transition | Drop-Off Cause | Fix |
|-----------|---------------|-----|
| Awareness → Consideration | Irrelevant content, slow site | Better targeting, speed optimization |
| Consideration → Decision | No social proof, unclear pricing | Add reviews, transparent pricing |
| Decision → Onboarding | Complex signup, payment friction | Simplify form, offer trial |
| Onboarding → Retention | No clear first value, poor UX | Guided setup, time-to-value focus |
| Retention → Advocacy | No program, not asked | Referral program, NPS follow-up |

## Persona-Based Journeys

Different personas take different paths. Create journey variants for:
- **By role:** Technical evaluator vs executive buyer vs end user
- **By company size:** SMB (self-serve) vs enterprise (sales-assisted)
- **By intent:** Problem-aware vs solution-aware vs product-aware
- **By channel:** Inbound (SEO/content) vs outbound (sales/ads)

## Integration with Other Skills

- **google-analytics** — Pull funnel data and conversion paths
- **cro-auditor** — Deep-dive on high-drop-off pages
- **retention-churn-prevention** — Retention and advocacy stage optimization
- **icp-research** — Define personas for journey variants
