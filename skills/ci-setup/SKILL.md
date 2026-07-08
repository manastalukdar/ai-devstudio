---
name: ci-setup
description: Configure CI/CD pipelines for GitHub Actions, GitLab CI, CircleCI with best practices
disable-model-invocation: true
---

# CI/CD Pipeline Setup

I'll set up a production-ready CI/CD pipeline with automated testing, linting, and deployment workflows.

**Supported Platforms:**
- GitHub Actions (auto-detected from .git/config)
- GitLab CI (.gitlab-ci.yml)
- CircleCI (circle CI config)
- Jenkins (Jenkinsfile)

## Token Optimization

**Expected range**: 400–1,000 tokens (initial), 100 tokens (cache hit)

**Caching**: Caches platform config in `.claude/cache/ci/platform-config.json` for 7 days. Invalidated when `.github/` or CI config changes.

**Early exit**: Returns immediately if CI configuration already exists and passes validation.

**Patterns used**: Grep-before-Read, early exit, template-based generation, caching
