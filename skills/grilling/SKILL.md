---
name: grilling
description: The interview primitive — relentlessly interview the user about a plan, decision, or idea by working through a design tree in rounds. Use when you want the interview with no wrapper, or when other skills (grill-me, grill-with-docs, wayfinder, improve-codebase-architecture) call for the underlying interview.
disable-model-invocation: false
risk: none
---

# Grilling

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

## Rounds

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask *now* without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format each round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a *later* round, not this one.

## Facts vs decisions

Finding **facts** is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, codebase), dispatch a sub-agent to find it. Don't block on it — a running exploration is an unsettled prerequisite, so only questions downstream of it wait; ask the rest of the frontier now.

The **decisions** are the user's: put each to them and wait.

## Completion

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Usage

```
/grilling              ← uses current conversation context
/grilling "add real-time notifications via WebSockets"
```

This is the primitive. `/grill-me` and `/grill-with-docs` are the two named wrappers. `/triage`, `/wayfinder`, and `/improve-codebase-architecture` all call it internally.

## Token Optimization

**Expected range**: 100–300 tokens per round (proportional to frontier size)

**Patterns used**: Bash for fact-finding sub-agents (avoids asking users for facts available in the environment), early exit (stops when frontier is empty and user confirms shared understanding)

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
