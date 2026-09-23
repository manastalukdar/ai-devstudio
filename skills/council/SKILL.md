---
name: council
description: Convene four voices (Architect, Skeptic, Pragmatist, Critic) to surface structured disagreement on an ambiguous decision or go/no-go call. Use when multiple credible paths exist and no single review agent should have the final word.
disable-model-invocation: false
risk: none
---

# Council

Four-voice structured disagreement for ambiguous decisions and go/no-go calls.

## Usage

```
/council <decision question>
/council <decision question> --round2   # follow-up round, prior verdict optional context
```

## Behavior

### 1. Extract the real question

State explicitly: what is being decided, what constraints matter, what counts as
success. If the question is vague, ask one clarifying question before proceeding.

### 2. Gather minimal context

Collect only the snippets, metrics, or constraints needed to judge the decision.
Skip repo detail for strategic/general questions unless it changes the answer.

### 3. Form an initial position

Before consulting other voices, write down a starting position, its three
strongest reasons, and its main risk. This prevents the synthesis from simply
mirroring whichever voice speaks last.

### 4. Launch three independent voices

Spawn each as a fresh subagent with only the question and the compact context
from step 2 — never the full conversation history. This is the anti-anchoring
mechanism: a voice that inherits the discussion tends to agree with it.

Apply tiered model delegation: Skeptic and Pragmatist can run on a cheaper
model (Haiku-class); reserve the stronger model for Critic or for synthesis
if the decision is high-stakes.

Prompt shape per voice:

```text
You are the [ROLE] on a four-voice decision council.

Question: [decision question]
Context: [only the relevant snippets or constraints]

Respond with:
1. Position - 1-2 sentences
2. Reasoning - 3 concise bullets
3. Risk - biggest risk in your recommendation
4. Surprise - one thing the other voices may miss

Be direct, no hedging, under 300 words.
```

Role emphasis:

| Voice | Lens |
| --- | --- |
| Architect (in-context) | correctness, maintainability, long-term implications |
| Skeptic | premise challenge, simplest credible alternative |
| Pragmatist | shipping speed, operational reality |
| Critic | edge cases, downside risk, failure modes |

### 5. Synthesize with bias guardrails

- Never dismiss an external view without saying why.
- If a voice changed the recommendation, say so explicitly.
- Always surface the strongest dissent, even when rejecting it.
- Two voices aligning against the initial position is a real signal, not noise.

### 6. Present the verdict

```markdown
## Council: [decision title]

**Architect:** [position] - [why]
**Skeptic:** [position] - [why]
**Pragmatist:** [position] - [why]
**Critic:** [position] - [why]

### Verdict
- Consensus: [where they align]
- Strongest dissent: [most important disagreement]
- Premise check: [did the Skeptic challenge the question itself?]
- Recommendation: [synthesized path]
```

### 7. Record the outcome

If the verdict is worth keeping, offer `/decision-log` to capture it as an ADR.
Do not write ad-hoc notes elsewhere.

## Examples

**Input:** `/council monorepo vs polyrepo for the new services`
**Output:** four short positions plus a verdict block recommending monorepo
with a named dissent from Critic on CI blast-radius, and an offer to log the
decision.

**Input:** `/council ship now or hold for polish`
**Output:** Pragmatist and Skeptic align on shipping a scoped subset; verdict
flags this as the deciding signal over the initial hold-for-polish position.

## Token Optimization

**Expected range**: 800-2,500 tokens initial (three subagent calls plus
synthesis); 150-350 tokens on a `--round2` follow-up that reuses the prior
verdict instead of re-gathering context.

**Caching**: none — each council convenes fresh subagents by design, so
caching a prior verdict would undermine anti-anchoring. `.claude/cache/council/`
is not used.

**Early exit**: if the question has one obvious answer (no real tradeoff),
say so in one line and skip convening the council.

**Patterns used**: tiered model delegation (cheaper model for Skeptic and
Pragmatist), progressive disclosure (verdict first, full transcripts only if
asked), early exit on non-ambiguous questions.

## Edge Cases

- **Question is really a code review or implementation task**: redirect to
  `/review` or standard implementation instead of convening the council.
- **User wants unanimous agreement**: explain that legible disagreement, not
  consensus, is the point; report dissent even if all four converge.
- **Follow-up round requested**: keep the new question narrow and pass only
  the prior verdict, not the full transcript, to preserve Skeptic value.

## Safety

Read-only advisory output. No file writes beyond an explicit, user-approved
`/decision-log` entry. Never feeds subagents the full conversation history.

## Related

`/brainstorm` for open-ended exploration before a decision exists,
`/first-principles` to strip assumptions before framing the question,
`/decision-log` to record the verdict as a durable ADR.
