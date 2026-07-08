---
name: test-coverage
description: Analyze test coverage and suggest tests for uncovered code
disable-model-invocation: false
---

# Test Coverage Analysis & Enhancement

I'll analyze your test coverage, identify untested code paths, and suggest comprehensive tests for uncovered areas.

Arguments: `$ARGUMENTS` - specific paths or coverage focus areas

## Phase 1: Coverage Tool Detection

**Pre-Flight Checks:**
Before starting, I'll verify:
- Test framework and coverage tool availability
- Existing test configuration
- Coverage thresholds and requirements
- CI/CD coverage reporting setup

<think>
When analyzing test coverage:
- Line coverage is basic but can be misleading (executes but doesn't assert)
- Branch coverage reveals untested conditionals and error paths
- Function coverage shows unused functionality
- Statement coverage differs from line coverage (multiple statements per line)
- 100% coverage doesn't guarantee quality - need meaningful assertions
- Uncovered code often hides edge cases and error handling
</think>

**Coverage Tool Detection:**
```bash
# Auto-detect coverage tooling
detect_coverage_tool() {
    if [ -f "package.json" ]; then
        # JavaScript/TypeScript ecosystem
        if grep -q "jest" package.json; then
            echo "jest --coverage"
        elif grep -q "vitest" package.json; then
            echo "vitest --coverage"
        elif grep -q "c8" package.json; then
            echo "c8"
        elif grep -q "nyc" package.json || grep -q "istanbul" package.json; then
            echo "nyc"
        fi
    elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
        # Python ecosystem
        if grep -q "pytest-cov" pyproject.toml setup.py requirements.txt 2>/dev/null; then
            echo "pytest-cov"
        elif command -v coverage >/dev/null 2>&1; then
            echo "coverage"
        fi
    elif [ -f "go.mod" ]; then
        # Go has built-in coverage
        echo "go test -cover"
    elif [ -f "Gemfile" ]; then
        # Ruby ecosystem
        if grep -q "simplecov" Gemfile; then
            echo "simplecov"
        fi
    elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
        # Java ecosystem
        echo "jacoco"
    fi
}

COVERAGE_TOOL=$(detect_coverage_tool)

if [ -z "$COVERAGE_TOOL" ]; then
    echo "No coverage tool detected. Suggestions:"
    echo "  - JavaScript: npm install --save-dev jest (includes coverage)"
    echo "  - Python: pip install pytest-cov"
    echo "  - Go: Built-in (go test -cover)"
    echo "  - Ruby: gem install simplecov"
    exit 1
fi

echo "Detected coverage tool: $COVERAGE_TOOL"
```

**Coverage Report Generation:**
I'll use bash to run coverage and parse reports efficiently:
```bash
# Generate coverage report with minimal output formats
case "$COVERAGE_TOOL" in
    "jest --coverage")
        # Only generate JSON summary (skip HTML report generation)
        npm test -- --coverage --coverageReporters=json-summary 2>&1 | tail -20
        ;;
    "pytest-cov")
        # Only generate JSON report (skip HTML)
        pytest --cov=. --cov-report=json --cov-report=term-missing:skip-covered 2>&1 | tail -20
        ;;
    "go test -cover")
        go test -coverprofile=coverage.out ./... 2>&1
        go tool cover -func=coverage.out | tail -20
        ;;
esac

# Parse coverage summary (avoid reading thousands of lines of HTML)
if [ -f "coverage/coverage-summary.json" ]; then
    # Jest/NYC format - extract just total metrics
    jq -c '.total' coverage/coverage-summary.json
elif [ -f "coverage.json" ]; then
    # pytest-cov format - extract just summary
    jq -c '.totals' coverage.json
fi
```

This gets coverage metrics without reading thousands of lines of HTML reports, saving 90%+ tokens.

## Phase 2: Coverage Metrics Analysis

**I'll analyze multiple coverage dimensions:**

1. **Line Coverage**
   - Percentage of lines executed
   - Identifies completely untested files

2. **Branch Coverage**
   - Percentage of if/else, switch paths tested
   - More meaningful than line coverage

3. **Function Coverage**
   - Percentage of functions called
   - Identifies unused code

4. **Statement Coverage**
   - More granular than line coverage
   - Multiple statements per line counted separately

**Coverage Report Parsing:**
```bash
# Extract low-coverage files for targeted analysis
parse_low_coverage_files() {
    if [ -f "coverage/coverage-summary.json" ]; then
        # Extract files with <80% coverage
        jq -r 'to_entries[] |
               select(.value.lines.pct < 80) |
               "\(.key): \(.value.lines.pct)% lines, \(.value.branches.pct)% branches"' \
               coverage/coverage-summary.json
    fi
}

LOW_COVERAGE_FILES=$(parse_low_coverage_files)
```

**Coverage Threshold Checking:**
```bash
# Check if project has coverage requirements
check_coverage_thresholds() {
    # Jest configuration
    if [ -f "jest.config.js" ] || [ -f "jest.config.json" ]; then
        grep -A 10 "coverageThreshold" jest.config.* 2>/dev/null
    fi

    # pytest configuration
    if [ -f "pyproject.toml" ]; then
        grep -A 5 "fail_under" pyproject.toml 2>/dev/null
    fi

    # Go coverage threshold (custom)
    if [ -f ".coverage-threshold" ]; then
        cat .coverage-threshold
    fi
}

THRESHOLDS=$(check_coverage_thresholds)
```

## Phase 3: Uncovered Code Identification

**Strategic File Analysis:**

I'll focus on files with coverage gaps using Grep before full Read:

```bash
# Find uncovered functions in low-coverage files (JavaScript/TypeScript)
Grep pattern="^(export )?(async )?function \w+"
     glob="$LOW_COVERAGE_FILE_PATTERN"
     output_mode="content"
     head_limit=15
     -n=true

# Find uncovered classes in low-coverage files (Python)
Grep pattern="^class \w+"
     glob="$LOW_COVERAGE_FILE_PATTERN"
     output_mode="content"
     head_limit=15
     -n=true

# Find error handling that might be uncovered
Grep pattern="throw new|raise |catch \(|except "
     glob="$LOW_COVERAGE_FILE_PATTERN"
     output_mode="content"
     head_limit=10
```

**Uncovered Code Patterns I'll Identify:**

1. **Error Handling Paths**
   ```javascript
   try {
       await operation();
   } catch (error) {
       // UNCOVERED: Error path not tested
       logger.error(error);
       throw new CustomError(error);
   }
   ```

2. **Edge Cases in Conditionals**
   ```javascript
   if (value > 100) {
       return 'high';
   } else if (value > 50) {
       return 'medium';
   } else {
       return 'low'; // UNCOVERED: Never tested
   }
   ```

3. **Validation Logic**
   ```python
   def validate_input(data):
       if not data:
           raise ValueError("Data required")  # UNCOVERED
       if not isinstance(data, dict):
           raise TypeError("Dict required")   # UNCOVERED
       return True
   ```

4. **Async Error Paths**
   ```javascript
   async function fetchData(url) {
       if (!url) {
           throw new Error('URL required'); // UNCOVERED
       }

       const response = await fetch(url);

       if (!response.ok) {
           throw new Error('Fetch failed'); // UNCOVERED
       }

       return response.json();
   }
   ```

5. **Default/Fallback Cases**
   ```javascript
   switch (action.type) {
       case 'CREATE':
           return handleCreate(action);
       case 'UPDATE':
           return handleUpdate(action);
       default:
           return state; // UNCOVERED: Default case not tested
   }
   ```

## Phase 4: Missing Test Identification

**I'll identify critical gaps:**

1. **Untested Public APIs**
   ```bash
   # Find exported functions
   EXPORTED_FUNCTIONS=$(Grep pattern="^export (async )?function (\w+)"
                             glob="src/**/*.{js,ts}"
                             output_mode="content"
                             head_limit=20)

   # Check which ones lack tests (bash comparison)
   echo "$EXPORTED_FUNCTIONS" | while read -r line; do
       FUNC_NAME=$(echo "$line" | grep -oP "function \K\w+")
       # Quick Grep check in test files
       HAS_TEST=$(Grep pattern="$FUNC_NAME"
                       glob="**/*.{test,spec}.*"
                       output_mode="files_with_matches"
                       head_limit=1)
       [ -z "$HAS_TEST" ] && echo "UNTESTED: $FUNC_NAME"
   done
   ```

2. **Untested Error Scenarios**
   ```bash
   # Find error throwing code in low-coverage files
   Grep pattern="throw new|raise |throw Error"
        glob="$LOW_COVERAGE_FILE_PATTERN"
        output_mode="content"
        head_limit=15
        -n=true
   ```

3. **Untested Edge Cases**
   - Empty array/object handling
   - Null/undefined checks
   - Boundary values (0, -1, MAX_INT)
   - Invalid input types

4. **Integration Points**
   - API endpoints
   - Database operations
   - External service calls
   - File system operations

## Phase 5: Test Suggestions & Generation

**For each uncovered area, I'll suggest tests:**

**Example: Uncovered Error Path**
```javascript
// Uncovered code in src/user-service.js:
async function createUser(data) {
    if (!data.email) {
        throw new Error('Email required'); // UNCOVERED
    }
    return db.users.create(data);
}

// Suggested test:
describe('UserService.createUser', () => {
    it('should throw error when email is missing', async () => {
        await expect(createUser({ name: 'Test' }))
            .rejects.toThrow('Email required');
    });

    it('should throw error when email is null', async () => {
        await expect(createUser({ email: null, name: 'Test' }))
            .rejects.toThrow('Email required');
    });

    it('should throw error when email is empty string', async () => {
        await expect(createUser({ email: '', name: 'Test' }))
            .rejects.toThrow('Email required');
    });
});
```

**Example: Uncovered Branch**
```python
# Uncovered code in src/calculator.py:
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")  # UNCOVERED
    return a / b

# Suggested test:
def test_divide_by_zero():
    """Test division by zero raises ValueError"""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_by_negative():
    """Test division by negative number"""
    assert divide(10, -2) == -5.0

def test_divide_floats():
    """Test division with floating point precision"""
    assert abs(divide(1, 3) - 0.333333) < 0.00001
```

**Example: Uncovered Edge Case**
```javascript
// Uncovered code in src/array-utils.js:
function getFirst(arr) {
    return arr[0]; // What if arr is empty? UNCOVERED
}

// Suggested tests:
describe('getFirst', () => {
    it('should return first element of array', () => {
        expect(getFirst([1, 2, 3])).toBe(1);
    });

    it('should return undefined for empty array', () => {
        expect(getFirst([])).toBeUndefined();
    });

    it('should handle single-element array', () => {
        expect(getFirst([42])).toBe(42);
    });

    it('should return first element even if falsy', () => {
        expect(getFirst([0, 1, 2])).toBe(0);
        expect(getFirst([null, 1, 2])).toBeNull();
    });
});
```

## Phase 6: Coverage Improvement Strategy

**Prioritization Framework:**

I'll prioritize test additions based on:

1. **Risk Level (Critical → Low)**
   - Critical: Security, data integrity, financial logic
   - High: Core business logic, user-facing features
   - Medium: Utility functions, helpers
   - Low: Logging, formatting, trivial getters

2. **Impact (High → Low)**
   - High: Code used frequently, critical paths
   - Medium: Occasional use, important features
   - Low: Rarely used, edge features

3. **Effort (Low → High)**
   - Low: Simple unit tests, pure functions
   - Medium: Mocked integration tests
   - High: Complex integration/E2E tests

**Coverage Improvement Plan:**
```
COVERAGE IMPROVEMENT STRATEGY
==============================

Phase 1: Critical Uncovered Code (Priority: High Risk + High Impact)
├── auth/login.js:45-52 - Error handling in authentication
├── payment/process.js:78-85 - Failed payment scenarios
└── user/validate.js:23-30 - Input validation edge cases

Phase 2: Important Features (Priority: High Impact + Low Effort)
├── api/users.js:120-135 - User creation edge cases
├── utils/format.js:45-60 - Edge cases in formatting
└── services/email.js:89-95 - Email send failure handling

Phase 3: Code Quality (Priority: Medium Impact + Low Effort)
├── helpers/string.js:12-25 - String utility edge cases
├── models/user.js:67-72 - Model validation
└── config/parser.js:34-40 - Config parsing errors

Phase 4: Comprehensive Coverage (Priority: Low Risk + Low Effort)
├── utils/constants.js - Getter coverage
├── types/validators.js - Type checking edge cases
└── formatters/date.js - Date formatting edge cases
```

## Phase 7: Test Generation & Implementation

**I'll generate and add tests:**

1. **Create git checkpoint**
   ```bash
   git add -A
   git commit -m "Pre test-coverage-improvement checkpoint" || echo "No changes"
   ```

2. **Generate tests for uncovered code:**
   - Write comprehensive test cases
   - Cover all branches and edge cases
   - Include descriptive test names
   - Add comments explaining edge cases

3. **Verify coverage improvement:**
   ```bash
   # Run tests with coverage
   npm test -- --coverage

   # Compare before/after coverage
   echo "Coverage improved from X% to Y%"
   ```

4. **Validate test quality:**
   - Tests actually assert behavior
   - No false positives (tests that pass without testing)
   - Good test organization and naming
   - Proper setup/teardown

## Integration with Existing Skills

**Workflow Integration:**
- After `/test` runs → Check coverage with `/test-coverage`
- After `/scaffold` → Ensure new code has tests
- Before `/commit` → Verify coverage thresholds met
- During `/review` → Include coverage analysis
- With `/test-async` → Cover async edge cases
- With `/test-antipatterns` → Quality + coverage together

**Skill Suggestions:**
- Low coverage in complex async → `/test-async`
- Coverage but poor quality → `/test-antipatterns`
- New feature needs tests → `/tdd-red-green`
- Complex uncovered logic → `/explain-like-senior`

## Reporting

**I'll provide comprehensive coverage analysis:**

```
TEST COVERAGE ANALYSIS REPORT
==============================

CURRENT COVERAGE:
├── Lines: 78.5% (target: 80%)
├── Branches: 65.2% (target: 75%)
├── Functions: 82.1% (target: 85%)
└── Statements: 77.8% (target: 80%)

FILES BELOW THRESHOLD:
├── src/auth/login.js: 45.2% (critical!)
├── src/payment/process.js: 52.8% (critical!)
├── src/api/users.js: 71.3%
├── src/utils/validate.js: 68.9%
└── src/helpers/format.js: 74.5%

UNCOVERED CRITICAL CODE:
├── Error handling paths: 23 instances
├── Edge case branches: 18 instances
├── Validation logic: 12 instances
└── Async error paths: 8 instances

TESTS SUGGESTED:
├── Authentication error scenarios: 8 tests
├── Payment failure handling: 6 tests
├── Input validation edge cases: 12 tests
├── API error responses: 10 tests
└── Utility function edge cases: 15 tests

AFTER IMPROVEMENTS:
├── Lines: 78.5% → 87.3% (+8.8%)
├── Branches: 65.2% → 81.7% (+16.5%)
├── Functions: 82.1% → 91.2% (+9.1%)
└── Statements: 77.8% → 86.9% (+9.1%)

TESTS ADDED: 51 new tests
FILES MODIFIED: 12 test files
EXECUTION TIME: +2.3s (acceptable)

NEXT STEPS:
├── Run tests to verify all pass
├── Review generated tests for quality
├── Update CI/CD coverage thresholds
└── Document testing coverage requirements
```

## Coverage Tools Configuration

**I can help set up coverage tools:**

**Jest (JavaScript/TypeScript):**
```json
{
  "jest": {
    "collectCoverage": true,
    "coverageDirectory": "coverage",
    "coverageReporters": ["text", "lcov", "json-summary"],
    "coverageThreshold": {
      "global": {
        "lines": 80,
        "branches": 75,
        "functions": 85,
        "statements": 80
      }
    },
    "collectCoverageFrom": [
      "src/**/*.{js,ts}",
      "!src/**/*.d.ts",
      "!src/**/*.test.{js,ts}"
    ]
  }
}
```

**pytest-cov (Python):**
```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80"

[tool.coverage.run]
omit = ["*/tests/*", "*/test_*.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError"
]
```

## Safety Guarantees

**What I'll NEVER do:**
- Generate tests that don't actually test
- Lower coverage thresholds to "pass"
- Test implementation details instead of behavior
- Add AI attribution to commits or code
- Create tests that give false confidence

**What I WILL do:**
- Generate meaningful, behavior-focused tests
- Cover edge cases and error paths
- Improve actual code quality, not just metrics
- Maintain test maintainability
- Create clear commit messages (no AI attribution)

## Credits

This skill is based on:
- **Istanbul/nyc** - JavaScript coverage tool standards
- **Jest** - Built-in coverage capabilities
- **pytest-cov** - Python coverage testing
- **JaCoCo** - Java code coverage library
- **SimpleCov** - Ruby coverage analysis
- **Testing Best Practices** - Community-driven coverage guidelines

## Token Optimization

**Expected range**: 1,200–2,000 tokens (initial), 200 tokens (coverage good)

**Caching**: Caches coverage tool detection in `.claude/cache/test-coverage/tool.json` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if all coverage thresholds are already met.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
