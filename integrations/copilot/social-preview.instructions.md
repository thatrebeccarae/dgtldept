Generate Open Graph social preview images (1280x640) for GitHub repositories. Creates branded OG images that display when repos are shared on Twitter, LinkedIn, and Slack. Supports custom templates, dark/light themes, and automated generation.


# Social Preview

Generate Open Graph social preview images (1280x640px) for GitHub repositories. The social preview is the single highest-leverage visual asset when repos are shared on Twitter, LinkedIn, Slack, and Discord.

## When to Use

- New public repo needs a social preview before sharing
- Rebranding a project (new colors, name change, logo update)
- Major release or launch -- refresh the preview to reflect the milestone
- Before marketing pushes (LinkedIn posts, Twitter threads, blog features)
- Audit existing repos to catch missing or outdated social previews

## Usage

```
/social-preview generate [repo-path]   # Create OG image from repo context
/social-preview audit [repo-path]      # Check if social preview is set, dimensions correct
```

Default `repo-path` is the current working directory if omitted.


## Procedure: Generate

Execute each step in order. Do not skip steps.

### Step 0: Parse Command

Expect: `/social-preview {mode} [repo-path]`

Extract mode (`generate` or `audit`). If missing or invalid:
```
Error: Invalid or missing mode.
Usage:
  /social-preview generate [repo-path]
  /social-preview audit [repo-path]
```
STOP.

Validate `repo-path` is a directory containing `.git`. Default to cwd if omitted.

### Step 1: Scan Repo for Context

Gather:
- **Project name** -- from `package.json` name, `Cargo.toml` [package] name, `pyproject.toml` name, or directory name
- **Description/tagline** -- from package.json description, repo description, or ask user
- **Primary language** -- from file extensions, package manager files, or `gh repo view --json primaryLanguage`
- **Logo/icon** -- check for `logo.png`, `logo.svg`, `icon.png`, `icon.svg`, `.github/logo.png`, `assets/logo.*`, `branding/logo.*`
- **Git remote** -- `git remote get-url origin` to extract owner/repo
- **Existing social preview** -- `gh api repos/{owner}/{repo}` to check current state

### Step 2: Select Template

Present template options to the user:

1. **Dark** (recommended) -- Dark background (#0d1117 or #141414), light text. Highest contrast, best performance on most feeds.
2. **Light** -- Light background (#fafbfc), dark text. Matches certain brand aesthetics.
3. **Minimal** -- Just project name + tagline, no decoration. Clean and typographic.

Ask: "Which template? [dark/light/minimal] (default: dark)"

If the repo has established brand colors (detected from CSS variables, tailwind config, or user-specified), offer to use those as accent colors.

### Step 3: Generate HTML Template

Create a standalone HTML file (1280x640px viewport) containing:

- **Project name** -- large, prominent, max 40 characters displayed. Use system-safe fonts only (no external font dependencies).
- **One-line description/tagline** -- below the name, lighter weight, max 80 characters.
- **Primary language/tech icon** (optional) -- simple text-based indicator or Unicode symbol. No external image dependencies.
- **Author/org attribution** (optional) -- small, bottom corner. GitHub username or org name.
- **Background** -- solid color, CSS gradient, or subtle CSS pattern (dots, grid). No external images.

Write the HTML file to `{repo-path}/social-preview.html` (or `/tmp/social-preview-{repo-name}.html` if user prefers).


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
