---
name: merge-strategy
description: Intelligent merge/rebase strategy selection with safe execution
disable-model-invocation: false
---

# Intelligent Merge Strategy Selector

I'll help you choose the optimal Git merge strategy and execute it safely based on branch analysis, history, and team conventions.

Arguments: `$ARGUMENTS` - branch name, strategy preference (merge/rebase/squash), or 'auto'

## Token Optimization

**Expected range**: 1,500–2,500 tokens (initial), 100 tokens (fast-forward)

**Caching**: No persistent caching — analyzes current git state on each run.

**Early exit**: Returns immediately if the merge is a clean fast-forward.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries
