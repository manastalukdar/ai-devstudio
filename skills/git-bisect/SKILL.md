---
name: git-bisect
description: Automated git bisect for bug hunting with test script execution
disable-model-invocation: false
---

# Automated Git Bisect - Bug Hunter

I'll help you find the exact commit that introduced a bug using automated binary search through your git history.

Arguments: `$ARGUMENTS` - bug description, test command, or commit range

## Token Optimization

**Expected range**: 1,500–2,500 tokens (initial), 300 tokens (existing session)

**Caching**: No persistent caching — git bisect state is maintained by git itself.

**Early exit**: Returns immediately if a bisect session is already in progress.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries
