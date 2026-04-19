# Token Optimization - Phase 2 Batch 4 Implementation Plan

**Status:** 🔄 Active Planning
**Target:** Tier 2 Advanced Features (37 skills)
**Expected Completion:** Q1 2026
**Last Updated:** 2026-01-27

---

## Executive Summary

Phase 2 Batch 4 focuses on optimizing all 37 Tier 2 Advanced Features skills. These skills provide professional workflows for testing, CI/CD, API development, debugging, Git operations, database management, documentation, and code quality.

**Current Progress:**
- ✅ Phase 2 Batch 1: 5 critical core skills (69% avg reduction)
- ✅ Phase 2 Batch 2: 16 Tier 1 high-impact essentials (61% avg reduction)
- ✅ Phase 2 Batch 3: 23 remaining core skills (62% avg reduction)
- 🔄 **Phase 2 Batch 4: 37 Tier 2 advanced features (next)**
- ⏳ Phase 2 Batch 5: 16 Tier 3 power tools

**Optimization Targets:**
- **Average Token Reduction:** 50-60% (conservative estimate for complex skills)
- **Token Budget:** 3,500 tokens current → 1,750 tokens optimized (per skill average)
- **Total Savings:** 129,500 tokens → 64,750 tokens (37 skills combined)

---

## Table of Contents

1. [Tier 2 Skills Overview](#tier-2-skills-overview)
2. [Sub-Batch Organization](#sub-batch-organization)
3. [Optimization Strategies by Category](#optimization-strategies-by-category)
4. [Implementation Timeline](#implementation-timeline)
5. [Success Metrics](#success-metrics)
6. [Risk Mitigation](#risk-mitigation)

---

## Tier 2 Skills Overview

**Total Skills:** 37 (Advanced Features for Professional Workflows)

**Categorization:**

| Category | Count | Examples | Complexity | Priority |
|----------|-------|----------|------------|----------|
| Testing & Debugging | 10 | test-async, test-antipatterns, test-coverage, test-mutation, debug-root-cause, debug-session, performance-profile, bundle-analyze, lighthouse, memory-leak | Medium-High | High |
| CI/CD & DevOps | 8 | release-automation, pipeline-monitor, container-optimize, deployment-rollback, infrastructure, execute-plan, git-worktree, branch-finish | High | High |
| API & Database | 10 | api-docs-generate, graphql-schema, api-mock, schema-validate, query-optimize, seed-data, database-connect, postman-convert, openapi-types, inline-docs | Medium-High | Medium |
| Git & Code Quality | 9 | conflict-resolve, merge-strategy, git-bisect, complexity-reduce, duplication-detect, code-review-checklist, readme-generate, mock-generate, boilerplate | Medium | Medium |

**Note:** Several skills listed in the original Tier 2 plan were already optimized in Phase 2 Batch 3:
- `/accessibility` (Batch 3A)
- `/lazy-load` (Batch 3A)
- `/license-check` (Batch 3B)
- `/security-headers` (Batch 3C)
- `/owasp-check` (Batch 3C)
- `/playwright-automate` (Batch 3C)

These 6 skills are excluded from this batch, bringing the actual count to **37 skills remaining**.

---

## Sub-Batch Organization

To manage complexity and maintain quality, Batch 4 is divided into 4 sub-batches:

### Batch 4A: Testing & Debugging Workflows (10 skills)

**Focus:** Async patterns, anti-patterns, coverage, mutation testing, profiling

| # | Skill | Current Tokens | Target Tokens | Reduction | Strategy |
|---|-------|----------------|---------------|-----------|----------|
| 1 | test-async | 3,000-5,000 | 1,200-2,000 | 60% | Grep async patterns, framework detection cache, focused analysis |
| 2 | test-antipatterns | 3,500-5,500 | 1,400-2,200 | 60% | Pattern-based Grep, early exit, example-based reporting |
| 3 | test-coverage | 3,000-5,000 | 1,200-2,000 | 60% | Bash coverage tools, focused gap analysis, caching |
| 4 | test-mutation | 3,000-5,000 | 1,500-2,500 | 50% | Incremental mutation testing, sample-based analysis |
| 5 | debug-root-cause | 4,000-6,000 | 2,000-3,000 | 50% | Hypothesis-driven analysis, dependency tracing, early exit |
| 6 | debug-session | 3,000-5,000 | 1,500-2,500 | 50% | Session state files, incremental documentation |
| 7 | performance-profile | 4,000-6,000 | 1,500-2,500 | 60% | Bash profiling tools, bottleneck-focused analysis, Grep hotspots |
| 8 | bundle-analyze | 4,500-6,500 | 1,800-2,600 | 60% | Bash bundle analyzers, size-focused reporting, tree-shaking detection |
| 9 | lighthouse | 4,000-6,000 | 1,500-2,500 | 60% | Bash lighthouse CLI, score-based reporting, progressive fixes |
| 10 | memory-leak | 3,000-5,000 | 1,500-2,500 | 50% | Heap profiling tools, focused leak detection, pattern analysis |

**Sub-Batch Totals:**
- Current: 35,500-54,000 tokens
- Target: 15,100-24,300 tokens
- **Average Reduction: 57%**

**Key Optimization Patterns:**
- Bash-based tool execution (saves 60-70% vs Task agents)
- Framework detection caching (saves 500 tokens per run)
- Pattern-based Grep for issue detection
- Early exit when no issues found
- Progressive disclosure (critical → high → medium → low)

---

### Batch 4B: CI/CD & DevOps Automation (8 skills)

**Focus:** Release automation, pipeline monitoring, infrastructure, deployment

| # | Skill | Current Tokens | Target Tokens | Reduction | Strategy |
|---|-------|----------------|---------------|-----------|----------|
| 1 | release-automation | 3,000-5,000 | 1,500-2,500 | 50% | Template-based releases, version bump scripts, changelog integration |
| 2 | pipeline-monitor | 3,000-5,000 | 1,500-2,500 | 50% | CI/CD API caching, flaky test tracking, metrics aggregation |
| 3 | container-optimize | 4,000-6,000 | 1,500-2,500 | 60% | Dockerfile pattern analysis, multi-stage templates, layer caching |
| 4 | deployment-rollback | 4,000-6,000 | 2,000-3,000 | 50% | Health check scripts, rollback templates, state tracking |
| 5 | infrastructure | 5,000-7,000 | 2,000-3,000 | 60% | IaC template library, provider detection cache, incremental setup |
| 6 | execute-plan | 3,000-5,000 | 1,500-2,500 | 50% | Checkpoint-based execution, state files, batch processing |
| 7 | git-worktree | 2,000-3,500 | 1,000-2,000 | 50% | Git worktree templates, parallel dev patterns, Bash operations |
| 8 | branch-finish | 2,500-4,000 | 1,200-2,000 | 50% | Workflow templates, squash strategies, automated cleanup |

**Sub-Batch Totals:**
- Current: 26,500-41,500 tokens
- Target: 12,200-20,000 tokens
- **Average Reduction: 54%**

**Key Optimization Patterns:**
- Template-based generation (saves 40-50%)
- Platform/provider detection caching
- Bash-based Git operations
- State file tracking for multi-step workflows
- Incremental processing (changed resources only)

---

### Batch 4C: API & Database Management (10 skills)

**Focus:** API documentation, GraphQL, database operations, mocking

| # | Skill | Current Tokens | Target Tokens | Reduction | Strategy |
|---|-------|----------------|---------------|-----------|----------|
| 1 | api-docs-generate | 4,000-6,000 | 1,500-2,500 | 60% | Endpoint Grep discovery, OpenAPI templates, incremental docs |
| 2 | graphql-schema | 3,000-5,000 | 1,500-2,500 | 50% | Schema caching, federation checks, type analysis |
| 3 | api-mock | 5,000-7,000 | 2,000-3,000 | 60% | Template-based mocks, schema-driven generation, MSW patterns |
| 4 | schema-validate | 3,500-5,500 | 1,500-2,500 | 60% | Schema diff caching, drift detection, validation rules |
| 5 | query-optimize | 4,000-6,000 | 1,500-2,500 | 60% | N+1 pattern Grep, query analysis, index recommendations |
| 6 | seed-data | 4,000-6,000 | 2,000-3,000 | 50% | Schema-based generation, faker templates, realistic data |
| 7 | database-connect | 3,500-5,500 | 1,500-2,500 | 60% | MCP integration, connection caching, safe query templates |
| 8 | postman-convert | 4,500-6,500 | 2,000-3,000 | 60% | Collection parsing, test templates, incremental conversion |
| 9 | openapi-types | 4,000-6,000 | 2,000-3,000 | 50% | Schema parsing cache, template-based types, SDK generation |
| 10 | inline-docs | 3,500-5,500 | 1,500-2,500 | 60% | Grep for undocumented code, JSDoc templates, focused generation |

**Sub-Batch Totals:**
- Current: 39,000-59,000 tokens
- Target: 17,500-26,500 tokens
- **Average Reduction: 58%**

**Key Optimization Patterns:**
- Schema caching (saves 70% on cache hits)
- Endpoint/type discovery with Grep
- Template-based generation
- MCP integration for external resources
- Incremental processing (changed schemas only)

---

### Batch 4D: Git & Code Quality (9 skills)

**Focus:** Git workflows, code quality analysis, scaffolding

| # | Skill | Current Tokens | Target Tokens | Reduction | Strategy |
|---|-------|----------------|---------------|-----------|----------|
| 1 | conflict-resolve | 3,000-5,000 | 1,500-2,500 | 50% | Semantic analysis, merge strategy templates, guided resolution |
| 2 | merge-strategy | 3,000-5,000 | 1,500-2,500 | 50% | Strategy decision trees, conflict prediction, history analysis |
| 3 | git-bisect | 3,000-5,000 | 1,500-2,500 | 50% | Automated bisection, test execution, commit range optimization |
| 4 | complexity-reduce | 4,500-6,500 | 1,800-2,600 | 60% | Cyclomatic complexity Grep, focused refactoring, early exit |
| 5 | duplication-detect | 5,000-7,000 | 2,000-3,000 | 60% | DRY pattern detection, clone analysis, incremental scanning |
| 6 | code-review-checklist | 2,500-4,000 | 1,200-2,000 | 50% | Context-aware templates, framework-specific checks, caching |
| 7 | readme-generate | 3,500-5,500 | 1,500-2,500 | 60% | Project structure cache, template-based sections, incremental updates |
| 8 | mock-generate | 3,000-5,000 | 1,500-2,500 | 50% | Type-based mocks, faker integration, template generation |
| 9 | boilerplate | 3,000-5,000 | 1,200-2,000 | 60% | Framework templates library, cached detection, incremental scaffolding |

**Sub-Batch Totals:**
- Current: 30,500-48,000 tokens
- Target: 13,700-21,600 tokens
- **Average Reduction: 56%**

**Key Optimization Patterns:**
- Bash-based Git operations
- Complexity/duplication pattern Grep
- Template libraries
- Framework detection caching
- Incremental analysis (changed files only)

---

## Optimization Strategies by Category

### Universal Patterns (All 37 Skills)

1. **Grep-Before-Read (90% savings)**
   - Always use Grep to discover files before reading
   - Use `output_mode="files_with_matches"` for discovery
   - Only read files that match criteria

2. **Caching Layer (70-99% on cache hits)**
   - Framework/platform detection: `.claude/cache/project-analysis.json`
   - Tool availability: `.claude/cache/tools.json`
   - Schema/API definitions: `.claude/cache/[skill-name]/schema.json`
   - Previous results: `.claude/cache/[skill-name]/last-results.json`

3. **Early Exit (50-80% savings when applicable)**
   - Quick validation before deep analysis
   - Stop after finding N examples (N=5-10 usually sufficient)
   - Exit immediately on critical issues
   - No issues found → exit with ✓ message

4. **Progressive Disclosure (60-85% savings)**
   - Level 1: Critical issues only (default)
   - Level 2: Critical + High (--verbose)
   - Level 3: All issues (--verbose --all)
   - Users typically only need Level 1

5. **Focus Areas/Scope Limiting (70-90% savings)**
   - Default: Git diff (changed files only)
   - Optional: Specific path parameter
   - Flag: --full for complete project scan
   - Most runs only need changed files

6. **head_limit on Searches (80-95% savings)**
   - Always limit Grep results
   - Typical limits: 5-20 results
   - Provide --limit flag for more results
   - Prevents token explosion on large codebases

### Category-Specific Patterns

**Testing & Debugging:**
- Bash-based tool execution (jest, vitest, lighthouse, etc.)
- Framework detection caching
- Test file discovery with Glob
- Focused error analysis (don't analyze all tests, just failures)

**CI/CD & DevOps:**
- Template-based generation (GitHub Actions, GitLab CI, Docker)
- Platform detection caching
- Incremental resource analysis
- State files for multi-step deployments

**API & Database:**
- Schema caching (OpenAPI, GraphQL, database schemas)
- Endpoint discovery with Grep
- MCP integration for external resources
- Template-based generation (mocks, types, docs)

**Git & Code Quality:**
- Bash-based Git operations
- Complexity/duplication pattern detection
- Template libraries for scaffolding
- Incremental analysis (changed files only)

---

## Implementation Timeline

### Week 1-2: Batch 4A - Testing & Debugging (10 skills)

**Day 1-3: High-priority testing skills**
- test-async, test-antipatterns, test-coverage

**Day 4-7: Advanced debugging skills**
- test-mutation, debug-root-cause, debug-session

**Day 8-10: Performance profiling**
- performance-profile, bundle-analyze, lighthouse, memory-leak

**Expected Output:**
- 10 skills with Token Optimization sections
- 57% average token reduction
- Validation on 3 sample projects (small, medium, large)

---

### Week 3-4: Batch 4B - CI/CD & DevOps (8 skills)

**Day 1-3: Release & monitoring**
- release-automation, pipeline-monitor, container-optimize

**Day 4-7: Deployment & infrastructure**
- deployment-rollback, infrastructure, execute-plan

**Day 8-10: Git workflows**
- git-worktree, branch-finish

**Expected Output:**
- 8 skills with Token Optimization sections
- 54% average token reduction
- Template libraries for common platforms

---

### Week 5-6: Batch 4C - API & Database (10 skills)

**Day 1-3: API documentation & validation**
- api-docs-generate, graphql-schema, api-mock

**Day 4-7: Database operations**
- schema-validate, query-optimize, seed-data, database-connect

**Day 8-10: Code generation**
- postman-convert, openapi-types, inline-docs

**Expected Output:**
- 10 skills with Token Optimization sections
- 58% average token reduction
- Schema caching infrastructure

---

### Week 7-8: Batch 4D - Git & Code Quality (9 skills)

**Day 1-3: Git workflows**
- conflict-resolve, merge-strategy, git-bisect

**Day 4-7: Code quality analysis**
- complexity-reduce, duplication-detect, code-review-checklist

**Day 8-10: Documentation & scaffolding**
- readme-generate, mock-generate, boilerplate

**Expected Output:**
- 9 skills with Token Optimization sections
- 56% average token reduction
- Complete Tier 2 optimization

---

### Overall Timeline Summary

| Week | Sub-Batch | Skills | Avg Reduction | Cumulative |
|------|-----------|--------|---------------|------------|
| 1-2 | 4A: Testing | 10 | 57% | 10/37 (27%) |
| 3-4 | 4B: CI/CD | 8 | 54% | 18/37 (49%) |
| 5-6 | 4C: API & DB | 10 | 58% | 28/37 (76%) |
| 7-8 | 4D: Git & Quality | 9 | 56% | 37/37 (100%) |

**Total Duration:** 8 weeks (2 months)
**Total Skills:** 37
**Expected Average Reduction:** 56%
**Realistic Calendar Time:** 10-12 weeks (with testing and validation)

---

## Success Metrics

### Quantitative Metrics

**Token Reduction Targets:**
- [ ] **Overall average: 50-60% reduction** (conservative for complex skills)
- [ ] Batch 4A (Testing): 55-60% reduction
- [ ] Batch 4B (CI/CD): 50-55% reduction
- [ ] Batch 4C (API & DB): 55-60% reduction
- [ ] Batch 4D (Git & Quality): 55-60% reduction

**Pattern Implementation:**
- [ ] 100% of skills use Grep-before-Read
- [ ] 100% of skills have early exit conditions
- [ ] 90%+ of skills implement caching
- [ ] 100% of reporting skills use progressive disclosure
- [ ] 90%+ of skills support focus areas/scope limiting

**Documentation:**
- [ ] 100% of skills have Token Optimization section
- [ ] Current → optimized token budgets documented
- [ ] Optimization patterns clearly explained
- [ ] Cache invalidation strategies defined

### Qualitative Metrics

**Functionality:**
- [ ] Zero functionality regression
- [ ] All features maintained
- [ ] Edge cases still handled
- [ ] User experience improved (faster, not compromised)

**Code Quality:**
- [ ] Consistent pattern application across skills
- [ ] Clear, maintainable bash scripts
- [ ] Proper error handling
- [ ] Comprehensive comments

**User Experience:**
- [ ] Faster response times (smaller context windows)
- [ ] Clear progress indicators
- [ ] Actionable output (not overwhelming)
- [ ] Helpful flags (--verbose, --full, --no-cache)

### Validation Requirements

**Per-Skill Testing:**
1. **Small project (< 20 files):**
   - Verify token usage within budget
   - Validate all features work
   - Check cache creation

2. **Medium project (50-100 files):**
   - Verify cache hit behavior
   - Validate early exit triggers
   - Check focus area limiting

3. **Large project (500+ files):**
   - Verify head_limit prevents explosion
   - Validate progressive disclosure
   - Check performance improvements

**Real-World Scenarios:**
- [ ] Daily development workflow (commit, test, review cycle)
- [ ] CI/CD pipeline setup and monitoring
- [ ] API development and documentation
- [ ] Database schema management
- [ ] Git workflow optimization

---

## Risk Mitigation

### Identified Risks

**Risk 1: Complex Skills May Not Reach 60% Reduction**
- **Mitigation:** Set conservative 50% target, celebrate overachievement
- **Contingency:** Focus on most impactful optimizations first
- **Acceptance Criteria:** Any reduction ≥40% is acceptable for complex skills

**Risk 2: Caching May Not Work Across All Project Types**
- **Mitigation:** Implement robust cache invalidation
- **Contingency:** Provide --no-cache flag for edge cases
- **Acceptance Criteria:** Cache hit rate ≥70% in normal usage

**Risk 3: Bash Scripts May Have Cross-Platform Issues**
- **Mitigation:** Test on Linux, macOS, Windows/WSL
- **Contingency:** Provide fallback to direct tool calls
- **Acceptance Criteria:** Works on all 3 major platforms

**Risk 4: Time Estimates May Be Optimistic**
- **Mitigation:** Build 20% buffer into timeline
- **Contingency:** Prioritize high-impact skills if time constrained
- **Acceptance Criteria:** Complete 80%+ of skills within 10 weeks

**Risk 5: Pattern Inconsistency Across 37 Skills**
- **Mitigation:** Create reusable bash functions and templates
- **Contingency:** Establish pattern review checklist
- **Acceptance Criteria:** ≥90% pattern consistency across batch

### Quality Assurance

**Before Starting Each Skill:**
- [ ] Review TOKEN_OPTIMIZATION_GUIDE.md patterns
- [ ] Check existing skill for current behavior
- [ ] Identify key optimization opportunities
- [ ] Plan token budget (current → target)

**During Implementation:**
- [ ] Apply patterns consistently
- [ ] Test incrementally
- [ ] Document decisions
- [ ] Validate token reduction

**After Completing Each Skill:**
- [ ] Test on 3 project sizes
- [ ] Verify functionality maintained
- [ ] Check pattern consistency
- [ ] Update TOKEN_OPTIMIZATION_AUDIT.md

**After Completing Each Sub-Batch:**
- [ ] Aggregate metrics validation
- [ ] Cross-skill pattern review
- [ ] Integration testing
- [ ] Documentation review

---

## Next Steps

### Immediate Actions (Week 1)

1. **Setup:**
   - [ ] Create shared bash function library (`.claude/lib/token-optimization.sh`)
   - [ ] Prepare sample projects (small, medium, large) for validation
   - [ ] Set up token usage tracking (if not already done)

2. **Begin Batch 4A:**
   - [ ] Start with test-async (high priority, moderate complexity)
   - [ ] Apply all optimization patterns
   - [ ] Document learnings for subsequent skills

3. **Documentation:**
   - [ ] Update TOKEN_OPTIMIZATION_AUDIT.md with Batch 4 progress
   - [ ] Create Batch 4A implementation notes
   - [ ] Track token reduction metrics

### Follow-Up Actions (Week 2-8)

- Continue through sub-batches 4A → 4B → 4C → 4D
- Weekly progress updates to TOKEN_OPTIMIZATION_AUDIT.md
- Real-world validation on actual projects
- Pattern refinement based on learnings

### Completion Actions (Week 9-10)

- [ ] Update all documentation (README.md, CLAUDE.md, CHANGELOG.md)
- [ ] Create comprehensive Phase 2 Batch 4 summary
- [ ] Aggregate metrics analysis
- [ ] Plan Phase 2 Batch 5 (Tier 3 Power Tools - 16 skills)

---

## Appendix

### Complete Skill List (37 Skills)

**Batch 4A (10):** test-async, test-antipatterns, test-coverage, test-mutation, debug-root-cause, debug-session, performance-profile, bundle-analyze, lighthouse, memory-leak

**Batch 4B (8):** release-automation, pipeline-monitor, container-optimize, deployment-rollback, infrastructure, execute-plan, git-worktree, branch-finish

**Batch 4C (10):** api-docs-generate, graphql-schema, api-mock, schema-validate, query-optimize, seed-data, database-connect, postman-convert, openapi-types, inline-docs

**Batch 4D (9):** conflict-resolve, merge-strategy, git-bisect, complexity-reduce, duplication-detect, code-review-checklist, readme-generate, mock-generate, boilerplate

### Reference Documents

- `TOKEN_OPTIMIZATION_GUIDE.md` - Comprehensive optimization patterns
- `TOKEN_OPTIMIZATION_AUDIT.md` - Current status and metrics
- `CLAUDE.md` - Project overview and status
- `SKILLS_EXPANSION_PLAN.md` - Original skill planning

---

**Document Status:** 🔄 Active Planning - Ready for Implementation
**Created:** 2026-01-27
**Author:** AI DevStudio Project
**Next Action:** Begin Batch 4A - Testing & Debugging Workflows (10 skills)
