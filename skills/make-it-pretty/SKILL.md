---
name: make-it-pretty
description: Improve code readability through formatting and structure enhancements
disable-model-invocation: false
---

# Make It Pretty

I'll improve code readability while preserving exact functionality.

## Token Optimization

**Expected range**: 300–1,600 tokens (initial), 100 tokens (cache hit)

**Caching**: Caches style patterns in `.claude/cache/make-it-pretty/` for 7 days. Invalidated when CSS/style files change.

**Early exit**: Returns immediately if no style issues are detected in changed files.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
