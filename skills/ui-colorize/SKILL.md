---
name: ui-colorize
description: Introduce strategic color to monochromatic or under-colored UIs — OKLCH-first palette generation with contrast validation, register-aware strategy, and specific anti-pattern warnings
disable-model-invocation: false
risk: safe
---

# UI Colorize

I'll audit the color usage in your UI, identify where color is absent or arbitrary, and propose a coherent palette with OKLCH coordinates and WCAG AA contrast ratios.

## Purpose

Monochromatic UIs feel flat; arbitrary color feels amateurish. This skill introduces color strategically — anchored to a single hue, expressed with OKLCH for perceptual consistency, and validated for accessibility.

## Usage

- `/ui-colorize` — audit changed UI files and propose color additions
- `/ui-colorize [file]` — target a specific file
- `/ui-colorize --apply` — apply proposed palette to files after user approval

## Behavior

### Step 1 — Detect existing color usage

```bash
# Find current color values
grep -rn "#[0-9a-fA-F]\{3,8\}\|rgb(\|hsl(\|oklch(\|color:" \
  --include="*.css" --include="*.scss" --include="*.tsx" | head -30

# Check for design system color tokens
grep -rn "primary\|secondary\|accent\|brand\|surface\|muted" \
  --include="*.css" --include="tailwind.config*" | head -20

# Check for the cream/sand/beige trap
grep -rni "cream\|sand\|beige\|bone\|ivory\|eggshell\|#f[5-9][e-f][0-9a-f]\{2\}" \
  --include="*.css" --include="*.scss" | head -10
```

Read the shape brief if present (`.claude/cache/ui-shape/`).

### Step 2 — Assess color health

Report:
- **Total unique colors found**: N
- **On a systematic scale?** Yes/No (are values drawn from a consistent set?)
- **Contrast failures?** Check text/background pairs
- **Cream trap detected?** Flag explicitly if colors fall in OKLCH L 0.84–0.97, C < 0.06, hue 40–100 (warm white that looks clinical under artificial light)
- **Missing color?** Is the UI entirely gray with no accent or brand signal?

### Step 3 — Propose palette

Based on register (from shape brief or inferred from file context):

**Brand register palette:**
```
Anchor hue: oklch(L C H) — one primary brand color
Light surface: oklch(0.98 0.005 H) — near-white with hue tint (not pure white, not cream)
Dark surface: oklch(0.15 0.01 H) — near-black with hue tint
Accent: oklch(L C H+120) — complementary, used sparingly (CTAs, highlights)
Status: standard red/amber/green in OKLCH
```

**Product register palette:**
```
Neutral surface hierarchy: oklch(0.99 0 0) → oklch(0.95 0 0) → oklch(0.90 0 0)
Single accent: oklch(0.55 0.18 H) — one purposeful color for primary actions
Status: oklch red/amber/green (accessible by default in OKLCH)
No decorative color
```

For each proposed color, state:
- OKLCH coordinates
- Hex equivalent
- Contrast ratio against white and black surfaces
- Intended use

### Step 4 — Apply (with `--apply` flag or user confirmation)

1. Propose changes as CSS custom properties
2. Read affected files
3. Apply in one Edit per file

```css
:root {
  --color-brand: oklch(0.55 0.18 255);
  --color-surface: oklch(0.98 0.005 255);
  --color-surface-muted: oklch(0.94 0.008 255);
  --color-text: oklch(0.15 0.01 255);
  --color-accent: oklch(0.60 0.20 195);
}
```

## Examples

```
/ui-colorize src/styles/globals.css
→ finds 47 unique hex values, no system → proposes 6-token OKLCH palette

/ui-colorize --apply
→ proposes palette → waits for approval → applies to CSS files
```

## Token Optimization

**Expected range**: 500–1,500 tokens

**Early exit**: If palette already uses OKLCH custom properties and passes contrast checks, report "Color system looks healthy" and stop.

**Patterns used**: Grep-before-Read, progressive disclosure (audit → propose → apply in stages)

## Edge Cases

- Dark mode: propose both light and dark surface tokens; check contrast for both
- Design system already configured (Tailwind color scale): extend it rather than replace; propose additions only
- No CSS files (CSS-in-JS): propose palette as a theme object constant

## Safety

Does not apply any color changes without user confirmation. Reads files before editing.
