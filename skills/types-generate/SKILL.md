---
name: types-generate
description: Generate TypeScript types from schemas/APIs
disable-model-invocation: true
---

# TypeScript Type Generator

I'll generate TypeScript types and interfaces from various sources: JSON schemas, OpenAPI specs, GraphQL schemas, databases, and API responses.

Arguments: `$ARGUMENTS` - schema file, API endpoint, or database connection

## Type Generation Philosophy

- **Type Safety**: Comprehensive type coverage
- **DRY**: Single source of truth
- **Documentation**: Generated JSDoc comments
- **Validation**: Runtime type guards included

---

## Token Optimization

**Expected range**: 500–2,000 tokens (initial), 100 tokens (types current)

**Caching**: Caches schema checksums in `.claude/cache/types/schema-checksums.json` for 7 days. Invalidated when schema files change.

**Early exit**: Returns immediately if schema checksums match cached values.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
