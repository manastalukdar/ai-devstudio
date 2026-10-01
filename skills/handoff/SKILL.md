---
name: handoff
description: Compact the current conversation into a portable handoff document so a fresh agent can continue the work. Use when switching harnesses, directories, or colleagues, or forking a side task mid-phase.
disable-model-invocation: true
risk: none
---

# Handoff

Write a handoff document summarising the current conversation so a fresh agent can continue the work.

## Usage

```
/handoff
/handoff "focus on the auth module next"
```

If arguments are passed, treat them as a description of what the next session will focus on and tailor the document accordingly.

## Output location

Save to the **temporary directory** of the user's OS — not the current workspace. Resolve from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows). Name it `handoff-<timestamp>.md`.

Tell the user the absolute path.

## Document contents

Include:

- **Current state**: what has been decided, built, or discovered
- **Next steps**: what the next session should do first
- **Context pointers**: paths or URLs to existing artifacts (specs, plans, ADRs, issues, commits, diffs) — do NOT duplicate their content; reference by path or URL instead
- **Suggested skills**: which skills the next agent should call the Skill tool for (e.g. `grilling`, `tdd`, `code-review`)
- **Open questions**: decisions still pending
- **Redacted secrets**: redact any sensitive information (API keys, passwords, PII) — write `<REDACTED>` in its place

## Format

```markdown
# Handoff: <brief description of the work>

**Generated**: <ISO timestamp>
**Next session focus**: <from arguments, or "continue from where we left off">

## Current state

<what has been decided and done>

## Context pointers

- Spec: <path or URL>
- Open tickets: <path or URL>
- Recent commits: <branch and hash range>

## Next steps

1. <first thing to do>
2. <second thing to do>

## Suggested skills

- `/grilling` — to sharpen <X>
- `/tdd` — to implement <Y>

## Open questions

- <decision still pending>
```

## When to use

Use `/handoff` narrowly: for a **new harness**, a **new directory**, a **colleague**, or forking a side task **mid-phase**. What it buys is portability.

If you're staying in the same harness and nothing here matters to what's next, `/clear` is cheaper. If you want to compress context and continue in the same session, use `/compact` instead.

## Token Optimization

**Expected range**: 200–600 tokens (reads conversation context + writes one file; no codebase exploration needed)

**Patterns used**: Early exit (stateless write — no file reads required unless referencing specific artifacts)

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
