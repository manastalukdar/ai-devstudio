---
name: browser-testing-with-devtools
description: Use Chrome DevTools MCP for live DOM inspection, console error capture, network request analysis, and paint profiling — runtime verification beyond what Playwright scripting covers.
disable-model-invocation: false
risk: none
---

# Browser Testing with DevTools

I'll connect to a running browser session and inspect it at runtime: DOM state, console errors, network traffic, and rendering performance. Requires Chrome DevTools MCP to be configured.

Arguments: `$ARGUMENTS` — URL to open or test to perform (e.g., "check login flow at http://localhost:3000")

## Token Optimization

**Expected range**: 300–800 tokens per inspection (snapshot + analysis)

**Early exit**: If no issues are found in the initial snapshot, report "No issues detected" and stop

**Patterns used**: Progressive disclosure (summary first, full DOM/network only on specific request)

## Prerequisites

Chrome DevTools MCP must be configured. Verify:

```bash
# Check if chrome-devtools-mcp is in MCP config
grep -r "devtools\|chrome" ~/.claude/settings.json .claude/settings.json 2>/dev/null | head -5
```

If not configured, report the requirement and stop.

## Step 1 — Open or Connect to Page

Navigate to the target URL:

```
Navigate to: [URL from $ARGUMENTS or inferred from project]
Wait for: DOM ready / network idle
```

Take an initial snapshot of the page state (accessibility tree + title).

## Step 2 — Console Error Scan

Capture all console messages:

```
Console output:
  errors:   [count]
  warnings: [count]
  logs:     [count]

Top errors (if any):
  [message] — [source file:line]
```

Any `console.error` or unhandled promise rejection is a test failure. Report immediately.

## Step 3 — DOM Inspection

For the specific flow being tested, inspect the relevant DOM elements:

- Verify expected elements exist and are visible
- Check ARIA roles, labels, and focus order for accessibility
- Confirm form inputs, buttons, and interactive elements are in the expected state
- Flag any elements with `display: none`, `visibility: hidden`, or `opacity: 0` that should be visible

```
DOM check:
  [element] — [found / not found / wrong state]
  [element] — [found / not found / wrong state]
```

## Step 4 — Network Request Analysis

Review network requests made during the test flow:

```
Network:
  total requests: [N]
  failed (4xx/5xx): [N]
  slow (>500ms): [N]

Failed requests:
  [URL] — [status] — [response body excerpt]
```

Flag any unexpected 404s, 401s, CORS errors, or requests to the wrong environment.

## Step 5 — Performance Snapshot

For pages where rendering performance matters:

```
Performance:
  FCP (First Contentful Paint): [N]ms — [good <1.8s / needs work / poor >3s]
  LCP (Largest Contentful Paint): [N]ms — [good <2.5s / needs work / poor >4s]
  Layout shifts: [N] — [stable / unstable]
```

Flag any Core Web Vitals that are in the "needs work" or "poor" range.

## Step 6 — Report

```
Browser Test: [URL] — [PASS / FAIL]

Issues found: [N]
  [severity] [category]: [description]
  ...

Passed checks:
  - [check description]
  ...
```

## Edge Cases

- **Chrome DevTools MCP not available**: report the requirement; suggest using Playwright for automated testing instead
- **Page requires authentication**: note the requirement; the user must provide a session cookie or perform login steps manually before calling this skill
- **Single-page app not fully hydrated**: wait for network idle before inspecting; add explicit wait if hydration takes more than 2 seconds
- **Local dev server not running**: detect via connection refused; report which server to start
