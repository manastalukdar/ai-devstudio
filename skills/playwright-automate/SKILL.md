---
name: playwright-automate
description: Browser automation workflows with Playwright MCP integration
disable-model-invocation: true
---

# Playwright Browser Automation

I'll help you automate browser tasks using Playwright for testing, screenshots, PDFs, and workflow automation.

Arguments: `$ARGUMENTS` - automation task (screenshot, pdf, scrape, test) or specific URL/workflow

## Automation Capabilities

**Common Workflows:**
- Browser testing and validation
- Screenshot capture (full page, specific elements)
- PDF generation from web pages
- Web scraping and data extraction
- Form automation and submissions
- Performance monitoring

## Token Optimization

**Expected range**: 500–2,000 tokens (initial), 100 tokens (no Playwright)

**Caching**: Caches selector patterns in `.claude/cache/playwright-automate/selector-patterns.json` for 7 days.

**Early exit**: Returns immediately if Playwright is not installed in the project.

**Patterns used**: Grep-before-Read, early exit, template-based generation, caching
