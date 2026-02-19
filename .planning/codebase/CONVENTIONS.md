# Coding Conventions

**Analysis Date:** 2026-02-19

## Language & Environment

**Primary Language:** Python 3.9+
- All scripts use `#!/usr/bin/env python3` shebang
- Use of `from __future__ import annotations` for forward compatibility
- No external dependencies for core functionality (stdlib-only core)

## Naming Patterns

**Files:**
- Snake case: `parse_export.py`, `sanitize.py`, `analyze.py`
- Descriptive names reflecting purpose: `generate_viz.py`, `klaviyo_client.py`

**Functions:**
- Snake case: `parse_date()`, `parse_connections()`, `inject_data()`, `cluster_network()`
- Private functions prefixed with underscore: `_safe_strip()`, `_normalise_ad_key()`, `_classify_company()`
- Verb-first naming: `parse_*`, `generate_*`, `analyze_*`, `sanitize_*`, `load_*`

**Variables & Constants:**
- Uppercase constants: `FOUNDER_KEYWORDS`, `ESSENTIAL_FLOWS`, `BENCHMARKS`, `API_REVISION`
- Snake case locals: `flow_names_lower`, `matched`, `found_count`, `engagement_tiers`
- Type hints used throughout: `Dict[str, List[str]]`, `list[dict[str, Any]]`, `Optional[str]`

**Classes:**
- PascalCase: `KlaviyoAnalyticsClient`, `KlaviyoAnalyzer`
- Descriptive: `Colors` (for ANSI codes), custom `JSONEncoder` subclasses

**Type Hints:**
- Comprehensive usage: function signatures include parameter and return types
- Union types: `str | None`, `list[dict[str, Any]]`, `Dict[str, Any]`
- Generic types from collections: `List[Dict]`, `Optional[str]`

## Code Style

**Formatting:**
- No apparent formatter enforcement (no .prettierrc, .editorconfig detected)
- Consistent 4-space indentation
- Line lengths appear to exceed 80 characters without strict enforcement
- Docstrings use triple quotes with detailed descriptions

**Linting:**
- No detected .eslintrc or pylint configuration
- Code appears to follow PEP 8 conventions implicitly

## Import Organization

**Order:**
1. Shebang and module docstring (if present)
2. `from __future__ import annotations`
3. Standard library imports (json, logging, re, sys, argparse, csv, pathlib, datetime, etc.)
4. Third-party imports (try/except wrapped for optional deps like `faker`, `klaviyo_api`, `dotenv`)
5. Local imports (same-directory modules like `from klaviyo_client import KlaviyoAnalyticsClient`)

**Pattern Examples:**
```python
#!/usr/bin/env python3
"""Module docstring."""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

try:
    from faker import Faker
    _HAS_FAKER = True
except ImportError:
    _HAS_FAKER = False
```

**Path Handling:**
- Use `pathlib.Path` exclusively: `Path(template_path)`, `path.read_text()`, `path.exists()`
- Avoid os.path in new code

## Error Handling

**Pattern - Try/Except at Module Level:**
```python
try:
    from faker import Faker
    _faker = Faker()
    _HAS_FAKER = True
except ImportError:
    _HAS_FAKER = False
    logger.debug("Faker not installed, using built-in name lists.")
```

**Pattern - Function-Level Validation:**
```python
def _safe_output_path(path: str) -> str:
    """Validate output path does not escape working directory."""
    resolved = os.path.realpath(path)
    cwd = os.path.realpath(os.getcwd())
    if not resolved.startswith(cwd + os.sep) and resolved != cwd:
        raise ValueError(f"Output path must be within working directory: {cwd}")
    return resolved
```

**Pattern - Broad Exception Handling with Logging:**
```python
try:
    return datetime.strptime(cleaned, fmt)
except ValueError:
    continue
except Exception as exc:
    logger.warning("Date parse failed for %r: %s", raw, exc)
return None
```

**Pattern - CSV/File Parsing Robustness:**
- Wrap file operations in try/except
- Log errors with context but continue processing
- Return empty collections rather than raising for missing data

Example from `parse_export.py`:
```python
try:
    # CSV reading logic
except Exception as exc:
    logger.error("Failed to parse connections: %s", exc)
    return []
```

## Logging

**Framework:** Python's `logging` module

**Pattern:**
```python
logger = logging.getLogger(__name__)
logger.warning("Date parse failed for %r: %s", raw, exc)
logger.debug("Faker available, using it for name generation.")
logger.error("Failed to parse connections: %s", exc)
```

**When to Log:**
- Warnings: Data quality issues, format problems, API connection issues
- Errors: Parse failures, missing files, invalid credentials
- Debug: Optional dependency detection, feature availability

## Comments & Docstrings

**Module Docstrings:**
Use triple-quoted strings with clear purpose. Include usage examples if applicable:
```python
"""
parse_export.py - LinkedIn CSV export ingestion with quirk handling.

Parses LinkedIn data export CSVs into structured Python dicts. Handles
known quirks: junk header lines in Connections.csv, semicolons inside
Ad_Targeting cells, null conversation IDs in messages, and mixed date
formats across files.

Uses only Python 3.9+ stdlib (csv, json, datetime, pathlib, re).
"""
```

**Function Docstrings:**
Format with description, Args, Returns, Raises sections:
```python
def parse_date(raw: str | None) -> datetime | None:
    """Detect and parse LinkedIn's two common date formats.

    Handles:
        - ``DD Mon YYYY`` (e.g. "12 Jan 2024")
        - ``YYYY-MM-DD HH:MM:SS UTC`` or just ``YYYY-MM-DD``

    Returns None on failure and logs a warning.
    """
```

**When to Comment:**
- Explain WHY, not WHAT
- Section dividers: `# -----------` (79 chars)
- Complex algorithms: Keyword matching, role clustering logic
- Data format quirks: "LinkedIn exports prepend 3 junk header lines"

**Section Headers:**
Use consistent format:
```python
# ---------------------------------------------------------------------------
# Role-clustering keyword sets
# ---------------------------------------------------------------------------
```

## Function Design

**Size:** Functions typically 20-100 lines
- Short utility functions: 5-10 lines
- Data processing functions: 30-80 lines
- Analysis methods: 50-150 lines (allowed for complex business logic)

**Parameters:**
- Limit to 3-5 positional parameters
- Use Optional[] for optional params
- Use Dict/List type hints for complex structures
- Validation at function start

**Return Values:**
- Single value: return directly
- Multiple related values: return Dict or namedtuple
- Errors: Return None or empty collection, log exception
- No raising from data processing (except validation)

**Example Pattern:**
```python
def cluster_network(
    connections: list[dict[str, Any]],
    messages: list[dict[str, Any]],
    invitations: list[dict[str, Any]],
) -> dict[str, Any]:
    """Cluster LinkedIn network by role."""
    # Validation
    if not connections or not isinstance(connections, list):
        return {}

    # Processing
    # ... logic ...

    # Return structured result
    return {
        "clusters": cluster_data,
        "metadata": {"total": len(connections)},
    }
```

## Module Design

**Exports:**
- No `__all__` declarations (all public functions importable)
- Private functions prefixed with `_`
- Classes and key functions documented at module level

**Barrel Files:**
Not used in this codebase

**Script vs Library Patterns:**
```python
# Library pattern (reusable functions)
def parse_connections(path: Path) -> list[dict]:
    """Parse and return data."""
    pass

# Script pattern (when invoked directly)
def main() -> None:
    """Entry point with argparse."""
    parser = argparse.ArgumentParser()
    # ... setup ...
    args = parser.parse_args()
    # ... execution ...

if __name__ == "__main__":
    main()
```

## Data Structures

**Dictionaries for Data:**
- Prefer `Dict[str, Any]` for heterogeneous data
- Use lowercase keys: `{"flow_name": "", "status": ""}`
- Flat structures preferred over deeply nested

**Lists:**
- `list[dict[str, Any]]` for collections of records
- Preserve insertion order (Python 3.7+)

**Type Aliases Not Used:**
Raw types preferred: `Dict[str, List[str]]`, `Optional[Dict]`

## Configuration

**Environment Variables:**
- Loaded via `load_dotenv()` from dotenv package
- Validated immediately on import
- Examples: `KLAVIYO_API_KEY`, `SHOPIFY_ACCESS_TOKEN`, `GOOGLE_APPLICATION_CREDENTIALS`

**Setup Pattern:**
- Interactive setup wizard in `setup.py`
- Validation functions for each env var
- Skip install flag: `--skip-install`
- Non-interactive mode: `--non-interactive`

---

*Convention analysis: 2026-02-19*
