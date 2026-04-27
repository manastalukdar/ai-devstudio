<!--
 Copyright (c) 2025 Manas Talukdar

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# AI DevStudio - Professional Claude Code Skills

## Project Overview

AI DevStudio is a comprehensive development environment featuring **115 professional skills** for Claude Code CLI that automate repetitive development tasks and save 10-15 hours per week.

Key capability areas: Testing & TDD, CI/CD & DevOps, API Development, Database Management, Security & Code Quality, Debugging & Performance, Git Workflows, Documentation, Code Generation, Session Management, MCP Integration.

## Architecture

### Three-Tier Skill Organization

- **Tier 1** (20 skills): High-impact essentials for immediate productivity
- **Tier 2** (49 skills): Advanced features for professional workflows
- **Tier 3** (16 skills): Power-user tools for specialized capabilities
- **Core** (30 skills): Original foundation skills

### Skill Structure

Each skill lives in `skills/<name>/SKILL.md` with YAML frontmatter. The installer copies all skills to `~/.claude/skills/`. See [`.claude/rules/skill-development.md`](.claude/rules/skill-development.md) for the full YAML field reference and quality standards.

Project-local utility skills (used by agents/commands, not user-invocable) live in `.claude/skills/`.

### Command → Agent → Skill Architecture

- **Commands** (`.claude/commands/`): Entry points that orchestrate agents and skills
- **Agents** (`.claude/agents/`): Specialized sub-agents with scoped tools and preloaded skills
- **Skills** (`skills/` + `.claude/skills/`): Reusable knowledge modules

**Agents**: `code-reviewer`, `security-auditor`, `test-runner`, `claude-md-auditor`, `quality-fixer`

**Architecture reference commands** (invoke mid-session for full reference):
- `/architecture:skill-system` — tiers, YAML fields, naming, token budgets
- `/architecture:hook-events` — all 19 hook events, compact reminder hook
- `/architecture:agent-command-system` — Command/Agent/Skill hierarchy, agent memory

### Persistent Agent Memory

Each agent accumulates institutional knowledge across conversations:

```
.claude/agent-memory/<agent-name>/MEMORY.md
```

Loaded into the agent's context on every invocation. Agents append new findings after completion.

## Auto-Loaded Rules

Detailed guidelines are in `.claude/rules/` (loaded automatically by Claude Code):

| File | Contents |
| --- | --- |
| `skill-development.md` | YAML frontmatter fields, tier organization, quality checklist |
| `git-workflow.md` | Commit rules, credentials policy, branching, checkpoints |
| `code-quality.md` | Language standards, anti-patterns, install script sync rule |
| `token-optimization.md` | 8 optimization patterns, token budgets, caching strategy |

## Critical Safety Rules

**NEVER use Claude or AI credentials for git commits.** All commits must use the developer's own configured git credentials. No AI attribution, no `Co-Authored-By: Claude`, no `git config` modifications.

**NEVER commit without explicit user request.**

**Always create a git checkpoint before destructive operations.**

## Installation

```bash
# Mac/Linux
curl -sSL https://raw.githubusercontent.com/manastalukdar/ai-devstudio/main/install.sh | bash

# Cross-platform
python install.py
```

See [README.md](README.md) for full installation instructions and skill listings.

## Current State

- **Skills**: 115 implemented
- **Token Optimization**: 100% complete — 60-70% average reduction across all skills
- **Tiers**: Tier 1 (20), Tier 2 (49), Tier 3 (16), Core (30)

See [`docs/skills/`](docs/skills/) for full expansion plan and per-batch implementation summaries.

## Usage Patterns

### Typical Development Session

```bash
claude "/session-start feature-name"
claude "/security-scan"
claude "/scaffold component-name"
claude "/session-update Added OAuth integration"
claude "/review"
claude "/test"
claude "/commit"
claude "/session-end"
```

### Quality Assurance Pipeline

```bash
claude "/security-scan" && claude "/review" && claude "/test"
claude "/find-todos" && claude "/fix-todos"
```

## Project Goals

1. Save 10-15 hours/week through 115 professional skills
2. Professional-grade code analysis, security scanning, and accessibility compliance
3. Streamline CI/CD, deployment validation, release automation, and IaC
4. Enforce TDD workflows, mutation testing, and comprehensive test coverage
5. Complete API lifecycle: testing → documentation → contract validation
6. Performance optimization: bundle analysis, profiling, memory leak detection
7. Enable seamless session continuity across Claude conversations
8. Universal compatibility across all technology stacks and frameworks
9. Optimize Claude API costs through intelligent tool usage patterns (60-90% savings)

## Next Steps

- Test skills in real-world projects across different tech stacks
- Create detailed skill reference documentation in `docs/skills-reference/`
- Gather user feedback and usage patterns
- Consider Tier 4+: ML integration, cloud-specific automation, enterprise security

## Development Context

Built upon excellent open-source work — see [README.md Acknowledgements](README.md#acknowledgements) for the full list of attributed projects including CCPlugins, claude-sessions, obra/superpowers, Anthropic Skills, MCP, Boris Cherny's multi-agent patterns, and claude-code-best-practice by shanraisshan.
