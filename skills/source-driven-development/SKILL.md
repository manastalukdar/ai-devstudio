---
name: source-driven-development
description: Fetch official docs before writing any framework-specific code — implement to documented patterns, cite the source, and flag any deviation from the official approach.
disable-model-invocation: false
risk: none
---

# Source-Driven Development

I'll look up the current official documentation for every framework, library, or API involved before writing implementation code. Training data may be stale. Docs are not.

Arguments: `$ARGUMENTS` — feature or task to implement; include library/framework names if known

## Token Optimization

**Expected range**: 400–1,200 tokens (doc fetch + implementation)

**Early exit**: If the API being used is project-internal (no external docs to fetch), skip doc lookup and proceed directly

**Caching**: Cache fetched docs in `.claude/cache/source-driven/<library>-<version>.md` for 24 hours

**Patterns used**: Grep-before-Read (check cache before fetching), progressive disclosure (API summary first, full docs on demand)

## Step 1 — Identify Documentation Targets

From `$ARGUMENTS` and the project context, identify every external library or API to be used:

```bash
# Check installed versions to target the correct docs
cat package.json 2>/dev/null | grep -E '"dependencies"|"devDependencies"' -A 30 | head -40
cat requirements.txt 2>/dev/null | head -20
cat Cargo.toml 2>/dev/null | grep -A 20 '\[dependencies\]'
```

List each target:
```
Libraries to document:
1. [library-name] @ [version]
2. [library-name] @ [version]
```

## Step 2 — Fetch Current Documentation

For each library, fetch the relevant documentation section using the context7 MCP server if available, otherwise fall back to web search:

```
Fetching: [library] v[version] — [specific API or feature]
Source: [URL or context7 library ID]
```

Check the cache first:
```bash
ls .claude/cache/source-driven/ 2>/dev/null | grep "^<library>"
```

## Step 3 — Summarize Relevant API Surface

From the fetched docs, extract only the API surface needed for this task:

```
[Library] v[version] — relevant API:

[Method/hook/config name]
  Signature: [exact signature from docs]
  Purpose: [one line]
  Key notes: [anything non-obvious or changed since common usage]

Source: [URL]
```

Flag any breaking changes or deprecations between the cached/assumed version and the current docs.

## Step 4 — Implement to Documented Patterns

Write the implementation using only the documented API surface from Step 3. For each non-trivial API call, add a source citation comment:

```typescript
// Docs: https://example.com/library/api#method-name
const result = library.method(params)
```

If the documented approach differs from the pattern you would have written from training data, note the difference:

```
Note: implemented using [documented pattern], not [common pattern from training].
Reason: [brief explanation from docs].
```

## Step 5 — Flag Deviations

If implementation requires deviating from the documented pattern (e.g., a known bug workaround, performance constraint), document it explicitly:

```
Deviation: [what differs from docs]
Reason: [why]
Risk: [what breaks if the library is updated to fix the issue]
```

## Edge Cases

- **Docs not publicly available** (private APIs, internal SDKs): proceed with training data, flag the uncertainty explicitly
- **Library version not in docs** (pre-release, fork): note the version gap; use the closest available docs
- **context7 not configured**: fall back to web search; note that results may not be perfectly current
- **Multiple conflicting doc sources** (blog post vs. official docs): always prefer the official library docs; cite both and note the discrepancy
