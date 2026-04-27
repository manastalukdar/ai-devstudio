---
name: learn
description: Record, list, search, and apply cross-session learnings — capture insights from completed work as JSONL entries so patterns persist across conversations and accumulate into institutional knowledge. Inspired by gstack's learn skill.
disable-model-invocation: false
---

# Learn

I'll capture insights from this session as persistent JSONL learnings so patterns accumulate into institutional knowledge across conversations. Inspired by gstack's learn skill.

## Token Optimization

**Expected range**: 50–200 tokens per operation

**Patterns used**: Bash for JSONL read/write, Grep for search, early exit (file not found for list/search)

**Early exit**: For `list` and `search`, if no learnings file exists, report "No learnings recorded yet" and stop.

## Storage

All learnings are stored in `.claude/learnings.jsonl` — one JSON object per line:

```json
{"id": "uuid", "date": "2026-04-27", "category": "testing", "learning": "Always run a single test file before the full suite to catch import errors early.", "tags": ["testing", "debugging"], "source": "session"}
```

## Usage

```bash
/learn add "Always run a single test file before the full suite"   # record a learning
/learn add "Use --force-with-lease instead of --force" --tag git   # with tag
/learn list                                                         # show all learnings
/learn list --tag git                                               # filter by tag
/learn search "force push"                                          # keyword search
/learn apply                                                        # surface relevant learnings for current context
/learn remove <id>                                                   # delete a learning by ID
```

## Step 1 — add

```bash
mkdir -p .claude
LEARNING_FILE=".claude/learnings.jsonl"
DATE=$(date '+%Y-%m-%d')
ID=$(python3 -c "import uuid; print(str(uuid.uuid4())[:8])")
CATEGORY="${CATEGORY:-general}"

# Build JSON entry
ENTRY=$(python3 -c "
import json, sys
entry = {
    'id': '$ID',
    'date': '$DATE',
    'category': '$CATEGORY',
    'learning': sys.argv[1],
    'tags': ['$TAG'] if '$TAG' else [],
    'source': 'manual'
}
print(json.dumps(entry))
" "$LEARNING_TEXT")

echo "$ENTRY" >> "$LEARNING_FILE"
echo "✓ Learning recorded [ID: $ID]"
echo "  $LEARNING_TEXT"
```

Auto-detect category from content keywords:
- "test", "spec", "mock" → `testing`
- "git", "commit", "branch", "push" → `git`
- "performance", "slow", "speed", "cache" → `performance`
- "security", "auth", "token", "secret" → `security`
- "api", "endpoint", "http", "curl" → `api`
- default → `general`

## Step 2 — list

```bash
LEARNING_FILE=".claude/learnings.jsonl"

if [ ! -f "$LEARNING_FILE" ]; then
    echo "No learnings recorded yet."
    echo "Use: /learn add \"your insight here\""
    exit 0
fi

# Filter by tag if provided
if [ -n "$TAG" ]; then
    grep "\"$TAG\"" "$LEARNING_FILE"
else
    cat "$LEARNING_FILE"
fi | python3 -c "
import json, sys
entries = [json.loads(l) for l in sys.stdin if l.strip()]
for e in sorted(entries, key=lambda x: x['date'], reverse=True):
    print(f\"[{e['id']}] {e['date']} ({e['category']}) — {e['learning'][:80]}\")
print(f'\n{len(entries)} learnings total')
"
```

## Step 3 — search

```bash
LEARNING_FILE=".claude/learnings.jsonl"
QUERY="$1"

grep -i "$QUERY" "$LEARNING_FILE" | python3 -c "
import json, sys
entries = [json.loads(l) for l in sys.stdin if l.strip()]
for e in entries:
    print(f\"[{e['id']}] {e['date']} — {e['learning']}\")
print(f'\n{len(entries)} match(es) for: $QUERY')
"
```

## Step 4 — apply

Surface learnings relevant to the current working context:

```bash
# Detect current context signals
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
RECENT_FILES=$(git diff --name-only HEAD~3 2>/dev/null | head -10)
STAGED=$(git diff --cached --name-only 2>/dev/null | head -5)

# Extract keywords from context
CONTEXT_KEYWORDS=$(echo "$BRANCH $RECENT_FILES $STAGED" | tr '/' ' ' | tr '-' ' ')

# Search learnings for each keyword
for KEYWORD in $CONTEXT_KEYWORDS; do
    [ ${#KEYWORD} -lt 4 ] && continue  # skip short words
    grep -i "$KEYWORD" .claude/learnings.jsonl 2>/dev/null
done | sort -u | python3 -c "
import json, sys
entries = set()
for l in sys.stdin:
    try:
        e = json.loads(l.strip())
        entries.add((e['id'], e['learning']))
    except: pass
if entries:
    print('Relevant learnings for this context:')
    for id_, learning in list(entries)[:5]:
        print(f'  [{id_}] {learning}')
else:
    print('No relevant learnings found for current context.')
"
```

## Step 5 — remove

```bash
ID="$1"
LEARNING_FILE=".claude/learnings.jsonl"

# Show the entry first
grep "\"id\": \"$ID\"" "$LEARNING_FILE" | python3 -c "import json,sys; e=json.loads(sys.stdin.read()); print(f\"Remove: {e['learning']}? [y/N]\")"

# On confirmation: filter out the entry
python3 -c "
import json, sys
entries = [json.loads(l) for l in open('$LEARNING_FILE') if l.strip()]
kept = [e for e in entries if e['id'] != '$ID']
with open('$LEARNING_FILE', 'w') as f:
    for e in kept:
        f.write(json.dumps(e) + '\n')
print(f'Removed [{\"$ID\"}] — {len(kept)} learnings remain')
"
```

## Integration with /retro

At the end of a `/retro` session, any pattern surfaced in Step 5 ("Carry Forward") can be recorded:

```
/learn add "Run smoke-test after every skill addition to catch count drift"  --tag workflow
```

## Edge Cases

- **Duplicate learning**: before adding, check if a very similar learning exists (Levenshtein > 80% match); warn but allow
- **Long learning text**: truncate display to 80 chars; store full text in JSONL
- **Corrupted JSONL**: skip malformed lines; report "N lines skipped (malformed)"
- **Empty file**: treat same as missing file
- **apply with no git**: fall back to current directory name and file types as context signals
