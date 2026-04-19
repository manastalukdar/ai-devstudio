# AI DevStudio

## What is `AI DevStudio`?

Professional development studio for Claude Code CLI with 99 enterprise-grade skills that save 10-15 hours per week on repetitive development tasks.

### The Problem

😊 Ask Claude to fix a bug → Get 15 test files  
😤 Request a simple refactor → Receive a dissertation on clean code  
🤪 "Please add a button" → Complete UI framework rewrite  
😭 Every conversation → "Act like a senior engineer who doesn't overengineer"

🚧 **Active Development Notice**: AI DevStudio is continuously evolving based on real-world usage. We thoroughly test each skill and refine them as we discover gaps and opportunities. This ensures you're always getting battle-tested, production-ready tools that solve actual developer problems.

**📢 New Claude Skills Format**: AI DevStudio has been updated to use the official Claude Skills format with proper YAML frontmatter and directory structure. Each skill now resides in its own directory (`skills/skill-name/SKILL.md`) following the [Agent Skills](https://agentskills.io) open standard.

AI DevStudio is the most comprehensive development environment for Claude Code CLI, featuring 100 professional skills across 4 tiers (Tier 1: 16 essentials, Tier 2: 38 advanced, Tier 3: 16 power-user, Core: 30 foundation). This intelligent development studio extends Claude with enterprise-grade workflows for TDD, CI/CD, API testing, performance optimization, security scanning, and advanced debugging - leveraging Claude's contextual understanding while delivering structured, predictable outcomes optimized for Opus 4 and Sonnet 4 models.

## Quick Links

- [🚀 Installation](#installation) - Get started in 30 seconds
- [💻 Skills](#skills) - See all available skills
- [🏗️ Project Infrastructure](#project-infrastructure) - Commands, agents, hooks, MCP, rules
- [🔧 How It Works](#how-it-works) - Understanding the magic
- [📚 Session Management](#session-management-workflow) - Professional development tracking
- [🧠 Technical Notes](#technical-notes) - Why conversational design matters
- [🤝 Contributing](#contributing) - Help make it better

## Installation

### Claude Code (default)

**Mac/Linux:**

```bash
curl -sSL https://raw.githubusercontent.com/manastalukdar/ai-devstudio/main/install.sh | bash
```

**Windows/Cross-platform:**

```bash
python install.py
```

**Manual:**

```bash
git clone https://github.com/manastalukdar/ai-devstudio.git
cd ai-devstudio
python install.py
```

### Other AI Tools & Models

AI DevStudio works with any AI coding tool or model. Clone the repo and run the installer with `--target`:

| Target | Tool | Output |
|---|---|---|
| `claude` | Claude Code CLI (default) | `~/.claude/skills/` |
| `gemini` | Gemini CLI | `GEMINI.md` in project root |
| `codex` | Codex CLI / OpenCode | `AGENTS.md` in project root |
| `cursor` | Cursor | `.cursor/rules/skill-*.md` |
| `aider` | Aider | `aider-skills/` + `.aider.conf.yml` |
| `generic` | Any tool or model API (Kimi K2, OpenCode, Ollama, etc.) | `system-prompt.md` |

```bash
git clone https://github.com/manastalukdar/ai-devstudio.git
cd ai-devstudio

# Gemini CLI
python install.py --target gemini        # → GEMINI.md (place in project root)

# Codex CLI / OpenCode
python install.py --target codex         # → AGENTS.md (place in project root)

# Cursor
python install.py --target cursor        # → .cursor/rules/skill-*.md

# Aider
python install.py --target aider         # → aider-skills/ + .aider.conf.yml

# Any tool/model (Kimi K2, Gemini API, Ollama, LM Studio, etc.)
python install.py --target generic       # → system-prompt.md

# Mac/Linux shell equivalents
bash install.sh --target gemini
bash install.sh --target generic
```

The skill **content** is model-agnostic and works with any capable LLM. The generated output includes a tool-name mapping table so the AI knows how to translate `Read`, `Bash`, `Grep`, etc. to its own capabilities.

> **Note:** Hooks, agents, and commands (`.claude/`) are Claude Code-specific and not generated for other targets.

### Uninstall

```bash
# Claude Code — Mac/Linux
./uninstall.sh

# Claude Code — Windows/Cross-platform
python uninstall.py

# Other targets — delete the generated file/directory
rm GEMINI.md                              # gemini
rm AGENTS.md                              # codex
rm -rf .cursor/rules/skill-*.md           # cursor
rm -rf aider-skills/ .aider.conf.yml      # aider
rm system-prompt.md                       # generic
```

## Skills

100 professional skills optimized for Claude Code CLI's native capabilities, organized across 4 tiers:

**🚀 Tier 1 (16 skills)**: High-impact essentials for immediate productivity
**⚡ Tier 2 (37 skills)**: Advanced features for professional workflows
**🔥 Tier 3 (16 skills)**: Power-user tools for specialized needs
**🏛️ Core (30 skills)**: Foundational daily-driver skills

**Invocation**: Skills are invoked using the `/skill-name` syntax (e.g., `/commit`, `/session-start`, `/test-mutation`). These are Claude Skills as defined by Claude Code CLI.

**Format**: Each skill follows the [official Claude Skills format](https://code.claude.com/docs/en/skills) with:
- YAML frontmatter for configuration
- Skill-specific directories (`skills/skill-name/SKILL.md`)
- Token optimization strategies (60-90% reduction)
- Proper invocation control (`disable-model-invocation` field)
- Support for the [Agent Skills](https://agentskills.io) open standard

### 🚀 Development Workflow

```bash
/cleanproject                    # Remove debug artifacts with git safety
/commit                          # Smart conventional commits with analysis
/format                          # Auto-detect and apply project formatter
/scaffold feature-name           # Generate complete features from patterns
/test                            # Run tests with intelligent failure analysis
/implement url/path/feature      # Import and adapt code from any source with validation phase
/refactor                        # Intelligent code restructuring with validation & de-para mapping
/undo                           # Safe rollback with git checkpoint restore
/tdd-red-green                   # Enforce true RED→GREEN→REFACTOR TDD workflow (NEW)
/e2e-generate                    # Generate end-to-end tests with Playwright (NEW)
```

### 🛡️ Code Quality & Security

```bash
/review                # Multi-agent analysis (security, performance, quality, architecture)
/security-scan         # Vulnerability analysis with extended thinking & remediation tracking
/predict-issues        # Proactive problem detection with timeline estimates
/remove-comments       # Clean obvious comments, preserve valuable docs
/fix-imports           # Repair broken imports after refactoring
/find-todos            # Locate and organize development tasks
/create-todos          # Add contextual TODO comments based on analysis results
/fix-todos             # Intelligently implement TODO fixes with context
/dependency-audit      # Comprehensive dependency security and license audit (NEW)
/secrets-scan          # Scan for exposed secrets/credentials/API keys (NEW)
```

### 🔍 Advanced Analysis & Debugging

```bash
/understand            # Analyze entire project architecture and patterns
/explain-like-senior   # Senior-level code explanations with context
/contributing          # Complete contribution readiness analysis
/make-it-pretty        # Improve readability without functional changes
/debug-systematic      # Systematic debugging workflow with hypothesis testing (NEW)
```

### 📋 Session & Project Management

```bash
/session-start [name]           # Begin documented sessions with Claude memory integration
/session-update [notes]         # Update current session with timestamped progress  
/session-end                    # Summarize and preserve session context
/session-current                # View current session status and recent updates
/session-list                   # List all past sessions with summaries
/session-help                   # Display session system help and skills
/session-resume                 # Resume previous session work
/sessions-init                  # Initialize and organize session directory structure
/docs                          # Smart documentation management and updates
/docs-sync                     # Sync CLAUDE.md, AGENTS.md, README.md, and docs/ with code changes
/todos-to-issues               # Convert code TODOs to GitHub issues
```

### ⚙️ CI/CD & DevOps (NEW)

```bash
/ci-setup                      # Configure CI/CD pipelines (GitHub Actions, GitLab CI, CircleCI)
/deploy-validate               # Pre-deployment validation (env config, deps, DB migrations, API compat)
```

### 🌐 API Development & Testing (NEW)

```bash
/api-test-generate             # Auto-generate comprehensive API tests for REST/GraphQL
/api-validate                  # API contract validation and breaking change detection
```

### 🗄️ Database Management (NEW)

```bash
/migration-generate            # Generate database migrations from schema changes
```

### 🎨 Code Generation & Type Safety (NEW)

```bash
/types-generate                # Generate TypeScript types from schemas/APIs
/changelog-auto                # Auto-generate changelogs from commit history
```

### 🤝 Collaboration & Planning (NEW)

```bash
/brainstorm                    # Interactive design refinement with structured exploration
/write-plan                    # Create detailed implementation plans with task breakdown
```

### 🔌 MCP & Tool Integration (NEW)

```bash
/mcp-setup                     # Set up and configure MCP servers
/tool-connect                  # Connect to external tools via MCP (GitHub, DB, APIs)
```

## Enhanced Features

### 🔍 Validation & Refinement

Complex skills now include validation phases to ensure completeness:

```bash
/refactor validate   # Find remaining old patterns, verify 100% migration
/implement validate  # Check integration completeness, find loose ends
```

### 🧠 Extended Thinking

Advanced analysis for complex scenarios:

- **Refactoring**: Deep architectural analysis for large-scale changes
- **Security**: Sophisticated vulnerability detection with chain analysis

### 🔗 Pragmatic Skill Integration

Natural workflow suggestions without over-engineering:

- Suggests `/test` after major changes
- Recommends `/commit` at logical checkpoints
- Maintains user control, no automatic execution

### 📚 Advanced Session Management

Professional development session tracking system:

- **Session Documentation**: Complete session tracking with goals, progress, and outcomes
- **Context Preservation**: Maintain development context across multiple Claude conversations
- **Session Continuity**: Resume previous work with full historical context
- **Progress Tracking**: Timestamped updates with git state and accomplishments
- **Knowledge Transfer**: Enable team collaboration with detailed session histories

## Project Infrastructure

Beyond skills, AI DevStudio ships a complete project-level infrastructure that wires up commands, agents, hooks, MCP servers, and auto-loaded rules.

### Commands

Commands (`.claude/commands/`) are high-level orchestrators that sequence multiple skills and agents, aggregate results, and manage user interaction. Invoke with `/command-name`.

| Command | Description |
|---|---|
| `/quality-pipeline` | Runs `/security-scan` → `/review` → `/test` in sequence; writes combined report to `reports/quality-pipeline-<date>.md` |
| `/release-workflow` | Full release flow: `/deploy-validate` → `/changelog-auto` → version bump → `/commit`; prompts for version type |
| `/session-daily` | Daily startup: start session, git status, find todos, project health check, security pulse, daily briefing |
| `/architecture:skill-system` | Mid-session reference: skill tiers, YAML frontmatter fields, naming conventions, token budgets |
| `/architecture:hook-events` | Mid-session reference: all 19 hook events, settings structure, compact reminder hook |
| `/architecture:agent-command-system` | Mid-session reference: Command/Agent/Skill hierarchy, agent table, persistent memory |

### Agents

Agents (`.claude/agents/`) are specialized workers with restricted tool sets. They are invoked by commands or directly, run in isolated context, and cannot perform operations outside their defined tool scope.

| Agent | Tools | Purpose |
|---|---|---|
| `code-reviewer` | Read, Grep, Glob, WebFetch (read-only) | Deep code review; backs the `/review` skill |
| `security-auditor` | Read, Grep, Glob, Bash (grep/git log only) | Security scanning; backs `/security-scan`, `/owasp-check`, `/secrets-scan` |
| `test-runner` | Read, Bash (test commands only) | Test execution; backs `/test`, `/tdd-red-green`, `/test-coverage` |
| `claude-md-auditor` | Read, Grep, Glob, Bash, Edit | Documentation drift detection — cross-references skill counts, tier totals, and file references across CLAUDE.md, AGENTS.md, README.md and surgically corrects discrepancies |
| `quality-fixer` | Read, Bash, Edit, Glob, Grep | Iterative lint/shellcheck/type fix cycles (max 5 iterations) for Python and shell scripts |

Agents use a **persistent memory pattern**: each agent has a `.claude/agent-memory/<name>/MEMORY.md` file loaded on every invocation, accumulating institutional knowledge about the codebase across conversations.

### Project-Local Skills

`.claude/skills/` holds internal skills consumed by agents and commands. These are hidden from the user menu (`user-invocable: false`) and are distinct from the 99 user-facing skills in `skills/`.

| Skill | Purpose |
|---|---|
| `project-health` | Checks skill count consistency across docs, stale sessions, cache size, install script syntax |
| `skill-validator` | Validates new skills: YAML frontmatter, Token Optimization section, line limit, naming conventions |

### Hooks

AI DevStudio registers handlers for all 19 Claude Code hook events via `.claude/hooks/scripts/hooks.py`. Hooks fire automatically — no user action required.

**What hooks do:**

- Play audio notifications on tool use, session start/end, errors, and task completion (platform-aware: `afplay` on macOS, `paplay`/`aplay`/`ffplay` on Linux, `winsound` on Windows)
- Log every event to `.claude/hooks/hooks-log.jsonl` with timestamp, event type, and tool name
- Support agent-specific sound mapping via `--agent=<name>` argument
- Inject a structured codebase reminder after context compaction events (`SessionStart` with `compact` matcher) to restore critical context lost during compaction
- Degrade gracefully when no audio player is available (log only)

**Supported hook events:**

```
PreToolUse      PostToolUse      PostToolUseFailure   PermissionRequest
UserPromptSubmit  Notification    Stop                 SubagentStart
SubagentStop    PreCompact       SessionStart          SessionEnd
Setup           TeammateIdle    TaskCompleted         ConfigChange
WorktreeCreate  WorktreeRemove  InstructionsLoaded
```

See [.claude/hooks/README.md](.claude/hooks/README.md) for configuration details.

### Auto-Loaded Rules

`.claude/rules/` contains Markdown rule files that Claude Code auto-loads for every conversation. Rules extend CLAUDE.md without bloating it beyond the ~200 line best-practice limit.

| Rule File | Contents |
|---|---|
| `skill-development.md` | YAML frontmatter fields, skill sections, naming conventions, tier criteria, token budget table |
| `git-workflow.md` | AI credential prohibition, conventional commits format, checkpoint rule, branch strategy |
| `code-quality.md` | Python/Shell/Markdown standards, no emoji, Edit-before-Write, install script sync rule |
| `token-optimization.md` | 8 optimization patterns with % savings, mandatory Token Optimization section template |

### MCP Servers

`.mcp.json` configures project-scoped MCP servers available in every Claude Code session:

| Server | Package | Purpose |
|---|---|---|
| `context7` | `@upstash/context7-mcp` | Up-to-date library docs — prevents hallucinated APIs |
| `playwright` | `@playwright/mcp` | Browser automation for `/playwright-automate` and `/e2e-generate` |
| `github` | `@modelcontextprotocol/server-github` | GitHub automation; requires `GITHUB_TOKEN` env var |
| `filesystem` | `@modelcontextprotocol/server-filesystem` | Inspect `~/.claude/skills/` without Bash |

### Project Settings

`.claude/settings.json` applies project-level Claude Code configuration:

- **Model**: `claude-sonnet-4-6`
- **Output style**: concise (matches project brevity preference)
- **Permissions**: pre-approved `Bash(git:*)`, `Bash(grep:*)`, `Edit(**)`, `Write(**)` etc.; `ask` for `Bash(rm:*)`, `Bash(git push:*)`, `Bash(sudo:*)`
- **All 19 hooks** registered to `.claude/hooks/scripts/hooks.py`
- **Plans directory**: `./reports`

## Real World Example

### Before `/cleanproject`

```plaintext
src/
├── UserService.js
├── UserService.test.js
├── UserService_backup.js    # Old version
├── debug.log               # Debug output
├── test_temp.js           # Temporary test
└── notes.txt              # Dev notes
```

### After `/cleanproject`

```plaintext
src/
├── UserService.js          # Clean production code
└── UserService.test.js     # Actual tests preserved
```

## 🔧 How It Works

### High-Level Architecture

AI DevStudio transforms Claude Code CLI into an intelligent development assistant through a three-tier Command → Agent → Skill architecture:

```plaintext
Developer
    │
    ├─ /command   → Command (.claude/commands/) → orchestrates multiple agents/skills
    │                        │
    │                        ├─ Agent (.claude/agents/) → specialized worker with restricted tools
    │                        │          │
    │                        └─────────→└─ Skill (skills/ or .claude/skills/) → atomic capability
    │
    └─ /skill     → Skill (skills/) → direct execution
    ↑                                                    ↓
    ←←←←←←←←←←←←←←←←← Clear Feedback & Results ←←←←←←←←
```

Hook events fire automatically at each lifecycle point (tool use, session start/end, etc.), enabling notifications and logging without user intervention.

### Execution Flow

When you invoke a skill:

1. **Skill Loading**: Claude reads the SKILL.md definition from `~/.claude/skills/skill-name/`
2. **Context Analysis**: Analyzes your project structure, technology stack, and current state
3. **Intelligent Planning**: Creates execution strategy based on your specific situation
4. **Safe Execution**: Performs actions with automatic checkpoints and validation
5. **Clear Feedback**: Provides results, next steps, and any warnings

### Core Architecture Components

**🧠 Intelligent Instructions**

- First-person conversational design activates collaborative reasoning
- Strategic thinking sections (`<think>`) for complex decision-making
- Context-aware adaptations without hardcoded assumptions

**🔧 Native Tool Integration**

- **Grep**: Lightning-fast pattern matching across codebases
- **Glob**: Intelligent file discovery and project mapping
- **Read**: Content analysis with full context understanding
- **Write**: Safe file modifications with automatic backups
- **TodoWrite**: Progress tracking and task management
- **Task**: Sub-agent orchestration for specialized analysis

**🛡️ Safety-First Design**

- Automatic git checkpoints before destructive operations
- Session persistence for cross-context continuity
- Rollback capabilities with clear recovery paths
- No AI attribution in commits or generated content

**🌐 Universal Compatibility**

- Framework-agnostic with intelligent auto-detection
- Cross-platform support (Windows, Linux, macOS)
- Works with any programming language or stack
- Adapts to your project's conventions and patterns

### Advanced Features

**🔄 Session Continuity**
Skills like `/implement` and `/refactor` maintain state across Claude sessions:

```
# Each skill creates its own folder in project root:
refactor/                  # Created by /refactor skill
├── plan.md               # Refactoring roadmap
└── state.json            # Completed transformations

implement/                 # Created by /implement skill
├── plan.md               # Implementation progress
└── state.json            # Session state and decisions

fix-imports/              # Created by /fix-imports skill
├── plan.md               # Import fixes plan
└── state.json            # Resolution progress

security-scan/            # Created by /security-scan skill
├── plan.md               # Vulnerabilities and fixes
└── state.json            # Remediation progress

scaffold/                 # Created by /scaffold skill
├── plan.md               # Scaffolding plan
└── state.json            # Created files tracking
```

**📚 Session Management System**
Advanced session tracking with Claude Code integration:

```
.claude/                   # Claude Code directory
├── sessions/             # Session storage directory
│   ├── .current-session # Tracks active session filename
│   ├── 2025-01-16-1347-feature-auth.md  # Named session file
│   ├── 2025-01-17-0930.md               # Timestamp-only session
│   └── feature-areas/    # Organized by project areas
│       ├── authentication/
│       ├── database/
│       └── ui-components/
└── CLAUDE.md            # Claude Code memory file
```

**🤖 Multi-Agent Architecture**
Complex skills orchestrate specialized sub-agents:

- Security analysis agent for vulnerability detection
- Performance optimization agent for bottleneck identification
- Architecture review agent for design pattern analysis
- Code quality agent for maintainability assessment

**📊 Performance Optimizations**

- Reduced verbosity for senior developer efficiency
- Smart caching of project analysis results
- Incremental processing for large codebases
- Parallel execution of independent tasks

## 🧠 Technical Notes

### Design Philosophy

**Why This Approach Works** (Based on Anthropic's Research):

- **Conversational Skills**: First-person language ("I'll help...") activates Claude's collaborative reasoning
- **Build-Agnostic Instructions**: No hardcoded tools = works everywhere
- **Think Tool Integration**: Strategic thinking improves decisions by 50%+ (Anthropic, 2025)
- **Native Tools Only**: Uses Claude Code's actual capabilities, not imaginary APIs

**Key Principles:**

- **Simplicity > Complexity**: Start simple, add only when proven necessary
- **Context Awareness**: Skills adapt to YOUR project, not vice versa
- **Safety First**: Git checkpoints before any destructive operation
- **Pattern Recognition**: Learn from your codebase, not assumptions

### Technical Architecture

**Native Tool Integration:**
All skills leverage Claude Code CLI's native capabilities:

- Grep tool for efficient pattern matching
- Glob tool for file discovery
- Read tool for content analysis
- TodoWrite for progress tracking
- Sub-agents for specialized analysis

**Safety-First Design:**

```bash
git add -A
git commit -m "Pre-operation checkpoint" || echo "No changes to commit"
```

**Conversational Interface:**
Skills use first-person collaborative language ("I'll analyze your code...") rather than imperative instructions, creating a natural partnership interaction that improves model performance.

**Framework Agnostic:**
Intelligent detection without hardcoded assumptions enables universal compatibility across technology stacks.

### User Skills Indicator

Custom skills appear with a `(user)` tag in Claude Code CLI to distinguish them from built-in skills. This is normal and indicates your skills are properly installed.

```
/commit
    Smart Git Commit (user)    ← Your custom skill
/help
    Show help                  ← Built-in skill
```

## Performance Metrics

| Task                | Manual Time | With AI DevStudio | Time Saved |
| ------------------- | ----------- | --------------------- | ---------- |
| Security analysis   | 45-60 min   | 3-5 min               | ~50 min    |
| Architecture review | 30-45 min   | 5-8 min               | ~35 min    |
| Feature scaffolding | 25-40 min   | 2-3 min               | ~30 min    |
| Git commits         | 5-10 min    | 30 sec                | ~9 min     |
| Code cleanup        | 20-30 min   | 1 min                 | ~25 min    |
| Import fixing       | 15-25 min   | 1-2 min               | ~20 min    |
| Code review         | 20-30 min   | 2-4 min               | ~20 min    |
| Issue prediction    | 60+ min     | 5-10 min              | ~50 min    |
| TODO resolution     | 30-45 min   | 3-5 min               | ~35 min    |
| Code adaptation     | 40-60 min   | 3-5 min               | ~45 min    |
| CI/CD setup         | 45-60 min   | 3-5 min               | ~50 min    |
| E2E test generation | 40-60 min   | 3-5 min               | ~45 min    |
| API test generation | 35-50 min   | 3-5 min               | ~40 min    |
| Deployment validation | 30-45 min | 2-3 min               | ~35 min    |
| DB migration creation | 25-40 min | 2-3 min               | ~30 min    |
| Type generation     | 20-35 min   | 1-2 min               | ~25 min    |
| Secrets scanning    | 30-45 min   | 2-3 min               | ~35 min    |
| Systematic debugging | 45-75 min  | 5-10 min              | ~50 min    |

**Total: 8-10 hours saved per week with AI DevStudio's professional-grade analysis and automation**

## Requirements

- Claude Code CLI
- Python 3.6+ (for installer)
- Git (for version control skills)

## Advanced Usage

### Creating Custom Skills

Create your own skills by adding directories to `~/.claude/skills/`:

```markdown
# My Custom Skill

I'll help you with your specific workflow.

[Your instructions here]
```

### Using Arguments

Skills support arguments via `$ARGUMENTS`:

```bash
/myskill some-file.js
# $ARGUMENTS will contain "some-file.js"
```

### CI/CD Integration

Use skills in automated workflows:

```bash
# Quality pipeline
claude "/security-scan" && claude "/review" && claude "/test"

# Pre-commit validation  
claude "/format" && claude "/commit"

# Feature development
claude "/scaffold api-users" && claude "/test"

# Complete workflow
claude "/security-scan" && claude "/create-todos" && claude "/todos-to-issues"

# TODO resolution workflow
claude "/find-todos" && claude "/fix-todos" && claude "/test"
```

### Manual Workflow Integration

Perfect for development routines:

```bash
# Morning routine
claude "/session-start feature-authentication"
claude "/security-scan"

# During development
claude "/scaffold user-management"
claude "/session-update Added OAuth integration"
claude "/review" 
claude "/format"

# Progress tracking
claude "/session-update Fixed Next.js 15 params Promise issue"
claude "/session-current"

# End of day
claude "/commit"
claude "/session-end"
```

### Session Management Workflow

Complete development session lifecycle:

```bash
# Starting a focused development session
claude "/session-start authentication-refactor"
# Define goals and begin work

# Regular progress updates during development
claude "/session-update Implemented Google OAuth middleware"
claude "/session-update Resolved async cookie handling issue"

# Check session status anytime
claude "/session-current"

# List and review past sessions
claude "/session-list"

# Resume previous work
claude "/session-resume"

# Initialize organized session structure
claude "/sessions-init"

# End with comprehensive summary
claude "/session-end"
```

## Security & Git Instructions

All skills that interact with git include security instructions to prevent AI attribution:

**Skills with git protection:**

- `/commit`, `/scaffold`, `/make-it-pretty`, `/cleanproject`, `/fix-imports`, `/review`, `/security-scan`
- `/contributing`, `/todos-to-issues`, `/predict-issues`, `/find-todos`, `/create-todos`, `/fix-todos`
- `/session-start`, `/session-update`, `/session-end`, `/session-current`, `/session-list`, `/session-resume`, `/sessions-init`

These skills will NEVER:

- Add "Co-authored-by" or AI signatures
- Include "Generated with Claude Code" messages
- Modify git config or credentials
- Add AI attribution to commits/issues

You can modify these instructions in individual skill files if needed.

## Session Management Documentation

For comprehensive details about the session management system, see [docs/session-management/sessions.md](docs/session-management/sessions.md). This documentation covers:

- Complete session workflow and best practices
- Advanced skill usage and examples
- Session file structure and organization
- Integration with Claude Code's memory system
- Tips for team collaboration and knowledge transfer

## Contributing

We welcome contributions that help developers save time. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Acknowledgements

This project builds upon and extends excellent work from the open-source community. We gratefully acknowledge the following projects that have contributed foundational concepts and implementations:

### Core Framework
- **[CCPlugins](https://github.com/brennercruvinel/CCPlugins)** - Professional skill framework and core development workflow skills
- **[claude-sessions](https://github.com/iannuttall/claude-sessions)** - Session management system architecture and documentation patterns
- **[claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)** by shanraisshan - Command/Agent/Skill architecture patterns, hooks infrastructure design, MCP server configuration, and advanced Claude Code settings best practices
- **[claude-devtools](https://github.com/matt1398/claude-devtools)** by matt1398 - Persistent agent memory pattern, compaction-aware SessionStart hook for context restoration, and architecture documentation as slash commands

### Development Methodologies & Patterns
- **[obra/superpowers](https://github.com/obra/superpowers)** - TDD methodology, RED/GREEN/REFACTOR workflow, YAGNI/DRY principles, and collaboration patterns
- **[Anthropic Skills](https://github.com/anthropics/skills)** - Official Claude Skills examples and best practices
- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io)** - MCP integration standards and server specifications

### Testing & Quality Assurance
- **[Playwright](https://playwright.dev)** - E2E testing framework and browser automation patterns
- **[Supertest](https://github.com/ladjs/supertest)** - API testing library and HTTP assertion patterns
- **[FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)** - API testing best practices for Python
- **[Jest Documentation](https://jestjs.io)** - JavaScript testing framework patterns
- **[Stryker](https://stryker-mutator.io)** - Mutation testing for JavaScript/TypeScript
- **[mutmut](https://github.com/boxed/mutmut)** - Python mutation testing framework
- **[xUnit Test Patterns](http://xunitpatterns.com)** - Gerard Meszaros' testing anti-patterns and best practices
- **[Istanbul/nyc](https://istanbul.js.org)** - JavaScript code coverage tool
- **[pytest](https://pytest.org)** - Python testing framework and coverage tools

### API & Schema Standards
- **[OpenAPI Specification](https://www.openapis.org)** - API contract validation and schema standards
- **[GraphQL Code Generator](https://the-guild.dev/graphql/codegen)** - Type generation from GraphQL schemas
- **[GraphQL Federation](https://www.apollographql.com/docs/federation/)** - Apollo Federation specification
- **[Postman](https://www.postman.com)** - API testing and collection format
- **[Prism](https://stoplight.io/open-source/prism)** - OpenAPI mock server
- **[MSW (Mock Service Worker)](https://mswjs.io)** - API mocking library
- **[WireMock](https://wiremock.org)** - HTTP API mocking

### CI/CD & DevOps
- **[GitHub Actions Documentation](https://docs.github.com/en/actions)** - CI/CD pipeline best practices
- **[GitLab CI Documentation](https://docs.gitlab.com/ee/ci/)** - GitLab CI/CD patterns
- **[CircleCI Documentation](https://circleci.com/docs/)** - CircleCI configuration standards
- **[Terraform](https://www.terraform.io)** - Infrastructure as Code for multi-cloud
- **[AWS CloudFormation](https://aws.amazon.com/cloudformation/)** - AWS infrastructure provisioning
- **[Pulumi](https://www.pulumi.com)** - Modern Infrastructure as Code
- **[Docker](https://www.docker.com)** - Container platform and best practices
- **[Kubernetes](https://kubernetes.io)** - Container orchestration platform
- **[Trivy](https://trivy.dev)** - Container security scanning

### Database & ORM
- **[Prisma](https://www.prisma.io)** - Database schema and type generation patterns
- **[TypeORM](https://typeorm.io)** - TypeScript/JavaScript ORM
- **[SQLAlchemy](https://www.sqlalchemy.org)** - Python SQL toolkit and ORM
- **[Django ORM](https://docs.djangoproject.com/en/stable/topics/db/)** - Django database ORM
- **[Sequelize](https://sequelize.org)** - Node.js ORM for SQL databases
- **[Mongoose](https://mongoosejs.com)** - MongoDB object modeling
- **[Faker.js](https://fakerjs.dev)** - Generate realistic fake data
- **[Python Faker](https://faker.readthedocs.io)** - Python fake data generator

### Performance & Optimization
- **[Lighthouse](https://developer.chrome.com/docs/lighthouse/)** - Google web performance auditing
- **[Webpack](https://webpack.js.org)** - Module bundler and optimization
- **[Vite](https://vitejs.dev)** - Next-generation frontend tooling
- **[esbuild](https://esbuild.github.io)** - Extremely fast JavaScript bundler
- **[Rollup](https://rollupjs.org)** - JavaScript module bundler
- **[clinic.js](https://clinicjs.org)** - Node.js performance profiling
- **[Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)** - Browser debugging and profiling
- **[memory_profiler](https://pypi.org/project/memory-profiler/)** - Python memory usage profiling

### Security & Code Quality
- **[gitleaks](https://github.com/gitleaks/gitleaks)** - Secrets detection patterns
- **[trufflehog](https://github.com/trufflesecurity/trufflehog)** - Credential scanning methodology
- **[Snyk](https://snyk.io)** - Dependency security scanning patterns
- **[OWASP Top 10](https://owasp.org/www-project-top-ten/)** - Security vulnerability standards
- **[WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)** - Web Content Accessibility Guidelines
- **[axe-core](https://github.com/dequelabs/axe-core)** - Accessibility testing engine (Deque Systems)
- **[pa11y](https://pa11y.org)** - Automated accessibility testing
- **[ESLint](https://eslint.org)** - JavaScript/TypeScript linting and complexity analysis
- **[radon](https://radon.readthedocs.io)** - Python code metrics and complexity
- **[jscpd](https://github.com/kucherenko/jscpd)** - Copy-paste detector for code duplication

### Architecture & Methodologies
- **[Boris Cherny](https://github.com/bcherny)** - Multi-agent parallel development workflow patterns
- **[Martin Fowler](https://martinfowler.com)** - Refactoring patterns and software design principles
- **[Thomas J. McCabe](https://en.wikipedia.org/wiki/Cyclomatic_complexity)** - Cyclomatic complexity metric
- **[The Pragmatic Programmer](https://pragprog.com/titles/tpp20/)** - DRY principle and programming best practices
- **[Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)** - Robert C. Martin's code quality principles
- **[Git Documentation](https://git-scm.com/doc)** - Git workflows, worktrees, bisect, and merge strategies

### Documentation & Diagramming
- **[Mermaid](https://mermaid.js.org)** - Markdown-based diagram generation
- **[PlantUML](https://plantuml.com)** - UML diagram generation
- **[Storybook](https://storybook.js.org)** - UI component development and documentation
- **[JSDoc](https://jsdoc.app)** - JavaScript documentation standard
- **[Godoc](https://go.dev/blog/godoc)** - Go documentation format
- **[Sphinx](https://www.sphinx-doc.org)** - Python documentation generator

### Standards & Conventions
- **[Conventional Commits](https://www.conventionalcommits.org)** - Commit message format standards
- **[Keep a Changelog](https://keepachangelog.com)** - Changelog generation standards
- **[Semantic Versioning](https://semver.org)** - Version management standards
- **[ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)** - Accessible Rich Internet Applications
- **[Section 508](https://www.section508.gov)** - Federal accessibility standards
- **[WebAIM](https://webaim.org)** - Web accessibility resources and guidelines

This repository enhances these foundations with 100 professional skills across 3 tiers, refined workflows, and integrated session management capabilities tailored for professional development environments.

## License

MIT License - see [LICENSE](LICENSE) file for details.
