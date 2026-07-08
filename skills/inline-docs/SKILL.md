---
name: inline-docs
description: Generate JSDoc/docstrings from code analysis
disable-model-invocation: true
---

# Inline Documentation Generator

I'll analyze your code and generate comprehensive JSDoc comments, Python docstrings, or Go documentation from function signatures and behavior.

**Supported Languages:**
- JavaScript/TypeScript (JSDoc)
- Python (Google-style, NumPy-style, reStructuredText)
- Go (godoc)
- Java (Javadoc)
- Rust (rustdoc)

## Token Optimization

**Expected range**: 500–2,000 tokens (initial), 100 tokens (fully documented)

**Caching**: No persistent caching — analyzes current file on each run.

**Early exit**: Returns immediately if all public functions already have documentation.

**Patterns used**: Grep-before-Read, early exit, git diff scope default
