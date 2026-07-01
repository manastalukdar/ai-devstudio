---
name: minimal-fix
description: Produce the smallest possible code change that fixes one specific, well-scoped issue — CI failure, reviewer comment, or bug report. Never touches unrelated code and respects a safety denylist.
disable-model-invocation: false
risk: safe
---

# Minimal Fix

Fix **one specific problem** with the **smallest diff that could work**. No drive-by refactors. No improvements beyond the stated target.

## Usage

```
/minimal-fix "<exact failure message or reviewer comment>"
/minimal-fix --file <path> "<issue>"   # hint the implicated file
/minimal-fix --dry-run "<issue>"       # show proposed diff without applying
```

## Behavior

### Step 1 — Confirm scope

Parse `$ARGUMENTS` for the exact failure. If ambiguous (multiple failures described), stop and ask which one to address. One problem per invocation — multiple failures should go through `/triage` first.

### Step 2 — Check the denylist

Never auto-edit files matching these patterns — escalate with context instead:

```
.env  .env.*  **/*secret*  **/*credential*  **/*_key*
auth/**  authentication/**  payments/**  billing/**
**/migrations/**  .terraform/**  k8s/production/**
```

```bash
# Detect if implicated file is on denylist
echo "$TARGET_FILE" | grep -Ei "\.env|secret|credential|_key|/auth/|/payment|/billing/|/migration|terraform|k8s/prod"
```

If matched → output escalation notice and stop.

### Step 3 — Locate the root cause

```bash
# For CI failures: find the failing line from the error message
grep -rn "<error substring>" --include="*.ts" --include="*.py" --include="*.js" . | head -10

# For reviewer comments: find the referenced code
git diff origin/main...HEAD -- . | grep -A5 -B5 "<comment keyword>"

# Focus on the exact file and line, not symptoms in distant files
```

Read **only** the implicated file(s). Do not read the full codebase.

### Step 4 — Confirm the minimal root cause

Identify the specific line(s) causing the failure. Write out:

```
Target: <file>:<line>
Root cause: <one sentence>
Proposed change: <what changes, what stays the same>
```

If the root cause spans more than 3 files → escalate. This is not a minimal fix scenario.

### Step 5 — Apply the fix

Change only what is required. Rules:
- No reformatting of untouched lines
- No variable renames beyond the fix
- No import additions beyond what the fix requires
- No test additions (unless the fix itself requires one to be non-broken)

### Step 6 — Verify

```bash
# Run only the tests relevant to the changed file
# For Node/TS:
npx jest <changed-file-pattern> --passWithNoTests 2>&1 | tail -20

# For Python:
python -m pytest <changed-file-path> -x -q 2>&1 | tail -20

# For Go:
go test ./$(dirname <changed-file>) 2>&1 | tail -20
```

### Step 7 — Report

```
MINIMAL FIX PROPOSAL

Target:    src/auth/token.ts:88
Problem:   refresh_token check uses == instead of === causing type coercion bypass
Change:    Line 88: == → ===  (1 line, 1 character)
Verified:  npm test src/auth -- 12 passed, 0 failed

Risk:      Low — single character change in equality check
Human review needed?  No — straightforward equality fix with passing tests

Files changed: 1  |  Lines changed: 1  |  Tests run: 12
```

## Edge Cases

- **Cannot reproduce locally**: Report what you found + ask the user to run verification.
- **Fix requires touching a denylist file**: Escalate with full context; never edit the file.
- **Root cause is architectural** (fix would span many files): Say so explicitly and suggest `/refactor` or `/incident-response` instead.
- **Flaky test**: Classify as flaky, do not code-fix — suggest quarantine and note in report.

## Token Optimization

**Expected range**: 300–800 tokens; 50–100 tokens (denylist hit, early exit)

**Patterns used**: Grep-before-Read (locate the exact line before reading the file), early exit (denylist check before any analysis), git diff scope (look at changed files first)

**Early exit**: Denylist match → exit immediately (saves ~700 tokens). Multiple failures in `$ARGUMENTS` → ask for one before proceeding.
