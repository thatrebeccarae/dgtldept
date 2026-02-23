# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities
2. Email **security@rebeccaraebarton.com** with details of the vulnerability
3. Include steps to reproduce, affected files, and potential impact

You can expect an initial response within 48 hours and a resolution timeline within 7 days.

## Security Design

These skills are built with a security-first approach. Here's how.

### Input Validation & Path Sanitization

All scripts validate and sanitize file paths before any file system operations. Directory traversal attempts (`../`) are blocked. Only expected file types and formats are processed.

### SSRF Protection

Scripts that make HTTP requests validate URLs against allowlists of known API endpoints (Klaviyo, Shopify, Google). No user-supplied URLs are fetched without validation.

### Credential Handling

- API keys are stored in `.env` files, which are **gitignored by default**
- Keys are read from environment variables at runtime — never hardcoded
- The setup wizard uses `getpass` for key input (no terminal echo)
- No credentials are logged, printed, or written to output files

### Read-Only API Access

All API access defaults to **read-only scopes**. The Klaviyo MCP server runs with `READ_ONLY=true` by default. Write scopes are only needed for developer integration tasks and must be explicitly enabled.

### No PII Beyond Aggregates

Skills work with aggregate metrics, not individual customer data. Klaviyo profile access is used for segment counts and cohort analysis — individual PII is not extracted, stored, or logged.

### No Persistent Data Storage

Skills do not create databases, caches, or persistent storage. All analysis is performed in-memory during the Claude Code session and output is written to local files you control.

## Protecting Your API Keys

### Use .env Files

Create a `.env` file in your project root (it's already in `.gitignore`):

```bash
# .env
KLAVIYO_API_KEY=pk_your_key_here
GOOGLE_ANALYTICS_PROPERTY_ID=123456789
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

### Claude Code Deny List

Add sensitive paths to your Claude Code settings to prevent accidental reads:

```json
// ~/.claude/settings.json
{
  "permissions": {
    "deny": [
      "Read(~/.env)",
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Read(**/credentials*.json)",
      "Read(**/service-account*.json)"
    ]
  }
}
```

### Key Rotation

Rotate API keys periodically. All platforms used by these skills support key rotation without downtime — generate a new key, update your `.env`, and revoke the old one.
