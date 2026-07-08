---
name: session-list
description: List all past development sessions with summaries and timestamps
disable-model-invocation: false
---

List all development sessions by:

1. Check if `.claude/sessions/` directory exists
2. List all `.md` files (excluding hidden files and `.current-session`)
3. For each session file:
   - Show the filename
   - Extract and show the session title
   - Show the date/time
   - Show first few lines of the overview if available
4. If `.claude/sessions/.current-session` exists, highlight which session is currently active
5. Sort by most recent first

Present in a clean, readable format.

## Token Optimization

**Expected range**: 100–400 tokens (initial), 50 tokens (cache hit)

**Caching**: Caches session index in `.claude/sessions/.session-index.json` for 7 days.

**Early exit**: Returns immediately if the session index is empty.

**Patterns used**: Grep-before-Read, early exit, caching
