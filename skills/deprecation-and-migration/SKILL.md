---
name: deprecation-and-migration
description: Full deprecation lifecycle for APIs, features, or internal code — Hyrum's Law analysis, deprecation notices, migration path design, and parallel-run execution strategy.
disable-model-invocation: false
risk: safe
---

# Deprecation and Migration

I'll help you retire code responsibly: assess the real blast radius using Hyrum's Law, write deprecation notices that callers can act on, design a migration path that is safe under concurrent usage, and execute a parallel-run strategy.

Arguments: `$ARGUMENTS` — the API, function, feature, or module to deprecate

## Token Optimization

**Expected range**: 500–2,000 tokens depending on codebase size

**Patterns used**: Grep-before-Read (find all callsites before reading files), git diff scope (only changed files)

**Early exit**: If no callers are found, report "No callers detected — safe to delete without migration path"

## Step 1 — Hyrum's Law Analysis

Before deciding what to deprecate, find everything that depends on the current behavior — including behavior that is not part of the documented contract:

```bash
# Find direct callsites
grep -rn "<symbol>" --include="*.ts" --include="*.js" --include="*.py" . | grep -v "node_modules\|dist\|build"

# Find indirect usage (via re-exports, dynamic require, etc.)
grep -rn "require\|import" . | grep "<module>" | grep -v "node_modules"

# Check for string-based usage (event names, config keys, URL paths)
grep -rn '"<symbol>"\|'"'"'<symbol>'"'" . | grep -v "node_modules"
```

Report:
```
Callsites found: [N] across [M] files
  [file:line] — [usage type: direct / indirect / string-based]
  ...

Hidden behavioral dependencies (Hyrum's Law risks):
  - [behavior callers may rely on that is not documented]
  - [e.g., error message format, return value order, side effects]
```

## Step 2 — Migration Cost Assessment

For each callsite, classify migration effort:

- **Trivial** — 1:1 rename or import change
- **Moderate** — signature change requiring caller updates
- **Complex** — behavioral change requiring caller logic changes
- **Risky** — caller crosses a team/service boundary; needs coordination

```
Migration effort breakdown:
  Trivial:  [N] callsites
  Moderate: [N] callsites
  Complex:  [N] callsites
  Risky:    [N] callsites — requires coordination with: [owners]

Estimated total effort: [S/M/L/XL]
Recommendation: [deprecate / deprecate-with-shim / redesign / do-not-deprecate]
```

## Step 3 — Write Deprecation Notice

Add deprecation markers at each callsite definition:

```typescript
/**
 * @deprecated Since [version/date]. Use [replacement] instead.
 * Migration guide: [docs link or inline steps]
 * Removal planned: [version/date]
 */
```

For runtime warnings (when appropriate):

```python
import warnings
warnings.warn(
    "function_name is deprecated. Use replacement instead. "
    "See: [migration guide URL]",
    DeprecationWarning,
    stacklevel=2,
)
```

## Step 4 — Design Migration Path

Produce a migration guide covering:

1. **What changes**: old API vs new API (side-by-side comparison)
2. **How to migrate**: step-by-step instructions a caller can follow
3. **Caveats**: behavioral differences, edge cases, timing constraints
4. **Rollback**: how to revert if migration causes problems

Save to `docs/migrations/<slug>.md` if a `docs/` directory exists.

## Step 5 — Parallel-Run Strategy

For high-risk migrations, implement a parallel run before removing the old path:

```
Parallel run plan:
  Phase 1 — Dual write:  write to both old and new path; read from old
  Phase 2 — Shadow read: write to both; read from new; compare results
  Phase 3 — Cutover:     write to new only; remove old path after [N] days
  Phase 4 — Cleanup:     delete old path and migration shim
```

Define explicit success criteria and rollback triggers for each phase.

## Edge Cases

- **No replacement exists yet**: design the replacement before deprecating; do not deprecate into a void
- **Cross-service dependency**: coordinate with the owner of each external callsite before marking deprecated
- **Public API / SDK**: follow semver — deprecation in minor release, removal in next major only
- **Database column or schema**: migration requires a data migration script and a maintenance window; flag this explicitly
