<!--
 Copyright (c) 2025 Manas Talukdar

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# AGENTS.md - AI Agent Guidelines for AI DevStudio

## Purpose

This document provides guidelines for AI assistants (particularly Claude Code) when working with the AI DevStudio project. It ensures consistent, safe, and effective collaboration between human developers and AI agents.

## Project Identity

**AI DevStudio** is a professional development environment that extends Claude Code CLI with 128 professional skills across 4 tiers for automated workflows, code quality analysis, and session management.

**Core Philosophy**: Time-saving automation with safety-first design and professional-grade code quality.

**Format**: All skills follow the [official Claude Skills format](https://code.claude.com/docs/en/skills) with YAML frontmatter and the [Agent Skills](https://agentskills.io) open standard. Each skill resides in `skills/skill-name/SKILL.md`.

## Critical Safety Rules

### 1. Git Credentials and Commits

**ABSOLUTE REQUIREMENT**: Never use Claude or AI credentials for git commits.

- ✅ **CORRECT**: All commits must use the developer's configured git credentials
- ❌ **NEVER**: Use "Claude Sonnet 4.5 <noreply@anthropic.com>" or any AI identity
- ❌ **NEVER**: Include "Co-Authored-By: Claude" or similar AI attribution in commits
- ❌ **NEVER**: Modify git config to set AI credentials

**Rationale**: Commits represent legal authorship and accountability. AI assistants are tools, not authors.

### 2. File Operations

- Always read files before editing or writing
- Use Edit tool for existing files, Write tool only for genuinely new files
- Preserve existing code style, formatting, and conventions
- Never create unnecessary documentation files unless explicitly requested

### 3. Skill Development

- All skills are in the `skills/` directory, each in its own subdirectory
- Each skill has a `SKILL.md` file (uppercase) with YAML frontmatter
- Skills must be self-contained with clear instructions
- Test skills thoroughly before marking as complete
- Follow the official Claude Skills format structure

## Development Workflows

### Working with Skills

1. **Reading Skills**: Use `Read` tool to examine `skills/skill-name/SKILL.md` files
2. **Creating Skills**:
   - Create directory in `skills/skill-name/`
   - Create `SKILL.md` with proper YAML frontmatter
   - Follow the template structure from existing skills
3. **Testing Skills**: Verify skill syntax and behavior before committing
4. **Documentation**: Update README.md and CLAUDE.md when adding/modifying skills

### Installation Scripts

- `install.py` and `install.sh` must be kept in sync
- `uninstall.py` and `uninstall.sh` must be kept in sync
- Installation copies from `skills/` to `~/.claude/skills/`
- Uninstallation removes from `~/.claude/skills/` (and legacy `~/.claude/commands/` if present)
- Test installation on multiple platforms when possible
- `install.sh` and `uninstall.sh` use dynamic discovery via the GitHub API — no manual array update needed when adding new skills
- Verify dynamic discovery works after adding a new skill: `ls skills/<new-skill>/SKILL.md`

### Session Management

Skills in the `session-*` family require special attention:

- Must integrate with `.claude/sessions/` directory structure
- Should preserve full context and history
- Must handle edge cases (no active session, corrupt session files, etc.)
- Follow the patterns established in `docs/session-management/sessions.md`

## Code Quality Standards

### Style and Formatting

- **Python**: Follow PEP 8, use type hints where beneficial
- **Shell Scripts**: Use shellcheck-compliant syntax
- **Markdown**: Use consistent formatting, proper headers, code blocks
- **Commands**: Clear structure with purpose, usage, examples, and edge cases

### Documentation

- Keep README.md as the primary user-facing documentation
- Use CLAUDE.md for project context and memory
- Use AGENTS.md (this file) for AI interaction guidelines
- Update CONTRIBUTING.md for contributor workflows

### Testing

- Manually test installation scripts on supported platforms
- Verify command behavior with Claude Code CLI
- Test edge cases and error handling
- Ensure backwards compatibility when modifying existing commands

## Skill Development Guidelines

### Skill Structure

Each skill must be in its own directory with a `SKILL.md` file (uppercase) that includes YAML frontmatter followed by markdown content:

```markdown
---
name: skill-name
description: Clear description of what it does and when to use it
disable-model-invocation: false  # true for manual-only skills
---

# Skill Name

## Purpose
Clear one-line description

## Usage
How to invoke the skill

## Behavior
Step-by-step process

## Examples
Real-world use cases

## Edge Cases
How to handle errors and unusual situations

## Safety Considerations
Any risks or precautions
```

**YAML Frontmatter Fields**:

- `name`: Skill name (lowercase, hyphens, max 64 chars)
- `description`: What it does and when to use it (helps Claude decide when to invoke)
- `disable-model-invocation`: Set to `true` for manual-only skills (side effects, user control)
- `user-invocable`: Set to `false` to hide from menu (default: `true`)
- `allowed-tools`: Optional - restrict which tools Claude can use
- `context`: Set to `fork` to run in subagent
- `agent`: Subagent type when using `context: fork`

### Skill Categories

1. **Development Workflow**: Automate repetitive tasks
2. **Code Quality & Security**: Analysis and improvement
3. **Advanced Analysis**: Deep understanding and explanation
4. **Session & Project Management**: Context preservation and collaboration

### Skill Naming

- Use kebab-case: `session-start`, `fix-todos`, `security-scan`
- Be descriptive but concise
- Follow established patterns in the skill family
- Avoid abbreviations unless universally understood

## Integration Points

### Claude Code CLI

- Skills are invoked via `/skill-name` syntax (Claude Skills)
- Skills receive context from Claude Code conversation history
- Skills can use Claude Code's built-in tools (Read, Write, Edit, Bash, etc.)
- Skills should be autonomous and minimize user interaction

### Git Integration

- Skills may read git status and history
- Skills should never commit without explicit user request
- Use git checkpoints for safety before destructive operations
- Respect user's git configuration and credentials

### File System

- Primary workspace: Project root directory
- Session data: `.claude/sessions/` directory
- Skill definitions: `skills/` directory (each skill in `skills/skill-name/SKILL.md`)
- Installation target: `~/.claude/skills/` (user-specific, personal skills) or `.claude/skills/` (project-specific)

## Common Patterns

### Error Handling

```markdown
If [error condition]:
1. Inform user of the issue
2. Provide clear error message
3. Suggest corrective action
4. Exit gracefully without making changes
```

### User Confirmation

For destructive operations:

1. Explain what will happen
2. Ask for explicit confirmation
3. Provide option to preview changes
4. Allow user to cancel

### Progress Feedback

For long-running operations:

1. Show clear progress indicators
2. Provide intermediate status updates
3. Estimate completion when possible
4. Allow interruption/cancellation

## Anti-Patterns to Avoid

### Never Do These

- ❌ Use AI credentials for git operations
- ❌ Commit code without explicit user request
- ❌ Make destructive changes without checkpoints
- ❌ Skip reading files before editing them
- ❌ Create unnecessary documentation files
- ❌ Add AI attribution to any generated content
- ❌ Override user's git configuration
- ❌ Modify files outside the project directory without permission
- ❌ Execute commands that could cause data loss without confirmation
- ❌ Hardcode paths or assume specific directory structures

### Discouraged Practices

- Creating new files when editing existing ones would suffice
- Over-engineering simple solutions
- Adding unnecessary abstractions
- Verbose explanations when concise ones work
- Using emoji in commits or generated code
- Adding comments to self-explanatory code

## Collaboration with Developers

### Communication Style

- **Concise**: Developers prefer brevity over verbosity
- **Technical**: Use precise technical terminology
- **Action-Oriented**: Focus on what needs to be done
- **Evidence-Based**: Reference specific files and line numbers

### Asking Questions

When clarification is needed:

1. Ask specific, focused questions
2. Provide context for why the information is needed
3. Suggest reasonable defaults when applicable
4. Don't ask questions with obvious answers

### Providing Options

When multiple approaches are valid:

1. Present 2-3 viable options
2. Explain trade-offs clearly
3. Recommend the best option with rationale
4. Let the developer make the final decision

## Project Maintenance

### Regular Tasks

- Update command descriptions when behavior changes
- Sync installation scripts with new commands
- Keep documentation current with codebase
- Test commands with new Claude Code CLI versions
- Review and close obsolete issues/TODOs

### Version Control

- Use conventional commit messages
- Keep commits focused and atomic
- Write clear commit messages explaining "why"
- Reference issues/PRs when applicable

### Release Process

1. Update version numbers consistently
2. Update CHANGELOG.md with changes
3. Test installation on all supported platforms
4. Verify all commands work with current Claude Code version
5. Tag releases with semantic versioning

## Security Considerations

### Code Scanning

- Use `/security-scan` command for vulnerability detection
- Never commit sensitive data (API keys, passwords, credentials)
- Be cautious with file operations outside project directory
- Validate user input in command implementations

### Privacy

- Session data may contain sensitive project information
- Never share session data without explicit permission
- Respect `.gitignore` patterns
- Don't expose internal implementation details unnecessarily

## Extension and Customization

### Adding New Skills

1. Create new directory: `skills/new-skill-name/`
2. Create `SKILL.md` with proper YAML frontmatter:
   - Set appropriate `name` and `description`
   - Choose correct `disable-model-invocation` setting
   - Add other frontmatter fields as needed
3. Add skill markdown content following established patterns
4. Test thoroughly with various scenarios
5. Update installation scripts to include new skill (`install.sh` uses dynamic discovery — no manual array update needed; verify `skills/<name>/SKILL.md` exists)
6. Document in README.md and CLAUDE.md (update skill count)
7. Update this file if new patterns are introduced

### Modifying Existing Skills

1. Read and understand current implementation
2. Identify specific changes needed
3. Maintain backwards compatibility when possible
4. Test all documented use cases
5. Update documentation if behavior changes
6. Consider impact on dependent skills

### Framework-Specific Extensions

When adding framework-specific features:

- Keep core commands framework-agnostic
- Create separate commands for framework-specific functionality
- Auto-detect framework when possible
- Gracefully handle absence of framework
- Document framework requirements clearly

## Subagent Orchestration Patterns

### Three-Tier Architecture

AI DevStudio uses a Command → Agent → Skill hierarchy:

- **Commands** (`.claude/commands/`): High-level orchestrators. Invoke agents and skills, manage user interaction, aggregate results.
- **Agents** (`.claude/agents/`): Specialized workers with restricted tool sets and preloaded skills. Run in isolated context.
- **Skills** (`skills/` or `.claude/skills/`): Atomic capability units. User-invocable or agent-consumed.

See `/architecture:agent-command-system` for a full mid-session reference.

### Current Agents

| Agent | Model | Purpose |
| --- | --- | --- |
| `code-reviewer` | sonnet | Read-only code quality analysis |
| `security-auditor` | sonnet | Vulnerability scanning, OWASP, secrets detection |
| `test-runner` | sonnet | Test execution, failure analysis, TDD enforcement |
| `claude-md-auditor` | opus | Documentation drift detection and repair (CLAUDE.md, AGENTS.md, README.md) |
| `quality-fixer` | sonnet | Iterative lint/shellcheck/type fix cycles (max 5 iterations) |

### Persistent Agent Memory

Each agent accumulates institutional knowledge across conversations via a memory directory:

```
.claude/agent-memory/
  claude-md-auditor/MEMORY.md
  code-reviewer/MEMORY.md
  security-auditor/MEMORY.md
  test-runner/MEMORY.md
  quality-fixer/MEMORY.md
```

Agents read their `MEMORY.md` at the start of each invocation and append new findings after completion.

### Architecture Reference Commands

| Command | Purpose |
| --- | --- |
| `/architecture:skill-system` | Skill tiers, YAML fields, naming, token budgets |
| `/architecture:hook-events` | All 19 hook events, settings structure, compact reminder |
| `/architecture:agent-command-system` | Command/Agent/Skill hierarchy, agent table, memory system |

### Running Skills in Subagents

Use `context: fork` in YAML frontmatter to run a skill in an isolated subagent:

```yaml
---
name: my-skill
description: Runs in a subagent
context: fork
agent: general
---
```

### Parallel Agent Pattern (Boris Cherny Workflow)

For independent parallel workstreams, use git worktrees + tmux:

1. Create worktrees for each workstream: `git worktree add ../feature-a feature-a`
2. Launch agents in separate tmux panes, each in their worktree
3. Agents communicate via shared state in `.claude/sessions/` — never via direct bash IPC
4. Use the `Task` tool (not `Bash`) for inter-agent communication
5. Merge results when all agents complete

Implemented by the `/parallel-agents` skill.

### Agent Design Rules

- Restrict tools to minimum required (e.g., read-only agents get `Read`, `Grep`, `Glob` only)
- Preload relevant skills via `preloadedSkills` frontmatter
- Never call `Bash(git commit)` from an agent — surface to user via Task output
- Agent-level self-evolution: agents may update their own skill files after execution to improve future runs

## Hooks System

Claude Code supports 19 hook events that trigger shell commands at lifecycle points.

### All 19 Hook Events

| Event | Trigger | `once` |
|---|---|---|
| `PreToolUse` | Before any tool call | No |
| `PostToolUse` | After successful tool call | No |
| `PostToolUseFailure` | After failed tool call | No |
| `PermissionRequest` | When Claude requests permission | No |
| `UserPromptSubmit` | When user submits a message | No |
| `Notification` | On notification events | No |
| `Stop` | When Claude stops responding | No |
| `SubagentStart` | When a subagent starts | No |
| `SubagentStop` | When a subagent stops | No |
| `PreCompact` | Before context compaction | Yes |
| `SessionStart` | When a session begins | Yes |
| `SessionEnd` | When a session ends | Yes |
| `Setup` | On initial setup | Yes |
| `TeammateIdle` | When a teammate goes idle | No |
| `TaskCompleted` | When a task completes | No |
| `ConfigChange` | On configuration change | No |
| `WorktreeCreate` | When a worktree is created | No |
| `WorktreeRemove` | When a worktree is removed | No |
| `InstructionsLoaded` | When instructions are loaded | No |

### Hook Configuration

Hooks are defined in `.claude/settings.json` under the `hooks` key:

```json
"hooks": {
  "PreToolUse": [{ "hooks": [{ "type": "command", "command": "python3 ${CLAUDE_PROJECT_DIR}/.claude/hooks/scripts/hooks.py", "timeout": 5000, "async": true }] }],
  "SessionStart": [{ "hooks": [{ "type": "command", "command": "...", "timeout": 5000, "async": true, "once": true }] }]
}
```

### Agent-Level Hooks

Agents can define their own hooks in YAML frontmatter:

```yaml
hooks:
  PostToolUse:
    - type: command
      command: echo "Tool used" >> .claude/hooks/hooks-log.jsonl
```

### DevStudio Hooks Script

`.claude/hooks/scripts/hooks.py` handles all 19 events with:

- Platform-aware audio notifications (afplay/paplay/aplay/winsound)
- JSONL logging to `.claude/hooks/hooks-log.jsonl`
- `--agent=<name>` argument for agent-specific sound mapping
- Graceful degradation when no audio player is available

## Success Metrics

A successful interaction with AI DevStudio:

1. **Time Saved**: Automates repetitive tasks effectively
2. **Quality Maintained**: Code quality matches or exceeds manual work
3. **Context Preserved**: Session continuity across conversations
4. **Safety Ensured**: No accidental data loss or corruption
5. **Standards Followed**: All guidelines in this document are followed

## Resources

- **Main Documentation**: README.md
- **Project Context**: CLAUDE.md
- **Contribution Guidelines**: CONTRIBUTING.md
- **Auto-Loaded Rules**: `.claude/rules/` (skill-development, git-workflow, code-quality, token-optimization)
- **Token Optimization Guide**: TOKEN_OPTIMIZATION_GUIDE.md
- **Session System**: docs/session-management/sessions.md
- **Hooks System**: `.claude/hooks/README.md`
- **Migration Documentation**: docs/migration/MIGRATION-PLAN.md
- **License**: LICENSE (MIT)

## Revision History

- **2025-01-25**: Initial creation with comprehensive AI agent guidelines
- Added critical safety rules for git credentials
- Documented command development patterns
- Established code quality standards
- Defined anti-patterns and best practices

---

**Remember**: AI DevStudio is a tool to enhance developer productivity. Always prioritize the developer's needs, maintain code quality, and follow safety-first principles.
