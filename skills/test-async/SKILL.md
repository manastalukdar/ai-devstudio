---
name: test-async
description: Async testing patterns with race condition and timing issue detection
disable-model-invocation: false
---

# Async Testing Pattern Analysis

I'll analyze and improve your async testing patterns, detecting race conditions, timing issues, and async/await anti-patterns.

Arguments: `$ARGUMENTS` - specific paths or async focus areas

## Phase 1: Async Pattern Discovery

**Pre-Flight Checks:**
Before starting, I'll verify:
- Test framework supports async testing (Jest, Mocha, Vitest, pytest-asyncio)
- Project uses async patterns (async/await, Promises, callbacks)
- Existing test files with async operations

<think>
When analyzing async testing:
- Race conditions often hide in Promise.all(), concurrent operations
- Timing issues manifest as flaky tests that pass/fail randomly
- Missing await keywords create silent failures
- Callback-based code needs proper done() handling
- Event emitters require careful cleanup to avoid leaks
- Timeout configurations affect test reliability
</think>

**Framework Detection:**
```bash
# Auto-detect async testing capabilities
if [ -f "package.json" ]; then
    # JavaScript/TypeScript ecosystem
    if grep -q "jest" package.json; then
        echo "Detected: Jest (supports async/await, done callbacks)"
    elif grep -q "mocha" package.json; then
        echo "Detected: Mocha (supports async/await, done callbacks)"
    elif grep -q "vitest" package.json; then
        echo "Detected: Vitest (supports async/await)"
    fi
fi

if [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    # Python ecosystem
    if grep -q "pytest-asyncio" pyproject.toml setup.py requirements.txt 2>/dev/null; then
        echo "Detected: pytest with asyncio support"
    fi
fi

# Check Go async testing patterns
if [ -f "go.mod" ]; then
    echo "Detected: Go (goroutines, channels in tests)"
fi
```

**Async Pattern Discovery:**
I'll use Grep first to identify files with async patterns before reading:
```bash
# Find files with async patterns (JavaScript/TypeScript)
Grep pattern="async |await |Promise\.|\.then\(|\.catch\("
     glob="**/*.{test,spec}.{js,ts,jsx,tsx}"
     output_mode="files_with_matches"
     head_limit=20

# Find files with async patterns (Python)
Grep pattern="async def|await |asyncio\."
     glob="**/test_*.py"
     output_mode="files_with_matches"
     head_limit=20

# Find files with goroutines (Go)
Grep pattern="go func|chan "
     glob="**/*_test.go"
     output_mode="files_with_matches"
     head_limit=20
```

This targets analysis to files that actually use async patterns, limiting results to avoid token explosion.

## Phase 2: Anti-Pattern Detection

I'll scan for common async anti-patterns:

**JavaScript/TypeScript Anti-Patterns:**

1. **Missing await** - Most dangerous, creates silent failures
   ```javascript
   // BAD: Promise not awaited
   async function test() {
       doAsyncOperation(); // Forgot await!
       expect(result).toBe(expected); // Runs before async completes
   }
   ```

2. **Floating Promises** - Unhandled rejections
   ```javascript
   // BAD: No error handling
   async function test() {
       Promise.all([op1(), op2()]); // Missing await + no catch
   }
   ```

3. **Race Conditions in Assertions**
   ```javascript
   // BAD: State changes race with assertions
   async function test() {
       await triggerAsync();
       expect(state.value).toBe(1); // Might not be updated yet
   }
   ```

4. **setTimeout/setInterval in Tests**
   ```javascript
   // BAD: Timing-dependent tests
   setTimeout(() => {
       expect(callback).toHaveBeenCalled();
       done();
   }, 100); // Brittle, slow, flaky
   ```

5. **Missing done() with Callbacks**
   ```javascript
   // BAD: Test completes before callback
   it('should call callback', (done) => {
       asyncOperation((result) => {
           expect(result).toBe(expected);
           // Forgot done()!
       });
   });
   ```

**Python Anti-Patterns:**

1. **Mixing sync and async** - Common with pytest
   ```python
   # BAD: Missing pytest-asyncio marker
   async def test_async_function():
       result = await async_operation()
       assert result == expected
   ```

2. **Blocking calls in async** - Deadlock risk
   ```python
   # BAD: Blocking in async context
   async def test_concurrent():
       result = time.sleep(1)  # Should be asyncio.sleep()
   ```

**Go Anti-Patterns:**

1. **Missing WaitGroup** - Tests exit before goroutines complete
   ```go
   // BAD: Test exits before goroutine finishes
   func TestAsync(t *testing.T) {
       go doAsync() // Test might finish first
       // No WaitGroup or channel to sync
   }
   ```

2. **Unbuffered channels** - Potential deadlocks
   ```go
   // BAD: Can deadlock
   ch := make(chan int)
   ch <- 1 // Blocks if nothing receiving
   ```

## Phase 3: Race Condition Analysis

**Detection Strategy:**

I'll look for:
- Shared mutable state accessed by concurrent operations
- Missing synchronization primitives (locks, semaphores)
- Incorrect Promise.all() usage
- Event listener registration/cleanup issues
- Database connection pooling problems

**JavaScript Race Condition Patterns:**
```bash
# Find concurrent operations without proper sequencing
Grep pattern="Promise\.all|Promise\.race|Promise\.allSettled"
     glob="**/*.{test,spec}.*"
     output_mode="content"
     head_limit=10

# Find potential state races (mutable variables in tests)
Grep pattern="(let |var )"
     glob="**/*.test.*"
     output_mode="files_with_matches"
     head_limit=20

# Find event emitter usage (cleanup risks)
Grep pattern="addEventListener|\.on\(|\.once\("
     glob="**/*.test.*"
     output_mode="content"
     head_limit=10
```

**Analysis Output:**
For each potential race condition:
- File and line number
- Concurrent operations involved
- Shared state at risk
- Suggested fix (proper await sequencing, locking)

## Phase 4: Timing Issue Detection

**Flaky Test Indicators:**

I'll identify tests that depend on timing:
- setTimeout/setInterval usage
- Fixed delays (sleep, waitFor with hardcoded values)
- Polling without proper conditions
- Missing waitFor/waitUntil patterns

**Better Patterns I'll Suggest:**

1. **Use Proper Waiters** (Jest/Vitest)
   ```javascript
   // GOOD: Condition-based waiting
   await waitFor(() => {
       expect(screen.getByText('Loaded')).toBeInTheDocument();
   }, { timeout: 5000 });
   ```

2. **Mock Timers** (Jest)
   ```javascript
   // GOOD: Control time in tests
   jest.useFakeTimers();
   asyncOperation();
   jest.runAllTimers();
   expect(result).toBe(expected);
   ```

3. **Proper Async Assertions** (Python)
   ```python
   # GOOD: Wait for condition
   async def test_async():
       await asyncio.wait_for(
           wait_for_condition(),
           timeout=5.0
       )
   ```

## Phase 5: Remediation & Fixes

**Systematic Fix Process:**

1. **Create git checkpoint**
   ```bash
   git add -A
   git commit -m "Pre async-testing-fixes checkpoint" || echo "No changes"
   ```

2. **Fix anti-patterns by priority:**
   - Critical: Missing awaits (silent failures)
   - High: Race conditions (data corruption)
   - Medium: Timing dependencies (flaky tests)
   - Low: Cleanup issues (resource leaks)

3. **Apply fixes safely:**
   - Add missing await keywords
   - Replace setTimeout with waitFor
   - Add proper error handling
   - Fix event listener cleanup
   - Add synchronization primitives

4. **Verify fixes:**
   - Run affected tests multiple times
   - Check for new timing issues
   - Validate error handling works
   - Ensure tests still test intended behavior

## Phase 6: Test Enhancement

**I'll suggest improvements:**

1. **Add async test helpers:**
   ```javascript
   // Create reusable helpers for common patterns
   async function waitForCondition(predicate, timeout = 5000) {
       const start = Date.now();
       while (!predicate()) {
           if (Date.now() - start > timeout) {
               throw new Error('Condition timeout');
           }
           await new Promise(resolve => setTimeout(resolve, 50));
       }
   }
   ```

2. **Improve test isolation:**
   - Proper beforeEach/afterEach cleanup
   - Reset mocks and timers
   - Clear event listeners
   - Reset shared state

3. **Add race condition tests:**
   ```javascript
   it('should handle concurrent requests safely', async () => {
       const results = await Promise.all([
           api.request(1),
           api.request(2),
           api.request(3)
       ]);
       expect(results).toHaveLength(3);
       // Verify no data corruption
   });
   ```

## Integration with Existing Skills

**Workflow Integration:**
- After `/test` detects flaky tests → Run `/test-async`
- Before `/commit` → Check async patterns with `/test-async`
- During `/review` → Include async pattern analysis
- With `/test-antipatterns` → Comprehensive test quality check

**Skill Suggestions:**
- Found complex race conditions → `/debug-systematic`
- Need deeper test analysis → `/test-antipatterns`
- Coverage gaps in async code → `/test-coverage`
- Implementing new async features → `/tdd-red-green`

## Reporting

**I'll provide a comprehensive report:**

```
ASYNC TESTING ANALYSIS REPORT
==============================

Files Analyzed: 45 test files
Async Patterns Found: 127

ISSUES DETECTED:
├── Missing await: 12 instances (CRITICAL)
├── Race conditions: 5 potential cases (HIGH)
├── Timing dependencies: 8 tests (MEDIUM)
├── Missing error handling: 15 cases (MEDIUM)
└── Cleanup issues: 6 cases (LOW)

FIXES APPLIED:
├── Added await keywords: 12
├── Replaced setTimeout: 8
├── Added proper waitFor: 8
├── Fixed error handling: 15
├── Added cleanup: 6

RECOMMENDATIONS:
├── Add async test helpers
├── Enable strict async lint rules
├── Run tests multiple times in CI
└── Document async testing patterns
```

## Safety Guarantees

**What I'll NEVER do:**
- Modify tests to pass incorrectly
- Remove async complexity without understanding
- Add AI attribution to commits or code
- Change test behavior without verification
- Skip necessary async operations

**What I WILL do:**
- Preserve test intent and coverage
- Fix genuine async bugs
- Improve test reliability
- Maintain code quality
- Create clear commit messages (no AI attribution)

## Credits

This skill is based on:
- **obra/superpowers** - TDD and testing methodology
- **Jest Testing Best Practices** - Async testing patterns
- **pytest-asyncio** - Python async testing standards
- **Go Testing Package** - Goroutine testing patterns

## Token Optimization

**Expected range**: 1,200–2,000 tokens (initial), 200 tokens (no issues)

**Caching**: Caches framework detection in `.claude/cache/test-async/framework.json` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if no async testing issues are detected.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
