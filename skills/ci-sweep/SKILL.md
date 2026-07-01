---
name: ci-sweep
description: React to CI failures on main or active branches — diagnose the failure type, propose a minimal fix for regressions, re-run flakes, and escalate infrastructure failures. Designed to run with /loop 15m.
disable-model-invocation: false
risk: safe
---

# CI Sweep

Reduce the time main stays red. Monitors CI, classifies each failure, and takes the smallest safe action — or escalates when human judgment is needed.

## Usage

```
/ci-sweep                         # check CI status on current branch
/ci-sweep --branch main           # sweep a specific branch
/ci-sweep --run <run-id>          # analyze a specific workflow run
/ci-sweep --report-only           # diagnose but do not apply any fix
```

Run on a loop for continuous reaction:
```
/loop 15m /ci-sweep --branch main
/loop 5m /ci-sweep              # during active development
```

## Behavior

### Step 1 — Check CI status

```bash
# Get recent runs on the target branch
BRANCH="${ARGUMENTS#*--branch }"
BRANCH="${BRANCH:-$(git branch --show-current)}"

gh run list --branch "$BRANCH" --limit 5 \
  --json databaseId,name,status,conclusion,createdAt,headSha \
  --jq '.[] | select(.status == "completed" and .conclusion != "success")'
```

If all runs are passing → report "CI green" and exit immediately.

### Step 2 — Get failure details

```bash
# Fetch logs for the failing job
gh run view <run-id> --log-failed 2>/dev/null | tail -100

# Identify the failing step
gh run view <run-id> --json jobs --jq '.jobs[] | select(.conclusion == "failure") | {name, steps: [.steps[] | select(.conclusion == "failure")]}'
```

### Step 3 — Classify the failure

| Type | Signals | Action |
|---|---|---|
| **Regression** | New failure on a line changed in recent commits | → Step 4: minimal-fix |
| **Flake** | Intermittent — passed in previous identical run | → Step 5: re-run |
| **Env/infra** | Missing secret, runner OOM, network timeout, Docker pull fail | → Escalate immediately |
| **Config** | YAML syntax error, missing workflow file, bad matrix | → Step 6: config fix |
| **Pre-existing** | Failure predates the current branch's commits | → Note and skip |

```bash
# Check if failure existed before recent commits
git log --oneline -10
gh run list --branch main --limit 20 --json conclusion,createdAt | \
  jq '[.[] | select(.conclusion != null)] | group_by(.conclusion) | .[] | {conclusion: .[0].conclusion, count: length}'
```

### Step 4 — Regression: propose minimal fix

Identify the exact failing line from the error output:

```bash
# Extract file and line from test failure
echo "$FAILURE_LOG" | grep -E "FAIL|Error|assert|expected" | head -20

# Find which recent commit touched that file
git log --oneline --since="2 days ago" -- <implicated-file> | head -5
```

Propose a fix using the minimal-fix pattern (one problem, smallest diff, denylist respected). Cap at **3 attempts** per failing job:

```bash
# Track attempt count
ATTEMPTS_FILE=".claude/cache/ci-sweep/attempts.json"
CURRENT=$(jq -r --arg job "$JOB_NAME" '.[$job] // 0' "$ATTEMPTS_FILE" 2>/dev/null || echo 0)

if [ "$CURRENT" -ge 3 ]; then
  echo "ESCALATE: 3 fix attempts exhausted for $JOB_NAME"
  exit 0
fi
```

After applying fix → invoke `/loop-verify` before staging. Do not mark the fix done yourself.

### Step 5 — Flake: re-run

```bash
gh run rerun <run-id> --failed
```

Record the re-run in state. If the same job flakes 3 times in 24h → flag for quarantine:

```
FLAKE DETECTED: <test-name> has failed intermittently 3× in 24h
Suggested action: quarantine this test and open a tracking issue
Do not code-fix a flake — address the non-determinism.
```

### Step 6 — Config fix

For YAML syntax errors or missing fields, read only the workflow file and apply the minimal correction:

```bash
# Validate workflow YAML
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/<file>.yml'))" 2>&1
```

Config files are not on the denylist; apply minimal fix and note it.

### Step 7 — Report

```
CI SWEEP — main @ abc1234 (2026-06-30 10:45 UTC)

Failing jobs (2)
  test-auth     REGRESSION  → minimal-fix proposed (attempt 1/3)
                            Error: AssertionError in test_refresh_token_expiry:88
                            Implicated commit: a1b2c3d "fix(auth): update token expiry logic"

  build-docker  FLAKE       → re-run triggered (2nd flake this run)

Escalated (1)
  deploy-staging ENV_FAIL   → GITHUB_TOKEN missing in workflow env; human action needed

Previously green: lint, type-check, unit-tests
```

## Edge Cases

- **All jobs passing**: "CI green on `<branch>`" — exit immediately.
- **No CI configured**: Report "No CI runs found for this branch" and exit.
- **Private repo without gh auth**: Surface the auth error; do not guess.
- **Main is perpetually red**: After 3 sweep attempts with no improvement, escalate with full timeline.

## Token Optimization

**Expected range**: 400–1,200 tokens per sweep; 50–100 tokens (CI green, early exit)

**Patterns used**: Bash (gh CLI), early exit (all-green), progressive disclosure (summary then per-job detail), attempt cap (3 fix attempts max)

**Caching**: Stores per-job attempt counts and flake history in `.claude/cache/ci-sweep/` (reset on successful run).

**Early exit**: All runs passing → single-line report and exit (saves ~1,000 tokens).
