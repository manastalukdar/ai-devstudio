---
name: lighthouse
description: Run Lighthouse audits and implement performance, accessibility, and SEO fixes
disable-model-invocation: false
---

# Lighthouse Performance Auditing & Fixes

I'll run comprehensive Lighthouse audits for performance, accessibility, SEO, and best practices, then implement prioritized fixes automatically.

**Audit Categories:**
- Performance (Core Web Vitals: LCP, FID, CLS)
- Accessibility (WCAG compliance)
- SEO (Search engine optimization)
- Best Practices (Security, modern standards)
- PWA (Progressive Web App)

**Arguments:** `$ARGUMENTS` - optional: URL to audit (defaults to http://localhost:3000) or mobile/desktop

<think>
Lighthouse auditing requires understanding:
- Core Web Vitals (LCP, FID, CLS) impact on user experience
- Accessibility barriers and WCAG guidelines
- SEO best practices and meta tag requirements
- Performance optimization opportunities
- Progressive enhancement strategies
</think>

---

## Token Optimization

**Expected range**: 300–2,800 tokens (initial), 100 tokens (good scores)

**Caching**: Caches last audit results in `.claude/cache/lighthouse/last-audit.json` for 7 days.

**Early exit**: Returns immediately if all Lighthouse scores are above the threshold.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
