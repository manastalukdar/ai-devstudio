# ETHOS.md — AI DevStudio Builder Philosophy

This document captures the core beliefs that shape how AI DevStudio is built and extended. These are not rules — they are convictions about what makes AI-augmented development genuinely valuable. Inspired by [gstack's ETHOS.md](https://github.com/garrytan/gstack).

---

## Boil the Lake

**Completeness is cheap. Partial coverage is not.**

With AI assistance, the marginal cost of handling one more edge case, one more language, one more framework is near zero. Partial tools create partial trust. A skill that works for JavaScript but silently fails for Python is worse than no skill — it trains developers to distrust automation.

When building a skill, ask: *What would make this work for everyone?* Not "what's the MVP?" If the incremental work to handle 95% coverage costs 5 extra minutes, do it.

The practical test: if a new developer runs this skill on their first day and it fails on their project, have we failed them?

---

## Search Before Building

**The best skill is one that already exists.**

Before adding a new skill, search: Is there already a skill that covers this? Could an existing skill be extended by one step? Skills should compose, not duplicate.

The same applies inside skills: before writing a shell script, check if a Bash one-liner already does it. Before building a cache, check if the cache is already written by another skill in the same session.

Redundancy is not robustness — it is maintenance debt.

The practical test: Can a new contributor explain what every skill does without any two descriptions overlapping?

---

## User Sovereignty

**The developer decides. The skill serves.**

AI DevStudio never commits without being asked. Never pushes without being asked. Never deletes without warning. Never makes irreversible choices on behalf of the developer.

Skills surface options and tradeoffs. They recommend. They warn. They preview. But they wait for a human decision before taking actions that cannot be undone.

This is not timidity — it is respect. The developer's code, the developer's production system, the developer's career are at stake. AI assistance that acts faster than the developer can think is not an asset.

The practical test: If the skill were run by a junior developer who did not read the documentation, would anything break without them realizing it?

---

## Signal Over Noise

**Every output must earn its pixels.**

A skill that outputs 200 lines of logs when 5 lines would communicate the same result has failed. Progressive disclosure: give the summary, offer the detail on request.

Token efficiency and output clarity are the same principle: respect the developer's attention.

The practical test: After running the skill, does the developer know exactly what happened and exactly what to do next?

---

## Accumulating Intelligence

**Each session should leave the project smarter than it found it.**

Skills write to agent memory. Sessions write to `.claude/sessions/`. Learnings write to `.claude/learnings.jsonl`. Retros write to `.claude/retros/`. The system should get better at understanding this specific project with every conversation.

A developer returning after two weeks should be able to run `/briefing` and understand the current state without reading hundreds of lines of commit history.

The practical test: After 10 sessions, does the system know things about this project that a new AI instance would have to rediscover?

---

## Safety as Default

**Make the safe path the easy path.**

`/careful` should not be something developers remember to run — destructive commands should surface warnings automatically. Git checkpoints should be the default before any risky operation. `/context-save` should be one invocation, not a procedure.

Every destructive operation in any skill must have a reversal path or a confirmed-intent gate.

The practical test: Can a developer use AI DevStudio all day and be confident that no irreversible action was taken without their explicit sign-off?

---

*These principles were adapted and extended from [gstack's builder philosophy](https://github.com/garrytan/gstack) by Garry Tan.*
