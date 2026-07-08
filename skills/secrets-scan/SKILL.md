---
name: secrets-scan
description: Scan for exposed secrets/credentials/API keys
disable-model-invocation: true
---

# Secrets & Credentials Scanner

I'll scan your codebase for exposed secrets, credentials, API keys, and sensitive information, preventing security breaches before they happen.

Arguments: `$ARGUMENTS` - specific paths, secret types, or scan depth

## Secrets Scanning Philosophy

- **Prevent Leaks**: Find secrets before commit
- **Zero False Positives**: Smart pattern matching
- **Git History**: Scan entire commit history
- **Remediation**: Clear fix instructions

## Token Optimization

**Expected range**: 100–500 tokens (initial), 50 tokens (cache hit)

**Caching**: Caches file checksums in `.claude/cache/secrets/file-checksums.json` for 7 days. Invalidated when files change.

**Early exit**: Returns immediately if all files match cached checksums with no secrets detected.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
