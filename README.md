# Claude Code Skills

Open-source skill packs and custom skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (Anthropic's AI coding assistant). Give Claude deep platform expertise in DTC e-commerce marketing, data visualization, and presentation generation. Install a skill and use natural language to audit Klaviyo, Shopify, and GA4 accounts, generate interactive visualizations, build polished decks, and more.

## What's Inside

| Skill | What Claude Can Do |
|-------|-------------------|
| **[LinkedIn Data Viz](skills/linkedin-data-viz/)** | Turn a LinkedIn data export into 9 interactive visualizations: D3.js network graphs, Chart.js charts, career timelines. Includes onboarding wizard, dark theme, and privacy-safe sanitization for publishing. [**Live Demo**](https://thatrebeccarae.github.io/claude-code-skills/skills/linkedin-data-viz/demo/) |
| **Klaviyo Analyst** | 4-phase account audit, flow gap analysis, segment health, deliverability diagnostics, revenue attribution, three-tier recommendations with implementation specs |
| **Klaviyo Developer** | Event schema design, SDK integration, webhook handling, rate limit strategy, catalog sync, integration health audit |
| **Shopify** | Store performance audit, product velocity, customer cohorts, conversion funnel analysis |
| **Google Analytics** | GA4 traffic analysis, channel comparison, conversion funnels, content performance |
| **Looker Studio** | Cross-platform dashboards via Google Sheets pipeline, DTC dashboard templates |
| **Pro Deck Builder** | Presentation-quality PowerPoint decks with dark/light modes (PptxGenJS) |

## Quick Start

### LinkedIn Data Viz

```bash
git clone https://github.com/thatrebeccarae/claude-code-skills.git
cp -r claude-code-skills/skills/linkedin-data-viz ~/.claude/skills/
```

Then in Claude Code, say: **"Analyze my LinkedIn data export"**

### DTC Skill Pack

```bash
cd claude-code-skills/skill-packs/dtc-skill-pack
python scripts/setup.py
```

The interactive wizard handles API keys, dependencies, and connection testing. For manual setup, see [GETTING_STARTED.md](skill-packs/dtc-skill-pack/GETTING_STARTED.md).

## Documentation

- [**LinkedIn Data Viz — SKILL.md**](skills/linkedin-data-viz/SKILL.md) — Skill definition, wizard flow, visualization descriptions
- [**LinkedIn Data Viz — REFERENCE.md**](skills/linkedin-data-viz/REFERENCE.md) — CSV schemas, parsing quirks, analysis algorithms, theme customization
- [**DTC Skill Pack — README**](skill-packs/dtc-skill-pack/README.md) — Skill details, MCP server setup, example prompts, FAQ
- [**DTC Skill Pack — Getting Started**](skill-packs/dtc-skill-pack/GETTING_STARTED.md) — Step-by-step setup for each platform

## Security

All scripts include input validation, path sanitization, SSRF protection, and secure credential handling. API keys are stored in `.env` files (gitignored) and never hardcoded.

## License

MIT
