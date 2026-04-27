---
name: briefing
description: Generate a daily development briefing — recent git activity, open TODOs, pending PRs, failing tests, and session context — so you can start work immediately without manually checking multiple sources.
disable-model-invocation: false
---

# Briefing

I compile a structured daily briefing from git history, open issues, TODOs, and session state so you have full situational awareness before writing a single line of code.

## Token Optimization

**Expected range**: 300–800 tokens (all bash queries), 100 tokens (quiet day with no open items)

**Patterns used**: Bash for all data collection, progressive disclosure (summary → details on request), early exit per section (skip empty sections)

**Early exit per section**: If a section has no items (no failing tests, no open TODOs, etc.), omit it from the briefing entirely.

## Step 1 — Collect Data (All Bash)

Run all queries in parallel where possible:

```bash
# Recent activity (last 24h)
git log --oneline --since="24 hours ago" 2>/dev/null | head -10

# Current branch and status
git branch --show-current
git status --short | head -20

# Open TODOs in recently changed files
git diff HEAD~3 --name-only 2>/dev/null | xargs grep -l "TODO\|FIXME\|HACK" 2>/dev/null | head -5

# Test status (if test runner available)
if [ -f "package.json" ]; then
    grep -q '"test"' package.json && echo "npm test available"
fi

# Session state (if session management is active)
ls .claude/sessions/*.json 2>/dev/null | tail -1 | xargs cat 2>/dev/null

# Skill count vs declared
actual=$(ls -d skills/*/ 2>/dev/null | wc -l | tr -d ' ')
declared=$(grep -oP '(?<=Skills\*\*: )\d+' CLAUDE.md 2>/dev/null | head -1)

# USER.md / PROJECT.md presence
ls -la USER.md PROJECT.md 2>/dev/null
```

## Step 2 — Assemble the Briefing

Format output as a scannable briefing card. Omit any section with no items.

```
── Daily Briefing ─────────────────────────────── <date> <time>

Branch: <current-branch>

Recent commits (last 24h):
  <hash> <message>
  ...
  (none — clean day so far)

Status:
  <M file.py>   modified
  <? new.md>    untracked

Open TODOs in active files:
  src/auth.py:42  TODO: handle token expiry edge case
  ...

Session context:
  Last session: <session-name> — <last-updated>
  In progress:  <status from session file>

Project health:
  Skills: <actual> (declared: <declared>)  ✓ consistent / ✗ drift detected

Onboarding context:
  USER.md: present / MISSING — run /project-onboard
  PROJECT.md: present / MISSING

───────────────────────────────────────────────────────────────
Ready. What are we working on today?
```

## Step 3 — Surface One Priority

After the briefing card, suggest one high-priority item based on the data:

- If tests are failing → "Suggest starting with the failing tests"
- If skill count drifts → "Suggest running /docs-sync"
- If active session exists → "Suggest resuming /session-resume <name>"
- If no USER.md → "Suggest running /project-onboard first"
- Otherwise → "No blocking items — ready for new work"

## Edge Cases

- **No git repo**: Skip git sections; note at the top of the briefing
- **No session files**: Omit session context section
- **Large commit history**: Cap at 10 commits regardless; offer `/session-list` for full history
- **CI integration**: If `.github/workflows/` exists and `gh` CLI is available, include last CI run status; otherwise skip
