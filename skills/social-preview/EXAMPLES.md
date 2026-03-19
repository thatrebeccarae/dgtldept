---
name: social-preview
description: "Usage examples for the social-preview skill."
---

# Social Preview -- Examples

## Example 1: Dark-Theme Social Preview for a CLI Tool

**User:**
```
/social-preview generate ~/Popoloto/Repos.nosync/aouda
```

**What happens:**

1. Skill scans the repo: name is `aouda`, description is "Autonomous AI agent framework", primary language is TypeScript, logo found at `branding/logo.png`.
2. Asks user for template preference. User picks **dark** (default).
3. Generates `social-preview.html`:

```html
<body>
  <div class="accent-bar"></div>
  <div class="project-name">aouda</div>
  <div class="tagline">Autonomous AI agent framework</div>
  <div class="language-badge">TypeScript</div>
  <div class="attribution">github.com/thatrebeccarae</div>
</body>
```

4. Guides user to render via Puppeteer on REDACTED:
```bash
ssh REDACTED
cd ~/Popoloto/Repos.nosync/aouda
node -e "const p=require('puppeteer');(async()=>{const b=await p.launch({headless:true});const pg=await b.newPage();await pg.setViewport({width:1280,height:640,deviceScaleFactor:2});await pg.goto('file://$(pwd)/social-preview.html',{waitUntil:'networkidle0'});await pg.screenshot({path:'social-preview.png',clip:{x:0,y:0,width:1280,height:640}});await b.close();})()"
```

5. Instructs user to upload via GitHub Settings > General > Social Preview.
6. Provides Twitter Card Validator URL to verify.

---

## Example 2: Branded Social Preview Matching Project Colors

**User:**
```
/social-preview generate ~/Popoloto/Repos.nosync/ouras
```

**What happens:**

1. Skill scans the repo: name is `ouras`, description is "Time tracking with presence", primary language is TypeScript. Detects Tailwind config with custom dark palette (`#08080d` background).
2. Asks user for template. User says: "Use the project's dark palette -- #08080d background, zinc text."
3. Skill modifies the dark template to use the project's brand colors:

```css
body {
  background: #08080d;
  color: #e4e4e7; /* zinc-200 */
}
.tagline {
  color: #a1a1aa; /* zinc-400 */
}
.accent-bar {
  background: linear-gradient(90deg, #a78bfa, #818cf8); /* project accent */
}
```

4. Generates HTML, renders to PNG, guides upload.

**Key takeaway:** When a project has established brand colors, adapt the template rather than using defaults. The social preview should feel like it belongs to the project.

---

## Example 3: Audit -- Missing Social Preview

**User:**
```
/social-preview audit ~/Popoloto/Repos.nosync/clawclip
```

**Output:**
```
=== Social Preview Audit: clawclip ===

Custom preview set: NO (using auto-generated)
Description:       "AI-powered agent orchestration dashboard"
Homepage URL:       not set

Recommendations:
  - No custom social preview is set. The auto-generated preview shows the
    default GitHub template (repo name + avatar). This is a missed opportunity
    for any link shared on Twitter, LinkedIn, or Slack.
  - Description is present and good length (42 chars). It will display well
    as the tagline in a generated preview.
  - Consider setting a homepage URL for additional context in OG metadata.

Run /social-preview generate to create one.
```

**User follows up:**
```
/social-preview generate
```

Skill picks up the same repo context, generates a dark-theme preview using the existing description, renders, and walks through the upload flow.

---

## Quick Reference: Common Workflows

| Scenario | Command |
|----------|---------|
| New repo, needs a preview | `/social-preview generate [path]` |
| Check if preview exists | `/social-preview audit [path]` |
| Rebrand -- new colors | `/social-preview generate [path]` (specify brand colors when asked) |
| Major release refresh | `/social-preview generate [path]` (update tagline to mention version) |
