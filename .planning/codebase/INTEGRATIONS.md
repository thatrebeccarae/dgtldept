# External Integrations

**Analysis Date:** 2026-02-19

## APIs & External Services

**Email & SMS Marketing:**
- **Klaviyo** - Email/SMS platform for DTC brands
  - SDK/Client: `klaviyo-api>=9.0.0,<23.0.0`
  - Auth: Environment variable `KLAVIYO_API_KEY` (format: `pk_*`)
  - Used by: `skill-packs/klaviyo-skill-pack/klaviyo-analyst/` and `skill-packs/klaviyo-skill-pack/klaviyo-developer/`
  - Implementation: `skill-packs/klaviyo-skill-pack/klaviyo-analyst/scripts/klaviyo_client.py` (415 lines) and `skill-packs/klaviyo-skill-pack/klaviyo-developer/scripts/klaviyo_client.py` (642 lines)
  - MCP Server: Klaviyo MCP server (via uvx: `klaviyo-mcp-server@latest`) provides live data access to flows, segments, campaigns, metrics
  - Scopes: Read-only recommended for analyst tasks (campaigns:read, flows:read, segments:read, lists:read, metrics:read); write scopes optional for developer integrations

**E-Commerce:**
- **Shopify Admin API** - Store performance and product data
  - SDK/Client: `ShopifyAPI>=12.0.0,<13.0.0`
  - Auth: Environment variables `SHOPIFY_STORE_URL` (format: `https://[store].myshopify.com`) and `SHOPIFY_ACCESS_TOKEN` (format: `shpat_*`)
  - Used by: `skill-packs/klaviyo-skill-pack/shopify/`
  - Implementation: `skill-packs/klaviyo-skill-pack/shopify/scripts/shopify_client.py` (400 lines)
  - Required scopes: `read_orders`, `read_products`, `read_customers`, `read_inventory`, optional `read_analytics`
  - API version: Defaults to 2024-10, configurable via `SHOPIFY_API_VERSION`

**Analytics:**
- **Google Analytics 4 (GA4)** - Web traffic and conversion data
  - SDK/Client: `google-analytics-data>=0.17.0,<1.0.0`
  - Auth:
    - `GOOGLE_ANALYTICS_PROPERTY_ID` (numeric ID from GA4 Admin > Property Settings)
    - `GOOGLE_APPLICATION_CREDENTIALS` (path to Google service account JSON)
  - Used by: `skill-packs/klaviyo-skill-pack/google-analytics/`
  - Implementation: `skill-packs/klaviyo-skill-pack/google-analytics/scripts/ga_client.py` (357 lines)
  - Health check: `python scripts/ga_client.py --days 7 --metrics sessions`

**Data & Reporting:**
- **Google Sheets API** - Central data warehouse for Looker Studio
  - SDK/Client: `google-api-python-client>=2.0.0,<3.0.0` + `google-auth>=2.0.0,<3.0.0`
  - Auth: Service account via `GOOGLE_APPLICATION_CREDENTIALS` (Google Cloud service account JSON)
  - Additional: `gspread>=5.0.0,<7.0.0` for high-level Sheets manipulation
  - Used by: `skill-packs/klaviyo-skill-pack/looker-studio/`
  - Implementation: `skill-packs/klaviyo-skill-pack/looker-studio/scripts/data_pipeline.py` (585 lines)
  - Scopes: `https://www.googleapis.com/auth/spreadsheets`, `https://www.googleapis.com/auth/drive`
  - Optional: Pre-existing spreadsheet ID via `GOOGLE_SHEETS_SPREADSHEET_ID`, or pipeline creates new sheets

- **Looker Studio** - Visualization and dashboard tool (no SDK, reads from Google Sheets)
  - Connection: Via Google Sheets as free data source
  - Used by: `skill-packs/klaviyo-skill-pack/looker-studio/`
  - Templates provided for CRM dashboards, lifecycle marketing, revenue attribution (defined in data_pipeline.py)

## Data Storage

**Databases:**
- Not used. All data is transient (in-memory analysis) or exported to Google Sheets

**File Storage:**
- Local filesystem only - all skill outputs written as static HTML files or JSON exports
- LinkedIn Data Viz exports visualizations to standalone HTML with embedded CSS and D3.js

**Caching:**
- None detected

## Authentication & Identity

**Auth Provider:**
- Custom API key authentication (not OAuth for analyst/developer skills)
  - Klaviyo: Private API key stored in environment variables
  - Shopify: Bearer token auth via API access token
  - Google: Service account credentials (JSON key file)

**Pattern:**
- Environment variables loaded via `python-dotenv>=1.0.0,<2.0.0`
- All credentials validated in setup wizard: `skill-packs/klaviyo-skill-pack/scripts/setup.py`
- No token refresh/expiration handling — API keys assumed long-lived

**Setup Flow:**
Interactive wizard (`python scripts/setup.py`) guides users:
1. Select skills to configure
2. Prompt for API keys/credentials with validation
3. Verify file paths exist (e.g., Google service account JSON)
4. Test connections via health check scripts
5. Install dependencies per skill
6. Store credentials in `.env` files

## Monitoring & Observability

**Error Tracking:**
- None detected (no Sentry, Rollbar, etc.)

**Logs:**
- Approach: Python `logging` module configured in scripts
- Example: `skill-packs/klaviyo-skill-pack/klaviyo-analyst/scripts/analyze.py` initializes logger at module level
- Output: Console logs with standard format

## CI/CD & Deployment

**Hosting:**
- Not applicable — skills are run locally in Claude Code or via MCP server

**CI Pipeline:**
- None detected (no GitHub Actions, CircleCI, etc.)

**Deployment:**
- Installation: Copy skill directories to `~/.claude/skills/` or use setup wizard
- Validation: Health checks in setup.py (GA4 example: `python scripts/ga_client.py --days 7 --metrics sessions`)

## Environment Configuration

**Required env vars by skill:**

**Klaviyo Analyst & Developer:**
- `KLAVIYO_API_KEY` - Private API key (pk_*)

**Google Analytics:**
- `GOOGLE_ANALYTICS_PROPERTY_ID` - GA4 property ID (numeric)
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to Google service account JSON

**Shopify:**
- `SHOPIFY_STORE_URL` - Store URL (https://[store].myshopify.com)
- `SHOPIFY_ACCESS_TOKEN` - Admin API access token (shpat_*)
- Optional: `SHOPIFY_API_VERSION` (defaults to 2024-10)

**Looker Studio Data Pipeline:**
- `GOOGLE_SHEETS_CREDENTIALS_PATH` - Path to Google service account JSON (required)
- Optional: `GOOGLE_SHEETS_SPREADSHEET_ID` (creates new sheet if not provided)
- Optional: `KLAVIYO_API_KEY`, `SHOPIFY_STORE_URL`, `SHOPIFY_ACCESS_TOKEN`, `GOOGLE_ANALYTICS_PROPERTY_ID` (for sync actions)

**Secrets location:**
- `.env` files in each skill directory (e.g., `skill-packs/klaviyo-skill-pack/google-analytics/.env`)
- Git-ignored via `.gitignore`
- Service account JSON files stored outside git repo on user's machine

**Setup example files:**
- `.env.example` templates provided in each skill directory
- Setup wizard generates `.env` from user input

## Webhooks & Callbacks

**Incoming:**
- Klaviyo developer skill includes webhook handling patterns
  - Location: `skill-packs/klaviyo-skill-pack/klaviyo-developer/REFERENCE.md` (webhook section)
  - Pattern: POST endpoints for Klaviyo subscription events, checkout abandonment, etc.
  - Implementation example in `skill-packs/klaviyo-skill-pack/klaviyo-developer/scripts/dev_tools.py` (webhook validation patterns)

**Outgoing:**
- Looker Studio integration pushes data via Google Sheets API (not webhooks)

## Data Pipeline Flow

```
Shopify (orders, products, customers)
    |
    +--> Klaviyo (flows, segments, campaigns, metrics) --> Google Sheets --> Looker Studio
    |
    +--> GA4 (traffic, behavior, conversions) --> Google Sheets --> Looker Studio
```

**Implementation:**
- `skill-packs/klaviyo-skill-pack/looker-studio/scripts/data_pipeline.py` orchestrates sync
- Actions: `sync-klaviyo`, `sync-shopify`, `sync-ga4`, `create-sheet`
- Templates for pre-built dashboard structures (CRM Performance, Lifecycle Marketing, Revenue Attribution)

## API Rate Limiting

**Documented patterns:**
- Klaviyo developer skill includes rate limit handling
  - Reference: `skill-packs/klaviyo-skill-pack/klaviyo-developer/REFERENCE.md` (rate limit section)
  - Pattern: Exponential backoff retry logic in `skill-packs/klaviyo-skill-pack/klaviyo-developer/scripts/dev_tools.py`

**No throttling detected in:**
- Google Analytics client (relies on SDK defaults)
- Shopify client (relies on SDK defaults)
- Google Sheets writes (relies on gspread defaults)

## MCP Server Integration

**Klaviyo MCP Server:**
- Location in setup: `~/.mcp.json` configuration
- Command: `uvx klaviyo-mcp-server@latest`
- Environment: `PRIVATE_API_KEY` (set from `KLAVIYO_API_KEY`), `READ_ONLY`, `ALLOW_USER_GENERATED_CONTENT`
- Used by: `klaviyo-analyst` and `klaviyo-developer` skills for real-time account data access
- Verification: `/mcp` command in Claude Code

---

*Integration audit: 2026-02-19*
