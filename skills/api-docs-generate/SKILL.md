---
name: api-docs-generate
description: Generate OpenAPI/Swagger documentation from code analysis
disable-model-invocation: true
---

# API Documentation Generation

I'll generate comprehensive OpenAPI/Swagger documentation from your API code.

**Features:**
- Auto-generate from Express, FastAPI, Next.js API routes
- OpenAPI 3.0 specification format
- Interactive Swagger UI setup
- Automatic schema extraction
- Integration with `/api-test-generate`

## Token Optimization

**Expected range**: 1,500–2,500 tokens (initial), 400–600 tokens (cache hit)

**Caching**: Caches OpenAPI spec analysis in `.claude/cache/api-docs/` for 7 days. Invalidated when API routes change.

**Early exit**: Returns immediately if spec already exists and is current.

**Patterns used**: Grep-before-Read, early exit, template-based generation, git diff scope default
