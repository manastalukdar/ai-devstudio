---
name: visual-ai-tells
description: Detect AI-generated UI patterns in CSS and component files — reports side-tab accents, gradient text, glassmorphism, bounce easing, template scaffolding, and monoculture font choices, then asks before removing anything
disable-model-invocation: false
risk: none
---

# Visual AI Tells

I'll scan UI files for specific CSS and HTML patterns that signal AI-generated or template-derived design, report each finding with a one-line explanation, then ask before removing anything.

## Purpose

Complements `/remove-ai-tells` (which targets written prose) by detecting the visual/CSS equivalent: patterns that appear when an AI generates frontend code from the same SaaS templates it was trained on. These are concrete, grep-detectable anti-patterns, not vague style judgments.

## Usage

- `/visual-ai-tells` — scan changed UI files
- `/visual-ai-tells [file or directory]` — scan a specific target
- `/visual-ai-tells --fix` — apply removals/replacements after report and user confirmation

## Behavior

### Step 1 — Identify target files

```bash
git diff --name-only HEAD -- '*.tsx' '*.jsx' '*.html' '*.css' '*.scss' '*.vue' '*.svelte'
```

If no changed UI files and no argument, ask for a target.

### Step 2 — Run pattern scan (grep only, no reads yet)

```bash
# Side-tab accent (colored border-left/right as card decoration)
grep -rn "border-left:.*[^0]px\|border-l-[2-9]\|border-left-[2-9]" \
  --include="*.css" --include="*.tsx" --include="*.jsx" | head -10

# Gradient text (background-clip: text)
grep -rn "background-clip.*text\|-webkit-background-clip.*text" \
  --include="*.css" --include="*.tsx" | head -10

# Glassmorphism (backdrop-filter blur on cards)
grep -rn "backdrop-filter.*blur\|backdrop-blur" \
  --include="*.css" --include="*.tsx" | head -10

# Bounce or elastic easing
grep -rn "bounce\|elastic\|cubic-bezier.*1\.[2-9]" \
  --include="*.css" --include="*.tsx" | head -10

# Inter as only font (monoculture)
grep -rn "'Inter'\|\"Inter\"" \
  --include="*.css" --include="*.tsx" --include="*.ts" | head -10

# 01/02/03 section numbering scaffolding
grep -rn '"0[1-9]"\|"[0-9][0-9]"\.' \
  --include="*.tsx" --include="*.jsx" | head -10

# Eyebrow-on-every-section (small tracked all-caps labels)
grep -rn "tracking-widest\|letter-spacing.*[3-9]px\|text-transform.*uppercase" \
  --include="*.tsx" --include="*.css" | head -15

# Hero metric template (large number + small label stacked)
grep -rn "text-[5-9]xl.*text-sm\|text-[5-9]xl.*text-xs\|[0-9]K+\|[0-9]M+" \
  --include="*.tsx" --include="*.jsx" | head -10

# Gray text on chromatic background (contrast trap)
grep -rn "text-gray\|text-slate\|text-zinc" \
  --include="*.tsx" | head -10

# Identical card grid (same card repeated with no variation)
grep -rn "\.map.*card\|\.map.*Card\|features\.map\|stats\.map\|items\.map" \
  --include="*.tsx" --include="*.jsx" | head -10

# Stripe background (repeating diagonal lines decoration)
grep -rn "repeating-linear-gradient\|stripes\|stripe-pattern" \
  --include="*.css" | head -10

# Decorative grid overlay
grep -rn "background.*grid\|bg-grid\|grid-pattern\|grid-background" \
  --include="*.css" --include="*.tsx" | head -10

# Over-rounded cards (≥ 24px radius signals template origin)
grep -rn "rounded-3xl\|rounded-\[2[4-9]px\]\|border-radius.*2[4-9]px\|border-radius.*[3-9][0-9]px" \
  --include="*.css" --include="*.tsx" | head -10
```

### Step 3 — Report findings

For each pattern with matches, report:
```
[PATTERN-NAME] file:line
  What it is: one sentence
  Why it signals AI/template origin: one sentence
  Suggested replacement: one sentence
```

Group by category:
- **Decorative overuse** (glassmorphism, gradient text, stripe backgrounds)
- **Template scaffolding** (01/02/03 numbering, hero metrics, eyebrows on every section)
- **Motion problems** (bounce/elastic easing)
- **Font monoculture** (Inter everywhere)
- **Structural tells** (over-rounded cards, identical card grids, side-tab accents)

End with: "Found N visual AI tells across M files. Remove/replace them? [y/n/select]"

### Step 4 — Apply fixes (with `--fix` or after confirmation)

For each confirmed finding:
1. Read the file
2. Apply the fix:
   - Side-tab accent → remove or convert to `border-left: 3px solid transparent` (invisible by default)
   - Gradient text → plain text color
   - Glassmorphism → solid background with appropriate opacity
   - Bounce easing → `ease-out`
   - 01/02/03 numbering → remove or replace with semantic icons
   - Eyebrow → demote to subtitle or remove
   - Over-rounded cards → `border-radius: 8px` or `border-radius: 12px`

## Examples

```
/visual-ai-tells src/
→ finds gradient text on 2 headings, bounce easing on modal, 01/02/03 section numbers
→ reports each, asks before fixing

/visual-ai-tells --fix
→ scans changed files → reports → applies all approved fixes
```

## Token Optimization

**Expected range**: 200–600 tokens (grep only, detection phase), 400–1,200 tokens (detection + fixes)

**Early exit**: If all greps return no matches → "No visual AI tells found" and stop immediately.

**Two-phase design**: Detection (Steps 1–3) always runs cheaply via grep. Fixes (Step 4) only run after user confirms in Step 3.

**Patterns used**: Grep-before-Read, early exit, progressive disclosure

## Edge Cases

- Intentional glassmorphism (documented in design brief): skip with a note
- Inter as part of a deliberate system (paired with a display font): flag but note context
- Dark-mode `backdrop-blur` for accessibility (blur on overlay to separate from content): flag but note valid use case

## Safety

Detection is read-only. Fixes read files before editing. Does not apply any changes without user confirmation.
