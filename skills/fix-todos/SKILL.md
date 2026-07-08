---
name: fix-todos
description: Intelligent TODO resolution with context-aware implementation
disable-model-invocation: false
---

# Fix TODOs

I'll systematically find and resolve TODO comments in your codebase with intelligent understanding and continuity across sessions.

Arguments: `$ARGUMENTS` - files, directories, or specific TODO patterns to fix

## Token Optimization

**Expected range**: 500–1,500 tokens (initial), 100 tokens (no TODOs)

**Caching**: Caches TODO state in `.claude/cache/fix-todos/` for 7 days.

**Early exit**: Returns immediately if no TODOs are found in the current scope.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, progressive disclosure
