---
name: implement
description: Import and adapt code from any source to your project with validation and testing
disable-model-invocation: false
---

# Smart Implementation Engine

I'll intelligently implement features from any source - adapting them perfectly to your project's architecture while maintaining your code patterns and standards.

Arguments: `$ARGUMENTS` - URLs, paths, or descriptions of what to implement

## Token Optimization

**Expected range**: 800–3,000 tokens (initial), 200 tokens (cache hit)

**Caching**: Loads project patterns from `.claude/cache/understand/` for 7 days. Invalidated when project structure changes.

**Early exit**: Returns immediately if the requested feature is already implemented.

**Patterns used**: Grep-before-Read, early exit, caching, git diff scope default
