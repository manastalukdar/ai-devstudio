# Agent and Command System Architecture Reference

Invoke this command mid-session to restore the full Command → Agent → Skill hierarchy reference.

---

## Three-Layer Architecture

```
Commands (.claude/commands/)
    ↓ orchestrate
Agents (.claude/agents/)
    ↓ use
Skills (skills/ or .claude/skills/)
```

- **Commands**: High-level entry points. Orchestrate agents and skills, manage user interaction, aggregate results.
- **Agents**: Specialized sub-agents with scoped tools and preloaded skills. Run in isolated context.
- **Skills**: Atomic capability units. User-invocable or agent-consumed.

## Current Agents

| Agent | Model | Purpose | Tools |
| --- | --- | --- | --- |
| `code-reviewer` | sonnet | Read-only code quality analysis | Read, Grep, Glob, WebFetch |
| `security-auditor` | sonnet | Vulnerability scanning, OWASP, secrets detection | Read, Grep, Glob, Bash |
| `test-runner` | sonnet | Test execution, failure analysis, TDD enforcement | Read, Bash |
| `claude-md-auditor` | opus | Documentation drift detection and repair | Read, Grep, Glob, Bash, Edit |
| `quality-fixer` | sonnet | Iterative lint/type/shellcheck fix cycles (max 5) | Read, Bash, Edit, Glob, Grep |

## Current Commands

| Command | Purpose |
| --- | --- |
| `quality-pipeline` | Security scan + code review + test suite → combined report |
| `release-workflow` | Validate → changelog → version bump → commit |
| `session-daily` | Daily session start: git status + open TODOs + health summary |
| `architecture/skill-system` | Skill system reference (tiers, YAML fields, token budgets) |
| `architecture/hook-events` | Hook events reference (all 19 events, settings structure) |
| `architecture/agent-command-system` | This file — Command/Agent/Skill hierarchy reference |

## Agent YAML Frontmatter

```yaml
---
name: agent-name
description: When and why to use this agent
tools: Read, Grep, Glob, Bash   # comma-separated, restricts available tools
model: sonnet                    # sonnet | opus | haiku | inherit
color: blue                      # terminal color for agent label
maxTurns: 10                     # optional turn limit
skills:
  - skill-name                   # preloaded skills
hooks:
  PostToolUse:
    - matcher: ".*"
      hooks:
        - type: command
          command: python3 ${CLAUDE_PROJECT_DIR}/.claude/hooks/scripts/hooks.py --agent=<name>
          timeout: 5000
          async: true
---
```

## Persistent Agent Memory

Each agent has a memory directory loaded on every invocation:

```
.claude/agent-memory/
  claude-md-auditor/MEMORY.md
  code-reviewer/MEMORY.md
  security-auditor/MEMORY.md
  test-runner/MEMORY.md
  quality-fixer/MEMORY.md
```

Agents read their MEMORY.md at the start of each session and append new findings after completion. This accumulates institutional knowledge across conversations.

## Agent Design Rules

- Restrict tools to minimum required (read-only agents: `Read`, `Grep`, `Glob` only)
- Never call `Bash(git commit)` from an agent — surface to user via output
- Model choice: `opus` for autonomous complex tasks, `sonnet` for focused analysis
- Fix agents (claude-md-auditor, quality-fixer): always use Edit tool, never commit

## Parallel Agent Pattern

For independent parallel workstreams:

1. Create git worktrees: `git worktree add ../feature-a feature-a`
2. Launch agents in separate tmux panes, each in their worktree
3. Agents communicate via shared state in `.claude/sessions/` — not via bash IPC
4. Use the `Task` tool (not `Bash`) for inter-agent communication
5. Merge results when all agents complete

Implemented by the `/parallel-agents` skill.

## Project-Local Skills (not user-invocable)

```
.claude/skills/
  project-health/SKILL.md    — health check for ai-devstudio itself
  skill-validator/SKILL.md   — validates new skills against project standards
```

These are consumed by agents and commands, hidden from the user skill menu (`user-invocable: false`).
