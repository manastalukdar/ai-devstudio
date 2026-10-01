---
name: prototype
description: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
disable-model-invocation: false
risk: safe
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered, using the user's prompt, the surrounding code, or by asking:

- **"Does this logic / state model feel right?"** → Build a single shareable HTML file (free-play buttons plus tabbed guided walkthroughs) that pushes the state machine through cases hard to reason about on paper, driveable by a non-developer.
- **"What should this look like?"** → Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (backend module → logic; page or component → UI) and state the assumption.

## Rules that apply to both branches

1. **Throwaway from day one, clearly marked as such.** Locate prototype code close to where it will actually be used (next to the module or page it's prototyping for) but name it so a casual reader sees it's a prototype. For throwaway UI routes, obey the project's existing routing convention.

2. **Trivial to run.** A UI prototype starts from one command in the project's task runner: `pnpm <name>`, `python <path>`, `bun <path>`. A logic demo is a single HTML file the user double-clicks. No thinking required to start it.

3. **No persistence by default.** State lives in memory. If the question explicitly involves a database, hit a scratch DB or local file with a clear "PROTOTYPE, wipe me" name.

4. **Skip the polish.** No tests, no error handling beyond what makes the prototype *runnable*, no abstractions. The point is to learn something fast.

5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.

6. **Capture it when done.** Fold any validated decision into the real code, then capture the prototype as a **primary source**: commit it to a throwaway branch out of main, and leave a context pointer to that branch on the implementation issue. Capture the answer (the verdict and the question it settled) in the issue or a commit. The main branch keeps only the validated decision.

## Token Optimization

**Expected range**: 300–1,500 tokens (reads relevant files to understand existing conventions, then generates artifact)

**Patterns used**: Grep-before-Read (routing conventions, task runner scripts), early exit to branch selection, minimal file generation

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
