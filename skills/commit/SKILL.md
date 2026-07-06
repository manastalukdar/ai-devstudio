---
name: commit
description: Analyze changes and create meaningful conventional commits with pre-commit quality checks
disable-model-invocation: true
---

# Smart Git Commit

## Absolute Credential Rules

**NEVER violate these — no exceptions:**

- **NEVER run `git config user.name` or `git config user.email`** — do not touch git identity settings
- **NEVER use `--author` to inject any name or email**
- **NEVER add a `Co-Authored-By:` trailer to any commit message**
- **NEVER add `Co-Authored-By: Claude`, `Co-Authored-By: Claude Sonnet`, or any variant with `noreply@anthropic.com`**
- **NEVER include "Generated with Claude Code", "AI-generated", or any AI attribution in the commit message or body**
- **NEVER modify `.git/config` or any git credential file**

The commit must use **only the developer's own git credentials** as already configured in their environment.

**Pre-Commit Quality Checks:** Before committing, verify build, tests, and linter pass (if commands exist in the project).

```bash
# Verify we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not a git repository"
    exit 1
fi

# Early exit if nothing to commit
if git diff --cached --quiet && git diff --quiet; then
    echo "No changes to commit"
    exit 0
fi

echo "Changes detected:"
git status --short
git diff --cached --stat
git diff --stat
```

```bash
# Check for cached commit conventions
CACHE_FILE=".claude/cache/commit/conventions.json"

if [ -f "$CACHE_FILE" ]; then
    LAST_MODIFIED=$(stat -c %Y "$CACHE_FILE" 2>/dev/null || stat -f %m "$CACHE_FILE" 2>/dev/null)
    CURRENT_TIME=$(date +%s)
    AGE=$((CURRENT_TIME - LAST_MODIFIED))
    if [ $AGE -lt 604800 ]; then
        echo "Using cached commit conventions"
    fi
fi
```

```bash
# If nothing is staged, stage modified tracked files
if git diff --cached --quiet; then
    echo "No files staged. Staging modified files..."
    git add -u
fi

git diff --cached --name-status

# Detect commit type from file patterns (cheap grep, no file reads)
CHANGED_FILES=$(git diff --cached --name-only)

if echo "$CHANGED_FILES" | grep -q "test"; then
    TYPE_HINT="test"
elif echo "$CHANGED_FILES" | grep -q "\.md$"; then
    TYPE_HINT="docs"
elif git diff --cached | grep -q "^+.*function\|^+.*class"; then
    TYPE_HINT="feat"
elif git diff --cached | grep -q "^+.*fix\|^+.*bug"; then
    TYPE_HINT="fix"
else
    TYPE_HINT="chore"
fi

# Extract scope from file path (e.g., src/auth/login.ts → auth)
SCOPE=$(echo "$CHANGED_FILES" | head -1 | cut -d'/' -f2)
```

Based on the analysis, create a conventional commit message:
- **Type**: `feat|fix|docs|style|refactor|test|chore` (detected via grep patterns)
- **Scope**: component or area affected (extracted from file paths)
- **Subject**: clear description in present tense, ≤72 characters, imperative mood, no period

```bash
# Create the commit
# Example: git commit -m "fix(auth): resolve login timeout issue"

# Cache conventions for future commits
mkdir -p .claude/cache/commit
cat > .claude/cache/commit/conventions.json <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "common_scopes": ["$SCOPE"],
  "last_type": "$TYPE_HINT",
  "project_patterns": "analyzed"
}
EOF
```

The commit uses only your existing git user configuration. No AI attribution. No emoji.

## Token Optimization

**Expected range**: 300–800 tokens (initial), 200–500 tokens (cache hit), 20–50 tokens (early exit)

**Early exit**: Exits before any analysis if no staged or unstaged changes — 95% savings.

**Caching**: Caches commit conventions (common scopes, preferred types) in `.claude/cache/commit/conventions.json` with a 7-day TTL. Invalidated when `package.json` changes.

**Patterns used**: Bash-based git operations instead of file reads; grep pattern detection for commit type; git diff scope limited to staged changes only; progressive disclosure (stat summary by default, full diff on `--verbose`).
