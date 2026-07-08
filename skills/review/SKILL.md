---
name: review
description: Multi-agent code analysis covering security, performance, quality, and architecture
disable-model-invocation: false
---

# Code Review

I'll review your code for potential issues.


```bash
# Check for focus area flags (saves 75% by running only requested sub-agents)
FOCUS_SECURITY=false
FOCUS_PERFORMANCE=false
FOCUS_QUALITY=false
FOCUS_ARCHITECTURE=false
FULL_REVIEW=false

# Parse arguments (e.g., --security, --full)
for arg in "$@"; do
    case $arg in
        --security) FOCUS_SECURITY=true ;;
        --performance) FOCUS_PERFORMANCE=true ;;
        --quality) FOCUS_QUALITY=true ;;
        --architecture) FOCUS_ARCHITECTURE=true ;;
        --full) FULL_REVIEW=true ;;
    esac
done

# Default to changed files only (90% token savings)
if [ "$FULL_REVIEW" = false ]; then
    FILES_TO_REVIEW=$(git diff --name-only HEAD)
    if [ -z "$FILES_TO_REVIEW" ]; then
        echo "✓ No changed files to review"
        exit 0  # Early exit, saves 95% tokens
    fi
    echo "Reviewing changed files: $(echo "$FILES_TO_REVIEW" | wc -l) files"
else
    echo "Reviewing entire codebase (--full flag)"
fi
```

**Optimization: Check Cached Review Results**

```bash
# Check cache for unchanged files (70% savings on re-reviews)
CACHE_FILE=".claude/cache/review/last-review.json"
if [ -f "$CACHE_FILE" ] && [ "$FULL_REVIEW" = false ]; then
    # Compare file checksums to detect changes
    CHANGED=$(echo "$FILES_TO_REVIEW" | while read file; do
        if [ -f "$file" ]; then
            CURRENT_CHECKSUM=$(md5sum "$file" 2>/dev/null | cut -d' ' -f1)
            CACHED_CHECKSUM=$(jq -r ".files.\"$file\".checksum" "$CACHE_FILE" 2>/dev/null)
            if [ "$CURRENT_CHECKSUM" != "$CACHED_CHECKSUM" ]; then
                echo "$file"
            fi
        fi
    done)

    if [ -z "$CHANGED" ]; then
        echo "✓ No file changes since last review"
        jq '.issues' "$CACHE_FILE"
        exit 0
    fi
fi
```

Let me create a checkpoint before detailed analysis:
```bash
git add -A
git commit -m "Pre-review checkpoint" || echo "No changes to commit"
```

I'll use specialized sub-agents for comprehensive analysis (optimized with focus areas):

**Sub-Agent Selection (saves 75% by running only what's needed):**
```bash
# Default: Run all agents on changed files only
# With flags: Run specific agents only

if [ "$FOCUS_SECURITY" = true ] || [ "$FULL_REVIEW" = true ]; then
    # Security sub-agent: Credential exposure, input validation, vulnerabilities
    echo "Running security analysis..."
fi

if [ "$FOCUS_PERFORMANCE" = true ] || [ "$FULL_REVIEW" = true ]; then
    # Performance sub-agent: Bottlenecks, memory issues, optimization
    echo "Running performance analysis..."
fi

if [ "$FOCUS_QUALITY" = true ] || [ "$FULL_REVIEW" = true ]; then
    # Quality sub-agent: Code complexity, maintainability, best practices
    echo "Running quality analysis..."
fi

if [ "$FOCUS_ARCHITECTURE" = true ] || [ "$FULL_REVIEW" = true ]; then
    # Architecture sub-agent: Layer separation, dependency direction, patterns
    echo "Running architecture analysis..."
fi
```

**Optimization: Grep-Before-Read Pattern (saves 85% in sub-agents)**

Each sub-agent will use Grep to identify problematic patterns before reading full files:

```bash
# Security Agent: Grep for security patterns first (100 tokens vs 5,000+)
SECURITY_ISSUES=$(Grep pattern="password|secret|api[_-]?key|token" files="$FILES_TO_REVIEW" head_limit=20)

# Performance Agent: Grep for performance anti-patterns
PERF_ISSUES=$(Grep pattern="for.*for|O\(n\^2\)|sleep|setTimeout.*loop" files="$FILES_TO_REVIEW" head_limit=20)

# Only read files that matched patterns (saves 85% tokens)
```

I'll examine files using optimized Grep-then-Read analysis:
1. **Security Issues** - credential exposure, input validation (Grep patterns)
2. **Logic Problems** - error handling, edge cases (Grep patterns)
3. **Performance Concerns** - inefficient patterns, bottlenecks (Grep patterns)
4. **Code Quality** - complexity, maintainability (Grep patterns)

When I find multiple issues, I'll create a todo list to address them systematically.

For each issue, I'll use **progressive disclosure** (saves 60% tokens):

**Critical Issues (show full details):**
- Show exact location with file references
- Explain the problem and potential impact
- Provide specific remediation steps

**High Priority (summarize):**
- List issue type and file location
- Brief impact description

**Medium/Low Priority (count only):**
- "Found 5 medium and 3 low priority issues"
- "Run with --verbose for full details"

**Save Review Results to Cache (70% savings on re-reviews)**

```bash
# Cache review results with file checksums
mkdir -p .claude/cache/review
cat > .claude/cache/review/last-review.json <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "files": {
    $(echo "$FILES_TO_REVIEW" | while read file; do
      CHECKSUM=$(md5sum "$file" 2>/dev/null | cut -d' ' -f1)
      echo "\"$file\": {\"checksum\": \"$CHECKSUM\"}"
    done | paste -sd,)
  },
  "issues": {
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0
  }
}
EOF
```

After review, I'll ask: "Create GitHub issues for critical findings?"
- Yes: I'll create prioritized issues with detailed descriptions
- Todos only: I'll maintain local tracking for resolution
- Summary: I'll provide actionable report (with progressive disclosure)

**Important**: I will NEVER:
- Add "Co-authored-by" or any Claude signatures to commits
- Add "Created by Claude" or any AI attribution to issues
- Include "Generated with Claude Code" in any output
- Modify git config or repository settings
- Add any AI/assistant signatures or watermarks
- Use emojis in commits, PRs, issues, or git-related content

This focuses on real problems that impact your application's reliability and maintainability.

## Token Optimization

**Expected range**: 2,000–8,000 tokens (initial), 100 tokens (no issues)

**Caching**: Caches last review results in `.claude/cache/review/last-review.json` for 7 days. Invalidated on new commits.

**Early exit**: Returns immediately if no staged changes are detected.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching, progressive disclosure
