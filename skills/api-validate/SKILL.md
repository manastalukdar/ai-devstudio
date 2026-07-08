---
name: api-validate
description: API contract validation and breaking change detection
disable-model-invocation: false
---

# API Contract Validation

I'll analyze your API contracts for breaking changes, compatibility issues, and schema validation.

Arguments: `$ARGUMENTS` - API spec paths, comparison targets, or validation focus

## Token Optimization

**Expected range**: 200–500 tokens (initial), 50–100 tokens (cache hit)

**Caching**: Caches schema checksums in `.claude/cache/api/` for 7 days. Invalidated when schema files change.

**Early exit**: Returns immediately if schema checksums match cached values.

**Patterns used**: Grep-before-Read, early exit, checksum-based caching, git diff scope default
