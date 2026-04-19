#!/bin/bash
# Shared utilities for AI DevStudio adapters

# Strip YAML frontmatter (content between first and second --- delimiters)
strip_frontmatter() {
    local file="$1"
    awk 'BEGIN{fm=0} /^---/{fm++; next} fm==1{next} fm>=2{print}' "$file"
}

# Extract a frontmatter field value
get_frontmatter_field() {
    local file="$1"
    local field="$2"
    awk -v field="$field" '
        BEGIN{fm=0}
        /^---/{fm++; next}
        fm==1 && $0 ~ "^"field":"{
            sub("^"field":[[:space:]]*", ""); print; exit
        }
        fm>=2{exit}
    ' "$file"
}

# List all skill directories from a local clone
list_local_skills() {
    local skills_dir="$1"
    find "$skills_dir" -mindepth 1 -maxdepth 1 -type d | sort
}

# List all skill names from GitHub API (requires curl; jq preferred)
list_remote_skills() {
    local api_url="$1"
    local response
    response=$(curl -sSL "$api_url" -H "Accept: application/vnd.github.v3+json")
    if command -v jq &> /dev/null; then
        echo "$response" | jq -r '.[].name' 2>/dev/null
    else
        echo "$response" | grep '"name"' | sed 's/.*"name": "\(.*\)".*/\1/' | grep -v '^\[' | sort -u
    fi
}

# Print a section header for combined output files
section_header() {
    local title="$1"
    printf '\n\n---\n\n# %s\n\n' "$title"
}
