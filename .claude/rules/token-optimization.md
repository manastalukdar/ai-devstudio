# Token Optimization Rules

## Core Optimization Patterns

Apply these patterns in all skills. Each pattern includes expected savings.

### 1. Grep-before-Read (85-95% savings on file discovery)

```
# Instead of: Read entire files to find relevant sections
# Do: Search for patterns first, read only matching files

Grep pattern="<search term>" path="." glob="*.ts"
# Then Read only the files returned
```

### 2. Glob for Structure (95% savings vs directory walks)

```
# Instead of: ls -la src/ recursively
# Do: Glob pattern="src/**/*.ts"
```

### 3. Early Exit (85-95% savings when condition already met)

Check preconditions before doing work:

```
# Check if tests already pass before analyzing
Bash: npm test --silent 2>&1 | tail -1
# If "All tests passed" → exit with confirmation
```

### 4. Progressive Disclosure (60-85% savings)

Return summary first. Provide details only if user asks:

- Level 1: "Found 3 issues: 2 security, 1 performance" (50 tokens)
- Level 2 (on request): Full issue descriptions (500 tokens)
- Level 3 (on request): Remediation code (2,000 tokens)

### 5. Git Diff Scope Defaults (80-90% savings)

Default to staged changes only, not entire codebase:

```bash
git diff --staged          # staged changes (default)
git diff HEAD              # all uncommitted changes (when requested)
git diff HEAD~1..HEAD      # last commit (when reviewing history)
```

### 6. Bash for System Queries (60-90% savings vs Read)

```bash
# Instead of: Read package.json to find version
# Do:
Bash: node -p "require('./package.json').version"

# Instead of: Read all files to count skills
# Do:
Bash: ls skills/ | wc -l
```

### 7. Caching (70-99% savings on cache hits)

Cache location: `.claude/cache/<skill-name>/`
Cache key: file checksum or timestamp
Default TTL: 7 days

Invalidation triggers:

- `package.json` modified → invalidate dependency cache
- `git pull` detected → invalidate architecture cache
- User runs `/cleanproject` → invalidate all caches

### 8. Template-Based Generation (70-90% savings on scaffolding)

Use fixed templates with variable substitution instead of LLM generation for boilerplate:

```
# Template: skills/scaffold/templates/component.md
# Variables: {{name}}, {{description}}, {{tier}}
# Substitution: sed or Python string replacement
```

### 9. Tiered Model Delegation (40-70% cost reduction)

Route each sub-task to the cheapest model that can handle it, rather than defaulting everything to the primary model.

**Routing heuristic:**

| Task type | Model | Rationale |
|---|---|---|
| File search, grep, list, count | Bash (no model) | Zero tokens |
| Simple edits, boilerplate, renaming | Haiku 4.5 | Cheap, fast |
| Multi-file implementation, standard review | Sonnet 4.6 | Balanced (default) |
| Complex architecture, security audit, deep analysis | Opus 4.8 | Worth the cost |

**Implementation in skills:**

```
# In a skill that spawns subagents, declare model per task:
agent("grep for TODO patterns", { model: "haiku" })     # exploration
agent("implement the fix", {})                           # default (Sonnet)
agent("audit for security regressions", { model: "opus" })  # deep analysis
```

**Expected savings:** 40-70% vs. running all tasks on Opus; 15-40% vs. running all on Sonnet.
Apply to any skill that fans out multiple sub-tasks via the Agent tool or parallel-agents.

### 10. Session State Tracking (70-80% savings on resume)

Store session state in `.claude/sessions/<session-name>.json`:

```json
{
  "last_analyzed": "2026-01-15T10:30:00Z",
  "files_checked": ["src/auth.ts", "src/api.ts"],
  "issues_found": 3,
  "status": "in_progress"
}
```

On resume, read state file first to avoid re-analyzing unchanged files.

## Token Budget Reference

| Skill Tier | Target Range | Acceptable Max |
| --- | --- | --- |
| Core | 300–1,500 | 3,000 |
| Tier 1 | 300–2,000 | 4,000 |
| Tier 2 | 500–4,000 | 8,000 |
| Tier 3 | 1,000–6,000 | 12,000 |

## Mandatory Token Optimization Section

Every skill SKILL.md must include a `## Token Optimization` section:

```markdown
## Token Optimization

**Expected range**: 300–800 tokens (initial), 50–100 tokens (cache hit)

**Caching**: Caches project structure analysis in `.claude/cache/skill-name/`
for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if no staged changes are detected.

**Patterns used**: Grep-before-Read, early exit, git diff scope default
```
