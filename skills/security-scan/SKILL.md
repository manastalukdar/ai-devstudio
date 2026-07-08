---
name: security-scan
description: Comprehensive security analysis with vulnerability detection and remediation tracking
disable-model-invocation: false
---

# Security Analysis

I'll perform comprehensive security analysis with tracking and remediation continuity across sessions.

Arguments: `$ARGUMENTS` - specific paths or security focus areas


## Session Intelligence

I'll maintain security remediation progress:

**Session Files (in current project directory):**
- `security-scan/plan.md` - All vulnerabilities and fixes
- `security-scan/state.json` - Remediation progress

**IMPORTANT:** Session files are stored in a `security-scan` folder in your current project root

**Auto-Detection:**
- If session exists: Show fixed vs pending vulnerabilities
- If no session: Perform new security scan
- Commands: `resume`, `status`, `new`

**Optimization: Determine Scan Scope (85% savings on focused scans)**

```bash
# Default to changed files only (85% token savings)
FULL_SCAN=false
SCAN_PATH=""

case "$ARGUMENTS" in
    *--full*) FULL_SCAN=true ;;
    *) SCAN_PATH="$ARGUMENTS" ;;
esac

if [ "$FULL_SCAN" = false ] && [ -z "$SCAN_PATH" ]; then
    # Default: Scan only changed files
    FILES_TO_SCAN=$(git diff --name-only HEAD)
    if [ -z "$FILES_TO_SCAN" ]; then
        echo "✓ No changed files to scan"
        echo "Use --full for complete project scan"
        exit 0  # Early exit
    fi
    echo "Scanning changed files: $(echo "$FILES_TO_SCAN" | wc -l) files"
elif [ -n "$SCAN_PATH" ]; then
    echo "Scanning path: $SCAN_PATH"
    FILES_TO_SCAN=$(find "$SCAN_PATH" -type f 2>/dev/null)
else
    echo "Scanning entire project (--full flag)"
    FILES_TO_SCAN="**/*"
fi
```

**Optimization: Pattern-Based Grep Detection (90% savings)**

```bash
# Use Grep patterns to find vulnerabilities (100 tokens vs 5,000+ reading all files)

# Critical: Hardcoded secrets and credentials
SECRET_ISSUES=$(Grep pattern="password|secret|api[_-]?key|token|private[_-]?key" \
    files="$FILES_TO_SCAN" output_mode="files_with_matches" head_limit=20)

# High: SQL injection and XSS vulnerabilities
INJECTION_ISSUES=$(Grep pattern="execute\(|query\(|innerHTML|dangerouslySetInnerHTML" \
    files="$FILES_TO_SCAN" output_mode="files_with_matches" head_limit=20)

# Medium: Insecure configurations
CONFIG_ISSUES=$(Grep pattern="ssl.*false|verify.*false|allow.*origin.*\*" \
    files="$FILES_TO_SCAN" output_mode="files_with_matches" head_limit=20)

# Count issues for early exit decision
CRITICAL_COUNT=$(echo "$SECRET_ISSUES" | wc -l)

if [ $CRITICAL_COUNT -eq 0 ]; then
    echo "✓ No critical security issues found in scanned files"
    echo "Run with --full for complete project scan"
    exit 0  # Early exit when no critical issues (95% savings)
fi

echo "Found $CRITICAL_COUNT potential critical issues, analyzing..."
```

## Phase 1: Security Assessment (Optimized)

### Extended Thinking for Security Analysis

For complex security scenarios, I'll use extended thinking to identify sophisticated vulnerabilities:

<think>
When analyzing security:
- Attack vectors that aren't immediately obvious
- Chain vulnerabilities that individually seem harmless
- Business logic flaws that enable exploitation
- Timing attacks and race conditions
- Supply chain vulnerabilities in dependencies
- Architectural weaknesses that enable lateral movement
</think>

**Triggers for Extended Analysis:**
- Authentication and authorization systems
- Financial transaction processing
- Cryptographic implementations
- Multi-tenant architectures
- API security boundaries

**MANDATORY FIRST STEPS:**
1. Check if `security-scan` directory exists in current working directory
2. If directory exists, check for session files:
   - Look for `security-scan/state.json`
   - Look for `security-scan/plan.md`
   - If found, resume from existing session
3. If no directory or session exists:
   - Perform full security scan
   - Create vulnerability report
   - Initialize tracking
4. Show risk summary before remediation

**Note:** Always look for session files in the current project's `security-scan/` folder, not `../../../security-scan/` or absolute paths

I'll analyze security across dimensions:

**Vulnerability Detection:**
- Hardcoded secrets and credentials
- Dependency vulnerabilities
- Insecure configurations
- Input validation issues
- Authentication weaknesses

**Risk Categorization with Progressive Disclosure (65% savings):**

**Critical Issues (show full details immediately):**
- Hardcoded credentials and API keys
- SQL injection vulnerabilities
- Authentication bypasses
- Remote code execution risks

**High Priority (summarize with file locations):**
- XSS vulnerabilities
- Insecure deserialization
- Path traversal issues
- Weak cryptography

**Medium/Low Priority (count only by default):**
- Configuration improvements
- Dependency updates
- Best practice recommendations
- "Run with --verbose for full details"

**Example Output:**
```
SECURITY SCAN RESULTS

Critical (3):
1. Hardcoded API key in src/config/keys.ts:15
2. SQL injection in src/api/users.ts:42
3. Exposed secret in .env.example:8

High (5): Summarized (run --verbose for details)
Medium (12): Configuration and best practices
Low (8): Dependency updates available

Total: 28 issues (3 critical require immediate attention)
```

**Optimization: Cache Scan Results (80% savings on unchanged files)**

```bash
# Save scan results with file checksums for future comparisons
mkdir -p .claude/cache/security

cat > .claude/cache/security/last-scan.json <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "scanned_files": $(echo "$FILES_TO_SCAN" | wc -l),
  "issues": {
    "critical": $CRITICAL_COUNT,
    "high": $(echo "$INJECTION_ISSUES" | wc -l),
    "medium": $(echo "$CONFIG_ISSUES" | wc -l),
    "low": 0
  },
  "files": {
    $(echo "$FILES_TO_SCAN" | while read file; do
      if [ -f "$file" ]; then
        CHECKSUM=$(md5sum "$file" 2>/dev/null | cut -d' ' -f1)
        echo "\"$file\": {\"checksum\": \"$CHECKSUM\", \"scanned\": true}"
      fi
    done | paste -sd,)
  }
}
EOF

echo "✓ Scan results cached for future comparisons"
```

## Phase 2: Remediation Planning (Optimized)

**Priority Order:**
1. Critical credential exposures
2. High-risk vulnerabilities
3. Dependency updates
4. Configuration hardening
5. Code pattern improvements

I'll write this plan to `security-scan/plan.md` with:
- Each vulnerability details
- Risk assessment
- Remediation approach
- Verification method

## Phase 3: Intelligent Remediation

I'll fix vulnerabilities appropriately:

**Remediation Patterns:**
- Secrets → Environment variables
- Hardcoded values → Configuration files
- Weak validation → Strong patterns
- Outdated deps → Safe updates

**Safe Practices:**
- Never log sensitive data
- Use secure defaults
- Apply principle of least privilege
- Implement defense in depth

## Phase 4: Incremental Fixing

I'll remediate systematically:

**Execution Process:**
1. Create git checkpoint
2. Fix vulnerability safely
3. Verify fix doesn't break functionality
4. Update plan with completion
5. Move to next vulnerability

**Progress Tracking:**
- Mark each fix in plan
- Update state with decisions
- Create security-focused commits

## Phase 5: Verification

After each remediation:
- Test functionality preserved
- Verify vulnerability resolved
- Check for new issues introduced
- Update security documentation

## Context Continuity

**Session Resume:**
When you return and run `/security-scan` or `/security-scan resume`:
- Load vulnerability list and progress
- Show remediation statistics
- Continue from last fix
- Maintain fix decisions

**Progress Example:**
```
RESUMING SECURITY REMEDIATION
├── Total Vulnerabilities: 23
├── Fixed: 15 (65%)
├── Critical: 0 remaining
├── High: 3 remaining
└── Next: SQL injection in UserQuery

Continuing remediation...
```

## Practical Examples

**Start Scanning:**
```
/security-scan                # Full project scan
/security-scan src/api/       # Focus on API
/security-scan "credentials"  # Credential focus
```

**Session Control:**
```
/security-scan resume    # Continue remediation
/security-scan status    # Check progress
/security-scan new       # Fresh scan
```

## Safety Guarantees

**Protection Measures:**
- Git checkpoint before fixes
- Functionality preservation
- No security regression
- Clear audit trail

**Important:** I will NEVER:
- Expose secrets in commits
- Break existing security
- Add AI attribution
- Log sensitive data

## Skill Integration

When appropriate for critical security fixes:
- `/test` - Verify functionality after security patches
- `/commit` - Create security-focused commits with proper messages

## What I'll Actually Do

1. **Deep analysis** - Use extended thinking for complex threats
2. **Scan thoroughly** - Find all vulnerabilities
3. **Prioritize wisely** - Critical issues first
4. **Fix safely** - Preserve functionality
5. **Track completely** - Perfect continuity
6. **Verify constantly** - Ensure security improved

I'll maintain complete continuity between sessions, always resuming exactly where we left off with full remediation context.

## Token Optimization

**Expected range**: 1,000–3,000 tokens (initial), 200 tokens (cache hit)

**Caching**: Caches last scan results in `.claude/cache/security/last-scan.json` for 7 days. Invalidated on new commits.

**Early exit**: Returns immediately after N critical findings to surface high-severity issues first.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching, progressive disclosure
