---
name: performance-profile
description: Performance profiling and bottleneck detection for Node.js, Python, and browser apps
disable-model-invocation: false
---

# Performance Profiling & Bottleneck Detection

I'll profile your application to identify performance bottlenecks and provide optimization recommendations.

**Supported Environments:**
- Node.js profiling (--inspect, clinic.js)
- Browser performance (Chrome DevTools)
- Python profiling (cProfile, line_profiler)
- Bottleneck identification
- Memory leak detection
- Optimization recommendations

**Arguments:** `$ARGUMENTS` - optional: `node|python|browser` or specific file/route to profile

---

## Token Optimization

**Expected range**: 400–2,500 tokens (initial), 200 tokens (cache hit)

**Caching**: Caches runtime detection in `.claude/cache/performance-profile/runtime.json` for 7 days. Invalidated when `package.json` changes.

**Early exit**: Returns immediately if the profiling environment is already configured.

**Patterns used**: Grep-before-Read, early exit, Bash for system queries, caching
