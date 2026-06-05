---
name: continuous-learning
description: Extract repeated patterns from archived sessions and offer to convert them into reusable skills
disable-model-invocation: false
risk: safe
---

# Continuous Learning

Scan archived session logs to surface recurring manual workflows, then offer to convert high-frequency patterns into new SKILL.md stubs so repeated work becomes permanent automation.

## Usage

```
/continuous-learning              # Scan all archived sessions for patterns
/continuous-learning --min 2      # Lower threshold (default: 3 repetitions)
/continuous-learning --generate   # Auto-generate stubs without prompting
```

## Behavior

### Phase 1: Discover sessions

```bash
# Find all archived session files (not the active .current-session pointer)
find .claude/sessions -name "*.md" -not -name ".current-session" 2>/dev/null | sort
```

If fewer than 3 session files exist, report "Not enough session history yet (need 3+)" and exit.

### Phase 2: Extract commands and workflows

Scan each session file for lines that match invocation patterns:

```bash
# Commands invoked (slash commands, skill names)
grep -h -E "^/[a-z]|^\*\*Command\*\*:|Ran:|Invoked:" .claude/sessions/**/*.md 2>/dev/null \
  | sed 's|.*: ||' | sort | uniq -c | sort -rn | head -40
```

Also extract multi-step sequences: look for clusters of 3+ consecutive commands that appear together in at least `--min` sessions.

### Phase 3: Build pattern registry

Load or create `.claude/cache/continuous-learning/patterns.json`:

```json
{
  "last_scan": "2026-06-04T00:00:00Z",
  "patterns": [
    {
      "commands": ["/security-scan", "/review", "/test"],
      "frequency": 5,
      "sessions": ["session-a.md", "session-b.md"],
      "candidate_name": "quality-gate"
    }
  ]
}
```

Merge new findings with prior registry. Patterns that drop below `--min` threshold are removed.

### Phase 4: Present findings

Display a ranked table of patterns that meet the threshold:

```
Repeated patterns found across your sessions:

  Rank  Frequency  Pattern
  ────  ─────────  ───────────────────────────────────────────
  1     7x         /security-scan → /review → /test
  2     5x         /find-todos → /fix-todos → /commit
  3     4x         /db-diagram → /migration-generate → /seed-data
  4     3x         /brainstorm → /write-plan → /implement

Convert any of these to a skill? (enter rank, or 'none'):
```

### Phase 5: Generate skill stub (if requested)

For the chosen pattern, emit a SKILL.md stub using the skillify template:

```markdown
---
name: <candidate-name>
description: <inferred one-line description>
disable-model-invocation: false
risk: safe
---

# <Title>

## Usage

\`/<candidate-name>\`

## Behavior

1. Run `/step-one`
2. Run `/step-two`
3. Run `/step-three`

## Token Optimization

**Expected range**: 200–600 tokens (delegates to constituent skills)
**Early exit**: Each constituent skill handles its own early exit.
**Patterns used**: Delegation to existing skills
```

Save to `skills/<candidate-name>/SKILL.md` and confirm location to user. Do not commit.

## Examples

**No patterns yet:**
```
/continuous-learning
→ Scanned 2 session files — need at least 3 to detect patterns.
  Run more sessions, then try again.
```

**Patterns found:**
```
/continuous-learning
→ Scanned 8 sessions. Found 3 repeated patterns (threshold: 3x).
  [table shown]
  Convert #1 to a skill? → User enters "1"
  → Stub written: skills/quality-gate/SKILL.md
```

## Token Optimization

**Expected range**: 400–900 tokens (initial scan), 150–300 tokens (cache hit)

**Caching**: Stores pattern registry in `.claude/cache/continuous-learning/patterns.json`. On subsequent runs, only sessions newer than `last_scan` are re-processed; old results are merged from cache.

**Early exit**: Exits immediately if fewer than 3 archived session files exist.

**Patterns used**: Grep-before-Read (scan with grep, never read full session files into context), Bash for system queries, progressive disclosure (summary table before detail), early exit.

## Edge Cases

- **No sessions directory**: Reports setup instructions and exits.
- **Sessions with no command lines**: Skips those files silently.
- **Candidate name collision with existing skill**: Appends `-2` suffix and warns user.
- **User declines all patterns**: Exits cleanly with "Nothing converted."

## Safety

- Never deletes or modifies existing skills or session files.
- Skill stubs are written to `skills/` only — not installed to `~/.claude/skills/` automatically.
- Does not commit anything; user must run `/commit` explicitly.
