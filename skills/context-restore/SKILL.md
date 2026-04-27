---
name: context-restore
description: Restore work-in-progress context saved by /context-save — finds the most recent WIP commit on the current branch and unpacks it back to the working tree so you can resume exactly where you left off. Inspired by gstack's context-restore skill.
disable-model-invocation: true
---

# Context Restore

I'll find the most recent WIP commit on this branch and unpack it back to your working tree so you can resume right where you left off. Inspired by gstack's context-restore skill.

## Token Optimization

**Expected range**: 100–250 tokens

**Patterns used**: Bash git commands, early exit (no WIP commit found)

**Early exit**: If no WIP commit exists on the current branch, report clearly and stop.

## Usage

```bash
/context-restore                  # restore most recent WIP on current branch
/context-restore --list           # show all WIP commits across all branches
/context-restore --pick           # choose from a list of WIP commits
```

## Step 1 — Find WIP Commits

```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Find the most recent WIP commit on this branch
WIP_SHA=$(git log --oneline | grep "^[a-f0-9]* wip:" | head -1 | cut -d' ' -f1)

if [ -z "$WIP_SHA" ]; then
    echo "No WIP commits found on branch: $BRANCH"
    echo ""
    echo "All WIP commits across all branches:"
    git log --all --oneline | grep "wip:" | head -10
    exit 0
fi

# Show what will be restored
WIP_MSG=$(git log --oneline -1 "$WIP_SHA")
echo "Found WIP commit: $WIP_MSG"
```

## Step 2 — Check Working Tree Safety

```bash
# Warn if current working tree has unsaved changes
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "⚠ Warning: You have uncommitted changes that will be overwritten."
    echo ""
    git status --short
    echo ""
    echo "Save them first? Run /context-save to preserve them."
    echo "Continue anyway? [y/N]"
    # Wait for confirmation
fi
```

## Step 3 — Restore the WIP Commit

```bash
# Unpack the WIP commit back to the working tree (mixed reset — keeps files)
git reset HEAD~1 --mixed

echo "✓ Context restored"
echo ""
git status --short
```

`--mixed` reset:
- Moves HEAD back one commit (removes the WIP commit from history)
- Leaves all changes in the working tree (unstaged)
- Staged files from the original `context-save` become unstaged

## Step 4 — Confirm Restoration

```
Context restored — wip: halfway through auth [feature/oauth] 2026-04-27 14:32

  3 files restored to working tree:
    M  src/auth/oauth.ts
    M  src/auth/session.ts
    A  src/auth/providers/github.ts

Resume where you left off. Use /context-save when switching again.
```

## --list Mode

```bash
# Show all WIP commits across all branches
git log --all --oneline --decorate | grep "wip:" | head -20
```

Output format:
```
abc1234 (feature/oauth) wip: halfway through auth [feature/oauth] 2026-04-27 14:32
def5678 (feature/billing) wip: stripe integration [feature/billing] 2026-04-26 09:15
```

## --pick Mode

Show the list and prompt for selection:

```
WIP commits available:
  [1] abc1234 — halfway through auth (feature/oauth, 2026-04-27 14:32)
  [2] def5678 — stripe integration (feature/billing, 2026-04-26 09:15)

Select a WIP commit to restore [1]:
```

After selection, switch to the relevant branch if needed, then restore.

## Edge Cases

- **WIP commit not at HEAD**: if HEAD is not the WIP commit (other commits were added after), warn and show the distance; offer to cherry-pick the diff instead
- **Conflicts on restore**: if the working tree changes conflict with the WIP commit, show the conflict and guide resolution
- **Multiple WIP commits stacked**: detect consecutive `wip:` commits and warn before restoring only the top one
- **Wrong branch**: if the WIP commit is for a different branch, warn and ask before switching branches
- **Detached HEAD**: if HEAD is detached, suggest creating a branch before restoring

## Paired Skill

Use `/context-save` to save your current work before switching tasks. `/context-restore` is always the inverse operation.
