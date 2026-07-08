---
name: release-automation
description: Automate complete release process with versioning and publishing
disable-model-invocation: true
---

# Release Automation

I'll automate your complete release process: version bumping, changelog generation, git tagging, release creation, and package publishing.

Arguments: `$ARGUMENTS` - version number (e.g., 1.2.0, major, minor, patch) or release type

## Release Philosophy

- **Semantic Versioning**: Proper MAJOR.MINOR.PATCH versioning
- **Automated Changelog**: Generated from conventional commits
- **Safe Defaults**: Validate before publishing
- **Platform Agnostic**: Support npm, PyPI, Go modules, Ruby gems, Cargo, Maven

---

## Token Optimization

**Expected range**: 800–2,500 tokens (initial), 100 tokens (clean state)

**Caching**: Caches package info in `.claude/cache/release-automation/package-info.json` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if the working tree is not clean.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
