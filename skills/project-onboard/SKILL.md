---
name: project-onboard
description: Run a structured onboarding interview to generate USER.md and PROJECT.md — capturing developer preferences, project constraints, access policies, and working style so every future agent session starts with full context.
disable-model-invocation: false
---

# Project Onboard

I conduct a focused interview across 6 phases and generate `USER.md` and `PROJECT.md` — persistent context files that every future Claude session loads automatically, eliminating repeated re-explanation of preferences and constraints.

## Token Optimization

**Expected range**: 800–2,000 tokens (full interview), 100 tokens (files already exist and are current)

**Patterns used**: Early exit (files already exist), progressive disclosure (ask one phase at a time), Bash to check existing files

**Early exit**: If `USER.md` and `PROJECT.md` already exist and were updated within 30 days, ask "Want to update them?" before proceeding.

## Step 1 — Check Existing Files

```bash
ls -la USER.md PROJECT.md 2>/dev/null
# Check age
stat -c "%y %n" USER.md PROJECT.md 2>/dev/null
```

If both exist and are recent, show a summary of what they contain and offer to update specific sections rather than re-running the full interview.

## Step 2 — Run the 6-Phase Interview

Ask each phase as a focused block. Wait for the user's response before moving to the next phase.

---

**Phase 1: Developer Identity**
- What is your name and role?
- What languages and frameworks do you work with most?
- How many years of experience do you have?
- Describe your coding style in one sentence (e.g., "pragmatic, tests first, no over-engineering")

**Phase 2: Project Identity**
- What does this project do in one sentence?
- Who are its users?
- What is the primary technology stack?
- What is the current phase? (greenfield / active dev / maintenance / legacy)

**Phase 3: Working Preferences**
- How do you prefer to receive code suggestions? (show diff / show full file / describe change)
- Do you want explanations, or just the code?
- How should ambiguous requirements be handled? (ask / make a choice and note it / list options)
- Are there topics or approaches you want me to avoid?

**Phase 4: Project Constraints**
- Are there any off-limits files, directories, or systems?
- Are there compliance or security requirements?
- Are there performance budgets or SLAs I should know about?
- What external systems does this project integrate with?

**Phase 5: Access Policy**
- Which operations require explicit confirmation before executing? (git push / file deletion / deploy / etc.)
- Which operations can run automatically without asking?
- Are there credentials or secrets handling rules?

**Phase 6: Heartbeat / Calibration**
- What was the last thing that frustrated you about working with an AI assistant?
- What worked really well?
- How should I signal uncertainty? (ask / flag inline / add TODO comment)

---

## Step 3 — Generate USER.md

Write `USER.md` to the project root:

```markdown
# USER.md — Developer Profile
Generated: <date>

## Identity
<name, role, experience level>

## Technical Background
<languages, frameworks, stack>

## Working Style
<preferences from Phase 1 and 3>

## Communication Preferences
<how to present code, handle ambiguity, level of explanation>

## Known Frustrations
<from Phase 6 — what to avoid>

## What Works Well
<from Phase 6 — what to keep doing>
```

## Step 4 — Generate PROJECT.md

Write `PROJECT.md` to the project root:

```markdown
# PROJECT.md — Project Context
Generated: <date>

## What This Project Does
<one sentence>

## Stack
<tech stack>

## Current Phase
<greenfield / active / maintenance / legacy>

## Constraints
<off-limits areas, compliance, performance budgets>

## External Integrations
<systems this project talks to>

## Access Policy
| Operation | Policy |
|---|---|
| git commit | auto |
| git push | confirm |
| file delete | confirm |
| <custom> | <policy> |

## Signals to Watch
<recurring issues, known fragile areas>
```

## Step 5 — Register Files in CLAUDE.md

Check if CLAUDE.md already references these files. If not, note to the user that adding them improves agent context on every session:

```bash
grep -l "USER.md\|PROJECT.md" CLAUDE.md 2>/dev/null
```

## Edge Cases

- **Partial answers**: If the user skips a phase, write `[not provided]` for that section; do not block on missing info
- **Solo project vs. team project**: Adjust Phase 4 questions accordingly (solo = fewer constraints)
- **Sensitive information**: If the user mentions secrets, credentials, or PII, remind them not to commit these files to a public repo
- **Re-run after major change**: If the project phase, stack, or access policy changes significantly, suggest re-running just the affected phases rather than the full interview
