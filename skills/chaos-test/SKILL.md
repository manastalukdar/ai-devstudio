---
name: chaos-test
description: Analyze codebase for resilience gaps — missing retry logic, absent timeouts, circuit-breaker opportunities, single points of failure, and degradation-mode blind spots
disable-model-invocation: false
risk: safe
---

# Chaos Test — Resilience Gap Analysis

Scan the codebase for failure modes that would surface under real-world stress: network partitions, dependency outages, slow consumers, and burst traffic.

## Usage

```
/chaos-test                  # full scan of staged changes and key integration points
/chaos-test <path>           # target a specific file or directory
/chaos-test --service <name> # focus on a named external service dependency
```

## Behavior

### Step 1 — Identify integration boundaries

```bash
# Find outbound HTTP calls, queue producers/consumers, DB calls, cache hits
grep -rn "fetch\|axios\|http\.\|requests\.\|redis\|pg\.\|mysql\|amqp\|kafka" \
  --include="*.ts" --include="*.py" --include="*.go" --include="*.js" \
  -l . | head -30
```

### Step 2 — Check each boundary for resilience controls

For every integration point found, verify presence of:

| Control | What to grep for | Risk if absent |
|---|---|---|
| Timeout | `timeout`, `AbortController`, `signal` | Hangs under slow upstream |
| Retry | `retry`, `backoff`, `attempt` | Single transient failure = hard failure |
| Circuit breaker | `opossum`, `cockatiel`, `breaker`, `circuitbreaker` | Cascading failure under sustained outage |
| Fallback / degraded mode | `fallback`, `default`, `catch` returning a stub | No graceful degradation |
| Rate-limit handling | `429`, `RateLimitError`, `retry-after` | Thundering herd kills upstream |
| Bulkhead / concurrency cap | `semaphore`, `pLimit`, `asyncio.Semaphore` | Single slow dep starves thread pool |

### Step 3 — Score each boundary

For each integration point, assign a risk tier:

- **Critical** — no timeout AND no retry AND no fallback
- **High** — missing two of the three controls above
- **Medium** — missing one control
- **Low** — all controls present; note any configuration concerns (timeout too high, retry without jitter, etc.)

### Step 4 — Report findings

Output a prioritized list:

```
CHAOS ANALYSIS — <path>

Critical (fix before next deploy)
  src/payments/stripe.ts:42   POST /charges — no timeout, no retry, no fallback
  src/auth/token.ts:88        Redis GET — no timeout; outage causes auth failure

High
  src/search/elastic.ts:17    ES query — no circuit breaker; slow queries block response

Medium
  src/email/sendgrid.ts:31    Retry present but no jitter (thundering herd risk)

Low
  src/cache/redis.ts:55       All controls present; timeout at 30s is high — consider 5s

Suggested experiment targets (fault to inject → expected behavior → gap if wrong):
  1. Kill Redis → auth should degrade to DB lookup → currently: hard 500
  2. Throttle Stripe to 2s → checkout should timeout at 1s → currently: no timeout set
```

### Step 5 — Suggest quick wins

For each Critical/High finding, propose the minimal fix:

```
stripe.ts:42 — Add AbortSignal timeout (5s) and exponential-backoff retry (3 attempts, 100ms base, jitter):
  const res = await fetch(url, { signal: AbortSignal.timeout(5000) })
```

## Edge Cases

- **No external dependencies**: Report "No integration boundaries detected" and exit.
- **Monorepo**: Scan from `$ARGUMENTS` path; skip test files unless `--include-tests` passed.
- **gRPC / GraphQL**: Detect `grpc`, `graphql-request`, and `apollo-client` as integration points.
- **Already uses resilience library**: Note which library is in use and check it is configured, not just imported.

## Token Optimization

**Expected range**: 600–2,000 tokens (grep-driven discovery); 100–300 tokens (no integrations found, early exit)

**Patterns used**: Grep-before-Read (scan for integration points before reading any file), git diff scope (staged changes first), progressive disclosure (summary → details on request)

**Early exit**: If `git diff --staged --name-only` returns no files and no `$ARGUMENTS` path is given, report "No staged changes to analyze" and exit.

**Caching**: Caches file list from boundary scan in `.claude/cache/chaos-test/boundaries.json` (invalidated when `package.json`, `go.mod`, or `requirements.txt` changes).
