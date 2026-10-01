---
name: ask-matt
description: Router over the skill flows in this repo. Use when you don't know which skill or flow fits your situation, or when asked "what skill should I use for X".
disable-model-invocation: true
risk: none
---

# Ask Matt

You don't remember every skill, so ask.

A **flow** is a path through the skills. Most paths run along one **main flow**, and two **on-ramps** merge onto it. Everything else is standalone, or a vocabulary layer that runs underneath.

## The main flow: idea → ship

The route most work travels. You have an idea and want it built.

1. **`/grill-with-docs`** sharpens the idea by interview. Start here whenever you are **working in a working directory**: it's stateful, retaining what it learns in `GLOSSARY.md` and ADRs. (No working directory? Use `/grill-me` instead. Both run the same `/grilling` primitive; `grill-with-docs` is the one that leaves a paper trail.)
2. **Branch: can you settle every question in conversation?** If a question needs a runnable answer (state, business logic, a UI you have to see), detour through a prototype, bridged by **`/handoff`** in both directions:
   - **`/handoff`** out, open a fresh session,
   - **`/prototype`** to answer the question with throwaway code,
   - **`/handoff`** back what you learned.
3. **Branch: is this a multi-session build?**
   - **Yes** → **`/to-spec`** (synthesize the thread into a spec), then **`/to-tickets`** to split it into tracer-bullet tickets with blocking edges. Then:
     - **`/implement`** per ticket, clearing context between each one; or
     - **`/implement-spec`** for the whole spec in one orchestrated run (parallel implementer subagents across the frontier).
   - **No** → **`/implement`** right here.

   Either way, code is built driving **`/tdd`** and closes with **`/code-review``. When the work goes up as a PR, **`/pr`** shapes the body.

4. **`/retro`** closes the loop — looks back and suggests changes to the agent's environment.

### Context hygiene

Keep steps 1–3 in **one unbroken context window** (don't compact or clear until after `/to-tickets`). Each `/implement` then starts fresh. The limit is the **smart zone** (~150k tokens): if a session approaches it before `/to-tickets`, `/compact` at the nearest phase boundary.

## On-ramps

- **Bugs and requests piling up** → **`/triage`**: moves issues through triage roles and produces agent-ready issues for `/implement`.
- **Something's broken** → **`/diagnosing-bugs`**: for hard bugs — refuses to theorise until it has a tight feedback loop, then fixes with a regression test.
- **A huge, foggy effort** → **`/wayfinder`**: charts a shared map of decision tickets and resolves them one at a time until the way is clear.

## Codebase health

- **`/improve-codebase-architecture`**: surfaces deepening opportunities; picking one generates an idea to take into the main flow at `/grill-with-docs`.

## Vocabulary underneath

Two model-invoked references beneath the other skills:

- **`/domain-modeling`**: sharpen the project's domain language, challenge fuzzy terms, record hard-to-reverse decisions as ADRs.
- **`/codebase-design`**: deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) for designing a module's shape.

## Phase boundaries

At a phase boundary you have five options:

- **Continue**: stay put. Costs nothing, loses nothing.
- **`/clear`**: empty the window when nothing here matters to what's next.
- **`/handoff`**: writes a portable markdown file — use for a new harness, new directory, a colleague, or forking a side task mid-phase.
- **Subagent**: send a tightly-scoped task to its own window.
- **`/compact`**: compress this context and seed a fresh session — the default at the bottom of the tree.

## Standalone

Off the main flow entirely:

- **`/grill-me`**: same interview as `/grill-with-docs`, but stateless — no working directory needed.
- **`/grilling`**: the interview primitive itself — use directly when you want the interview with no wrapper.
- **`/prototype`**: throwaway code that answers one design question.
- **`/research`**: delegate reading legwork to a background agent; produces a cited Markdown file.
- **`/to-questionnaire`**: turns a decision into a Markdown questionnaire for async handoff to a domain expert.
- **`/wizard`**: generates an interactive bash wizard for manual human-only steps.
- **`/wait-what`**: re-pitches the last unclear message in plain English using GLOSSARY.md vocabulary.
- **`/teach`**: learn a concept over multiple sessions using the current directory as a stateful workspace.
- **`/writing-for-agents`**: reference for writing skills, AGENTS.md, CLAUDE.md.

## Token Optimization

**Expected range**: 50–150 tokens (this skill is a guide read — no file I/O required)

**Patterns used**: Early exit (stateless reference; returns immediately after presenting the map)

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
