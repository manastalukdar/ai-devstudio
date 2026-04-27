---
name: careful
description: Intercept destructive commands before execution — rm -rf, DROP TABLE, force-push, git reset --hard, and similar irreversible operations. Prompts for confirmation and suggests safer alternatives. Inspired by gstack's careful skill.
disable-model-invocation: false
---

# Careful

I'll catch destructive commands before they run and give you a moment to confirm — or choose a safer path. Inspired by gstack's careful skill.

## Token Optimization

**Expected range**: 100–300 tokens per intercept, 20 tokens (no destructive pattern detected)

**Patterns used**: Grep-based pattern matching, early exit (no match), progressive disclosure (warning → alternatives)

**Early exit**: If no destructive pattern is found in the proposed command, exit immediately without comment.

## When to Use

Invoke before running a command you're unsure about, or configure as a pre-execution hook:

```bash
/careful rm -rf dist/
/careful git push --force
/careful "DROP TABLE users;"
```

Or paste a multi-line script and I'll scan the whole thing.

## Step 1 — Scan for Destructive Patterns

Match the input against known high-risk patterns:

```bash
# Filesystem destruction
rm -rf | rmdir | shred | find.*-delete | find.*-exec rm

# Git irreversible operations
git push --force | git push -f | git reset --hard | git clean -fd | git rebase.*--force
git branch -D | git tag -d | git reflog expire

# Database
DROP TABLE | DROP DATABASE | TRUNCATE | DELETE FROM.*WHERE 1=1 | DELETE FROM.*no WHERE

# Process/infrastructure
kill -9 | pkill -9 | killall
docker rm -f | docker system prune | kubectl delete.*--force
terraform destroy | ansible.*state=absent

# Package/dependency
npm run clean | pip uninstall -y | pip install --force-reinstall
rm.*node_modules | rm.*__pycache__ | rm.*\.venv

# Data overwrite
dd if=.*of= | mkfs | fdisk | parted
truncate -s 0 | > file  (redirect clobber)
```

If no pattern matches: exit silently (the command is not flagged).

## Step 2 — Risk Assessment

Rate the detected operation:

| Level | Color | Description |
|---|---|---|
| CRITICAL | RED | Data loss with no recovery path (DROP TABLE, rm -rf /) |
| HIGH | ORANGE | Data loss recoverable with backups (git reset --hard, force push) |
| MEDIUM | YELLOW | Reversible but annoying to undo (npm clean, docker prune) |

## Step 3 — Warn and Offer Alternatives

```
⚠ CAREFUL — HIGH RISK — git push --force

This will overwrite the remote branch history. Team members with local checkouts
will have diverged histories.

Safer alternatives:
  git push --force-with-lease    ← only force if no one else pushed
  git push --force-if-includes   ← safer still (Git 2.30+)

What's your intent?
  [1] I understand the risk — run it
  [2] Use --force-with-lease instead
  [3] Cancel and explain more
```

Wait for user response before proceeding.

## Step 4 — Alternatives Reference

**File deletion:**
- `rm -rf dist/` → `trash dist/` (recoverable via Trash) or `mv dist/ dist.bak/`
- `find . -name "*.log" -delete` → dry run first: `find . -name "*.log"` without `-delete`

**Git resets:**
- `git reset --hard` → `git stash` first (recoverable), then reset if needed
- `git push --force` → `git push --force-with-lease`
- `git clean -fd` → `git clean -nfd` (dry run preview)

**Database:**
- `DROP TABLE` → rename first: `ALTER TABLE users RENAME TO users_backup_20260427`
- `DELETE FROM` without WHERE → add `LIMIT 1` first to verify filter, then remove limit

**Docker:**
- `docker system prune` → `docker system prune --filter "until=24h"` (only old images)

**Kubernetes:**
- `kubectl delete` → `kubectl get` first to verify target, then delete with explicit name

## Edge Cases

- **Pipeline commands** (`cmd1 && rm -rf`): scan the full pipeline, flag any destructive step
- **Shell scripts**: scan all lines, report all flagged lines with line numbers
- **Aliases**: note that `alias rm='rm -i'` provides interactive prompts by default
- **CI/CD environment**: if `$CI=true` is set, emit a machine-readable warning and exit non-zero rather than prompting
- **Already stashed/committed**: if the working tree is clean before the destructive op, note that recovery is easier

## Safety Note

This skill intercepts at the description layer — it does not actually block shell execution. For enforced guardrails in a CI pipeline, use a pre-commit hook or shell alias.
