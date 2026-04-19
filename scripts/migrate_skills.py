#!/usr/bin/env python3
"""
Migrate command files to new Claude Skills format with YAML frontmatter.
"""

import os
from pathlib import Path

# Define the base directories
BASE_DIR = Path("/media/manas/Study/dev/_my-projects/manastalukdar/ai-devstudio")
COMMANDS_DIR = BASE_DIR / "commands"
SKILLS_DIR = BASE_DIR / "skills"

# Skill categorization
MANUAL_ONLY_SKILLS = {
    "cleanproject": "Remove debug artifacts and temporary files safely with git checkpoint protection",
    "commit": "Analyze changes and create meaningful conventional commits with pre-commit quality checks",
    "format": "Auto-detect and apply code formatting using project's configured formatter",
    "scaffold": "Generate complete feature structures based on your project patterns with full continuity",
    "undo": "Rollback the last destructive operation using git or project backups",
    "session-start": "Begin documented development session using Claude Code CLI's memory system",
    "session-update": "Track progress with timestamps, git status, and todo list updates in current session",
    "session-end": "Generate comprehensive summary and archive session to appropriate project directory",
    "sessions-init": "Organize and synchronize session directory structure based on project architecture",
    "todos-to-issues": "Scan codebase for TODO comments and create professional GitHub issues with context",
}

AUTO_INVOKABLE_SKILLS = {
    "review": "Multi-agent code analysis covering security, performance, quality, and architecture",
    "security-scan": "Comprehensive security analysis with vulnerability detection and remediation tracking",
    "predict-issues": "Proactive problem identification through code analysis and pattern detection",
    "understand": "Project architecture analysis to understand structure, patterns, and dependencies",
    "explain-like-senior": "Senior-level code explanations with deep technical insights and context",
    "contributing": "Contribution readiness assessment analyzing project guidelines and requirements",
    "test": "Intelligent test execution based on context with automatic failure analysis and fixes",
    "implement": "Import and adapt code from any source to your project with validation and testing",
    "refactor": "Structured code restructuring preserving functionality with continuous validation",
    "fix-imports": "Repair broken imports automatically across the project",
    "fix-todos": "Intelligent TODO resolution with context-aware implementation",
    "find-todos": "Locate development tasks and TODO comments across the codebase",
    "create-todos": "Add contextual TODO comments for future development work",
    "remove-comments": "Clean obvious and redundant comments from code",
    "make-it-pretty": "Improve code readability through formatting and structure enhancements",
    "docs": "Smart documentation management for creating and updating project documentation",
    "session-help": "Show help for the session management system and available commands",
    "session-current": "View active session status with progress and context information",
    "session-list": "List all past development sessions with summaries and timestamps",
    "session-resume": "Resume previous work from archived session with full context restoration",
}

def create_skill_file(skill_name: str, description: str, disable_model_invocation: bool):
    """Create a skill file with YAML frontmatter and original content."""

    # Read original content
    original_file = COMMANDS_DIR / f"{skill_name}.md"
    if not original_file.exists():
        print(f"⚠️  Warning: {original_file} not found, skipping...")
        return False

    with open(original_file, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Create skill directory
    skill_dir = SKILLS_DIR / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Create SKILL.md with frontmatter
    skill_file = skill_dir / "SKILL.md"

    # Build frontmatter
    frontmatter = f"""---
name: {skill_name}
description: {description}
disable-model-invocation: {str(disable_model_invocation).lower()}
---

"""

    # Write the new file
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write(original_content)

    print(f"✅ Created {skill_name}/SKILL.md")
    return True

def main():
    """Main migration function."""
    print("🚀 Starting skill migration...\n")

    # Create skills directory
    SKILLS_DIR.mkdir(exist_ok=True)
    print(f"📁 Created {SKILLS_DIR}\n")

    # Migrate manual-only skills
    print("📝 Migrating manual-only skills (disable-model-invocation: true):")
    manual_count = 0
    for skill_name, description in MANUAL_ONLY_SKILLS.items():
        if create_skill_file(skill_name, description, disable_model_invocation=True):
            manual_count += 1

    print(f"\n✨ Migrated {manual_count}/{len(MANUAL_ONLY_SKILLS)} manual-only skills\n")

    # Migrate auto-invokable skills
    print("🤖 Migrating auto-invokable skills (disable-model-invocation: false):")
    auto_count = 0
    for skill_name, description in AUTO_INVOKABLE_SKILLS.items():
        if create_skill_file(skill_name, description, disable_model_invocation=False):
            auto_count += 1

    print(f"\n✨ Migrated {auto_count}/{len(AUTO_INVOKABLE_SKILLS)} auto-invokable skills\n")

    # Summary
    total_expected = len(MANUAL_ONLY_SKILLS) + len(AUTO_INVOKABLE_SKILLS)
    total_migrated = manual_count + auto_count

    print("=" * 60)
    print(f"🎉 Migration Complete!")
    print(f"   Total skills migrated: {total_migrated}/{total_expected}")
    print(f"   Manual-only: {manual_count}")
    print(f"   Auto-invokable: {auto_count}")
    print("=" * 60)

    if total_migrated == total_expected:
        print("\n✅ All skills successfully migrated!")
    else:
        print(f"\n⚠️  {total_expected - total_migrated} skills were not migrated")

if __name__ == "__main__":
    main()
