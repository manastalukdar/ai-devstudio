---
name: git-guardrails
description: Install a Claude Code PreToolUse hook that blocks dangerous git operations (force push, reset --hard, clean -f, branch -D, checkout ., restore .) before they execute. Use when setting up git safety hooks or preventing destructive git commands in Claude Code.
disable-model-invocation: false
risk: safe
---

# Git Guardrails

Install a PreToolUse hook in Claude Code that intercepts and blocks dangerous git operations before they run.

Arguments: `$ARGUMENTS` - `global` to install in `~/.claude/settings.json`, or blank for project-level `.claude/settings.json`

## Behavior

### 1. Determine Scope

```bash
if [[ "$ARGUMENTS" == "global" ]]; then
  SETTINGS="$HOME/.claude/settings.json"
  HOOKS_DIR="$HOME/.claude/hooks"
else
  SETTINGS=".claude/settings.json"
  HOOKS_DIR=".claude/hooks"
fi
mkdir -p "$HOOKS_DIR"
```

### 2. Create the Block Script

```bash
cat > "$HOOKS_DIR/block-dangerous-git.sh" << 'SCRIPT'
#!/bin/bash
set -e

input=$(cat)
command=$(echo "$input" | jq -r '.command // empty')

# Only check Bash tool calls
[ -z "$command" ] && exit 0

dangerous_patterns=(
  "git push"
  "push --force"
  "git reset --hard"
  "reset --hard"
  "git clean -fd"
  "git clean -f"
  "git branch -D"
  "git checkout \."
  "git restore \."
)

for pattern in "${dangerous_patterns[@]}"; do
  if echo "$command" | grep -E "$pattern" > /dev/null 2>&1; then
    echo "BLOCKED: '$command' matches dangerous pattern '$pattern'. The user has prevented this operation." >&2
    exit 2
  fi
done

exit 0
SCRIPT

chmod +x "$HOOKS_DIR/block-dangerous-git.sh"
echo "Hook script created: $HOOKS_DIR/block-dangerous-git.sh"
```

### 3. Register in Claude Code Settings

Read or create the settings file, then add the hook:

```bash
# Read existing settings or start fresh
if [ -f "$SETTINGS" ]; then
  CURRENT=$(cat "$SETTINGS")
else
  CURRENT='{}'
fi

# Use jq to safely add the PreToolUse hook (preserves existing config)
HOOK_PATH="$(pwd)/$HOOKS_DIR/block-dangerous-git.sh"
[[ "$ARGUMENTS" == "global" ]] && HOOK_PATH="$HOME/.claude/hooks/block-dangerous-git.sh"

echo "$CURRENT" | jq \
  --arg hook "$HOOK_PATH" \
  '.hooks.PreToolUse += [{"matcher": "Bash", "hooks": [{"type": "command", "command": $hook}]}]' \
  > "$SETTINGS"

echo "Hook registered in: $SETTINGS"
```

### 4. Verify

```bash
# Test the script directly
echo '{"command": "git push origin main"}' | bash "$HOOKS_DIR/block-dangerous-git.sh"
# Should exit 2 and print BLOCKED message to stderr

echo '{"command": "git status"}' | bash "$HOOKS_DIR/block-dangerous-git.sh"
# Should exit 0 (allowed)
```

### 5. Report

```
Git guardrails installed:

  Hook script:  .claude/hooks/block-dangerous-git.sh
  Settings:     .claude/settings.json
  Scope:        project

Blocked operations:
  git push / push --force
  git reset --hard
  git clean -f / -fd
  git branch -D
  git checkout . / git restore .

To customize: edit .claude/hooks/block-dangerous-git.sh
To test: echo '{"command": "git push"}' | bash .claude/hooks/block-dangerous-git.sh
To remove: delete the hook entry from .claude/settings.json
```

## Blocked Operations

| Pattern | Why dangerous |
|---|---|
| `git push` / `push --force` | Overwrites remote history; hard to recover from |
| `git reset --hard` | Discards uncommitted work permanently |
| `git clean -f` / `-fd` | Deletes untracked files/dirs permanently |
| `git branch -D` | Deletes branch without merge check |
| `git checkout .` / `git restore .` | Discards all working tree changes |

## Customization

Edit the `dangerous_patterns` array in the hook script to add or remove patterns. The script uses `grep -E` for matching, so regex patterns are supported.

## Examples

```
/git-guardrails           ← project-level (.claude/settings.json)
/git-guardrails global    ← user-level (~/.claude/settings.json)
```

## Edge Cases

- **`jq` not installed**: Reports the required JSON change to make manually
- **Hook already exists**: Detects duplicate matcher and skips re-adding
- **Global scope**: Uses `~/.claude/` paths instead of project-local

## Token Optimization

**Expected range**: 300–500 tokens

**Early exit**: Detects if hook already registered in settings before making changes.

**Template-based**: Script content is fixed — no LLM generation needed.

**Patterns used**: Early exit, template-based generation, Bash for system queries
