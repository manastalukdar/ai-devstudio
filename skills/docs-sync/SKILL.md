---
name: docs-sync
description: Sync documentation files with code changes — detects what changed, finds affected docs, and applies surgical updates so docs never drift from code. Works in any repo.
disable-model-invocation: false
---

# Documentation Sync

I'll detect what changed in the codebase and surgically update every affected documentation file — README, CHANGELOG, API docs, architecture docs, and any files under `docs/` or `documentation/` — so docs never drift from code.

## Token Optimization

**Expected range**: 800–2,500 tokens (initial), 100–200 tokens (no-op when docs are already current)

**Patterns used**: Grep-before-Read, git diff scope, early exit, progressive disclosure

**Early exit**: If no code files changed since the last doc update, report "docs are current" and stop immediately.

## Step 1 — Detect Changed Files

```bash
# Use staged changes if available, otherwise last commit, otherwise working tree
if ! git diff --cached --quiet; then
    CHANGED=$(git diff --cached --name-only)
    SCOPE="staged changes"
elif [[ -n "$ARGUMENTS" ]]; then
    # Support: /docs-sync HEAD~3..HEAD or /docs-sync <commit>
    CHANGED=$(git diff --name-only $ARGUMENTS)
    SCOPE="$ARGUMENTS"
else
    CHANGED=$(git diff HEAD~1 --name-only 2>/dev/null || git diff --name-only)
    SCOPE="last commit"
fi

echo "Scope: $SCOPE"
echo "$CHANGED"
```

If no files changed, report "Nothing to sync" and stop.

## Step 2 — Discover Documentation Files

Scan the repo for doc files without reading them:

```bash
# Find all markdown/rst/txt documentation files
find . -type f \( -name "*.md" -o -name "*.rst" -o -name "*.txt" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/vendor/*" \
  | sort

# Identify the main docs: README, CHANGELOG, API docs, architecture docs
ls README* CHANGELOG* CONTRIBUTING* LICENSE* 2>/dev/null
ls docs/ documentation/ 2>/dev/null
```

## Step 3 — Map Changed Code to Affected Docs

For each changed code file, find which doc files reference it by name, module, or path:

```bash
for file in $CHANGED; do
    # Extract meaningful name tokens (filename without extension, parent directory)
    name=$(basename "$file" | sed 's/\.[^.]*$//')
    dir=$(dirname "$file" | xargs basename)

    # Search for references in doc files
    grep -rl "$name\|$dir" \
      $(find . -name "*.md" -not -path "*/.git/*" -not -path "*/node_modules/*") \
      2>/dev/null
done | sort -u
```

General mapping rules (adapt to what you find in the repo):

| Type of change | Likely affected docs |
|---|---|
| New public function / class / module | README usage section, API reference, relevant `docs/` page |
| Renamed / removed symbol | Any doc that mentions the old name |
| New CLI flag or config option | README, config reference docs |
| Dependency added / removed | README installation section, CONTRIBUTING setup guide |
| New file in a documented directory | README file listing or architecture doc |
| Bug fix with user-visible behavior change | CHANGELOG, README caveats |
| Breaking change | CHANGELOG, README migration section, CONTRIBUTING |

## Step 4 — Read Only Affected Sections

Do NOT read entire doc files. Use Grep to find the exact lines that need updating:

```bash
# Find the section that mentions the changed item
grep -n "<item-name>" <doc-file> | head -20

# Find version or count references that may need updating
grep -n "v[0-9]\+\.[0-9]\+\|[0-9]\+ feature\|[0-9]\+ command" README.md

# Find installation or setup sections
grep -n "^## Install\|^## Setup\|^## Getting Started" README.md
```

Read only the relevant line ranges (use offset + limit).

## Step 5 — Determine Required Updates

For each affected doc, identify the minimal change:

**New public API (function, class, endpoint):**
- Add one entry to the relevant section in README or API docs
- Add a CHANGELOG entry if the project uses one

**Renamed or removed:**
- Update every occurrence of the old name
- Add a deprecation/migration note if the project has a migration guide

**New CLI flag or config key:**
- Add one row to the relevant options table
- Update any example commands that show related flags

**Dependency change:**
- Update installation commands in README if the install step changed
- Update minimum version requirements if they changed

**Breaking change:**
- Add a CHANGELOG entry under the correct version heading
- Add a migration note in README or a dedicated migration doc

## Step 6 — Apply Surgical Updates

Use the Edit tool for each change — never rewrite an entire file. Make the smallest edit that brings the doc into sync.

```bash
# Before editing, verify the exact text to replace
grep -n "<old-text>" <doc-file>
```

Then apply each edit with the Edit tool, preserving surrounding formatting (table alignment, list indentation, heading levels).

## Step 7 — Verify Consistency

After all edits, do a quick sanity check:

```bash
# Check that renamed items no longer appear under old names
grep -r "<old-name>" docs/ README.md 2>/dev/null

# Check for broken relative links
grep -oh '\[.*\]([^)#]*)' README.md docs/**/*.md 2>/dev/null \
  | sed 's/.*(\(.*\))/\1/' \
  | while read f; do
      [[ -f "$f" ]] || echo "BROKEN LINK: $f"
    done
```

Fix any remaining references before reporting done.

## Step 8 — Report

```
docs-sync complete

Scope: last commit (3 files changed)

Updated:
  README.md          — added myFunction to API reference section
  docs/api.md        — added parameter description for --verbose flag
  CHANGELOG.md       — added entry under [Unreleased]

No changes needed:
  docs/architecture.md — no references to changed files
  CONTRIBUTING.md      — setup instructions unchanged

Skipped (doc-only changes, no code drift):
  docs/guides/tutorial.md
```

## Edge Cases

- **No git repo**: Prompt the user to describe what changed; then scan all doc files for likely affected sections
- **No existing docs**: Note which doc files are missing; suggest creating them with `/docs` but do not create them automatically
- **Ambiguous section**: If multiple doc sections could apply, list them and ask the user to confirm before editing
- **Large diffs (50+ files)**: Summarize by change category; ask the user to confirm scope before editing
- **Generated docs** (e.g., from JSDoc, Sphinx, rustdoc): Note that they need to be regenerated rather than hand-edited; skip them and report
- **CHANGELOG format varies**: Detect the format (Keep a Changelog, simple bullet list, etc.) from existing entries before adding new ones
