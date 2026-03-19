---
name: react-best-practices
description: Comprehensive React and Next.js performance optimization guide with 40+ rules for eliminating waterfalls, optimizing bundles, and improving rendering. Use when optimizing React apps, reviewing performance, or refactoring components.
license: MIT
origin: marketplace
author: Vercel Engineering
author_url: https://vercel.com
metadata:
  version: 1.0.0
  category: developer-tools
  domain: react
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# React Best Practices — Performance Optimization

40+ performance optimization rules for React and Next.js applications organized by impact level.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/react-best-practices ~/.claude/skills/
```

## When to Use

- Optimizing React or Next.js application performance
- Reviewing code for performance improvements
- Refactoring existing components
- Debugging slow rendering or loading issues
- Reducing bundle size
- Eliminating request waterfalls

## Quick Reference — Critical Priorities

1. **Defer await until needed** — Move awaits into branches where they are used
2. **Use Promise.all()** — Parallelize independent async operations
3. **Avoid barrel imports** — Import directly from source files
4. **Dynamic imports** — Lazy-load heavy components
5. **Strategic Suspense** — Stream content while showing layout

## Categories

### 1. Eliminating Waterfalls (CRITICAL)
The #1 performance killer. Each sequential await adds full network latency.

### 2. Bundle Size Optimization (CRITICAL)
Reducing initial bundle improves TTI and LCP.

### 3. Server-Side Performance (HIGH)
Optimize RSC and data fetching.

### 4. Client-Side Data Fetching (MEDIUM-HIGH)
Automatic deduplication and efficient patterns.

### 5. Re-render Optimization (MEDIUM)
Reduce unnecessary re-renders.

### 6. Rendering Performance (MEDIUM)
Optimize browser rendering process.

### 7. JavaScript Performance (LOW-MEDIUM)
Micro-optimizations for hot paths.

### 8. Advanced Patterns (LOW)
Specialized techniques for edge cases.

## Implementation Approach

1. **Profile first**: Use React DevTools Profiler and browser performance tools
2. **Focus on critical paths**: Start with waterfalls and bundle size
3. **Measure impact**: Verify with LCP, TTI, FID metrics
4. **Apply incrementally**: Do not over-optimize prematurely
5. **Test thoroughly**: Ensure optimizations do not break functionality

## Complete Guidelines

The full 40+ rules with code examples are in `references/react-performance-guidelines.md`.

## Key Metrics

- **TTI**: When page becomes fully interactive
- **LCP**: When main content is visible
- **FID**: Responsiveness to user interactions
- **CLS**: Visual stability
- **Bundle size**: Initial JavaScript payload
