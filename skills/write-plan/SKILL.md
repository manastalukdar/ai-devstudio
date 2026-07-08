---
name: write-plan
description: Create detailed implementation plans with task breakdown
disable-model-invocation: true
---

# Implementation Plan Writer

I'll create comprehensive implementation plans with task breakdowns, timelines, and success criteria.

Arguments: `$ARGUMENTS` - feature description, requirements, or planning focus

## Planning Philosophy

Based on **obra/superpowers** planning methodology:
- Break work into concrete, testable tasks
- Clear acceptance criteria for each task
- Identify dependencies and blockers
- Estimate complexity honestly
- Plan for validation and testing

## Token Optimization

**Expected range**: 1,200–3,000 tokens (initial), 300 tokens (cache hit)

**Caching**: Caches project patterns in `.claude/cache/plans/project-patterns.json` for 7 days.

**Early exit**: Returns immediately if an identical plan already exists for the requested feature.

**Patterns used**: Grep-before-Read, early exit, caching, template-based generation
