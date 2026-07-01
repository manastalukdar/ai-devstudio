---
name: loop-design
description: Pre-flight readiness checklist for a new loop before enabling unattended execution — verifies maker/checker split, state file, budget caps, denylist, kill switch, attempt cap, and human escalation paths
disable-model-invocation: false
risk: none
---

# Loop Design Checklist

Score a loop design before enabling it for unattended runs. A loop missing key safety controls is not production-ready — this skill helps you find what's missing before it causes problems.

## Usage

```
/loop-design "<loop name or description>"   # score a loop you're about to enable
/loop-design --pattern <name>               # check a named pattern (pr-babysitter, ci-sweep, etc.)
/loop-design --audit                        # audit all currently configured loops
```

## Behavior

### Step 1 — Establish the loop under review

If `$ARGUMENTS` names a pattern (pr-babysitter, ci-sweep, dep-sweep, issue-triage, post-merge, daily-triage), load its known structure. Otherwise, ask:

1. What does this loop do? (one sentence)
2. What is the cadence? (every N minutes/hours/days)
3. What actions can it take? (report-only / propose fix / apply fix / open PR / merge)
4. What external systems does it touch? (GitHub, Linear, Slack, database, etc.)

### Step 2 — Score against the readiness checklist

Work through each section and mark PASS / FAIL / MISSING:

**Purpose & Scope**
- [ ] Single clear goal (one sentence)
- [ ] Explicit non-goals documented
- [ ] Target scope defined (which repos, branches, labels, or queues)
- [ ] Phase rollout planned (report-only first, then act)

**Scheduling**
- [ ] Cadence chosen and justified (urgency matches interval)
- [ ] Off-hours behavior defined (pause, slow down, or continue)
- [ ] Self-cleanup on empty watchlist (no pointless runs)

**Maker / Checker Split**
- [ ] Implementer and verifier are **separate** agents or models
- [ ] Implementer cannot mark its own work "done"
- [ ] Verifier runs tests independently before approving
- [ ] If no verifier: loop is report-only or escalates all actions to human

**State / Memory**
- [ ] State file or board schema defined
- [ ] Loop reads prior state at start of every run
- [ ] Loop writes outcomes and timestamps at end of every run
- [ ] Resolved/closed items are pruned on each run
- [ ] Human overrides are recorded in state

**Human Escalation**
- [ ] Attempt cap defined (e.g. max 3 fix attempts per issue)
- [ ] Escalation triggers explicit (cap exhausted, high-risk path, ambiguity)
- [ ] Denylist paths configured (auth, payments, secrets, infra)
- [ ] Notification channel defined (where does escalation land?)

**Cost & Safety**
- [ ] Token budget estimated per run
- [ ] Daily cap defined in `loop-budget.md` or equivalent
- [ ] Kill switch documented (label, flag, or `loop-pause-all`)
- [ ] Run log configured (`loop-run-log.md` or equivalent)

**Connectors (if any)**
- [ ] Minimum permissions for each connector (read vs write)
- [ ] Bot identity clear on any auto-posted comments/PRs
- [ ] Write-scope connectors require verifier or human gate

### Step 3 — Calculate readiness score

| Section | Max points | Scoring |
|---|---|---|
| Purpose & Scope | 20 | 5 per item |
| Scheduling | 15 | 5 per item |
| Maker/Checker Split | 25 | pass/fail per item |
| State / Memory | 25 | 5 per item |
| Human Escalation | 20 | 5 per item |
| Cost & Safety | 20 | 5 per item |
| Connectors | 15 | conditional |

**Readiness levels:**
- **L1 (≥ 60)**: Safe for report-only runs
- **L2 (≥ 80)**: Safe for supervised fix-proposal runs
- **L3 (≥ 95)**: Safe for unattended fix-apply runs

### Step 4 — Surface critical blockers

Flag any FAIL in these items as blockers regardless of score:

- **No kill switch** → loop can run indefinitely, no way to stop quickly
- **No attempt cap** → infinite fix loops and token burn possible
- **Same agent implements and verifies** → confirmation bias, weak tests get approved
- **Denylist not configured** → loop may touch auth/payments/secrets
- **No state file** → loop acts on stale or ghost items from prior runs

### Step 5 — Output report

```
LOOP DESIGN REVIEW — PR Babysitter

Readiness Score: 78/100 → L2 (supervised fix-proposal)

PASS (15/20 items)

BLOCKERS (fix before enabling)
  ✗ No attempt cap — CI fix loop could run forever on a hard regression
    Fix: set max_attempts = 3 per PR in state file

GAPS (improve before L3)
  ✗ No run log — token spend is invisible
    Fix: append JSON entry to loop-run-log.md after each sweep
  ✗ Verifier not configured — fixes are self-approved
    Fix: invoke /loop-verify after each /minimal-fix attempt

RECOMMENDATIONS
  → Start in report-only mode (--dry-run) for 3 days
  → Review STATE.md after first week; prune ghost items
  → Add loop-budget.md with daily cap before enabling L2 actions

Suggested first command:
  /loop 10m /pr-babysitter --dry-run
```

## Anti-Patterns Flagged

The checklist specifically surfaces these known failure modes:

| Anti-pattern | Detected when |
|---|---|
| Self-verification | Same skill listed as both implementer and verifier |
| No attempt cap | No max_attempts field in state schema |
| Vague triage output | No structured output format defined |
| L3 before L1 quality | Actions enabled before report-only phase completed |
| MCP with broad write scope | Connector has merge/delete/post permissions from day one |
| No kill switch | No label, flag, or `loop-pause-all` mechanism defined |
| Shared state without schema | Multiple loops writing same STATE.md without section ownership |

## Edge Cases

- **Pattern name not recognized**: Ask for the loop description and score from scratch.
- **Existing loop audit (`--audit`)**: Find all configured loops by scanning LOOP.md, `.github/workflows/`, and session schedules, then score each.
- **Score exactly at a tier boundary**: Recommend the lower tier until blockers are resolved.

## Token Optimization

**Expected range**: 300–800 tokens

**Patterns used**: Progressive disclosure (score first, blockers second, full checklist on request), early exit (if loop is report-only with no actions, many safety checks are N/A)

**No caching needed**: Each loop design is unique; scores are not reusable across sessions.
