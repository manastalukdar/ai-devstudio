---
name: graphql-schema
description: GraphQL schema validation and optimization with federation support
disable-model-invocation: true
---

# GraphQL Schema Validation & Optimization

I'll validate and optimize your GraphQL schema with support for federation, deprecated fields, and performance improvements.

**Features:**
- Schema validation and linting
- Query optimization suggestions
- Federation support analysis
- Schema stitching validation
- Deprecated field detection
- Breaking change detection

## Token Optimization

**Expected range**: 1,500–2,500 tokens (initial), 100 tokens (valid schema)

**Caching**: No persistent caching — validates current schema on each run.

**Early exit**: Returns immediately if the schema is already valid with no type errors.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries
