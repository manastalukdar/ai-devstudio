---
name: dep-sweep
description: Proactively discover outdated and vulnerable dependencies, apply patch and safe minor updates in isolation, verify with tests, and escalate major bumps and high-severity CVEs to a human. Designed to run with /loop 6h or /loop 1d.
disable-model-invocation: false
risk: safe
---

# Dependency Sweep

Active loop-driven dependency maintenance. Unlike `/dependency-audit` (which reports risk), this skill applies safe updates, verifies them in isolation, and escalates anything risky — closing the loop without waiting for human intervention on routine bumps.

## Usage

```
/dep-sweep                        # sweep all dependency files
/dep-sweep --ecosystem npm        # target a specific ecosystem
/dep-sweep --patch-only           # only apply patch-level updates
/dep-sweep --report-only          # surface findings without applying any changes
```

Run on a loop for continuous maintenance:
```
/loop 6h /dep-sweep --patch-only
/loop 1d /dep-sweep
```

## Behavior

### Step 1 — Detect ecosystems

```bash
[ -f "package.json" ]      && echo "npm"
[ -f "requirements.txt" ] || [ -f "pyproject.toml" ] && echo "python"
[ -f "go.mod" ]            && echo "go"
[ -f "Gemfile" ]           && echo "ruby"
[ -f "pom.xml" ]           && echo "java-maven"
[ -f "build.gradle" ]      && echo "java-gradle"
```

### Step 2 — Scan for outdated packages

**npm:**
```bash
npm outdated --json 2>/dev/null | jq 'to_entries[] | {name: .key, current: .value.current, wanted: .value.wanted, latest: .value.latest}'
npm audit --json 2>/dev/null | jq '.vulnerabilities | to_entries[] | {name: .key, severity: .value.severity, fixAvailable: .value.fixAvailable}'
```

**Python:**
```bash
pip list --outdated --format=json 2>/dev/null
pip-audit --format=json 2>/dev/null 2>/dev/null || safety check --json 2>/dev/null
```

**Go:**
```bash
go list -m -u -json all 2>/dev/null | jq 'select(.Update != null) | {module: .Path, current: .Version, update: .Update.Version}'
govulncheck ./... 2>/dev/null | head -40
```

### Step 3 — Risk classify each package

| Category | Criteria | Action |
|---|---|---|
| **Safe** | Patch bump, no CVE, no breaking changes | Apply automatically |
| **Cautious** | Minor bump, no CVE | Apply with test verification |
| **High risk** | Major bump OR high/critical CVE | Escalate to human |
| **Denylist** | Packages in project denylist | Never touch automatically |

```bash
# Check project denylist
DENYLIST_FILE=".claude/dep-sweep-denylist.txt"
[ -f "$DENYLIST_FILE" ] && DENYLIST=$(cat "$DENYLIST_FILE") || DENYLIST=""

# Check if a package is on denylist
echo "$DENYLIST" | grep -qw "$PACKAGE_NAME" && echo "SKIP (denylist)"
```

### Step 4 — Apply safe updates in isolation

For each safe/cautious package:

```bash
# Create an isolated branch for the update
git checkout -b "dep-sweep/$(date +%Y%m%d)-$PACKAGE_NAME" main

# Apply the update
case $ECOSYSTEM in
  npm)    npm install "$PACKAGE_NAME@$NEW_VERSION" ;;
  python) pip install "$PACKAGE_NAME==$NEW_VERSION" && pip freeze > requirements.txt ;;
  go)     go get "$MODULE_PATH@$NEW_VERSION" && go mod tidy ;;
esac
```

### Step 5 — Verify in isolation

After each update:

```bash
# Run the full test suite
case $ECOSYSTEM in
  npm)    npm test 2>&1 | tail -20 ;;
  python) python -m pytest -x -q 2>&1 | tail -20 ;;
  go)     go test ./... 2>&1 | tail -20 ;;
esac

# Run build if applicable
case $ECOSYSTEM in
  npm)    npm run build 2>&1 | tail -10 ;;
  python) python -c "import $PACKAGE_NAME" 2>/dev/null ;;
esac
```

**Tests fail** → discard branch, note failure, move to next package. Do not escalate failed patch updates — they are not safe, move to cautious/risky tier.

**Tests pass** → commit the update:

```bash
git add package.json package-lock.json  # or equivalent
git commit -m "chore(deps): bump $PACKAGE_NAME from $OLD_VERSION to $NEW_VERSION"
```

### Step 6 — Escalate risky updates

For major bumps, high/critical CVEs, or test failures on minor bumps:

```
ESCALATION REQUIRED — human decision needed

Package: express (npm)
Current: 4.18.2  →  Latest: 5.0.0 (MAJOR)
CVE: none
Risk: Major version — breaking middleware API changes
Breaking changes summary: [link to changelog]

Suggested action: Review migration guide, update incrementally
Do NOT apply automatically.
```

For critical CVEs with no safe fix available:

```
CRITICAL CVE — immediate human attention needed

Package: lodash
CVE: CVE-2021-23337 (prototype pollution, CVSS 7.2)
Fix: upgrade to 4.17.21 (patch — safe to apply)
Status: Fix available → applying automatically in next sweep
```

### Step 7 — Report

```
DEP SWEEP — 2026-06-30 (npm + python)

Applied automatically (3)
  lodash         4.17.20 → 4.17.21   patch   CVE-2021-23337 fixed   tests: ✓
  date-fns       3.6.0   → 3.6.1     patch   no CVE                 tests: ✓
  httpx          0.26.0  → 0.27.0    minor   no CVE                 tests: ✓

Escalated to human (2)
  express        4.18.2  → 5.0.0     MAJOR   breaking API changes
  cryptography   41.0.0  → 42.0.0    MAJOR   OpenSSL binding changes

Skipped — denylist (1)
  stripe         (pinned by team decision, see dep-sweep-denylist.txt)

No action needed (14 packages up to date)

Branches created: dep-sweep/20260630-lodash, dep-sweep/20260630-date-fns, dep-sweep/20260630-httpx
Next sweep: 6h
```

## Edge Cases

- **No package manager found**: Report which files were checked and exit.
- **Tests don't exist**: Apply patch updates with a warning; escalate minor and above.
- **Monorepo**: Sweep each workspace independently; commit per-workspace.
- **Lockfile-only projects**: Update lockfile using the appropriate command (`npm ci`, `pip-compile`, etc.).
- **CI will verify**: If the project has CI that runs on push, prefer opening PRs over direct commits so CI validates the update.

## Token Optimization

**Expected range**: 500–1,500 tokens (multi-ecosystem scan); 100–200 tokens (all up to date, early exit)

**Patterns used**: Bash (npm/pip/go CLI), early exit (nothing outdated), progressive disclosure (summary → per-package detail on request), attempt isolation (separate branch per update)

**Caching**: Caches scan results in `.claude/cache/dep-sweep/last-scan.json` (invalidated when lockfiles change). Caches denylist from `.claude/dep-sweep-denylist.txt`.

**Early exit**: All packages up to date and no CVEs → single-line report and exit.
