# Security Auditor — Institutional Memory

Loaded into the agent's context on every invocation. Uses the **Compiled Truth + Timeline** pattern: Compiled Truth holds the current synthesized understanding; Timeline is an append-only evidence trail. Update Compiled Truth in place when findings confirm or contradict it. Prepend new Timeline entries.

---

## Compiled Truth

**Project security posture:**
- Pure CLI tooling — no server-side execution, no external API integrations, no PII handling
- Primary attack surface: install scripts that write to `~/.claude/skills/` and `~/.claude/commands/`
- Hook scripts receive raw JSON from stdin — validate structure before parsing in `hooks.py`
- Skill content is trusted markdown — no code execution within skills themselves
- No credentials, API keys, or tokens in any tracked file (confirmed)
- No `eval()`, `exec()`, or dynamic code execution in Python scripts (confirmed)
- No network calls in hook scripts (file I/O and local audio player only)

**Known clean areas (skip deep scan):**
- `skills/*/SKILL.md` — markdown only, no executable content
- `docs/` — documentation only
- `.claude/agent-memory/` — memory files, no executable content

**Areas requiring scan on every audit:**
- `install.sh`, `uninstall.sh` — writes to home directory; check for path traversal
- `.claude/hooks/scripts/hooks.py` — parses stdin JSON; check for injection
- Any new file in `scripts/` or `adapters/`

---

## Timeline

_Prepend new entries here after each security audit. Format: `- YYYY-MM-DD: <finding or confirmed-clean>`_
