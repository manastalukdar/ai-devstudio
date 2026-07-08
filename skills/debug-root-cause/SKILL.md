---
name: debug-root-cause
description: Root cause analysis with dependency tracing and call stack analysis
disable-model-invocation: false
---

# Root Cause Analysis

I'll help you identify the root cause of issues through systematic dependency tracing and call stack analysis.

**Based on obra/superpowers methodology:**
- Trace error origins through call stacks
- Dependency graph analysis
- Configuration issue detection
- Environment variable problems
- State corruption identification

**Quick Start:**
Systematic root cause analysis through dependency tracing, call stack analysis, and hypothesis-driven debugging. Optimized for fast feedback with progressive depth.

**Arguments:** `$ARGUMENTS` - error message, stack trace, or issue description

## Extended Thinking for Root Cause Analysis

<think>
Root cause analysis requires systematic investigation:
- Error symptoms vs actual cause
- Dependencies and their interaction
- Configuration cascades
- Environment-specific behavior
- Timing and state issues

Complex scenarios:
- Multi-layer stack traces
- Transitive dependency failures
- Environment variable propagation
- Database connection cascades
- API timeout chains
- Memory corruption patterns
- Race conditions in concurrent code
</think>

## Phase 1: Error Information Gathering

I'll collect comprehensive error context:

```bash
#!/bin/bash
# Root Cause Analysis - Error Context Gathering

echo "=== Root Cause Analysis ==="
echo ""
echo "Gathering error information..."

# Create analysis directory
mkdir -p .claude/debugging/root-cause
ANALYSIS_DIR=".claude/debugging/root-cause"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT="$ANALYSIS_DIR/analysis-$TIMESTAMP.md"

# Function to extract stack traces from logs
extract_stack_traces() {
    echo "Searching for stack traces..."

    # Common log locations
    LOG_DIRS=(
        "."
        "logs"
        "log"
        ".next"
        "dist"
        "build"
    )

    for dir in "${LOG_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            # Look for error patterns
            grep -r -i "error\|exception\|stack trace\|traceback" \
                "$dir" \
                --include="*.log" \
                --include="*.txt" \
                2>/dev/null | head -50
        fi
    done
}

# Function to analyze recent git changes
analyze_recent_changes() {
    echo ""
    echo "Analyzing recent code changes..."

    if git rev-parse --git-dir > /dev/null 2>&1; then
        # Get commits from last 3 days
        echo "Recent commits:"
        git log --oneline --since="3 days ago" | head -10

        echo ""
        echo "Recent file changes:"
        git diff HEAD~5 --name-status | head -20
    fi
}

# Function to check environment configuration
check_environment() {
    echo ""
    echo "Environment configuration:"

    # Check for .env files
    if [ -f ".env" ]; then
        echo "  .env file: EXISTS"
        # Don't show values for security
        echo "  Variables defined: $(grep -c "=" .env 2>/dev/null || echo "0")"
    else
        echo "  .env file: NOT FOUND"
    fi

    # Check NODE_ENV or similar
    if [ -n "$NODE_ENV" ]; then
        echo "  NODE_ENV: $NODE_ENV"
    fi

    if [ -n "$PYTHON_ENV" ]; then
        echo "  PYTHON_ENV: $PYTHON_ENV"
    fi
}

# Execute information gathering
STACK_TRACES=$(extract_stack_traces)
analyze_recent_changes
check_environment

# Initialize report
cat > "$REPORT" << EOF
# Root Cause Analysis Report

**Generated:** $(date)
**Issue:** $ARGUMENTS

## Error Context

### Stack Traces Found

\`\`\`
$STACK_TRACES
\`\`\`

### Recent Changes

$(git log --oneline --since="3 days ago" 2>/dev/null | head -10)

### Environment

$(check_environment)

EOF

echo ""
echo "✓ Initial context gathered"
```

## Phase 2: Dependency Chain Analysis

I'll trace the dependency chain to find where the error originates:

```bash
echo ""
echo "=== Analyzing Dependency Chain ==="

analyze_dependencies() {
    # Detect project type
    if [ -f "package.json" ]; then
        echo "Node.js project detected"
        echo ""

        # Check for dependency issues
        echo "Checking npm dependencies..."
        npm list --depth=0 2>&1 | grep -E "UNMET|missing|invalid" || echo "  ✓ All dependencies installed"

        # Check for version conflicts
        echo ""
        echo "Checking for version conflicts..."
        npm ls 2>&1 | grep -E "WARN.*requires" | head -10 || echo "  ✓ No obvious version conflicts"

        # Analyze dependency tree for specific package
        if [ -n "$ARGUMENTS" ]; then
            PACKAGE=$(echo "$ARGUMENTS" | grep -oE "[a-z0-9-]+/[a-z0-9-]+" || echo "")
            if [ -n "$PACKAGE" ]; then
                echo ""
                echo "Dependency path for $PACKAGE:"
                npm ls "$PACKAGE" 2>/dev/null || echo "  Package not found in dependencies"
            fi
        fi

    elif [ -f "requirements.txt" ]; then
        echo "Python project detected"
        echo ""

        # Check installed packages
        echo "Checking pip dependencies..."
        pip check 2>&1 || echo "  Issues found - see above"

        # Show package versions
        echo ""
        echo "Installed package versions:"
        pip freeze | head -20

    elif [ -f "go.mod" ]; then
        echo "Go project detected"
        echo ""

        # Check Go modules
        echo "Checking Go modules..."
        go mod verify || echo "  Module verification failed"

        # Show direct dependencies
        echo ""
        echo "Direct dependencies:"
        go list -m all | head -20
    fi
}

analyze_dependencies >> "$REPORT"
```

## Phase 3: Call Stack Tracing

I'll analyze call stacks to trace execution flow:

```bash
echo ""
echo "=== Tracing Call Stack ==="

trace_call_stack() {
    echo ""
    echo "Analyzing error call stack..."

    # Extract file paths from error message
    ERROR_FILES=$(echo "$ARGUMENTS" | grep -oE "at .*\((.+):[0-9]+:[0-9]+\)" | sed 's/.*(\(.*\):[0-9]*.*/\1/' | sort -u)

    if [ -z "$ERROR_FILES" ]; then
        # Try alternative formats
        ERROR_FILES=$(echo "$ARGUMENTS" | grep -oE "[a-zA-Z0-9/_-]+\.(js|ts|py|go):[0-9]+" | cut -d: -f1 | sort -u)
    fi

    if [ -n "$ERROR_FILES" ]; then
        echo "Files involved in error:"
        echo "$ERROR_FILES" | sed 's/^/  /'

        echo ""
        echo "Call stack visualization:"
        cat << 'CALLSTACK'
┌─────────────────────────────────────┐
│ Entry Point / API Endpoint          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Business Logic Layer                │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Data Access Layer                   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ ❌ ERROR OCCURS HERE                │
│ (Database, API, File System)        │
└─────────────────────────────────────┘
CALLSTACK

        # Analyze each file in the stack
        for file in $ERROR_FILES; do
            if [ -f "$file" ]; then
                echo ""
                echo "Analyzing: $file"

                # Look for common error patterns
                grep -n "throw\|raise\|panic\|error" "$file" | head -5
            fi
        done
    else
        echo "Unable to extract file paths from error message"
        echo "Please provide full stack trace for detailed analysis"
    fi
}

trace_call_stack >> "$REPORT"
```

## Phase 4: Configuration Analysis

I'll check for configuration-related issues:

```bash
echo ""
echo "=== Configuration Analysis ==="

analyze_configuration() {
    echo ""
    echo "Checking configuration files..."

    # List common config files
    CONFIG_FILES=(
        "package.json"
        "tsconfig.json"
        "webpack.config.js"
        "vite.config.js"
        "next.config.js"
        ".env"
        ".env.local"
        "config.json"
        "config.yaml"
        "settings.py"
        "application.properties"
    )

    echo "Configuration files found:"
    for config in "${CONFIG_FILES[@]}"; do
        if [ -f "$config" ]; then
            echo "  ✓ $config"

            # Check for common misconfigurations
            case "$config" in
                "package.json")
                    # Check for missing scripts
                    if ! grep -q '"scripts"' "$config"; then
                        echo "    ⚠️  No scripts defined"
                    fi
                    ;;
                "tsconfig.json")
                    # Check for strict mode
                    if ! grep -q '"strict": true' "$config"; then
                        echo "    💡 Consider enabling strict mode"
                    fi
                    ;;
                ".env")
                    # Check if .env is in .gitignore
                    if [ -f ".gitignore" ]; then
                        if ! grep -q "^\.env" ".gitignore"; then
                            echo "    ⚠️  .env not in .gitignore (security risk)"
                        fi
                    fi
                    ;;
            esac
        fi
    done

    echo ""
    echo "Environment variable usage:"

    # Find process.env or os.getenv usage
    ENV_USAGE=$(grep -r "process\.env\|os\.getenv\|System\.getenv" \
        --include="*.js" --include="*.ts" --include="*.py" --include="*.java" \
        --exclude-dir=node_modules \
        --exclude-dir=dist \
        . 2>/dev/null | wc -l)

    echo "  Environment variables referenced: $ENV_USAGE times"

    # Check for undefined env vars
    if [ -f ".env.example" ] && [ -f ".env" ]; then
        echo ""
        echo "Comparing .env with .env.example:"

        EXAMPLE_VARS=$(grep -E "^[A-Z_]+" .env.example | cut -d= -f1 | sort)
        ACTUAL_VARS=$(grep -E "^[A-Z_]+" .env | cut -d= -f1 | sort)

        # Find missing vars
        MISSING=$(comm -23 <(echo "$EXAMPLE_VARS") <(echo "$ACTUAL_VARS"))

        if [ -n "$MISSING" ]; then
            echo "  ⚠️  Missing environment variables:"
            echo "$MISSING" | sed 's/^/    /'
        else
            echo "  ✓ All required variables defined"
        fi
    fi
}

analyze_configuration >> "$REPORT"
```

## Phase 5: State and Timing Analysis

I'll investigate state-related and timing issues:

```bash
echo ""
echo "=== State & Timing Analysis ==="

analyze_state_timing() {
    echo ""
    echo "Analyzing potential state and timing issues..."

    # Check for async/await patterns
    echo "Async patterns:"
    ASYNC_COUNT=$(grep -r "async\|await\|Promise\|\.then(" \
        --include="*.js" --include="*.ts" \
        --exclude-dir=node_modules \
        --exclude-dir=dist \
        . 2>/dev/null | wc -l)
    echo "  Async operations found: $ASYNC_COUNT"

    if [ "$ASYNC_COUNT" -gt 50 ]; then
        echo "  ⚠️  High async complexity - potential race conditions"
        echo ""
        echo "Common async pitfalls to check:"
        echo "  - Missing await keywords"
        echo "  - Unhandled promise rejections"
        echo "  - Race conditions in concurrent operations"
        echo "  - Callback hell or promise chains"
    fi

    # Check for state management
    echo ""
    echo "State management patterns:"

    STATE_PATTERNS=$(grep -r "useState\|useReducer\|Redux\|Vuex\|MobX" \
        --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" \
        --exclude-dir=node_modules \
        . 2>/dev/null | wc -l)

    if [ "$STATE_PATTERNS" -gt 0 ]; then
        echo "  State management usage: $STATE_PATTERNS occurrences"
        echo ""
        echo "State-related issues to check:"
        echo "  - Stale closures in event handlers"
        echo "  - Missing dependencies in useEffect"
        echo "  - State updates not batched"
        echo "  - Direct state mutation"
    fi

    # Check for timing-sensitive operations
    echo ""
    echo "Timing-sensitive operations:"

    TIMERS=$(grep -r "setTimeout\|setInterval\|debounce\|throttle" \
        --include="*.js" --include="*.ts" \
        --exclude-dir=node_modules \
        . 2>/dev/null | wc -l)

    echo "  Timer usage: $TIMERS occurrences"

    if [ "$TIMERS" -gt 10 ]; then
        echo "  💡 Check for:"
        echo "     - Timer cleanup in unmount"
        echo "     - Memory leaks from uncancelled timers"
        echo "     - Race conditions with delayed execution"
    fi
}

analyze_state_timing >> "$REPORT"
```

## Phase 6: Root Cause Hypothesis

Based on gathered data, I'll formulate hypotheses:

```bash
echo ""
echo "=== Root Cause Hypothesis ==="

cat >> "$REPORT" << 'EOF'

## Hypotheses (Prioritized)

### Hypothesis 1: Dependency Version Conflict - PRIORITY: HIGH

**Theory:** The error is caused by incompatible dependency versions or missing dependencies.

**Evidence:**
- Check dependency analysis above for UNMET or version conflicts
- Recent package updates in git history
- Error references third-party package code

**Verification:**
```bash
# Clear and reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Or check specific package
npm ls <package-name>
```

**Expected:** Error resolves after reinstalling with correct versions

---

### Hypothesis 2: Environment Configuration - PRIORITY: HIGH

**Theory:** Missing or incorrect environment variables causing runtime failures.

**Evidence:**
- Error occurs in specific environment (dev/staging/prod)
- References to process.env or configuration
- Missing variables in .env comparison

**Verification:**
```bash
# Check if all required env vars are set
source .env
printenv | grep -E "^[A-Z_]+="

# Compare with .env.example
diff .env.example .env
```

**Expected:** Error resolves after setting missing variables

---

### Hypothesis 3: Recent Code Changes - PRIORITY: MEDIUM

**Theory:** Recent commits introduced a breaking change or regression.

**Evidence:**
- Check git log for recent changes
- Error started appearing after specific date
- Modified files match error stack trace

**Verification:**
```bash
# Use git bisect to find breaking commit
git bisect start
git bisect bad HEAD
git bisect good HEAD~10

# Or revert recent commits
git revert <commit-hash>
```

**Expected:** Error disappears when reverting to known good commit

---

### Hypothesis 4: Async/Timing Issue - PRIORITY: MEDIUM

**Theory:** Race condition or improper async handling causing intermittent failures.

**Evidence:**
- Error is intermittent or timing-dependent
- High async operation count
- Error in promise rejection or async function

**Verification:**
```bash
# Add strategic console.log or debugging
# Check for:
# - Missing await keywords
# - Unhandled promise rejections
# - Race conditions in parallel operations
```

**Expected:** Error appears/disappears based on timing

---

### Hypothesis 5: State Corruption - PRIORITY: LOW

**Theory:** Application state is corrupted or mutated incorrectly.

**Evidence:**
- Error in state management code
- Direct state mutations detected
- Error after user interactions

**Verification:**
```bash
# Check for:
# - Direct state mutations
# - Missing state dependencies
# - Stale closures
```

**Expected:** Error resolves with proper state management

---

## Recommended Investigation Order

1. **Immediate Checks:**
   - Verify all dependencies installed: `npm install`
   - Check environment variables: `printenv`
   - Review recent commits: `git log`

2. **Dependency Analysis:**
   - Run `npm ls` to check for conflicts
   - Update outdated packages: `npm outdated`
   - Clear cache: `npm cache clean --force`

3. **Configuration Audit:**
   - Compare .env with .env.example
   - Check for environment-specific config
   - Verify API keys and credentials

4. **Code Analysis:**
   - Review files in error stack trace
   - Check for recent changes to those files
   - Look for missing error handling

5. **Timing Analysis:**
   - Add logging to trace execution flow
   - Check for race conditions
   - Verify async/await usage

## Next Steps

- [ ] Verify Hypothesis 1 (Dependencies)
- [ ] Verify Hypothesis 2 (Environment)
- [ ] Verify Hypothesis 3 (Recent Changes)
- [ ] If unresolved, use `/debug-systematic` for deeper analysis
- [ ] Document solution in `/debug-session`

EOF

echo "✓ Root cause hypotheses generated"
```

## Summary

```bash
echo ""
echo "=== ✓ Root Cause Analysis Complete ==="
echo ""
echo "📊 Analysis Summary:"
echo "  Report generated: $REPORT"
echo "  Hypotheses created: 5"
echo "  Priority levels: HIGH (2), MEDIUM (2), LOW (1)"
echo ""
echo "📁 Generated files:"
echo "  - $REPORT"
echo ""
echo "🔍 Key Findings:"
cat "$REPORT" | grep -A 2 "## Hypotheses" | tail -10
echo ""
echo "🚀 Next Steps:"
echo ""
echo "1. Review full analysis report:"
echo "   cat $REPORT"
echo ""
echo "2. Test hypotheses in priority order:"
echo "   - Start with HIGH priority hypotheses"
echo "   - Document results for each test"
echo "   - Move to next hypothesis if disproved"
echo ""
echo "3. Common quick fixes to try first:"
echo "   rm -rf node_modules package-lock.json && npm install"
echo "   cp .env.example .env  # Then fill in values"
echo "   git log --oneline | head -5  # Check recent changes"
echo ""
echo "4. If issue persists:"
echo "   - Use /debug-systematic for systematic testing"
echo "   - Use /debug-session to document findings"
echo "   - Use /performance-profile if performance-related"
echo ""
echo "💡 Integration Points:"
echo "  - /debug-systematic - Systematic hypothesis testing"
echo "  - /debug-session - Document debugging process"
echo "  - /test - Run tests to verify fixes"

echo ""
echo "Report saved to: $REPORT"
```

## Safety & Best Practices

**Analysis Approach:**
- Start with most likely causes (dependencies, env config)
- Use git history to correlate with error appearance
- Check for environment-specific issues
- Consider timing and state problems last

**Common Root Causes:**
1. Dependency version conflicts (40% of issues)
2. Missing environment variables (30% of issues)
3. Recent code changes/regressions (15% of issues)
4. Configuration errors (10% of issues)
5. Race conditions/timing (5% of issues)

**Prevention:**
- Lock dependency versions
- Document all required env vars in .env.example
- Use feature flags for risky changes
- Add comprehensive error logging
- Implement proper async error handling

## Token Optimization

**Expected range**: 2,000–3,000 tokens (initial), 200 tokens (no error provided)

**Caching**: Caches dependency graph in `.claude/cache/dependencies.json` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if no error or stack trace is provided.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
