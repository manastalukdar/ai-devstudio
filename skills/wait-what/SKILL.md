---
name: wait-what
description: Re-pitch the last message that didn't land — use when the user is confused by what was just said. Re-explains in plain English using ASD-STE100 Simplified Technical English and GLOSSARY.md vocabulary.
disable-model-invocation: true
risk: none
---

# Wait What

That last message didn't land.

Re-pitch it: give a little bit of context, speak in **ASD-STE100 Simplified Technical English** (short sentences, active voice, one idea per sentence, no jargon without definition), and use the ubiquitous language from `GLOSSARY.md`.

If the repo has multiple glossaries, follow `GLOSSARY-MAP.md` to the right one.

## ASD-STE100 basics

- Short sentences. One idea per sentence.
- Active voice: "The agent sends the message" not "The message is sent."
- Common words. Define any technical term the first time you use it.
- No nominalizations: "decide" not "make a decision".
- No abbreviations without expansion on first use.

## Usage

```
/wait-what
```

Use mid-conversation, inside any other skill. Works after the fact — `/grill-with-docs` is the upfront cure (a shared language agreed early stops the jargon arriving at all).

## Token Optimization

**Expected range**: 100–300 tokens (re-pitches the immediately preceding response; optionally reads GLOSSARY.md)

**Patterns used**: Grep-before-Read (checks for GLOSSARY.md existence before reading), early exit (no re-pitch needed if message was already plain)

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
