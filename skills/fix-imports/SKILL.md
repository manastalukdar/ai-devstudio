---
name: fix-imports
description: Repair broken imports automatically across the project
disable-model-invocation: false
---

# Fix Broken Imports

I'll systematically fix import statements broken by file moves or renames, with full continuity across sessions.

Arguments: `$ARGUMENTS` - specific paths or import patterns to fix

## Token Optimization

**Expected range**: 750–1,150 tokens (initial), 200 tokens (cache hit)

**Caching**: Caches import patterns in `.claude/cache/fix-imports/patterns.json` for 7 days. Invalidated when `tsconfig.json` changes.

**Early exit**: Returns immediately if no broken imports are detected in staged/changed files.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
