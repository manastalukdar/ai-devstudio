# Subagent Routing Convention

When to spawn a subagent vs. handle work inline.

Adapted from [gbrain's subagent routing pattern](https://github.com/garrytan/gbrain).

---

## Spawn a Subagent When

- The task is **independent** of the current response (result not needed before replying)
- The task is **slow** (file scanning, large grep, test runs) and would block the main thread
- The task requires **specialized tools** that shouldn't pollute the main agent's context
- The task is **always-on ambient** work (e.g., signal-detector, background indexing)
- Running **multiple analyses in parallel** would save wall-clock time

## Handle Inline When

- The result is **needed immediately** to continue the current response
- The task is **fast** (single file read, simple grep, one bash command)
- The task is **stateful** — it must share context with the current conversation
- The task involves **user confirmation** — subagents cannot prompt for input

## AI DevStudio Subagent Types

| Agent | When to spawn |
|---|---|
| `code-reviewer` | Code review tasks, skill validation |
| `security-auditor` | Security scans, CVE checks, secrets detection |
| `test-runner` | Running tests, coverage analysis |
| `quality-fixer` | Lint/type error fix cycles |
| `claude-md-auditor` | Doc drift audits, CLAUDE.md validation |

Spawn via the Agent tool with `subagent_type` set to the agent name.

## Signal Detector is Always Parallel

`/signal-detector` must always run as a background parallel task — never inline. It should never delay the main response.

## Coordination Pattern

When spawning multiple subagents:
1. Identify which tasks are independent
2. Launch all independent tasks in a single message (parallel tool calls)
3. Aggregate results after all complete
4. Present a unified summary — do not show raw subagent output unless the user asks

## Context Isolation

Subagents do not inherit the parent conversation context unless you explicitly pass it in the prompt. Always brief the subagent with:
- What to do (specific task)
- What not to do (scope limit)
- What to return (format and length)
