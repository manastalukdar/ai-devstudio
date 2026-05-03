---
name: setup-pre-commit
description: Install Husky pre-commit hooks with lint-staged (Prettier), type checking, and test automation. Auto-detects package manager. Use when adding pre-commit hooks, setting up Husky, configuring lint-staged, or adding commit-time formatting and type checking.
disable-model-invocation: false
risk: safe
---

# Setup Pre-Commit

Install Husky pre-commit hooks with Prettier formatting, type checking, and test automation.

Arguments: `$ARGUMENTS` - `--no-tests` to skip test hook, `--no-typecheck` to skip typecheck hook

## Behavior

### 1. Detect Package Manager

```bash
if [ -f "bun.lockb" ]; then PM="bun"
elif [ -f "pnpm-lock.yaml" ]; then PM="pnpm"
elif [ -f "yarn.lock" ]; then PM="yarn"
elif [ -f "package-lock.json" ]; then PM="npm"
else PM="npm"  # default
fi
echo "Package manager: $PM"
```

### 2. Check Existing Setup

```bash
# Early exit if already configured
if [ -f ".husky/pre-commit" ] && [ -f ".lintstagedrc" ]; then
  echo "Pre-commit hooks already configured. Show current config?"
  cat .husky/pre-commit
  exit 0
fi

# Check for existing Prettier config
ls .prettierrc .prettierrc.js .prettierrc.json .prettier.config.js 2>/dev/null || MISSING_PRETTIER=true
```

### 3. Install Dependencies

```bash
case "$PM" in
  bun)  bun add -d husky lint-staged prettier ;;
  pnpm) pnpm add -D husky lint-staged prettier ;;
  yarn) yarn add -D husky lint-staged prettier ;;
  npm)  npm install --save-dev husky lint-staged prettier ;;
esac
```

### 4. Initialize Husky

```bash
npx husky init
# Husky v9+ doesn't need shebangs in hook files
```

### 5. Create Pre-Commit Hook

```bash
cat > .husky/pre-commit << 'EOF'
npx lint-staged

EOF

# Add typecheck if script exists and not opted out
if [ "$ARGUMENTS" != *"--no-typecheck"* ] && \
   node -e "const p=require('./package.json'); process.exit(p.scripts?.typecheck ? 0 : 1)" 2>/dev/null; then
  echo 'npm run typecheck --if-present' >> .husky/pre-commit
fi

# Add tests if script exists and not opted out
if [ "$ARGUMENTS" != *"--no-tests"* ] && \
   node -e "const p=require('./package.json'); process.exit(p.scripts?.test ? 0 : 1)" 2>/dev/null; then
  echo 'npm run test --if-present' >> .husky/pre-commit
fi
```

### 6. Create lint-staged Config

```bash
cat > .lintstagedrc << 'EOF'
{
  "*": "prettier --write --ignore-unknown"
}
EOF
# prettier --ignore-unknown skips files Prettier can't parse
```

### 7. Create Prettier Config (if missing)

```bash
if [ "$MISSING_PRETTIER" = true ]; then
  cat > .prettierrc << 'EOF'
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
EOF
fi
```

### 8. Verify

```bash
# Verify all files exist
ls -la .husky/pre-commit .lintstagedrc

# Test lint-staged (dry run against staged files)
git add -N . 2>/dev/null || true
echo "Run 'npx lint-staged' to test against staged files."
```

### 9. Report

```
Pre-commit hooks installed:
  .husky/pre-commit    — runs lint-staged [+ typecheck] [+ tests]
  .lintstagedrc        — Prettier on all staged files
  .prettierrc          — default formatting config [if created]

Package manager: pnpm
Hooks active: lint-staged, typecheck, test

Test it: git add <file> && git commit -m "test"
```

## Examples

```
/setup-pre-commit
/setup-pre-commit --no-tests
/setup-pre-commit --no-typecheck
```

## Edge Cases

- **No `package.json`**: Reports "not a Node.js project" and exits
- **Husky already installed**: Shows current config and offers to update
- **No typecheck/test scripts**: Skips those hooks silently (uses `--if-present`)
- **Monorepo**: Detects workspace root and installs at root level

## Token Optimization

**Expected range**: 300–600 tokens

**Early exit**: Returns immediately if `.husky/pre-commit` and `.lintstagedrc` already exist.

**Bash for detection**: Package manager and existing config detected via filesystem checks — no file reads.

**Patterns used**: Early exit, Bash for system queries, template-based generation
