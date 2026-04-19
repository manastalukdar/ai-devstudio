#!/usr/bin/env python3
"""
AI DevStudio Hooks Handler

Handles all 19 Claude Code hook events with audio notifications and JSONL logging.
Inspired by shanraisshan/claude-code-best-practice.

Usage:
    python3 hooks.py [--agent=<agent-name>]

Hook events are passed via stdin as JSON. The CLAUDE_HOOK_EVENT environment
variable contains the event name.
"""

import argparse
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).parent.parent.parent.parent))
LOG_FILE = PROJECT_DIR / ".claude" / "hooks" / "hooks-log.jsonl"

# Events that fire only once per session (once=true in settings.json)
ONCE_EVENTS = {"SessionStart", "SessionEnd", "Setup", "PreCompact"}

# Sound configuration: map event name → sound file basename (without extension)
# Place .wav or .mp3 files in .claude/hooks/sounds/ to enable audio
SOUNDS_DIR = PROJECT_DIR / ".claude" / "hooks" / "sounds"

SOUND_MAP: dict[str, str] = {
    "SessionStart": "session-start",
    "SessionEnd": "session-end",
    "TaskCompleted": "task-complete",
    "PostToolUseFailure": "error",
    "Stop": "stop",
    "PreCompact": "compact",
    "SubagentStart": "subagent-start",
    "SubagentStop": "subagent-stop",
    "WorktreeCreate": "worktree-create",
    "WorktreeRemove": "worktree-remove",
}

# Special bash command patterns → sound override
BASH_SOUND_OVERRIDES: dict[str, str] = {
    "git commit": "commit",
    "git push": "push",
    "git merge": "merge",
    "npm test": "test-run",
    "pytest": "test-run",
    "cargo test": "test-run",
}

# ---------------------------------------------------------------------------
# Platform audio support
# ---------------------------------------------------------------------------


def get_audio_player() -> list[str] | None:
    """Return the audio player command prefix for the current platform, or None."""
    system = platform.system()
    if system == "Darwin":
        return ["afplay"]
    if system == "Linux":
        for player in ("paplay", "aplay", "ffplay"):
            try:
                subprocess.run(
                    ["which", player],
                    capture_output=True,
                    check=True,
                )
                if player == "ffplay":
                    return ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]
                return [player]
            except subprocess.CalledProcessError:
                continue
    if system == "Windows":
        return ["powershell", "-c", "(New-Object Media.SoundPlayer '{sound}').PlaySync()"]
    return None


def play_sound(sound_name: str) -> None:
    """Play a sound file if available. Silently skips if no audio player or file found."""
    player = get_audio_player()
    if player is None:
        return

    # Try common audio extensions
    for ext in (".wav", ".mp3", ".ogg"):
        sound_path = SOUNDS_DIR / f"{sound_name}{ext}"
        if sound_path.exists():
            try:
                cmd = [p.replace("{sound}", str(sound_path)) for p in player]
                if "{sound}" not in player[-1]:
                    cmd = player + [str(sound_path)]
                subprocess.run(cmd, capture_output=True, timeout=5)
            except (subprocess.SubprocessError, FileNotFoundError, OSError):
                pass
            return


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def log_event(event_name: str, payload: dict, agent: str | None = None) -> None:
    """Append a JSONL log entry for the hook event."""
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event_name,
            "agent": agent,
            "tool": payload.get("tool_name") or payload.get("tool") or None,
            "command": _extract_command(payload),
        }
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass  # Never fail on log errors


def _extract_command(payload: dict) -> str | None:
    """Extract the bash command from a tool use payload if present."""
    tool_input = payload.get("tool_input") or {}
    if isinstance(tool_input, dict):
        return tool_input.get("command")
    return None


# ---------------------------------------------------------------------------
# Sound selection logic
# ---------------------------------------------------------------------------


def resolve_sound(event_name: str, payload: dict) -> str | None:
    """Determine which sound to play for this event."""
    # Check for bash command override
    command = _extract_command(payload)
    if command and event_name in ("PreToolUse", "PostToolUse"):
        for pattern, sound in BASH_SOUND_OVERRIDES.items():
            if pattern in command:
                return sound

    return SOUND_MAP.get(event_name)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="AI DevStudio hook handler")
    parser.add_argument("--agent", default=None, help="Agent name for agent-specific handling")
    args = parser.parse_args()

    # Read event name from environment (Claude Code sets this)
    event_name = os.environ.get("CLAUDE_HOOK_EVENT", "Unknown")

    # Read payload from stdin (Claude Code sends JSON)
    payload: dict = {}
    try:
        raw = sys.stdin.read()
        if raw.strip():
            payload = json.loads(raw)
    except (json.JSONDecodeError, OSError):
        pass

    # Log the event
    log_event(event_name, payload, agent=args.agent)

    # Play sound if configured
    sound = resolve_sound(event_name, payload)
    if sound:
        play_sound(sound)


if __name__ == "__main__":
    main()
