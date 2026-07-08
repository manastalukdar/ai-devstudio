---
name: owasp-check
description: OWASP Top 10 vulnerability scanning and remediation
disable-model-invocation: true
---

# OWASP Top 10 Vulnerability Scanner

I'll scan your application for OWASP Top 10 vulnerabilities and provide remediation guidance for common web security issues.

Arguments: `$ARGUMENTS` - specific vulnerability category or full scan

## OWASP Top 10 (2021) Coverage

**Vulnerabilities Checked:**
1. **A01:2021** - Broken Access Control
2. **A02:2021** - Cryptographic Failures
3. **A03:2021** - Injection (SQL, NoSQL, Command)
4. **A04:2021** - Insecure Design
5. **A05:2021** - Security Misconfiguration
6. **A06:2021** - Vulnerable Components
7. **A07:2021** - Authentication Failures
8. **A08:2021** - Data Integrity Failures
9. **A09:2021** - Logging & Monitoring Failures
10. **A10:2021** - Server-Side Request Forgery (SSRF)

## Token Optimization

**Expected range**: 600–1,000 tokens (quick scan), 1,500–3,000 tokens (full scan)

**Caching**: Caches vulnerability patterns in `.claude/cache/owasp-check/patterns/` for 7 days.

**Early exit**: Returns immediately on critical findings to surface them without scanning low-priority code.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching, progressive disclosure
