Customer retention analysis, churn prediction, cohort analysis, win-back campaigns, and loyalty program design. Use when the user asks about churn, retention, customer lifetime value, cohort analysis, or win-back strategies.


# Retention & Churn Prevention

Analyze churn, predict at-risk customers, and design retention strategies.

## Churn Analysis Framework

### Churn Types

| Type | Definition | Signal |
|------|-----------|--------|
| **Voluntary** | Customer actively cancels | Cancellation request, downgrade |
| **Involuntary** | Payment failure, card expiry | Failed charge, dunning |
| **Silent** | Stops using but does not cancel | Usage decline, no logins |

### Churn Rate Calculation

```
Monthly churn rate = Customers lost / Customers at start of month
Annual churn rate = 1 - (1 - monthly rate)^12
Net revenue retention = (Start MRR + Expansion - Contraction - Churn) / Start MRR
```

### Benchmarks

| Metric | Excellent | Good | Concerning |
|--------|----------|------|-----------|
| Monthly churn (SaaS) | <1% | 1-2% | >3% |
| Annual churn (SaaS) | <5% | 5-10% | >15% |
| Net revenue retention | >120% | 100-120% | <100% |

## Customer Health Scoring

| Signal | Weight | Healthy | At Risk |
|--------|--------|---------|---------|
| Product usage | 25% | Daily/weekly | Monthly or less |
| Feature adoption | 20% | 5+ features | 1-2 features |
| Support sentiment | 15% | Positive/none | Negative |
| Billing health | 15% | On time, expanding | Late, downgrading |
| Engagement | 15% | Opens, clicks | Ignores |
| NPS/CSAT | 10% | Promoter (9-10) | Detractor (0-6) |

## Early Warning Signals

| Timeframe | Signal | Action |
|-----------|--------|--------|
| 7 days | Login frequency drops 50%+ | In-app nudge, value reminder |
| 14 days | Key feature usage stops | CS outreach, usage tips |
| 30 days | No logins for 2+ weeks | Personal CS email, re-engagement |
| 60 days | NPS detractor, unresolved ticket | Executive escalation, save offer |
| 90 days | Cancellation signals | Retention call, custom offer |

## Win-Back Campaigns

### Timing

| Post-Churn Period | Response Rate | Approach |
|------------------|---------------|----------|
| 0-7 days | 15-25% | Immediate save, address exit reason |
| 7-30 days | 8-15% | New feature announcement, incentive |
| 30-90 days | 3-8% | Major update, significant discount |
| 90+ days | <3% | Annual check-in |

### Win-Back Sequence

```
Email 1 (Day 1): Address exit reason, offer to help
Email 2 (Day 7): New features since they left
Email 3 (Day 14): Comeback incentive (discount or extended trial)
Email 4 (Day 30): Final offer with urgency
```

## Retention Levers

1. **Onboarding** — Time to first value predicts retention more than any other factor
2. **Engagement loops** — Regular touchpoints (weekly reports, digests)
3. **Feature adoption** — Users who adopt 3+ features churn 50% less
4. **Community** — Community members have 2-3x higher retention
5. **Switching costs** — Integrations and data create healthy lock-in
6. **Proactive support** — Reach out before problems become cancellations

## CLV Calculation

```
Simple CLV = ARPU / Monthly Churn Rate
Full CLV = ARPU * Gross Margin % * (1 / Churn Rate)
CLV:CAC ratio target: >3:1
```

## Integration with Other Skills


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
