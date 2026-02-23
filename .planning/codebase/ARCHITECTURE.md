# Architecture

**Analysis Date:** 2026-02-19

## Pattern Overview

**Overall:** Modular Skill-Based Architecture

This codebase implements a **skill pack system** where Claude Code skills are self-contained, independently deployable modules. Each skill defines its own entry points (via SKILL.md), requirements, and supporting scripts. Skills are grouped into two hierarchical levels: individual skills (`skills/`) and skill packs (`skill-packs/`) containing multiple related skills.

**Key Characteristics:**
- **Declarative skill definition** - Each skill has a SKILL.md file declaring its name, description, triggers, and wizard flow
- **Pipeline-based data processing** - Multi-stage data transformation (parse → analyze → generate/output)
- **Zero-dependency Python stdlib** - Core scripts use only Python 3.9+ stdlib, no pip dependencies required
- **Template-based output generation** - HTML templates with `{{DATA}}` and `{{THEME_CSS}}` placeholders for customization
- **Modular client patterns** - Reusable API client classes (KlaviyoAnalyticsClient, KlaviyoDevClient, etc.) for external integrations
- **Hierarchical documentation** - Each skill has SKILL.md (wizard flow), REFERENCE.md (technical details), EXAMPLES.md (prompts)

## Layers

**Skill Presentation Layer:**
- Purpose: Define how Claude interacts with the skill (YAML frontmatter in SKILL.md)
- Location: `skills/*/SKILL.md`, `skill-packs/*/*/SKILL.md`
- Contains: Skill metadata (name, description, triggers), wizard flow steps, interactive UI guidance
- Depends on: Nothing (static documentation)
- Used by: Claude Code when skill is invoked

**Data Processing Pipeline Layer:**
- Purpose: Extract, transform, and analyze input data through sequential stages
- Location: `skills/linkedin-data-viz/scripts/`, `skill-packs/*/*/scripts/`
- Contains: Stage-specific Python scripts (parse → analyze → generate/output)
  - Parse stage: Input validation, format normalization, CSV/API quirk handling
  - Analyze stage: Business logic, algorithmic processing, scoring/ranking
  - Generate stage: Template injection, output file creation, theme application
- Depends on: External APIs (Klaviyo, Shopify, GA4) via client classes
- Used by: Claude Code via subprocess calls during wizard execution

**Client/Integration Layer:**
- Purpose: Abstract external API interactions and provide consistent interface
- Location: `skill-packs/*/*/scripts/*_client.py`
- Contains: API authentication, rate limiting, error handling, data marshaling
  - `klaviyo_client.py` - Klaviyo REST API + MCP server integration
  - `shopify_client.py` - Shopify Admin API access
  - `ga_client.py` - Google Analytics Data API v1
  - `data_pipeline.py` - Google Sheets integration for Looker Studio
- Depends on: External APIs and their authentication mechanisms
- Used by: Analyze stage scripts for data retrieval

**Template/Theme Layer:**
- Purpose: Separate presentation logic from data (templates inject {{DATA}})
- Location: `skills/linkedin-data-viz/templates/`, `skills/linkedin-data-viz/assets/`
- Contains: HTML templates (10 visualizations + dashboard), CSS themes (carrier-dark.css)
- Depends on: Chart libraries (D3.js, Chart.js) injected into templates
- Used by: Generate stage to produce final HTML outputs

**Documentation Layer:**
- Purpose: Guide Claude through skill interaction and customization
- Location: All SKILL.md, REFERENCE.md, EXAMPLES.md files
- Contains: Wizard flow procedures, algorithm explanations, troubleshooting, theme customization guides
- Depends on: Nothing (reference only)
- Used by: Claude during skill execution and user support

## Data Flow

**LinkedIn Data Viz Skill Flow:**

1. **User initiates skill** - Claude reads `skills/linkedin-data-viz/SKILL.md`
2. **Preflight check** - Python version, output directory setup
3. **Export location** - User provides path to LinkedIn CSV export folder
4. **Parse stage** - `parse_export.py` reads all CSVs, handles LinkedIn quirks (3-line header skip, date format normalization, null conversation IDs), outputs `parsed.json`
5. **Analysis preview** - Claude summarizes parsed data; user selects visualizations
6. **Theme selection** - User picks Carrier Dark (default) or custom CSS
7. **Analyze stage** - `analyze.py` runs algorithms on `parsed.json`, outputs `analysis.json`
8. **Generate stage** - `generate_viz.py` injects `analysis.json` into 10 HTML templates + dashboard, applies theme CSS
9. **Output** - 11 HTML files written to output directory
10. **Post-generation** - Optional: narrative insights, sanitization, custom theming

**Klaviyo Analyst Skill Flow:**

1. **User initiates skill** - Claude reads `skill-packs/dtc-skill-pack/klaviyo-analyst/SKILL.md`
2. **User selects analysis type** - Full audit, flow audit, segment health, campaign comparison, deliverability, or revenue attribution
3. **Data retrieval** - `analyze.py` instantiates `KlaviyoAnalyticsClient`, fetches live data from Klaviyo API or MCP server
4. **Analysis execution** - Runs selected analysis algorithm (flow gap matching, segment health scoring, benchmarking, etc.)
5. **Output generation** - Returns structured JSON analysis results to Claude
6. **Presentation** - Claude formats results with three-tier recommendations, markdown tables, implementation specs
7. **Follow-up** - User can request Pro Deck Builder to turn analysis into presentation

**Cross-Skill Integration Flow (Looker Studio example):**

1. User asks Claude to "Build a CRM dashboard"
2. Claude uses Looker Studio skill's `data_pipeline.py` to push Klaviyo + Shopify data to Google Sheets
3. Looker Studio templates reference the Google Sheets data source
4. User views/edits dashboard in Looker Studio

**State Management:**

- **Transient** (within single skill execution):
  - `parsed.json` - Intermediate between parse and analyze stages
  - `analysis.json` - Intermediate between analyze and generate stages
  - Command-line arguments, user preferences
- **Persistent** (across skill invocations):
  - `.env` files - API keys and authentication credentials
  - Output HTML files - User's generated visualizations
  - User's source data (LinkedIn export CSVs, Shopify database, etc.)

## Key Abstractions

**SKILL.md Wizard Flow:**

- Purpose: Declarative specification of interactive user experience
- Examples: `skills/linkedin-data-viz/SKILL.md` (7-step preflight→export→locate→preview→theme→generate→next), `skill-packs/dtc-skill-pack/klaviyo-analyst/SKILL.md` (analysis selection framework)
- Pattern: Each step is a Claude action that performs validation, gathers input, or executes scripts. Steps are sequential; errors halt flow and provide remediation guidance.

**Quirk Handler Pattern:**

- Purpose: Normalize external data formats and handle known edge cases
- Examples:
  - `parse_export.py` skips 3 junk header lines in Connections.csv (LinkedIn quirk)
  - Handles two date formats: "DD Mon YYYY" and "YYYY-MM-DD HH:MM:SS UTC"
  - Null conversation IDs preserved for orphan message detection
  - Ad_Targeting.csv semicolon-delimited values within cells split to arrays
  - Inferences.csv column name variations (Category vs Type, Inference vs Type Description)
- Pattern: Centralized format detection and fallback parsing in parse stage

**Analysis Algorithm Pattern:**

- Purpose: Business logic for ranking, scoring, and gap detection
- Examples:
  - `linkedin-data-viz/scripts/analyze.py` - Network quality scoring, connection categorization (Active/Dormant/NeverMessaged), posting correlation via Pearson coefficient
  - `klaviyo-analyst/scripts/analyze.py` - Flow gap matching (fuzzy name matching against essential flows checklist), benchmarking against thresholds (open_rate.good=0.20, click_rate.great=0.04, etc.), three-tier recommendations (CRITICAL/HIGH/MEDIUM/LOW priority)
- Pattern: Self-contained functions with configurable thresholds and weighting; algorithms handle missing data gracefully

**API Client Pattern:**

- Purpose: Abstract platform-specific authentication and API quirks
- Examples:
  - `klaviyo_client.py` - Handles MCP server vs direct API fallback, pagination, rate limiting
  - `shopify_client.py` - Manages OAuth token refresh, API version handling
  - `ga_client.py` - Constructs GA4 Data API queries with dimension/metric validation
- Pattern: Class-based with lazy initialization, error context in exceptions for debugging

**Template Injection Pattern:**

- Purpose: Separate presentation from data; enable theme customization
- Examples: `skills/linkedin-data-viz/templates/01-network-universe.html` contains `{{DATA}}` placeholder for D3.js data, `{{THEME_CSS}}` for carrier-dark.css
- Pattern: Simple string replacement in `generate_viz.py`; templates are self-contained HTML with inline JavaScript

## Entry Points

**linkedin-data-viz Skill:**
- Location: `skills/linkedin-data-viz/SKILL.md`
- Triggers: "Analyze my LinkedIn data export", "LinkedIn visualization", "LinkedIn network analysis"
- Responsibilities: Define 7-step wizard flow, validate CSV requirements, orchestrate parse→analyze→generate pipeline
- CLI Commands:
  - `python3 scripts/parse_export.py <csv_folder> -o parsed.json`
  - `python3 scripts/analyze.py parsed.json -o analysis.json`
  - `python3 scripts/generate_viz.py --templates templates/ --data analysis.json --output ~/linkedin-viz-output --theme assets/carrier-dark.css`
  - `python3 scripts/sanitize.py analysis.json -o sanitized.json`

**Klaviyo Analyst Skill:**
- Location: `skill-packs/dtc-skill-pack/klaviyo-analyst/SKILL.md`
- Triggers: "Audit my Klaviyo account", "Analyze my Klaviyo flows", "Three-tier recommendations for Klaviyo"
- Responsibilities: Present analysis type menu, fetch live Klaviyo data, run selected analysis, format results with benchmarks and recommendations
- CLI Commands:
  - `python3 scripts/analyze.py --analysis-type full-audit`
  - `python3 scripts/analyze.py --analysis-type flow-audit`
  - `python3 scripts/analyze.py --analysis-type segment-health`

**Setup Wizard (Skill Pack):**
- Location: `skill-packs/dtc-skill-pack/scripts/setup.py`
- Triggers: User runs `python scripts/setup.py` after cloning skill pack
- Responsibilities: Check Python version, verify API key setup, install dependencies, test connections, provide .env template
- Outputs: Configured `.env` files, pip dependencies installed

**Looker Studio Skill:**
- Location: `skill-packs/dtc-skill-pack/looker-studio/SKILL.md`
- Responsibilities: Push Klaviyo + Shopify + GA4 data to Google Sheets via `data_pipeline.py`, generate Looker Studio dashboard templates
- CLI Commands:
  - `python3 scripts/data_pipeline.py --source klaviyo --sheet-id <id> --auth-token <token>`

**Pro Deck Builder Skill:**
- Location: `skill-packs/dtc-skill-pack/pro-deck-builder/SKILL.md`
- Triggers: "Create a deck", "Build a presentation", "Generate PowerPoint"
- Responsibilities: Ask user for design preferences (dark/light, palette, fonts), generate PPTX via PptxGenJS
- Requires: Node.js, PptxGenJS npm package

## Error Handling

**Strategy:** Fail fast with user-actionable guidance; preserve state for debugging.

**Patterns:**

- **Parser-level validation** - CSV files checked for required columns before parsing; malformed rows logged but skipped (not fatal)
  - Example: `parse_export.py` logs "Skipping malformed connection row: ..." on column KeyError, continues with valid rows
- **Date parsing resilience** - Unrecognized date formats logged with context (raw value shown) but don't halt processing
  - Example: `parse_date()` returns None for unparseable dates; downstream code handles null gracefully
- **Fallback field names** - When LinkedIn changes CSV column names, try multiple variants before giving up
  - Example: `parse_messages.py` tries `FROM`, `SENDER PROFILE URL`, or `Sender` in order
- **API error context** - KlaviyoAnalyticsClient wraps API errors with operation context (e.g., "Failed to fetch flows: 401 Unauthorized")
- **Output directory validation** - `_safe_output_path()` prevents path traversal attacks; raises ValueError with clear message
- **Graceful degradation** - Optional files (e.g., Shares.csv) are skipped if missing; visualizations that depend on them are omitted

## Cross-Cutting Concerns

**Logging:**
- Approach: Python logging module (stdlib) at DEBUG/INFO/WARNING/ERROR levels
- Configure with `-v` flag for verbose output during troubleshooting
- Logs are written to stderr, JSON/structured data to stdout or files

**Validation:**
- Input validation in CLI parsers (argparse)
- CSV column existence checks before reading
- Path existence checks (Path.exists())
- API response schema validation in client classes
- Output path safety checks via `_safe_output_path()`

**Authentication:**
- Environment variables (.env files, gitignored) for API keys
- KlaviyoAnalyticsClient reads `KLAVIYO_API_KEY` or falls back to MCP server
- Google Analytics uses service account JSON (path specified in .env)
- Shopify uses OAuth token from .env
- No hardcoded credentials anywhere

---

*Architecture analysis: 2026-02-19*
