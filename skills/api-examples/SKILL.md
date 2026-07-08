---
name: api-examples
description: Generate API usage examples and tutorials from code analysis
disable-model-invocation: false
---

# API Examples & Tutorial Generator

I'll analyze your API and generate comprehensive usage examples, code snippets, and tutorials for developers.

Arguments: `$ARGUMENTS` - specific API focus or language (e.g., "REST", "GraphQL", "python", "javascript")

## Strategic Planning Process

<think>
Effective API examples require understanding:

1. **API Analysis**
   - What type of API? (REST, GraphQL, gRPC, WebSocket)
   - What endpoints/operations exist?
   - What's the authentication method?
   - What are common use cases?
   - What error handling is needed?

2. **Audience Consideration**
   - Who are the API consumers? (internal, external, partners)
   - What languages do they use?
   - What's their experience level?
   - What examples will be most valuable?

3. **Example Types**
   - Quick start / Getting started
   - Authentication examples
   - CRUD operation examples
   - Complex workflow examples
   - Error handling patterns
   - Best practices and anti-patterns

4. **Format & Organization**
   - Code snippets for common operations
   - Complete working examples
   - Interactive tutorials
   - SDK usage examples
   - cURL/HTTP examples for testing
</think>

## Token Optimization

**Expected range**: 800–2,000 tokens (initial), 200 tokens (cache hit)

**Caching**: Caches API schema in `.claude/cache/api/api_schema.json` for 7 days. Invalidated when API routes change.

**Early exit**: Returns immediately if examples already exist for the target endpoint.

**Patterns used**: Grep-before-Read, early exit, caching, template-based generation
