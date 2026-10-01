---
name: to-questionnaire
description: Turn a decision you can't fully answer into a questionnaire for someone else to fill in. Use when the thing blocking you is knowledge held by another person, not something in your head or the codebase.
disable-model-invocation: true
risk: none
---

# To Questionnaire

Turn something the user can't answer alone into a **questionnaire**: a Markdown document they hand to one person to fill in async, or fill out together in a meeting. The recipient holds knowledge the user lacks; the questionnaire pulls it out of them.

**Grill the send, not the subject.** Interview the user only about the *send* — who it goes to and what they need back. The questions in the document then target the **gap** between what the recipient knows and what the user needs.

## Process

### 1. Who is it going to?

Ask, in one exchange: the recipient's role, expertise, and relationship to the user. This fixes the questionnaire's tone and how much context it must carry.

Done when you know who the recipient is and what they know that the user doesn't.

### 2. What do you need back?

Ask, in one exchange: the specific decisions or facts the user can't resolve alone and needs from this person.

Done when you have a concrete list of what the user must walk away able to do or decide.

### 3. Write the questionnaire

Draft questions aimed at the gap from steps 1–2. Write it to `to-questionnaire-<slug>.md` in the current directory (slug from the topic). Report the path.

Done when the file exists and every item from step 2 is covered by a question.

## Document structure

Frame it as a **discovery questionnaire**: the user lacks context, the recipient holds it. Order questions most-important-first (async means you may only get one pass). Group under `##` headings by theme once there are more than a handful.

```markdown
# <Questionnaire title>

**Purpose:** why this questionnaire exists and the decision riding on it.

**From:** <the user>, **To:** <the recipient>, **How your answers will be used:** <where they go>

## Context

One paragraph orienting a recipient who wasn't in the user's head. Enough to answer well, not a page.

## How to answer

Deadline and rough effort. Partial answers and "I don't know" are useful: flag anything you're unsure of rather than skipping it.

## <Theme heading>

One `##` section per theme. Under each, its questions, most-important-first. Every question is one idea, never compound, with an answer stub directly beneath, and a one-line _why this matters_ only where the question could be misread or invite a throwaway answer.

### <Question text>

_Why this matters: <why>_

>

## Anything else?

A closing catch-all: anything we didn't ask that we should know?

>
```

## Usage

```
/to-questionnaire
/to-questionnaire "what infrastructure constraints does the ops team have?"
```

Arguments are used as initial context for the grilling steps.

## Token Optimization

**Expected range**: 200–600 tokens (two-exchange grilling + file write; no codebase reads needed)

**Patterns used**: Progressive disclosure (two-step grilling before writing), early exit (writes immediately once recipient and needs are clear)

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
