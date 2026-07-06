---
name: ui-typeset
description: Fix typography hierarchy, font choices, type scale, and line-length in UI files — applies register-aware rules (brand vs product) with concrete CSS fixes
disable-model-invocation: false
risk: safe
---

# UI Typeset

I'll audit the typography in your UI files and apply concrete fixes for hierarchy, scale, readability, and font choice.

## Purpose

Typography is the most common source of "looks cheap" feedback. This skill catches the specific failures that make UIs look unpolished: skipped heading levels, inconsistent scale, Inter-everywhere default, and lines too wide to read comfortably.

## Usage

- `/ui-typeset` — audit and fix changed UI files
- `/ui-typeset [file]` — audit a specific file
- `/ui-typeset --audit` — report only, no fixes

## Behavior

### Step 1 — Detect register and existing type system

```bash
# Check for design tokens / existing type scale
grep -rn "font-size\|text-[a-z]\|typography\|typeScale\|fontSize" \
  --include="*.css" --include="*.scss" --include="*.ts" \
  --include="tailwind.config*" | head -20

# Check fonts in use
grep -rn "font-family\|fontFamily\|google.*font\|@font-face\|next/font" \
  --include="*.css" --include="*.tsx" --include="*.ts" | head -10
```

Read the shape brief if present (`.claude/cache/ui-shape/`) to determine register.

### Step 2 — Grep for typography issues in target files

```bash
# Skipped heading levels (h1 → h3 with no h2)
grep -rn "<h[1-6]" --include="*.tsx" --include="*.jsx" --include="*.html" | sort

# Hardcoded pixel font sizes (prefer rem/em/clamp)
grep -rn "font-size.*[0-9]px" --include="*.css" --include="*.scss" | head -20

# Line length without max-width (prose text nodes)
grep -rn "<p\b\|prose\|body-text\|description" --include="*.tsx" --include="*.jsx" | \
  grep -v "max-w\|max-width\|ch\b" | head -15

# Inter as the sole font (check for overreliance)
grep -rn "Inter\b" --include="*.css" --include="*.tsx" --include="*.ts" | head -10
```

### Step 3 — Read matched files and assess

For each file, check:

**Heading hierarchy** — levels must be sequential; `h1 → h2 → h3`, never skipping.
**Type scale** — is there a consistent scale (e.g., Tailwind text-sm/base/lg/xl, or a custom scale)? Arbitrary one-off sizes are a smell.
**Line length** — prose text should have `max-width: 65ch` or `max-width: 75ch`. Wider than 80ch reduces readability.
**Font stack**:
  - Brand register: expressive display font for headings is appropriate; body should be readable
  - Product register: system font stack preferred; Inter is acceptable but `font-system` or `ui-sans-serif` costs nothing and looks native

**Line height** — body text line-height should be 1.5–1.75; headings 1.1–1.3.

### Step 4 — Apply fixes

For each finding:
1. Describe the fix
2. Read the file
3. Apply the fix

Common fixes:
```css
/* Line length */
.prose { max-width: 65ch; }

/* System font stack */
font-family: ui-sans-serif, system-ui, -apple-system, sans-serif;

/* Fluid type scale (brand register) */
font-size: clamp(1rem, 2.5vw, 1.5rem);
```

If `--audit` flag: report findings only, no edits.

## Examples

```
/ui-typeset src/pages/Landing.tsx
→ detects Inter-only, no line-length cap on hero copy → fixes both

/ui-typeset --audit
→ reports all typography issues in changed files without editing
```

## Token Optimization

**Expected range**: 400–1,200 tokens (grep + targeted reads + fixes)

**Early exit**: No CSS/UI files in scope → stop.

**Patterns used**: Grep-before-Read, git diff scope default, early exit

## Edge Cases

- Project uses a design system (Tailwind, MUI, Chakra): note configured scale instead of proposing raw CSS
- No heading elements found: skip hierarchy check, note it in output
- Font loaded via CDN (Google Fonts): note that `next/font` or `@font-face` self-hosting improves performance

## Safety

Reads files before editing. Does not modify `package.json`, `tailwind.config.*`, or global design token files without explicit user confirmation.
