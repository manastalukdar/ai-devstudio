---
name: discernment-nudge
description: Appends 2-3 reflection questions after substantive answers the user might act on — estimates, advice, factual claims — to prompt critical thinking. Fires at most once per conversation.
disable-model-invocation: false
risk: none
---

# Discernment Nudge

After a substantive answer the user might act on, append 2–3 short questions prompting them to verify key facts, question the reasoning, or notice missing context.

## Purpose

Help users catch errors, gaps, and unexamined assumptions — without lecturing.

## Behavior

### When to add the nudge

Add the nudge after answers that involve:

- **Estimates**: time, cost, performance, capacity
- **Advice in consequential domains**: architecture decisions, security, finance, legal-adjacent, health
- **Factual claims** the user may rely on without checking
- **Multi-step reasoning** where an early mistake cascades
- **Data interpretation**: trends, comparisons, correlations
- **Drafted artifacts**: plans, proposals, emails the user will send

### When to skip it

Do NOT add the nudge for:

- Simple factual lookups (dictionary definitions, syntax checks)
- Purely educational explanations the user won't directly act on
- Creative writing, fiction, brainstorming
- Casual conversational exchanges
- Code the user will run (tests will catch it)
- Reformatting or summarizing material the user supplied
- Cases where the user already asked for verification, citations, a quick answer, or a review of their own work
- Opinion requests ("what do you think of X?")

### Frequency

**At most once per conversation.** After it has fired, skip it for all subsequent turns.

## Format

Follow the answer with:

```
A few things worth a second look:
- [Question 1 tied to something specific in the answer]
- [Question 2 tied to something specific in the answer]
- [Question 3 tied to something specific in the answer]  ← optional
```

**Question rules:**
- Tied to something concrete in the answer — not generic ("are you sure?")
- Phrased as the user would ask themselves
- Under ~120 characters each
- No preamble beyond the fixed lead-in line
- Nothing after the questions

## Examples

After estimating a migration will take 2 weeks:
```
A few things worth a second look:
- Does the 2-week estimate account for the staging environment setup you mentioned?
- Have you confirmed the target database supports the JSON column types in the schema?
- Is there a rollback plan if the cutover window runs long?
```

After recommending a rate-limiting approach:
```
A few things worth a second look:
- Does your load balancer strip the X-Forwarded-For header before it reaches the app?
- Have you load-tested this limit against your actual p99 traffic pattern?
```

## Token Optimization

**Expected range**: 100–200 tokens (the nudge itself), 0 tokens (skipped turns)

**Early exit**: Skips silently for all ineligible answer types and after the first fire.

**Patterns used**: Early exit
