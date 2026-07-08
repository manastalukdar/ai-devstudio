---
name: brainstorm
description: Interactive design refinement with structured exploration
disable-model-invocation: false
---

# Interactive Design Brainstorming

I'll help you explore and refine design ideas through structured brainstorming sessions with comprehensive documentation.

Arguments: `$ARGUMENTS` - design challenge, feature idea, or problem to solve

## Token Optimization

**Expected range**: 1,200–2,500 tokens (initial), 300 tokens (cache hit)

**Caching**: Caches session state in `.claude/cache/brainstorm/session-state.json` for 7 days.

**Early exit**: Returns immediately if an identical brainstorm session result exists in cache.

**Patterns used**: Grep-before-Read, early exit, caching, progressive disclosure
