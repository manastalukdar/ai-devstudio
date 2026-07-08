---
name: branch-finish
description: Complete branch workflow with squash, rebase, and cleanup
disable-model-invocation: false
---

# Branch Finish Workflow

I'll help you complete your branch workflow with intelligent squashing, rebasing, and cleanup.

Arguments: `$ARGUMENTS` - target branch (defaults to main/master)

## Branch Completion Philosophy

Finish branches cleanly:
- Smart commit squashing with meaningful messages
- Intelligent rebase strategy selection
- Local and remote branch cleanup
- PR/MR status verification
- Integration with `/commit` workflow

## Token Optimization

**Expected range**: 2,000–3,000 tokens (initial), 500 tokens (fast-forward)

**Caching**: Caches branch analysis in `.branch-finish-cache/<branch>/` with a 5-minute TTL.

**Early exit**: Returns immediately for single-commit branches or fast-forward merges.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
