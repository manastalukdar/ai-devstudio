---
name: issue-triage
description: Discover, deduplicate, prioritize, and label incoming GitHub issues and discussions — produce a structured priority queue with one-line summaries and suggested labels. Designed to run with /loop 2h or on demand.
disable-model-invocation: false
risk: safe
---

# Issue Triage

Keep the issue backlog clean and actionable. Scans open issues, identifies duplicates, extracts priority signals, and produces a structured queue the team (or other loops) can consume.

## Usage

```
/issue-triage                        # triage all open issues
/issue-triage --repo <owner/repo>    # triage a specific repo
/issue-triage --since <date>         # only issues opened since date (ISO 8601)
/issue-triage --label <label>        # filter to a specific label
/issue-triage --report-only          # produce report without applying any labels
```

Run on a loop for continuous triage:
```
/loop 2h /issue-triage
/loop 1d /issue-triage --since yesterday
```

## Behavior

### Step 1 — Load open issues

```bash
# Fetch open issues with metadata
gh issue list --state open --limit 100 \
  --json number,title,body,labels,createdAt,updatedAt,comments,reactions,assignees \
  | jq 'sort_by(.reactions.totalCount) | reverse'
```

If 0 issues → report "No open issues" and exit.

### Step 2 — Deduplicate

For each issue, check for existing duplicates:

```bash
# Search for similar titles (keyword extraction)
KEYWORDS=$(echo "$ISSUE_TITLE" | tr '[:upper:]' '[:lower:]' | grep -oE '\b\w{4,}\b' | head -5 | tr '\n' ' ')
gh issue list --state open --search "$KEYWORDS" --json number,title | head -5
```

If a likely duplicate is found:
- Add `duplicate` label to the newer issue
- Comment with the original issue number
- **Do not close** — human confirms duplicates

### Step 3 — Extract priority signals

For each issue, score priority (1–5) from:

| Signal | Weight | How to detect |
|---|---|---|
| Reactions (👍, ❤️) | High | `reactions.totalCount` |
| Comments count | Medium | `comments` length |
| Age (older = more urgent) | Medium | `createdAt` |
| Bug label present | High | `labels[]` |
| "crash", "data loss", "security" in title | Critical | keyword grep |
| Assignee present | Low (already tracked) | `assignees` |
| Linked PR or "fix:" commit | Reduces priority | search commits |

```bash
# Check for critical keywords
echo "$ISSUE_TITLE $ISSUE_BODY" | grep -iE "crash|data.loss|security|vulnerability|CVE|regression|production|outage" && PRIORITY=1
```

### Step 4 — Suggest labels

Based on issue content, suggest labels:

| Content signal | Suggested label |
|---|---|
| Stack trace / error message | `bug` |
| "would be nice", "could you add" | `enhancement` |
| "docs", "documentation", "typo" | `documentation` |
| First comment from new contributor | `good first issue` |
| No steps to reproduce | `needs-repro` |
| Ambiguous or unclear ask | `needs-clarification` |
| Priority score 1–2 | `priority: high` |

```bash
# Apply suggested labels (unless --report-only)
gh issue edit <number> --add-label "<label>"
```

Only add labels — never remove existing human-assigned labels.

### Step 5 — Produce structured output

```
ISSUE TRIAGE — <repo> (2026-06-30 10:45 UTC)
Open: 23 issues  |  New since last run: 4  |  Needs human: 2

TOP 5 (by priority score)

  #487  [BUG] Crash on export with files > 100MB               P1  7👍  3 comments
        Labels: bug, needs-repro | Suggested: priority:high
        Action: Request reproduction steps (no steps provided)

  #412  [FEAT] Dark mode support                                P2  24👍 12 comments
        Labels: enhancement | Suggested: add to roadmap discussion
        Action: None — actively discussed

  #501  Security: SSRF via webhook URL parameter               P1  1👍  0 comments
        Labels: (none) | Suggested: bug, security, priority:high
        Action: Label applied; escalate to security review

DUPLICATES FOUND (1)
  #499 is likely a duplicate of #412 (dark mode) — duplicate label added

NEEDS HUMAN (2)
  #489  Ambiguous feature request — unclear acceptance criteria
  #493  Potential duplicate of #234 but different enough to confirm manually

NOISE / IGNORED (5)
  #480–#484  Dependabot alerts (handled by dep-sweep)

State written to: .claude/cache/issue-triage/state.json
```

### Step 6 — Update state

```bash
mkdir -p .claude/cache/issue-triage
jq -n \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg open "$OPEN_COUNT" \
  --arg new "$NEW_COUNT" \
  '{last_run: $ts, open_count: $open, new_since_last_run: $new}' \
  > .claude/cache/issue-triage/state.json
```

## Edge Cases

- **No GitHub auth**: Report the error; suggest `gh auth login`.
- **Large backlog (100+ issues)**: Process in batches of 50; note total count in report.
- **Private repo**: Works the same; `gh` handles auth.
- **No labels configured in repo**: Skip label suggestions; only produce priority report.
- **Issue already has `blocked` or `wontfix`**: Skip — do not re-triage human decisions.

## Token Optimization

**Expected range**: 400–1,200 tokens; 50–100 tokens (no issues, early exit)

**Patterns used**: Bash (gh CLI), early exit (0 issues), progressive disclosure (summary then top-5 then full list on request), caching (state avoids re-reading unchanged issues)

**Caching**: Stores last-run timestamp and issue count in `.claude/cache/issue-triage/state.json`. On resume, reads only issues updated since `last_run`.

**Early exit**: 0 open issues → single-line report and exit.
