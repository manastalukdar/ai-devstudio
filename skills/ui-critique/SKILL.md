---
name: ui-critique
description: Dual-agent UX design review — Assessment A runs design-director heuristics while Assessment B runs visual pattern analysis; results synthesized into a prioritized critique snapshot
disable-model-invocation: false
risk: none
---

# UI Critique

I'll conduct a two-perspective design review and synthesize findings into a prioritized, persisted snapshot that feeds `/ui-polish`.

## Purpose

Catch design quality issues before they reach users. The dual-agent approach surfaces problems that a single-perspective review misses — heuristic reviewers overlook CSS anti-patterns; pattern checkers miss information hierarchy failures.

## Usage

- `/ui-critique` — review changed UI files
- `/ui-critique [file or directory]` — review a specific target
- `/ui-critique --full` — review all UI files in the project

## Behavior

### Step 1 — Identify target files

```bash
# Default: changed UI files only
git diff --name-only HEAD -- '*.tsx' '*.jsx' '*.html' '*.css' '*.vue' '*.svelte' '*.css' '*.scss'

# If no changed UI files, check staged:
git diff --cached --name-only -- '*.tsx' '*.jsx' '*.html' '*.css' '*.vue' '*.svelte'
```

If still empty and no argument provided, report "No UI files in scope" and stop.

### Step 2 — Load context

```bash
# Read shape brief if present (guides heuristic review)
ls .claude/cache/ui-shape/ 2>/dev/null | head -5

# Read previous critique snapshot if present (avoids re-reporting fixed issues)
ls .claude/cache/ui-critique/ 2>/dev/null | head -5
```

### Step 3 — Run dual assessment (parallel)

Spawn two independent assessment agents. Neither sees the other's output before synthesis.

**Assessment A — Design Director Heuristics:**
Review for:
- Information hierarchy: does visual weight match content importance?
- Typography: consistent scale, appropriate line-height, readable measure (65–75ch target)
- Spacing rhythm: consistent spacing units, not cramped (< 8px padding on interactive elements)
- Color: sufficient contrast (WCAG AA minimum), purposeful use, not decorative noise
- Empty and error states: are they designed or absent?
- Touch targets: interactive elements ≥ 44×44px

**Assessment B — Visual Pattern Analysis:**
Grep target files for known AI/template anti-patterns:

```bash
# Side-tab accent (border-left/right as decorative stripe)
grep -rn "border-left\|border-right" --include="*.css" --include="*.tsx" | grep -v "border-left: 0\|border-right: 0"

# Gradient text
grep -rn "background-clip.*text\|webkit-background-clip.*text" --include="*.css" --include="*.tsx"

# Glassmorphism overuse
grep -rn "backdrop-filter\|backdrop-blur" --include="*.css" --include="*.tsx"

# Bounce/elastic easing
grep -rn "bounce\|elastic\|spring\|cubic-bezier.*1\.[2-9]" --include="*.css" --include="*.tsx"

# Over-rounded corners (≥ 24px on cards)
grep -rn "border-radius.*[2-9][4-9]px\|border-radius.*[3-9][0-9]px" --include="*.css"

# Eyebrow-on-every-section (small all-caps tracking)
grep -rn "letter-spacing.*[2-9]px\|text-transform.*uppercase" --include="*.css" --include="*.tsx"

# Numbered section markers (01/02/03)
grep -rn '"0[1-9]"\|"[0-9][0-9]"\.' --include="*.tsx" --include="*.jsx" | head -10
```

Report each match with file:line and a one-line description of why it's a problem.

### Step 4 — Synthesize

If both assessments ran independently: synthesize normally.
If only one ran: prepend **[DEGRADED — single-perspective review]** to the output.

Produce a scored critique:
- **P0 — Blockers**: accessibility failures, illegible text, broken layouts
- **P1 — Major**: hierarchy failures, prominent anti-patterns, missing states
- **P2 — Minor**: polish opportunities, subtle pattern issues

### Step 5 — Persist snapshot

```bash
mkdir -p .claude/cache/ui-critique
# Write snapshot as SCOPE-DATE.md
```

Snapshot format:
```
Score: P0: N, P1: N, P2: N
Target: <files reviewed>
Date: <ISO date>

[P0] <issue> — <file:line>
[P1] <issue> — <file:line>
...
```

Report: "Critique complete. Run `/ui-polish` to work through the backlog."

## Examples

```
/ui-critique src/components/Dashboard.tsx
→ dual assessment → synthesis → snapshot saved

/ui-critique
→ reviews changed UI files → P0/P1/P2 prioritized findings
```

## Token Optimization

**Expected range**: 800–2,500 tokens (dual assessment + synthesis)

**Early exit**: No UI files in scope → stop immediately (50 tokens).

**Patterns used**: Grep-before-Read (Assessment B uses grep only), git diff scope default, progressive disclosure (P0 first, P1/P2 summarized)

**Cache**: Reads shape brief; writes critique snapshot for `/ui-polish` to consume.

## Edge Cases

- All grep matches are false positives (e.g., `border-left: 0`): report "Pattern checks clean"
- No shape brief present: Assessment A runs with general design heuristics
- Large files (> 500 lines): grep only, note that full read was skipped

## Safety

Read-only except for writing the critique cache snapshot. No source file edits.
