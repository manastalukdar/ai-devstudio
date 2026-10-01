---
name: writing-for-agents
description: Reference for writing documents that agents consume — skills, AGENTS.md, CLAUDE.md, pointed-at docs. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.
disable-model-invocation: false
risk: none
---

# Writing for Agents

Reference for writing any document an agent consumes: a skill, an `AGENTS.md` / `CLAUDE.md`, a doc reached by a pointer. The packaging differs; the writing does not — the same levers make each one predictable, since the agent takes the same *process* every run rather than producing the same output.

## Context pointers

A **context pointer** is a reference held in the agent's context that names some out-of-context material and encodes the condition for reaching it. A skill's description is one; a line in `AGENTS.md` naming a doc is the same object.

The pointer's *wording*, not its target, decides when the agent reaches the material, and how reliably. A must-have target behind a weakly worded pointer is a variance bug: sharpen the wording first, and inline the material only if sharpening fails.

A pointer does two jobs: state what the material is, and list the **branches** that should trigger reaching it.

- **Front-load the leading word**: the pointer does its triggering work there.
- **One trigger per branch.** Synonyms that rename a single branch collapse into one.
- **Cut identity the body already carries.**

## The two loads

- **Context load**: the cost of always-loaded material on the agent's window. An `AGENTS.md` line, a skill description — spending tokens and attention every turn whether or not it fires.
- **Cognitive load**: the cost on the human — which documents exist and when to reach for each. Not a cost to minimise: it's the price of human agency.

## Information hierarchy

A document is built from **steps** (ordered actions the agent performs) and **reference** (definitions, rules, facts consulted on demand). The core decision is where each piece sits on the hierarchy:

1. **In-file step**: what the agent does, in order (primary tier)
2. **In-file reference**: consulted on demand
3. **Disclosed reference**: a separate file reached by a context pointer, loaded only when the pointer fires

**Progressive disclosure** is the move down the ladder — pushing material behind a pointer so the top stays legible. The cleanest disclosure test: inline what every branch needs, push behind a pointer what only some branches reach.

**Co-location**: keep a concept's definition, rules, and caveats under one heading rather than scattered. A concept's definition and its caveats are one meaning; scattering fragments one meaning across many places is a variance bug.

**Sprawl** is the failure mode: a document too long even when every line is live. The cure is the ladder.

## Steps and completion criteria

Every step ends on a **completion criterion** — the condition that tells the agent the work is done.

- **Clarity**: can the agent tell done from not-done? A vague bound invites premature completion. Sharpen the bound first.
- **Demand**: how much it requires. "Every modified model accounted for" forces thorough work where "produce a change list" does not.

The strongest criteria are both checkable and exhaustive.

## When to split

Split one document into two only when the cut earns it:

- **By sequence**: split where post-completion steps would tempt the agent to rush the step in front.
- **By invocation**: split when one branch never needs what another branch always uses.

## Leading words

A **leading word** is a compact concept from the model's pretraining that the agent thinks with while running the document (_lesson_, _fog of war_, _tracer bullets_). Repeated as a token, it accumulates a distributed definition and anchors behaviour in the fewest tokens.

Hunt for opportunities to refactor with leading words. A triad spelled out at three sites, a pointer spending a sentence to gesture at one idea — each begging to collapse into a single token.

**Negation is the failure mode beside this lever.** Steering by prohibition drags the forbidden behaviour into context and makes it *more* available. Prompt the **positive**: state the target behaviour. A prohibition earns its place only as a hard guardrail you cannot phrase positively.

## Pruning

- Keep each meaning in a **single source of truth**: one authoritative place. Duplication costs maintenance and inflates prominence.
- The **environment** is a source of truth too (`package.json` scripts, config files, `--help` output). Cache what the agent cannot find by looking: unwritten conventions, reasons behind choices, gotchas no config confesses.
- Check every line for **relevance**: does it still bear on what the document does? Without pruning the default fate is **sediment** — stale layers that settle because adding feels safe and removing feels risky.
- Hunt **no-ops** sentence by sentence: an instruction the model already obeys by default pays load to say nothing.

## Token Optimization

**Expected range**: 100–400 tokens (reference read; no file I/O)

**Patterns used**: Loaded as reference when creating or editing agent-consumed documents; early exit when only a single pattern needs clarification

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
