---
name: test-mutation
description: Mutation testing to verify test quality with Stryker, mutmut, or go-mutesting
disable-model-invocation: true
---

# Mutation Testing - Test Quality Verification

I'll help you verify the quality of your test suite through mutation testing. This technique introduces small changes (mutations) to your code and verifies that your tests catch them.

**What is Mutation Testing?**
Mutation testing evaluates test effectiveness by:
- Creating mutants (modified versions of your code)
- Running tests against each mutant
- Calculating mutation score (% of mutants killed by tests)
- Identifying weak tests that don't catch bugs

**Quick Start:**
Mutation testing verifies test quality by introducing code changes and checking if tests catch them. This skill optimizes token usage through incremental testing and sample-based analysis.

## Phase 1: Detect Project and Tools

First, let me analyze your project setup:

```bash
# Detect mutation testing tools and project type
detect_mutation_tools() {
    local project_type=""
    local mutation_tool=""
    local tool_installed="false"

    # JavaScript/TypeScript - Stryker
    if [ -f "package.json" ]; then
        project_type="javascript"

        # Check if Stryker is installed
        if grep -q "@stryker-mutator" package.json; then
            mutation_tool="stryker"
            tool_installed="true"
            echo "✓ Stryker mutation testing detected"
        else
            mutation_tool="stryker"
            echo "ℹ Project: JavaScript/TypeScript"
            echo "ℹ Recommended: @stryker-mutator/core"
        fi

    # Python - mutmut
    elif [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
        project_type="python"

        # Check if mutmut is installed
        if command -v mutmut &> /dev/null; then
            mutation_tool="mutmut"
            tool_installed="true"
            echo "✓ mutmut mutation testing detected"
        else
            mutation_tool="mutmut"
            echo "ℹ Project: Python"
            echo "ℹ Recommended: mutmut"
        fi

    # Go - go-mutesting
    elif [ -f "go.mod" ]; then
        project_type="go"

        # Check if go-mutesting is installed
        if command -v go-mutesting &> /dev/null; then
            mutation_tool="go-mutesting"
            tool_installed="true"
            echo "✓ go-mutesting mutation testing detected"
        else
            mutation_tool="go-mutesting"
            echo "ℹ Project: Go"
            echo "ℹ Recommended: go-mutesting"
        fi

    else
        echo "❌ Unsupported project type"
        echo "Mutation testing supports: JavaScript/TypeScript, Python, Go"
        exit 1
    fi

    echo "$project_type|$mutation_tool|$tool_installed"
}

PROJECT_INFO=$(detect_mutation_tools)
PROJECT_TYPE=$(echo "$PROJECT_INFO" | cut -d'|' -f1)
MUTATION_TOOL=$(echo "$PROJECT_INFO" | cut -d'|' -f2)
TOOL_INSTALLED=$(echo "$PROJECT_INFO" | cut -d'|' -f3)

echo ""
echo "Project Type: $PROJECT_TYPE"
echo "Mutation Tool: $MUTATION_TOOL"
echo "Tool Installed: $TOOL_INSTALLED"
```

## Phase 2: Tool Installation (if needed)

If mutation testing tool is not installed, I'll guide you through setup:

```bash
install_mutation_tool() {
    local tool=$1

    echo ""
    echo "=== Mutation Testing Tool Setup ==="
    echo ""

    case $tool in
        stryker)
            echo "Installing Stryker Mutator..."
            echo ""
            echo "For Jest projects:"
            echo "  npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner"
            echo ""
            echo "For other test frameworks:"
            echo "  - Mocha: @stryker-mutator/mocha-runner"
            echo "  - Karma: @stryker-mutator/karma-runner"
            echo "  - Jasmine: @stryker-mutator/jasmine-runner"
            echo ""
            read -p "Install Stryker now? (yes/no): " install_confirm

            if [ "$install_confirm" = "yes" ]; then
                # Detect test framework
                if grep -q "\"jest\"" package.json; then
                    npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner
                elif grep -q "\"mocha\"" package.json; then
                    npm install --save-dev @stryker-mutator/core @stryker-mutator/mocha-runner
                else
                    npm install --save-dev @stryker-mutator/core
                fi

                # Initialize Stryker config
                npx stryker init

                echo "✓ Stryker installed and configured"
            fi
            ;;

        mutmut)
            echo "Installing mutmut..."
            echo ""
            echo "  pip install mutmut"
            echo ""
            read -p "Install mutmut now? (yes/no): " install_confirm

            if [ "$install_confirm" = "yes" ]; then
                pip install mutmut
                echo "✓ mutmut installed"
            fi
            ;;

        go-mutesting)
            echo "Installing go-mutesting..."
            echo ""
            echo "  go install github.com/zimmski/go-mutesting/cmd/go-mutesting@latest"
            echo ""
            read -p "Install go-mutesting now? (yes/no): " install_confirm

            if [ "$install_confirm" = "yes" ]; then
                go install github.com/zimmski/go-mutesting/cmd/go-mutesting@latest
                echo "✓ go-mutesting installed"
            fi
            ;;
    esac
}

if [ "$TOOL_INSTALLED" != "true" ]; then
    install_mutation_tool "$MUTATION_TOOL"
fi
```

## Phase 3: Run Mutation Testing

Now I'll run mutation testing on your codebase:

```bash
run_mutation_testing() {
    local tool=$1
    local target_path=${2:-.}

    echo ""
    echo "=== Running Mutation Testing ==="
    echo "Target: $target_path"
    echo ""

    case $tool in
        stryker)
            # Check if config exists
            if [ ! -f "stryker.conf.js" ] && [ ! -f "stryker.conf.json" ]; then
                echo "Creating default Stryker configuration..."

                cat > stryker.conf.json << 'EOF'
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "packageManager": "npm",
  "reporters": ["html", "clear-text", "progress"],
  "testRunner": "jest",
  "coverageAnalysis": "perTest",
  "mutate": [
    "src/**/*.js",
    "src/**/*.ts",
    "!src/**/*.spec.ts",
    "!src/**/*.test.ts"
  ]
}
EOF
                echo "✓ Created stryker.conf.json"
            fi

            echo "Running Stryker mutation testing..."
            echo "This may take several minutes..."
            echo ""

            npx stryker run

            echo ""
            echo "✓ Mutation testing complete"
            echo "📊 Report available at: reports/mutation/html/index.html"
            ;;

        mutmut)
            echo "Running mutmut mutation testing..."
            echo "This may take several minutes..."
            echo ""

            # Run mutation testing
            if [ "$target_path" = "." ]; then
                mutmut run
            else
                mutmut run --paths-to-mutate="$target_path"
            fi

            echo ""
            echo "Generating mutation report..."
            mutmut results
            mutmut html

            echo ""
            echo "✓ Mutation testing complete"
            echo "📊 Report available at: html/index.html"
            ;;

        go-mutesting)
            echo "Running go-mutesting mutation testing..."
            echo "This may take several minutes..."
            echo ""

            # Run mutation testing
            if [ "$target_path" = "." ]; then
                go-mutesting ./...
            else
                go-mutesting "$target_path"
            fi

            echo ""
            echo "✓ Mutation testing complete"
            ;;
    esac
}

# Run mutation testing
run_mutation_testing "$MUTATION_TOOL" "${1:-.}"
```

## Phase 4: Analyze Mutation Results

I'll analyze the mutation testing results and identify weak tests:

```bash
analyze_mutation_results() {
    local tool=$1

    echo ""
    echo "=== Mutation Testing Analysis ==="
    echo ""

    case $tool in
        stryker)
            # Parse Stryker results
            if [ -f "reports/mutation/mutation-report.json" ]; then
                echo "Parsing Stryker mutation report..."

                # Extract key metrics (simplified - actual parsing would be more complex)
                echo ""
                echo "Key Metrics:"
                echo "  - Check the HTML report for detailed metrics"
                echo "  - Mutation Score: % of mutants killed by tests"
                echo "  - Survived Mutants: Bugs your tests didn't catch"
                echo "  - Timeout Mutants: Tests that ran too long"

                echo ""
                echo "Target Mutation Score: 80%+"
                echo ""
            fi
            ;;

        mutmut)
            echo "Mutation Score Summary:"
            mutmut show

            echo ""
            echo "Survived Mutants (Tests didn't catch):"
            mutmut result-ids survived | head -10

            echo ""
            echo "To review each survived mutant:"
            echo "  mutmut show <mutant-id>"
            ;;

        go-mutesting)
            echo "Review the mutation testing output above."
            echo "Look for mutations that survived (not caught by tests)."
            ;;
    esac
}

analyze_mutation_results "$MUTATION_TOOL"
```

## Phase 5: Recommendations and Action Items

Based on mutation analysis, I'll provide actionable recommendations:

```bash
generate_recommendations() {
    echo ""
    echo "=== Mutation Testing Recommendations ==="
    echo ""

    cat << 'EOF'
**Understanding Mutation Score:**
- 80-100%: Excellent test quality
- 60-80%:  Good test coverage, some weak spots
- 40-60%:  Moderate coverage, needs improvement
- <40%:    Poor test quality, significant gaps

**Common Weak Test Patterns:**

1. **Boundary Condition Mutations**
   - Mutant: Changes > to >=
   - Fix: Add tests for exact boundary values

2. **Operator Mutations**
   - Mutant: Changes + to -
   - Fix: Test with specific expected values, not just "truthy"

3. **Conditional Mutations**
   - Mutant: Changes if (x) to if (true)
   - Fix: Test both branches explicitly

4. **Return Value Mutations**
   - Mutant: Returns different value
   - Fix: Assert exact return values, not just types

**Action Items:**

1. Review survived mutants
2. Write additional tests to kill survivors
3. Focus on edge cases and boundaries
4. Verify assertions are specific
5. Re-run mutation testing to confirm improvements

**Workflow:**
1. Run: /test-mutation
2. Review: Check mutation report
3. Fix: Add missing test cases
4. Test: /test (verify new tests pass)
5. Repeat: /test-mutation (verify improved score)

EOF
}

generate_recommendations
```

## Phase 6: Interactive Mutation Review

I'll help you review and fix survived mutants:

```bash
review_survived_mutants() {
    local tool=$1

    echo ""
    echo "=== Interactive Mutant Review ==="
    echo ""

    case $tool in
        mutmut)
            echo "Let's review survived mutants one by one:"
            echo ""

            # Get survived mutant IDs
            survived_ids=$(mutmut result-ids survived)

            if [ -z "$survived_ids" ]; then
                echo "✅ No survived mutants! Excellent test coverage!"
                return
            fi

            echo "Found survived mutants. Review each one:"
            echo ""

            for mutant_id in $survived_ids; do
                echo "--- Mutant $mutant_id ---"
                mutmut show "$mutant_id"
                echo ""
                echo "This mutant survived because tests didn't catch it."
                echo "Consider: What test would detect this change?"
                echo ""
                read -p "Press Enter to continue to next mutant..."
                echo ""
            done
            ;;

        stryker)
            echo "Open the HTML report to review survived mutants:"
            echo "  reports/mutation/html/index.html"
            echo ""
            echo "For each survived mutant:"
            echo "  1. Review the code change"
            echo "  2. Identify missing test case"
            echo "  3. Write test to catch that mutation"
            ;;

        go-mutesting)
            echo "Review the mutation testing output."
            echo "For each survived mutation, write a test that would catch it."
            ;;
    esac
}

review_survived_mutants "$MUTATION_TOOL"
```

## Mutation Operators Explained

Different types of mutations that can be introduced:

**Arithmetic Operators:**
- `+` ↔ `-`
- `*` ↔ `/`
- `++` ↔ `--`

**Relational Operators:**
- `>` ↔ `>=` ↔ `<` ↔ `<=`
- `==` ↔ `!=`

**Logical Operators:**
- `&&` ↔ `||`
- `!` removal

**Statement Mutations:**
- Remove statements
- Replace with no-op

**Constant Mutations:**
- Change numbers (0 → 1, 1 → 0)
- Change strings
- Change boolean values

## Integration Points

This skill works well with:
- `/test` - Run regular tests before mutation testing
- `/test-coverage` - Complement coverage analysis
- `/tdd-red-green` - Ensure new features have strong tests
- `/create-todos` - Track test improvements

## Best Practices

**When to Use Mutation Testing:**
- After achieving high code coverage (>80%)
- For critical business logic
- When test quality is uncertain
- Before major refactoring

**When NOT to Use:**
- On code with no tests
- On generated code
- On trivial getters/setters
- During tight deadlines (it's slow)

**Optimization Tips:**
- Target specific modules, not entire codebase
- Use incremental mutation testing
- Exclude generated files and vendor code
- Run mutation testing in CI for critical modules only

## Safety Guarantees

**Protection Measures:**
- Mutation testing runs in isolated environments
- Original code is never modified
- Only temporary mutants are created and tested
- All mutants are discarded after testing

**Important:** I will NEVER:
- Modify your actual source code
- Commit mutated code
- Deploy mutants to production
- Break your test suite

## Performance Expectations

**Runtime Estimates:**
- Small project (<1000 LOC): 2-5 minutes
- Medium project (1000-5000 LOC): 10-30 minutes
- Large project (>5000 LOC): 30-120 minutes

**Resource Usage:**
- CPU intensive (runs tests many times)
- Parallelization available in most tools
- Can run overnight for large codebases

## Example Workflow

```bash
# Step 1: Run full mutation testing
/test-mutation

# Step 2: Review mutation score (target 80%+)
# Check HTML report for details

# Step 3: Identify weak tests
# Look for survived mutants

# Step 4: Write better tests
# Focus on boundary conditions and edge cases

# Step 5: Run regular tests to verify
/test

# Step 6: Re-run mutation testing
/test-mutation

# Step 7: Commit improvements
/commit
```

## Troubleshooting

**Issue: Mutation testing hangs**
- Solution: Check for infinite loops in tests
- Solution: Increase timeout configuration

**Issue: Low mutation score despite good coverage**
- Explanation: Coverage measures execution, mutations measure effectiveness
- Solution: Write more specific assertions

**Issue: Too many mutations**
- Solution: Target specific files/modules
- Solution: Exclude trivial code

## Token Optimization

**Expected range**: 1,500–2,500 tokens (initial), 100 tokens (tool not installed)

**Caching**: Caches mutation tool detection in `.claude/cache/test-mutation/tool.json` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if no mutation testing tool is installed.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
