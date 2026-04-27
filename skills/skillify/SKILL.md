---
name: skillify
description: Convert a bug fix, repeated workaround, or solved problem into a permanent, testable Claude Code skill. Runs a 10-item conformance checklist before writing the skill file.
disable-model-invocation: false
---

# Skillify

I'll turn a fix or workaround you just applied into a reusable, permanently documented skill so the same problem never requires manual intervention again.

## Token Optimization

**Expected range**: 500–1,500 tokens (initial), 100–200 tokens (checklist only)

**Patterns used**: Grep-before-Read (check if skill exists), early exit (skill already covers the case), progressive disclosure (checklist summary → full skill draft)

**Early exit**: If an existing skill already covers the pattern, report the skill name and stop.

## Step 1 — Capture the Problem

Ask the user (or infer from conversation context):

1. What was the problem? (one sentence)
2. What was the fix or workaround? (steps taken)
3. How often does this pattern recur? (one-off / occasional / frequent)
4. What should trigger this skill in the future? (keywords, file types, error messages)

If the conversation already contains this context, skip asking and proceed.

## Step 2 — Check for Existing Coverage

```bash
# Search existing skills for overlap before writing a new one
grep -ril "<problem-keyword>" ~/.claude/skills/ 2>/dev/null | head -10
ls skills/ 2>/dev/null
```

If a closely related skill exists, report it and ask whether to:
- Extend the existing skill (preferred)
- Create a new skill (only if the domain is genuinely distinct)

## Step 3 — Run the 10-Item Conformance Checklist

Score each item pass/fail before drafting the skill:

| # | Requirement | Pass/Fail |
|---|---|---|
| 1 | Saves ≥5 minutes of real developer work | |
| 2 | Works without project-specific configuration | |
| 3 | Handles the empty/no-op edge case gracefully | |
| 4 | Output is actionable, not just explanatory | |
| 5 | Under 100 lines of instructions (excluding frontmatter and token section) | |
| 6 | Has YAML frontmatter with `name`, `description`, `disable-model-invocation` | |
| 7 | Has a Token Optimization section with concrete token estimates | |
| 8 | Uses Grep-before-Read where applicable | |
| 9 | Has an early exit for the no-change case | |
| 10 | Description field triggers invocation correctly (specific and action-oriented) | |

If any item fails, fix the draft before writing the file.

## Step 4 — Determine Tier

| Tier | Criteria |
|---|---|
| Tier 1 | Zero config, universally applicable, saves time on first use |
| Tier 2 | Requires some context or setup, applicable to most projects |
| Tier 3 | Specialized domain, complex orchestration, power-user |
| Core | Daily-driver workflow (commit, test, review, session) |

## Step 5 — Draft the Skill

Write the skill following the standard section order:

1. YAML frontmatter
2. One-line purpose statement
3. Token Optimization section
4. Numbered steps with bash blocks
5. Edge cases

Use the fix steps from Step 1 as the basis for the skill's behavior section. Translate imperative past-tense ("I ran X then Y") into present-tense instructions ("Run X, then Y").

## Step 6 — Write the File

```bash
mkdir -p skills/<name>
# Write skills/<name>/SKILL.md
```

Then verify it passes `bash -n` (for any shell blocks) and appears in:

```bash
ls skills/<name>/SKILL.md
```

## Step 7 — Update Skill Counts

If the skill was written to the project skills directory, remind the user to update the counts in CLAUDE.md, README.md, and AGENTS.md, or run `/docs-sync` to propagate the change.

## Edge Cases

- **One-off fix**: If the problem is truly unique, recommend documenting it in a CHANGELOG entry or commit message instead of a skill
- **Tool-specific fix**: If the fix only works with a specific version of a dependency, note that constraint in the skill's Edge Cases section
- **Conflict with existing skill**: If the new skill overlaps significantly with an existing one, propose merging rather than creating a duplicate
