---
name: predict-issues
description: Proactive problem identification through code analysis and pattern detection
disable-model-invocation: false
---

# Predictive Code Analysis  

I'll analyze your codebase to predict potential problems before they impact your project.

## Strategic Thinking Process

<think>
To make accurate predictions, I need to consider:

1. **Pattern Recognition**
   - Which code patterns commonly lead to problems?
   - Are there growing complexity hotspots?
   - Do I see anti-patterns that will cause issues at scale?
   - Are there ticking time bombs (hardcoded values, assumptions)?

2. **Risk Assessment Framework**
   - Likelihood: How probable is this issue to occur?
   - Impact: How severe would the consequences be?
   - Timeline: When might this become a problem?
   - Effort: How hard would it be to fix now vs later?

3. **Common Problem Categories**
   - Performance: O(n²) algorithms, memory leaks, inefficient queries
   - Maintainability: High complexity, poor naming, tight coupling
   - Security: Input validation gaps, exposed secrets, weak auth
   - Scalability: Hardcoded limits, single points of failure

4. **Prediction Strategy**
   - Start with highest risk areas (critical path code)
   - Look for patterns that break at 10x, 100x scale
   - Check for technical debt accumulation
   - Identify brittleness in integration points
</think>

## Token Optimization

**Expected range**: 1,200–3,500 tokens (initial), 200 tokens (no high-risk patterns)

**Caching**: Caches issue predictions in `.claude/cache/predict-issues/` for 7 days. Invalidated on new commits.

**Early exit**: Returns immediately if no high-risk patterns are detected in changed files.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
