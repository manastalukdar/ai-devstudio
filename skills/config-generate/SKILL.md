---
name: config-generate
description: Generate configuration files for development tools
disable-model-invocation: true
---

# Configuration File Generator

I'll generate configuration files for common development tools: TypeScript, ESLint, Prettier, Jest, Vitest, and more.

Arguments: `$ARGUMENTS` - config type (tsconfig, eslint, prettier, jest, etc.)

**Supported Configs:**
- TypeScript: tsconfig.json
- Linting: .eslintrc.js, .eslintignore
- Formatting: .prettierrc, .prettierignore
- Testing: jest.config.js, vitest.config.ts
- Bundling: vite.config.ts, webpack.config.js
- Git: .gitignore, .gitattributes

## Token Optimization

**Expected range**: 400–800 tokens (initial), 100 tokens (cache hit)

**Caching**: Caches config templates in `.claude/cache/config_templates.json` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if `package.json` is missing or config already exists.

**Patterns used**: Grep-before-Read, early exit, template-based generation, caching
