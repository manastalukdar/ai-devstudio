---
name: todos-to-issues
description: Scan codebase for TODO comments and create professional GitHub issues with context
disable-model-invocation: true
---

# TODOs to GitHub Issues

I'll scan your codebase for TODO comments and create professional GitHub issues following your project's standards.

## Token Optimization

**Expected range**: 100–400 tokens (initial), 50 tokens (no new TODOs)

**Caching**: Loads TODO inventory from `.claude/cache/find-todos/todo-inventory.json` if available.

**Early exit**: Returns immediately if no new TODOs exist since last sync.

**Patterns used**: Grep-before-Read, early exit, caching
