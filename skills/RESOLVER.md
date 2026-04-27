# RESOLVER.md — Intent-to-Skill Dispatcher

When the user describes what they want rather than naming a skill, use this file to route to the correct skill. Match the user's phrasing to the intent groups below.

Inspired by [gbrain's RESOLVER.md pattern](https://github.com/garrytan/gbrain).

---

## Disambiguation Rules

1. **Prefer the most specific skill** — if two skills match, choose the one with narrower scope
2. **Chain explicitly** — if the task requires multiple skills in sequence, name them all (e.g., `/security-scan` → `/review` → `/commit`)
3. **When in doubt, ask** — one clarifying question beats routing to the wrong skill
4. **Signal detector runs in parallel** — always spawn `/signal-detector` as a background task; never block on it

---

## Session & Project Setup

| User says... | Route to |
|---|---|
| "start a session", "begin work on X", "new session" | `/session-start` |
| "end session", "wrap up", "I'm done for today" | `/session-end` |
| "resume", "pick up where I left off", "what was I doing?" | `/session-resume` |
| "update session", "log progress", "checkpoint" | `/session-update` |
| "list sessions", "show my sessions", "session history" | `/session-list` |
| "session help", "how do sessions work?" | `/session-help` |
| "initialize sessions", "set up session management" | `/sessions-init` |
| "daily briefing", "what's going on today?", "morning standup" | `/briefing` |
| "onboard me", "set up my profile", "create USER.md" | `/project-onboard` |
| "health check", "smoke test", "is everything working?" | `/smoke-test` |
| "project health", "check skill counts", "are docs in sync?" | `/project-health` |

---

## Code Understanding

| User says... | Route to |
|---|---|
| "explain this code", "what does X do?", "walk me through" | `/explain-like-senior` |
| "understand this codebase", "give me an overview", "how is this structured?" | `/understand` |
| "draw the architecture", "diagram this", "show me the system" | `/architecture-diagram` |
| "show the database schema", "ER diagram", "table relationships" | `/db-diagram` |

---

## Code Quality & Cleanup

| User says... | Route to |
|---|---|
| "review my code", "code review", "review staged changes" | `/review` |
| "second opinion", "review the review", "quality gate" | `/cross-modal-review` |
| "review checklist", "what should I check?" | `/code-review-checklist` |
| "remove comments", "clean up comments", "delete obvious comments" | `/remove-comments` |
| "improve names", "rename variables", "better naming" | `/naming-improve` |
| "reduce complexity", "simplify this function", "cyclomatic complexity" | `/complexity-reduce` |
| "find duplicates", "DRY this", "repeated code" | `/duplication-detect` |
| "make it prettier", "clean up formatting", "readable" | `/make-it-pretty` |
| "predict issues", "what could go wrong?", "proactive review" | `/predict-issues` |
| "clean project", "remove temp files", "housekeeping" | `/cleanproject` |
| "remove AI tells", "clean up AI writing", "humanize this doc" | `/remove-ai-tells` |

---

## Testing

| User says... | Route to |
|---|---|
| "run tests", "test this", "check if tests pass" | `/test` |
| "TDD", "red-green-refactor", "write failing test first" | `/tdd-red-green` |
| "test coverage", "what's not covered?", "coverage report" | `/test-coverage` |
| "mutation testing", "test quality", "are my tests meaningful?" | `/test-mutation` |
| "async tests", "test async code", "race conditions in tests" | `/test-async` |
| "test anti-patterns", "fix bad tests", "test smell" | `/test-antipatterns` |
| "generate E2E tests", "Playwright tests", "browser tests" | `/e2e-generate` |
| "generate API tests", "test this endpoint", "HTTP tests" | `/api-test-generate` |
| "automate browser", "UI automation", "click testing" | `/playwright-automate` |
| "generate mocks", "mock this", "stub this dependency" | `/mock-generate` |
| "generate seed data", "fixture data", "test data" | `/seed-data` |

---

## Security

| User says... | Route to |
|---|---|
| "security scan", "find vulnerabilities", "security audit" | `/security-scan` |
| "OWASP check", "OWASP top 10", "injection vulnerabilities" | `/owasp-check` |
| "check secrets", "find leaked credentials", "secrets scan" | `/secrets-scan` |
| "security headers", "HTTP headers", "CSP, CORS, HSTS" | `/security-headers` |
| "audit dependencies", "vulnerable packages", "CVE check" | `/dependency-audit` |
| "check licenses", "license compliance", "open source licenses" | `/license-check` |
| "security review of PR", "review for security" | `/security-review` (agent command) |

---

## Debugging & Performance

| User says... | Route to |
|---|---|
| "debug this", "systematic debugging", "find the bug" | `/debug-systematic` |
| "root cause", "why is this failing?", "trace the failure" | `/debug-root-cause` |
| "debug session", "interactive debugging", "step through" | `/debug-session` |
| "bisect", "find which commit broke this", "git bisect" | `/git-bisect` |
| "profile performance", "what's slow?", "performance analysis" | `/performance-profile` |
| "memory leak", "find memory leak", "heap analysis" | `/memory-leak` |
| "optimize query", "slow query", "N+1 problem" | `/query-optimize` |

---

## Refactoring & Implementation

| User says... | Route to |
|---|---|
| "refactor this", "restructure", "clean up this code" | `/refactor` |
| "implement this", "add this feature", "build X" | `/implement` |
| "scaffold", "generate boilerplate", "create component" | `/scaffold` (or `/boilerplate`) |
| "fix imports", "broken imports", "missing imports" | `/fix-imports` |
| "fix TODOs", "resolve TODOs", "address the TODOs" | `/fix-todos` |
| "find TODOs", "list TODOs", "what's pending?" | `/find-todos` |
| "create TODOs", "add TODO markers", "mark future work" | `/create-todos` |
| "write a plan", "plan this out", "implementation plan" | `/write-plan` |
| "execute the plan", "work through the plan", "run the plan" | `/execute-plan` |

---

## APIs & Schema

| User says... | Route to |
|---|---|
| "generate API docs", "document the API", "OpenAPI spec" | `/api-docs-generate` |
| "API examples", "show me how to use this API" | `/api-examples` |
| "mock API", "stub server", "API mock" | `/api-mock` |
| "validate API contract", "breaking changes", "API diff" | `/api-validate` |
| "generate types from OpenAPI", "TypeScript from spec" | `/openapi-types` |
| "GraphQL schema", "generate GraphQL types" | `/graphql-schema` |
| "generate migration", "database migration", "schema change" | `/migration-generate` |
| "validate schema", "schema drift", "DB schema check" | `/schema-validate` |
| "connect to database", "DB setup" | `/database-connect` |
| "connect tool/MCP", "add MCP server", "tool setup" | `/tool-connect` |
| "Postman collection", "convert Postman", "import Postman" | `/postman-convert` |
| "GitHub integration", "set up GitHub", "gh CLI" | `/github-integration` |

---

## Git & Version Control

| User says... | Route to |
|---|---|
| "commit", "commit my changes", "git commit" | `/commit` |
| "merge strategy", "how should I merge?", "rebase or merge?" | `/merge-strategy` |
| "resolve conflict", "merge conflict", "fix conflict" | `/conflict-resolve` |
| "finish branch", "close this branch", "squash and merge" | `/branch-finish` |
| "worktree", "parallel branch work", "git worktree" | `/git-worktree` |
| "undo", "rollback", "revert last operation" | `/undo` |
| "save context", "save my WIP", "checkpoint my work", "switch tasks" | `/context-save` |
| "restore context", "resume WIP", "get my work back", "unpause" | `/context-restore` |

---

## Documentation

| User says... | Route to |
|---|---|
| "update docs", "fix docs", "document this change" | `/docs` |
| "sync docs with code", "docs are stale", "update README" | `/docs-sync` |
| "generate README", "write README" | `/readme-generate` |
| "add inline docs", "add docstrings", "JSDoc" | `/inline-docs` |
| "update CHANGELOG", "changelog entry", "what changed?" | `/changelog-auto` |
| "contributing guide", "how to contribute", "check readiness" | `/contributing` |

---

## CI/CD & DevOps

| User says... | Route to |
|---|---|
| "set up CI", "GitHub Actions", "CI pipeline" | `/ci-setup` |
| "monitor pipeline", "CI status", "flaky tests in CI" | `/pipeline-monitor` |
| "validate deploy", "pre-deploy check", "deployment readiness" | `/deploy-validate` |
| "rollback deployment", "revert deploy", "deployment rollback" | `/deployment-rollback` |
| "Docker optimization", "optimize container", "smaller image" | `/container-optimize` |
| "infrastructure as code", "Terraform", "CloudFormation" | `/infrastructure` |
| "release", "cut a release", "publish version" | `/release-automation` |
| "set up MCP", "configure MCP server" | `/mcp-setup` |

---

## Frontend & Accessibility

| User says... | Route to |
|---|---|
| "accessibility check", "a11y", "WCAG compliance" | `/accessibility` |
| "Lighthouse audit", "performance audit", "web vitals" | `/lighthouse` |
| "bundle analysis", "bundle size", "what's making the bundle big?" | `/bundle-analyze` |
| "webpack config", "Vite config", "build optimization" | `/webpack-optimize` |
| "lazy load", "code splitting", "defer loading" | `/lazy-load` |
| "cache strategy", "HTTP caching", "service worker cache" | `/cache-strategy` |
| "component library", "Storybook", "design system" | `/component-library` |

---

## Deployment & Monitoring

| User says... | Route to |
|---|---|
| "watch the deploy", "monitor after deploy", "post-deploy check" | `/canary` |
| "is my deployment healthy?", "poll the health endpoint", "check for regressions" | `/canary` |

---

## Developer Experience

| User says... | Route to |
|---|---|
| "audit developer experience", "DX review", "onboarding friction" | `/devex-review` |
| "review planning session", "stop and think before coding", "YC office hours" | `/office-hours` |
| "weekly retro", "retrospective", "what shipped this week?" | `/retro` |
| "record a learning", "save this pattern", "remember this insight" | `/learn add` |
| "show my learnings", "what have I learned?", "list learnings" | `/learn list` |
| "apply learnings", "relevant patterns for this context" | `/learn apply` |

---

## Safety & Guardrails

| User says... | Route to |
|---|---|
| "is this command safe?", "should I run this?", "warn me before X" | `/careful` |
| "rm -rf", "DROP TABLE", "force push", "git reset --hard" | `/careful` (auto-intercept) |

---

## Skill & Project Meta

| User says... | Route to |
|---|---|
| "create a new skill", "build a skill for X", "skillify this fix" | `/skillify` |
| "detect signals", "capture this to memory", "remember this" | `/signal-detector` |
| "brainstorm", "explore options", "think through this" | `/brainstorm` |
| "parallel agents", "run multiple agents", "split the work" | `/parallel-agents` |
| "run quality pipeline", "full QA", "security + review + test" | `/quality-pipeline` |
| "generate config", "config file for X" | `/config-generate` |
| "format code", "run formatter", "lint and format" | `/format` |
| "generate types", "TypeScript types from X" | `/types-generate` |
| "TODOs to GitHub issues", "create issues from TODOs" | `/todos-to-issues` |
| "session daily start", "start of day routine" | `/session-daily` |

---

## Always-On (run in background without user instruction)

| Condition | Skill |
|---|---|
| Every session | `/signal-detector` (spawn as background task) |
| After any major change | `/smoke-test` |
| After modifying skills/ or docs | `/docs-sync` |
