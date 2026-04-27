# Claude MD Auditor — Institutional Memory

Loaded into the agent's context on every invocation. Uses the **Compiled Truth + Timeline** pattern: Compiled Truth holds the current synthesized understanding; Timeline is an append-only evidence trail. Update Compiled Truth in place when findings confirm or contradict it. Prepend new Timeline entries.

---

## Compiled Truth

- Skill count in `CLAUDE.md` (header and "Current State" section) is the most frequently stale number — must be updated after every batch of new skills
- `AGENTS.md` project identity line mirrors CLAUDE.md and typically lags one update behind
- README.md skill tables are the most complex to check: per-tier counts and the total appear in multiple sections and can diverge independently
- Tier totals must sum exactly: Tier 1 + Tier 2 + Tier 3 + Core = total skill count
- The `skills/` directory is the authoritative source for skill count — always count from filesystem, not from docs
- `skills/RESOLVER.md` and `skills/conventions/` are structural files, not skills — do not count them toward skill totals

---

## Timeline

_Prepend new entries here after each audit run. Format: `- YYYY-MM-DD: <finding>`_
