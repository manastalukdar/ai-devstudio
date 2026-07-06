---
name: ui-animate
description: Add purposeful animations and transitions to UI — enforces motion budget, bans bounce/elastic easing, and requires prefers-reduced-motion fallbacks on every animated element
disable-model-invocation: false
risk: safe
---

# UI Animate

I'll add purposeful motion to your UI within a register-appropriate budget, using physically plausible easing and mandatory reduced-motion fallbacks.

## Purpose

Motion communicates state changes and spatial relationships. This skill adds animation where it aids comprehension, removes animation where it distracts, and ensures every animated element degrades gracefully for users who request reduced motion.

## Usage

- `/ui-animate` — audit changed UI files and add missing transitions; flag problematic animations
- `/ui-animate [file]` — target a specific file
- `/ui-animate --audit` — report only, no edits

## Behavior

### Step 1 — Audit existing animations

```bash
# Find all animation declarations
grep -rn "animation\|transition\|@keyframes\|motion\|animate-" \
  --include="*.css" --include="*.scss" --include="*.tsx" | head -30

# Find bounce/elastic easing (physically implausible)
grep -rn "bounce\|elastic\|cubic-bezier.*1\.[2-9]\|spring\|overshoot" \
  --include="*.css" --include="*.tsx" | head -15

# Find missing reduced-motion fallbacks
grep -rn "animation\|transition" --include="*.css" | head -20
# Then check if prefers-reduced-motion is in the same file:
grep -rn "prefers-reduced-motion" --include="*.css" | head -10
```

### Step 2 — Assess motion budget (from shape brief or inferred)

**Brand register**: transitions up to 400ms, entrance animations permitted, expressive easing allowed
**Product register**: transitions ≤ 150ms only, no decorative motion, every animation must serve task clarity

### Step 3 — Flag problematic patterns

Report each as a finding:

- **Bounce/elastic easing** — replace with `ease-out` or a gentle `cubic-bezier(0.16, 1, 0.3, 1)`
- **Animations > 400ms** (brand) or **> 200ms** (product) — overly slow, feels unresponsive
- **`animation: none` missing in `@media (prefers-reduced-motion: reduce)`** — accessibility failure
- **Animating layout properties** (`width`, `height`, `top`, `left`) — use `transform` instead for GPU compositing
- **Infinite loops** (`animation-iteration-count: infinite`) on non-background elements — distracting

### Step 4 — Add purposeful transitions

For elements that would benefit from motion but have none:

**State transitions** (hover, focus, active, disabled):
```css
/* Button */
.btn {
  transition: background-color 120ms ease-out, transform 80ms ease-out;
}
.btn:active { transform: scale(0.97); }

@media (prefers-reduced-motion: reduce) {
  .btn { transition: none; }
}
```

**Entrance animations** (brand register only, on mount):
```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.hero { animation: fade-up 300ms ease-out; }

@media (prefers-reduced-motion: reduce) {
  .hero { animation: none; }
}
```

**Skeleton/loading states** (product register):
```css
@keyframes shimmer {
  from { background-position: -200% 0; }
  to   { background-position: 200% 0; }
}
@media (prefers-reduced-motion: reduce) {
  .skeleton { animation: none; background: var(--color-surface-muted); }
}
```

### Step 5 — Apply fixes

Read each file, apply changes. Every new animation block must include a `@media (prefers-reduced-motion: reduce)` counterpart.

If `--audit` flag: report findings only.

## Examples

```
/ui-animate src/components/Modal.tsx
→ finds no open/close transition → adds opacity + scale entrance, reduced-motion fallback

/ui-animate --audit
→ flags bounce easing on 3 elements, missing reduced-motion on 5 animations
```

## Token Optimization

**Expected range**: 400–1,200 tokens

**Early exit**: If all animations already have `prefers-reduced-motion` fallbacks and use valid easing → "Motion looks good" and stop.

**Patterns used**: Grep-before-Read, early exit, git diff scope default

## Edge Cases

- Framer Motion / React Spring: note equivalent APIs instead of raw CSS (`reduceMotion` hook, `useReducedMotion`)
- CSS Modules: apply fixes in the `.module.css` file, not inline
- Tailwind: use `motion-safe:` and `motion-reduce:` variants

## Safety

Reads files before editing. Does not remove existing animations without reporting them as findings first.
