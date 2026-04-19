# Quality Fixer — Institutional Memory

This file is loaded into the agent's context on every invocation. It records
recurring quality issues and fix patterns for AI DevStudio.

## Project Quality Stack

- Python scripts (hooks.py, install.py, uninstall.py, compact-reminder.py):
  - Syntax: `python3 -m py_compile <file>`
  - Linting: `ruff check <file>` if ruff available, else `python3 -m pyflakes <file>`
  - Type check: `mypy <file> --ignore-missing-imports` if mypy available
- Shell scripts (install.sh, uninstall.sh):
  - Lint: `shellcheck <file>` (must pass with zero warnings)
  - Syntax: `bash -n <file>`
- Markdown (SKILL.md, docs): consistent heading hierarchy, fenced code blocks with language id

## Recurring Issues

_Append quality patterns found across multiple fix runs here._

## Fix History

_Append per-run summaries here after each quality fix cycle._
