# Test Runner — Institutional Memory

This file is loaded into the agent's context on every invocation. It records
recurring test patterns, failure modes, and coverage gaps for AI DevStudio.

## Project Test Landscape

- No automated test suite currently — testing is manual: install scripts on
  supported platforms, skill behavior with Claude Code CLI.
- Install script verification: `bash -n install.sh` (syntax check) and
  `python3 -m py_compile install.py` (Python syntax).
- Shell script quality: `shellcheck install.sh uninstall.sh` with no warnings.
- Hook script: `python3 -m py_compile .claude/hooks/scripts/hooks.py` and
  `python3 -m pyflakes .claude/hooks/scripts/hooks.py` if pyflakes available.

## Failure Patterns

- Dynamic discovery in `install.sh` depends on GitHub raw URL format — test
  after any install.sh changes that touch the URL construction.
- Audio player detection on Linux can fail silently if none of
  paplay/aplay/ffplay are installed — this is expected behavior.

## Test History

_Append codebase-specific test findings here after test runs._
