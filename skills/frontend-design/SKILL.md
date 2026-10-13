---
name: frontend-design
description: Design-lead guidance for building distinctive UI — avoids AI defaults, applies deliberate typography, color, and layout choices
disable-model-invocation: false
risk: none
---

# Frontend Design

Act as a design lead. Give each project a distinct visual identity rather than reaching for templated AI defaults.

## Purpose

Help build new or existing UI with deliberate aesthetic choices grounded in the product's subject matter.

## Usage

`/frontend-design [component or page description]`

## Process

### Phase 1 — Ground the design

Before touching code or tokens:

1. **Identify the subject**: Industry, audience, vernacular. If the brief doesn't name it, propose one and confirm.
2. **Define the hero**: The most characteristic element of the subject's world — open with it. Avoid defaulting to big numbers, small labels, and gradient accents unless genuinely the best fit.
3. **Draft the token plan**: Commit to:
   - Color: 1 primary, 1 accent, neutral ramp, semantic states
   - Type: 1–2 clearly distinct typefaces, explicit type scale
   - Layout: grid, spacing rhythm, container widths
   - Principles: 2–3 design constraints specific to this subject

### Phase 2 — Review the plan

Before building, check the plan against these questions:

- Does the color choice feel generic? (cream + terracotta, near-black + acid-green → try harder)
- Are all cards the same rounded rectangle? Break the grid.
- Are there tracked-out eyebrow labels? Replace with structure.
- Is there a middle-dot meta string? Find a better separator.
- Does every link end with "→"? Pick a different affordance.
- Are data labels in monospace by default? Use it only when alignment demands it.

### Phase 3 — Build

Implement from the token plan. Keep one element memorable; let the rest be quiet.

**Typography rules:**
- One or two typefaces, clearly distinct from each other
- Treat type as an active design element, not filler
- No single-word headline accents or unnecessary all-caps labels
- Line length: under ~80 characters
- Serif body text: slightly more line-height than sans-serif

**Structure rules:**
- Borders, numbering, dividers must encode real information
- Numbered markers only for actual sequences
- Avoid decorative dividers that carry no meaning

**Motion rules:**
- One orchestrated moment — not scattered micro-animations
- Motion responds to user actions, not page load by default
- Always respect `prefers-reduced-motion`

**Copy rules:**
- Write from the user's perspective
- Active voice, consistent action names
- Errors and empty states give clear next steps

**Quality floor** (non-negotiable):
- Responsive at mobile widths
- Keyboard focus visible on all interactive elements
- Color contrast meets WCAG AA
- `prefers-reduced-motion` respected

### Phase 4 — Self-critique

After building, review against the plan:

- Does it feel like the subject's world, or like a generic SaaS?
- Is there one memorable element?
- Check CSS specificity conflicts, especially around section spacing.
- Fix any token drift (hard-coded colors instead of variables).

## Common defaults to avoid

| Default | Better |
|---|---|
| Cream background + terracotta accent | Something grounded in the subject |
| Near-black + acid-green | Use if it fits; pick something else if not |
| Identical rounded card grid | Break the grid where content allows |
| Tracked-out eyebrow labels | Encode hierarchy through scale and weight |
| Middle-dot meta strings | Find a layout that doesn't need a separator |
| "→" on every link | Pick one affordance and commit to it |
| Monospace data labels everywhere | Reserve for alignment-critical numerics |
| Single-word headline accent spans | Let the full headline do the work |

## Token Optimization

**Expected range**: 300–600 tokens (initial), 50 tokens (cache hit)

**Patterns used**: Progressive disclosure — plan phase returns token summary; build phase is separate invocation

**Early exit**: If no subject can be identified from the brief and user declines to propose one, return a subject-first prompt rather than a generic design.
