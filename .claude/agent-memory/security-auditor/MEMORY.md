# Security Auditor — Institutional Memory

This file is loaded into the agent's context on every invocation. It records
security patterns, known clean areas, and past findings for AI DevStudio.

## Project Security Posture

- No external API integrations — pure CLI tooling, no server-side execution
- No authentication or user data handling — no PII concerns
- Primary attack surface: install scripts that write to `~/.claude/skills/`
- Hook scripts receive raw JSON from stdin — validate before parsing in hooks.py
- Skill content is trusted markdown — no code execution within skills themselves

## Known Clean Areas

- No credentials, API keys, or tokens in any tracked file
- No eval(), exec(), or dynamic code execution in Python scripts
- No network calls in hooks (audio player and file I/O only)

## Audit History

_Append codebase-specific security findings here after each audit._
