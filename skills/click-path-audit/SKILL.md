---
name: click-path-audit
description: Trace every user-facing touchpoint (button, toggle, form submit) through its full state-change sequence to find interaction bugs where handlers individually work but conflict when combined — silent resets, async races, stale closures. Use when a button "does nothing" despite no crash or type error, after modifying a shared state store, or after a refactor touching shared state, and static debugging already came up empty.
disable-model-invocation: false
risk: safe
---

# Click Path Audit

Find interaction bugs that reading code or running the debugger misses: a handler calls two functions that each work in isolation, but the second silently undoes the first's state change.

## Usage

```
/click-path-audit                    # audit UI files changed in the working tree
/click-path-audit <file-or-dir>      # audit a specific component or directory
/click-path-audit --store <name>     # audit every consumer of one shared state store
```

## Behavior

### Phase 1: Map shared state side effects

Before auditing any handler, build a side-effect map for every store/context action in scope (Redux slice, Zustand store, React context, signal, view-model — whichever this stack uses):

```
For each action/setter/reducer case:
  - fields it sets
  - fields it resets as a side effect (not the fields the caller asked it to change)
```

Flag any action that resets a field it does not own — that is the recurring root cause. Skip this phase if the audit target has no shared state (a single stateless component).

### Phase 2: Trace each touchpoint

For every interactive element in scope (click, submit, change, keydown handlers):

1. List the handler's function calls in call order.
2. For each call, note what it reads, what it sets, and what it resets (from the Phase 1 map).
3. Check whether a later call undoes an earlier call's state change (Sequential Undo).
4. Check async calls for order-dependent resolution (Async Race).
5. Check closures capturing stale values across repeated calls (Stale Closure).
6. Check the handler actually performs the action its label promises, not just a partial step (Missing Transition).
7. Check guard conditions that can never be true at that point (Dead Path).
8. Check for a watcher/effect that reacts to this state and reverts it (Effect Interference).

### Phase 3: Report

One entry per confirmed bug, worst first:

```
Touchpoint: <label> in <file>:<line>
Pattern: <Sequential Undo | Async Race | Stale Closure | Missing Transition | Dead Path | Effect Interference>
Trace: call 1 sets {x:true} -> call 2 resets {x:false}
Expected: <what the label promises>
Actual: <observed final state>
Fix: <minimal change>
```

Report zero findings plainly if none are confirmed — do not pad with stylistic notes.

## Examples

**Store-focused audit after a refactor:**
```
/click-path-audit --store cartStore
```
Finds that `removeItem(id)` resets `checkoutStep` to 0 as a side effect, so the "Continue to checkout" button silently returns users to step 0 after they remove one item mid-checkout.

**Single component after a bug report:**
```
/click-path-audit src/components/ComposeButton.tsx
```
Finds the handler calls `openCompose(true)` then `selectItem(null)`, and `selectItem` resets `composeOpen: false` — the button does nothing, no crash, no type error.

## Token Optimization

**Expected range**: 800–3,000 tokens (initial), 150–350 tokens (cache hit)

**Caching**: Caches the Phase 1 side-effect map per store file in `.claude/cache/click-path-audit/<store-hash>.json`, keyed on the store file's content hash, 7-day TTL. Reused across Phase 2 runs against the same store until the store file changes.

**Early exit**: If the audit target has no shared state store or context (grep for common store/reducer/context patterns returns nothing), skip Phase 1 and audit handlers as self-contained — report immediately if none call more than one state-mutating function.

**Patterns used**: Grep-before-Read to locate store definitions and handlers before reading full files, git diff scope default (changed UI files only when no target given), caching, progressive disclosure (summary list first, full trace on request).

## Edge Cases

- **No shared state anywhere in scope**: Phase 1 is skipped; only Async Race, Stale Closure, Missing Transition, and Dead Path patterns apply.
- **Large app with no target given**: scope to files changed in the working tree (`git diff --name-only HEAD`); ask the user to confirm scope before a full-app sweep, since this audit is expensive per touchpoint.
- **Store spans multiple files (slices/modules)**: build one combined side-effect map before Phase 2; a partial map produces false negatives.
- **Handler behavior only diverges under async timing**: note the race as a finding even if it cannot be reproduced deterministically; do not discard it for being non-repro.

## Safety

Read-only analysis. No file changes and no test runs. Use `/ui-harden` for production-readiness UI gaps (empty/error states, overflow) and `/e2e-generate` to turn a confirmed finding into a regression test — this skill does not generate or run tests itself.
