---
name: skill-validator
description: Internal skill that validates a new or modified AI DevStudio skill against project standards. Checks YAML frontmatter, token optimization section, line limit, and naming conventions. Used by the code-reviewer agent during PR review.
user-invocable: false
disable-model-invocation: false
---

# Skill Validator Skill

Internal skill used by the `code-reviewer` agent when reviewing skill contributions. Validates a skill file against AI DevStudio standards.

## Usage

Called with the path to a skill file to validate. Context will contain the file path.

## Validation Checks

### 1. File Location

Verify the skill is in the correct location:

```
skills/<skill-name>/SKILL.md
```

Reject if in wrong directory or wrong filename.

### 2. YAML Frontmatter

Read the skill file and check:

- `name` field present and matches directory name (kebab-case)
- `description` field present and non-empty (>10 characters)
- `disable-model-invocation` field present and is a boolean
- No unknown frontmatter fields (warn on unrecognized keys)

### 3. Line Count

```bash
Bash: wc -l < skills/<name>/SKILL.md
```

Warn if over 100 lines of instruction content (excluding frontmatter, code blocks, Token Optimization section).

Estimate instruction lines:
- Total lines minus frontmatter (lines between `---`)
- Minus code block lines (between ``` markers)
- Minus Token Optimization section

### 4. Token Optimization Section

Check that the file contains a `## Token Optimization` section:

```bash
Bash: grep -n "## Token Optimization" skills/<name>/SKILL.md
```

Fail if missing. The section must include expected token range.

### 5. Naming Conventions

- Directory name: kebab-case only
- No underscores, no camelCase
- Name matches `name` field in frontmatter

### 6. No Hardcoded Paths

```bash
Bash: grep -n "/Users/\|/home/[a-z]\|C:\\Users" skills/<name>/SKILL.md
```

Fail if any absolute user-specific paths found.

## Output Format

```
Skill Validation: skills/<name>/SKILL.md

PASS / FAIL / WARNINGS

Checks:
  [PASS] File location
  [PASS] YAML frontmatter
  [WARN] Line count: 112 lines (limit: 100 instruction lines)
  [PASS] Token Optimization section present
  [PASS] Naming conventions
  [PASS] No hardcoded paths

Summary: Ready to merge / Needs fixes
```

## Token Optimization

**Expected range**: 150-400 tokens

**Patterns used**: Bash grep for specific checks, early exit on critical failures
