---
name: code-tour
description: Generate VS Code CodeTour .tour JSON files with persona-targeted, step-by-step walkthroughs anchored to real file:line locations. Use when the user asks for a code tour, onboarding walkthrough, PR tour, architecture walkthrough, RCA tour, or a reusable guided explanation of how a subsystem works.
disable-model-invocation: false
risk: safe
---

# Code Tour

Generate CodeTour `.tour` JSON files: guided, persona-targeted walkthroughs that open directly to real files and line ranges in any editor with the CodeTour extension. Tours live in `.tours/` at the repo root.

## Usage

```
/code-tour onboarding for the payments service
/code-tour architecture tour of src/services
/code-tour PR tour for the current branch
/code-tour explain the auth middleware for a new joiner
```

## Behavior

### Phase 1: Discover

Explore before writing: README, entry points, folder structure, relevant config, and (for PR tours) the changed files via `git diff --name-only`. Do not draft steps before understanding the shape of the code.

### Phase 2: Infer persona and depth

Pick a persona and step count from the request shape:

| Request shape | Persona | Steps |
| --- | --- | --- |
| onboarding, new joiner | `new-joiner` | 9-13 |
| quick tour, overview | `quick-look` | 5-8 |
| architecture | `architect` | 14-18 |
| tour this PR | `pr-reviewer` | 7-11 |
| why did this break | `rca-investigator` | 7-11 |
| security review | `security-reviewer` | 7-11 |
| explain this feature | `feature-explainer` | 7-11 |
| debug this path | `bug-fixer` | 7-11 |

### Phase 3: Verify anchors

Every anchor must be real. For each candidate `file:line`:

```bash
[[ -f "path/to/file" ]] && echo exists
wc -l < "path/to/file"   # confirm the line number is in range
```

If the file is likely to churn, use a `pattern` step instead of a fixed line. Never guess a line number.

### Phase 4: Choose `ref`

`ref` pins the tour to a git branch or commit. When it points anywhere other than what the reader has checked out, CodeTour reads each file from that revision, not from disk — a step on a file that revision lacks fails silently ("could not be opened") while the rest of the tour still renders.

| Tour type | `ref` |
| --- | --- |
| PR tour | the PR branch — never the base branch |
| Onboarding / architecture | the reader's branch (often `main`), or omit |
| Unsure | omit — CodeTour then reads from disk |

### Phase 5: Write the tour

Write to `.tours/<persona>-<focus>.tour`. Structure the narrative as: orientation, module map, core execution path, edge case or gotcha, closing. Each step description should cover situation, mechanism, implication, and the gotcha a careful reader would miss — compact and specific, never generic.

### Phase 6: Validate

Before finishing, confirm: every path exists, every line/selection is in range, the first step anchors to a real file or directory (never content-only), and every referenced file exists at the chosen `ref`.

## Examples

Step types:

```json
{ "directory": "src/services", "title": "Service Layer", "description": "Core orchestration logic lives here." }
```

```json
{ "file": "src/auth/middleware.ts", "line": 42, "title": "Auth Gate", "description": "Every protected request passes here first." }
```

```json
{ "file": "src/app.ts", "pattern": "export default class App", "title": "Application Entry" }
```

Full tour:

```json
{
  "$schema": "https://aka.ms/codetour-schema",
  "title": "Payments Service Tour",
  "description": "Request path through the payments service.",
  "ref": "main",
  "steps": [
    { "directory": "src", "title": "Source Root", "description": "All runtime code starts here." },
    { "file": "src/server.ts", "line": 12, "title": "Entry Point", "description": "The server boots and wires middleware before any route is reached." },
    { "title": "Next Steps", "description": "You can now trace a payment request end to end." }
  ]
}
```

## Token Optimization

**Expected range**: 800-3,200 tokens (initial), 150-350 tokens (cache hit)

**Caching**: Caches the repo's entry-point and folder-structure discovery from Phase 1 in `.claude/cache/code-tour/<repo-hash>.json` for 7 days. Invalidated when `package.json` (or equivalent manifest) changes, or when the requested focus path falls outside the cached scan.

**Early exit**: If a `.tour` file already exists at the target path with the same persona and focus, report its location instead of regenerating.

**Patterns used**: Grep-before-Read for discovery, git diff scope default for PR tours, caching, early exit.

## Edge Cases

- **No git repo / no `ref` context**: omit `ref` and note that the tour reads from disk.
- **Volatile file under active refactor**: use a `pattern` step instead of a line anchor.
- **Requested focus has no `.tours/` directory yet**: create it as part of the write.
- **PR tour where new files aren't on the base branch**: set `ref` to the PR branch, not the base, or the new-file steps will fail to open.
- **Repo too large for the requested step count**: cut steps rather than pad; scope to the relevant package or module instead of touring everything.

## Safety

Only writes `.tour` JSON files under `.tours/`; never modifies source code. All anchors are verified against the actual working tree (or the chosen `ref`) before the file is written — no fabricated line numbers or file paths.

## Related

Cross-reference `understand` for broader architecture analysis before scoping a tour, and `explain-like-senior` for a one-off explanation when a reusable `.tour` artifact isn't needed.
