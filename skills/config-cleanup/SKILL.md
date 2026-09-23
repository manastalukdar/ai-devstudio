---
name: config-cleanup
description: Garbage-collect a bloated Claude Code configuration (~/.claude and project .claude) — finds stale/duplicate skills, orphaned hooks, redundant permissions, dead MCP servers, and old caches/sessions, then confirms each deletion one at a time. Use when the user says "clean up my config", "my .claude is bloated", "too many skills", "audit my Claude setup", or after installing a large skill pack.
disable-model-invocation: true
risk: critical
allowed-tools: Read, Bash, Grep, Glob
---

# Config Cleanup

Garbage-collect Claude Code configuration: reclaim space and reduce noise in `~/.claude` and project `.claude/` without deleting anything the user didn't approve.

## Usage

```
/config-cleanup                 # scan all channels, walk through candidates
/config-cleanup skills          # scan only one channel: skills|hooks|permissions|mcp|cache
/config-cleanup --report-only   # scan and print candidates, ask nothing, delete nothing
```

## Behavior

### Phase 1: Scan

For each channel below, collect candidates as (path, channel, signal, size, last-modified). Cap the run at 20 candidates total — this is a periodic sweep, not an exhaustive purge.

- **Skills** (`~/.claude/skills/*/`, project `.claude/skills/*/`): near-duplicate names/descriptions, empty or malformed `SKILL.md`, skills with no matching invocation in recent transcripts.
- **Hooks** (`~/.claude/hooks/`, `settings.json` hook entries): scripts on disk referenced by no hook config; hook configs pointing at scripts that no longer exist.
- **Permissions** (`permissions.allow` in `settings.json` / `settings.local.json`): exact duplicates; specific grants already covered by a wildcard already in the list.
- **MCP servers** (`~/.claude.json`, project `.mcp.json`): servers that fail to connect; functional duplicates (same backend, two configs).
- **Caches/sessions** (`.claude/cache/`, `.claude/sessions/`, `file-history/`, `shell-snapshots/`): items older than 30 days, sorted by size descending.

### Phase 2: Rank and present

Sort candidates by confidence (broken/orphaned = high, merely old = low). Present as a numbered table: channel, path, signal, size/age. Do not act on anything yet.

### Phase 3: Checkpoint

Before any deletion, create a git checkpoint if the target is inside a git-tracked project directory:

```bash
git add -A && git stash push -m "checkpoint before config-cleanup"
```

For paths outside version control (most of `~/.claude`), back up the file instead:

```bash
cp ~/.claude/settings.local.json ~/.claude/settings.local.json.bak
```

### Phase 4: Confirm one by one

For every candidate, show the evidence and ask `[y/n/skip]`. No bulk approval, no "delete all". The user can stop at any point and the run still logs what happened up to there.

### Phase 5: Soft-delete

- Skills, hook scripts, cache/session files: move to `.claude/_gc_trash/<date>/` rather than `rm`. Do not rename in place — a renamed `skills/foo.disabled/SKILL.md` is still discovered and loaded.
- Hook config entries: remove from `settings.json` with `jq`, after the Phase 3 backup exists.
- Permission entries: remove from the JSON array with `jq`, after the Phase 3 backup exists.

Only use a hard, unrecoverable delete when the user explicitly asks for one.

### Phase 6: Log and report

Append every action to `.claude/gc_log.md`: timestamp, path, channel, reason, undo instructions. Report reclaimed size, channels left untouched, and a suggested next review date (+30 days).

## Examples

```
/config-cleanup
→ Scanned 5 channels, found 12 candidates.
  1. [hooks]  ~/.claude/hooks/old-lint.sh        orphaned, no config references it   (y/n/skip)
  2. [perms]  Bash(git push)                     shadowed by Bash(*)                (y/n/skip)
  3. [cache]  .claude/cache/review/ (140 files)  38 days old, 4.2 MB                (y/n/skip)
  ...
→ Reclaimed 4.2 MB, moved 1 hook to trash, removed 1 permission entry.
  Logged to .claude/gc_log.md. Next review: 2026-10-23.
```

```
/config-cleanup --report-only
→ 12 candidates found, 0 actions taken (report-only mode).
```

## Token Optimization

**Expected range**: 800–3,000 tokens (initial scan across 5 channels), 150–350 tokens (cache hit)

**Caching**: Stores the last scan result in `.claude/cache/config-cleanup/scan.json` with a 7-day TTL, keyed on the mtimes of `settings.json`, `settings.local.json`, and the skills directory listing. A repeat run within the TTL with no config changes skips straight to "no new candidates since <date>".

**Early exit**: If all five channels return zero candidates, report "config is clean" in one line and skip Phases 2-6 entirely.

**Patterns used**: Bash for system queries (mtime/size scans instead of reading file contents), early exit, caching, progressive disclosure (summary table first, evidence only per-candidate on confirmation).

## Edge Cases

- **No `~/.claude` directory**: report nothing to scan and exit.
- **Non-git project `.claude/`**: skip the `git stash` checkpoint, use file-copy backups only, and say so.
- **Wildcard permission entries with no specific grants**: nothing to shadow-check; skip channel.
- **User stops mid-confirmation**: log what was actioned so far, report partial results, do not silently continue.
- **Skill referenced by a command or agent**: check `.claude/commands/` and `.claude/agents/` for the name before flagging a skill as unused; if referenced, exclude it from candidates.

## Safety

Report-first: nothing is scanned into a delete queue without being shown to the user first. Every deletion requires an individual `[y/n/skip]` confirmation — no bulk approval. A checkpoint (git stash or file backup) is created before the first action of a run. All soft-deletes are reversible (`_gc_trash/` move) with the undo path recorded in `gc_log.md`; hard deletes require explicit user request. Never touches project source code, chat history, or anything outside `~/.claude` and the project's `.claude/` directory.

## Related Skills

- `.claude/skills/project-health` — checks this repo's own doc/skill-count consistency; config-cleanup targets a user's live `~/.claude` install instead.
- `cleanproject` — removes debug artifacts and temp files from a project's source tree; config-cleanup only touches Claude Code configuration.
