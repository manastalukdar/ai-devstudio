---
name: signal-detector
description: Always-on ambient skill that captures decisions, patterns, entity mentions, and original thinking from the current conversation and writes them to agent memory. Run in parallel — never blocks the main response.
disable-model-invocation: false
---

# Signal Detector

I run silently in the background on every session to capture signals worth remembering — architectural decisions, recurring patterns, entity mentions, and original insights — and write them to the appropriate agent memory file.

## Token Optimization

**Expected range**: 100–400 tokens (ambient background call), 20–50 tokens (no signals found)

**Patterns used**: Early exit (no signal detected), Bash for file lookups, progressive disclosure (write summary only)

**Early exit**: If the conversation contains only routine tool calls with no decisions, entities, or insights, write nothing and exit silently.

## What Counts as a Signal

**Architectural decisions** — choices about structure, technology, or approach that constrain future work:
- "We're using X instead of Y because..."
- "The pattern for this is..."
- "Never do Z in this codebase"

**Recurring patterns** — something done more than once that should become a skill or convention:
- Same workaround applied twice
- Same question asked twice
- Same error resolved the same way twice

**Entity mentions** — people, tools, services, external systems referenced in context:
- Team members and their roles
- External APIs and their constraints
- Key files, directories, or modules that are referenced frequently

**Original insights** — non-obvious observations about the codebase or workflow:
- Performance characteristics discovered
- Hidden coupling between components
- Surprising behavior of a dependency

## Step 1 — Scan Conversation for Signals

Review the current conversation context. For each signal type, check:

```
Decisions:  Any "we chose X", "the rule is Y", "always/never Z" statements?
Patterns:   Any fix or approach applied more than once in this session?
Entities:   Any names, tools, or systems worth remembering for next session?
Insights:   Any non-obvious discovery about the code or system?
```

If none found → exit silently.

## Step 2 — Route Signal to the Right Memory File

```bash
# Identify the relevant agent memory file
ls .claude/agent-memory/

# Route by signal type:
# Architectural decisions → .claude/agent-memory/code-reviewer/MEMORY.md
# Test patterns / failures → .claude/agent-memory/test-runner/MEMORY.md
# Security findings → .claude/agent-memory/security-auditor/MEMORY.md
# Quality / lint patterns → .claude/agent-memory/quality-fixer/MEMORY.md
# Doc drift patterns → .claude/agent-memory/claude-md-auditor/MEMORY.md
# Cross-cutting / project-wide → all relevant files
```

## Step 3 — Write to Agent Memory (Compiled Truth + Timeline)

Each agent memory file uses two sections:

**Compiled Truth** — the current synthesized understanding (overwrite/update in place):
```markdown
## Compiled Truth
- The project uses X pattern for Y (confirmed 2026-04-27)
- Never modify Z directly; always go through the wrapper
```

**Timeline** — append-only evidence trail (prepend new entries):
```markdown
## Timeline
- 2026-04-27: Discovered that X causes Y when Z; fixed by W
- 2026-04-20: [prior entry]
```

Write the signal to the Timeline first. If it confirms or contradicts a Compiled Truth entry, update that entry. If it's new, add it to Compiled Truth.

## Step 4 — Notability Gate

Before writing, apply the notability gate — do NOT write if:
- The signal is already captured in an existing Compiled Truth entry
- The signal is ephemeral (specific to this one file, one run, one error message)
- The signal is a routine status update with no lasting relevance

Only write signals that will change how a future agent session approaches the project.

## Step 5 — Exit Silently

Do not report what was written unless the user asks. This skill runs as background ambient capture — it should not interrupt the main workflow.

If the user asks "what did you just remember?", report the new Timeline entries written this session.

## Edge Cases

- **No agent memory directory**: Create `.claude/agent-memory/` and a generic `MEMORY.md`; note this in the response
- **Signal spans multiple agents**: Write to each relevant file; keep entries concise and cross-reference where useful
- **Contradiction with existing Compiled Truth**: Flag the contradiction explicitly in the Timeline entry; do not silently overwrite — ask the user which is correct before updating Compiled Truth
