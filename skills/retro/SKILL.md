---
name: retro
description: Run a weekly retrospective — what shipped, what broke, what slowed you down, and what to change next week. Produces a dated retro entry and concrete action items.
disable-model-invocation: false
---

# Retro

I'll run a structured weekly retrospective: what shipped, what broke, what patterns to carry forward, and concrete changes for next week. Inspired by gstack's retro skill.

## Token Optimization

**Expected range**: 400–900 tokens (git log + interview), 50 tokens (no activity in window)

**Patterns used**: Bash for git history, progressive disclosure (questions first, synthesis after), early exit (no commits in window)

**Early exit**: If there are no commits in the last 7 days, report "No activity this week" and stop.

## Step 1 — Gather the Week's Data

```bash
# Commits from the last 7 days
git log --oneline --since="7 days ago" --no-merges 2>/dev/null

# Files most changed this week
git diff --stat HEAD~20 HEAD 2>/dev/null | sort -rn | head -10

# Any TODOs or FIXMEs added this week
git diff --since="7 days ago" -S "TODO\|FIXME" --name-only 2>/dev/null | head -10

# Check session files for activity log
ls -lt .claude/sessions/*.json 2>/dev/null | head -5
```

If no commits found, report "Nothing to retro — no commits this week." and stop.

## Step 2 — Four Retro Questions

Ask each question in order. Keep answers brief — one to three sentences each.

---

**What shipped?**
List the things you completed and merged. Use the git log as a prompt if needed.

**What broke or slowed you down?**
What took longer than expected? What broke unexpectedly? What required repeated attempts?

**What pattern do you want to carry into next week?**
Something that worked well — a workflow, a tool, an approach — that you want to do more of.

**What is the one change you will make next week?**
One concrete, specific change. Not "be more careful" — something you can act on Monday morning.

---

## Step 3 — Produce the Retro Entry

Write a dated entry to `.claude/retros/YYYY-MM-DD.md`:

```markdown
# Retro — YYYY-MM-DD

## Shipped
- <item>
- <item>

## Broke / Slowed Down
- <item>

## Pattern to Carry Forward
<one sentence>

## One Change for Next Week
<one concrete action>

## Commit Activity
<count> commits across <N> files
Most active: <top 3 files>
```

```bash
mkdir -p .claude/retros
# Write the entry
```

## Step 4 — Surface Action Items

Extract any concrete next-week commitments and print them as a checklist:

```
Next week:
  [ ] <action from Q4>
  [ ] <any fix mentioned in Q2 that is still open>
```

## Step 5 — Update Learnings (if /learn is available)

If any pattern or anti-pattern surfaced that should persist beyond this week, suggest running `/learn add "<pattern>"` to record it.

## Edge Cases

- **First retro**: No prior retros to compare against; just run it fresh
- **Sparse week**: A short retro is still useful — ship it even with one item per section
- **Multiple engineers**: Ask each person's answers separately before synthesizing; credit them by name in the entry
- **Old retros**: Running `/retro --list` shows all past entries; `/retro --show 2026-04-20` opens a specific one
