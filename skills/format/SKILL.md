---
name: format
description: Auto-detect and apply code formatting using project's configured formatter
disable-model-invocation: true
---

# Auto Format Code

I'll format your code using the project's configured formatter.

## Token Optimization

**Expected range**: 200–800 tokens (initial), 50 tokens (no changes)

**Caching**: Caches formatter configuration in `.claude/cache/format/` for 7 days. Invalidated when formatter config files change.

**Early exit**: Returns immediately if no files have changed since last format run.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
