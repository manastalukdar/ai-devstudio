---
name: ui-polish
description: Final pre-ship UI quality pass — reads the persisted critique snapshot as a prioritized backlog and implements fixes from P0 down
disable-model-invocation: false
risk: safe
---

# UI Polish

I'll work through the persisted critique backlog from `/ui-critique`, fixing issues in priority order (P0 → P1 → P2) and confirming each fix before moving on.

## Purpose

Convert critique findings into shipped fixes without losing track of which issues remain. Designed to run after `/ui-critique` has produced a snapshot.

## Usage

- `/ui-polish` — fix changed UI files using the most recent critique snapshot
- `/ui-polish [file]` — fix a specific file using the snapshot
- `/ui-polish --p0` — fix only blockers
- `/ui-polish --dry-run` — list planned fixes without applying them

## Behavior

### Step 1 — Load critique snapshot

```bash
# Find most recent snapshot
ls -t .claude/cache/ui-critique/*.md 2>/dev/null | head -1
```

If no snapshot found: "No critique snapshot found. Run `/ui-critique` first, or proceed with general polish heuristics? [y/n]"

If snapshot found, read it and extract open issues by priority.

### Step 2 — Scope check

```bash
# Which files in the snapshot are in the current diff? (prefer those)
git diff --name-only HEAD -- '*.tsx' '*.jsx' '*.html' '*.css' '*.vue' '*.svelte'
```

Prioritize fixing issues in changed files. Flag snapshot issues in unchanged files as "deferred — not in current diff."

### Step 3 — Fix in priority order

For each P0 issue:
1. Read the affected file
2. Describe the planned fix in one sentence
3. Apply the fix
4. Confirm: "Fixed [P0] issue in file:line. Continue to next? [y to proceed / n to stop]"

For P1 issues: batch-describe all planned P1 fixes, ask for confirmation, then apply.

For P2 issues: list them and ask "Apply all P2 polish fixes? [y/n/select]"

### Step 4 — Update snapshot

After fixes are applied, update the snapshot to mark resolved issues and report remaining open items.

```bash
# Append resolution summary to snapshot
echo "\n## Resolved $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> .claude/cache/ui-critique/<snapshot-file>
```

Report: "Polish pass complete. P0: N fixed, P1: N fixed, P2: N fixed. N issues remain."

## Examples

```
/ui-polish
→ loads snapshot → fixes P0 blockers → confirms before P1 → lists P2

/ui-polish --p0
→ fixes only accessibility failures and broken layouts, stops

/ui-polish --dry-run
→ lists all planned fixes without touching files
```

## Token Optimization

**Expected range**: 500–2,000 tokens (depends on snapshot size and files changed)

**Early exit**: No snapshot and user declines general polish → stop immediately.

**Patterns used**: git diff scope default, progressive disclosure (P0 first), early exit on no-snapshot

**Cache**: Reads `.claude/cache/ui-critique/`; updates snapshot in place.

## Edge Cases

- Snapshot references deleted files: skip with a note
- Fix for one issue conflicts with another: surface the conflict and ask which to prioritize
- `--p0` flag with no P0 issues: report "No P0 blockers found in snapshot"

## Safety

Reads source files before editing. Creates a git checkpoint before applying P0 fixes:

```bash
git add -A && git stash push -m "checkpoint before ui-polish"
```

Confirm with user before applying any batch of changes.
