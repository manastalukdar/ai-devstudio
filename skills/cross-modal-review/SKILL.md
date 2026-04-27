---
name: cross-modal-review
description: Run a second-model quality gate on staged changes, a skill draft, or any generated output. A cheaper, independent model reviews the primary output for correctness, safety, and completeness before the user sees the final result.
disable-model-invocation: false
---

# Cross-Modal Review

I act as a second, independent reviewer — catching errors, blind spots, and assumptions the primary pass missed. Inspired by gbrain's cross-modal quality gate pattern.

## Token Optimization

**Expected range**: 400–1,500 tokens (second-pass review), 50 tokens (trivial change, skip)

**Patterns used**: Git diff scope default (staged only), early exit (no reviewable content), progressive disclosure (verdict first → issues → details)

**Early exit**: If the target is a single-line change or a comment-only edit, report "Trivial change — cross-modal review skipped" and stop.

## When to Use

Invoke after:
- `/review` — to get a second opinion on the primary review output
- Generating a new skill draft — to validate it passes conformance before writing
- Writing complex business logic — to catch logic errors the primary pass may rationalize
- Security-sensitive changes — to add a second set of eyes before commit

Can also be invoked directly: `/cross-modal-review` with staged changes as the default target.

## Step 1 — Identify Target

```bash
# Default: staged changes
git diff --cached --stat
git diff --cached --name-only

# If no staged changes, check for an argument (file path or prior output)
[[ -z "$ARGUMENTS" ]] && git diff --cached --quiet && echo "Nothing to review" && exit 0
```

## Step 2 — Frame the Second-Pass Review

Review the target with deliberate adversarial framing — assume the primary pass was optimistic. Check specifically:

**Correctness**
- Does the logic match the stated intent?
- Are there off-by-one errors, missed null checks, or incorrect assumptions?
- Do variable names match what they actually contain?

**Completeness**
- Are edge cases handled?
- Are error paths covered?
- Does the change handle the empty/zero/nil case?

**Safety**
- Are there command injection, path traversal, or injection vulnerabilities?
- Are credentials, tokens, or PII handled correctly?
- Are destructive operations guarded?

**Consistency**
- Does the change follow the patterns in the surrounding code?
- Are naming conventions consistent?
- Are existing tests updated to cover the change?

**Skill-Specific (when reviewing a SKILL.md)**
- Does the frontmatter have all required fields?
- Is the Token Optimization section present with concrete estimates?
- Does the description trigger correctly?
- Are there early exit conditions?
- Is it under 100 lines of instructions?

## Step 3 — Report

```
Cross-modal review — <target>

Verdict: PASS / PASS WITH NOTES / FAIL

Issues found:
  [CRITICAL] <issue> — <location>
  [WARN]     <issue> — <location>
  [NOTE]     <issue> — <location>

Passed:
  ✓ Logic matches intent
  ✓ No injection vulnerabilities
  ...

Recommendation: <one sentence>
```

**Verdict definitions:**
- `PASS` — No issues; safe to proceed
- `PASS WITH NOTES` — Minor issues that don't block; worth fixing before merge
- `FAIL` — One or more CRITICAL issues; do not proceed until resolved

## Step 4 — On FAIL

List each CRITICAL issue with:
- Where it is (file:line or section name)
- Why it is critical
- The minimal fix

Do not apply fixes automatically — this is a review, not a fixer. The user decides whether to fix and re-run.

## Edge Cases

- **Reviewing a review**: If the input is the output of `/review`, compare both reviews and flag any disagreements between them as areas needing human judgment
- **Large diff (50+ files)**: Focus on the highest-risk files (auth, deploy, schema changes) and sample the rest; note what was sampled
- **No prior review**: Runs as a standalone first-pass review if no prior review output is available
