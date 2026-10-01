---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
disable-model-invocation: false
risk: none
---

# Research

Spin up a **background agent** to do the research, so you keep working while it reads.

## Background agent job

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs) — not secondary write-ups. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention. If there is none, put it somewhere sensible and say where.

## Usage

```
/research "how does Postgres LISTEN/NOTIFY work under high connection load?"
/research "what are the rate limits for the GitHub API?"
/research "what changed in React 19 that affects useEffect cleanup?"
```

## Guidelines

- **Primary sources over summaries**: official docs, RFCs, changelog entries, source code comments.
- **Cite everything**: every claim in the output file links to the source that makes it.
- **No hallucination**: if a primary source can't be found for a claim, say so explicitly in the file rather than asserting the claim.
- The output file is a **primary source pointer**, not a conclusion — it feeds into `/grill-with-docs` or `/to-spec`, where decisions are made.

## Output location

Check for existing research/notes conventions in this order:

1. `docs/research/`
2. `.scratch/research/`
3. `research/`
4. Root of repo (last resort; state the path clearly)

Save as `<slug>.md` where slug is derived from the question.

## Token Optimization

**Expected range**: 50–200 tokens (orchestrator only; research work runs in background subagent)

**Patterns used**: Subagent isolation keeps orchestrator context minimal; background agent runs while main session continues

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
