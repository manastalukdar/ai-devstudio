# Contributing to AI DevStudio

Thanks for your interest in improving AI DevStudio! This development studio helps developers save 10-15 hours per week with professional automation.

## Branch Strategy

We keep it simple:

1. **`main`** - primary stable branch; all PRs merge here
2. **`running`** - author's daily driver; used as download source for testing
3. **`add/your-feature`** - any contribution (new skill, fix, docs)

### Workflow Example

```bash
git checkout -b add/new-skill
# make your changes
git push origin add/new-skill
# open PR to main
```

## How to Contribute

### 1. New Skills

We welcome skills that solve real developer problems. Good skills:

- Save at least 5 minutes of repetitive work
- Are language/framework agnostic when possible
- Use context analysis rather than rigid rules
- Follow the [official Claude Skills format](https://code.claude.com/docs/en/skills)

**To add a skill:**

1. Create directory `skills/yourskill/`
2. Create `skills/yourskill/SKILL.md` with proper YAML frontmatter:
   ```yaml
   ---
   name: yourskill
   description: Clear description of what it does and when to use it
   disable-model-invocation: false  # true for manual-only skills
   ---
   ```
3. Add skill instructions after frontmatter
4. Follow the existing skill structure
5. Test it solves a real problem
6. Submit a PR with a clear use case

### 2. Improving Existing Skills

Found a bug or have an enhancement? Great! Please:

- Describe the current vs desired behavior
- Include examples if relevant
- Keep changes focused and minimal
- Consider adding validation phases for complex skills
- Use extended thinking for sophisticated analysis scenarios
- Update YAML frontmatter if invocation control changes

### 3. Bug Reports

Open an issue with:

- What skill failed
- What you expected
- Error message (if any)
- Your OS and Claude Code version

## Development Setup

```bash
git clone https://github.com/manastalukdar/ai-devstudio
cd ai-devstudio
python install.py  # Test your changes
```

## Pull Request Guidelines

1. **One skill per PR** - Makes review easier
2. **Test your changes** - Run `python install.py` to verify
3. **Keep it simple** - This project values pragmatism over perfection
4. **Update README** - Add your skill to the appropriate section with a one-line description
5. **Update install scripts** - `install.sh` uses dynamic GitHub API discovery — no manual update needed. Verify your skill directory exists at `skills/<name>/SKILL.md`
6. **Quick merges** - If it works and helps, we merge it

### Commit Messages

Keep them simple:

- `add: skill-name` for new skills
- `fix: what you fixed` for fixes
- `docs: what you updated` for documentation

## Skill Quality Checklist

- [ ] Saves real time (5+ minutes)
- [ ] Works without configuration
- [ ] Handles common edge cases
- [ ] Clear, actionable output
- [ ] Under 100 lines of instructions (excluding frontmatter, code blocks, and Token Optimization section)
- [ ] Includes proper YAML frontmatter
- [ ] Includes validation phase for complex skills
- [ ] No emojis in git-related output
- [ ] Proper `disable-model-invocation` setting

## Advanced Skill Features

For complex skills, consider implementing:

### Validation Phases

Skills like `/refactor` and `/implement` should include validation:

```plaintext
/refactor validate  # Check completeness, find loose ends
/implement validate # Verify integration completeness
```

### Extended Thinking

Use `<think>` blocks for sophisticated analysis in:

- Complex architectural refactoring
- Security vulnerability detection
- Multi-step problem solving

### Skill Integration

Minimal, pragmatic suggestions for natural workflow:

- Suggest `/test` after major changes
- Suggest `/commit` at logical checkpoints
- Avoid over-engineering skill chains

### Invocation Control

Use proper frontmatter settings:

- **Manual-only** (`disable-model-invocation: true`): Skills with side effects like `/commit`, `/deploy`
- **Auto-invokable** (`disable-model-invocation: false`): Skills Claude can use automatically like `/review`, `/test`
- **Agent-consumed** (`user-invocable: false`): Skills used internally by agents or commands, hidden from the user menu. Place these in `.claude/skills/<name>/SKILL.md` rather than `skills/<name>/SKILL.md`.

### Skill Tier Assignment

When contributing a new skill, assign it to the appropriate tier:

| Tier | Criteria | Examples |
|---|---|---|
| **Core** | Foundational workflows every developer uses daily | `/commit`, `/review`, `/test`, `/session-*` |
| **Tier 1** | High-impact tools with broad applicability; saves 15+ min/use | `/tdd-red-green`, `/ci-setup`, `/api-test-generate` |
| **Tier 2** | Advanced features for professional workflows; saves 5-15 min/use | `/test-antipatterns`, `/query-optimize`, `/bundle-analyze` |
| **Tier 3** | Power-user and specialized tools; high value for specific scenarios | `/test-mutation`, `/infrastructure`, `/parallel-agents` |

Update the README.md table to include your skill under the correct tier section.

## What We're Looking For

**Yes:**

- Skills that automate tedious tasks
- Cross-platform compatibility improvements
- Real-world workflow optimizations
- Validation phases for complex operations
- Pragmatic skill integration
- Proper YAML frontmatter configuration

**No:**

- Framework-specific tools (unless very popular)
- Skills requiring external dependencies
- Overly complex multi-step wizards
- Over-engineered skill orchestration
- Missing or incorrect frontmatter

## Issue Templates

When creating issues, please use these templates:

### Bug Report

```plaintext
**Skill:** /skill-name
**Expected behavior:** What should happen
**Actual behavior:** What actually happened
**Steps to reproduce:**
1. Run skill with these arguments
2. See error

**Environment:**
- OS: Windows/Linux/macOS
- Claude Code version: X.X.X
```

### Feature Request

```plaintext
**Problem:** What repetitive task are you doing?
**Solution:** How would the skill help?
**Time saved:** Estimate minutes saved per use
**Example usage:** /proposed-skill argument
**Invocation:** Manual-only or auto-invokable?
```

## Community Standards

1. **Professional Communication** - Clear, concise, technical
2. **No Emojis in Code** - Keep skills, commits, PRs, and issues clean and professional
3. **Respect Time** - Quick reviews, fast merges for good contributions
4. **Test Before Submit** - Ensure your skill works on major platforms
5. **Clean Architecture** - Follow clean code principles, no over-engineering
6. **Follow Standards** - Use official [Claude Skills format](https://code.claude.com/docs/en/skills) and [Agent Skills](https://agentskills.io) standard

## Continuous Improvement

AI DevStudio is actively maintained. We:

- Test skills thoroughly before release
- Refine based on real usage patterns
- Fix issues as they're discovered
- Welcome community feedback
- Keep up with Claude Code Skills format updates

Remember: Every skill should make a developer's day a little easier.
