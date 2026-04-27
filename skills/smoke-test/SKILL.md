---
name: smoke-test
description: Run 8 post-session-start health checks to verify the project is in a working state — git clean, no broken imports, tests pass, key files present, and agent memory intact.
disable-model-invocation: false
---

# Smoke Test

I run 8 quick health checks after starting a session or after a major change to verify the project is in a working state before any serious work begins.

## Token Optimization

**Expected range**: 200–600 tokens (all checks via bash), 50 tokens (all pass, early exit)

**Patterns used**: Bash for all checks (no file reads), early exit (all green), progressive disclosure (pass/fail summary → details on failure only)

**Early exit**: If all 8 checks pass, output a single green summary line and stop.

## The 8 Checks

Run all checks in sequence. Collect results before reporting.

### Check 1 — Git Status Clean

```bash
git status --short
```

**Pass**: No untracked files, no unstaged changes in critical files  
**Fail**: Uncommitted changes in SKILL.md, CLAUDE.md, install scripts, or hooks

### Check 2 — No Merge Conflicts

```bash
grep -rl "<<<<<<< " . --include="*.md" --include="*.ts" --include="*.py" --include="*.sh" 2>/dev/null | grep -v ".git"
```

**Pass**: No output  
**Fail**: List conflicted files

### Check 3 — Installer Syntax Valid

```bash
bash -n install.sh && echo "install.sh OK" || echo "install.sh BROKEN"
python3 -m py_compile install.py && echo "install.py OK" || echo "install.py BROKEN"
```

**Pass**: Both exit 0  
**Fail**: Report which installer is broken

### Check 4 — Skill Directory Structure Intact

```bash
# Every skill directory must contain a SKILL.md
broken=()
for d in skills/*/; do
    [[ -f "${d}SKILL.md" ]] || broken+=("$d")
done
echo "${#broken[@]} broken skill dirs"
[[ ${#broken[@]} -gt 0 ]] && printf '%s\n' "${broken[@]}"
```

**Pass**: 0 broken skill dirs  
**Fail**: List directories missing SKILL.md

### Check 5 — Key Files Present

```bash
for f in CLAUDE.md AGENTS.md README.md install.sh install.py uninstall.sh uninstall.py skills/RESOLVER.md; do
    [[ -f "$f" ]] && echo "  OK  $f" || echo "  MISSING  $f"
done
```

**Pass**: All files present  
**Fail**: List missing files

### Check 6 — Skill Count Consistency

```bash
actual=$(ls -d skills/*/  2>/dev/null | wc -l | tr -d ' ')
declared=$(grep -oP '(?<=Skills\*\*: )\d+' CLAUDE.md | head -1)
echo "Actual: $actual | Declared in CLAUDE.md: $declared"
```

**Pass**: Counts match  
**Fail**: Report the delta; suggest running `/docs-sync`

### Check 7 — Agent Memory Files Present

```bash
for agent in code-reviewer security-auditor test-runner quality-fixer claude-md-auditor; do
    f=".claude/agent-memory/$agent/MEMORY.md"
    [[ -f "$f" ]] && echo "  OK  $agent" || echo "  MISSING  $agent"
done
```

**Pass**: All 5 present  
**Fail**: List missing files; note that the agent will start without institutional memory

### Check 8 — Hooks Script Syntax Valid

```bash
python3 -m py_compile .claude/hooks/scripts/hooks.py && echo "hooks.py OK" || echo "hooks.py BROKEN"
python3 -m py_compile .claude/hooks/scripts/compact-reminder.py && echo "compact-reminder.py OK" || echo "compact-reminder.py BROKEN"
```

**Pass**: Both exit 0  
**Fail**: Report which hook script is broken

## Report Format

```
Smoke test — AI DevStudio

  ✓ Git status clean
  ✓ No merge conflicts
  ✓ Installer syntax valid
  ✓ Skill directory structure intact  (107 skills)
  ✗ Key files present                 — skills/RESOLVER.md missing
  ✓ Skill count consistent
  ✓ Agent memory files present
  ✓ Hooks syntax valid

7/8 passed. 1 issue requires attention.
```

For each failure, append a one-line remediation hint below the summary.

## Edge Cases

- **Not a git repo**: Skip Check 1 and Check 2; note they were skipped
- **No skills/ directory**: Fail Check 4 immediately with "skills/ directory not found — is this the right working directory?"
- **Running after install**: Check 4 and 5 verify the installed state; if running against the repo itself, counts may differ from installed counts — note this
