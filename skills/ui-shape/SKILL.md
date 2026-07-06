---
name: ui-shape
description: Design planning interview before writing UI code — produces a design brief covering register, typography strategy, color constraints, and motion budget to prevent costly rework
disable-model-invocation: false
risk: none
---

# UI Shape

I'll run a focused design planning interview before any code is written, then produce a concrete design brief that guides implementation.

## Purpose

Capture design intent upfront so the implementation has a clear target. Prevents the common failure mode of building first and fixing visual quality later at high cost.

## Usage

- `/ui-shape` — interview for the current feature/file context
- `/ui-shape [feature description]` — interview for a specific feature
- `/ui-shape --brief` — skip interview, generate brief from existing code/context

## Behavior

### Step 1 — Determine scope

```bash
# If argument provided, use it. Otherwise check for active file or git diff.
git diff --name-only HEAD -- '*.tsx' '*.jsx' '*.html' '*.css' '*.vue' '*.svelte' | head -10
```

If no UI files in scope and no argument, ask: "What feature or screen are we designing?"

### Step 2 — Register interview (3 questions max)

Ask these in sequence, stopping early if the answers make the rest obvious:

1. **Register**: "Is the design itself the product (marketing site, landing page) or does it serve a product (app UI, dashboard, form)?" — *Brand* vs *Product* register drives every downstream choice.

2. **Audience signal**: "Who is the primary user, and what is their task context?" (e.g., executive scanning metrics, developer debugging, consumer browsing)

3. **Personality** (brand register only): "Three words that describe the intended feeling?" (e.g., precise / editorial / restrained)

Skip question 3 for product-register UIs — personality is secondary to task clarity.

### Step 3 — Generate design brief

Output a structured brief with these sections:

**Register**: Brand | Product
**Audience**: one sentence
**Typography**:
- Brand register: fluid `clamp()` scale, expressive weights permitted, 1–2 typefaces max
- Product register: fixed `rem` scale, system font stack preferred, high density acceptable

**Color strategy**:
- Specify OKLCH as the working color space
- Brand: 1 anchor hue + neutral + up to 2 accents
- Product: functional palette (status colors, neutral surface hierarchy)
- Flag forbidden territory: cream/sand/beige trap (OKLCH L 0.84–0.97, C < 0.06, hue 40–100)

**Motion budget**:
- Brand: transitions ≤ 400ms, entrance animations permitted
- Product: transitions ≤ 150ms, no decorative motion, `prefers-reduced-motion` required

**Anti-patterns to avoid** (register-specific list of 3–5 specific traps)

### Step 4 — Offer handoff

"Brief saved. Run `/ui-critique` after implementation to validate against it, or `/ui-colorize`/`/ui-typeset` for targeted refinement."

Persist brief to `.claude/cache/ui-shape/<scope-slug>.md` for downstream skills to read.

## Examples

```
/ui-shape login page
→ interview → brief covering brand/product register, type scale, OKLCH color anchors, motion budget

/ui-shape --brief
→ reads active files, infers register from context, generates brief without interview
```

## Token Optimization

**Expected range**: 200–600 tokens (interview), 300–800 tokens (brief generation)

**Early exit**: If `--brief` flag and no UI files in scope, report and stop.

**Patterns used**: git diff scope default, progressive disclosure (brief on request)

**Cache**: Saves brief to `.claude/cache/ui-shape/` for `/ui-critique` and `/ui-polish` to consume.

## Edge Cases

- No UI files and no argument: ask one clarifying question rather than aborting
- Ambiguous register (hybrid page): pick the dominant use case and note the exception in the brief
- Existing design system in repo: grep for design tokens first and incorporate them into the brief rather than proposing conflicting values

## Safety

Read-only except for writing the brief cache file. No file edits.
