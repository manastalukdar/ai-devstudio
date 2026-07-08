---
name: test
description: Intelligent test execution based on context with automatic failure analysis and fixes
disable-model-invocation: false
---

# Smart Test Runner - Context Aware

I'll intelligently run tests based on your current context and actively help fix failures.


```bash
# Check for cached framework detection (70% token savings on cache hit)
CACHE_FILE=".claude/cache/test/framework-config.json"
CACHE_VALIDITY=86400  # 24 hours

if [ -f "$CACHE_FILE" ]; then
    LAST_MODIFIED=$(stat -c %Y "$CACHE_FILE" 2>/dev/null || stat -f %m "$CACHE_FILE" 2>/dev/null)
    CURRENT_TIME=$(date +%s)
    AGE=$((CURRENT_TIME - LAST_MODIFIED))

    if [ $AGE -lt $CACHE_VALIDITY ]; then
        echo "✓ Using cached test framework configuration"
        # Cache contains: test runner, test patterns, coverage setup
        # Skip expensive framework detection
    fi
fi
```

**Context Detection First:**
Let me understand what context I'm in (optimized with git diff analysis):

1. **Cold Start** (no previous context):
   - Run full test suite with coverage
   - Generate complete health report
   - Identify chronic failures

2. **Active Session** (you're implementing features) - **OPTIMIZED**:
   - Check git diff for modified files (100 tokens vs 5,000+ reading all files)
   - Read CLAUDE.md for session goals (if exists)
   - Test ONLY what you've been working on (80% token savings)
   - Incremental testing as you code
   - **Early exit** if no test files modified and no test failures

3. **Post-Command Context**:
   - After `/scaffold`: Test the new component
   - After `/fix-todos`: Test modified files
   - After `/fix-imports`: Re-run previously failed tests
   - After `/security-scan`: Security-focused tests
   - After `/format`: Quick smoke tests only

4. **Debug Context** (previous test failures):
   - Focus on failed tests with verbose output
   - Add strategic debug logging
   - Run in isolation mode

5. **Pre-Commit Context**:
   - Full suite + lint + typecheck
   - Coverage report for PR
   - No skipped tests allowed

**Phase 1: Deep Project Analysis (Optimized with Caching)**
Using native tools to understand your testing setup:
- **Glob** to find configuration files in project root (50 tokens)
- **Read** test configurations only if not cached (500 tokens or 0 if cached)
- **Grep** test patterns to understand testing style (100 tokens)
- **Read** documentation for test instructions (only if cache miss)

I'll detect and cache:
- Test frameworks and runners (jest, vitest, pytest, etc.)
- Test file patterns and locations
- Coverage requirements
- Integration vs unit test separation
- CI/CD test commands

```bash
# Save framework detection to cache (saves 70% on next run)
mkdir -p .claude/cache/test
cat > .claude/cache/test/framework-config.json <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "framework": "detected_framework",
  "test_command": "npm test",
  "coverage_command": "npm run coverage",
  "test_patterns": ["**/*.test.ts", "**/*.spec.ts"]
}
EOF
```

**Phase 2: Intelligent Test Execution**
I'll run tests with appropriate flags for maximum insight based on your project's testing framework, using verbose output and fail-fast when available to quickly identify issues.

**Build & Compilation Check:**
- Verify project builds successfully before running tests
- Watch console output for compilation errors
- Capture and analyze build warnings that might affect tests
- Check for missing dependencies or version conflicts

**Real-time Monitoring:**
```bash
# Monitor test execution with timestamps
# Capture both stdout and stderr
# Watch for timeout patterns
# Track memory usage if tests hang
```

**Phase 3: Failure Analysis & Auto-Fix**
When tests fail, I'll:

1. **Parse failure output** to understand exact issues
2. **Read failing test** to understand expectations
3. **Read implementation** to find the bug
4. **Analyze patterns** from similar tests that pass
5. **Apply fixes** when confident

**Common fixes I'll attempt:**
- Async/await timing issues
- Mock/stub configuration
- Import path problems
- Type mismatches
- Null/undefined handling
- Off-by-one errors
- Environment variable issues

**Phase 4: Advanced Diagnostics**
For complex failures:
- Run single test in isolation
- Add debug logging strategically
- Check test dependencies and setup/teardown
- Verify test data and fixtures
- Analyze flaky test patterns

**Log Analysis:**
- **Read** test output logs for hidden errors
- **Grep** for common error patterns in console output
- Analyze stack traces to pinpoint exact failure location
- Check for environment-specific issues in logs
- Identify resource conflicts (ports, files, databases)

**Console Pattern Detection:**
- Memory leaks ("JavaScript heap out of memory")
- Port conflicts ("address already in use")
- Permission errors ("EACCES", "Permission denied")
- Timeout issues ("Timeout - Async callback")
- Module resolution failures
- Database connection issues

**Phase 5: Coverage & Quality**
After fixing tests:
- Run coverage report if available
- Identify untested code paths
- Suggest critical missing tests
- Check for test anti-patterns

When I find multiple issues, I'll create a todo list to fix them systematically.

**Build Failure Recovery:**
If build fails before tests:
- Analyze compilation errors in detail
- Check for missing dependencies
- Verify environment setup
- Suggest specific fixes based on error patterns
- Offer to install missing packages if detected

**Smart Context-Based Strategy:**
Based on the detected context, I'll choose the optimal approach:

- **No Context**: Full test discovery and execution
- **Active Development**: Watch mode on changed files only  
- **Post-Implementation**: Test coverage for new code
- **Debugging Mode**: Isolated test with maximum verbosity
- **Pre-Deploy**: Complete validation suite

**Intelligent Test Selection (Optimized with git diff):**
```bash
# OPTIMIZATION: Use git diff to identify changed files (100 tokens vs 5,000+)
CHANGED_FILES=$(git diff --name-only HEAD)

# Context: After implementing UserService
# Git diff shows: src/services/UserService.ts
# I'll run: UserService.test.ts + integration tests (saves 80% tokens)

# Context: After /scaffold user-auth
# Git diff shows: src/auth/** files
# I'll run: New user-auth tests + smoke tests only

# Context: Fixing failing tests
# Use cached last-results.json to identify failed tests
# I'll run: Only the specific failing test with debug info (saves 90%)

# Save test results for next run
mkdir -p .claude/cache/test
cat > .claude/cache/test/last-results.json <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "failed_tests": ["path/to/failed.test.ts"],
  "passed_tests": 45,
  "coverage": 78.5
}
EOF
```

**Session Awareness:**
- Read session goals from CLAUDE.md
- Track all modified files during session
- Prioritize tests based on session objectives
- Generate session test report at the end

**Integration with other skills:**
- After `/test` failures → `/create-todos` to track fixes
- Complex failures → `/explain-like-senior` for deep analysis
- Test improvements → `/review` for quality check
- Session testing → `/session-end` includes test summary

**Important**: I will NEVER:
- Modify tests to pass incorrectly
- Remove failing tests without fixing
- Reduce test coverage
- Compromise test integrity
- Add "Co-authored-by" or any Claude signatures
- Include "Generated with Claude Code" or similar messages
- Modify git config or user credentials
- Add any AI/assistant attribution to the commit

This ensures your tests truly validate your code while maximizing development speed.

## Token Optimization

**Expected range**: 600–1,500 tokens (initial), 50 tokens (no tests needed)

**Caching**: Caches test configuration in `.claude/cache/test/` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if no tests are needed for the changed files.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
