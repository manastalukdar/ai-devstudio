---
name: test-antipatterns
description: Detect and fix testing anti-patterns for better test quality
disable-model-invocation: false
---

# Test Anti-Pattern Detection & Remediation

I'll identify and fix testing anti-patterns that create brittle, flaky, or slow tests.

Arguments: `$ARGUMENTS` - specific paths or anti-pattern focus areas

## Phase 1: Test Quality Assessment

**Pre-Flight Checks:**
Before starting, I'll verify:
- Test framework and runner configuration
- Test file locations and naming conventions
- Existing test patterns and style
- CI/CD test execution configuration

<think>
When analyzing test anti-patterns:
- Brittle tests break on unrelated changes (over-specification)
- Flaky tests pass/fail randomly (timing, state, randomness)
- Slow tests reduce productivity (unnecessary setup, poor isolation)
- Test interdependencies create cascade failures
- Poor mocking leads to integration tests disguised as unit tests
- Assertion roulette makes failures hard to diagnose
</think>

**Framework Detection:**
```bash
# Auto-detect testing framework
detect_test_framework() {
    if [ -f "package.json" ]; then
        if grep -q "jest" package.json; then
            echo "jest"
        elif grep -q "mocha" package.json; then
            echo "mocha"
        elif grep -q "vitest" package.json; then
            echo "vitest"
        elif grep -q "cypress" package.json; then
            echo "cypress"
        fi
    elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
        echo "pytest"
    elif [ -f "go.mod" ]; then
        echo "go-test"
    elif [ -f "Gemfile" ]; then
        echo "rspec"
    fi
}

FRAMEWORK=$(detect_test_framework)
echo "Detected test framework: $FRAMEWORK"
```

**Anti-Pattern Discovery:**
I'll use Grep to find test files with anti-pattern indicators:
```bash
# Find tests with timing anti-patterns (flaky tests)
Grep pattern="sleep|wait|setTimeout|setInterval"
     glob="**/*.{test,spec}.{js,ts,jsx,tsx,py}"
     output_mode="files_with_matches"
     head_limit=20

# Find disabled/focused tests (.only, .skip, fdescribe, etc.)
Grep pattern="\.only\(|\.skip\(|fdescribe|fit|xdescribe|xit"
     glob="**/*.{test,spec}.*"
     output_mode="files_with_matches"
     head_limit=20

# Find shared state indicators (test dependencies)
Grep pattern="beforeAll|afterAll"
     glob="**/*.{test,spec}.*"
     output_mode="files_with_matches"
     head_limit=20

# Find potential over-mocking
Grep pattern="jest\.mock|mock\(|spy\(|stub\("
     glob="**/*.test.*"
     output_mode="count"
     head_limit=20
```

This targets files likely to have anti-patterns before full Read analysis.

## Phase 2: Anti-Pattern Detection

I'll scan for these common anti-patterns:

### Category 1: Brittle Tests (Over-Specification)

**1. Implementation Detail Testing**
```javascript
// BAD: Testing internal implementation
expect(component.state.internalCounter).toBe(5);

// GOOD: Testing observable behavior
expect(component.getDisplayValue()).toBe('5');
```

**Detection:**
- Direct state access in tests
- Testing private methods
- Mocking every dependency
- Assertions on internal data structures

**2. Fragile Selectors (E2E/Integration)**
```javascript
// BAD: Brittle selectors
cy.get('div > ul > li:nth-child(3) > button.btn-primary')

// GOOD: Semantic selectors
cy.get('[data-testid="submit-button"]')
```

### Category 2: Flaky Tests (Non-Deterministic)

**1. Test Order Dependencies**
```javascript
// BAD: Tests depend on execution order
describe('User tests', () => {
    it('should create user', () => {
        user = createUser(); // Sets global state
    });

    it('should update user', () => {
        updateUser(user); // Depends on previous test
    });
});
```

**Detection Pattern:**
```bash
# Find tests that might share state (mutable variables)
Grep pattern="(let |var )"
     glob="**/*.test.*"
     output_mode="content"
     head_limit=10
     -B=2
     -A=2

# Find setup that creates shared state
Grep pattern="beforeAll|afterAll"
     glob="**/*.{test,spec}.*"
     output_mode="content"
     head_limit=10
```

**2. Random Data Issues**
```javascript
// BAD: Uncontrolled randomness
const testData = {
    id: Math.random(),
    timestamp: Date.now()
};

// GOOD: Deterministic test data
const testData = {
    id: 'test-id-123',
    timestamp: new Date('2024-01-01').getTime()
};
```

**3. Network/External Dependencies**
```python
# BAD: Real API calls in tests
def test_api():
    response = requests.get('https://api.example.com')
    assert response.status_code == 200

# GOOD: Mocked external calls
@patch('requests.get')
def test_api(mock_get):
    mock_get.return_value.status_code = 200
    response = api_client.fetch_data()
    assert response.status_code == 200
```

### Category 3: Slow Tests (Performance Issues)

**1. Unnecessary Database/IO**
```javascript
// BAD: Real DB for unit test
beforeEach(async () => {
    await database.reset();
    await database.seed();
});

// GOOD: In-memory or mocked
beforeEach(() => {
    repository = new InMemoryRepository();
});
```

**Detection:**
```bash
# Find tests with expensive database setup
Grep pattern="database\.|db\.|createConnection|mongoose\.connect|knex\("
     glob="**/*.{test,spec}.*"
     output_mode="files_with_matches"
     head_limit=15

# Find tests with expensive seeding operations
Grep pattern="beforeEach.*await.*(create|seed|insert)"
     glob="**/*.test.*"
     output_mode="content"
     head_limit=10
     multiline=true
```

**2. Excessive Test Fixtures**
```javascript
// BAD: Creating more data than needed
beforeEach(() => {
    users = createUsers(1000); // Only need 2-3
    posts = createPosts(5000);
    comments = createComments(10000);
});
```

**3. Sleep/Wait Anti-Patterns**
```javascript
// BAD: Arbitrary waits
await sleep(1000);
expect(element).toBeVisible();

// GOOD: Condition-based waiting
await waitFor(() => expect(element).toBeVisible());
```

### Category 4: Test Structure Issues

**1. Assertion Roulette**
```javascript
// BAD: Which assertion failed?
expect(result.id).toBeDefined();
expect(result.name).toBeDefined();
expect(result.email).toBeDefined();
expect(result.status).toBe('active');

// GOOD: Clear, specific assertions
expect(result).toMatchObject({
    id: expect.any(String),
    name: expect.any(String),
    email: expect.any(String),
    status: 'active'
});
```

**2. Mystery Guest**
```javascript
// BAD: Hidden test data
it('should validate user', () => {
    const user = getTestUser(); // What user?
    expect(validator.validate(user)).toBe(true);
});

// GOOD: Explicit test data
it('should validate user with valid email', () => {
    const user = { email: 'test@example.com', name: 'Test' };
    expect(validator.validate(user)).toBe(true);
});
```

**3. Test Logic in Tests**
```javascript
// BAD: Conditional logic in tests
if (config.environment === 'production') {
    expect(result).toBe(productionValue);
} else {
    expect(result).toBe(devValue);
}

// GOOD: Separate tests
it('should return production value in prod', () => {
    config.environment = 'production';
    expect(result()).toBe(productionValue);
});
```

### Category 5: Mock/Stub Anti-Patterns

**1. Over-Mocking**
```javascript
// BAD: Mocking everything = integration test disguised as unit
jest.mock('./service');
jest.mock('./repository');
jest.mock('./validator');
jest.mock('./logger');
jest.mock('./cache');

// GOOD: Mock only external boundaries
jest.mock('./apiClient');
```

**2. Not Verifying Mocks**
```javascript
// BAD: Mock without verification
const mockFn = jest.fn();
doSomething(mockFn);
// No assertion!

// GOOD: Verify mock usage
const mockFn = jest.fn();
doSomething(mockFn);
expect(mockFn).toHaveBeenCalledWith(expectedArgs);
```

### Category 6: Test Independence Issues

**1. Leftover State**
```python
# BAD: Global state not cleaned
cache = {}

def test_cache_set():
    cache['key'] = 'value'
    assert cache['key'] == 'value'

def test_cache_empty():
    assert len(cache) == 0  # FAILS if run after test_cache_set
```

**Detection:**
```bash
# Find global variables in test files (potential shared state)
Grep pattern="^(let|var|const) [A-Z_][A-Z0-9_]*\s*="
     glob="**/*.{test,spec}.*"
     output_mode="content"
     head_limit=10

# Find tests modifying global objects
Grep pattern="global\.|window\.|process\.env\[|document\."
     glob="**/*.test.*"
     output_mode="content"
     head_limit=10
```

## Phase 3: Flaky Test Identification

**Statistical Analysis:**
```bash
# Run tests multiple times to find flaky tests
echo "Running tests 10 times to detect flakiness..."
for i in {1..10}; do
    npm test 2>&1 | tee "test-run-$i.log"
done

# Analyze results
echo "Analyzing test stability..."
# Look for tests that sometimes pass, sometimes fail
```

**Common Flakiness Patterns:**
- Tests that use `Date.now()` or `new Date()`
- Tests with hardcoded timeouts
- Tests that depend on system resources
- Tests with race conditions
- Tests that don't clean up properly

## Phase 4: Test Interdependency Analysis

**Dependency Detection:**
```bash
# Find tests that might depend on execution order
Grep pattern="beforeAll|afterAll"
     glob="**/*.{test,spec}.*"
     output_mode="content"
     head_limit=10
     -B=2
     -A=10

# Find shared mutable state
Grep pattern="(let |var )"
     glob="**/*.test.*"
     output_mode="files_with_matches"
     head_limit=20

# Find tests marked as .only or .skip (test focus/skip indicators)
Grep pattern="\.only\(|\.skip\(|fdescribe|fit|xdescribe|xit"
     glob="**/*.{test,spec}.*"
     output_mode="content"
     head_limit=10
```

**Test Isolation Verification:**
I'll suggest running tests:
- In random order
- In reverse order
- Individual tests in isolation
- With different parallelization settings

## Phase 5: Remediation & Fixes

**Systematic Fix Process:**

1. **Create git checkpoint**
   ```bash
   git add -A
   git commit -m "Pre test-antipattern-fixes checkpoint" || echo "No changes"
   ```

2. **Fix anti-patterns by priority:**
   - **Critical**: Flaky tests (breaks CI/CD)
   - **High**: Test interdependencies (cascade failures)
   - **Medium**: Slow tests (developer productivity)
   - **Low**: Brittle tests (maintenance burden)

3. **Common Fixes I'll Apply:**

   **Fix Flaky Tests:**
   ```javascript
   // Before: Timing-dependent
   setTimeout(() => expect(value).toBe(true), 100);

   // After: Condition-based
   await waitFor(() => expect(value).toBe(true));
   ```

   **Fix Test Dependencies:**
   ```javascript
   // Before: Shared state
   let user;
   beforeAll(() => { user = createUser(); });

   // After: Isolated state
   beforeEach(() => { user = createUser(); });
   ```

   **Fix Slow Tests:**
   ```javascript
   // Before: Real DB
   beforeEach(async () => await db.migrate.latest());

   // After: In-memory
   beforeEach(() => { repo = new InMemoryRepo(); });
   ```

   **Fix Brittle Selectors:**
   ```javascript
   // Before: Implementation detail
   expect(component.find('div').at(2).text()).toBe('Hello');

   // After: Behavior-focused
   expect(screen.getByRole('heading')).toHaveTextContent('Hello');
   ```

4. **Verify fixes:**
   - Run tests multiple times
   - Run tests in random order
   - Check test execution time
   - Verify test isolation

## Phase 6: Test Quality Improvements

**Suggestions I'll Make:**

1. **Add Test Utilities:**
   ```javascript
   // Create reusable test builders
   function createTestUser(overrides = {}) {
       return {
           id: 'test-id',
           email: 'test@example.com',
           name: 'Test User',
           ...overrides
       };
   }
   ```

2. **Improve Test Organization:**
   ```javascript
   describe('UserService', () => {
       describe('create', () => {
           it('should create user with valid data', () => {});
           it('should reject invalid email', () => {});
           it('should reject duplicate email', () => {});
       });

       describe('update', () => {
           // Update tests
       });
   });
   ```

3. **Add Test Documentation:**
   ```javascript
   it('should calculate total with tax and shipping', () => {
       // Given: Cart with $100 items
       // When: Checkout in California (9% tax)
       // Then: Total = $100 + $9 + $10 shipping = $119
   });
   ```

## Integration with Existing Skills

**Workflow Integration:**
- After `/test` finds failures → Run `/test-antipatterns`
- Before `/commit` → Check test quality
- During `/review` → Include test anti-pattern analysis
- With `/test-async` → Comprehensive async test check
- With `/test-coverage` → Ensure quality tests, not just quantity

**Skill Suggestions:**
- Found complex async anti-patterns → `/test-async`
- Need coverage analysis → `/test-coverage`
- Implementing new features → `/tdd-red-green`
- Complex debugging needed → `/debug-systematic`

## Reporting

**I'll provide a comprehensive report:**

```
TEST ANTI-PATTERN ANALYSIS REPORT
==================================

Test Files Analyzed: 87
Total Tests: 432

ANTI-PATTERNS DETECTED:
├── Brittle Tests: 23 (over-specification, fragile selectors)
├── Flaky Tests: 8 (timing, state, randomness)
├── Slow Tests: 15 (unnecessary DB/IO, excessive setup)
├── Test Dependencies: 12 (shared state, order-dependent)
├── Poor Mocking: 18 (over-mocking, unverified mocks)
└── Structure Issues: 31 (assertion roulette, mystery guest)

SEVERITY BREAKDOWN:
├── Critical: 8 flaky tests (break CI/CD)
├── High: 12 interdependent tests (cascade failures)
├── Medium: 15 slow tests (>1s each)
└── Low: 71 maintainability issues

FIXES APPLIED:
├── Replaced setTimeout with waitFor: 8
├── Fixed shared state: 12
├── Optimized test setup: 15
├── Improved assertions: 23
├── Fixed mock verification: 18
├── Enhanced test organization: 31

PERFORMANCE IMPACT:
├── Before: 45.3s total test time
├── After: 12.8s total test time
└── Improvement: 71.7% faster

RECOMMENDATIONS:
├── Add test-utils for common builders
├── Enable random test order in CI
├── Set up test performance monitoring
├── Document testing best practices
└── Add pre-commit test quality checks
```

## Safety Guarantees

**What I'll NEVER do:**
- Remove tests to fix issues
- Modify tests to pass incorrectly
- Skip necessary test coverage
- Add AI attribution to commits or code
- Change test behavior without verification

**What I WILL do:**
- Preserve test intent and coverage
- Fix genuine anti-patterns
- Improve test reliability and speed
- Maintain test quality standards
- Create clear commit messages (no AI attribution)

## Credits

This skill is based on:
- **obra/superpowers** - TDD and testing methodology
- **xUnit Test Patterns** - Anti-pattern catalog by Gerard Meszaros
- **Jest Best Practices** - Testing patterns and anti-patterns
- **pytest Good Integration Practices** - Python testing standards
- **Testing Best Practices** - Community-driven testing guidelines

## Token Optimization

**Expected range**: 1,400–2,200 tokens (initial), 200 tokens (no issues)

**Caching**: Caches framework detection in `.claude/cache/test-antipatterns/framework.json` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if no anti-pattern violations are found.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
