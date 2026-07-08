---
name: find-todos
description: Locate development tasks and TODO comments across the codebase
disable-model-invocation: false
---

# Find Development Tasks

I'll locate all TODO comments and unfinished work markers in your codebase.

## Token Optimization

**Expected range**: 100–400 tokens (initial), 50 tokens (cache hit)

**Caching**: Caches TODO inventory in `.claude/cache/find-todos/todo-inventory.json` for 7 days. Invalidated when source files change.

**Early exit**: Returns immediately if no TODO/FIXME/HACK patterns are found.

**Patterns used**: Grep-before-Read, early exit, git diff scope default
