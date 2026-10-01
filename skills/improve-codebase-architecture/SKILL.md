---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. Use when you want to surface architectural friction and refactor shallow modules into deep ones.
disable-model-invocation: true
risk: none
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This skill is _informed_ by the project's domain model and built on a shared design vocabulary:

- Call the Skill tool with `codebase-design` for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles. Use these terms exactly; don't drift into "component," "service," "API," or "boundary."
- The domain language in `GLOSSARY.md` gives names to good seams; ADRs in `docs/adr/` record decisions this skill should not re-litigate.

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening pays off by making future changes easier, so weight heavily the parts of the codebase that have recently changed.

- If the user named a direction (a module, a subsystem, a pain point), take it.
- Otherwise, walk back recent commit history (`git log --oneline`) to find hot spots — files that keep coming up — and let those pull attention first.

Read `GLOSSARY.md` and any ADRs in the area you're touching first.

Then spawn a sub-agent to walk the codebase organically, noting friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts are untested, or hard to test through their current interface?

Apply the **deletion test** to anything suspect: would deleting it concentrate complexity, or just move it?

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory (`$TMPDIR` → `/tmp` on Linux/macOS → `%TEMP%` on Windows). Name it `architecture-review-<timestamp>.html`. Open it for the user and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and **Mermaid via CDN** for diagrams where graph-shaped relationships benefit from it. Each candidate gets a before/after visualisation.

For each candidate, render a card with:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture causes friction
- **Solution**: plain English description of what would change
- **Benefits**: explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram**: side-by-side, illustrating shallowness and the deepening
- **Recommendation strength**: `Strong`, `Worth exploring`, or `Speculative` as a badge

End the report with a **Top recommendation** section.

Use `GLOSSARY.md` vocabulary for domain terms and `/codebase-design` vocabulary for architecture. If an ADR contradicts a candidate, only surface it when the friction is real enough to warrant reopening the ADR — mark it with a warning callout.

**Do NOT propose interfaces yet.** After the file is written, ask: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, call the Skill tool with `grilling` to walk the decision tree: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallise — call the Skill tool with `domain-modeling` to keep the domain model current:

- **Naming a deepened module after a concept not in `GLOSSARY.md`?** Add the term.
- **Sharpening a fuzzy term?** Update `GLOSSARY.md` right there.
- **User rejects with a load-bearing reason?** Offer an ADR so future reviews don't re-suggest it.

## Token Optimization

**Expected range**: 500–3,000 tokens (exploration subagent + report generation)

**Patterns used**: Git diff scope (hot-spot detection from `git log`), Grep-before-Read for GLOSSARY.md, subagent isolation for codebase walk, early exit if user named a direction

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
