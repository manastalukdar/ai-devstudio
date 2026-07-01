---
name: assumption-map
description: Map and prioritize the riskiest assumptions behind a feature, product decision, or technical design — surface what would kill it if wrong, then propose the cheapest test for each
disable-model-invocation: false
risk: none
---

# Assumption Map

Surface hidden assumptions behind a plan, feature, or decision. Rank them by risk (probability × impact if wrong), then propose the cheapest experiment that would credibly validate each.

## Usage

```
/assumption-map "<feature or decision to analyze>"   # map assumptions for a specific thing
/assumption-map                                       # map assumptions behind the current task context
/assumption-map --technical                           # focus on technical/architecture assumptions only
/assumption-map --product                             # focus on user/market/business assumptions only
```

## Behavior

### Step 1 — Establish the subject

If `$ARGUMENTS` is provided, use it as the subject. Otherwise, ask:

> What are we mapping assumptions for? (feature, technical decision, architecture choice, or product bet)

### Step 2 — Extract assumptions by category

Generate assumptions across these four layers, using the subject as context:

**Desirability assumptions** (do users want this?)
- Users have the problem we think they have
- Users will change their current behavior to use this
- The UX we plan is how users expect to solve it
- The benefit is compelling enough to overcome switching cost

**Feasibility assumptions** (can we build it?)
- The technology stack can support this without major re-architecture
- The performance characteristics will meet requirements at scale
- The required third-party APIs / data sources are accessible and reliable
- The team has the skills to deliver this in the timeframe

**Viability assumptions** (is it sustainable?)
- The economics work (build + operate cost < value generated)
- We can acquire users at acceptable cost
- No regulatory or compliance blocker

**Technical / architecture assumptions** (for code/design decisions)
- The abstraction will hold as requirements evolve
- The chosen library / framework will remain maintained
- The data model is flexible enough for anticipated variation
- Performance under load will match our estimates

### Step 3 — Rate each assumption

For each assumption, assign:

- **Confidence** (how sure are you this is true?): High / Medium / Low
- **Impact if wrong** (what breaks?): Catastrophic / Major / Minor
- **Risk tier** = Confidence × Impact:

| | High confidence | Medium confidence | Low confidence |
|---|---|---|---|
| **Catastrophic if wrong** | Monitor | Validate soon | Validate now |
| **Major if wrong** | Monitor | Validate soon | Validate soon |
| **Minor if wrong** | Accept | Accept | Monitor |

### Step 4 — Propose validation experiments

For each "Validate now" or "Validate soon" assumption, propose the cheapest credible test:

| Assumption | Cheapest test | Cost | Time | What counts as validated |
|---|---|---|---|---|
| Users have this problem | 5 user interviews asking about current behavior | ~2h | 1 week | 4/5 describe the problem unprompted |
| API supports feature X | Write a proof-of-concept calling the API | ~4h | 1 day | Call succeeds with real data |
| Performance at scale | Load test with realistic data volume | ~1 day | 1 week | p95 latency < 500ms at 10× expected load |
| Abstraction holds | Implement two concrete cases against the interface | ~1 day | 3 days | No leaky abstraction required |

### Step 5 — Output the assumption map

```
ASSUMPTION MAP — <subject>

VALIDATE NOW (highest risk)
  [1] Users will abandon their spreadsheet workflow for this tool
      Confidence: Low | Impact if wrong: Catastrophic
      Test: Interview 5 current spreadsheet users — ask about switching triggers
      Validated when: 3/5 name a specific pain point our tool eliminates

  [2] The vector database can handle 10M embeddings at p95 < 100ms
      Confidence: Low | Impact if wrong: Catastrophic
      Test: Benchmark with synthetic 10M-record dataset (1 day spike)
      Validated when: Benchmark confirms p95 < 100ms

VALIDATE SOON
  [3] SendGrid API supports batch sends > 10k recipients per call
      Confidence: Medium | Impact if wrong: Major
      Test: Read SendGrid docs / call with test batch
      Validated when: Confirmed in API docs or test succeeds

  [4] The chosen data model handles multi-tenancy without schema changes
      Confidence: Medium | Impact if wrong: Major
      Test: Model two tenants with different configs against the schema
      Validated when: Both cases work without adding columns

MONITOR (low risk — check at next milestone)
  [5] The team can deliver this in 6 weeks
      Confidence: High | Impact if wrong: Major

ACCEPT (low risk — not worth testing)
  [6] Markdown rendering will work in the UI
      Confidence: High | Impact if wrong: Minor
```

## Edge Cases

- **Too many assumptions**: Focus the map on assumptions that affect the go/no-go decision in the next sprint or milestone. Defer long-horizon assumptions.
- **Technical decision only**: Use the Technical/Architecture layer only; skip Desirability and Viability.
- **Already in progress**: Flag assumptions that were never validated but have already been acted upon — these are the riskiest.

## Token Optimization

**Expected range**: 300–900 tokens

**Patterns used**: Progressive disclosure (map first, experiments on request), early exit (if subject is clear from context, skip asking)

**No caching needed**: Each assumption map is context-specific and not reusable across sessions.
