---
name: first-principles
description: Decompose a problem to its irreducible truths before proposing solutions — strip inherited assumptions, rebuild from fundamentals, surface the real constraint
disable-model-invocation: false
risk: none
---

# First Principles

Force-question the assumptions behind a problem before jumping to solutions. Useful when conventional approaches feel stuck, when a design debate is going in circles, or when you suspect the framing of the problem is wrong.

## Usage

```
/first-principles "<problem or question to decompose>"
/first-principles                   # decompose the current task or decision
/first-principles --fast            # condensed version: just constraints + one rebuilt solution
```

## Behavior

### Step 1 — State the problem as given

Capture the problem exactly as it was framed. If from `$ARGUMENTS`, use that. Otherwise, ask for a one-sentence statement.

### Step 2 — Strip the solution framing

Identify and list every assumption embedded in the current framing:

> These phrases are assumption flags: "we have to", "we always", "everyone does", "the system requires", "we can't change", "that's just how it works"

For each assumption, ask: **"Why?"** until you reach a constraint that is physically, legally, or economically non-negotiable — not just conventional.

Example:
```
Assumption: "We need a SQL database"
  Why? → "Because we need transactions"
  Why transactions? → "Because two tables must update together"
  Why two tables? → "Because we modeled them separately"
  Real constraint: "Atomic updates are required" (schema is not the constraint)
```

### Step 3 — List the irreducible constraints

Write down only what is genuinely non-negotiable:
- Physical laws (latency of light, disk I/O speed)
- Hard legal / compliance requirements
- Contractual obligations
- Immovable external system interfaces

Everything else is a convention, a habit, or a past decision that can be revisited.

### Step 4 — Rebuild from the constraints

Starting only from the irreducible constraints, derive a solution fresh:

> "If we only knew what we *must* do, and had no knowledge of how it's currently done, what would we build?"

Generate 2–3 solutions that satisfy the constraints. Do not favor the conventional approach; treat it as one option among others.

For each:
- What does it give up compared to the current approach?
- What does it gain?
- What assumption does it challenge?

### Step 5 — Compare and recommend

| Solution | Gains | Gives up | Key assumption challenged |
|---|---|---|---|
| Current approach | Familiar, low change risk | [the thing that's stuck] | None |
| Option A (rebuilt) | [gain] | [tradeoff] | [assumption dropped] |
| Option B (rebuilt) | [gain] | [tradeoff] | [assumption dropped] |

Recommend the option with the best gain-to-change-cost ratio. Flag if the current approach is actually optimal — first principles sometimes confirms the existing solution.

### Step 6 — Identify what to validate first

If a rebuilt solution is recommended, name the one assumption most likely to break it:

```
The rebuilt solution depends on: [key assumption]
Cheapest test: [how to validate it in < 1 day]
```

## Example

```
Problem as given: "Our API is too slow — we need to add a caching layer"

Assumptions stripped:
  "Add a caching layer" → assumes slowness is read-heavy and cacheable
  "The API is slow" → assumes slowness is in the API, not the client or network
  "Too slow" → what is the actual latency? What is the target?

Irreducible constraint:
  Response must arrive in < 200ms p95 for the user experience to feel instant

Rebuilt from constraints:
  Option A: Cache (assumed path) — valid if > 60% of requests are cache-hit eligible
  Option B: Profile first — instrument p95 breakdown before adding infrastructure
  Option C: Push to client — preload data at login; API slowness irrelevant for most flows

Recommendation: Option B (profile first) — the constraint is 200ms p95; we don't yet
know if the API is the bottleneck. Caching solves read latency; if the bottleneck is a
slow write or external call, caching adds complexity without fixing the problem.

Validate: Add timing logs to the 3 slowest endpoints; read results in < 1 day.
```

## Edge Cases

- **Problem is genuinely well-framed**: Confirm the current approach is optimal and state why; do not invent alternatives for their own sake.
- **Multiple competing problems**: Decompose each separately; do not mix constraints across different problems.
- **Technical decision**: Focus Step 2 on architectural assumptions (not just business ones).
- **Fast mode (`--fast`)**: Output only the stripped constraints and one rebuilt solution; skip the comparison table.

## Token Optimization

**Expected range**: 300–800 tokens

**Patterns used**: Progressive disclosure (constraints first, solutions second), early exit (if problem is clear and well-constrained, go straight to Step 3)

**No files read**: This skill operates on conversation context and the stated problem; no codebase analysis unless needed to identify constraints.
