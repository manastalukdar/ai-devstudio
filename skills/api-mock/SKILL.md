---
name: api-mock
description: Generate API mocks and stub servers from OpenAPI specs or code analysis
disable-model-invocation: false
---

# API Mock Server Generator

I'll help you generate API mock servers and stub services for testing and development, based on OpenAPI specifications or code analysis.

**Mock Server Tools:**
- **json-server**: Simple REST API mocking
- **MSW (Mock Service Worker)**: Browser and Node.js request interception
- **Prism**: OpenAPI-based mock server
- **WireMock**: Advanced API simulation

## Token Optimization

**Expected range**: 2,000–3,000 tokens (initial), 500 tokens (cache hit)

**Caching**: Caches endpoint inventory and mock templates in `.claude/cache/api-mock/` for 7 days. Invalidated when API routes change.

**Early exit**: Returns immediately if mock server already exists for the target routes.

**Patterns used**: Grep-before-Read, early exit, template-based generation, git diff scope default
