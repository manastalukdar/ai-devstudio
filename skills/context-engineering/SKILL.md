---
name: context-engineering
description: Audit and curate the 5-layer agent context hierarchy to prevent quality degradation mid-session — rules files, specs, source files, error output, and conversation history.
disable-model-invocation: false
risk: none
---

# Context Engineering

I'll audit your current context load, identify what is inflating it unnecessarily, and restructure the 5-layer hierarchy so the agent stays sharp for the rest of the session.

Arguments: `$ARGUMENTS` — optional focus (e.g., "optimize for implementation", "optimize for debugging")

## Token Optimization

**Expected range**: 200–600 tokens (audit report + recommendations)

**Early exit**: If context appears healthy (no redundant files loaded, no stale error traces), report "Context healthy — no changes needed"

**Patterns used**: Bash for file size checks, progressive disclosure (summary first, details on request)

## The 5-Layer Context Hierarchy

```
Layer 1 — Rules files       CLAUDE.md, .claude/rules/*.md
Layer 2 — Specs / designs   docs/specs/, PRD, ADRs
Layer 3 — Source files      only the files currently being changed
Layer 4 — Error output      compiler errors, test failures, logs
Layer 5 — Conversation      current session history
```

Each layer has an appropriate size budget. Layers 3–5 are the most common source of bloat.

## Step 1 — Audit Current Context

```bash
# Estimate context pressure indicators
wc -l .claude/rules/*.md 2>/dev/null | tail -1
find . -name "CLAUDE.md" | xargs wc -l 2>/dev/null | tail -1
ls -la docs/specs/ 2>/dev/null | head -10
```

Check for common inflation sources:
- Entire files loaded when only a function is needed
- Stale error traces from previous attempts (no longer relevant)
- Spec documents for features not currently being implemented
- Multiple versions of the same file loaded
- Test output exceeding 200 lines

## Step 2 — Report Findings

```
Context Audit:

Layer 1 (Rules):     [N lines] — [healthy / inflated]
Layer 2 (Specs):     [N files loaded] — [relevant / stale]
Layer 3 (Source):    [N files] — [scoped / over-broad]
Layer 4 (Errors):    [N lines] — [current / stale]
Layer 5 (History):   [estimated turns] — [fresh / compressible]

Top 3 inflation sources:
1. [source] — [recommended action]
2. [source] — [recommended action]
3. [source] — [recommended action]
```

## Step 3 — Apply Recommendations

For each inflation source, take the recommended action:

**Over-broad source files**: Identify the specific functions or classes needed; reference by grep pattern rather than loading the whole file

**Stale error traces**: Summarize to the key error type and location (1–2 lines); drop the full stack trace from active context

**Off-topic specs**: Note the spec exists and where to find it; remove it from active context

**Redundant conversation**: Summarize completed sub-tasks as a single line each; carry forward only open items

## Step 4 — Curate Going Forward

Recommend a loading strategy for the rest of the session based on `$ARGUMENTS`:

```
Recommended context loading strategy:
- Layer 3: Load only [file list] — grep for symbols before loading full files
- Layer 4: Keep error output to last 50 lines per error type
- Layer 5: Summarize completed phases; keep only current phase in full detail
```

## Edge Cases

- **No CLAUDE.md or rules files**: note the absence; recommend creating minimal rules for consistent behavior
- **Context already very large**: recommend starting a fresh session with a focused handoff prompt; provide a handoff template
- **Cannot determine what is loaded**: provide the optimization heuristics and let the user apply them manually
