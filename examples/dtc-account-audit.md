# Workflow: DTC Account Audit to Client Deck

**Skills used:** ICP Research, Klaviyo Analyst, Google Analytics, Pro Deck Builder
**Time:** ~45 minutes hands-on, mostly waiting for Claude
**Output:** Polished audit deck ready to present to a client or stakeholder

---

## The Scenario

You're onboarding a new DTC e-commerce client. You need to understand their customer, audit their Klaviyo and GA4 setup, and deliver a professional deck summarizing findings and recommendations — all before the first strategy call.

## Step 1: Build the ICP (ICP Research)

Start by understanding who the client's customers actually are.

```
Build an ICP for [brand name] — they sell [product category] direct-to-consumer,
price point $[X]-$[Y], primary channel is [Instagram/TikTok/etc].
Include pain points, buying triggers, objections, and where this audience
gathers online.
```

**What you get:** A structured customer profile with psychographics, objections, community research, and messaging angles. Save this — the next skills will reference it.

## Step 2: Audit Klaviyo (Klaviyo Analyst)

With the ICP context loaded, audit the email/SMS program.

```
Run a full Klaviyo audit for this account. Here's the ICP we built:
[paste ICP output or reference the file]

Focus on: flow coverage gaps, segment health, deliverability,
and revenue attribution. Flag anything misaligned with the ICP.
```

**What you get:** A 4-phase audit covering flows, segments, campaigns, and deliverability — with specific recommendations tied to the customer profile you just built.

> **Tip:** If you have the Klaviyo MCP server configured, Claude pulls live data directly. Otherwise, export your flow list and metrics from Klaviyo and paste them in.

## Step 3: Audit GA4 (Google Analytics)

Now check the analytics layer.

```
Analyze this GA4 property for [brand name]. Compare against the ICP
and Klaviyo audit findings. I want to understand:
- Which channels drive the highest-value traffic
- Where the conversion funnel leaks
- Whether email/SMS attribution aligns with what Klaviyo reports
```

**What you get:** Channel analysis, funnel diagnostics, and cross-platform attribution comparison — grounded in the ICP and Klaviyo findings from earlier steps.

## Step 4: Build the Deck (Pro Deck Builder)

Package everything into a client-ready deliverable.

```
Create an audit deck from today's analysis. Include:
- ICP summary (1 slide)
- Klaviyo audit findings with severity ratings (2-3 slides)
- GA4 traffic and funnel analysis (2 slides)
- Cross-platform gaps and recommendations (1-2 slides)
- Prioritized action plan with quick wins and strategic plays (1 slide)

Use dark section dividers between major sections.
```

**What you get:** A polished HTML deck with dark covers, warm content slides, metric cards, and a prioritized recommendation section — ready to export to PDF and present.

---

## Why This Works

Each skill adds a layer of context that the next skill uses:

```
ICP Research → customer understanding
    ↓
Klaviyo Analyst → email/SMS audit grounded in ICP
    ↓
Google Analytics → traffic/funnel audit cross-referenced with email findings
    ↓
Pro Deck Builder → everything packaged into a professional deliverable
```

Without chaining, you'd get four disconnected analyses. With chaining, each step builds on the last — the Klaviyo audit flags gaps *relative to the ICP*, the GA4 analysis checks attribution *against Klaviyo findings*, and the deck synthesizes *all three layers* into a coherent story.

## Variations

- **Add Shopify:** Insert a Shopify store audit between GA4 and the deck for a complete e-commerce picture
- **Add Looker Studio:** After the deck, build a live dashboard the client can monitor ongoing
- **Skip the ICP:** If you already know the customer well, start at Step 2
