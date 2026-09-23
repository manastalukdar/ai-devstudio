---
name: search-first
description: Research existing libraries, tools, and in-repo helpers before writing custom code. Use when starting a new feature, adding a dependency, or about to create a new utility/helper/abstraction.
disable-model-invocation: false
risk: none
---

# Search First

Check whether a need is already solved — by code already in this repo, an installed dependency, or a maintained package — before writing anything custom.

## Usage

```
/search-first "resilient HTTP client with retries"
/search-first "markdown dead-link checker"
```

## Behavior

### Phase 1: Preflight

Check which search channels are actually available; state any that are skipped rather than silently omitting them.

```bash
rg --version >/dev/null 2>&1 && echo "repo search: ok"
npm --version >/dev/null 2>&1 || python3 -m pip --version >/dev/null 2>&1
gh auth status >/dev/null 2>&1 && echo "gh: ok"
```

### Phase 2: In-repo search (always first)

```bash
rg -il "<keyword>" --glob '!node_modules' --glob '!dist'
```

A helper, util, type, or pattern that already lives in this repo wins outright — reuse it, do not reimplement it a few files over.

### Phase 3: Stdlib / native / already-installed check

In order: language stdlib, a native platform feature, then an already-installed dependency (check `package.json`/`requirements.txt`/`go.mod`). Any of these beats adding something new.

### Phase 4: External search (only if 1-3 come up empty)

Search the package registry for the language in use (npm, PyPI, crates.io, etc.), then a GitHub code search for maintained OSS. For framework-specific APIs, prefer `/source-driven-development` to pull official docs over guessing from memory.

### Phase 5: Decide

| Signal | Action |
| --- | --- |
| Exact match, well-maintained, permissive license | Adopt as-is |
| Partial match, solid foundation | Extend with a thin wrapper |
| Multiple weak matches | Compose 2-3 small pieces |
| Nothing suitable | Build custom, informed by what was found |

### Phase 6: Implement

Hand off to `/implement` for adopted/extended code, or write the minimal custom code directly. Either way, this is where the actual build happens — search-first only gates what comes before it.

## Examples

**"Add retry logic to our API calls"**
```
Repo search: no existing retry helper
Installed deps: axios (Node) has no built-in retry
Registry search: p-retry (8/10, maintained, MIT)
Decision: Adopt — npm install p-retry, wrap the one call site
```

**"Add a config schema validator"**
```
Repo search: no validator present
Stdlib: none
Registry search: ajv (widely used, MIT)
Decision: Adopt + Extend — install ajv, write the project-specific schema
```

## Token Optimization

**Expected range**: 500-1,500 tokens (initial), 100-300 tokens (cache hit)

**Caching**: Caches registry/GitHub search results per query in `.claude/cache/search-first/<query-hash>.json` for 7 days; invalidated when `package.json`/`requirements.txt`/`go.mod` changes.

**Early exit**: If Phase 2 (repo search) or Phase 3 (stdlib/native/installed) already satisfies the need, stop there and skip Phases 4+ entirely.

**Patterns used**: Grep-before-Read, early exit, caching.

## Edge Cases

- No network access: skip Phase 4, state it explicitly, decide from repo/stdlib/installed deps only.
- No `gh` CLI or registry tooling: fall back to what is available and say so rather than claiming full coverage.
- Everything found is a partial match: prefer Extend over Build; a thin wrapper beats reimplementing the whole thing.
- Registry result is unmaintained or has an incompatible license: treat as "nothing suitable" and fall through to Build.

## Safety

Read-only research phase (network/registry queries, no writes). Only Phase 6 (implementation) touches the working tree, and that is a separate, explicit step the user can decline.
