---
name: debug-session
description: Document debugging sessions with hypothesis tracking and knowledge base
disable-model-invocation: true
---

# Debug Session Documentation

I'll create structured documentation for your debugging session to build a knowledge base and track your investigation process.

**Based on session management patterns:**
- Create structured debug logs in `.claude/debugging/`
- Hypothesis tracking with test results
- Solution documentation
- Timeline of investigation
- Knowledge base building for future reference

**Arguments:** `$ARGUMENTS` - session name or issue description

---

## Token Optimization

**Expected range**: 150–1,200 tokens (initial), 50 tokens (session update)

**Caching**: Caches current debug session in `.claude/cache/debug-session/current.json` for 7 days.

**Early exit**: Returns immediately for session updates, skipping full re-analysis.

**Patterns used**: Grep-before-Read, early exit, caching, progressive disclosure
