---
name: pr
description: Write a PR body using a structured template with visual summary, evidence, and merge danger assessment. Use when writing or reviewing a pull request description.
disable-model-invocation: false
risk: none
---

# PR

Use this template for writing the PR body:

```markdown
## Summary

<diagram, diff-sketch, or tree>

## Evidence

- **Before:** <screenshot/output/failing test run>
  **After:** <screenshot/output/passing test run>

## Merge Danger

**Door:** <one-way or two-way>

<optional: description>

**Blast Radius:** <one-word description>

<optional: potential ramifications of merge>
```

## Sections

Skip all preambles and keep prose brief. Use the project's domain language from `GLOSSARY.md`.

### Summary

Pick the smallest view that makes the key point clear.

- **Logic or algorithm** → pseudocode:

```text
on(save)
  if content is unchanged
    return cached result
  write new content
  return fresh result
```

- **Runtime control flow** → call tree:

```text
submitForm
  createSession
    persistPrompt
    launchAgent
  navigateToSession
```

- **UI structure** → component tree with state and module boundaries:

```text
<SessionPage> (apps/example/src/routes/session.tsx)
  useSessionEvents()
  <SessionToolbar>
    <RunSkillButton> (packages/ui)
```

- **File responsibility or broad refactor** → shallow file tree:

```text
src/
├── commands/       # parses user actions
├── sessions/       # owns session state
└── transport/      # sends API requests
```

- **Component interaction or data flow** → Mermaid sequence diagram
- **What changes** → diff (match the diff shape to the topic: component, file-layout, call-tree, or state/control-flow)
- **Mostly new code** → whole block

Place each visual next to the short text it supports. Keep only the calls, files, props, states, and boundaries needed to answer the current question. Use your judgement — you may use one or several visuals, unlikely you'll need all of them.

### Evidence

Concrete evidence that the change works. Show a before and after.

- **Screenshots** are S-tier — when the environment supports it and the change is visual.
- **Execution-based evidence** is A-tier — test results, console output. Show the exact test that now fails then passes.

### Merge Danger

**Door**: one-way (hard to roll back) or two-way (cheap to roll back). Changes with destructive actions or hard-to-reverse decisions are one-way doors.

**Blast Radius**: the potential impact or scope of the changes. Consider layout shifts, breakages for consumers, mobile responsiveness, etc.

## Token Optimization

**Expected range**: 100–400 tokens (template fill; optionally reads GLOSSARY.md)

**Patterns used**: Early exit (template is fixed), Grep-before-Read for GLOSSARY.md only when domain terms are referenced

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution. Original show-me template credited to Dex Horthy / Humanlayer.*
