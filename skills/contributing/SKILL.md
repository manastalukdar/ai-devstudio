---
name: contributing
description: Contribution readiness assessment analyzing project guidelines and requirements
disable-model-invocation: false
---

# Complete Contribution Strategy - Context Aware

I'll analyze everything needed for your successful contribution based on your current context and work.

## Strategic Thinking Process

<think>
For a successful contribution, I need to analyze:

1. **Current Work Context**
   - What has been done in this session?
   - Are we mid-implementation or post-completion?
   - What type of changes were made (feature, fix, refactor)?
   - Is the work ready for contribution?

2. **Project Type & Standards**
   - Is this open source, company, or personal project?
   - What are the contribution guidelines?
   - Are there specific workflows to follow?
   - What quality gates exist (tests, lint, reviews)?

3. **Contribution Strategy**
   - Should this be one PR or multiple?
   - Which issues does this work address?
   - What documentation needs updating?
   - Who should review this?

4. **Pre-flight Checklist**
   - Do all tests pass?
   - Is the code properly formatted?
   - Are there any lint warnings?
   - Is documentation updated?
   - Are commits well-organized?
</think>

## Token Optimization

**Expected range**: 500–1,500 tokens (initial), 100 tokens (cache hit)

**Caching**: Caches project structure in `.claude/cache/understand/project_structure.json` for 7 days.

**Early exit**: Returns immediately if `CONTRIBUTING.md` already exists and is current.

**Patterns used**: Grep-before-Read, early exit, template-based generation, caching
