---
name: context-budget
description: Report estimated context window utilization and flag when approaching the compaction threshold
disable-model-invocation: false
risk: none
---

# Context Budget

Report how much of the current context window is estimated to be consumed, identify the largest contributors, and recommend actions when approaching the compaction threshold. Run this before starting a long task or when responses feel slow or truncated.

## Usage

```
/context-budget              # Current utilization snapshot
/context-budget --verbose    # Show per-contributor breakdown
/context-budget --compact    # Recommend what to compact or save
```

## Behavior

### Phase 1: Measure loaded content

Collect byte sizes of all content that contributes to context:

```bash
# CLAUDE.md files (auto-loaded)
find . -name "CLAUDE.md" -not -path "*/node_modules/*" | xargs wc -c 2>/dev/null | tail -1

# Active session file
[ -f ".claude/sessions/.current-session" ] && \
  wc -c < "$(cat .claude/sessions/.current-session)" 2>/dev/null || echo 0

# Auto-loaded rules
find .claude/rules -name "*.md" 2>/dev/null | xargs wc -c 2>/dev/null | tail -1

# Agent memory files loaded this session
find .claude/agent-memory -name "MEMORY.md" 2>/dev/null | xargs wc -c 2>/dev/null | tail -1

# This project's memory index
[ -f ".claude/memory/MEMORY.md" ] && wc -c < ".claude/memory/MEMORY.md" || echo 0
```

### Phase 2: Estimate token counts

Convert bytes to tokens using the ~4 chars/token heuristic for English prose:

```bash
TOTAL_BYTES=$(( CLAUDE_MD_BYTES + SESSION_BYTES + RULES_BYTES + MEMORY_BYTES ))
ESTIMATED_TOKENS=$(( TOTAL_BYTES / 4 ))
```

Add an overhead estimate for conversation history: prompt the user to confirm if the session has been long (>30 turns) — add 20k tokens per 30 turns as an approximation.

### Phase 3: Map to model context windows

| Model       | Context Window | Compaction Threshold (80%) |
|-------------|---------------|---------------------------|
| Haiku 4.5   | 200k tokens   | 160k tokens               |
| Sonnet 4.6  | 200k tokens   | 160k tokens               |
| Opus 4.8    | 200k tokens   | 160k tokens               |

Assume Sonnet 4.6 (200k) unless the user specifies otherwise.

### Phase 4: Display utilization

```
Context Budget — 2026-06-04  (model: Sonnet 4.6, 200k window)

  Contributor            Est. Tokens   % of Window
  ───────────────────────────────────────────────
  CLAUDE.md (3 files)        3,200        1.6%
  Auto-loaded rules          1,800        0.9%
  Active session             2,400        1.2%
  Agent memory                 600        0.3%
  Conversation history      ~24,000      12.0%  (est. ~30 turns)
  ───────────────────────────────────────────────
  Total estimated           32,000       16.0%

  Status: OK — 84% remaining (~168k tokens free)
  Compaction threshold: 160k tokens (80%)
```

**Status levels:**
- `OK` — below 60% utilized
- `WATCH` — 60–80% utilized; consider `/context-save` before long tasks
- `COMPACT SOON` — 80–90% utilized; run `/context-save` now
- `CRITICAL` — above 90%; Claude Code will auto-compact on next response

### Phase 5: Recommendations (with `--compact` flag)

When status is WATCH or above, suggest specific actions:

```
Recommendations to free context:

  1. /context-save    — checkpoint WIP to .claude/wip/ before compaction
  2. Start a new conversation after saving — context resets to baseline (~8k tokens)
  3. If session file is large (>50k chars), run /session-end to archive it

Largest reducible contributors:
  - Conversation history: 24,000 tokens — only reducible by starting a new session
  - Active session file: 2,400 tokens — archive with /session-end if work is done
```

## Token Optimization

**Expected range**: 200–500 tokens (initial), 100–200 tokens (subsequent calls)

**Caching**: Stores last measurement in `.claude/cache/context-budget/snapshot.json` with a 5-minute TTL. Subsequent calls within the TTL return cached values instantly.

**Early exit**: If all measured contributors total < 10k tokens (well under threshold), reports "OK — ample context remaining" in one line and exits.

**Patterns used**: Bash for system queries, early exit, progressive disclosure (`--verbose` for full breakdown, default shows summary only).

## Examples

**Healthy session:**
```
/context-budget
→ Total estimated: 18,000 tokens (9% of 200k)
  Status: OK — 91% remaining
```

**Approaching limit:**
```
/context-budget --compact
→ Total estimated: 152,000 tokens (76% of 200k)
  Status: WATCH — consider /context-save before starting a long task
  [recommendations shown]
```

## Edge Cases

- **No active session**: Session contribution shows 0; other contributors still measured.
- **No `.claude/` directory**: All internal contributions show 0; only conversation history estimate is shown.
- **User on Opus with extended thinking**: Context consumption is higher; recommend reducing threshold to 70% manually.
- **Long conversations (100+ turns)**: Heuristic may underestimate; note this limitation in output.

## Safety

Read-only. No writes except to the cache file. No network calls.
