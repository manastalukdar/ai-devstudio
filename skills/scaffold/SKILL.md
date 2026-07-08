---
name: scaffold
description: Generate complete feature structures based on your project patterns with full continuity
disable-model-invocation: true
---

# Intelligent Scaffolding

I'll create complete feature structures based on your project patterns, with full continuity across sessions.

Arguments: `$ARGUMENTS` - feature name or component to scaffold

---

## Token Optimization

**Expected range**: 1,200–2,000 tokens (initial), 100 tokens (already exists)

**Caching**: Caches project analysis in `.claude/cache/understand/project-analysis.json` for 7 days.

**Early exit**: Returns immediately if the requested feature or component already exists.

**Patterns used**: Grep-before-Read, early exit, template-based generation, caching
