---
name: deployment-rollback
description: Safe deployment rollback with health checks and database migration reversal
disable-model-invocation: false
---

# Safe Deployment Rollback

I'll help you safely rollback deployments with automated health checks, database migration reversal, and multi-environment support.

**Rollback Capabilities:**
- Application version rollback
- Database migration reversal
- Infrastructure state restoration
- Configuration rollback
- Health monitoring and validation

Arguments: `$ARGUMENTS` - environment (staging/production), version, or rollback target

---

## Token Optimization

**Expected range**: 800–2,500 tokens (initial), 200 tokens (safe state)

**Caching**: Caches platform detection in `.claude/cache/deployment-rollback/platform.json` for 7 days.

**Early exit**: Returns immediately if the deployment is already in a safe state.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
