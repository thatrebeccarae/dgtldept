<div align="center">

# Claude Code Skills

**Production-tested skill packs that give Claude Code deep expertise in DTC marketing, data visualization, and presentation generation.**

[![GitHub stars](https://img.shields.io/github/stars/thatrebeccarae/claude-code-skills?style=for-the-badge&logo=github&color=181717)](https://github.com/thatrebeccarae/claude-code-skills/stargazers)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Rebecca%20Rae%20Barton-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/rebeccaraebarton)
[![Substack](https://img.shields.io/badge/Substack-dgtl%20dept*-FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://dgtldept.substack.com/welcome)
[![X](https://img.shields.io/badge/X-@thatrebeccarae-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/thatrebeccarae)
[![Website](https://img.shields.io/badge/rebeccaraebarton.com-4A90D9?style=for-the-badge&logo=google-chrome&logoColor=white)](https://rebeccaraebarton.com)

```bash
git clone https://github.com/thatrebeccarae/claude-code-skills.git
```

**Works on Mac, Windows, and Linux.**

<br>

<a href="https://thatrebeccarae.github.io/claude-code-skills/skill-packs/dtc-skill-pack/demo/">
  <img src="assets/terminal.svg" alt="DTC Skill Pack installation" width="760">
</a>

<br>

<!--
### What people are saying

> "Quote here" — **Name**, Role at Company

> "Quote here" — **Name**, Role at Company

> "Quote here" — **Name**, Role at Company
-->

[Why I Built This](#why-i-built-this) · [Skill Packs](#skill-packs) · [Quick Start](#quick-start) · [How It Works](#how-it-works) · [Contributing](CONTRIBUTING.md)

</div>

---

## Why I Built This

Claude Code is powerful out of the box — but it doesn't know the difference between a good and great abandoned cart flow. It can't tell you that a 1.2% click rate on your welcome series is below benchmark, or that your Shopify checkout completion rate signals a shipping cost surprise.

I kept having the same experience: Claude would give me a structurally correct answer that missed the domain context entirely. It would suggest a welcome flow without knowing that best-in-class DTC brands send 4-7 messages over 14 days, not 3 messages over a week. It would analyze GA4 data without knowing which metrics actually matter for e-commerce.

The insight was simple: **domain expertise beats general intelligence for operational work.** A senior DTC consultant doesn't just know the tools — they know the benchmarks, the patterns, the diagnostic frameworks that separate useful analysis from surface-level summaries.

That's what these skills add. Real benchmarks. Real frameworks. The same diagnostic patterns I use in my own consulting work. Install what you need, ask in plain English, get implementation-ready answers.

## Who This Is For

- **DTC marketers** who want Claude to actually understand their stack
- **Email and CRM operators** running Klaviyo, Shopify, or GA4
- **Growth teams** that need cross-platform analysis, not platform-by-platform reports
- **Agencies and consultants** who want to scale their diagnostic process
- **Shopify merchants** trying to figure out why checkout completion is 31%

If you want implementation-ready answers — not tutorials, not blog-post-level overviews — these skills are for you.

## Skill Packs

### [DTC Skill Pack](skill-packs/dtc-skill-pack/) — 6 skills for e-commerce marketing

> [**View Live Demo**](https://thatrebeccarae.github.io/claude-code-skills/skill-packs/dtc-skill-pack/demo/) — See all 6 skills in action with example terminal output.

| Skill | What Claude Can Do |
|-------|-------------------|
| **[Klaviyo Analyst](skill-packs/dtc-skill-pack/klaviyo-analyst/)** | 4-phase account audit, flow gap analysis, segment health, deliverability diagnostics, revenue attribution, three-tier recommendations with implementation specs |
| **[Klaviyo Developer](skill-packs/dtc-skill-pack/klaviyo-developer/)** | Event schema design, SDK integration, webhook handling, rate limit strategy, catalog sync, integration health audit |
| **[Shopify](skill-packs/dtc-skill-pack/shopify/)** | 12-step store audit, conversion funnel analysis, site speed diagnostics, marketing stack integration |
| **[Google Analytics](skill-packs/dtc-skill-pack/google-analytics/)** | GA4 traffic analysis, channel comparison, conversion funnels, content performance |
| **[Looker Studio](skill-packs/dtc-skill-pack/looker-studio/)** | Cross-platform dashboards via Google Sheets pipeline, DTC dashboard templates, calculated field library |
| **[Pro Deck Builder](skill-packs/dtc-skill-pack/pro-deck-builder/)** | Polished HTML slide decks and PDF-ready reports with dark cover pages and warm light content slides |

### [LinkedIn Data Viz](skills/linkedin-data-viz/) — Interactive career visualizations

> [**View Live Demo**](https://thatrebeccarae.github.io/claude-code-skills/skills/linkedin-data-viz/demo/)

Turn a LinkedIn data export into 9 interactive visualizations: D3.js network graphs, Chart.js charts, career timelines. Includes onboarding wizard, dark theme, and privacy-safe sanitization for publishing.

### Coming Soon

Additional marketing skill packs are in development — covering paid media, content strategy, and multi-channel attribution. [Star the repo](https://github.com/thatrebeccarae/claude-code-skills/stargazers) to get notified when they drop.

## Quick Start

### Setup Wizard (Recommended)

```bash
git clone https://github.com/thatrebeccarae/claude-code-skills.git
cd claude-code-skills/skill-packs/dtc-skill-pack
python scripts/setup.py
```

The wizard checks prerequisites, walks you through API key setup, installs dependencies, and tests connections.

<details>
<summary><strong>Manual install (skip the wizard)</strong></summary>

```bash
# Copy all 6 skills to Claude Code
for skill in klaviyo-analyst klaviyo-developer google-analytics shopify looker-studio pro-deck-builder; do
  cp -r claude-code-skills/skill-packs/dtc-skill-pack/$skill ~/.claude/skills/
done
```

See [GETTING_STARTED.md](skill-packs/dtc-skill-pack/GETTING_STARTED.md) for detailed API key setup per platform.

</details>

<details>
<summary><strong>LinkedIn Data Viz install</strong></summary>

```bash
git clone https://github.com/thatrebeccarae/claude-code-skills.git
cp -r claude-code-skills/skills/linkedin-data-viz ~/.claude/skills/
```

Then say: **"Analyze my LinkedIn data export"**

</details>

## Example Prompts

```
"Audit my Klaviyo flows and identify which essential flows I'm missing"

"My checkout completion rate is 31% — what's causing the drop-off?"

"Which traffic sources are driving the most conversions this month?"

"Plan a CRM dashboard reconciling Klaviyo and Shopify data"

"Create a dark-mode deck summarizing this month's email performance"

"Debug why my webhook events aren't triggering flows"
```

## How It Works

Claude Code skills are structured knowledge packs that load automatically when you invoke them. Each skill gives Claude specific domain expertise it doesn't have out of the box.

### What a Skill Contains

| File | Purpose |
|------|---------|
| **SKILL.md** | Frontmatter + instructions Claude reads at invocation — frameworks, decision trees, diagnostic patterns |
| **REFERENCE.md** | Platform-specific data: industry benchmarks, API schemas, field mappings, rate limits |
| **EXAMPLES.md** | Working examples with realistic prompts and expected output format |
| **scripts/** | Utility scripts for setup, data fetching, health checks (where applicable) |

### How Claude Uses Them

1. You ask a question in natural language (e.g., *"Audit my Klaviyo flows"*)
2. Claude loads the relevant skill's SKILL.md, which contains the diagnostic framework
3. Claude references REFERENCE.md for benchmarks, thresholds, and platform-specific data
4. If an MCP server is configured (e.g., Klaviyo), Claude pulls live data from your account
5. Claude delivers structured analysis with specific recommendations — not generic advice

Skills work without MCP servers too. You can paste data, share screenshots, or use the included scripts to export data manually. The MCP server just makes it seamless.

## Configuration

### Setup Wizard Options

| Flag | What It Does |
|------|-------------|
| `python scripts/setup.py` | Full interactive setup |
| `--skip-install` | Skip dependency installation |
| `--skills klaviyo,shopify` | Install specific skills only |
| `--non-interactive` | Use environment variables, skip prompts |

### API Keys by Platform

| Platform | Key Required | Where to Get It |
|----------|-------------|-----------------|
| **Klaviyo** | Private API Key (`pk_...`) | Klaviyo > Settings > API Keys |
| **Google Analytics** | Service account JSON + Property ID | Google Cloud Console > IAM > Service Accounts |
| **Shopify** | Admin API access token | Shopify Admin > Apps > Develop Apps |
| **Looker Studio** | Google Sheets API credentials | Google Cloud Console > APIs & Services |

<details>
<summary><strong>Klaviyo MCP server setup</strong></summary>

The [Klaviyo MCP server](https://developers.klaviyo.com/en/docs/klaviyo_mcp_server) gives Claude direct access to your Klaviyo account data.

1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Add to `~/.mcp.json`:

```json
{
  "mcpServers": {
    "klaviyo": {
      "command": "uvx",
      "args": ["klaviyo-mcp-server@latest"],
      "env": {
        "PRIVATE_API_KEY": "${KLAVIYO_API_KEY}",
        "READ_ONLY": "true",
        "ALLOW_USER_GENERATED_CONTENT": "false"
      }
    }
  }
}
```

3. Restart Claude Code and verify with `/mcp`

See the [DTC Skill Pack README](skill-packs/dtc-skill-pack/README.md) for recommended Klaviyo API scopes.

</details>

## Security

All scripts include input validation, path sanitization, SSRF protection, and secure credential handling. Key principles:

- **API keys** stored in `.env` files (gitignored), never hardcoded
- **Read-only API access** by default — write scopes are opt-in
- **No PII extraction** — skills work with aggregates, not individual customer data
- **No persistent storage** — analysis runs in-memory, output goes to local files you control

For vulnerability reporting and full security design details, see [SECURITY.md](SECURITY.md).

## Troubleshooting

<details>
<summary><strong>Skills not loading in Claude Code</strong></summary>

1. Verify skills are in the right directory: `ls ~/.claude/skills/`
2. Each skill folder should contain at least a `SKILL.md` file
3. Restart Claude Code after copying skills
4. Check that SKILL.md frontmatter is valid YAML

</details>

<details>
<summary><strong>API key errors</strong></summary>

1. Confirm your `.env` file is in the project root (not inside a skill folder)
2. Klaviyo keys must start with `pk_` — if yours doesn't, you may have copied a public key
3. Google service account JSON path must be absolute, not relative
4. Run `python scripts/setup.py` to re-validate all keys

</details>

<details>
<summary><strong>Python version issues</strong></summary>

The setup wizard requires Python 3.8+. Check your version:

```bash
python --version
# or
python3 --version
```

On macOS, `python` may point to Python 2. Use `python3` explicitly or install via Homebrew: `brew install python`

</details>

<details>
<summary><strong>MCP server not connecting</strong></summary>

1. Verify `~/.mcp.json` syntax is valid JSON (no trailing commas)
2. Confirm `uv` is installed: `uv --version`
3. Check that your `KLAVIYO_API_KEY` environment variable is set: `echo $KLAVIYO_API_KEY`
4. Restart Claude Code — MCP servers load at startup

</details>

## Documentation

| Resource | Description |
|----------|-------------|
| [DTC Skill Pack README](skill-packs/dtc-skill-pack/README.md) | Skill details, architecture, MCP server setup, example prompts, FAQ |
| [DTC Getting Started](skill-packs/dtc-skill-pack/GETTING_STARTED.md) | Step-by-step setup for each platform |
| [LinkedIn Data Viz SKILL.md](skills/linkedin-data-viz/SKILL.md) | Wizard flow, visualization descriptions |
| [LinkedIn Data Viz REFERENCE.md](skills/linkedin-data-viz/REFERENCE.md) | CSV schemas, parsing quirks, theme customization |
| [CHANGELOG](CHANGELOG.md) | Version history and release notes |
| [SECURITY](SECURITY.md) | Security design and vulnerability reporting |
| [CONTRIBUTING](CONTRIBUTING.md) | How to contribute skills, report bugs, submit PRs |

## Contributing

Contributions are welcome — bug reports, documentation fixes, skill suggestions, and new skills. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting skills, the required file structure, and the PR process.

## License

[MIT](LICENSE) — built by [Rebecca Rae Barton](https://rebeccaraebarton.com)

<div align="center">

---

**Domain expertise > general intelligence.** Install the skills. Ask in plain English. Get answers that actually know your stack.

</div>
