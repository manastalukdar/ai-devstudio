---
name: completion-verify
description: Verify a session's own work (build, types, lint, tests, diff scope, quick security check) before claiming a task is done. Use when about to say "done", before opening a PR, or after a feature/refactor is finished.
disable-model-invocation: false
risk: safe
---

# Completion Verify

Run the quality gates a task must clear before you tell the user it is done.

## Usage

```
/completion-verify              # verify current uncommitted work
/completion-verify --staged      # verify staged changes only
```

## Behavior

### Phase 1: Diff scope

```bash
git diff --stat
git diff --name-only
```

Confirm the changed files match what the task actually required. Flag anything unrelated.

### Phase 2: Build

```bash
npm run build 2>&1 | tail -20 || pnpm build 2>&1 | tail -20
```

Stop and fix before continuing if the build fails.

### Phase 3: Type check

```bash
npx --no-install tsc --noEmit 2>&1 | head -30
# or: pyright . 2>&1 | head -30
```

### Phase 4: Lint

```bash
npm run lint 2>&1 | head -30
# or: ruff check . 2>&1 | head -30
```

### Phase 5: Tests

```bash
npm test 2>&1 | tail -50
# or: pytest -q 2>&1 | tail -50
```

Report pass/fail counts. Never disable or skip a failing test to make this pass.

### Phase 6: Quick security check

```bash
git diff | grep -E "sk-|api[_-]?key|password\s*=|BEGIN.*PRIVATE KEY" | head -10
```

### Phase 7: Verdict

```
COMPLETION CHECK
Scope:    N files, all within task
Build:    PASS/FAIL
Types:    PASS/FAIL (N errors)
Lint:     PASS/FAIL (N warnings)
Tests:    PASS/FAIL (X/Y passed)
Security: PASS/FAIL (N findings)

Verdict: READY / NOT READY
```

Only claim the task is done when every gate that applies to the project passes.

## Examples

**Clean finish:**
```
/completion-verify
→ 3 files changed, build PASS, types PASS, tests 42/42, no findings
  Verdict: READY
```

**Caught issue:**
```
/completion-verify
→ tests 40/42 (2 failed in UserService.test.ts)
  Verdict: NOT READY — fix failing tests before claiming done
```

## Token Optimization

**Expected range**: 500–1,500 tokens (initial), 100–300 tokens (cache hit)

**Caching**: Caches detected build/test/lint commands in `.claude/cache/completion-verify/config.json` for 7 days, invalidated when `package.json` (or equivalent manifest) changes.

**Early exit**: If `git diff --stat` is empty, reports "nothing to verify" and exits immediately.

**Patterns used**: Git diff scope default, caching, grep-before-read for the security check, early exit.

## Edge Cases

- **No test suite**: Report tests as N/A, note the gap, still verify build/types/lint.
- **No build step (e.g. interpreted scripts)**: Skip Phase 2, note it as N/A.
- **Monorepo**: Scope build/test/lint to the packages touched by the diff, not the whole repo.
- **Nothing staged or changed**: Exit early with "nothing to verify".

## Safety

Read-only: runs build/lint/test commands and greps the diff, but makes no file changes itself. If any command mutates files (e.g. an autofix lint script), do not run it here — surface the failure and let the user choose to fix it.

## See Also

- `/loop-verify` — an independent checker that gates loop-produced changes with an APPROVE/REJECT/ESCALATE_HUMAN verdict; use that when a separate agent must validate another agent's automated change. `/completion-verify` is for verifying your own session's work before claiming completion.
- `/test` — full context-aware test runner with failure analysis and auto-fix; `/completion-verify` calls tests as one gate among several, not a replacement for it.
