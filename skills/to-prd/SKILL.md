---
name: to-prd
description: Synthesize the current conversation context and codebase into a full PRD — problem statement, user stories, implementation decisions, testing decisions, and scope boundaries. Use when user wants to turn a discussion into a formal PRD or publish requirements as an issue.
disable-model-invocation: false
risk: safe
---

# To PRD

Synthesize the current conversation and codebase understanding into a full PRD. Do NOT interview — just synthesize what is already known.

Arguments: `$ARGUMENTS` - optional scope hint or `publish` to push directly to the issue tracker

## Behavior

### 1. Explore the Codebase

```bash
# Understand current state relevant to the feature being discussed
ls CONTEXT.md 2>/dev/null  # check for domain vocabulary
find . -type d -name "src" -o -name "app" -o -name "lib" \
  2>/dev/null | head -5

# Check for existing tests as prior art
find . -name "*.test.*" -o -name "*.spec.*" \
  2>/dev/null | grep -v node_modules | head -10
```

Use domain vocabulary from `CONTEXT.md` throughout the PRD if it exists. Respect any ADRs in the area being touched.

### 2. Identify Deep Module Opportunities

Before writing the PRD, sketch the major modules to build or modify. Look for opportunities to extract deep modules — ones with small, stable interfaces that encapsulate substantial behavior and can be tested in isolation.

Check with the user that the module sketch matches their expectations. Confirm which modules require tests.

### 3. Produce the PRD

```markdown
## Problem Statement

[The problem from the user's perspective — not technical, not solution-oriented. What pain exists today?]

## Solution

[The solution from the user's perspective. What changes for them?]

## User Stories

[Numbered list — comprehensive. Cover happy path, edge cases, error states, admin flows, and any affected adjacent features.]

1. As a [actor], I want [feature], so that [benefit]
2. As a [actor], I want [feature], so that [benefit]
...

## Implementation Decisions

[What will be built or modified. Include:]
- Modules to build/modify and their interfaces (not file paths)
- Architectural decisions and their rationale
- Schema changes and API contracts
- Specific technical constraints or interactions
- How this fits with existing patterns in the codebase

Do NOT include specific file paths or code snippets — they go stale.

## Testing Decisions

- What makes a good test for this feature (test observable behavior through public interfaces, not implementation details)
- Which modules will have tests
- Prior art: similar test patterns already in the codebase
- What is NOT worth testing (implementation details, framework internals)

## Out of Scope

[Explicit list of related things that are NOT in this PRD — prevents scope creep and documents deliberate exclusions]

## Further Notes

[Open questions, dependencies on other work, known risks, or constraints not captured above]
```

### 4. Publish (when `publish` argument or user confirms)

```bash
# Publish to GitHub Issues with needs-triage label
gh issue create \
  --title "[PRD] $FEATURE_TITLE" \
  --body "$PRD_CONTENT" \
  --label "needs-triage,enhancement" 2>/dev/null || \
  echo "gh CLI not available — PRD written to docs/prds/$(date +%Y-%m-%d)-$SLUG.md"
```

If `gh` is unavailable, write to `docs/prds/YYYY-MM-DD-slug.md`.

### 5. Review Checkpoint

Before finalizing, ask:
- "Does the module sketch match your expectations?"
- "Which modules do you want tests written for?"
- "Anything that should be explicitly out of scope that isn't listed?"

## Examples

```
/to-prd
/to-prd "real-time notification system"
/to-prd publish
```

## Token Optimization

**Expected range**: 600–2,000 tokens (full PRD), 200–400 tokens (codebase exploration phase)

**Grep-before-Read**: Scans for existing patterns and prior art via grep before reading full test files.

**No interview**: Synthesizes from conversation context — avoids back-and-forth question cycles that inflate token usage.

**Patterns used**: Grep-before-Read, template-based generation, progressive disclosure (module sketch → PRD on confirm)
