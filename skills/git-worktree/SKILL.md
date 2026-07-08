---
name: git-worktree
description: Manage git worktrees for parallel feature development
disable-model-invocation: true
---

# Git Worktree Management

I'll help you manage git worktrees for parallel development workflows.

Arguments: `$ARGUMENTS` - action (add/list/remove) and worktree name

## Worktree Philosophy

Based on **obra/superpowers** parallel development patterns:
- Work on multiple features simultaneously
- Keep main worktree clean
- Isolate experimental branches
- Quick context switching
- No stashing required

## Token Optimization

**Expected range**: 1,500–2,500 tokens (initial), 100 tokens (list-only)

**Caching**: No persistent caching — worktree state is maintained by git itself.

**Early exit**: Returns immediately for list-only operations without creating a new worktree.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries
