---
name: complexity-reduce
description: Reduce cyclomatic complexity with targeted refactoring strategies
disable-model-invocation: false
---

# Cyclomatic Complexity Reduction

I'll analyze your code for high cyclomatic complexity, identify complex functions and methods, and suggest targeted refactoring strategies to improve maintainability.

**Supported Languages:**
- JavaScript/TypeScript (ESLint complexity rules)
- Python (Radon, mccabe)
- Go (gocyclo)
- Java (Checkstyle complexity)

## Token Optimization

**Expected range**: 1,500–2,500 tokens (initial), 400 tokens (cache hit)

**Caching**: Caches complexity analysis in `.claude/cache/complexity/` for 7 days. Invalidated when source files change.

**Early exit**: Returns immediately if all functions are below the complexity threshold.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, Bash for system queries
