---
name: project-health
description: Internal health check skill for AI DevStudio project. Checks skill count consistency across docs, detects stale sessions, and identifies cache files to clean. Not user-facing.
user-invocable: false
disable-model-invocation: false
---

# Project Health Check Skill

Internal skill used by the `session-daily` command. Checks the health of the AI DevStudio project itself.

## Checks

### 1. Skill Count Consistency

Verify that the skill count (99) is consistent across all documentation files:

```bash
Bash: ls skills/ | wc -l
```

Then check these files reference the correct count:

- `CLAUDE.md`: grep for skill count
- `AGENTS.md`: grep for skill count
- `README.md`: grep for skill count

Report any inconsistencies found.

### 2. Stale Session Files

```bash
Bash: find .claude/sessions/ -name "*.json" -mtime +30 2>/dev/null | wc -l
```

Report count of session files older than 30 days. Suggest running `/cleanproject` if count > 5.

### 3. Cache Size

```bash
Bash: du -sh .claude/cache/ 2>/dev/null || echo "No cache directory"
```

Report cache size. Suggest cleanup if > 50MB.

### 4. Install Script Sync

```bash
Bash: python3 -c "import ast, sys; ast.parse(open('install.py').read()); print('install.py: OK')" 2>&1
Bash: bash -n install.sh 2>&1 && echo "install.sh: OK"
```

Report any syntax errors.

### 5. Documentation Currency

Check that `docs/` modification dates are recent relative to `skills/` changes:

```bash
Bash: git log --oneline -1 -- skills/ docs/
```

## Output Format

```
Project Health: <OK|ISSUES FOUND>

Skill count: N (consistent: yes/no)
Stale sessions: N files
Cache: <size>
Install scripts: OK / <error>
Docs currency: OK / <last updated>
```

## Token Optimization

**Expected range**: 200-500 tokens

**Patterns used**: Bash-based queries, early exit if all checks pass
