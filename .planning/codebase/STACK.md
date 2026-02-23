# Technology Stack

**Analysis Date:** 2026-02-19

## Languages

**Primary:**
- Python 3.9+ - Backend analysis, data processing, API clients, and CLI tools
- HTML5 - Interactive visualization templates for LinkedIn Data Viz skill
- JavaScript (vanilla) - Client-side D3.js and Chart.js visualizations, no frameworks
- YAML - Skill definitions and configuration files

**Secondary:**
- Bash - Setup scripts and automation

## Runtime

**Environment:**
- Python 3.9+ (minimum, based on `from __future__ import annotations` syntax in scripts)

**Package Manager:**
- pip - Python package management
- No Node.js/npm required (pro-deck-builder uses PptxGenJS but is abstracted as Claude Code skill)

**Environment Configuration:**
- `.env` files for credentials (python-dotenv library)
- No lockfile detected (pip requirements.txt per skill pack)

## Frameworks

**Backend/Data:**
- klaviyo-api>=9.0.0,<23.0.0 - Klaviyo Private API client
- google-analytics-data>=0.17.0,<1.0.0 - GA4 Data API client
- ShopifyAPI>=12.0.0,<13.0.0 - Shopify Admin API client
- google-api-python-client>=2.0.0,<3.0.0 - Google Sheets & Drive API
- google-auth>=2.0.0,<3.0.0 - Google service account authentication
- gspread>=5.0.0,<7.0.0 - Google Sheets manipulation

**Frontend Visualization:**
- D3.js v7 (cdn: https://d3js.org/d3.v7.min.js) - Network graphs, interactive visualizations
- Chart.js (cdn: https://cdn.jsdelivr.net/npm/chart.js) - Bar charts, line charts, metrics

**Testing:**
- No test framework detected (no pytest/unittest configs)

**Utilities:**
- python-dotenv>=1.0.0,<2.0.0 - Environment variable loading
- requests>=2.28.0,<3.0.0 - HTTP client (Shopify skill)

## Key Dependencies

**Critical:**
- klaviyo-api - Used by both `klaviyo-analyst` (`skill-packs/dtc-skill-pack/klaviyo-analyst/`) and `klaviyo-developer` (`skill-packs/dtc-skill-pack/klaviyo-developer/`) skills for direct API access
- google-auth + google-api-python-client - Required for GA4 (`skill-packs/dtc-skill-pack/google-analytics/`) and Looker Studio data pipeline (`skill-packs/dtc-skill-pack/looker-studio/`)
- D3.js - Powers interactive network graphs in LinkedIn Data Viz (`skills/linkedin-data-viz/templates/01-network-universe.html`)

**Infrastructure:**
- gspread - Enables Google Sheets as free data warehouse for Looker Studio dashboards
- ShopifyAPI - Shopify store audit and order/product analysis

## Configuration

**Environment:**
- Secrets managed via `.env` files (one per skill pack subdirectory, e.g., `skill-packs/dtc-skill-pack/google-analytics/.env.example`)
- Never committed to git (included in `.gitignore`)
- Service account JSON files stored outside git repo

**Build:**
- No build pipeline detected. Scripts are run directly via `python scripts/[name].py`
- Interactive setup wizard: `python scripts/setup.py` at repo root (`skill-packs/dtc-skill-pack/scripts/setup.py`)

## Platform Requirements

**Development:**
- Python 3.9+
- pip
- Text editor or IDE (skills are CLI-oriented)
- API credentials:
  - Klaviyo Private API Key (pk_* format)
  - Google Cloud service account JSON (for GA4 and Looker Studio)
  - Shopify Admin API access token
  - LinkedIn data export CSV (for LinkedIn Data Viz)

**Production:**
- Python 3.9+ runtime
- No server/container requirement (all skills designed to run locally in Claude Code)
- Static HTML outputs (visualization templates are generated to standalone HTML files)

## API Clients

All skills interact with external platform APIs using official SDKs or REST clients:

- `skill-packs/dtc-skill-pack/klaviyo-analyst/scripts/klaviyo_client.py` - Wraps klaviyo-api SDK
- `skill-packs/dtc-skill-pack/klaviyo-developer/scripts/klaviyo_client.py` - Enhanced client with webhook/schema patterns
- `skill-packs/dtc-skill-pack/google-analytics/scripts/ga_client.py` - Wraps google-analytics-data SDK
- `skill-packs/dtc-skill-pack/shopify/scripts/shopify_client.py` - Wraps ShopifyAPI SDK
- `skill-packs/dtc-skill-pack/looker-studio/scripts/data_pipeline.py` - Uses gspread + google-auth for Sheets access

## Notable Patterns

**No external dependencies for core logic:**
- LinkedIn Data Viz analysis (`skills/linkedin-data-viz/scripts/analyze.py`) uses only Python stdlib (json, collections, datetime, regex, pathlib)
- Data parsing (`skills/linkedin-data-viz/scripts/parse_export.py`) uses only stdlib
- Sanitization (`skills/linkedin-data-viz/scripts/sanitize.py`) uses only stdlib

**Frontend-agnostic:**
- All visualizations render as static HTML files with inline D3.js/Chart.js
- No build step required — templates support variable substitution: `{{TITLE}}`, `{{DATA}}`, `{{THEME_CSS}}`
- Dark and light theme CSS injected at render time

**Setup automation:**
- Interactive wizard (`skill-packs/dtc-skill-pack/scripts/setup.py`) detects OS, validates credentials, installs dependencies, runs health checks
- Supports non-interactive mode and selective skill installation

---

*Stack analysis: 2026-02-19*
