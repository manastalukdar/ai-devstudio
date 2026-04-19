---
name: docs-sync
description: Sync documentation files with code changes — updates CLAUDE.md, AGENTS.md, README.md, and docs/**/*.md to reflect what actually changed in the codebase. Run after adding features, refactoring, or changing project structure.
disable-model-invocation: false
---

# Documentation Sync

I'll detect what changed in the codebase and surgically update every affected documentation file — CLAUDE.md, AGENTS.md, README.md, and any files under `docs/` or `documentation/` — so docs never drift from code.

## Token Optimization

**Expected range**: 800–2,500 tokens (initial), 100–200 tokens (no-op when docs are already current)

**Patterns used**: Grep-before-Read, git diff scope, early exit, progressive disclosure

**Early exit**: If no relevant code files changed since last doc update (checked via `git diff`), report "docs are current" and stop immediately.

**Caching**: Skips re-reading doc files whose sections haven't changed. Uses `git diff` output to scope work to only affected areas.

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

## Step 2 — Classify Changes

Map each changed file to the documentation areas it may affect:

| Changed file pattern | Potentially affected docs |
|---|---|
| `skills/*/SKILL.md` (new) | README.md skill listing, CLAUDE.md skill count |
| `skills/*/SKILL.md` (modified) | README.md description for that skill |
| `skills/*/SKILL.md` (deleted) | README.md, CLAUDE.md skill count |
| `.claude/agents/*.md` | AGENTS.md agents section, CLAUDE.md |
| `.claude/commands/*.md` | AGENTS.md commands section, CLAUDE.md |
| `.claude/hooks/**` | AGENTS.md hooks section, README.md hooks section |
| `.claude/rules/*.md` | CLAUDE.md rules table |
| `adapters/*.sh` | README.md installation section |
| `install.sh` / `install.py` / `uninstall.*` | README.md installation section |
| `docs/**/*.md` | Nothing (these ARE docs — check for internal cross-refs) |
| `*.py` / `*.ts` / `*.js` / `*.go` / `*.rs` | Relevant `docs/` files if they describe that code |

Use Grep to check which doc files already reference the changed items:

```bash
# For each changed skill/agent/command, check if it's referenced in docs
for item in $CHANGED; do
    basename=$(basename "$item" .md | sed 's/SKILL//')
    grep -rl "$basename" README.md CLAUDE.md AGENTS.md docs/ 2>/dev/null
done
```

## Step 3 — Read Only Affected Sections

Do NOT read entire doc files. Use Grep to locate the exact line ranges that need updating:

```bash
# Find skill listing section in README
grep -n "skill\|Skill" README.md | head -20

# Find skill count references
grep -n "[0-9]\+ skill\|skill.*[0-9]\+" CLAUDE.md AGENTS.md README.md

# Find agent/command tables
grep -n "^| \`\|^| Agent\|^| Command" AGENTS.md README.md
```

Read only those specific sections using offset and limit to minimize token usage.

## Step 4 — Determine Required Updates

For each affected doc, identify the minimal change needed:

**New skill added:**
- README.md: Add one line to the correct tier section's bash block
- CLAUDE.md: Increment skill count (e.g., `99` → `100`)
- AGENTS.md: Update "99 professional skills" references if present

**Skill modified (description changed):**
- README.md: Update the one-line description in the skill listing
- CLAUDE.md: Update description if it appears in the current state summary

**Agent added/modified:**
- AGENTS.md: Update or add row in the agents table
- CLAUDE.md: Update agents list if it appears in the architecture section
- README.md: Update the agents table in Project Infrastructure section

**Command added/modified:**
- AGENTS.md: Update commands section
- README.md: Update commands table in Project Infrastructure section
- CLAUDE.md: Update commands list if referenced

**Hook changed:**
- README.md: Update hooks section if behavior changed
- AGENTS.md: Update hooks system section

**Adapter added/modified:**
- README.md: Update the targets table in the installation section

**Source code changed (`.py`, `.ts`, etc.):**
- Search `docs/` for files that describe the changed module
- Read only those files and update the relevant sections

## Step 5 — Apply Surgical Updates

Use the Edit tool for each change — never rewrite an entire file. Make the smallest edit that brings the doc into sync.

**Naming and count updates:**

If a skill count changed, find all occurrences and update each:

```bash
grep -n "[0-9]\+ skill\|[0-9]\+ professional" CLAUDE.md AGENTS.md README.md
```

Edit each occurrence with the correct count.

**Table row additions/updates:**

Insert or replace exactly one row in the relevant markdown table. Preserve table alignment.

**Skill listing additions:**

Insert exactly one line in the correct section's bash block in README.md. Match surrounding indentation and comment style.

## Step 6 — Verify Cross-References

After all edits, do a quick consistency check:

```bash
# All skill counts should agree
grep -h "[0-9]\+ skill" CLAUDE.md AGENTS.md README.md | sort -u

# No broken links to docs files
grep -roh '\[.*\](\(docs/[^)]*\))' README.md CLAUDE.md AGENTS.md | \
  sed 's/.*(\(.*\))/\1/' | while read f; do
    [[ -f "$f" ]] || echo "BROKEN: $f"
  done
```

If counts disagree or links are broken, fix them before reporting done.

## Step 7 — Report

Summarize changes made:

```
docs-sync complete

Updated:
  README.md          — added docs-sync to Tier 2 skill listing
  CLAUDE.md          — skill count 99 → 100
  AGENTS.md          — no changes needed (count not referenced)

No changes needed:
  docs/skills/       — no matching docs for changed files

Skipped (no relevant changes):
  .claude/agents/    — agent files unchanged
```

## Edge Cases

- **No git repo**: Fall back to scanning for doc files and prompting the user to describe what changed
- **Ambiguous skill tier**: Ask the user which tier before updating README.md
- **Doc file missing**: Note it in the report but do not create it — use `/docs` for new doc creation
- **Conflicting counts**: Report the discrepancy; ask the user which count is correct before writing
- **Large diffs (50+ files)**: Summarize by category rather than processing file-by-file; ask user to confirm scope before editing
