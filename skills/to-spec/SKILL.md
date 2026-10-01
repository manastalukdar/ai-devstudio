---
name: to-spec
description: Turn the current conversation into a spec and publish it to the project issue tracker — no interview, just synthesis of what's already been discussed. Use after grilling or a design conversation when ready to commit to a plan.
disable-model-invocation: true
risk: none
---

# To Spec

Takes the current conversation context and codebase understanding and produces a spec. **Do NOT interview the user** — just synthesize what you already know.

## Process

### 1. Explore the repo

Understand the current state of the codebase if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

### 2. Sketch the test seams

Identify the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. Fewer seams across the codebase is better — the ideal number is one.

Check with the user that these seams match their expectations.

### 3. Write and publish the spec

Use the template below. Then publish it to the project issue tracker with the `ready-for-agent` label — no additional triage needed.

## Spec template

```markdown
## Problem Statement

The problem the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A numbered list of user stories. Each in the format:

1. As an <actor>, I want a <feature>, so that <benefit>

This list should be extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets (they go stale fast).

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts only.

## Testing Decisions

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (similar types of tests in the codebase)

## Out of Scope

A description of what is out of scope for this spec.

## Further Notes

Any further notes about the feature.
```

## Token Optimization

**Expected range**: 400–2,000 tokens (codebase exploration + spec synthesis)

**Patterns used**: Grep-before-Read for GLOSSARY.md and ADRs, git diff scope (staged changes as context anchor), progressive disclosure (spec synthesized from conversation context)

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
