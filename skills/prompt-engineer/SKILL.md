---
name: prompt-engineer
description: Design, optimize, and evaluate prompts for LLM applications — system prompts, few-shot examples, chain-of-thought, structured outputs, and caching strategy
disable-model-invocation: false
risk: safe
---

# Prompt Engineering

Design and optimize prompts for production LLM applications with structured outputs, caching, and evaluation.

Arguments: `$ARGUMENTS` - goal description, existing prompt to refine, or `audit` to review prompts in the current codebase

## Behavior

### 1. Detect Mode

```bash
# Check if auditing existing prompts or designing new ones
if [[ "$ARGUMENTS" == "audit" ]]; then
  grep -rn "system_prompt\|SYSTEM\|<system>\|role.*system\|systemPrompt" . \
    --include="*.py" --include="*.ts" --include="*.js" --include="*.md" \
    -l 2>/dev/null | head -20
fi
```

### 2. For New Prompt Design

Gather context first:
```bash
# Check if project uses Anthropic SDK
grep -r "anthropic\|claude" package.json requirements.txt pyproject.toml 2>/dev/null | head -5
# Check for existing prompt patterns
find . -name "*.md" -path "*/prompts/*" -o -name "*prompt*" -not -path "*/node_modules/*" 2>/dev/null | head -10
```

Apply these patterns based on the goal:

**System prompt structure:**
```xml
<system>
You are [role]. Your task is [specific task].

Rules:
- [constraint 1]
- [constraint 2]

Output format: [JSON schema / markdown / plain text]
</system>
```

**Few-shot examples** (include 2-3 for classification/extraction tasks):
```xml
<examples>
<example>
<input>...</input>
<output>...</output>
</example>
</examples>
```

**Chain-of-thought** (use for reasoning tasks):
```
Think through this step by step before answering.
First, identify... Then, determine... Finally, output...
```

**Structured output** (prefer when consuming programmatically):
```python
# Use with tool_use or response_format for guaranteed JSON
```

### 3. Caching Strategy

Identify cacheable vs. dynamic parts:
- Cache: system prompt, few-shot examples, static context (documents, schemas)
- Dynamic: user message, session history, runtime variables

```python
# Anthropic prompt caching pattern
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": static_context,
                "cache_control": {"type": "ephemeral"}  # cache this block
            },
            {
                "type": "text",
                "text": user_query  # not cached — changes each turn
            }
        ]
    }
]
```

Cache breakeven: ~1,000 tokens. Cache everything above that threshold that doesn't change per-request.

### 4. For Prompt Audits

Review each found prompt for:
- Ambiguity: instructions that could be interpreted multiple ways
- Missing constraints: what the model should NOT do
- Output format: is it specified? is it enforced?
- Caching opportunity: is static context sent uncached every call?
- Token waste: repeated instructions that could be in system prompt

Report format:
```
File: src/prompts/classifier.py
Issues:
  [HIGH] No output format specified — add JSON schema or example
  [MED]  Static 2KB context sent uncached — add cache_control
  [LOW]  Instruction "be helpful" is redundant — remove
```

### 5. Evaluation Checklist

Before finalizing a prompt:
- [ ] Tested with at least 5 diverse inputs
- [ ] Edge cases handled (empty input, adversarial input, off-topic)
- [ ] Output format enforced (not just requested)
- [ ] Caching applied to static blocks > 1,000 tokens
- [ ] System prompt under 500 tokens where possible (use cache for longer)
- [ ] No hallucination-prone instructions ("always answer confidently")

## Examples

```
/prompt-engineer "classify customer support tickets into 5 categories and return JSON"
/prompt-engineer "refine this system prompt: <paste prompt>"
/prompt-engineer audit
```

## Token Optimization

**Expected range**: 400–1,200 tokens (new design), 600–2,000 tokens (audit)

**Early exit**: Audit with no LLM prompt files found → reports "no prompts detected" immediately.

**Grep-before-Read**: Locates prompt files via grep before reading any content.

**Patterns used**: Grep-before-Read, early exit, progressive disclosure (issues by severity)
