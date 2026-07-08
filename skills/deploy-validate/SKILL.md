---
name: deploy-validate
description: Pre-deployment validation with environment config, dependencies, DB migrations, and API compatibility checks
disable-model-invocation: true
---

# Deployment Validation

I'll perform comprehensive pre-deployment validation to catch issues before they reach production.

**Validation Checks:**
- Environment configuration
- Dependency verification
- Database migration status
- API compatibility
- Build artifacts
- Security checks

## Token Optimization

**Expected range**: 400–1,500 tokens (initial), 100 tokens (critical failure)

**Caching**: Caches environment config in `.claude/cache/deploy/environment.json` for 7 days.

**Early exit**: Returns immediately on critical validation failures before running remaining checks.

**Patterns used**: Grep-before-Read, early exit, progressive disclosure, caching
