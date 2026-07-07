---
name: spec-driven-development
description: Gated 4-phase workflow (Specify → Plan → Tasks → Implement) where nothing advances without explicit human review — surfaces assumptions before any code is written.
disable-model-invocation: false
risk: none
---

# Spec-Driven Development

I'll walk you through four locked phases: Specify, Plan, Tasks, Implement. Nothing moves forward without your explicit "proceed" at each gate. All assumptions surface in Phase 1 before any code is written.

Arguments: `$ARGUMENTS` — feature, bug fix, or initiative to drive through the workflow

## Token Optimization

**Expected range**: 500–1,500 tokens per phase; cache the spec artifact and reuse across phases

**Early exit**: If `$ARGUMENTS` already contains a written spec document, skip Phase 1 and open Phase 2

**Patterns used**: Git diff scope (only changed files in Phase 4), progressive disclosure (one phase at a time)

## Phase 1 — Specify

Produce a spec document covering:

- **Goal**: one sentence — what success looks like
- **Scope**: what is in and explicitly what is out
- **Assumptions**: everything assumed true that could be wrong; flag any high-risk assumption
- **Acceptance criteria**: numbered, each independently verifiable
- **Open questions**: items that need answers before implementation begins

Save to `docs/specs/<slug>.md` if a `docs/` directory exists, otherwise output inline.

**Gate**: "Proceed to Plan?" — do not continue until the user confirms or amends the spec.

## Phase 2 — Plan

With the confirmed spec, produce an architecture plan:

- **Approach**: chosen design and why (one paragraph)
- **Alternatives considered**: 2–3 alternatives and why they were ruled out
- **Files affected**: list every file that will change, be created, or be deleted
- **Dependencies**: external packages, APIs, or services required
- **Risks**: top 3 risks and mitigations

**Gate**: "Proceed to Tasks?" — do not continue until the user confirms or amends the plan.

## Phase 3 — Tasks

Break the confirmed plan into a dependency-ordered task list:

- Each task must be independently completable and testable
- Annotate tasks with `[~30m]`, `[~2h]`, etc. effort estimates
- Mark blocking dependencies between tasks explicitly
- Each task ends with a clear "done when" criterion

Save to `tasks/<slug>-tasks.md` if a `tasks/` directory exists, otherwise output inline.

**Gate**: "Proceed to Implement?" — do not continue until the user confirms or amends the task list.

## Phase 4 — Implement

Execute tasks in dependency order. For each task:

1. State which task is starting
2. Implement it
3. Run the applicable test or verification command
4. Report "Task N complete — [done-when criterion met]" before moving to the next task

Follow `/incremental-implementation` discipline: no more than ~100 lines of new code before verifying.

## Edge Cases

- **User skips a gate ("just do it all")**: Acknowledge, warn that skipping gates increases rework risk, then proceed if they confirm
- **Spec reveals the wrong problem**: Surface this in Phase 1; do not silently pivot
- **Phase 4 reveals a spec gap**: Pause, add the gap to the spec as an amendment, confirm with the user, then resume
- **No `docs/` or `tasks/` directory**: Output artifacts inline; note they were not persisted
