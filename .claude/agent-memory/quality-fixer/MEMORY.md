# Quality Fixer — Institutional Memory

Loaded into the agent's context on every invocation. Uses the **Compiled Truth + Timeline** pattern: Compiled Truth holds the current synthesized understanding; Timeline is an append-only evidence trail. Update Compiled Truth in place when findings confirm or contradict it. Prepend new Timeline entries.

---

## Compiled Truth

**Quality tool stack:**
- Python (`hooks.py`, `install.py`, `uninstall.py`, `compact-reminder.py`):
  - Syntax: `python3 -m py_compile <file>`
  - Linting: `ruff check <file>` if available, else `python3 -m pyflakes <file>`
  - Type check: `mypy <file> --ignore-missing-imports` if available
- Shell (`install.sh`, `uninstall.sh`):
  - Lint: `shellcheck <file>` — must pass with zero warnings
  - Syntax: `bash -n <file>`
- Markdown (SKILL.md, docs): consistent heading hierarchy, fenced code blocks with language identifier, no trailing whitespace

**Recurring patterns to check first:**
- Missing language identifier on fenced code blocks in SKILL.md files
- `shellcheck` SC2086 (unquoted variable) in shell scripts
- f-string vs `.format()` inconsistency in Python files
- Trailing whitespace in markdown tables

---

## Timeline

_Prepend new entries here after each fix cycle. Format: `- YYYY-MM-DD: <issue found and fixed>`_
