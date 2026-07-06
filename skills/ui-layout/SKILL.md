---
name: ui-layout
description: Fix spacing rhythm, visual hierarchy, and layout issues in UI files — enforces consistent spacing units, adequate padding on interactive elements, and proper visual weight distribution
disable-model-invocation: false
risk: safe
---

# UI Layout

I'll audit the spacing, rhythm, and visual hierarchy in your UI and apply concrete fixes to make it feel intentional rather than arbitrary.

## Purpose

Inconsistent spacing is the second most common source of "looks unfinished" feedback after typography. This skill detects arbitrary spacing values, cramped interactive elements, and hierarchy failures where visual weight doesn't match content importance.

## Usage

- `/ui-layout` — audit and fix changed UI files
- `/ui-layout [file]` — audit a specific file
- `/ui-layout --audit` — report only, no fixes

## Behavior

### Step 1 — Detect spacing system

```bash
# Check for spacing scale (Tailwind, custom tokens, CSS vars)
grep -rn "spacing\|gap\|padding\|margin" \
  --include="tailwind.config*" --include="*.css" --include="*.scss" | head -15

# Check for CSS custom properties (design tokens)
grep -rn "^\s*--space\|^\s*--gap\|^\s*--padding" --include="*.css" | head -10
```

### Step 2 — Grep for layout issues

```bash
# Cramped padding on interactive elements (< 8px)
grep -rn "p-0\b\|p-1\b\|padding.*[0-7]px\|py-0\|px-0\|py-1\b\|px-1\b" \
  --include="*.tsx" --include="*.jsx" --include="*.html" | head -20

# Arbitrary magic-number spacing (not on a scale)
grep -rn "margin.*[^0-9][3-9][13579]px\|padding.*[^0-9][3-9][13579]px" \
  --include="*.css" --include="*.scss" | head -15

# Nested cards (cards inside cards — common AI pattern)
grep -rn "card.*card\|rounded.*shadow.*rounded.*shadow" \
  --include="*.tsx" --include="*.jsx" | head -10

# Elements competing for visual prominence (too many bold/large)
grep -rn "font-bold\|font-semibold\|text-xl\|text-2xl" \
  --include="*.tsx" --include="*.jsx" | wc -l
```

### Step 3 — Read matched files and assess

**Spacing rhythm** — are spacing values drawn from a consistent scale (multiples of 4px or 8px)? Arbitrary values like 13px or 37px break the rhythm.

**Padding adequacy** — interactive elements need ≥ 8px padding on all sides; primary buttons need ≥ 12px vertical.

**Visual hierarchy** — count high-prominence elements (bold, large text, colored backgrounds). If > 30% of visible elements are prominent, hierarchy has collapsed.

**Nested cards** — cards inside cards add visual noise. Flag instances where a card already has a `shadow` and contains a child with another `shadow` or `border`.

**Breathing room** — sections need consistent vertical rhythm. If top-level sections use inconsistent `mb-` or `mt-` values, standardize to the nearest scale step.

### Step 4 — Apply fixes

For each issue:
1. Read the file
2. Apply the fix in one Edit call per file

Common fixes:
```css
/* Bring arbitrary spacing onto scale */
padding: 13px → padding: 12px (3 × 4px scale)

/* Cramped button */
.btn { padding: 8px 16px; } /* minimum */

/* Break nested card */
/* Remove inner shadow, use border instead */
box-shadow: none;
border: 1px solid var(--color-border);
```

If `--audit` flag: report findings only.

## Examples

```
/ui-layout src/components/Sidebar.tsx
→ finds cramped nav items (p-1), nested card shadows → fixes both

/ui-layout --audit
→ reports hierarchy and spacing issues in changed files without editing
```

## Token Optimization

**Expected range**: 400–1,200 tokens

**Early exit**: No UI files in scope → stop.

**Patterns used**: Grep-before-Read, git diff scope default

## Edge Cases

- Tailwind project: map Tailwind spacing classes to pixel values before assessing scale consistency
- CSS-in-JS (styled-components, Emotion): grep for template literal spacing values
- Dense data tables: cramped padding is intentional; flag only if padding < 4px

## Safety

Reads files before editing. Does not modify global design token files without user confirmation.
