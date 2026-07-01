---
name: ai-system-review
description: Review LLM application code for context assembly quality, retrieval integration, prompt construction, output validation, cost controls, and failure handling
disable-model-invocation: false
risk: safe
---

# AI System Review

Evaluate LLM-powered application code for reliability, quality, and cost. Covers context assembly, retrieval pipelines (RAG), prompt design, output validation, error handling, and spend controls.

## Usage

```
/ai-system-review                 # review staged changes
/ai-system-review <path>          # review a specific directory or file
/ai-system-review --prompts       # focus only on prompt quality
/ai-system-review --costs         # focus only on token cost controls
```

## Behavior

### Step 1 — Map the LLM system boundary

```bash
# Find model client calls
grep -rn "openai\|anthropic\|bedrock\|vertexai\|litellm\|langchain\|llamaindex" \
  --include="*.ts" --include="*.py" --include="*.js" -l . | head -20

# Find prompt templates
find . -name "*.txt" -o -name "*.md" -o -name "*.jinja" | xargs grep -l "{{.*}}\|\${.*}\|<user>\|<system>" 2>/dev/null | head -10
```

### Step 2 — Review context assembly

Check how context is built before each LLM call:

| Concern | What to look for | Risk |
|---|---|---|
| Context window overflow | No token counting before call | Truncation silently corrupts prompt |
| Injection risk | User input concatenated directly into system prompt | Prompt injection |
| Stale context | No timestamp or recency check on retrieved chunks | Outdated information presented as current |
| Missing metadata | Retrieved chunks lack source / date | Hallucination is unverifiable |
| Token waste | Entire documents passed when only sections needed | Unnecessary cost |

### Step 3 — Review retrieval pipeline (if RAG)

```bash
grep -rn "similarity_search\|retrieve\|vectorstore\|embed\|chromadb\|pinecone\|weaviate\|qdrant" \
  --include="*.ts" --include="*.py" -l . 2>/dev/null
```

Check:
- **Chunking strategy**: Fixed-size vs semantic; chunk size vs model context window
- **Retrieval quality signals**: Is `score` / `distance` checked before including chunks?
- **Top-k threshold**: Hard cap on retrieved chunks regardless of relevance score?
- **Re-ranking**: Any cross-encoder re-ranking before context assembly?
- **Hybrid search**: BM25 + dense retrieval or dense-only?

### Step 4 — Review prompt construction

For each prompt template:

- **System prompt scope**: Is it the minimum necessary? Bloated system prompts cost on every call.
- **Few-shot examples**: Are they hardcoded or dynamically selected? Hardcoded examples may be irrelevant.
- **Output format instructions**: Does the prompt specify JSON/structured output? Is it enforced with tool use / response format?
- **Role separation**: System vs user vs assistant boundaries respected?
- **Instruction conflict**: Contradictory instructions in system + user turns?

### Step 5 — Review output validation

```bash
grep -rn "JSON.parse\|json.loads\|parse\|validate\|schema\|zod\|pydantic" \
  --include="*.ts" --include="*.py" -l . 2>/dev/null | head -10
```

Check:
- Is LLM output parsed and validated before use?
- Is there a fallback when output is malformed?
- Are numeric/boolean outputs range-checked?
- For agentic workflows: are tool call results validated before passing back to model?

### Step 6 — Review cost controls

```bash
grep -rn "max_tokens\|maxTokens\|stream\|usage\|cost\|budget" \
  --include="*.ts" --include="*.py" -l . 2>/dev/null | head -10
```

Check:
- `max_tokens` / `max_completion_tokens` set on every call?
- Streaming used for long outputs (reduces TTFB)?
- Token usage logged per request?
- Monthly spend cap or alert configured?
- Caching for repeated identical prompts (`cache_control`, `prompt_caching`)?

### Step 7 — Review error handling

- What happens when the LLM API returns 429 (rate limit)?
- What happens on 500 or timeout?
- Is there a retry with exponential backoff?
- Does the application surface a graceful degradation to the user?

### Step 8 — Report findings

```
AI SYSTEM REVIEW — <path>

Context Assembly (2 issues)
  src/chat/context.py:34   No token counting — long conversations will silently truncate
  src/search/rag.py:78     User query concatenated directly into system prompt (injection risk)

Retrieval (1 issue)
  src/rag/retriever.py:55  Retrieved chunks used regardless of similarity score — low-relevance
                           context degrades answer quality

Prompt Quality (2 issues)
  prompts/system.txt       System prompt is 1,800 tokens — costs $0.002/call at current volume
  prompts/extract.txt      No structured output format specified — JSON parsing will fail intermittently

Output Validation (1 issue)
  src/api/handler.py:92    LLM JSON parsed with json.loads, no schema validation — malformed
                           output propagates to downstream service

Cost Controls (2 issues)
  src/llm/client.py        No max_tokens set — runaway responses possible
  No prompt caching         Repeated system prompt costs money on every call (enable cache_control)

Error Handling (1 issue)
  src/llm/client.py:18     No retry logic — single API error returns 500 to user
```

## Edge Cases

- **Multiple providers**: Check each client independently; flag inconsistent error handling across providers.
- **Agentic / multi-step**: Trace the full loop — check that tool results are validated before re-entry.
- **Streaming**: Verify error handling works mid-stream (not just at call start).
- **No RAG**: Skip Step 3 and note it was not applicable.

## Token Optimization

**Expected range**: 500–2,000 tokens (grep-driven analysis); 200–400 tokens (single-focus mode with `--prompts` or `--costs`)

**Patterns used**: Grep-before-Read, git diff scope, progressive disclosure, early exit

**Early exit**: If no LLM client imports detected in the target path, report "No LLM integration found" and exit.
