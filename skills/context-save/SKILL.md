---
name: context-save
description: Save current work-in-progress context as a git WIP commit — captures all staged and unstaged changes with a timestamped stash message so you can switch contexts safely and restore later. Inspired by gstack's context-save skill.
disable-model-invocation: true
---

# Context Save

I'll snapshot your current work-in-progress into a named git WIP commit so you can switch tasks safely and pick up exactly where you left off. Inspired by gstack's context-save skill.

## Token Optimization

**Expected range**: 100–250 tokens

**Patterns used**: Bash git commands, early exit (clean working tree)

**Early exit**: If the working tree is already clean, report it and stop.

## Usage

```bash
/context-save                        # auto-name from branch and timestamp
/context-save "halfway through auth"  # descriptive label
```

## Step 1 — Check Working Tree

```bash
# Verify there is something to save
if git diff --quiet && git diff --cached --quiet; then
    echo "✓ Working tree is clean — nothing to save"
    exit 0
fi

# Show what will be saved
echo "Changes to save:"
git status --short
git stash list | head -3
```

## Step 2 — Stage Everything

```bash
# Stage all changes (tracked and untracked) for the WIP commit
git add -A

# Verify staging
git diff --cached --stat
```

## Step 3 — Create WIP Commit

```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
LABEL="${1:-WIP}"

git commit -m "wip: ${LABEL} [${BRANCH}] ${TIMESTAMP}"
```

The commit message format: `wip: <label> [<branch>] <timestamp>`

Example: `wip: halfway through auth [feature/oauth] 2026-04-27 14:32`

## Step 4 — Confirm Save

```
Context saved — wip: halfway through auth [feature/oauth] 2026-04-27 14:32

  3 files staged, 127 additions, 34 deletions

To restore: /context-restore
To see all WIP saves: git log --oneline | grep "^wip:"
```

## Step 5 — Record in Session State (Optional)

If a `.claude/sessions/` directory exists, append a note to the active session:

```bash
if ls .claude/sessions/*.json 2>/dev/null | head -1 | grep -q json; then
    ACTIVE=$(ls -t .claude/sessions/*.json | head -1)
    # Append WIP save event to session
fi
```

## Edge Cases

- **Untracked binary files**: `git add -A` includes them; note large files in the confirmation
- **Already on a WIP commit**: warn "The current HEAD is already a WIP commit — save anyway? [y/N]"
- **Merge conflict state**: do not save during active merge; tell user to resolve conflicts first
- **Detached HEAD**: warn that the WIP commit will be orphaned; suggest creating a branch first
- **Submodules**: `git add -A` does not recurse into submodules; note if any are dirty

## Restore

Use `/context-restore` to undo the WIP commit and restore all changes to the working tree.

## Safety

This skill creates a git commit — it does **not** modify history. The WIP commit can always be undone with `git reset HEAD~1 --mixed` (restores files to working tree) or `git reset HEAD~1 --hard` (discards changes — use carefully).
