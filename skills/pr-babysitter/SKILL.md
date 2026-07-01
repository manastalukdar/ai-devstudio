---
name: pr-babysitter
description: Herd open pull requests through review, CI, and merge — surface aging PRs, trigger minimal-fix on CI failures, nudge for rebases, and escalate blocked ones. Designed to run with /loop 5m.
disable-model-invocation: false
risk: safe
---

# PR Babysitter

Reduce the human time spent herding pull requests. Monitors open PRs, identifies what's blocking each one, and takes the smallest action to unblock — or escalates to a human when judgment is needed.

## Usage

```
/pr-babysitter                    # single sweep of all open PRs
/pr-babysitter --author <handle>  # watch only PRs by a specific author
/pr-babysitter --label <label>    # filter by label (e.g. "ready-for-review")
/pr-babysitter --dry-run          # report actions without taking them
```

Run on a loop for continuous herding:
```
/loop 5m /pr-babysitter
/loop 10m /pr-babysitter --author @me
```

## Behavior

### Step 1 — Discover open PRs

```bash
# List open PRs with key metadata
gh pr list --state open --json number,title,author,createdAt,reviewDecision,statusCheckRollup,isDraft \
  --limit 50 | jq '.[] | select(.isDraft == false)'
```

Skip draft PRs unless `--include-drafts` is passed.

### Step 2 — Triage each PR

For each open PR, classify its blocking state:

| State | Condition | Action |
|---|---|---|
| **CI red** | Any required check failing | → Step 3: Diagnose and minimal-fix |
| **Needs rebase** | Merge conflict or "branch is behind" | → Step 4: Rebase nudge |
| **Awaiting review** | No reviewer assigned or all reviewers haven't responded | → Step 5: Nudge |
| **Changes requested** | Review with requested changes | → Step 6: Surface to author |
| **Approved, not merged** | All checks pass + approved | → Step 7: Merge prompt |
| **Aging** | Open > N days with no activity | → Step 8: Age alert |
| **Blocked** | Explicit "blocked" label or comment | → Escalate, do not touch |

```bash
# Check CI status for a specific PR
gh pr checks <number> --json name,state,conclusion 2>/dev/null

# Check merge status
gh pr view <number> --json mergeable,mergeStateStatus,reviewDecision
```

### Step 3 — CI failure: diagnose and propose fix

```bash
# Get failing check logs
gh run view --log-failed $(gh pr checks <number> --json databaseId --jq '.[0].databaseId') 2>/dev/null | tail -50
```

Classify the failure:
- **Flake**: Same test has failed intermittently on other PRs → re-run the check, note as flake
- **Regression**: New failure introduced by this PR → invoke `/minimal-fix` with the error
- **Env/infra**: Missing secret, broken runner → escalate to human immediately
- **Unrelated**: Failure pre-dates the PR → note and skip (not the PR author's problem)

Cap fix attempts at 3 per PR. After 3 → escalate with full context.

```bash
# Re-run a flaky check
gh run rerun <run-id> --failed
```

### Step 4 — Rebase nudge

If the branch is behind main but has no conflicts, comment with the rebase command:

```bash
gh pr comment <number> --body "Branch is behind main. To update:
\`\`\`
git fetch origin
git rebase origin/main
git push --force-with-lease
\`\`\`"
```

Do not auto-rebase unattended — conflicts require human judgment.

### Step 5 — Review nudge

If no reviewer has been assigned after N hours (default: 24h):

```bash
gh pr edit <number> --add-reviewer <suggested-reviewer>
# or
gh pr comment <number> --body "This PR is awaiting review assignment."
```

Only assign reviewers if the project has a CODEOWNERS file or a known reviewer rotation.

### Step 6 — Changes requested

Surface the blocking review comments to the PR author. Do not attempt to resolve review feedback automatically.

```bash
gh pr view <number> --json reviews --jq '.reviews[] | select(.state == "CHANGES_REQUESTED") | .body'
```

### Step 7 — Approved and ready to merge

```bash
# Confirm all checks pass + required reviews met
gh pr view <number> --json mergeable,reviewDecision,statusCheckRollup
```

If `mergeable == MERGEABLE` and `reviewDecision == APPROVED` → post a merge-ready comment or merge if auto-merge policy allows.

**Default: never auto-merge.** Only merge automatically if `--auto-merge` flag is explicitly passed AND the PR is in the allow list (no denylist files changed).

### Step 8 — Age alert

Flag PRs open longer than the threshold without activity:

```bash
# PRs with no commits, comments, or review activity in N days
gh pr list --state open --json number,title,updatedAt | \
  jq --arg cutoff "$(date -d '7 days ago' -u +%Y-%m-%dT%H:%M:%SZ)" \
  '.[] | select(.updatedAt < $cutoff)'
```

Post a comment asking for status update. Do not close — human decides.

### Step 9 — Run report

Output a summary after each sweep:

```
PR BABYSITTER — sweep complete (2026-06-30 10:45 UTC)

CI Red (2)
  #1241  fix/auth-refresh        → minimal-fix proposed (attempt 1/3)
  #1238  feat/search-v2          → env failure, escalated to human

Awaiting Review (1)
  #1245  docs/api-update         → 26h with no reviewer, reviewer assigned

Aging (1)
  #1230  refactor/legacy-model   → 9 days no activity, comment posted

Approved + Ready (1)
  #1243  fix/typo                → ready to merge (awaiting /pr-babysitter --auto-merge)

Nothing blocking (3): #1240, #1242, #1244
```

## Edge Cases

- **No open PRs**: Report "Nothing to watch" and exit cleanly.
- **No CI configured**: Skip CI checks; focus on review state and aging.
- **Rate limits on gh**: Back off and note in report.
- **PR with `blocked` label**: Skip entirely — do not comment, do not attempt fix.

## Token Optimization

**Expected range**: 400–1,200 tokens per sweep; 50–100 tokens (no open PRs, early exit)

**Patterns used**: Bash for gh CLI queries, progressive disclosure (summary then per-PR detail), early exit (no PRs = immediate exit), attempt cap (max 3 fix attempts per PR)

**Caching**: Stores per-PR attempt counts in `.claude/cache/pr-babysitter/attempts.json` (reset when PR is closed or merged).

**Early exit**: If `gh pr list --state open` returns 0 results → report and exit immediately.
