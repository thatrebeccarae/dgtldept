# Composing Skills

Skills are designed to work independently, but they're most powerful when chained together. Each skill's output becomes context for the next — building layers of analysis that a single skill can't achieve alone.

## How Skill Composition Works

Claude Code maintains context within a conversation. When you run one skill and then invoke another, Claude carries forward everything from the previous step. This means:

1. **You don't need special syntax** — just ask Claude to do the next thing
2. **Full context transfers** — findings, data, recommendations all carry forward
3. **Each skill adds a layer** — the second skill's output is informed by the first

### The Pattern

```
[Skill A] → produces analysis/data
    ↓ (context carries forward automatically)
[Skill B] → uses Skill A's output as input context
    ↓
[Skill C] → builds on both A and B
```

### In Practice

You don't need to copy-paste between steps. Just keep working in the same Claude Code session:

```
You:  "Audit my Klaviyo flows"
      → Claude loads klaviyo-analyst, produces audit

You:  "Now analyze my GA4 data and cross-reference with the Klaviyo findings"
      → Claude loads google-analytics, references the audit it just produced

You:  "Package both analyses into a client deck"
      → Claude loads pro-deck-builder, synthesizes everything into slides
```

### When to Start a New Session

Start fresh when:
- You're switching to an unrelated project or client
- The conversation is very long and Claude is losing earlier context
- You want a clean analysis without prior assumptions

### Tips

- **Reference earlier output explicitly** if you want Claude to focus on specific findings: *"The Klaviyo audit flagged 3 missing flows — make sure those appear in the deck recommendations"*
- **Order matters** — diagnostic skills (audits, research) should run before synthesis skills (decks, reports, restructuring plans)
- **Save intermediate output** — if a research brief or audit is particularly good, save it to a file so you can reference it in future sessions without re-running the skill

## Workflow Examples

| Workflow | Skills Used | What You Get |
|----------|------------|--------------|
| [DTC Account Audit](dtc-account-audit.md) | ICP Research → Klaviyo Analyst → Google Analytics → Pro Deck Builder | Client-ready audit deck |
| [Paid Media Optimization](paid-media-optimization.md) | Wasted Spend Finder → Competitor Ads Analyst → Google Ads → Account Structure Review | Exclusion lists + restructuring roadmap |
| [Content Production](content-production.md) | Research Digest → ICP Research → SEO Content Writer → Content Workflow | SEO article + social distribution pack |
