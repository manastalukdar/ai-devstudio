---
name: incident-response
description: Structured production incident workflow — gather symptoms, run diagnostics, correlate recent deploys, draft a timeline and incident report
disable-model-invocation: false
risk: safe
---

# Incident Response

Run a structured triage when something is broken in production. Collects symptoms, correlates recent changes, generates diagnostic commands, and drafts an incident report.

## Usage

```
/incident-response                         # start a new incident triage
/incident-response "<symptom description>" # start with known symptom
/incident-response report                  # draft final incident report from current session
```

## Behavior

### Step 1 — Establish severity and scope

Ask (or infer from `$ARGUMENTS`):

1. What is broken? (service / endpoint / feature)
2. Who is affected? (all users / subset / internal only)
3. Since when? (approximate start time)
4. Is it complete outage or degraded performance?

Assign severity:
- **SEV1**: Complete outage or data loss risk
- **SEV2**: Major feature broken, workaround unavailable
- **SEV3**: Degraded performance or minor feature broken

### Step 2 — Correlate recent changes

```bash
# Last 20 commits across the affected timeframe
git log --oneline --since="6 hours ago"

# Recently modified config or infra files
git diff HEAD~5..HEAD --name-only | grep -E "\.env|config|deploy|k8s|helm|terraform"

# Any dependency bumps
git diff HEAD~5..HEAD -- package.json package-lock.json requirements.txt go.mod
```

Flag any commit touching the affected service within the incident window.

### Step 3 — Generate diagnostic commands

Based on the symptom, output a runbook of commands to execute:

**For HTTP errors (4xx/5xx spike):**
```bash
# Tail application logs for error patterns
grep -i "error\|exception\|fatal" app.log | tail -50

# Check error rate by endpoint
grep "HTTP/1.1\" [45][0-9][0-9]" access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -20
```

**For latency spike:**
```bash
# Find slow requests
grep -E "took [0-9]{4,}ms|duration=[0-9]{4,}" app.log | tail -20

# Check DB slow query log
grep "slow query" /var/log/mysql/slow.log 2>/dev/null | tail -20
```

**For memory / CPU:**
```bash
ps aux --sort=-%mem | head -10
free -h
df -h
```

**For dependency outage:**
```bash
# Test external health endpoints
curl -s -o /dev/null -w "%{http_code}" https://status.stripe.com/api/v2/status.json
```

### Step 4 — Identify blast radius

Check which other services or features share the affected component:

```bash
# Which files import the affected module?
grep -rn "from.*<affected-module>\|require.*<affected-module>" --include="*.ts" --include="*.py" -l .
```

### Step 5 — Propose immediate mitigations

For each confirmed root cause, offer the minimum safe mitigation:

- **Recent bad deploy**: rollback command (`git revert <sha>`, feature flag off)
- **Dependency outage**: enable fallback, disable non-critical feature
- **Config change**: revert specific key
- **Traffic spike**: rate-limit endpoint, scale horizontally

### Step 6 — Draft incident report

```markdown
## Incident Report — [TITLE]

**Severity**: SEV[1/2/3]
**Start**: [timestamp]
**End / Ongoing**: [timestamp or ONGOING]
**Affected**: [service/feature/users]

### Timeline
- HH:MM — Symptom first observed
- HH:MM — Alert fired / team notified
- HH:MM — Root cause identified
- HH:MM — Mitigation applied
- HH:MM — Service restored

### Root Cause
[What broke, why it broke]

### Impact
[Users affected, error rate, duration]

### Mitigation
[What was done to restore service]

### Follow-up Actions
- [ ] Long-term fix (link to issue)
- [ ] Add monitoring / alerting for [metric]
- [ ] Add resilience control for [dependency]
- [ ] Update runbook for [scenario]
```

## Edge Cases

- **No git history**: Skip Step 2 and note it; continue with diagnostics.
- **No access to logs**: List diagnostic commands for the operator to run; generate report from provided output.
- **Ongoing incident**: Focus on mitigation steps first; defer full report to Step 6 until service is restored.

## Token Optimization

**Expected range**: 400–1,200 tokens (triage phase); 300–600 tokens (report-only mode)

**Patterns used**: Bash for system queries (git log, grep), progressive disclosure (diagnostics → root cause → report), early exit (if no symptom provided, ask before proceeding)

**Early exit**: Running `/incident-response report` with no prior triage context prompts for the incident summary before generating the report.
