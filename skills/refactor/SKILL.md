---
name: refactor
description: Structured code restructuring preserving functionality with continuous validation
disable-model-invocation: false
---

# Intelligent Refactoring Engine

I'll help you restructure your code systematically - preserving functionality while improving structure, readability, and maintainability.

Arguments: `$ARGUMENTS` - files, directories, or refactoring scope

## Token Optimization

**Expected range**: 1,500–4,000 tokens (initial), 400 tokens (resumed session)

**Caching**: Caches refactoring patterns in `.claude/cache/refactor/patterns.json` for 7 days. Invalidated when source files change.

**Early exit**: Returns immediately for resumed sessions, skipping already-completed changes.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching, progressive disclosure
