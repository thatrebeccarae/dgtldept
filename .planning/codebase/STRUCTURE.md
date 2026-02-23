# Codebase Structure

**Analysis Date:** 2026-02-19

## Directory Layout

```
claude-code-skills/
├── .git/                           # Git repository
├── .gitignore                      # Ignore .env, node_modules, etc.
├── .planning/                      # Planning documents (generated)
│   └── codebase/
├── README.md                       # Project overview and quick start
├── LICENSE                         # MIT license
│
├── skills/                         # Individual skills (installable via ~/.claude/skills/)
│   └── linkedin-data-viz/
│       ├── SKILL.md                # Skill definition (name, description, triggers, wizard flow)
│       ├── REFERENCE.md            # Technical reference (CSV schemas, algorithms, quirks)
│       ├── scripts/                # Data processing pipeline
│       │   ├── parse_export.py     # Parse LinkedIn CSV exports → parsed.json
│       │   ├── analyze.py          # Analyze parsed data → analysis.json
│       │   ├── generate_viz.py     # Inject data into templates → HTML files
│       │   └── sanitize.py         # Strip PII from analysis data
│       ├── templates/              # HTML templates with {{DATA}} and {{THEME_CSS}} placeholders
│       │   ├── 01-network-universe.html
│       │   ├── 02-inferences-vs-reality.html
│       │   ├── 03-high-value-messages.html
│       │   ├── 04-company-follows.html
│       │   ├── 05-inbound-outbound.html
│       │   ├── 06-connection-quality.html
│       │   ├── 07-connection-timeline.html
│       │   ├── 08-inbox-quality.html
│       │   ├── 09-posting-correlation.html
│       │   ├── 10-career-strata.html
│       │   ├── unified-dashboard.html
│       │   └── base.html            # Base template structure (partial)
│       ├── assets/                 # Static assets
│       │   └── carrier-dark.css     # Default theme (dark mode SaaS aesthetic)
│       ├── references/             # Skill-specific reference materials
│       │   └── prompts.md           # Example prompts for narrative insights
│       ├── demo/                   # Live demo output (demo/index.html)
│       │   └── index.html
│       └── scripts/                # (duplicate of scripts/ above for clarity)
│
└── skill-packs/                    # Collections of related skills
    ├── marketing-skills/           # Skills for content and marketing
    │   └── .git/
    │   └── Skills for Claude/      # (Content folder)
    │
    └── dtc-skill-pack/         # Complete DTC marketing toolkit
        ├── README.md               # Overview, quick start, setup wizard
        ├── GETTING_STARTED.md      # Step-by-step setup for each skill
        ├── scripts/
        │   └── setup.py            # Interactive wizard: check prereqs, install deps, test connections
        │
        ├── klaviyo-analyst/        # Audit flows, segments, campaigns, revenue
        │   ├── SKILL.md            # Skill definition + 4-phase audit framework
        │   ├── REFERENCE.md        # Benchmarks, analysis algorithms, three-tier recommendations
        │   ├── EXAMPLES.md         # Example prompts ("Audit my Klaviyo account", etc.)
        │   ├── .env.example        # Template: KLAVIYO_API_KEY
        │   ├── requirements.txt     # Python dependencies
        │   └── scripts/
        │       ├── analyze.py      # Main analyzer: flow audit, segment health, campaign compare, etc.
        │       └── klaviyo_client.py  # KlaviyoAnalyticsClient (API/MCP integration)
        │
        ├── klaviyo-developer/      # Build integrations, event tracking, webhooks
        │   ├── SKILL.md
        │   ├── REFERENCE.md        # Event schema best practices, SDK usage, webhook handling
        │   ├── EXAMPLES.md
        │   ├── .env.example
        │   ├── requirements.txt
        │   └── scripts/
        │       ├── dev_tools.py    # Integration audit, schema validation
        │       └── klaviyo_client.py  # KlaviyoDevClient
        │
        ├── shopify/                # Store performance, product velocity, customer cohorts
        │   ├── SKILL.md
        │   ├── REFERENCE.md
        │   ├── EXAMPLES.md
        │   ├── .env.example        # Template: SHOPIFY_API_KEY, SHOPIFY_STORE_URL
        │   ├── requirements.txt
        │   └── scripts/
        │       ├── analyze.py
        │       └── shopify_client.py  # ShopifyClient (Admin API)
        │
        ├── google-analytics/       # GA4 traffic, content, conversions
        │   ├── SKILL.md
        │   ├── REFERENCE.md
        │   ├── EXAMPLES.md
        │   ├── .env.example        # Template: GA4_PROPERTY_ID, GA4_CREDENTIALS_JSON
        │   ├── requirements.txt
        │   └── scripts/
        │       ├── analyze.py
        │       └── ga_client.py     # GoogleAnalyticsClient (Data API v1)
        │
        ├── looker-studio/          # Cross-platform dashboards via Google Sheets
        │   ├── SKILL.md
        │   ├── REFERENCE.md        # Dashboard templates, calculated fields
        │   ├── EXAMPLES.md
        │   ├── .env.example        # Template: GOOGLE_SHEETS_CREDS, LOOKER_STUDIO_API_KEY
        │   ├── requirements.txt
        │   └── scripts/
        │       └── data_pipeline.py  # Push data to Google Sheets
        │
        ├── pro-deck-builder/       # Create PowerPoint decks (PptxGenJS)
        │   ├── SKILL.md            # Design language, color systems, font selection
        │   ├── REFERENCE.md        # PptxGenJS API, slide layout patterns, icon pipeline
        │   └── (no scripts; uses PptxGenJS directly)
        │
        └── demo/
            └── index.html          # Live demo of Klaviyo analysis
```

## Directory Purposes

**skills/**
- Purpose: Installable individual skills (each can be used standalone)
- Contains: Self-contained skill implementations
- Key files: SKILL.md (entry point), REFERENCE.md (technical details), scripts/ (execution)
- Installation: `cp -r skills/linkedin-data-viz ~/.claude/skills/`

**skill-packs/**
- Purpose: Thematic collections of related skills (DTC marketing, content, etc.)
- Contains: Multiple subdirectories, each a complete skill
- Common patterns: Shared setup.py, integrated documentation, cross-skill examples
- Installation: `python scripts/setup.py` or copy individual skills manually

**[skill-name]/scripts/**
- Purpose: Executable Python modules for data processing
- Contains: Data transformation pipeline stages (parse, analyze, generate, output)
- Naming: Stage-specific (`parse_export.py`, `analyze.py`, `generate_viz.py`, `sanitize.py`)
- Execution: Invoked by Claude via subprocess with command-line arguments
- Dependencies: stdlib only (no pip required) OR specified in `requirements.txt`

**[skill-name]/templates/**
- Purpose: HTML templates with data/theme injection points
- Contains: One template per visualization, plus dashboard template
- Placeholders: `{{DATA}}` (JSON data for JavaScript), `{{THEME_CSS}}` (injected CSS), `{{GENERATED_AT}}` (timestamp)
- Pattern: Self-contained HTML with inline JavaScript (D3.js, Chart.js); no server required
- Location: `skills/linkedin-data-viz/templates/` (other skills don't have templates)

**[skill-name]/assets/**
- Purpose: Static CSS themes and branding assets
- Contains: CSS files with CSS custom properties for customization
- Location: `skills/linkedin-data-viz/assets/carrier-dark.css` (dark-mode SaaS theme)
- Usage: Injected into HTML via `{{THEME_CSS}}` placeholder

**[skill-name]/.env.example**
- Purpose: Template for environment-variable configuration
- Contains: API keys, credentials, service URLs
- Usage: Copy to `.env`, add actual values, is read by scripts via `os.getenv()`
- Security: Actual `.env` files are gitignored (listed in `.gitignore`)

## Key File Locations

**Entry Points:**
- `skills/linkedin-data-viz/SKILL.md` - LinkedIn Data Viz skill definition (7-step wizard)
- `skill-packs/dtc-skill-pack/README.md` - Skill pack overview (6 skills, integration guide)
- `skill-packs/dtc-skill-pack/scripts/setup.py` - Interactive setup wizard for entire skill pack

**Configuration:**
- `skill-packs/dtc-skill-pack/*/`.env.example` - API key templates for each skill (Klaviyo, Shopify, GA4, Google Sheets)
- `skill-packs/dtc-skill-pack/*/requirements.txt` - Python dependencies per skill
- `.gitignore` - Excludes `.env`, `node_modules`, `.next`

**Core Logic:**
- `skills/linkedin-data-viz/scripts/parse_export.py` - CSV parsing + LinkedIn quirk handling (470 lines)
- `skills/linkedin-data-viz/scripts/analyze.py` - Analysis algorithms (network quality, connection categorization, posting correlation) (816 lines)
- `skills/linkedin-data-viz/scripts/generate_viz.py` - Template injection + HTML generation (342 lines)
- `skill-packs/dtc-skill-pack/klaviyo-analyst/scripts/analyze.py` - Klaviyo analysis: flow audit, benchmarking (879 lines)
- `skill-packs/dtc-skill-pack/klaviyo-analyst/scripts/klaviyo_client.py` - Klaviyo API client (415 lines)

**Testing & Demo:**
- `skills/linkedin-data-viz/demo/` - Live demo output (index.html with real visualization data)
- `skill-packs/dtc-skill-pack/demo/index.html` - Demo of Klaviyo analysis output

**Documentation:**
- `README.md` - Project overview, skills summary table, quick start for each skill
- `skills/linkedin-data-viz/REFERENCE.md` - CSV schemas, parsing quirks, analysis algorithms, theme customization (detailed)
- `skill-packs/dtc-skill-pack/klaviyo-analyst/REFERENCE.md` - Benchmarks, flow checklist, analysis framework, three-tier recommendations
- `skill-packs/dtc-skill-pack/GETTING_STARTED.md` - Step-by-step manual setup (API keys, MCP server, dependencies)

## Naming Conventions

**Files:**
- Skills and features: `lowercase-with-hyphens.md` (e.g., `linkedin-data-viz`, `pro-deck-builder`)
- Scripts: `lowercase_with_underscores.py` (e.g., `parse_export.py`, `klaviyo_client.py`)
- Templates: `NN-description.html` where NN is 2-digit sequence (e.g., `01-network-universe.html`, `unified-dashboard.html`)
- Themes/assets: `descriptor-name.css` (e.g., `carrier-dark.css`)
- Configuration: `.env`, `.env.example`
- Documentation: UPPERCASE with topic (e.g., `SKILL.md`, `REFERENCE.md`, `EXAMPLES.md`, `GETTING_STARTED.md`)

**Directories:**
- Skill names: `lowercase-with-hyphens` (e.g., `linkedin-data-viz`, `klaviyo-analyst`, `pro-deck-builder`)
- Function directories: `lowercase` (e.g., `scripts`, `templates`, `assets`, `references`, `demo`)
- Special: `.planning`, `.git`

## Where to Add New Code

**New Skill (independent feature):**
- Create: `skills/{skill-name}/`
  - `SKILL.md` - Define name, description, triggers, wizard flow (required)
  - `REFERENCE.md` - Technical details (optional but recommended)
  - `EXAMPLES.md` - Example prompts (optional)
  - `scripts/` - Python modules for execution
  - `templates/` - HTML templates if generating HTML output
  - `assets/` - CSS/images if needed
  - `.env.example` - If using API keys

**New Skill in Existing Pack:**
- Create: `skill-packs/{pack-name}/{skill-name}/`
- Same structure as above (SKILL.md, REFERENCE.md, EXAMPLES.md, scripts/, etc.)
- Add entry to `skill-packs/{pack-name}/README.md` skills table
- Add setup instructions to `skill-packs/{pack-name}/GETTING_STARTED.md` if required

**New Script in Existing Skill:**
- Add to: `skills/{skill-name}/scripts/` or `skill-packs/{pack-name}/{skill-name}/scripts/`
- Follow pipeline naming: `parse_*.py`, `analyze_*.py`, `generate_*.py`, or `*_client.py`
- Use only stdlib imports, or add to `requirements.txt` and update `setup.py`
- Test via Claude's subprocess invocation in SKILL.md wizard flow

**New Template:**
- Add to: `skills/{skill-name}/templates/`
- Use template naming: `NN-description.html` (follow numeric sequence)
- Include `{{DATA}}` placeholder for JSON injection, `{{THEME_CSS}}` for theme
- Ensure self-contained HTML (inline CSS, inline JavaScript)
- Update `generate_viz.py` INDIVIDUAL_TEMPLATES dict to include new file

**New Theme/Asset:**
- Add to: `skills/{skill-name}/assets/`
- CSS files with CSS custom properties (for user customization)
- Reference in REFERENCE.md under "Customization" section
- Update generate_viz.py or skill's theme selection to offer as option

**Utilities or Shared Code:**
- For repeated logic across multiple skills, create in `skill-packs/{pack-name}/scripts/` if pack-specific
- If truly shared across packs, document in root README.md and link to implementation
- Current pattern: Each skill is isolated; client classes are duplicated (e.g., `klaviyo_client.py` exists in both analyst and developer skills)

## Special Directories

**[skill-name]/demo/**
- Purpose: Live demo output or sample generated files
- Generated: Yes (by running skill on sample data)
- Committed: Yes (to GitHub for live preview)
- Examples:
  - `skills/linkedin-data-viz/demo/` - Contains sample visualizations (index.html with generated HTML files)
  - `skill-packs/dtc-skill-pack/demo/index.html` - Sample Klaviyo analysis dashboard

**.planning/**
- Purpose: Project planning and codebase documentation
- Generated: Yes (by GSD orchestrator agents)
- Committed: Yes (to track planning history)
- Contents: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, CONCERNS.md, STACK.md, INTEGRATIONS.md

**.git/**
- Purpose: Git repository metadata
- Generated: Yes (by git init)
- Committed: Yes (essential for version control)

## Installation and Use Patterns

**Pattern 1: Individual Skill Copy**
```bash
cp -r skills/linkedin-data-viz ~/.claude/skills/
# User can now say "Analyze my LinkedIn data export" to Claude
```

**Pattern 2: Skill Pack Setup Wizard**
```bash
cd skill-packs/dtc-skill-pack
python scripts/setup.py
# Wizard: Python version check → API key setup → dependency install → connection test
```

**Pattern 3: Manual Multi-Skill Installation**
```bash
for skill in klaviyo-analyst klaviyo-developer shopify looker-studio pro-deck-builder; do
  cp -r skill-packs/dtc-skill-pack/$skill ~/.claude/skills/
done
```

**Pattern 4: Skip Setup, Copy Skills Directly**
```bash
# If you already have API keys in ~/.env or system env vars
cp -r skill-packs/dtc-skill-pack/* ~/.claude/skills/
```

---

*Structure analysis: 2026-02-19*
