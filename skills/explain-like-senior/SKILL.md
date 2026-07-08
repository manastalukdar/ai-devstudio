---
name: explain-like-senior
description: Senior-level code explanations with deep technical insights and context
disable-model-invocation: false
---

# Senior Developer Explanation

I'll explain this code as a senior developer would, focusing on the why behind decisions.

## Token Optimization

**Expected range**: 350–2,500 tokens (initial), 100 tokens (cache hit)

**Caching**: Caches architecture analysis in `.claude/cache/understand/architecture.json` for 7 days.

**Early exit**: Returns immediately if the target is too simple to require senior-level explanation.

**Patterns used**: Grep-before-Read, early exit, caching, progressive disclosure
