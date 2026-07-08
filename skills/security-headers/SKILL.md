---
name: security-headers
description: Web security headers validation and configuration generation
disable-model-invocation: true
---

# Security Headers Validation

I'll analyze and implement web security headers (CSP, HSTS, X-Frame-Options, etc.) to protect against common attacks.

Arguments: `$ARGUMENTS` - URL to check, or framework for configuration generation

## Security Headers Overview

**Essential Headers:**
- **Content-Security-Policy (CSP)** - Prevent XSS and injection attacks
- **Strict-Transport-Security (HSTS)** - Enforce HTTPS
- **X-Frame-Options** - Prevent clickjacking
- **X-Content-Type-Options** - Prevent MIME sniffing
- **Referrer-Policy** - Control referrer information
- **Permissions-Policy** - Feature access control

## Token Optimization

**Expected range**: 400–1,500 tokens (initial), 100 tokens (server not accessible)

**Caching**: Caches header analysis in `.claude/cache/security-headers/` for 7 days.

**Early exit**: Returns immediately if the server is not accessible at the target URL.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching, progressive disclosure
