---
name: docx
description: Comprehensive Word document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when working with .docx files for creating new documents, modifying existing content, adding tracked changes (redlining), or extracting and analyzing document contents.
license: MIT
origin: anthropic
author: Anthropic
author_url: https://github.com/anthropics
metadata:
  version: 1.0.0
  category: developer-tools
  domain: document-management
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# DOCX Creation, Editing, and Analysis

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/docx ~/.claude/skills/
```

## Overview

Work with .docx files — create, edit, or analyze. A .docx file is a ZIP archive containing XML files and other resources that can be read or edited directly.

## Workflow Decision Tree

### Reading/Analyzing Content
Use text extraction or raw XML access sections below.

### Creating New Document
Use the docx-js workflow (JavaScript/TypeScript).

### Editing Existing Document
- **Your own document + simple changes**: Use basic OOXML editing workflow
- **Someone else's document**: Use **redlining workflow** (recommended)
- **Legal, academic, business, or government docs**: Use **redlining workflow** (required)

## Reading and Analyzing Content

### Text Extraction
Convert to markdown using pandoc:
```bash
pandoc --track-changes=all path-to-file.docx -o output.md
```

### Raw XML Access
For comments, complex formatting, metadata, and embedded media — unpack the document:
```bash
python ooxml/scripts/unpack.py <office_file> <output_directory>
```

Key files: `word/document.xml` (main content), `word/comments.xml` (comments), `word/media/` (images).

## Creating a New Word Document

Use **docx-js** (JavaScript/TypeScript):

1. **Read `docx-js.md`** for detailed syntax and best practices
2. Create a JavaScript file using Document, Paragraph, TextRun components
3. Export as .docx using `Packer.toBuffer()`

## Editing an Existing Document

Use the **Document library** (Python OOXML manipulation):

1. **Read `ooxml.md`** for the Document library API and XML patterns
2. Unpack: `python ooxml/scripts/unpack.py <file.docx> <dir>`
3. Create and run a Python script using the Document library
4. Pack: `python ooxml/scripts/pack.py <dir> <output.docx>`

## Redlining Workflow

For tracked changes with professional-quality diffs:

1. **Get markdown**: `pandoc --track-changes=all file.docx -o current.md`
2. **Identify and group changes** into batches of 3-10 related edits
3. **Read `ooxml.md`** and unpack the document
4. **Implement changes in batches** using the Document library
5. **Pack the document**: `python ooxml/scripts/pack.py unpacked/ reviewed.docx`
6. **Verify**: Convert final document and check all changes applied

**Principle: Minimal, Precise Edits** — Only mark text that actually changes. Break replacements into [unchanged] + [deletion] + [insertion] + [unchanged].

## Converting Documents to Images

```bash
soffice --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

## Dependencies

- **pandoc**: Text extraction and markdown conversion
- **docx** (npm): Creating new documents
- **LibreOffice**: PDF conversion
- **Poppler** (pdftoppm): PDF to image conversion
- **defusedxml** (pip): Secure XML parsing
