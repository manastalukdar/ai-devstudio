---
name: incremental-implementation
description: Enforce vertical-slice discipline — implement one thin slice (~100 lines max), test it, verify it works, commit it, then repeat. Never write more than can be tested in a single step.
disable-model-invocation: false
risk: none
---

# Incremental Implementation

I'll implement your feature in the smallest working slices possible. Each slice gets implemented, tested, verified as working, and committed before the next one starts. The system must be in a working state after every slice.

Arguments: `$ARGUMENTS` — feature or task to implement incrementally

## Token Optimization

**Expected range**: 300–800 tokens per slice (implement + test + verify)

**Early exit**: If `$ARGUMENTS` already maps to a single file change under 50 lines, implement it directly without splitting

**Patterns used**: Git diff scope (staged only), early exit (passing tests = done)

## Before Starting — Decompose Into Slices

Before writing any code, list the vertical slices:

```
Slices:
1. [one-line description] — done when: [verifiable criterion]
2. [one-line description] — done when: [verifiable criterion]
...
```

A vertical slice cuts through all layers (route → handler → service → storage) for a thin but complete capability — not a horizontal layer ("add all models first"). If a proposed slice cannot be tested in isolation, split it further.

**Confirm the slice list before implementing.** If the user wants to adjust, do so now.

## Per-Slice Loop

Repeat for each slice:

### Step 1 — Announce the Slice

```
Starting slice N/M: [description]
Target: ~[estimated lines] lines
Done when: [criterion]
```

### Step 2 — Implement

Write only the code for this slice. Hard limit: ~100 lines of new/changed production code. If the slice requires more, stop and split it.

### Step 3 — Test

Run the applicable test command immediately:

```bash
# Examples — infer from project
npm test -- --testPathPattern=<relevant>
pytest tests/test_<relevant>.py
go test ./...
cargo test
```

If no automated tests exist for this slice, write a minimal test first (Red), then implement (Green).

### Step 4 — Verify

Confirm the done-when criterion is met:

```
Slice N complete.
  - Test result: [pass/fail count]
  - Done when: [criterion] → MET
  - System state: working (no regressions)
```

If any test fails or the criterion is not met, fix it before continuing.

### Step 5 — Commit

```bash
git add -p  # stage only slice changes
git status  # confirm no unintended files
```

Report what would be committed and wait for confirmation before committing (or commit directly if the user has enabled auto-commit for this session).

## Rules

- **No skipping ahead**: do not start slice N+1 while slice N has a failing test
- **No horizontal layers**: never implement "all the models" or "all the routes" as a slice
- **No orphaned code**: every slice leaves the system in a state where it builds and tests pass
- **No big bangs**: if a slice grows past ~100 lines, decompose further

## Edge Cases

- **Circular dependencies between slices**: note the cycle, choose the ordering that leaves the most useful intermediate state, add a TODO stub for the other direction
- **External API or DB not available in tests**: use a minimal fake/stub for the slice; note the limitation
- **User wants to skip testing for a spike**: acknowledge, label the slice as a spike (not a commit), remove it from the committed history before the real implementation
- **Build is already broken before starting**: stop, report the breakage, do not proceed until the baseline is green
