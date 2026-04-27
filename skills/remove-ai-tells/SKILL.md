---
name: remove-ai-tells
description: Remove AI-generated writing patterns from documents — detects filler openers, hedge phrases, cliché transitions, AI vocabulary, and overused intensifiers, then rewrites them to sound natural.
disable-model-invocation: false
---

# Remove AI Tells

I'll scan a document for patterns that signal AI-generated writing and rewrite them to read naturally.

## Token Optimization

**Expected range**: 400–1,200 tokens (initial), 50–100 tokens (early exit when file is clean)

**Patterns used**: Grep-before-Read, early exit, progressive disclosure, git diff scope default

**Early exit**: If none of the grep patterns match, report "No AI tells found" and stop immediately.

## Step 1 — Identify Target File(s)

Resolution order — use the first that yields a valid file:

1. **Explicit argument** — `/remove-ai-tells docs/report.md`
2. **IDE active file** — when running inside the VSCode extension, Claude Code receives the currently opened file as `<ide_opened_file>` context. If that file has a doc extension (`.md`, `.txt`, `.rst`, `.adoc`) and no argument was given, use it automatically.
3. **Staged doc files** — any staged files with a doc extension.
4. **Ask** — if none of the above yield a target, prompt the user.

```bash
# Steps 1 and 3 are bash-resolvable; step 2 is resolved from IDE context.

if [[ -n "$ARGUMENTS" ]]; then
    TARGETS="$ARGUMENTS"
elif [[ -n "$IDE_ACTIVE_FILE" ]] && echo "$IDE_ACTIVE_FILE" | grep -qE '\.(md|txt|rst|adoc)$'; then
    # IDE_ACTIVE_FILE is populated from <ide_opened_file> context when available
    TARGETS="$IDE_ACTIVE_FILE"
    echo "Using IDE active file: $TARGETS"
elif ! git diff --cached --quiet; then
    TARGETS=$(git diff --cached --name-only | grep -E '\.(md|txt|rst|adoc)$')
else
    echo "No target file specified and no staged doc files found."
    echo "Usage: /remove-ai-tells <file>"
    exit 1
fi

echo "Targets: $TARGETS"
```

## Step 2 — Grep for AI-Tell Patterns (Early Exit)

Run all pattern checks before reading any file content. If nothing matches, stop immediately.

```bash
# Filler openers (sentence-start affirmations)
grep -niE "^(Certainly|Absolutely|Of course|Sure,|Great!|Excellent!|Awesome|Wonderful)[,!.]" $TARGETS

# Hedging phrases
grep -niE "(It('s| is) (worth|important) (noting|to note)|Please note that|It should be noted|Note that,)" $TARGETS

# Transition clichés
grep -niE "\b(Moreover,|Furthermore,|Additionally,|In conclusion,|In summary,|That being said,|With that in mind,|Having said that,|At the end of the day,|It goes without saying)" $TARGETS

# AI vocabulary — words/phrases statistically overrepresented in LLM output
grep -niE "\b(delve|leverage[sd]?|utilize[sd]?|facilitate[sd]?|robust(ness)?|seamless(ly)?|holistic(ally)?|synergy|synergize|cutting-edge|state-of-the-art|groundbreaking|transformative|revolutionize|unlock(ing)? (the )?(full |true )?potential|foster(ing)?|empower(ing)?|best practices)\b" $TARGETS

# Self-referential AI phrases
grep -niE "(As an AI|As a language model|As your assistant|I('m| am) here to help|Feel free to (ask|reach out)|Don't hesitate to|I'd be (happy|glad|delighted) to)" $TARGETS

# Padding openers
grep -niE "^(In other words,|To put it simply,|Simply put,|In essence,|Essentially,|Basically,|Ultimately,|Overall,)" $TARGETS

# Excessive affirmative intensifiers
grep -niE "\b(very very|really really|quite (quite|very))\b" $TARGETS

# Em dash overuse — flag any line containing 2+ em dashes, or count total per file
grep -nc "—" $TARGETS | awk -F: '$2 >= 2 {print $1": "$2" em dash(es)"}' || true
# Also flag lines with multiple em dashes on one line
grep -nE ".+—.+—" $TARGETS
```

If zero matches across all patterns, output:

```
No AI tells found in <file>. Document reads naturally.
```

and stop.

## Step 3 — Categorize and Report Findings

Group matches by category and report with line numbers before making any changes:

```
AI tells found in docs/report.md:

Filler openers (2)
  L3:  "Certainly, here is the summary..."
  L47: "Absolutely! The next step is..."

AI vocabulary (5)
  L12: "leverage the existing infrastructure"
  L18: "seamless integration"
  L29: "robust solution"
  L34: "let's delve into the specifics"
  L61: "holistic approach"

Hedge phrases (1)
  L55: "It's worth noting that performance may vary"

Transition clichés (2)
  L40: "Furthermore, this approach..."
  L70: "In conclusion, we recommend..."

Total: 10 patterns across 1 file
```

## Step 4 — Apply Fixes

### Automatic replacements (safe, no ambiguity)

Apply these without asking — the replacement is always better:

| Pattern | Replacement |
|---|---|
| `utilize` | `use` |
| `leverage` (verb) | `use` / `apply` |
| `facilitate` | `help` / `enable` |
| `delve` (any form) | `explore` / `examine` / `investigate` / `look at` |
| `In conclusion,` | *(remove — just end the section)* |
| `In summary,` | *(remove, or keep if it heads a genuine summary block)* |
| `It's worth noting that` | *(remove — just state the thing)* |
| `Please note that` | `Note:` |
| `It should be noted that` | *(remove)* |
| `feel free to` | *(remove)* |
| `don't hesitate to` | *(remove)* |
| `I'd be happy to` | *(remove)* |
| `seamless` | *(remove or replace with specific adjective)* |
| `robust` | *(remove or replace with specific adjective)* |
| `holistic` | `end-to-end` / `full` / *(remove)* |
| `cutting-edge` | *(remove or name the specific technology)* |
| `state-of-the-art` | *(remove or name the specific capability)* |
| `groundbreaking` | *(remove)* |
| `Furthermore,` | *(remove the opener — let the sentence stand alone)* |
| `Moreover,` | *(remove)* |
| `Additionally,` | `Also,` *(or remove)* |
| `That being said,` | *(remove)* |
| `With that in mind,` | *(remove)* |
| `At the end of the day,` | *(remove)* |

Apply all automatic replacements first using Edit, removing the minimal surrounding text.

### Confirmation-required replacements

For these, show the current line and the proposed rewrite, then ask before changing:

- Filler openers (`Certainly!`, `Absolutely!`, etc.) — show the full sentence so the user can see if removing the opener changes meaning
- Em dashes — show each occurrence in context; replace with a comma, colon, or parentheses depending on use, or remove the clause if it is padding. Flag files where em dashes appear more than once per 30 lines as likely overused.
- `leverage` when used as a noun ("leverage over competitors") — may be correct usage
- `best practices` — sometimes the appropriate term for the domain
- Self-referential phrases that may be intentional (e.g., a disclaimer section)
- Any sentence where the replacement changes meaning or register

Example prompt:
```
L3: "Certainly, the migration requires three steps."
     → "The migration requires three steps."
Apply? (y/n/edit)
```

## Step 5 — Report

After all edits:

```
remove-ai-tells complete — docs/report.md

Fixed automatically (8):
  utilize → use (×2)
  delve into → examine (×1)
  Furthermore, → [removed] (×2)
  It's worth noting that → [removed] (×1)
  seamless → [removed] (×1)
  robust → [removed] (×1)

Confirmed by user (2):
  L3  filler opener removed
  L47 filler opener removed

Skipped (0):
  none

Remaining AI tells: 0
```

## Edge Cases

- **Non-doc files**: If the target is a code file, warn that this skill targets human-readable prose, not source code
- **Technical writing where "robust" is accurate**: If context clearly justifies the word (e.g., "RFC 9293 defines robust error recovery"), skip it and note why
- **Non-English content**: Detect via charset/content check; report that patterns are English-only and skip
- **Large files (>500 lines)**: Process in sections; report progress per section
- **Multiple files**: Process each file independently; report a combined summary at the end
- **Legitimate uses of flagged words**: When a flagged word appears in a quote, code block, or heading that is intentionally citing AI output, skip it
