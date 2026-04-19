#!/bin/bash
# Cursor adapter — generates .cursor/rules/*.md files, one rule file per skill.
# Cursor reads .cursor/rules/ automatically; each file becomes an AI rule.
#
# Usage:
#   ./adapters/cursor.sh [--output-dir <dir>] [--skills-dir <dir>]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=adapters/utils.sh
source "$SCRIPT_DIR/utils.sh"

SKILLS_DIR="${SKILLS_DIR:-$SCRIPT_DIR/../skills}"
OUTPUT_DIR="${OUTPUT_DIR:-.cursor/rules}"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
        --skills-dir) SKILLS_DIR="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

mkdir -p "$OUTPUT_DIR"
echo "Generating Cursor rules -> $OUTPUT_DIR/"

skill_count=0
while IFS= read -r -d '' skill_dir; do
    skill_name="$(basename "$skill_dir")"
    skill_file="$skill_dir/SKILL.md"
    [[ -f "$skill_file" ]] || continue

    out="$OUTPUT_DIR/skill-${skill_name}.md"
    {
        printf '---\n'
        printf 'description: Claude DevStudio skill: %s\n' "$skill_name"
        printf 'alwaysApply: false\n'
        printf '---\n\n'
        strip_frontmatter "$skill_file"
    } > "$out"

    ((skill_count++)) || true
done < <(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

echo "[OK] Generated $skill_count rule files in $OUTPUT_DIR/"
echo "     Cursor will load these automatically. Reference a skill with @skill-<name>."
