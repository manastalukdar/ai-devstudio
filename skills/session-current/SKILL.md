---
name: session-current
description: View active session status with progress and context information
disable-model-invocation: false
---

Show the current session status by:

1. Check if `.claude/sessions/.current-session` exists
2. If no active session, inform user and suggest starting one
3. If active session exists:
   - Show session name and filename
   - Calculate and show duration since start
   - Show last few updates
   - Show current goals/tasks
   - Remind user of available skills

Keep the output concise and informative.

## Token Optimization

**Expected range**: 150–300 tokens (initial), 50 tokens (cache hit)

**Caching**: Caches active session metadata in `.claude/cache/session-current/` for 7 days.

**Early exit**: Returns immediately if no active session is found.

**Patterns used**: Grep-before-Read, early exit, caching
