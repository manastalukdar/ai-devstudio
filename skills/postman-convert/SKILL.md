---
name: postman-convert
description: Convert Postman collections to automated tests with environment preservation
disable-model-invocation: false
---

# Postman to Automated Tests Converter

I'll help you convert Postman collections into automated test suites, preserving environment variables, authentication, and test assertions.

**Conversion Targets:**
- **Jest + Supertest**: Node.js/Express API tests
- **pytest + requests**: Python API tests
- **Go testing + net/http**: Go API tests
- **REST Assured**: Java API tests

## Token Optimization

**Expected range**: 2,000–3,000 tokens (initial), 100 tokens (already converted)

**Caching**: No persistent caching — converts current collection on each run.

**Early exit**: Returns immediately if an equivalent converted file already exists.

**Patterns used**: Grep-before-Read, early exit, template-based generation
