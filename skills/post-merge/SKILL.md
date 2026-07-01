---
name: post-merge
description: Sweep for follow-up work after recent merges — TODOs added in merged PRs, stale feature flags, dead code, documentation gaps, and tech-debt tickets left by merge comments.
disable-model-invocation: false
risk: safe
---

# Post-Merge Cleanup

Catch the follow-up work that gets left behind when a PR merges. Scans recent merges for TODOs, deprecated paths, stale flags, and doc gaps — then surfaces a prioritized cleanup list.

## Usage

```
/post-merge                       # sweep merges from the last 24h
/post-merge --since <date>        # merges since a specific date
/post-merge --pr <number>         # sweep a specific merged PR
/post-merge --report-only         # surface items without opening issues
```

## Behavior

### Step 1 — Find recent merges

```bash
# Get merged PRs in the target window
gh pr list --state merged --limit 20 \
  --json number,title,mergedAt,files,body,headRefName \
  --jq 'sort_by(.mergedAt) | reverse | .[:10]'
```

Or use git log for repos without GitHub:

```bash
git log --merges --since="24 hours ago" --oneline
git log --merges --since="24 hours ago" --format="%H %s" | head -10
```

### Step 2 — Scan for TODOs and follow-ups

```bash
# TODOs added (not removed) in recent merges
git log --merges --since="24 hours ago" --format="%H" | while read sha; do
  git diff "${sha}^" "$sha" | grep "^+.*TODO\|^+.*FIXME\|^+.*HACK\|^+.*XXX" | grep -v "^+++"
done | head -30

# Merge commit messages mentioning follow-up
git log --merges --since="24 hours ago" --format="%s %b" | \
  grep -i "follow.up\|tech.debt\|cleanup\|todo\|later\|next.pr\|separate.ticket" | head -10
```

### Step 3 — Detect stale feature flags

```bash
# Find flags that were activated in the merge and may need cleanup
git log --merges --since="24 hours ago" --format="%H" | while read sha; do
  git diff "${sha}^" "$sha" | grep -E "^\+.*(feature_flag|featureFlag|FEATURE_|isEnabled|FLAG_)" | grep -v "^+++"
done | head -20

# Find flags that may have been permanently enabled (defaulted to true)
grep -rn "feature_flag\|featureFlag\|FEATURE_" --include="*.ts" --include="*.py" --include="*.js" . | \
  grep -i "= true\|= True\|: true" | head -10
```

### Step 4 — Check for dead code introduced

```bash
# Functions or classes added in the merge that are never called
git log --merges --since="24 hours ago" --format="%H" | while read sha; do
  git diff "${sha}^" "$sha" --name-only
done | sort -u | while read file; do
  # Check for exported symbols with no import elsewhere
  grep -n "^export function\|^export class\|^def \|^class " "$file" 2>/dev/null | head -5
done
```

### Step 5 — Identify documentation gaps

```bash
# New public API surface added without doc update
git log --merges --since="24 hours ago" --format="%H" | while read sha; do
  git diff "${sha}^" "$sha" | grep -E "^\+.*(export function|export class|def |public )" | \
    grep -v "test\|spec\|__" | grep -v "^+++"
done | head -20

# Check if corresponding docs were updated in the same merge
git log --merges --since="24 hours ago" --format="%H" | while read sha; do
  HAS_CODE=$(git diff "${sha}^" "$sha" --name-only | grep -v "\.md$" | wc -l)
  HAS_DOCS=$(git diff "${sha}^" "$sha" --name-only | grep "\.md$" | wc -l)
  [ "$HAS_CODE" -gt 0 ] && [ "$HAS_DOCS" -eq 0 ] && git log -1 --format="%s" "$sha"
done
```

### Step 6 — Score and prioritize cleanup items

For each item found, assign:
- **Risk if ignored**: High (flag blocks release, dead code causes confusion) / Medium / Low
- **Effort**: Small (< 1h) / Medium (1–4h) / Large (> 4h)
- **Suggested action**: fix-it-now / open-issue / defer

### Step 7 — Report and optionally open issues

```
POST-MERGE CLEANUP — since 2026-06-29 (3 merges scanned)

TODOs Added (3)
  src/payments/processor.ts:142   TODO: Remove legacy retry path after v2 rollout
    Risk: Medium | Effort: Small | → open issue (link to PR #1245)
  src/auth/token.ts:88            FIXME: Hardcoded 30s timeout, make configurable
    Risk: Low | Effort: Small | → open issue
  src/api/routes.ts:23            HACK: Temporary workaround for rate limit bug
    Risk: High | Effort: Medium | → open issue + priority:high label

Feature Flags (1)
  src/features/search-v2.ts       FEATURE_SEARCH_V2 now hardcoded true — remove old path?
    Risk: Low | Effort: Medium | → suggest cleanup after 2 sprint soak

Documentation Gaps (2)
  PR #1243 added 3 new API endpoints with no doc update
    Suggested: update docs/api/ for GET /v2/search, POST /v2/index, DELETE /v2/cache
  PR #1241 changed auth flow — README.md authentication section is now stale

No dead code detected in recent merges.

Issues to open (if approved): 3  |  Defer: 2
Run with --create-issues to open GitHub issues for approved items.
```

### Step 8 — Optionally create issues

```bash
# With --create-issues flag, open GitHub issues for High/Medium items
gh issue create \
  --title "cleanup: Remove legacy retry path in payments/processor.ts (from PR #1245)" \
  --body "TODO added in PR #1245 at src/payments/processor.ts:142. Remove after v2 rollout is stable." \
  --label "tech-debt,cleanup"
```

## Edge Cases

- **No recent merges**: "No merges in the last 24h" — exit cleanly.
- **Non-GitHub repo**: Use `git log --merges` only; skip PR-specific steps.
- **Large diff**: Process first 50 changed files; note if truncated.
- **TODOs that were removed** (not added): Do not flag — that's already done cleanup work.

## Token Optimization

**Expected range**: 400–1,200 tokens; 50–100 tokens (no recent merges, early exit)

**Patterns used**: Bash (git log, gh CLI, grep), git diff scope (recent merges only), early exit (no merges), progressive disclosure (count summary → item list → issue creation on request)

**Early exit**: No merges in the target window → single-line report and exit.
