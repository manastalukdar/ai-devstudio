---
name: cost-track
description: Report token spend per session and cumulative totals from session logs
disable-model-invocation: true
risk: none
---

# Cost Tracker

Report estimated token spend per development session and cumulative totals, using session file sizes and logged metadata as proxies. Works without API access.

## Usage

```
/cost-track              # Summary for current + recent sessions
/cost-track --all        # All archived sessions
/cost-track --reset      # Clear cumulative cost register
```

## Behavior

### Phase 1: Check active session

```bash
if [ -f ".claude/sessions/.current-session" ] && [ -s ".claude/sessions/.current-session" ]; then
    ACTIVE=$(cat ".claude/sessions/.current-session")
    ACTIVE_SIZE=$(wc -c < "$ACTIVE" 2>/dev/null || echo 0)
    # Rough estimate: ~4 chars per token for session narrative
    ACTIVE_TOKENS=$((ACTIVE_SIZE / 4))
    echo "Active session: ~${ACTIVE_TOKENS} tokens estimated"
fi
```

### Phase 2: Scan archived sessions

```bash
# Collect all archived session files
find .claude/sessions -name "*.md" -not -name ".current-session" | sort -r | head -20
```

For each file, compute:
- File size → divide by 4 for rough token estimate
- Session name and date from filename
- Number of `/skill` invocations via `grep -c "^/" <file>`

### Phase 3: Load cost register

```bash
REGISTER=".claude/cache/cost-track/register.json"
if [ -f "$REGISTER" ]; then
    CUMULATIVE=$(jq -r '.cumulative_tokens' "$REGISTER")
    SESSIONS_COUNTED=$(jq -r '.sessions_counted' "$REGISTER")
else
    CUMULATIVE=0
    SESSIONS_COUNTED=0
fi
```

### Phase 4: Compute estimates and update register

Apply the following rate table for cost estimation (USD, approximate as of mid-2025):

| Model         | Input (per 1M tokens) | Output (per 1M tokens) |
|---------------|-----------------------|------------------------|
| Haiku 4.5     | $0.80                 | $4.00                  |
| Sonnet 4.6    | $3.00                 | $15.00                 |
| Opus 4.8      | $15.00                | $75.00                 |

Default: assume Sonnet 4.6, 70% input / 30% output split.

```bash
# Per-session cost estimate
TOKENS_IN=$((ACTIVE_TOKENS * 70 / 100))
TOKENS_OUT=$((ACTIVE_TOKENS * 30 / 100))
COST_USD=$(echo "scale=4; ($TOKENS_IN * 3 + $TOKENS_OUT * 15) / 1000000" | bc)
```

Write updated register:

```bash
jq -n --argjson cum "$((CUMULATIVE + ACTIVE_TOKENS))" \
       --argjson cnt "$((SESSIONS_COUNTED + 1))" \
  '{cumulative_tokens: $cum, sessions_counted: $cnt, last_updated: now | todate}' \
  > "$REGISTER"
```

### Phase 5: Display report

```
Cost Tracker — 2026-06-04

Active session
  File size:   12,840 bytes
  Est. tokens: ~3,210
  Est. cost:   ~$0.0577  (Sonnet 4.6, 70/30 split)

Recent archived sessions (last 5)
  session-2026-06-03-feature-auth.md   ~2,800 tokens  ~$0.0504
  session-2026-06-02-bugfix-api.md     ~1,950 tokens  ~$0.0351
  session-2026-06-01-refactor.md       ~4,100 tokens  ~$0.0738

Cumulative (18 sessions tracked)
  Est. tokens: ~52,300
  Est. cost:   ~$0.94

Note: estimates are file-size proxies; actual API usage may differ.
Run /cost-track --reset to zero the cumulative register.
```

## Token Optimization

**Expected range**: 80–200 tokens (all Bash, no model invocation)

**Caching**: Writes running totals to `.claude/cache/cost-track/register.json`. The register persists across sessions; only new/unprocessed session files are added to the total.

**Early exit**: If no sessions directory exists, prints a one-line setup message and exits.

**Patterns used**: Bash for system queries, early exit, caching.

## Edge Cases

- **No `bc` available**: Falls back to integer arithmetic with `$((...))`.
- **No session files**: Reports "0 sessions tracked" and exits.
- **`--reset` flag**: Prompts for confirmation before clearing the register, then writes zeros.
- **Very large session files**: Caps display at 20 most recent; `--all` removes cap.

## Safety

Read-only except for writing to `.claude/cache/cost-track/register.json`. No external network calls. No commits.
