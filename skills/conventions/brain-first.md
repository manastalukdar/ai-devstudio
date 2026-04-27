# Brain-First Convention

Before reaching for an external tool, search local context first.

Adapted from [gbrain's brain-first lookup pattern](https://github.com/garrytan/gbrain).

---

## The Rule

**Check local knowledge before external APIs.**

In order:
1. Agent memory (`.claude/agent-memory/<agent>/MEMORY.md`)
2. Project context files (`USER.md`, `PROJECT.md`, `CLAUDE.md`, `AGENTS.md`)
3. Git history (`git log`, `git blame`)
4. Source code (Read / Grep)
5. External APIs or web search (last resort)

## Why

- Local context is faster and free (no API calls)
- Local context is authoritative for this project's conventions and decisions
- External search returns general answers; local context returns project-specific answers
- Avoids re-discovering things already learned in prior sessions

## Application

**When asked about a project decision** (e.g., "why do we use X?"):
1. Grep agent memory for the decision
2. Check CLAUDE.md architecture section
3. Check git log for the commit that introduced X
4. Only then search externally

**When asked about a pattern** (e.g., "how do we do auth here?"):
1. Grep source for the existing pattern
2. Check agent memory for recorded conventions
3. Do not invent a new pattern if one already exists

**When asked about a person or team member**:
1. Check `USER.md` and `PROJECT.md`
2. Check `.claude/agent-memory/` for prior references
3. Do not fabricate information not found locally

## When Brain-First Does Not Apply

- Library/framework documentation: always fetch current docs (training data may be stale)
- Security advisories: always check current CVE databases
- Dependency versions: always check the registry
- When the user explicitly asks to search the web

## Recording New Knowledge

When external lookup is required and yields useful information, record it:
- Project-specific findings → agent memory (Compiled Truth section)
- General patterns → consider `/skillify` to make it reusable
