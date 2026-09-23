---
name: fact-forcing-gate
description: Install a Claude Code PreToolUse hook that blocks the first Edit/Write/MultiEdit on each file until concrete investigation facts (importers, data schema, user instruction) are stated. Use when setting up a hook to stop guessed edits, or when Claude tends to edit before investigating.
disable-model-invocation: false
risk: safe
---

# Fact-Forcing Gate

Install a PreToolUse hook that blocks the first edit or write to each file per
session until the model states what it actually checked. Self-evaluation
("are you sure?") always returns "yes" — asking for concrete facts forces a
Grep/Glob/Read pass that self-evaluation never triggers.

Arguments: `$ARGUMENTS` - `global` to install in `~/.claude/settings.json`, or blank for project-level `.claude/settings.json`

## Usage

```
/fact-forcing-gate           # project-level (.claude/settings.json)
/fact-forcing-gate global    # user-level (~/.claude/settings.json)
```

## Behavior

### 1. Determine scope

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

### 2. Write the gate script

```bash
cat > "$HOOKS_DIR/fact-forcing-gate.sh" << 'SCRIPT'
#!/bin/bash
set -e

input=$(cat)
tool=$(echo "$input" | jq -r '.tool_name // empty')
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
session=$(echo "$input" | jq -r '.session_id // "default"')

[[ "$tool" != "Edit" && "$tool" != "Write" && "$tool" != "MultiEdit" ]] && exit 0
[[ -z "$file_path" ]] && exit 0

STATE_DIR="${FACT_FORCING_GATE_STATE_DIR:-.claude/cache/fact-forcing-gate}/$session"
mkdir -p "$STATE_DIR" 2>/dev/null || exit 0
key=$(echo -n "$file_path" | md5sum | cut -d' ' -f1)
marker="$STATE_DIR/$key"

[[ -f "$marker" ]] && exit 0
touch "$marker"

cat >&2 << MSG
Before touching $file_path, present these facts, then retry:

1. List every file that imports/requires it (Glob/Grep, or find/grep via Bash)
2. If it reads or writes a data file, state the field names, types, and date
   format (synthetic or redacted values, never real production data)
3. Quote the user's current instruction verbatim
MSG
exit 2
SCRIPT

chmod +x "$HOOKS_DIR/fact-forcing-gate.sh"
```

### 3. Register in settings (idempotent)

```bash
[[ -f "$SETTINGS" ]] && CURRENT=$(cat "$SETTINGS") || CURRENT='{}'
HOOK_PATH="$(pwd)/$HOOKS_DIR/fact-forcing-gate.sh"
[[ "$ARGUMENTS" == "global" ]] && HOOK_PATH="$HOME/.claude/hooks/fact-forcing-gate.sh"

ALREADY=$(echo "$CURRENT" | jq --arg h "$HOOK_PATH" \
  '[.hooks.PreToolUse[]?.hooks[]? | select(.command == $h)] | length')

if [[ "$ALREADY" == "0" ]]; then
  echo "$CURRENT" | jq \
    --arg matcher "Edit|Write|MultiEdit" --arg hook "$HOOK_PATH" \
    '.hooks.PreToolUse += [{"matcher": $matcher, "hooks": [{"type": "command", "command": $hook}]}]' \
    > "$SETTINGS"
  echo "Hook registered in: $SETTINGS"
else
  echo "Hook already registered in: $SETTINGS — skipped"
fi
```

### 4. Verify

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/x.py"},"session_id":"t"}' \
  | bash "$HOOKS_DIR/fact-forcing-gate.sh"
# First run: exits 2, prints the fact-force block to stderr
# Same input again: exits 0 (marker already set)
```

### 5. Report

```
Fact-forcing gate installed:

  Hook script:  .claude/hooks/fact-forcing-gate.sh
  Settings:     .claude/settings.json
  Scope:        project

Blocks the first Edit/Write/MultiEdit per file per session until the model
states its importers, the data schema touched, and the user's instruction.
To remove: delete the PreToolUse entry pointing at fact-forcing-gate.sh.
```

## Examples

**First edit to a file this session:**
```
Claude calls Edit on src/billing/invoice.py
→ Hook exits 2: "Before touching ... present these facts ..."
Claude runs Grep for importers, reads the schema, quotes the instruction
Claude retries the same Edit → hook exits 0, edit proceeds
```

**Second edit to the same file:**
```
Claude calls Edit on src/billing/invoice.py again
→ Hook exits 0 immediately (marker already set for this session)
```

## Token Optimization

**Expected range**: 500–1,200 tokens (initial install), 100–200 tokens (re-run, already registered)

**Caching**: Per-file "already investigated" markers live in
`.claude/cache/fact-forcing-gate/<session_id>/`, scoped to the session so a
new session re-gates every file. No project-content caching applies.

**Early exit**: Skips non-Edit/Write/MultiEdit tool calls immediately (exit 0
before any state check); skips a file whose marker already exists; skips
re-registering the hook if `jq` finds it already present in settings.

**Patterns used**: Early exit, template-based generation (fixed script, no
LLM authoring), Bash for system queries.

## Edge Cases

- **`jq` not installed**: report the required JSON change to make manually,
  same as `git-guardrails`.
- **Hook already registered**: detected via `jq` lookup by command path,
  install step is skipped and reported, not duplicated.
- **State directory unwritable** (read-only filesystem, sandboxed tmp): the
  script exits 0 rather than blocking every edit indefinitely.
- **Batched parallel edits to a not-yet-touched file**: the first call in the
  batch is denied and marks the file as checked, so sibling edits in the same
  batch proceed unblocked. Send dependent edits to a new file sequentially,
  not in one parallel batch, and re-read the file after presenting facts.
- **`MultiEdit`**: gated once per file, same as a single `Edit`, since all its
  edits target one `file_path`.

## Safety

Only ever blocks (exit 2) or allows (exit 0); never modifies files itself.
Applies only to `Edit`, `Write`, and `MultiEdit` — no interaction with `Bash`
or other tools. State markers are session-scoped filesystem files, safe to
delete (`rm -rf .claude/cache/fact-forcing-gate/`) to force re-gating.
