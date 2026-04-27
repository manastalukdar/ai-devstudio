# Test Runner — Institutional Memory

Loaded into the agent's context on every invocation. Uses the **Compiled Truth + Timeline** pattern: Compiled Truth holds the current synthesized understanding; Timeline is an append-only evidence trail. Update Compiled Truth in place when findings confirm or contradict it. Prepend new Timeline entries.

---

## Compiled Truth

**Project test landscape:**
- No automated test suite — testing is manual: install scripts on supported platforms, skill behavior with Claude Code CLI
- Syntax verification is the primary automated check:
  - `bash -n install.sh` and `bash -n uninstall.sh`
  - `python3 -m py_compile install.py uninstall.py`
  - `python3 -m py_compile .claude/hooks/scripts/hooks.py .claude/hooks/scripts/compact-reminder.py`
  - `shellcheck install.sh uninstall.sh` — must be zero warnings

**Known failure patterns:**
- Dynamic discovery in `install.sh` depends on GitHub raw URL format — must test after any URL changes
- Audio player detection on Linux can fail silently if none of `paplay`/`aplay`/`ffplay` are installed — expected behavior, not a bug
- `shellcheck` behavior may differ between macOS and Linux; CI uses Linux

**Coverage gaps (known):**
- No integration test for skill installation end-to-end
- No test for `install.py --target gemini/codex/cursor/aider` targets
- No test for hook event firing in a real Claude Code session

---

## Timeline

_Prepend new entries here after each test run. Format: `- YYYY-MM-DD: <what was tested and outcome>`_
