---
name: dependency-audit
description: Comprehensive dependency security and license audit
disable-model-invocation: true
---

# Dependency Security & License Audit

I'll perform comprehensive security and license audits of your project dependencies, identifying vulnerabilities, license issues, and outdated packages.

Arguments: `$ARGUMENTS` - specific packages, severity level, or audit focus

## Audit Philosophy

- **Security First**: Identify all vulnerabilities
- **License Compliance**: Ensure legal compatibility
- **Supply Chain Security**: Verify package integrity
- **Update Strategy**: Safe upgrade paths

## Token Optimization

**Expected range**: 400–1,000 tokens (initial), 50 tokens (no vulnerabilities)

**Caching**: Caches last audit results in `.claude/cache/deps/last-audit.json` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if no vulnerabilities are found.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
