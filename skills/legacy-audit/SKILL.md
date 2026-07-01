---
name: legacy-audit
description: Map modernization opportunities in a legacy codebase — identify unsupported dependencies, architecture seams, and migration paths using strangler fig, adapter, and parallel-run patterns
disable-model-invocation: false
risk: safe
---

# Legacy Audit

Systematic modernization planning for codebases carrying technical debt. Maps what is actually risky vs merely old, identifies seams for incremental migration, and sequences candidates by cost/benefit.

## Usage

```
/legacy-audit                  # audit the full project
/legacy-audit <path>           # audit a specific service or directory
/legacy-audit --deps           # focus on dependency risk only
/legacy-audit --architecture   # focus on structural seams only
```

## Behavior

### Step 1 — Inventory the codebase age and health

```bash
# Language versions in use
node --version 2>/dev/null; python --version 2>/dev/null; java -version 2>/dev/null; go version 2>/dev/null

# File age distribution (years untouched)
git log --diff-filter=M --format="%ad" --date=format:"%Y" -- . | sort | uniq -c

# Oldest uncommitted files
find . -name "*.js" -o -name "*.py" -o -name "*.java" | \
  xargs git log --format="%ad %f" --date=short -- 2>/dev/null | \
  sort | head -20
```

### Step 2 — Audit dependency risk

```bash
# Node: check for outdated packages
npm outdated 2>/dev/null | head -20

# Python: check for outdated packages
pip list --outdated 2>/dev/null | head -20

# Check for explicitly deprecated or unmaintained packages
grep -rn "deprecated\|unmaintained\|no longer" node_modules/.package-lock.json \
  package-lock.json requirements.txt 2>/dev/null | head -10

# Find packages with known EOL (e.g., Node 14, Python 2, Java 8)
grep -rn "\"node\"\s*:\s*\"[<>]*[0-9]" package.json .nvmrc .node-version 2>/dev/null
```

Classify each dependency:
- **Critical risk**: EOL, no security patches, known CVEs
- **High risk**: Major version behind, breaking changes on upgrade path
- **Medium risk**: Minor/patch behind, deprecated APIs in use
- **Low risk**: Up to date, well-maintained

### Step 3 — Map architecture seams

Find natural split points where modernization can happen incrementally without rewriting everything:

```bash
# Find large, high-churn files (hardest to change, most valuable to refactor)
git log --format="%f" -- . | sort | uniq -c | sort -rn | head -20

# Find files with no tests (hardest to change safely)
find . -name "*.py" -o -name "*.ts" -o -name "*.js" | \
  grep -v test | grep -v spec | grep -v __test__ | wc -l

# Find circular dependencies (architecture entanglement)
npx madge --circular . 2>/dev/null | head -20
```

Identify:
- **Strangler seams**: HTTP endpoints or function interfaces where a new implementation can run alongside the old one
- **Adapter opportunities**: Abstraction boundaries where a compatibility layer would isolate change
- **Isolation walls**: Modules with clean interfaces that can be modernized independently
- **Big balls of mud**: Tightly coupled modules where any change touches everything — isolate last

### Step 4 — Score modernization candidates

For each candidate module or dependency, score:

| Factor | Weight | Score (1–5) |
|---|---|---|
| Risk if left alone (CVEs, EOL, fragility) | 40% | |
| Churn rate (how often it changes) | 25% | |
| Test coverage (safe to change?) | 20% | |
| Business value (how critical is it?) | 15% | |

**Priority = (Risk × 0.4) + (Churn × 0.25) + (Coverage × 0.20) + (Value × 0.15)**

### Step 5 — Recommend migration patterns

For each high-priority candidate, recommend the appropriate pattern:

| Pattern | When to use | Risk level |
|---|---|---|
| **Strangler fig** | HTTP service boundary exists; old and new can run in parallel | Low — route traffic gradually |
| **Branch by abstraction** | Internal module with multiple callers; extract interface first | Medium — all callers updated |
| **Parallel run** | High-stakes logic; run old and new, compare outputs before switching | Low — old path stays live |
| **Adapter / anti-corruption layer** | Wrapping an external system or legacy API you can't change | Low — isolates coupling |
| **Expand-contract** | Database schema change; add new column, migrate, remove old | Low — zero-downtime |
| **Big bang rewrite** | Module is so entangled that incremental change is impossible | High — only if all else fails |

### Step 6 — Output the modernization roadmap

```
LEGACY AUDIT — <path>

Dependency Risk
  CRITICAL  lodash@3.10.1        EOL; CVE-2021-23337 (prototype pollution)
  CRITICAL  Python 2.7           EOL since 2020-01-01; no security patches
  HIGH      express@4.17.1       express@5 available; breaking middleware API
  MEDIUM    moment@2.29.4        Deprecated in favor of date-fns or dayjs

Architecture Seams
  Strangler opportunity  src/api/routes.ts     Clean HTTP boundary; new service can shadow
  Adapter opportunity    src/db/queries.js     Raw SQL strings; wrap in repository interface
  Big ball of mud        src/legacy/core.js    1,400 lines, 0% test coverage, 47 callers

Modernization Roadmap (sequenced by priority score)

  Sprint 1 (do now — security)
    [ ] Upgrade lodash to ^4.17.21 (patch, no breaking changes)
    [ ] Pin Python 3.11; containerize to enforce version
    [ ] Run npm audit fix --force for CVE-2021-23337

  Sprint 2–3 (high value, safe to move)
    [ ] Wrap src/db/queries.js in repository interface (adapter pattern)
        → enables DB engine swap without touching business logic
    [ ] Replace moment with date-fns (direct API swap, no behavior change)

  Sprint 4–6 (structural — higher risk, higher reward)
    [ ] Strangler fig on /api/v1/orders → new service, traffic-shifted 10% → 100%
    [ ] Isolate src/legacy/core.js behind a facade before any internal changes
        → add characterization tests first (see /test-antipatterns for golden master pattern)

  Defer (not worth the risk/cost now)
    [ ] express@5 upgrade — breaking changes, low CVE risk, deprioritize
```

## Edge Cases

- **Greenfield with no legacy**: Report "No legacy patterns detected" and exit.
- **No git history**: Skip churn analysis; base seam detection on file size and coupling only.
- **Monorepo**: Audit each service separately; cross-service dependency risk appears in the shared packages layer.
- **No test coverage**: Always recommend adding characterization tests before migrating any big-ball-of-mud module.

## Token Optimization

**Expected range**: 600–2,000 tokens; 200–400 tokens (`--deps` or `--architecture` single-focus mode)

**Patterns used**: Bash for system queries (npm outdated, git log), grep-before-Read, progressive disclosure (risk summary → roadmap → per-item detail)

**Caching**: Caches dependency scan results in `.claude/cache/legacy-audit/deps.json` (invalidated when `package.json`, `requirements.txt`, or `go.mod` changes).

**Early exit**: If no files older than 2 years and all dependencies are current, report "No significant legacy risk detected" and exit.
