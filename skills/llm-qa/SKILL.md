---
name: llm-qa
description: Investigate LLM output quality issues — trace hallucination root causes across context, retrieval, prompts, tool use, and workflow design
disable-model-invocation: false
risk: safe
---

# LLM QA — Output Quality Investigation

Root-cause analysis for LLM output failures: hallucinations, refusals, format errors, incomplete answers, and regression in answer quality.

## Usage

```
/llm-qa "<description of the quality issue>"   # investigate a specific failure
/llm-qa --regression                           # compare output quality before/after a change
/llm-qa --prompts <path>                       # audit prompt files for known quality anti-patterns
```

## Behavior

### Step 1 — Classify the failure type

Identify which category the quality issue falls into:

| Failure type | Symptoms | Primary suspects |
|---|---|---|
| **Hallucination** | Confident wrong facts, invented citations | Context gap, stale retrieval, no grounding |
| **Refusal** | Unexpected "I can't help with that" | System prompt over-restriction, safety over-triggering |
| **Format error** | Malformed JSON, missing fields, wrong structure | No output schema, inconsistent instructions |
| **Incomplete answer** | Truncated, missing steps, dropped context | max_tokens too low, context window overflow |
| **Quality regression** | Correct before, wrong after recent change | Prompt changed, model changed, retrieval changed |
| **Inconsistency** | Different answers to the same question | Temperature too high, no seed, non-deterministic retrieval |

### Step 2 — Reconstruct the failing call

Ask for (or locate in code):
1. The exact system prompt used
2. The user input that triggered the failure
3. The retrieved context (if RAG)
4. The model and parameters (temperature, max_tokens, top_p)
5. The actual vs expected output

```bash
# Find where the failing call is constructed
grep -rn "system_prompt\|systemPrompt\|messages\s*=" --include="*.py" --include="*.ts" -n . | head -20
```

### Step 3 — Audit context quality

Check whether the model had the information it needed:

- **Context gap**: Was the correct information present in the retrieved chunks or conversation history?
- **Context relevance**: Were irrelevant chunks crowding out relevant ones? Check similarity scores.
- **Context recency**: Is the retrieved information current? Check timestamps or version markers.
- **Context length**: Was the context near the model's limit? Truncation causes hallucination at boundaries.

```bash
# Estimate tokens in context (rough: 1 token ≈ 4 chars)
wc -c context.txt | awk '{print int($1/4), "approx tokens"}'
```

### Step 4 — Audit the prompt

Check the system prompt and user message for known quality failure patterns:

| Anti-pattern | Example | Fix |
|---|---|---|
| Contradictory instructions | "Be concise" + "explain in detail" | Remove one; make priority explicit |
| Ambiguous output format | "Return JSON" without schema | Provide exact JSON schema or use structured output |
| Missing grounding instruction | No "only use provided context" | Add explicit grounding constraint |
| Persona over-restriction | "Never discuss X" too broad | Narrow to specific harmful case |
| Missing failure instruction | No "if unsure, say so" | Add explicit uncertainty handling |
| Long system prompt noise | 2,000+ token system prompt with irrelevant rules | Trim to minimum necessary |

### Step 5 — Audit model parameters

| Parameter | Risk if wrong | Check |
|---|---|---|
| `temperature` | > 0.7 increases inconsistency | Set 0–0.3 for factual tasks |
| `max_tokens` | Too low truncates response | Check against expected output length |
| `top_p` | Combined with high temp amplifies randomness | Use one of temp or top_p, not both |
| `seed` | Absent means non-deterministic | Set for reproducibility in tests |

### Step 6 — Identify root cause and fix

Map the failure to its root cause layer:

```
Root cause layers (in order of likelihood):
  1. Context gap / retrieval miss → fix retrieval query or chunk strategy
  2. Prompt instruction conflict → remove or clarify conflicting rule
  3. Missing output schema → add structured output / response format
  4. Context overflow → reduce chunk count or trim system prompt
  5. Model parameter → adjust temperature or max_tokens
  6. Model capability limit → switch to a more capable model for this task
```

### Step 7 — Propose regression test

For each root cause fixed, generate a test case to prevent recurrence:

```python
# Regression test template
def test_llm_no_hallucination_on_unknown_topic():
    response = llm_call(
        system="Only answer based on the provided context. If unsure, say 'I don't know'.",
        user="What is the capital of Zorbania?",
        context=""  # empty context — model must refuse, not hallucinate
    )
    assert "don't know" in response.lower() or "not sure" in response.lower()
```

## Edge Cases

- **No access to logs or prompt**: Guide the user to capture the failing call; provide a logging snippet to add.
- **Regression after model upgrade**: Check for model-specific behavior changes; test with previous model version if possible.
- **Non-English output failure**: Check tokenization differences for the target language; consider language-specific prompts.
- **Tool call failures in agentic loop**: Trace the tool result that re-entered the context and check if it introduced confusion.

## Token Optimization

**Expected range**: 400–1,500 tokens (full investigation); 200–500 tokens (`--prompts` audit mode)

**Patterns used**: Grep-before-Read (locate prompt files before reading), progressive disclosure (classification → audit → root cause → fix), early exit

**Early exit**: If the failure type is immediately obvious from the description (e.g., "max_tokens too low causing truncation"), skip to Step 6 and propose the fix directly.
