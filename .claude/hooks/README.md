# AI DevStudio Hooks System

Claude Code fires hook events at key lifecycle moments. This directory contains the hooks infrastructure for AI DevStudio.

## How It Works

All 19 hook events route to `.claude/hooks/scripts/hooks.py`, which:

1. **Logs** every event to `.claude/hooks/hooks-log.jsonl` (timestamp, event, tool, command)
2. **Plays audio** notifications if sound files are present in `.claude/hooks/sounds/`

The hooks script is configured in `.claude/settings.json` under the `"hooks"` key.

## Supported Hook Events (19 total)

| Event | Trigger | `once` |
| --- | --- | --- |
| `PreToolUse` | Before any tool executes | No |
| `PostToolUse` | After a tool succeeds | No |
| `PostToolUseFailure` | After a tool fails | No |
| `PermissionRequest` | When Claude requests a permission | No |
| `UserPromptSubmit` | When user submits a message | No |
| `Notification` | When Claude sends a notification | No |
| `Stop` | When Claude finishes responding | No |
| `SubagentStart` | When a subagent starts | No |
| `SubagentStop` | When a subagent finishes | No |
| `PreCompact` | Before context is compacted | Yes |
| `SessionStart` | At the start of a session | Yes |
| `SessionEnd` | At the end of a session | Yes |
| `Setup` | During initial setup | Yes |
| `TeammateIdle` | When a teammate agent is idle | No |
| `TaskCompleted` | When a task finishes | No |
| `ConfigChange` | When configuration changes | No |
| `WorktreeCreate` | When a git worktree is created | No |
| `WorktreeRemove` | When a git worktree is removed | No |
| `InstructionsLoaded` | When CLAUDE.md instructions load | No |

Events marked `once: true` fire at most once per session.

## Adding Audio Notifications

Place audio files in `.claude/hooks/sounds/`. Supported formats: `.wav`, `.mp3`, `.ogg`.

Default sound name mappings:

| Event | Sound file (without extension) |
| --- | --- |
| `SessionStart` | `session-start` |
| `SessionEnd` | `session-end` |
| `TaskCompleted` | `task-complete` |
| `PostToolUseFailure` | `error` |
| `Stop` | `stop` |
| `PreCompact` | `compact` |
| `SubagentStart` | `subagent-start` |
| `SubagentStop` | `subagent-stop` |
| `WorktreeCreate` | `worktree-create` |
| `WorktreeRemove` | `worktree-remove` |

Bash command overrides (play different sounds for specific commands):

| Command pattern | Sound file |
| --- | --- |
| `git commit` | `commit` |
| `git push` | `push` |
| `git merge` | `merge` |
| `npm test` / `pytest` / `cargo test` | `test-run` |

The sound directory is not tracked by git. Add your own audio files locally.

## Disabling Hooks

To disable all hooks temporarily, set in `.claude/settings.json`:

```json
"disableAllHooks": true
```

To disable a specific event, remove its entry from the `"hooks"` object in `.claude/settings.json`.

## Agent-Level Hooks

Individual agents can define their own hooks in their YAML frontmatter, separate from project-level hooks:

```yaml
---
name: my-agent
hooks:
  PostToolUse:
    - matcher: ".*"
      hooks:
        - type: command
          command: python3 ${CLAUDE_PROJECT_DIR}/.claude/hooks/scripts/hooks.py --agent=my-agent
          timeout: 5000
          async: true
---
```

## Log File

Events are logged to `.claude/hooks/hooks-log.jsonl` (excluded from git via `.gitignore`).

Each line is a JSON object:

```json
{"timestamp": "2026-01-15T10:30:00+00:00", "event": "PostToolUse", "agent": null, "tool": "Edit", "command": null}
{"timestamp": "2026-01-15T10:30:01+00:00", "event": "PostToolUse", "agent": null, "tool": "Bash", "command": "git commit -m \"feat: add skill\""}
```

## Platform Support

Audio playback is platform-aware:

- **macOS**: `afplay`
- **Linux**: `paplay` → `aplay` → `ffplay` (first available)
- **Windows**: PowerShell `Media.SoundPlayer`

If no audio player is available, the script logs only (no error).
