# social-preview


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

### Step 4: Render to PNG

Guide the user through one of three rendering paths:

**Option A -- Browser screenshot (simplest, no deps):**
1. Open the HTML file in any browser
2. Set viewport to exactly 1280x640
3. Take a full-page screenshot
4. Save as PNG

**Option B -- Puppeteer/Playwright (automated, requires Node):**
```bash
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 640, deviceScaleFactor: 2 });
  await page.goto('file:///PATH/TO/social-preview.html', { waitUntil: 'networkidle0' });
  await page.screenshot({ path: 'social-preview.png', clip: { x: 0, y: 0, width: 1280, height: 640 } });
  await browser.close();
})();
"
```

**Option C -- Cloud renderer:**
- Use `npx @vercel/og` or a hosted OG image service if the user prefers URL-based generation.

### Step 5: Set as Social Preview

Guide the user through one of two methods:

**Method A -- GitHub UI:**
1. Go to `https://github.com/{owner}/{repo}/settings`
2. Scroll to "Social preview"
3. Click "Edit" -> "Upload an image..."
4. Upload the generated PNG
5. Click "Save"

**Method B -- GitHub API:**
```bash
gh api repos/{owner}/{repo} \
  --method PATCH \
  --field "social_preview=$(base64 -i social-preview.png)"
```

Note: The GitHub REST API does not directly support uploading social preview images via base64. The UI method is the most reliable. For automation, use the repository settings page.

### Step 6: Verify

Provide validation URLs:
- Twitter Card Validator: `https://cards-dev.twitter.com/validator`
- Facebook Sharing Debugger: `https://developers.facebook.com/tools/debug/`
- LinkedIn Post Inspector: `https://www.linkedin.com/post-inspector/inspect/`
- Open Graph Debugger: `https://opengraph.dev/`

Tell user to paste the repo URL and verify the preview renders correctly.


## Procedure: Audit

### Step 1: Check Repo

Validate repo-path is a git repo with a remote.

### Step 2: Fetch Current Social Preview State

```bash
gh api repos/{owner}/{repo} --jq '.description, .homepage'
```

Check if a custom social preview image is set (GitHub auto-generates one if not).

### Step 3: Report

```
=== Social Preview Audit: {repo-name} ===

Custom preview set: {YES / NO (using auto-generated)}
Description:       {repo description or "MISSING -- add one"}
Homepage URL:       {homepage or "not set"}

Recommendations:
  - {actionable items: missing preview, missing description, etc.}

Run /social-preview generate to create one.
```


## Design Principles

- **Readable at thumbnail size.** Social feeds show previews at ~400px wide. Text must be legible at that scale.
- **High contrast.** Dark backgrounds with light text outperform on most platforms. Minimum 4.5:1 contrast ratio.
- **No small text.** If it won't be readable at 400px wide, remove it. Project name should be 48-72px at 1280px canvas.
- **2:1 aspect ratio.** 1280x640 is the standard. Platforms crop outside this ratio.
- **No external dependencies.** HTML must render with zero network requests. System fonts only. Inline all CSS.
- **Keep text minimal.** Project name + one-line tagline. Nothing else is guaranteed to be readable.
- **Test at actual share size.** Always preview at 400x200 before finalizing.

## Key Principles

1. Dark backgrounds perform better across Twitter, LinkedIn, and Slack feeds.
2. Keep text to two lines maximum: name + tagline.
3. Test at actual share size (400px wide), not at full resolution.
4. PNG format, under 1MB. Avoid JPEG for text-heavy images (compression artifacts).
5. Update the preview when the project description or branding changes.
6. A missing social preview is worse than a simple one -- GitHub's auto-generated preview is generic and forgettable.

## Files

- **HTML template:** `{repo-path}/social-preview.html` or `/tmp/social-preview-{repo-name}.html`
- **PNG output:** `{repo-path}/social-preview.png`

## Anti-Patterns

- No external font CDN links -- system fonts only for guaranteed rendering
- No images or logos that require network requests -- inline SVG or omit
- No text below 24px at 1280px canvas (will be illegible at thumbnail size)
- No busy backgrounds or photographic backgrounds -- solid or gradient only
- No more than 3 colors total (background, primary text, accent)
- No rounded corners or complex shapes that get lost at small sizes
- Do not include full URLs in the image -- waste of space, unreadable at thumbnail

---

---
name: social-preview
description: "Reference documentation for OG image specifications, HTML templates, platform rendering behavior, and GitHub API integration."
---

# Social Preview -- Reference

## OG Image Specifications

| Property | Value |
|----------|-------|
| Recommended size | 1280 x 640px (2:1 ratio) |
| Minimum size | 640 x 320px |
| Maximum file size | 5MB |
| Supported formats | PNG, JPEG |
| Color space | sRGB |
| Bit depth | 8-bit (24-bit color) |

GitHub auto-generates a social preview if none is set: repo name + description + owner avatar on a dark background. It is functional but generic -- a custom preview stands out significantly more in feeds.

---

## HTML Template: Dark Theme

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280">
<title>Social Preview</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    width: 1280px;
    height: 640px;
    overflow: hidden;
    background: #0d1117;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    color: #f0f6fc;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 80px 96px;
  }

  .project-name {
    font-size: 64px;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 20px;
  }

  .tagline {
    font-size: 28px;
    font-weight: 400;
    color: #8b949e;
    line-height: 1.4;
    max-width: 900px;
  }

  .language-badge {
    display: inline-block;
    margin-top: 40px;
    padding: 8px 20px;
    border: 1px solid #30363d;
    border-radius: 24px;
    font-size: 16px;
    color: #8b949e;
    letter-spacing: 0.05em;
  }

  .attribution {
    position: absolute;
    bottom: 40px;
    right: 96px;
    font-size: 16px;
    color: #484f58;
  }

  .accent-bar {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #58a6ff, #3fb950);
  }
</style>
</head>
<body>
  <div class="accent-bar"></div>
  <div class="project-name">Project Name</div>
  <div class="tagline">A one-line description of what this project does and why it matters.</div>
  <div class="language-badge">TypeScript</div>
  <div class="attribution">github.com/owner</div>
</body>
</html>
```

---

## HTML Template: Light Theme

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280">
<title>Social Preview</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    width: 1280px;
    height: 640px;
    overflow: hidden;
    background: #fafbfc;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    color: #24292f;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 80px 96px;
  }

  .project-name {
    font-size: 64px;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 20px;
  }

  .tagline {
    font-size: 28px;
    font-weight: 400;
    color: #57606a;
    line-height: 1.4;
    max-width: 900px;
  }

  .language-badge {
    display: inline-block;
    margin-top: 40px;
    padding: 8px 20px;
    border: 1px solid #d0d7de;
    border-radius: 24px;
    font-size: 16px;
    color: #57606a;
    letter-spacing: 0.05em;
  }

  .attribution {
    position: absolute;
    bottom: 40px;
    right: 96px;
    font-size: 16px;
    color: #8b949e;
  }

  .accent-bar {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #0969da, #1a7f37);
  }
</style>
</head>
<body>
  <div class="accent-bar"></div>
  <div class="project-name">Project Name</div>
  <div class="tagline">A one-line description of what this project does and why it matters.</div>
  <div class="language-badge">Python</div>
  <div class="attribution">github.com/owner</div>
</body>
</html>
```

---

## CSS: Safe Fonts for Social Preview Images

Social preview HTML must render without network requests. Use only system font stacks:

```css
/* Primary -- GitHub system font stack */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;

/* Monospace -- for code-related projects */
font-family: 'SF Mono', 'Cascadia Code', 'Consolas', 'Liberation Mono', Menlo, monospace;
```

Never use Google Fonts, Fontshare, or any CDN-hosted font in social preview HTML. The rendering environment (Puppeteer headless, browser screenshot) may not have network access.

---

## GitHub API: Social Preview

GitHub does not expose a direct REST API endpoint for uploading social preview images. The recommended workflow:

```bash
# Check if repo has a custom social preview
gh api repos/{owner}/{repo} --jq '.description, .homepage'

# The social preview must be uploaded through the GitHub UI:
# Settings -> General -> Social preview -> Edit -> Upload
```

For programmatic workflows, consider maintaining the HTML template in the repo and rendering + uploading via a GitHub Action.

---

## Platform-Specific Rendering

| Platform | Display Size | Crop Behavior | Notes |
|----------|-------------|---------------|-------|
| Twitter | 1200 x 628 | Slight crop top/bottom | Cards validator caches aggressively; wait 5-10min after upload |
| LinkedIn | 1200 x 627 | Similar to Twitter | Post Inspector clears cache on demand |
| Slack | ~400 x 209 | Scaled down significantly | Text must be large -- test at 400px wide |
| Discord | ~400 x 200 | Scaled + rounded corners | Small radius crop on corners; keep content away from edges |
| Facebook | 1200 x 630 | Minor crop | Sharing Debugger fetches fresh on demand |
| iMessage | ~300 x 157 | Heavily scaled | Only project name will be readable |

**Safe zone:** Keep all text within the center 1100 x 560px area (90px margin from each edge) to survive cropping across all platforms.

---

## Testing / Validation URLs

| Tool | URL | Notes |
|------|-----|-------|
| Twitter Card Validator | `https://cards-dev.twitter.com/validator` | Paste repo URL, check preview |
| Facebook Sharing Debugger | `https://developers.facebook.com/tools/debug/` | Click "Scrape Again" to refresh cache |
| LinkedIn Post Inspector | `https://www.linkedin.com/post-inspector/inspect/` | Refreshes on each inspection |
| Open Graph Debugger | `https://opengraph.dev/` | Shows all OG tags + preview |
| Metatags.io | `https://metatags.io/` | Side-by-side preview across platforms |

---

## Color Accessibility Tips

- **Minimum contrast ratio:** 4.5:1 for body text, 3:1 for large text (>24px bold or >18.66px regular). Use WebAIM Contrast Checker.
- **Dark theme safe pairs:**
  - `#f0f6fc` on `#0d1117` = 15.4:1 (excellent)
  - `#8b949e` on `#0d1117` = 5.1:1 (passes AA)
  - `#58a6ff` on `#0d1117` = 6.2:1 (passes AA)
- **Light theme safe pairs:**
  - `#24292f` on `#fafbfc` = 14.8:1 (excellent)
  - `#57606a` on `#fafbfc` = 5.7:1 (passes AA)
- **Avoid:** Red text on dark backgrounds (poor contrast). Yellow text on light backgrounds (illegible).
- **Color blindness:** Do not rely on color alone to convey information. The language badge uses border + text, not just color.

---

## Puppeteer Rendering Reference

```bash
# Render at 2x for retina-quality output
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 640, deviceScaleFactor: 2 });
  await page.goto('file:///absolute/path/to/social-preview.html', { waitUntil: 'networkidle0' });
  await page.screenshot({
    path: 'social-preview.png',
    clip: { x: 0, y: 0, width: 1280, height: 640 }
  });
  await browser.close();
  console.log('Rendered: social-preview.png (2560x1280 @2x)');
})();
"
```

Output will be 2560x1280px at 2x deviceScaleFactor. GitHub scales down gracefully. The extra resolution ensures sharpness on retina displays.
