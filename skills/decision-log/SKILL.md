---
name: decision-log
description: Record architectural and design decisions as structured ADR files in docs/decisions/, with auto-indexing and link suggestions to related decisions
disable-model-invocation: false
risk: safe
---

# Decision Log

Persist design and architectural decisions as ADR (Architecture Decision Record) files.

Arguments: `$ARGUMENTS` - decision title or description, or `list` to show all decisions, or `search <term>` to find related decisions

## Behavior

### 1. Route by Mode

```bash
# Detect mode from arguments
if [[ "$ARGUMENTS" == "list" ]]; then
  ls -t docs/decisions/*.md 2>/dev/null | head -20 || echo "No decisions recorded yet."
  exit 0
fi

if [[ "$ARGUMENTS" == search* ]]; then
  TERM="${ARGUMENTS#search }"
  grep -rn "$TERM" docs/decisions/ 2>/dev/null | head -20
  exit 0
fi
```

### 2. Initialize Decisions Directory

```bash
mkdir -p docs/decisions

# Check for existing ADRs to get next sequence number
LAST=$(ls docs/decisions/*.md 2>/dev/null | grep -o '[0-9]\{4\}' | sort -n | tail -1)
NEXT=$(printf "%04d" $(( ${LAST:-0} + 1 )))
DATE=$(date +%Y-%m-%d)
```

### 3. Generate ADR File

Filename: `docs/decisions/NNNN-<slugified-title>.md`

```markdown
# NNNN. [Decision Title]

**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Rejected | Deprecated | Superseded by [NNNN]
**Deciders**: [names or teams]

## Context

[What is the issue motivating this decision? What forces are at play — technical, business, schedule?
Include relevant constraints. 2-4 sentences.]

## Decision

[The change being proposed or that was made. State it as a full sentence starting with "We will..."]

## Alternatives Considered

### Option A: [Name] (chosen)
- Pros: ...
- Cons: ...

### Option B: [Name]
- Pros: ...
- Cons: ...
- Reason rejected: ...

## Consequences

**Positive**: [benefits that follow from this decision]

**Negative**: [tradeoffs, risks, or things that become harder]

**Neutral**: [side effects that are neither good nor bad]

## Related Decisions
[Links to superseded or related ADRs]
```

### 4. Update Index

```bash
# Maintain docs/decisions/README.md as an index
INDEX="docs/decisions/README.md"

if [ ! -f "$INDEX" ]; then
  echo "# Decision Log" > "$INDEX"
  echo "" >> "$INDEX"
  echo "| # | Title | Status | Date |" >> "$INDEX"
  echo "|---|-------|--------|------|" >> "$INDEX"
fi

# Append new entry
echo "| $NEXT | [$TITLE]($FILENAME) | Proposed | $DATE |" >> "$INDEX"
```

### 5. Link Suggestions

After creating the ADR, search for related decisions:
```bash
# Find thematically related decisions
KEYWORDS=$(echo "$ARGUMENTS" | tr ' ' '\n' | grep -v '^.\{,3\}$')  # words > 3 chars
for kw in $KEYWORDS; do
  grep -li "$kw" docs/decisions/*.md 2>/dev/null
done | sort -u | grep -v "$FILENAME"
```

Report: "Related decisions that may be relevant: [list]"

### 6. Git Checkpoint

```bash
# Stage the new ADR (do not commit — user must explicitly request)
git add docs/decisions/
echo "ADR staged. Review with: git diff --staged"
echo "Commit with: git commit -m 'docs(decisions): add $NEXT - $TITLE'"
```

## Examples

```
/decision-log "use PostgreSQL instead of MongoDB for primary storage"
/decision-log "adopt event sourcing for the orders domain"
/decision-log list
/decision-log search authentication
```

## Output

```
Decision recorded: docs/decisions/0007-use-postgresql-for-primary-storage.md
Index updated:     docs/decisions/README.md

Related decisions:
  0003-database-connection-pooling.md
  0005-orm-selection.md

Staged for commit. Review: git diff --staged
```

## Token Optimization

**Expected range**: 200–500 tokens (new decision), 100–200 tokens (list/search)

**Early exit**: `list` and `search` modes return immediately from filesystem without LLM generation.

**Bash for system queries**: Uses `ls` and `grep` to find sequence numbers and related files — no file reads needed.

**Patterns used**: Early exit, Bash for system queries, template-based generation
