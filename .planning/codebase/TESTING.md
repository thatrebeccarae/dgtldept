# Testing Patterns

**Analysis Date:** 2026-02-19

## Test Framework

**Status:** No automated test framework detected

**Finding:**
- No `pytest`, `unittest`, or `vitest` configuration found
- No test files (*.test.py, *_test.py, *.spec.py) in codebase
- No testing dependencies in requirements.txt files
- No CI/CD pipeline configuration detected

This is a **manual testing codebase** for Claude Code skills — an interactive tool context where users provide data and Claude Code executes scripts and displays results in real-time.

## Testing Approach Used

**Interactive Validation Pattern:**
The codebase uses a validation-first approach with graceful degradation rather than unit tests:

**1. Health Check Scripts:**
`setup.py` includes CLI-based health checks for each skill:
```python
"health_check": "scripts/ga_client.py --days 7 --metrics sessions",
```

These are run manually after setup to verify API connectivity and credentials.

**2. Input Validation at Script Entry:**
Each script validates inputs before processing:

```python
def _safe_output_path(path: str) -> str:
    """Validate output path does not escape working directory."""
    resolved = os.path.realpath(path)
    cwd = os.path.realpath(os.getcwd())
    if not resolved.startswith(cwd + os.sep) and resolved != cwd:
        raise ValueError(f"Output path must be within working directory: {cwd}")
    return resolved
```

**3. Credential Validation During Initialization:**
Client classes validate credentials in `__init__`:

From `klaviyo_client.py`:
```python
def __init__(self):
    """Initialize the client with credentials from environment."""
    load_dotenv()

    api_key = os.environ.get("KLAVIYO_API_KEY")
    if not api_key:
        raise ValueError(
            "KLAVIYO_API_KEY environment variable not set. "
            "Find your API key in Klaviyo: Settings > Account > API Keys"
        )

    if not api_key.startswith("pk_"):
        raise ValueError(
            "KLAVIYO_API_KEY should start with 'pk_'. "
            "Use a Private API Key, not a Public API Key."
        )

    try:
        self.client = KlaviyoAPI(api_key, max_delay=60, max_retries=3)
    except Exception:
        raise RuntimeError("Failed to initialize Klaviyo client. Check your API key.")
```

**4. Robust Parsing with Fallback:**
Data parsing is defensive, returning empty or partial results rather than crashing:

From `parse_export.py`:
```python
def parse_connections(path: Path) -> list[dict[str, Any]]:
    """Parse Connections.csv.

    Handles known quirks...
    """
    try:
        # ... parsing logic ...
    except Exception as exc:
        logger.error("Failed to parse connections: %s", exc)
        return []  # Return empty list, don't crash
```

**5. Date Parsing with Multiple Format Support:**
```python
def parse_date(raw: str | None) -> datetime | None:
    """Detect and parse LinkedIn's two common date formats."""
    if not raw or not raw.strip():
        return None
    raw = raw.strip()
    try:
        if _RE_DMY.match(raw):
            return datetime.strptime(raw, "%d %b %Y")
        if _RE_ISO.match(raw):
            cleaned = raw.replace(" UTC", "").strip()
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.strptime(cleaned, fmt)
                except ValueError:
                    continue
    except Exception as exc:
        logger.warning("Date parse failed for %r: %s", raw, exc)
    logger.warning("Unrecognised date format: %r", raw)
    return None
```

Returns `None` and logs warning on parse failure — won't crash processing pipeline.

## Data Validation Patterns

**Environment Variable Validation:**
From `setup.py`:
```python
SKILLS = {
    "klaviyo-analyst": {
        "env_vars": {
            "KLAVIYO_API_KEY": {
                "prompt": "Klaviyo Private API Key (starts with pk_)",
                "validation": lambda v: v.startswith("pk_") and len(v) > 10,
                "error": "Key should start with 'pk_' and be 36+ characters",
            },
        },
    },
    "google-analytics": {
        "env_vars": {
            "GOOGLE_APPLICATION_CREDENTIALS": {
                "validation": lambda v: os.path.exists(v),
                "error": "File not found at that path",
            },
        },
    },
}
```

Each env var has:
- Prompt (user-friendly)
- Validation function (lambda predicate)
- Error message (on failure)

**CSV Quirk Handling:**
From `parse_export.py`:
```python
# Pattern: "12 Jan 2024"
_RE_DMY = re.compile(r"^\d{1,2}\s+\w{3}\s+\d{4}$")
# Pattern: "2024-01-12 08:30:45 UTC" or "2024-01-12 08:30:45"
_RE_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}")

# LinkedIn exports prepend 3 junk header lines — skip them
csv_reader = csv.DictReader(fp, skip_initial_space=True)
```

Handles:
- Multiple date formats
- Junk header rows
- Semicolons inside quoted cells
- Missing/null fields

## Fuzzy Matching Patterns

**For Flow/Segment Categorization:**
From `analyze.py`:
```python
# Fuzzy match: check if essential flow name keywords appear
keywords = essential["name"].lower().split()
matched = any(
    all(kw in flow_name for kw in keywords)
    for flow_name in flow_names_lower
)

# Also check common alternate names
alt_names = {
    "welcome series": ["welcome", "onboarding"],
    "abandoned cart": ["abandon", "cart recovery", "checkout abandon"],
}

if not matched:
    alts = alt_names.get(essential["name"].lower(), [])
    matched = any(
        any(alt in flow_name for alt in alts)
        for flow_name in flow_names_lower
    )
```

This prevents false negatives due to naming variations.

## Error Recovery Patterns

**Pattern - Missing File Handling:**
```python
def _find_file(folder: Path, candidates: list[str]) -> Path | None:
    """Find first existing file from candidate list."""
    for candidate in candidates:
        path = folder / candidate
        if path.exists():
            return path
    return None

# Usage:
connections_file = _find_file(
    folder,
    ["Connections.csv", "connections.csv", "LinkedIn_Connections.csv"]
)
if not connections_file:
    logger.error("Could not find connections file")
    return {}
```

**Pattern - Optional Dependencies:**
```python
try:
    from faker import Faker
    _faker = Faker()
    _HAS_FAKER = True
    logger.debug("Faker available, using it for name generation.")
except ImportError:
    _HAS_FAKER = False
    logger.debug("Faker not installed, using built-in name lists.")

# Later, check before use:
if _HAS_FAKER:
    name = _faker.first_name()
else:
    name = random.choice(FAKE_FIRST_NAMES_F)
```

## CLI Testing

**Arguments as Test Cases:**
Each script accepts command-line arguments for different scenarios:

From `generate_viz.py`:
```python
parser.add_argument("--data", required=True, help="Path to analysis JSON file")
parser.add_argument("--output", required=True, help="Output directory")
parser.add_argument("--theme", default="carrier", help="CSS theme name")
```

Users can test different data files and themes:
```bash
python generate_viz.py --data sample.json --output /tmp/viz --theme dark
python generate_viz.py --data production.json --output ./output
```

From `analyze.py`:
```python
parser.add_argument(
    "--analysis-type",
    choices=["full-audit", "flow-audit", "segment-health"],
    required=True,
)
parser.add_argument("--days", type=int, default=30)
parser.add_argument("--output", type=str, help="Output file path")
```

## Integration Test Pattern

**Setup Wizard as Integration Test:**
`setup.py` performs integration testing during setup:

```python
if skill_config.get("health_check"):
    print(f"\n{Colors.BLUE}Running health check...{Colors.END}")
    result = subprocess.run(
        [sys.executable, skill_config["health_check"]],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"{Colors.RED}Health check failed:{Colors.END}")
        print(result.stderr)
    else:
        print(f"{Colors.GREEN}Health check passed!{Colors.END}")
```

This validates:
- Environment setup is correct
- API credentials work
- Dependencies are installed
- Network connectivity works

## Manual Testing Artifacts

**Demo Data:**
- `skills/linkedin-data-viz/demo/` contains pre-built HTML visualizations
- `demo.html` and `index.html` can be opened in browser for manual testing
- Used to verify visualization rendering before actual user data

**Sample Data:**
Built-in fallback data and name lists for testing without external dependencies:

From `sanitize.py`:
```python
FAKE_FIRST_NAMES_F: list[str] = [
    "Aria", "Nova", "Luna", "Sage", ...
]

FAKE_COMPANIES: dict[str, list[str]] = {
    "dtc": ["Lumina Beauty", "Woven Home", ...],
    "tech": ["NexaFlow", "Prism Labs", ...],
}

FAKE_MESSAGES_GENUINE: list[str] = [
    "Great to connect! Would love to chat about your work in the space.",
    ...
]
```

These allow testing data transformation logic without real user data.

## Test Coverage Gaps

Since this is a manual testing codebase, critical areas without automation:

**Not Tested Automatically:**
- Full end-to-end skill workflows (user imports LinkedIn export → visualization generated)
- API rate limiting and retry logic
- Webhook handling in developer skills
- Real Shopify/GA4/Klaviyo API responses
- Large dataset performance (memory usage, processing time)
- Concurrent skill execution
- Error messages to end users

**Risk Mitigation:**
- Code is simple and linear (minimal branching)
- Data processing is defensive (doesn't crash on bad input)
- Logging captures failures for debugging
- Users see results immediately in Claude Code interface

---

*Testing analysis: 2026-02-19*
