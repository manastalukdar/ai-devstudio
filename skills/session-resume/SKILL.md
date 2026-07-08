---
name: session-resume
description: Resume previous work from archived session with full context restoration
disable-model-invocation: false
---

# Claude Session Resume

1. Check for an active session by reading the `.claude/sessions/.current-session` file.
2. If the file is empty or doesn't exist, inform the user that there is no active session to resume and stop the process.
3. If the file exists, read contents and provide summary to user. Also provide points on possible next steps to potentially resume that session.

## Token Optimization

**Expected range**: 200–600 tokens (initial), 100 tokens (cache hit)

**Caching**: No persistent caching beyond the session file itself.

**Early exit**: Returns immediately if the named session does not exist.

**Patterns used**: Early exit, caching (session files)
