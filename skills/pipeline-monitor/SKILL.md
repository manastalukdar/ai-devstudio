---
name: pipeline-monitor
description: Track build success rates and identify flaky tests from CI logs
disable-model-invocation: false
---

# CI/CD Pipeline Monitor

I'll analyze your CI/CD pipeline metrics, track build success rates, identify flaky tests, and provide performance trend analysis.

Arguments: `$ARGUMENTS` - pipeline platform (github, gitlab, circle), time range, or specific build numbers

## Monitoring Philosophy

- **Data-Driven Insights**: Identify trends, not just failures
- **Flaky Test Detection**: Find tests that fail inconsistently
- **Performance Tracking**: Monitor build duration over time
- **Success Rate Metrics**: Track reliability trends
- **Multi-Platform**: Support GitHub Actions, GitLab CI, CircleCI, Jenkins

---

## Token Optimization

**Expected range**: 400–2,500 tokens (initial), 100 tokens (cache hit)

**Caching**: Caches platform detection in `.claude/cache/pipeline-monitor/platform.json` for 7 days.

**Early exit**: Returns immediately if the pipeline is healthy and no issues are detected.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
