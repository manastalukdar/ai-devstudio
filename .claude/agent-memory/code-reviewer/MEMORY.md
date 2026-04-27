# Code Reviewer — Institutional Memory

Loaded into the agent's context on every invocation. Uses the **Compiled Truth + Timeline** pattern: Compiled Truth holds the current synthesized understanding; Timeline is an append-only evidence trail. Update Compiled Truth in place when findings confirm or contradict it. Prepend new Timeline entries.

---

## Compiled Truth

- Skills are markdown files — review for correct YAML frontmatter (required fields: `name`, `description`, `disable-model-invocation`) and required sections (Token Optimization with concrete estimates, numbered steps, edge cases)
- Install scripts (`install.sh`, `install.py`, `uninstall.sh`, `uninstall.py`) use dynamic skill discovery — no hardcoded arrays; shell scripts must pass `shellcheck` with zero warnings
- Python scripts must follow PEP 8, use type hints, and use f-strings
- No emoji in any file; no AI attribution in any generated content
- Token optimization section is mandatory in every new SKILL.md — reject skills missing it
- `skills/RESOLVER.md` and `skills/conventions/` are structural files, not skills — do not flag them as missing SKILL.md
- The conformance checklist in `/skillify` is the authoritative standard for new skill quality

---

## Timeline

_Prepend new entries here after each review that surfaces a recurring pattern. Format: `- YYYY-MM-DD: <finding>`_
