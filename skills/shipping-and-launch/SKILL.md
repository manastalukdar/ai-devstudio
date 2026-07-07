---
name: shipping-and-launch
description: Unified pre-launch checklist + staged rollout strategy (0%→5%→25%→100%) + rollback triggers — consolidates deploy validation, canary monitoring, and rollback planning in one workflow.
disable-model-invocation: false
risk: safe
---

# Shipping and Launch

I'll run the complete pre-launch checklist, configure a staged rollout, and define explicit rollback triggers before anything goes to production.

Arguments: `$ARGUMENTS` — service, feature, or release to ship; optionally include rollout target (e.g., "user-service v2.3.1")

## Token Optimization

**Expected range**: 800–2,500 tokens (full checklist run)

**Early exit**: If any Phase 1 (code quality) check fails, stop and report — do not proceed to later phases

**Patterns used**: Bash for all checks, progressive disclosure (phase summary before details), git diff scope

## Phase 1 — Code Quality Gate

```bash
# Run tests
npm test 2>&1 | tail -5  # or pytest / go test / cargo test

# Check for uncommitted changes
git status --short

# Verify build succeeds
npm run build 2>&1 | tail -10  # or equivalent

# Check for obvious secrets/credentials in diff
git diff HEAD~1..HEAD | grep -iE "password|secret|token|api.key|private.key" | grep "^+" | grep -v ".example\|.md"
```

Gate: all tests pass, build succeeds, no secrets in diff. Hard stop on any failure.

## Phase 2 — Security Checklist

Quick security scan against staged changes:

```bash
# Check dependencies for known vulnerabilities
npm audit --audit-level=high 2>/dev/null | tail -10
# or: pip-audit, cargo audit, bundle audit

# Verify auth is not accidentally bypassed
git diff HEAD~1..HEAD | grep -iE "auth|permission|role|admin" | grep "^+" | head -20
```

Report:
```
Security:
  Dependency vulnerabilities (high+): [N]
  Auth changes (review required): [N lines]
  Status: [PASS / REVIEW REQUIRED / FAIL]
```

## Phase 3 — Observability Checklist

Verify the deployment can be monitored:

```bash
# Check for health endpoint
grep -rn "health\|ping\|ready\|live" --include="*.ts" --include="*.js" --include="*.py" . | grep -E "route|endpoint|path" | head -5

# Verify error logging
grep -rn "console\.error\|logger\.error\|log\.error" --include="*.ts" --include="*.js" --include="*.py" . | grep -v "node_modules" | wc -l

# Check for structured logging
grep -rn "trace_id\|request_id\|correlation" . | grep -v "node_modules" | wc -l
```

Report:
```
Observability:
  Health endpoint: [present / missing]
  Error logging coverage: [N callsites]
  Structured logging (trace IDs): [present / missing]
  Status: [PASS / NEEDS WORK]
```

## Phase 4 — Staged Rollout Plan

Define explicit gates for each rollout stage:

```
Rollout plan for: [service/feature]

Stage 0% → 5%   (canary)
  Duration: 30 minutes minimum
  Success criteria:
    - Error rate < [baseline + 0.5%]
    - p99 latency < [baseline + 20%]
    - No new error types in logs
  Rollback trigger: any criterion missed

Stage 5% → 25%  (early adopters)
  Duration: 2 hours minimum
  Success criteria:
    - Error rate < [baseline + 0.25%]
    - p99 latency within 10% of baseline
    - Zero severity-1 alerts
  Rollback trigger: any criterion missed

Stage 25% → 100% (general availability)
  Duration: proceed when 25% stage stable for 2+ hours
  Success criteria: all above criteria maintained
  Rollback trigger: error rate spike or latency regression

Rollback command:
  [deployment rollback command — infer from project]
```

## Phase 5 — Launch Checklist Sign-Off

```
Pre-launch sign-off:

  [x] All tests pass
  [x] Build succeeds
  [x] No secrets in diff
  [x] Security scan: [result]
  [x] Health endpoint present
  [x] Error logging in place
  [x] Rollout plan defined
  [x] Rollback command confirmed

Launch status: READY / NOT READY
```

If NOT READY, list each blocking item with the action required to resolve it.

## Edge Cases

- **No staged rollout available** (no feature flags / traffic splitting): note the limitation; recommend a blue-green or canary deployment approach
- **Emergency hotfix** (skip staged rollout): acknowledge the risk, require explicit "ship it" confirmation, set a shorter monitoring window (15 min canary)
- **Monorepo — partial deployment**: scope all checks to the changed service/package only
- **Static site or library release**: skip health endpoint and rollout staging; focus on build, security, and changelog checks
