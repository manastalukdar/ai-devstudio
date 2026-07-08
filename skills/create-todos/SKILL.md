---
name: create-todos
description: Add contextual TODO comments for future development work
disable-model-invocation: false
---

# Create Smart TODOs

I'll analyze recent operations and create contextual TODO comments in your code.

## Token Optimization

**Expected range**: 400–1,200 tokens (initial), 100 tokens (early exit)

**Caching**: Caches TODO format template in `.claude/cache/create-todos/format.json` for 7 days.

**Early exit**: Returns immediately if the scope already has sufficient TODOs.

**Patterns used**: Grep-before-Read, early exit, git diff scope default
