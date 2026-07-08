---
name: docs
description: Smart documentation management for creating and updating project documentation
disable-model-invocation: false
---

# Documentation Manager

I'll intelligently manage your project documentation by analyzing what actually happened and updating ALL relevant docs accordingly.

---

## Token Optimization

**Expected range**: 1,200–2,000 tokens (initial), 300 tokens (cache hit)

**Caching**: Caches framework detection in `.claude/cache/docs/framework.json` for 7 days. Invalidated when source files change.

**Early exit**: Returns immediately if no source changes are detected.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
