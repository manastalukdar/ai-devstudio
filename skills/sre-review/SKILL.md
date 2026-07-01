---
name: sre-review
description: Review code and configuration for SRE concerns — SLO/SLA coverage, observability gaps, toil, alerting blind spots, and reliability anti-patterns
disable-model-invocation: false
risk: safe
---

# SRE Review

Evaluate a service or change for site reliability concerns: missing observability, absent SLOs, high toil, alerting gaps, and patterns that erode error budgets.

## Usage

```
/sre-review                  # review staged changes for reliability regressions
/sre-review <path>           # review a service directory
/sre-review --slo            # focus only on SLO/SLA coverage gaps
/sre-review --toil           # identify and quantify toil sources
```

## Behavior

### Step 1 — Detect service type and observability stack

```bash
# Identify metrics/tracing/logging libraries in use
grep -rn "prometheus\|datadog\|opentelemetry\|jaeger\|statsd\|pino\|winston\|structlog\|zap" \
  --include="*.ts" --include="*.py" --include="*.go" -l . | head -20

# Find existing SLO/alert definitions
find . -name "*.yaml" -o -name "*.yml" | xargs grep -l "slo\|alert\|rule\|record" 2>/dev/null | head -10
```

### Step 2 — Check observability coverage

For each critical path (HTTP endpoints, queue consumers, scheduled jobs), verify:

| Signal | What to look for | Gap indicator |
|---|---|---|
| **Metrics** | Request rate, error rate, latency histogram | No `counter`/`histogram`/`gauge` instrumentation |
| **Traces** | Span creation at service boundaries | No `startSpan`/`tracer.trace`/`@trace` |
| **Logs** | Structured logging with correlation IDs | `console.log`, unstructured strings, no request ID |
| **Health checks** | `/health`, `/ready`, `/live` endpoints | No health endpoint registered |

### Step 3 — Review SLO/SLA coverage

Check for:
- Defined availability target (e.g., 99.9%)
- Error budget burn rate alerts (fast burn: 2% in 1h; slow burn: 5% in 6h)
- Latency SLO (p50, p95, p99 thresholds)
- SLO dashboards or recording rules

If no SLO definitions found, propose a minimal starting set:

```
Suggested SLOs for <service>:
  Availability: 99.9% (allow 43.8 min/month downtime)
  Latency p95:  < 500ms for /api/* endpoints
  Error rate:   < 0.1% of requests return 5xx
```

### Step 4 — Identify toil

Toil is manual, repetitive work that scales with service load. Flag:

- Manual steps in deployment scripts (no automation)
- Ad-hoc fixes applied more than once (visible in git log)
- Runbooks without automation links
- Cron jobs that require human verification
- Alerting rules with no automated remediation

```bash
# Find manual steps or TODOs in ops files
grep -rn "TODO\|FIXME\|manual\|manually\|hand" deploy/ ops/ scripts/ k8s/ 2>/dev/null | head -20
```

### Step 5 — Check alerting quality

For each alert rule found:

- **Signal to noise**: Does the alert fire on symptoms (not causes)?
- **Actionability**: Does the alert link to a runbook?
- **Severity calibration**: Is it paging the right level (P1 vs P2)?
- **Missing alerts**: No alert on error rate, no alert on SLO burn rate

Flag:
- Alerts with no `runbook_url` annotation
- Severity: critical alerts that are informational in practice
- Missing burn-rate alerts when SLOs are defined

### Step 6 — Report findings

```
SRE REVIEW — <service/path>

Observability Gaps (3)
  src/payments/processor.ts   No latency histogram on charge() — p95 invisible
  src/jobs/email-worker.ts    console.log only — no structured logging, no correlation ID
  No /health endpoint         Load balancer cannot distinguish healthy from unhealthy pods

SLO Issues (2)
  No SLO definitions found — error budget burn goes undetected
  Suggested starter SLOs: [see below]

Toil (2)
  scripts/deploy.sh:45   Manual DB migration step before every deploy
  k8s/cronjob.yaml       Nightly report job requires human sign-off email

Alerting Gaps (1)
  No error rate alert — 5xx spikes are invisible until users report them

Reliability Anti-patterns (1)
  src/cache/redis.ts:88   Cache-aside with no stampede protection (thundering herd risk at TTL expiry)

Suggested SLOs:
  Availability: 99.9% | Latency p95: 500ms | Error rate: < 0.1%
```

## Edge Cases

- **No observability libraries**: Recommend adding the lightest option for the detected stack (e.g., `pino` for Node, `structlog` for Python).
- **No staged changes**: Analyze the full path provided in `$ARGUMENTS`.
- **Kubernetes**: Check Deployment `livenessProbe`/`readinessProbe` and resource `requests`/`limits`.
- **Serverless**: Adapt checks for cold-start latency, concurrency limits, and function timeout settings.

## Token Optimization

**Expected range**: 500–1,800 tokens; 100–200 tokens (early exit, no integrations)

**Patterns used**: Grep-before-Read, git diff scope defaults, progressive disclosure (summary then detail per category)

**Early exit**: If `--slo` flag and no YAML config files exist, report the gap immediately without scanning source files.
