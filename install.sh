#!/bin/bash
# AI DevStudio Installer for Mac/Linux
#
# Targets:
#   --target claude   (default) Install to ~/.claude/skills/ for Claude Code CLI
#   --target gemini   Generate GEMINI.md for Gemini CLI
#   --target codex    Generate AGENTS.md for Codex CLI
#   --target cursor   Generate .cursor/rules/ for Cursor
#   --target aider    Generate aider-skills/ + .aider.conf.yml for Aider
#   --target generic  Generate system-prompt.md for any AI tool or model API

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="claude"

# Parse flags
while [[ $# -gt 0 ]]; do
    case "$1" in
        --target) TARGET="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Non-Claude targets delegate entirely to the adapter scripts
if [[ "$TARGET" != "claude" ]]; then
    adapter="$SCRIPT_DIR/adapters/${TARGET}.sh"
    if [[ ! -f "$adapter" ]]; then
        echo "[ERROR] Unknown target '$TARGET'. Valid targets: claude gemini codex cursor aider generic"
        exit 1
    fi
    export SKILLS_DIR="$SCRIPT_DIR/skills"
    bash "$adapter"
    exit 0
fi

# ── Claude Code target ─────────────────────────────────────────────────────────
SKILLS_DIR="$HOME/.claude/skills"
MANIFEST_FILE="$SKILLS_DIR/.ai-devstudio-manifest"
REPO_URL="https://raw.githubusercontent.com/manastalukdar/ai-devstudio/main/skills"
API_URL="https://api.github.com/repos/manastalukdar/ai-devstudio/contents/skills"

mkdir -p "$SKILLS_DIR"

# Dynamically discover all skills from GitHub API
echo "Fetching skill list from repository..."
API_RESPONSE=$(curl -sSL "$API_URL" -H "Accept: application/vnd.github.v3+json")

# Parse skill names (requires jq; falls back to grep+sed)
# Use while-read instead of mapfile for bash 3.2 compatibility (macOS default shell)
SKILLS=()
if command -v jq &> /dev/null; then
    while IFS= read -r line; do
        [[ -n "$line" ]] && SKILLS+=("$line")
    done < <(echo "$API_RESPONSE" | jq -r '.[].name' 2>/dev/null)
else
    while IFS= read -r line; do
        [[ -n "$line" ]] && SKILLS+=("$line")
    done < <(echo "$API_RESPONSE" | grep '"name"' | sed 's/.*"name": "\(.*\)".*/\1/' | grep -v '^\[' | sort -u)
fi

if [[ "${#SKILLS[@]}" -eq 0 ]]; then
    echo "[ERROR] Failed to fetch skill list from GitHub. Check your network connection."
    echo "Tip: Try the Python installer instead: python3 install.py"
    exit 1
fi

echo "Found ${#SKILLS[@]} skills."

# Check for existing skills
EXISTING=0
for skill in "${SKILLS[@]}"; do
    if [[ -d "$SKILLS_DIR/$skill" ]]; then
        ((EXISTING++)) || true
    fi
done

if [[ "$EXISTING" -gt 0 ]]; then
    echo "[WARNING] Found $EXISTING existing skills in $SKILLS_DIR"
    read -p "Overwrite existing skills? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "[CANCELLED] Installation cancelled."
        echo "Tip: Use uninstall script first to remove old skills."
        exit 0
    fi
fi

echo "Downloading skills..."
echo "Note: skills with bundled scripts/data (e.g. drawio-skill) require 'python3 install.py' for full installation."
INSTALLED=0
FAILED=0
for skill in "${SKILLS[@]}"; do
    mkdir -p "$SKILLS_DIR/$skill"
    if curl -sSL "$REPO_URL/$skill/SKILL.md" -o "$SKILLS_DIR/$skill/SKILL.md" 2>/dev/null; then
        echo "  + $skill"
        ((INSTALLED++)) || true
    else
        echo "  ! Failed: $skill"
        ((FAILED++)) || true
    fi
done

# Write manifest for uninstaller
printf '%s\n' "${SKILLS[@]}" > "$MANIFEST_FILE"

echo ""
echo "[SUCCESS] Installed $INSTALLED skills to $SKILLS_DIR"
[[ "$FAILED" -gt 0 ]] && echo "[WARNING] $FAILED skills failed to download"
echo "Type / in Claude Code to see available skills"
