---
name: grill-me
description: Relentlessly interview the user about a plan or design, walking down every branch of the decision tree one question at a time until reaching shared understanding. Use when user wants to stress-test a plan, get challenged on their design, or says "grill me".
disable-model-invocation: false
risk: none
---

# Grill Me

Conduct a relentless interview about every aspect of the current plan or design until reaching shared understanding.

Arguments: `$ARGUMENTS` - the plan, design, or topic to be grilled on (or leave blank to use current conversation context)

## Behavior

Interview relentlessly. Walk down each branch of the decision tree, resolving dependencies between decisions one by one. For each question, provide your recommended answer as a starting point.

**Ask exactly one question at a time.** Wait for the response before asking the next.

If a question can be answered by exploring the codebase, explore the codebase instead of asking.

Continue until every branch of the decision tree is resolved — not just the obvious ones. Press on:
- Why this approach over the alternatives
- What happens at the edge cases
- How this interacts with existing architecture
- What gets harder / what gets easier downstream
- What assumptions are baked in that could be wrong
- What the rollback looks like if this turns out to be wrong

Do not accept vague answers. If the answer is "it depends", follow up with "depends on what, exactly?"

## Examples

```
/grill-me "add real-time notifications via WebSockets"
/grill-me "migrate from REST to GraphQL"
/grill-me  ← uses current conversation context
```

## Sample Question Sequence

```
1. What's the primary trigger for a notification — user action, system event, or both?
   → Recommended: system event (decoupled, easier to test)

[wait for answer]

2. Should notifications be persistent (stored + replayable) or fire-and-forget?
   → Recommended: persistent — users expect to see missed notifications on login

[wait for answer]

3. You mentioned Postgres — are you planning to use LISTEN/NOTIFY or a separate message queue?
   → Recommended: LISTEN/NOTIFY for < 10k concurrent users; add Redis if you scale past that

...continues until all branches resolved
```

## Completion Criteria

Stop when:
- Every major decision has been made explicitly
- Edge cases have been addressed
- The user can articulate the approach without ambiguity
- No open "it depends" branches remain

Then offer: `/write-plan` to capture decisions as an implementation plan, or `/to-prd` to produce a full PRD.

## Token Optimization

**Expected range**: 100–300 tokens per question turn

**Codebase exploration**: Uses Grep/Bash to verify claims rather than asking questions that can be answered by reading code — avoids unnecessary back-and-forth.

**Patterns used**: Early exit (stops when all branches resolved), progressive disclosure (one question at a time)
