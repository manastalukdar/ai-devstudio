---
name: office-hours
description: Run a YC-style office hours session before writing code — six forcing questions that surface wrong premises, missing constraints, and better approaches so you build the right thing the first time.
disable-model-invocation: false
---

# Office Hours

Stop. Before writing a line of code, I'll put your plan through six forcing questions that surface wrong premises, hidden constraints, and better approaches. Inspired by gstack's office-hours skill and Garry Tan's YC office hours format.

The goal is not to block progress — it is to spend 5 minutes now to avoid spending 5 hours on the wrong thing.

## Token Optimization

**Expected range**: 400–1,000 tokens (interview + synthesis), 100 tokens (user has clear answers, no reframing needed)

**Patterns used**: Progressive disclosure (one question at a time), early exit (user explicitly skips with `/office-hours --skip`)

**Early exit**: If invoked with `--skip`, acknowledge and proceed without questions.

## When to Use

Invoke before:
- Starting a new feature or significant refactor
- Writing a plan (`/write-plan`)
- Any task that would take more than 2 hours of engineering work
- When you feel uncertain about scope or approach

## The Six Forcing Questions

Ask each question one at a time. Wait for the user's response before proceeding to the next.

---

**Question 1 — What problem are you actually solving?**

Describe the problem in one sentence without mentioning the solution. If you find yourself describing implementation details, you are not describing the problem yet.

*Purpose: Separates problem definition from solution assumption.*

---

**Question 2 — Who specifically has this problem, and how do you know?**

Name a real user or situation. If the answer is "everyone" or "developers generally," the problem is not specific enough.

*Purpose: Forces concrete user grounding vs. abstract feature building.*

---

**Question 3 — What is the simplest thing that could possibly work?**

Not the best solution — the simplest. What is the minimum version that would validate whether the problem is real?

*Purpose: Surfaces whether the planned approach is over-engineered.*

---

**Question 4 — What assumptions are you making that could be wrong?**

List at least two. These are beliefs about the user, the system, or the environment that you have not verified.

*Purpose: Makes hidden risk explicit before it becomes a bug.*

---

**Question 5 — What would make this a bad idea?**

Under what conditions is this the wrong approach entirely? What would you need to see to abandon the plan?

*Purpose: Forces adversarial thinking while the cost of changing direction is low.*

---

**Question 6 — What will you cut if this takes 3× longer than expected?**

Scope always expands. Define what is non-negotiable vs. what is nice-to-have before you start.

*Purpose: Prevents scope creep from killing the project.*

---

## Synthesis

After all six answers, produce a one-page summary:

```
Office Hours Summary

Problem: <one sentence>
User: <specific>
Minimum viable approach: <what to build first>
Top risks: <the two biggest assumptions>
Kill conditions: <what would make this wrong>
Non-negotiable scope: <what ships no matter what>
Nice-to-have (cut first): <what gets dropped under pressure>

Recommendation: <proceed / reframe / stop>
```

**Recommendations:**
- **Proceed** — answers are clear, approach is well-grounded
- **Reframe** — answers reveal the plan needs adjustment before starting; suggest a revised framing
- **Stop** — the problem is not real, the solution is wrong, or the assumptions are too fragile; explain why

## Edge Cases

- **User skips a question**: Record as `[skipped]` and move on; do not block
- **User already has a plan**: Run questions anyway — the plan may change, and that is the point
- **Small tasks (under 30 minutes)**: Still worth asking Questions 1 and 3; skip the rest
- **Repeated invocation on the same task**: Show the prior summary and ask which answers have changed
