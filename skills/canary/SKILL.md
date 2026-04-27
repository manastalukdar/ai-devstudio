---
name: canary
description: Monitor a deployment for errors and regressions after shipping — polls logs, error rates, and key endpoints in a configurable loop until the deployment is confirmed healthy or a problem is detected.
disable-model-invocation: false
---

# Canary

I'll watch your deployment after it goes live, polling for errors and regressions until health is confirmed or a problem surfaces. Inspired by gstack's canary skill.

## Token Optimization

**Expected range**: 200–600 tokens per poll cycle, 50 tokens (healthy exit)

**Patterns used**: Bash for all checks, early exit (all green on first check), progressive disclosure (status line per cycle → details only on failure)

**Early exit**: If all checks pass on the first cycle, report "Deployment healthy — all checks green" and stop.

## Step 1 — Identify What to Monitor

Infer from the project or accept explicit arguments:

```bash
# Check for common deployment indicators
ls -la .env .env.production docker-compose.yml Procfile 2>/dev/null

# Check for health endpoint conventions
grep -r "health\|ping\|status" --include="*.json" --include="*.yaml" -l 2>/dev/null | head -5

# Check for error log locations
ls -la logs/ /var/log/app.log 2>/dev/null
```

If no targets are auto-detected, ask:
- What URL or endpoint should I poll?
- Where are the application logs?
- What error patterns should I watch for?

## Step 2 — Configure the Watch Loop

**Defaults (override via arguments):**
- Poll interval: 30 seconds
- Max duration: 10 minutes
- Error threshold: 2 consecutive failures = alert
- Success threshold: 3 consecutive passes = declare healthy

```bash
# Example: /canary --url https://api.example.com/health --interval 30 --duration 10m
```

## Step 3 — Poll Loop

Each cycle runs these checks in order. Stop looping on first FAIL or when success threshold is reached.

### Check A — HTTP Health Endpoint

```bash
# Poll the health/status endpoint
status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$HEALTH_URL" 2>/dev/null)
echo "HTTP $status — $(date '+%H:%M:%S')"
```

**Pass**: 200–299  
**Warn**: 3xx or slow response (>2s)  
**Fail**: 4xx, 5xx, timeout

### Check B — Error Log Scan

```bash
# Scan for new errors since last cycle
tail -n 50 "$LOG_FILE" 2>/dev/null | grep -iE "error|exception|fatal|panic|crash" | tail -5
```

**Pass**: No new errors  
**Warn**: Errors matching known non-critical patterns  
**Fail**: New unrecognized error or stack trace

### Check C — Key Endpoint Smoke Test

```bash
# Hit one or two critical endpoints beyond the health check
for endpoint in "${CRITICAL_ENDPOINTS[@]}"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$endpoint")
    echo "  $endpoint → $code"
done
```

### Check D — Error Rate (if metrics available)

```bash
# If a metrics endpoint is available (Prometheus, Datadog, etc.)
# Check error rate is below threshold
```

## Step 4 — Report Each Cycle

```
Canary — cycle 3/20 — 14:32:05

  ✓ Health endpoint    200 (142ms)
  ✓ Error log          0 new errors
  ✓ /api/users         200
  ✓ /api/health        200

Status: WATCHING (3 consecutive passes — need 3 to declare healthy)
```

## Step 5 — Terminal States

**HEALTHY**: Three consecutive all-pass cycles:
```
Canary — HEALTHY after 4 minutes

All checks passed 3× in a row. Deployment is confirmed healthy.
```

**ALERT**: Two consecutive failures on any check:
```
Canary — ALERT — cycle 6

  ✗ Health endpoint    503 (timeout)
  ✓ Error log          0 new errors

Action required: health endpoint is returning 503. Check logs and consider rollback.
Suggest: /deployment-rollback
```

**TIMEOUT**: Max duration reached without declaring healthy:
```
Canary — INCONCLUSIVE after 10 minutes

No failures detected, but success threshold not reached.
Recommend: extend monitoring or check manually.
```

## Edge Cases

- **No health endpoint**: Fall back to checking error logs only; note the limitation
- **Flaky endpoint** (intermittent 5xx): Apply jitter to poll interval; require 2 consecutive failures to alert
- **No log access**: Skip log check; note it was skipped
- **CI environment**: Disable interactive output; write results to `.claude/canary-results.json`
