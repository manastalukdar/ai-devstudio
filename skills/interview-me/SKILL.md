---
name: interview-me
description: Extract requirements one targeted question at a time before any plan or code starts — hypothesizes user intent, scores confidence, and stops at ~95% confidence.
disable-model-invocation: false
risk: none
---

# Interview Me

I'll extract what you actually need before writing a single line of plan or code. I ask one question at a time, hypothesize your intent with a confidence score, and stop only when I reach ~95% confidence.

Arguments: `$ARGUMENTS` — optional initial context or topic to ground the interview

## Token Optimization

**Expected range**: 100–300 tokens per round (hypothesis + one question), 50 tokens (exit)

**Early exit**: If `$ARGUMENTS` contains enough context for 95%+ confidence, state the hypothesis and ask for confirmation rather than continuing to ask questions.

**Patterns used**: Progressive disclosure (one question per turn, no front-loading)

## Step 1 — Form Initial Hypothesis

Before asking anything, reason internally about what the user most likely wants based on `$ARGUMENTS` and conversation context. Produce a one-sentence hypothesis and assign a confidence score (0–100%).

Output format:

```
Hypothesis: [one-sentence statement of what you think the user wants]
Confidence: [N]%
```

## Step 2 — Ask One Targeted Question

Identify the single biggest gap between current confidence and 95%. Ask exactly one question that would most efficiently close that gap. Do not ask compound questions. Do not explain why you are asking it.

## Step 3 — Update Hypothesis

After receiving the answer, update the hypothesis and confidence score. Show the updated hypothesis and confidence. Repeat Steps 2–3 until confidence reaches 95% or the user says "enough" / "proceed".

## Step 4 — Confirm and Hand Off

At 95%+ confidence:

1. State the confirmed hypothesis as a clear, one-paragraph requirement summary
2. List any remaining open questions as assumptions (not blockers)
3. Suggest the next step: `/spec-driven-development`, `/write-plan`, or direct implementation

```
Confirmed: [requirement summary]

Assumptions made:
- [assumption 1]
- [assumption 2]

Ready to proceed. Suggest: /spec-driven-development
```

## Stop Rule

In non-interactive contexts (CI, `/loop`, no terminal): skip the interview, output the hypothesis at current confidence, list all open questions as assumptions, and proceed.

## Edge Cases

- **User provides very detailed initial context**: Jump directly to Step 4 if confidence is already ≥95%
- **User gives contradictory answers**: Surface the contradiction, ask a clarifying question, do not silently ignore it
- **User keeps answering with "I don't know"**: Mark the item as an assumption and move on; do not get stuck
- **User says "just start"**: Treat as a signal to confirm the current hypothesis and proceed immediately
