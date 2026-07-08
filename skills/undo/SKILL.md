---
name: undo
description: Rollback the last destructive operation using git or project backups
disable-model-invocation: true
---

# Undo Last Operation

I'll help you rollback the last destructive operation performed by AI DevStudio commands.

## Token Optimization

**Expected range**: 100–500 tokens (initial), 50 tokens (already clean)

**Caching**: Uses shared cache in `.claude/cache/` — no undo-specific cache.

**Early exit**: Returns immediately if the working tree is already clean with no stashes.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries
