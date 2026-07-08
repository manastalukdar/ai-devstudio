---
name: license-check
description: License compliance checking and conflict detection
disable-model-invocation: true
---

# License Compliance Checker

I'll analyze your project dependencies for license compliance, detect conflicts, and ensure legal compatibility.

Arguments: `$ARGUMENTS` - focus area (commercial, gpl, conflicts) or specific packages

## License Compliance Philosophy

**Core Principles:**
- Identify all dependency licenses
- Detect incompatible license combinations
- Flag copyleft licenses for commercial projects
- Generate compliance documentation
- Track license changes

## Token Optimization

**Expected range**: 300–1,500 tokens (initial), 100 tokens (cache hit)

**Caching**: Caches license results keyed by dependency checksum in `.claude/cache/license-check/` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if all licenses are compatible with the project license.

**Patterns used**: Grep-before-Read, early exit, caching, Bash for system queries
