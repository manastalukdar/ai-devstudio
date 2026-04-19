#!/usr/bin/env python3
# AI DevStudio Uninstaller

"""
AI DevStudio Uninstaller
Removes skill directories from ~/.claude/skills/ and legacy command files from ~/.claude/commands/
"""

import os
import shutil
from pathlib import Path

def main():
    claude_dir = Path.home() / ".claude"
    skills_dir = claude_dir / "skills"
    commands_dir = claude_dir / "commands"

    # Skills to remove
    skills = [
        "cleanproject",
        "commit",
        "contributing",
        "create-todos",
        "docs",
        "explain-like-senior",
        "find-todos",
        "fix-imports",
        "fix-todos",
        "format",
        "implement",
        "make-it-pretty",
        "predict-issues",
        "refactor",
        "remove-comments",
        "review",
        "scaffold",
        "security-scan",
        "session-current",
        "session-end",
        "session-help",
        "session-list",
        "session-resume",
        "session-start",
        "session-update",
        "sessions-init",
        "test",
        "todos-to-issues",
        "understand",
        "undo"
    ]

    # Legacy command files (for backward compatibility)
    legacy_commands = [f"{skill}.md" for skill in skills]
    legacy_commands.extend(["cleanup-types.md", "context-cache.md"])  # Old removed commands

    print("AI DevStudio Uninstaller")
    print("=" * 40)

    # Check for skills (new format)
    installed_skills = 0
    if skills_dir.exists():
        for skill in skills:
            if (skills_dir / skill).exists():
                installed_skills += 1

    # Check for legacy commands (old format)
    installed_legacy = 0
    if commands_dir.exists():
        for cmd in legacy_commands:
            if (commands_dir / cmd).exists():
                installed_legacy += 1

    if installed_skills == 0 and installed_legacy == 0:
        print("[INFO] No AI DevStudio skills or commands found.")
        return

    # Show what will be removed
    if installed_skills > 0:
        print(f"[FOUND] {installed_skills} AI DevStudio skills (new format)")
    if installed_legacy > 0:
        print(f"[FOUND] {installed_legacy} legacy command files (old format)")

    response = input("\nRemove all AI DevStudio skills and commands? (y/N): ")

    if response.lower() != 'y':
        print("[CANCELLED] Uninstall cancelled.")
        return

    # Remove skills (new format)
    removed_skills = 0
    if skills_dir.exists():
        for skill in skills:
            skill_path = skills_dir / skill
            if skill_path.exists():
                try:
                    shutil.rmtree(skill_path)
                    print(f"  - Removed skill: {skill}")
                    removed_skills += 1
                except Exception as e:
                    print(f"  ! Failed to remove skill {skill}: {e}")

    # Remove legacy commands (old format)
    removed_legacy = 0
    if commands_dir.exists():
        for cmd in legacy_commands:
            cmd_path = commands_dir / cmd
            if cmd_path.exists():
                try:
                    os.remove(cmd_path)
                    print(f"  - Removed legacy command: {cmd}")
                    removed_legacy += 1
                except Exception as e:
                    print(f"  ! Failed to remove {cmd}: {e}")

    # Clean up cache and backups if requested
    cache_dir = claude_dir / ".ccplugins_cache"
    backup_dir = claude_dir / ".ccplugins_backups"

    if cache_dir.exists() or backup_dir.exists():
        response = input("\nAlso remove cache and backups? (y/N): ")
        if response.lower() == 'y':
            if cache_dir.exists():
                shutil.rmtree(cache_dir)
                print("  - Removed cache directory")
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
                print("  - Removed backups directory")

    total_removed = removed_skills + removed_legacy
    print(f"\n[SUCCESS] Uninstalled {removed_skills} skills and {removed_legacy} legacy commands ({total_removed} total)")
    print("Thanks for trying AI DevStudio!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[CANCELLED] Uninstall cancelled.")
    except Exception as e:
        print(f"\n[ERROR] Uninstall failed: {e}")