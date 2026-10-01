---
name: to-tickets
description: Break a plan, spec, or the current conversation into tracer-bullet tickets with blocking edges. Use after /to-spec or after a grilling session when ready to break work into agent-ready vertical slices.
disable-model-invocation: true
risk: none
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you haven't already explored the codebase, do so to understand the current state. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets:

- Each slice cuts a narrow but **complete** path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception.** A wide refactor is one mechanical change (rename a column, retype a shared symbol) whose blast radius fans across the whole codebase. Sequence it as **expand–contract**:
1. **Expand**: add the new form beside the old so nothing breaks
2. **Migrate**: call sites in batches, each batch a ticket blocked by expand, CI green throughout
3. **Contract**: delete the old form once no caller remains, blocked by every migrate batch

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets must complete first (if any)
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask:
- Does the granularity feel right?
- Are the blocking edges correct?
- Should any tickets be merged or split?

Iterate until the user approves.

### 5. Publish

Publish approved tickets to the configured tracker.

**Local files**: write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered in dependency order (blockers first).

**Real issue tracker (GitHub, Linear, etc.)**: publish one issue per ticket in dependency order. Use native blocking/sub-issue relationships where available. Apply the `ready-for-agent` label.

Work the **frontier**: any ticket whose blockers are all done.

Do NOT close or modify any parent issue.

## Local ticket template

```markdown
# <NN>: <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective.

**Blocked by:** the numbers/titles of the tickets that gate this one, or "None (can start immediately)".

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
```

## Issue tracker template

```markdown
## Parent

A reference to the parent issue (if the source was an existing issue; otherwise omit).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)".
```

In either form, avoid specific file paths or code snippets — they go stale fast. Exception: prototype-derived snippets that encode a decision more precisely than prose can (trimmed to decision-rich parts only).

## Token Optimization

**Expected range**: 400–2,000 tokens (codebase exploration + ticket drafting)

**Patterns used**: Grep-before-Read for GLOSSARY.md and ADRs, progressive disclosure (draft list presented before publishing), early exit if spec already contains a clear breakdown

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
