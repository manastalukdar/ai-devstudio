---
name: devex-review
description: Audit the developer experience of your project — setup friction, onboarding clarity, local dev loop speed, tooling consistency, and documentation gaps. Produces a DX scorecard and prioritized improvement list. Inspired by gstack's devex-review skill.
disable-model-invocation: false
---

# DevEx Review

I'll audit your project's developer experience end-to-end: setup friction, onboarding, local dev loop, tooling consistency, documentation gaps. You get a scored DX report and a ranked list of quick wins. Inspired by gstack's devex-review skill.

## Token Optimization

**Expected range**: 400–1,000 tokens (full audit), 50 tokens (no project structure found)

**Patterns used**: Bash for file discovery, Grep-before-Read, progressive disclosure (scores → details on request)

**Early exit**: If no `package.json`, `Makefile`, `pyproject.toml`, or similar project manifest is found, report "No project manifest found — cannot audit DX" and stop.

## Step 1 — Discover Project Structure

```bash
# Detect project type and manifest files
ls -la package.json pyproject.toml Cargo.toml go.mod Makefile Dockerfile \
   README.md CONTRIBUTING.md .env.example .envrc 2>/dev/null

# Check for common dev tooling
ls -la .github/workflows/ .circleci/ .gitlab-ci.yml \
   .editorconfig .prettierrc .eslintrc* .flake8 2>/dev/null

# Check dev setup scripts
ls -la scripts/ bin/ Makefile 2>/dev/null | head -20

# Local dev loop — what commands exist?
if [ -f package.json ]; then
    node -e "const p=require('./package.json'); console.log(JSON.stringify(Object.keys(p.scripts||{})))" 2>/dev/null
fi
if [ -f Makefile ]; then
    grep "^[a-zA-Z].*:" Makefile | head -20
fi
```

## Step 2 — Evaluate Eight DX Dimensions

Score each dimension 1–5 (5 = excellent, 1 = painful).

### D1 — First-Run Setup (weight: high)

- Is there a `README.md` with setup steps? (no README → 1)
- Does `README` have a "Getting Started" or "Quick Start" section?
- Are prerequisites listed (Node version, Python version, etc.)?
- Is there a setup script (`make setup`, `npm run bootstrap`, etc.)?
- Does `.env.example` exist with all required variables documented?

**Score signals**: README + setup script + .env.example = 5; bare README only = 2; nothing = 1

### D2 — Local Dev Loop Speed (weight: high)

- Is there a `dev`/`start`/`watch` command with hot reload?
- Is the build incremental (webpack HMR, vite, turbowatch, etc.)?
- Are there known slow steps (full rebuild on every change)?
- Is there a documented way to run a single test file?

### D3 — Onboarding Documentation (weight: medium)

- Is there a `CONTRIBUTING.md`?
- Are architecture decisions documented (`docs/`, `ADRs/`, comments in key files)?
- Is the project purpose stated clearly in the first 100 words of README?
- Are external dependencies explained (why Redis? why Postgres vs SQLite?)?

### D4 — Test Feedback Loop (weight: medium)

- Is there a test runner configured (`npm test`, `pytest`, `cargo test`)?
- Can tests be run in watch mode?
- Is test output human-readable (not just exit codes)?
- Is coverage reported?

### D5 — Tooling Consistency (weight: medium)

- Is there a formatter configured (Prettier, Black, rustfmt)?
- Is there a linter configured (ESLint, flake8, clippy)?
- Are these run in CI (`.github/workflows/`)?
- Is there an `.editorconfig` for editor-agnostic style?

### D6 — Environment Reproducibility (weight: medium)

- Is there a lockfile (`package-lock.json`, `poetry.lock`, `Cargo.lock`)?
- Is there a `.nvmrc`, `.python-version`, or `rust-toolchain.toml`?
- Is there a `Dockerfile` or `docker-compose.yml` for consistent env?
- Are environment-specific configs separated from code?

### D7 — Error Clarity (weight: low)

- Do setup failures produce helpful error messages?
- Are common setup errors documented in README/CONTRIBUTING?
- Is there a `make doctor` or similar diagnostics command?

### D8 — Dependency Freshness (weight: low)

```bash
# Check for stale lockfiles or missing updates
if [ -f package.json ]; then
    npm outdated 2>/dev/null | head -10 || echo "(npm not available)"
fi
```

## Step 3 — Produce DX Scorecard

```
DX Review — <project-name> — <date>

Dimension                    Score   Weight    Weighted
─────────────────────────────────────────────────────
D1 First-Run Setup            4/5    high       8/10
D2 Local Dev Loop Speed       3/5    high       6/10
D3 Onboarding Documentation   2/5    medium     4/8
D4 Test Feedback Loop         4/5    medium     6/8 (not configured)
D5 Tooling Consistency        5/5    medium     6/8
D6 Environment Reproducibility 3/5   medium     4/8
D7 Error Clarity              2/5    low        2/4
D8 Dependency Freshness       4/5    low        3/4
─────────────────────────────────────────────────────
Overall DX Score: 72/100  (Good — room for improvement)
```

DX Grade:
- 90–100: Excellent — world-class DX
- 75–89: Good — minor friction points
- 60–74: Adequate — noticeable pain for new contributors
- Below 60: Needs work — onboarding is a barrier

## Step 4 — Quick Win Recommendations

Rank by (impact × effort⁻¹):

```
Quick Wins (high impact, low effort):
  1. Add .env.example with all variables documented [D1 +1 point, ~15 min]
  2. Add "Getting Started in 5 minutes" to README [D3 +1 point, ~30 min]
  3. Add `make doctor` to check prerequisites [D7 +2 points, ~1 hour]

Bigger Wins (high impact, higher effort):
  4. Configure Prettier + ESLint with pre-commit hook [D5 +2 points, ~2 hours]
  5. Add watch mode to test runner [D4 +1 point, ~1 hour]

Low Priority:
  6. Pin Node version in .nvmrc [D6 +0.5 points, ~5 min]
```

## Edge Cases

- **Monorepo**: audit each package's DX separately if they diverge significantly; flag inconsistencies
- **Internal tool**: weight D3 (docs) lower if there's only one consumer team
- **Open source project**: weight D1 and D3 higher (contributor onboarding is critical)
- **Greenfield**: some dimensions may be N/A; exclude from score rather than penalizing
- **CI not present**: note it as a gap but don't fail the audit
