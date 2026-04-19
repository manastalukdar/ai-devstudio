# Claude MD Auditor — Institutional Memory

This file is loaded into the agent's context on every invocation. It records
recurring drift patterns and past corrections for the AI DevStudio project.
Append new entries after each audit run.

## Known Drift Patterns

- Skill count in `CLAUDE.md` (header and "Current State" section) is the most
  frequently stale number — update after every batch of new skills.
- `AGENTS.md` project identity line ("99 professional skills") mirrors CLAUDE.md
  and often lags one update behind.
- README.md skill tables are the most complex to check: there are per-tier tables
  and the total count appears multiple times in different sections.
- Tier totals must sum to the total skill count: Tier 1 + Tier 2 + Tier 3 + Core = total.

## Audit History

_Append entries here after each audit using the format shown in the agent instructions._
