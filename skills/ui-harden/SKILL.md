---
name: ui-harden
description: Production-readiness pass for UI — audits and fixes error states, empty states, text overflow, small touch targets, and i18n gaps before shipping
disable-model-invocation: false
risk: safe
---

# UI Harden

I'll audit UI components for production edge cases that look fine in happy-path demos but break under real-world conditions.

## Purpose

Catch the class of UI failures that only appear in production: long strings wrapping badly, empty database results with no state, truncated translated text, touch targets too small for thumbs.

## Usage

- `/ui-harden` — audit changed UI files
- `/ui-harden [file or directory]` — audit a specific target
- `/ui-harden --fix` — apply fixes automatically after audit

## Behavior

### Step 1 — Identify target files

```bash
git diff --name-only HEAD -- '*.tsx' '*.jsx' '*.html' '*.vue' '*.svelte'
```

If no changed UI files and no argument, ask for a target.

### Step 2 — Grep for known gaps

```bash
# No empty state handling
grep -rn "\.map(" --include="*.tsx" --include="*.jsx" | grep -v "empty\|length.*===.*0\|!.*length" | head -20

# No error boundary or error state
grep -rn "fetch\|axios\|useQuery\|useSWR" --include="*.tsx" | grep -v "error\|catch\|onError" | head -10

# Hardcoded strings (i18n gaps)
grep -rn '"[A-Z][a-zA-Z ]{4,}"' --include="*.tsx" --include="*.jsx" | grep -v "className\|id=\|data-\|aria-" | head -20

# Small touch targets (explicit small sizes)
grep -rn "w-[1-7]\b\|h-[1-7]\b\|width.*[1-3][0-9]px\|height.*[1-3][0-9]px" --include="*.tsx" --include="*.css" | head -10

# Text that can overflow without truncation
grep -rn "whitespace-nowrap\|overflow-hidden" --include="*.tsx" --include="*.css" | head -10
# Inverse: text nodes without overflow protection
grep -rn "<h[1-6]\|<p\b" --include="*.tsx" --include="*.jsx" | grep -v "truncate\|overflow\|ellipsis\|line-clamp" | head -20
```

### Step 3 — Read and analyze matched files

For each file with grep matches, read it and assess:

**Empty states** — does every list/table/grid have an empty state UI?
**Error states** — does every async operation have an error UI?
**Loading states** — does every async operation have a loading UI?
**Text overflow** — can all text strings handle 2× their expected length?
**Touch targets** — are all interactive elements ≥ 44×44px (or 48×48px for mobile-primary)?
**i18n** — are user-visible strings externalized or at least in a constants file?

### Step 4 — Report findings

Group by severity:
- **Missing** (no state handler at all): must fix before ship
- **Fragile** (state handled but breaks at edge): fix before ship
- **Deferred** (i18n not wired but strings centralized): acceptable with a note

If `--fix` flag:
- Add empty state JSX/HTML after each uncovered `.map()` call
- Add overflow protection (`overflow-hidden text-ellipsis` or `line-clamp`) to long-text nodes
- Add `min-h-[44px] min-w-[44px]` or equivalent to small interactive elements
- Read file before editing; apply all fixes in one Edit call per file

## Examples

```
/ui-harden src/components/UserTable.tsx
→ greps for missing states → reads file → reports empty/error/loading gaps

/ui-harden --fix
→ audits changed files → applies fixes automatically for clear-cut cases
```

## Token Optimization

**Expected range**: 400–1,500 tokens (grep + targeted reads)

**Early exit**: No UI files in scope → stop immediately.

**Patterns used**: Grep-before-Read, git diff scope default, progressive disclosure

## Edge Cases

- Component uses a design system with built-in empty states (e.g., `<DataTable>` with `emptyMessage` prop): flag as likely covered, note the prop to verify
- Test files in scope: skip `*.test.*` and `*.spec.*` files
- No async data fetching found: skip error/loading state checks

## Safety

Reads files before editing. For `--fix`, describe each change before applying it. Does not create or delete files.
