---
name: bundle-analyze
description: Bundle size analysis and optimization for Webpack, Vite, and esbuild
disable-model-invocation: false
---

# Bundle Size Analysis & Optimization

I'll analyze your JavaScript bundle size, identify large dependencies, suggest tree-shaking opportunities, and recommend code splitting strategies.

**Supported Build Tools:**
- Webpack (webpack-bundle-analyzer)
- Vite (rollup-plugin-visualizer)
- esbuild (esbuild-visualizer)
- Rollup (rollup-plugin-visualizer)
- Next.js (@next/bundle-analyzer)

**Arguments:** `$ARGUMENTS` - optional: production/development or specific entry point

<think>
Bundle optimization requires understanding:
- JavaScript bundle composition and size impact
- Tree-shaking effectiveness
- Code splitting strategies
- Lazy loading opportunities
- Dependency bloat identification
- Framework-specific optimization patterns
</think>

---

## Token Optimization

**Expected range**: 300–2,500 tokens (initial), 200 tokens (cache hit)

**Caching**: Caches build tool detection in `.claude/cache/bundle-analyze/build-tool.json` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately for already-analyzed bundles or if no build output exists.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
