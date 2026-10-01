---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow that resists a first glance.
disable-model-invocation: false
risk: none
---

# Diagnosing Bugs

A discipline for hard bugs. Skip phases only when explicitly justified.

When exploring the codebase, read `GLOSSARY.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars so credentials stay in the environment. If redacted output is not enough to diagnose, say so and ask the user.

## Phase 1: Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug (one command that goes red on *this* bug), you will find the cause. If you don't, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one, in roughly this order

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) that drives the UI and asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it in isolation.
6. **Throwaway harness.** Minimal subset of the system that exercises the bug code path.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs.
8. **Bisection harness.** Automate "boot at state X, check, repeat" for `git bisect run`.
9. **Differential loop.** Run same input through old vs new version and diff outputs.
10. **HITL bash script.** Last resort for human-click steps — keeps the loop structured.

### Tighten the loop

- Can I make it faster? (Cache setup, skip unrelated init, narrow test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is a debugging superpower.

### Non-deterministic bugs

Goal is not a clean repro but a **higher reproduction rate**. Loop 100×, parallelise, add stress, narrow timing windows. A 50%-flake is debuggable; 1% is not.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask for: (a) access to the reproducing environment, (b) a redacted captured artifact (HAR file, log dump, core dump), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

### Completion criterion

Phase 1 is done when you can name **one command** you have **already run** that is:

- [ ] **Red-capable**: drives the actual bug code path and asserts the user's exact symptom
- [ ] **Deterministic**: same verdict every run
- [ ] **Fast**: seconds, not minutes
- [ ] **Agent-runnable**: unattended

If you catch yourself reading code to build a theory before this command exists, **stop**. No red-capable command, no Phase 2.

## Phase 2: Reproduce + minimise

Run the loop. Confirm the failure mode matches what the **user** described (wrong bug = wrong fix). Then shrink to the **smallest scenario that still goes red** — cut inputs, callers, config one at a time, re-running after each cut.

Done when every remaining element is load-bearing: removing any one makes the loop go green.

## Phase 3: Hypothesise

Generate **3–5 ranked hypotheses** before testing any. Each must be **falsifiable**:

> "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

Show the ranked list to the user before testing — they often re-rank instantly.

## Phase 4: Instrument

Each probe maps to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end is a single grep. **Perf branch**: for performance regressions, establish a baseline measurement first, then bisect.

## Phase 5: Fix + regression test

Write the regression test **before the fix**, but only if there is a **correct seam** for it (one where the test exercises the real bug pattern as it occurs at the call site).

**If no correct seam exists, that itself is the finding.** Flag it for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 loop against the original scenario.

## Phase 6: Cleanup

- [ ] Original repro no longer reproduces (re-run Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed
- [ ] Throwaway prototypes deleted
- [ ] The correct hypothesis is stated in the commit/PR message

## Token Optimization

**Expected range**: 300–1,500 tokens per phase (iterative — each phase uses only what's needed)

**Patterns used**: Grep-before-Read for codebase exploration, early exit when loop already exists, git diff scope for regression identification

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
