---
name: memory-leak
description: Memory leak detection and analysis for Node.js, Python, and browsers
disable-model-invocation: false
---

# Memory Leak Detection & Analysis

I'll help you detect, analyze, and fix memory leaks across your application stack.

Arguments: `$ARGUMENTS` - runtime environment (node/python/browser) or specific files

---

## Token Optimization

**Expected range**: 200–2,000 tokens (initial), 100 tokens (no leak pattern)

**Caching**: Caches runtime detection in `.claude/cache/memory-leak/runtime.json` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if no memory leak patterns are detected.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
