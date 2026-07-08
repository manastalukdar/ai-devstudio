---
name: boilerplate
description: Generate framework-specific boilerplate code
disable-model-invocation: true
---

# Framework Boilerplate Generator

I'll generate framework-specific boilerplate code following best practices and conventions for React, Vue, Next.js, Express, FastAPI, Django, and more.

Arguments: `$ARGUMENTS` - component/route/model name and type

**Supported Frameworks:**
- Frontend: React, Vue, Next.js, Angular, Svelte
- Backend: Express, Fastify, NestJS, FastAPI, Django
- Full-stack: Next.js, Remix, SvelteKit

## Token Optimization

**Expected range**: 1,200–2,000 tokens (initial), 300 tokens (cache hit)

**Caching**: Caches project analysis in `.claude/cache/understand/` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if the requested component already exists.

**Patterns used**: Grep-before-Read, early exit, template-based generation, caching
