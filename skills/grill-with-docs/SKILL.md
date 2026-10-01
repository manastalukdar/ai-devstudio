---
name: grill-with-docs
description: Relentless interview to sharpen a plan or design, which also creates docs (ADRs and glossary) as decisions crystallise. Use when working in a repo and wanting to stress-test an idea while building a paper trail.
disable-model-invocation: true
risk: none
---

# Grill With Docs

A stateful version of `/grill-me` that leaves a paper trail. Runs the same relentless interview, but writes what it learns to `GLOSSARY.md` and ADRs as decisions crystallise.

Use this whenever you are **working in a working directory**. If you have no repo, use `/grill-me` instead.

## Behavior

Call the Skill tool twice: once for **`grilling`** and once for **`domain-modeling`**.

The `grilling` skill drives the interview — working through the design tree in rounds, asking the whole frontier at once, waiting for answers.

The `domain-modeling` skill runs as a side effect — capturing resolved terms in `GLOSSARY.md` and offering ADRs for hard-to-reverse decisions the moment they crystallise. Don't batch; write as decisions land.

## Usage

```
/grill-with-docs
/grill-with-docs "add real-time notifications via WebSockets"
```

Arguments are passed as context to the grilling session.

## When to use vs grill-me

| Situation | Use |
|---|---|
| Working in a repo | `/grill-with-docs` |
| No working directory (sharpening a plan, a piece of writing) | `/grill-me` |
| Want the interview primitive with no wrapper | `/grilling` |

## Token Optimization

**Expected range**: 150–600 tokens per round (iterative; each round is proportional to frontier size)

**Patterns used**: Lazy file writes (GLOSSARY.md and ADRs only written when terms resolve), Grep-before-Read on GLOSSARY.md

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
