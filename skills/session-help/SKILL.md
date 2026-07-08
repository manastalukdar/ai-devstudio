---
name: session-help
description: Show help for the session management system and available commands
disable-model-invocation: false
---

Show help for the session management system:

## Session Management Skills

The session system helps document development work for future reference.

### Available Skills:

- `/project:session-start [name]` - Start a new session with optional name
- `/project:session-update [notes]` - Add notes to current session  
- `/project:session-end` - End session with comprehensive summary
- `/project:session-list` - List all session files
- `/project:session-current` - Show current session status
- `/project:session-help` - Show this help

### How It Works:

1. Sessions are markdown files in `.claude/sessions/`
2. Files use `YYYY-MM-DD-HHMM-name.md` format
3. Only one session can be active at a time
4. Sessions track progress, issues, solutions, and learnings

### Best Practices:

- Start a session when beginning significant work
- Update regularly with important changes or findings
- End with thorough summary for future reference
- Review past sessions before starting similar work

### Example Workflow:

```
/project:session-start refactor-auth
/project:session-update Added Google OAuth restriction
/project:session-update Fixed Next.js 15 params Promise issue
/project:session-end
```

## Token Optimization

**Expected range**: 200–400 tokens (initial), 50 tokens (cache hit)

**Caching**: Caches static help content — content is invariant and never regenerated.

**Early exit**: Returns immediately from cache on all subsequent calls after the first.

**Patterns used**: Early exit, caching (static content)
