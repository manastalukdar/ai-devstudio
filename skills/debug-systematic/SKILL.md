---
name: debug-systematic
description: Systematic debugging workflow with hypothesis testing
disable-model-invocation: false
---

# Systematic Debugging Workflow

I'll help you debug issues systematically using the scientific method - hypothesis formation, testing, and iterative refinement.

Arguments: `$ARGUMENTS` - error description, reproduction steps, or context

## Token Optimization

**Expected range**: 1,500–3,000 tokens (initial), 400 tokens (cache hit)

**Caching**: Caches debug state in `.claude/cache/debug/` for 7 days.

**Early exit**: Returns immediately if error pattern matches a known cached solution.

**Patterns used**: Grep-before-Read, early exit, caching, progressive disclosure
