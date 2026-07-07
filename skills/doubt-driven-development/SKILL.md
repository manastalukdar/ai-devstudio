---
name: doubt-driven-development
description: Spawn a fresh adversarial reviewer mid-implementation for any non-trivial decision — branching logic, cross-module boundaries, irreversible operations — to catch what confirmation bias misses.
disable-model-invocation: false
risk: none
context: fork
agent: code-reviewer
---

# Doubt-Driven Development

For any non-trivial code decision, I'll spawn a fresh context agent that is explicitly biased to find problems. If the skeptic cannot refute the approach, proceed with confidence.

Arguments: `$ARGUMENTS` — the decision, design, or code block to subject to adversarial review

## Token Optimization

**Expected range**: 400–1,000 tokens (claim summary + skeptic review + verdict)

**Early exit**: If `$ARGUMENTS` is a trivial change (rename, formatting, adding a log line), skip the skeptic and proceed

**Patterns used**: Git diff scope (review only the specific decision, not the entire file)

## When to Invoke

Trigger `doubt-driven-development` automatically for:
- Any conditional with 3+ branches or nested conditionals
- Any cross-module boundary (calling into a different service, package, or layer)
- Any operation that is difficult or impossible to reverse (delete, migrate, send, publish)
- Any security-sensitive path (auth, input validation, token handling)
- Any performance-critical path (hot loop, batch operation, query)

## Step 1 — Articulate the Decision

Summarize the decision under review in a form the skeptic can evaluate:

```
Decision: [one paragraph — what was decided and why]

Code in question:
[relevant code block — max 50 lines]

Alternatives considered:
1. [alternative] — ruled out because [reason]
2. [alternative] — ruled out because [reason]
```

## Step 2 — Spawn Adversarial Reviewer

A fresh agent (no memory of the session that produced the decision) reviews the decision with the following mandate:

**Skeptic prompt**: "Your job is to find problems with this decision. Default to skepticism. Look for: (1) edge cases the happy path ignores, (2) assumptions that could be wrong, (3) a simpler alternative that was missed, (4) security or correctness issues, (5) ways this breaks under load or failure. If you cannot find a real problem, say so explicitly — but try hard."

The skeptic returns one of:
- `REFUTED` — specific problem found; implementation should change
- `UNCERTAIN` — possible problem; needs investigation before proceeding
- `CONFIRMED` — could not find a meaningful objection

## Step 3 — Apply Verdict

**REFUTED**: Stop. Address the specific problem raised. Re-run `doubt-driven-development` after the fix.

**UNCERTAIN**: Investigate the flagged concern. If it turns out to be real, treat as REFUTED. If not, note the investigation and proceed.

**CONFIRMED**: Document the skeptic's confirmation in a brief comment and proceed.

```
// Adversarially reviewed: skeptic could not refute this approach.
// Key concern checked: [what the skeptic tested for]
```

## Edge Cases

- **Skeptic raises a known non-issue** (already handled upstream): cite where it is handled and treat as CONFIRMED
- **Multiple decisions in one invocation**: review them sequentially, not in bulk
- **User disagrees with the skeptic's REFUTED verdict**: note the disagreement, document the risk, and proceed only with explicit user confirmation
- **No fresh context available** (resource constraint): perform the adversarial review in the current context with an explicit "switch to skeptic mode" preamble; note it is less reliable
