---
name: agent-debug
description: Structured self-debugging for AI agent run failures — loop limits, repeated retries with no progress, context drift, or tool failures. Use when an agent session is stuck or degrading and needs a reproducible diagnosis instead of a blind retry.
disable-model-invocation: false
risk: none
---

# Agent Debug

Diagnose a failing or stuck agent run through capture, root-cause classification, contained recovery, and a structured introspection report — instead of retrying blindly.

## Usage

```
/agent-debug                  # Diagnose the current stuck/failing run
/agent-debug --report-only    # Skip recovery, just produce the introspection report
```

## Behavior

### Phase 1: Capture

Record the failure before touching anything:

- error type, message, last tool call sequence
- what the agent was trying to accomplish
- signs of context pressure: duplicated plans, oversized pasted output, repeated near-identical prompts
- environment assumptions to verify: cwd, branch, expected files, service state

### Phase 2: Diagnose

Match the failure to a known pattern before changing anything:

| Symptom | Likely cause | Check |
| --- | --- | --- |
| Same tool call repeated | loop with no exit condition | last N tool calls for repetition |
| Reasoning degrading, output rambling | context overflow from duplicated notes/logs | recent context for low-signal bulk |
| Connection refused / timeout | wrong port, service down | service health, URL, port |
| 429 / rate limit | retry storm, no backoff | call frequency and spacing |
| File missing after write | wrong cwd, race, branch drift | actual path, `git status`, file existence |
| "Fixed" but still failing | wrong hypothesis | isolate the exact failing case, re-derive |

Ask: is this logic, state, environment, or policy failure? Deterministic or transient? What is the smallest reversible check that would confirm the diagnosis?

### Phase 3: Contained Recovery

Take the smallest action that changes the diagnosis surface, in order:

1. Restate the actual goal in one sentence.
2. Verify real state directly (`git status`, `ls`, service check) instead of trusting memory.
3. Trim context to active goal, blockers, and evidence only.
4. Narrow scope to one failing command, file, or test.
5. Run one discriminating check.
6. Only then retry — and only the narrowed piece.

Never claim an unsupported auto-heal ("reset agent state", "reload harness config") unless actually invoking a real tool that does it. Escalate to the user when the failure is high-risk, externally blocked, or the diagnosis is still ambiguous after one recovery attempt.

### Phase 4: Introspection Report

```markdown
## Agent Self-Debug Report
- Task:
- Failure:
- Root cause:
- Recovery action taken:
- Result: success | partial | blocked
- Evidence:
- Follow-up needed:
```

Never end with "fixed it" alone — always give the pattern, root cause, action, and evidence.

## Examples

**Loop detected:**
```
/agent-debug
→ Pattern: same `npm test` call 4x with no diff between runs
→ Cause: no-exit retry path, error unread between attempts
→ Recovery: read the actual failure output, narrow to the one failing test
→ Result: partial — root cause identified, fix pending
```

**Context drift:**
```
/agent-debug
→ Pattern: last 6 turns re-paste the same 400-line log
→ Cause: context overflow, reasoning quality dropping
→ Recovery: trim to goal + last error line, restate objective
→ Result: success
```

## Token Optimization

**Expected range**: 500–2,000 tokens (initial), 100–300 tokens (cache hit)

**Caching**: None — each failure is unique context; nothing to cache across calls.

**Early exit**: If the last 2 tool calls already show forward progress (no repetition, no error), reports "no stuck pattern detected" in one line and exits without running full diagnosis.

**Patterns used**: Early exit, progressive disclosure (capture and diagnose before recovery, report last).

## Edge Cases

- **No error captured**: still runs Phase 1 against the described symptom (e.g., "feels stuck") rather than skipping capture.
- **Diagnosis inconclusive**: report says so explicitly and escalates rather than guessing a recovery action.
- **Recovery attempted but symptom persists**: re-run Phase 2 with the new evidence before attempting a second recovery; do not repeat the same recovery action twice.

## Safety

Read-only by default: Phase 3 recovery actions are diagnostic (reading state, trimming context, narrowing scope), not destructive. No file deletion, no `git reset`, no force operations. If a recovery step would touch tracked files, create a git checkpoint first per `.claude/rules/git-workflow.md`.

Distinct from `/llm-qa` (investigates LLM *output* quality — hallucination, retrieval, prompt issues in a shipped app) and `/debug-systematic` (hypothesis-driven debugging of *application code* bugs). Use this skill instead when the failure is in the *agent's own run* — loops, drift, or tool-call breakdowns — not in the code or output it produced.
