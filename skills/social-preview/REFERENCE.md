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
