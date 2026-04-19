#!/usr/bin/env python3
"""
Compact-aware SessionStart hook for AI DevStudio.

Fires after a context compaction event (SessionStart with trigger=compact).
Outputs a structured codebase reminder so Claude restores critical context
that the compaction window would otherwise lose.

Claude Code injects the stdout of this script as a system message.
"""

REMINDER = """
## AI DevStudio — Post-Compaction Context Restore

You are working in the **AI DevStudio** project. Here is the critical context
you need to continue work after compaction:

### Project Identity
- 99 professional Claude Code skills in `skills/<name>/SKILL.md`
- Three tiers: Tier 1 (16), Tier 2 (37), Tier 3 (16), Core (30)
- Install copies skills to `~/.claude/skills/`

### Critical Safety Rules
- NEVER use AI credentials for git commits — use developer's own git config
- NEVER add `Co-Authored-By: Claude` or any AI attribution to commits
- NEVER commit without explicit user request
- Always create a git checkpoint before destructive operations:
  `git add -A && git stash push -m "checkpoint before <operation>"`

### Key Directories
- `skills/`              — 99 user-invocable skill definitions
- `.claude/agents/`      — specialized sub-agents (code-reviewer, security-auditor, test-runner, claude-md-auditor, quality-fixer)
- `.claude/commands/`    — high-level orchestration commands
- `.claude/rules/`       — auto-loaded rules (skill-development, git-workflow, code-quality, token-optimization)
- `.claude/hooks/`       — hook scripts and JSONL log
- `.claude/agent-memory/` — persistent agent memory across conversations
- `docs/skills/`         — implementation summaries per batch
- `install.sh` / `install.py` — installers using dynamic discovery (no manual array update needed)

### Skill Development Rules
- Each skill: `skills/<name>/SKILL.md` with YAML frontmatter
- Required frontmatter: `name`, `description`, `disable-model-invocation`
- Required sections: Purpose, Usage, Behavior, Examples, Token Optimization, Edge Cases, Safety
- Token budgets: Core 300–1500, Tier 1 300–2000, Tier 2 500–4000, Tier 3 1000–6000
- Under 100 lines of instructions (excluding frontmatter, code blocks, Token Optimization)

### Token Optimization Patterns
1. Grep-before-Read: search first (100 tokens) before reading full files (2000+ tokens)
2. Early exit: check if work is done before starting
3. Progressive disclosure: summary first, details on request
4. Git diff scope: default to `git diff --staged`, not full codebase
5. Bash for system queries vs reading config files

### Commit Message Format
`type(scope): description` — types: feat, fix, docs, refactor, test, chore, ci, perf
No emoji, no AI attribution, imperative mood, max 72 chars subject line.

### Documentation Sync Rule
When skill counts change, update: CLAUDE.md, AGENTS.md, README.md
"""

if __name__ == "__main__":
    print(REMINDER)
