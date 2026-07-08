---
name: remove-comments
description: Clean obvious and redundant comments from code
disable-model-invocation: false
---

# Remove Obvious Comments

I'll clean up redundant comments while preserving valuable documentation.

## Token Optimization

**Expected range**: 200–400 tokens (small project), 50 tokens (cache hit)

**Caching**: Caches comment patterns in `.claude/cache/remove-comments/` for 7 days. Invalidated when source files change.

**Early exit**: Returns immediately if no comments are detected in changed files.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
