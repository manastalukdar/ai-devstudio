---
name: changelog-auto
description: Auto-generate changelogs from commit history
disable-model-invocation: true
---

# Automatic Changelog Generator

I'll generate professional changelogs from your git commit history, organized by version and category.

Arguments: `$ARGUMENTS` - version range, tag names, or changelog format

## Changelog Philosophy

- **User-Focused**: Written for end users, not developers
- **Categorized**: Features, fixes, breaking changes
- **Semantic Versioning**: Follow semver principles
- **Keep a Changelog**: Follow keepachangelog.com format


## Phase 1: Commit Analysis

First, let me analyze your git history:

```bash
#!/bin/bash
# Analyze git commit history for changelog generation

analyze_git_history() {
    echo "=== Git History Analysis ==="
    echo ""

    # 1. Check if we're in a git repo
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "❌ Not a git repository"
        exit 1
    fi

    # 2. Get latest tag
    LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
    if [ -z "$LATEST_TAG" ]; then
        echo "No tags found. Analyzing all commits..."
        COMMIT_RANGE="HEAD"
    else
        echo "Latest tag: $LATEST_TAG"
        COMMIT_RANGE="$LATEST_TAG..HEAD"
    fi

    # 3. Count commits by type
    echo ""
    echo "Commits since $LATEST_TAG:"
    git log $COMMIT_RANGE --oneline | wc -l

    echo ""
    echo "Breakdown by type:"
    echo "  Features:  $(git log $COMMIT_RANGE --oneline | grep -c '^[a-f0-9]* feat' || echo 0)"
    echo "  Fixes:     $(git log $COMMIT_RANGE --oneline | grep -c '^[a-f0-9]* fix' || echo 0)"
    echo "  Docs:      $(git log $COMMIT_RANGE --oneline | grep -c '^[a-f0-9]* docs' || echo 0)"
    echo "  Refactor:  $(git log $COMMIT_RANGE --oneline | grep -c '^[a-f0-9]* refactor' || echo 0)"
    echo "  Chore:     $(git log $COMMIT_RANGE --oneline | grep -c '^[a-f0-9]* chore' || echo 0)"

    # 4. Check for breaking changes
    BREAKING_COUNT=$(git log $COMMIT_RANGE --oneline | grep -c '!' || echo 0)
    if [ $BREAKING_COUNT -gt 0 ]; then
        echo ""
        echo "⚠️  WARNING: $BREAKING_COUNT breaking changes detected"
    fi
}

analyze_git_history
```

## Phase 2: Version Detection

I'll determine the next version number:

```bash
#!/bin/bash
# Determine next version using semantic versioning

determine_next_version() {
    local commit_range="$1"

    # Get current version
    CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "0.0.0")
    echo "Current version: $CURRENT_VERSION"

    # Parse version
    IFS='.' read -r MAJOR MINOR PATCH <<< "${CURRENT_VERSION#v}"

    # Check for breaking changes
    HAS_BREAKING=$(git log $commit_range --oneline | grep -E '(^[a-f0-9]* \w+!:|BREAKING CHANGE:)' || echo "")

    # Check for features
    HAS_FEATURES=$(git log $commit_range --oneline | grep '^[a-f0-9]* feat' || echo "")

    # Check for fixes
    HAS_FIXES=$(git log $commit_range --oneline | grep '^[a-f0-9]* fix' || echo "")

    # Determine version bump
    if [ ! -z "$HAS_BREAKING" ]; then
        NEXT_VERSION="$((MAJOR + 1)).0.0"
        BUMP_TYPE="MAJOR (breaking changes)"
    elif [ ! -z "$HAS_FEATURES" ]; then
        NEXT_VERSION="$MAJOR.$((MINOR + 1)).0"
        BUMP_TYPE="MINOR (new features)"
    elif [ ! -z "$HAS_FIXES" ]; then
        NEXT_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
        BUMP_TYPE="PATCH (bug fixes)"
    else
        NEXT_VERSION="$CURRENT_VERSION"
        BUMP_TYPE="NONE (no releasable changes)"
    fi

    echo ""
    echo "Next version: v$NEXT_VERSION"
    echo "Bump type: $BUMP_TYPE"
    echo ""

    echo "$NEXT_VERSION"
}

NEXT_VERSION=$(determine_next_version "$COMMIT_RANGE")
```

## Phase 3: Changelog Generation

I'll generate the changelog in Keep a Changelog format:

```bash
#!/bin/bash
# Generate changelog from git commits

generate_changelog() {
    local version="$1"
    local commit_range="$2"
    local output_file="${3:-CHANGELOG.md}"

    echo "Generating changelog for version $version..."

    # Start changelog
    cat > "$output_file.new" << EOF
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [${version}] - $(date +%Y-%m-%d)

EOF

    # Extract breaking changes
    BREAKING=$(git log $commit_range --grep='BREAKING CHANGE' --format='- %s' || echo "")
    if [ ! -z "$BREAKING" ]; then
        echo "### ⚠️ BREAKING CHANGES" >> "$output_file.new"
        echo "" >> "$output_file.new"
        git log $commit_range --grep='BREAKING CHANGE' --format='- %s%n%b' | \
            sed 's/^BREAKING CHANGE: //' | \
            sed '/^$/d' >> "$output_file.new"
        echo "" >> "$output_file.new"
    fi

    # Extract features
    FEATURES=$(git log $commit_range --oneline | grep '^[a-f0-9]* feat' || echo "")
    if [ ! -z "$FEATURES" ]; then
        echo "### Added" >> "$output_file.new"
        echo "" >> "$output_file.new"
        git log $commit_range --oneline --format='- %s' | \
            grep '^- feat' | \
            sed 's/^- feat[(:]*/- /' | \
            sed 's/^- feat /- /' | \
            sed 's/:.*//' >> "$output_file.new"
        echo "" >> "$output_file.new"
    fi

    # Extract fixes
    FIXES=$(git log $commit_range --oneline | grep '^[a-f0-9]* fix' || echo "")
    if [ ! -z "$FIXES" ]; then
        echo "### Fixed" >> "$output_file.new"
        echo "" >> "$output_file.new"
        git log $commit_range --oneline --format='- %s' | \
            grep '^- fix' | \
            sed 's/^- fix[(:]*/- /' | \
            sed 's/^- fix /- /' | \
            sed 's/:.*//' >> "$output_file.new"
        echo "" >> "$output_file.new"
    fi

    # Extract performance improvements
    PERF=$(git log $commit_range --oneline | grep '^[a-f0-9]* perf' || echo "")
    if [ ! -z "$PERF" ]; then
        echo "### Performance" >> "$output_file.new"
        echo "" >> "$output_file.new"
        git log $commit_range --oneline --format='- %s' | \
            grep '^- perf' | \
            sed 's/^- perf[(:]*/- /' | \
            sed 's/^- perf /- /' >> "$output_file.new"
        echo "" >> "$output_file.new"
    fi

    # Extract refactoring
    REFACTOR=$(git log $commit_range --oneline | grep '^[a-f0-9]* refactor' || echo "")
    if [ ! -z "$REFACTOR" ]; then
        echo "### Changed" >> "$output_file.new"
        echo "" >> "$output_file.new"
        git log $commit_range --oneline --format='- %s' | \
            grep '^- refactor' | \
            sed 's/^- refactor[(:]*/- /' | \
            sed 's/^- refactor /- /' >> "$output_file.new"
        echo "" >> "$output_file.new"
    fi

    # Extract deprecations
    DEPRECATED=$(git log $commit_range --grep='deprecate' -i --format='- %s' || echo "")
    if [ ! -z "$DEPRECATED" ]; then
        echo "### Deprecated" >> "$output_file.new"
        echo "" >> "$output_file.new"
        echo "$DEPRECATED" >> "$output_file.new"
        echo "" >> "$output_file.new"
    fi

    # Extract removals
    REMOVED=$(git log $commit_range --oneline | grep -E '^[a-f0-9]* (remove|delete)' -i || echo "")
    if [ ! -z "$REMOVED" ]; then
        echo "### Removed" >> "$output_file.new"
        echo "" >> "$output_file.new"
        git log $commit_range --oneline --format='- %s' | \
            grep -E '^- (remove|delete)' -i | \
            sed 's/^- remove[(:]*/- /' | \
            sed 's/^- delete[(:]*/- /' >> "$output_file.new"
        echo "" >> "$output_file.new"
    fi

    # Add comparison link
    if [ ! -z "$LATEST_TAG" ]; then
        REPO_URL=$(git remote get-url origin | sed 's/\.git$//')
        echo "[${version}]: ${REPO_URL}/compare/${LATEST_TAG}...v${version}" >> "$output_file.new"
    fi

    # Prepend to existing changelog if it exists
    if [ -f "$output_file" ]; then
        echo "" >> "$output_file.new"
        tail -n +2 "$output_file" >> "$output_file.new"
    fi

    mv "$output_file.new" "$output_file"
    echo "✓ Changelog generated: $output_file"
}

generate_changelog "$NEXT_VERSION" "$COMMIT_RANGE" "CHANGELOG.md"
```

## Phase 4: Enhanced Changelog Formats

I can generate different changelog formats:

### Standard Format (Keep a Changelog)

```markdown
# Changelog

## [2.1.0] - 2026-01-25

### Added
- User profile customization
- Dark mode support
- Export data to CSV

### Fixed
- Login timeout issue
- Memory leak in image processing
- Incorrect timezone handling

### Changed
- Improved search performance by 40%
- Updated UI components to new design system

### Deprecated
- Old API endpoints (v1) - use v2 instead

### Removed
- Legacy payment processor integration

### Security
- Fixed XSS vulnerability in user comments
- Updated dependencies with security patches

[2.1.0]: https://github.com/user/repo/compare/v2.0.0...v2.1.0
```

### GitHub Releases Format

```markdown
## What's Changed

### 🚀 Features
* Add user profile customization by @username in #123
* Implement dark mode support by @username in #124
* Add CSV export functionality by @username in #125

### 🐛 Bug Fixes
* Fix login timeout issue by @username in #126
* Resolve memory leak in image processing by @username in #127
* Correct timezone handling by @username in #128

### ⚡ Performance
* Improve search performance by 40% by @username in #129

### 🔒 Security
* Fix XSS vulnerability in comments by @username in #130

**Full Changelog**: https://github.com/user/repo/compare/v2.0.0...v2.1.0
```

### Detailed Format (with descriptions)

```bash
#!/bin/bash
# Generate detailed changelog with commit bodies

generate_detailed_changelog() {
    local version="$1"
    local commit_range="$2"

    cat > CHANGELOG.md.new << EOF
# Changelog

## [${version}] - $(date +%Y-%m-%d)

### Added

EOF

    # Features with descriptions
    git log $commit_range --format='%h|||%s|||%b' | grep '^[a-f0-9]*|||feat' | while IFS='|||' read -r hash subject body; do
        echo "#### $(echo $subject | sed 's/^feat[(:]*//' | sed 's/^feat //')" >> CHANGELOG.md.new
        if [ ! -z "$body" ]; then
            echo "$body" | sed 's/^/  /' >> CHANGELOG.md.new
        fi
        echo "  ([$(echo $hash | cut -c1-7)](https://github.com/user/repo/commit/$hash))" >> CHANGELOG.md.new
        echo "" >> CHANGELOG.md.new
    done

    # Fixes with descriptions
    echo "### Fixed" >> CHANGELOG.md.new
    echo "" >> CHANGELOG.md.new

    git log $commit_range --format='%h|||%s|||%b' | grep '^[a-f0-9]*|||fix' | while IFS='|||' read -r hash subject body; do
        echo "#### $(echo $subject | sed 's/^fix[(:]*//' | sed 's/^fix //')" >> CHANGELOG.md.new
        if [ ! -z "$body" ]; then
            echo "$body" | sed 's/^/  /' >> CHANGELOG.md.new
        fi
        echo "  ([$(echo $hash | cut -c1-7)](https://github.com/user/repo/commit/$hash))" >> CHANGELOG.md.new
        echo "" >> CHANGELOG.md.new
    done
}
```

## Phase 5: Changelog Validation

I'll validate the generated changelog:

```bash
#!/bin/bash
# Validate changelog quality

validate_changelog() {
    local changelog="$1"

    echo "=== Changelog Validation ==="
    echo ""

    # Check for required sections
    if ! grep -q "## \[" "$changelog"; then
        echo "⚠️  WARNING: No version headers found"
    else
        echo "✓ Version headers present"
    fi

    # Check for dates
    if ! grep -q "[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}" "$changelog"; then
        echo "⚠️  WARNING: No dates found"
    else
        echo "✓ Dates present"
    fi

    # Check for categories
    CATEGORIES=("Added" "Changed" "Deprecated" "Removed" "Fixed" "Security")
    for category in "${CATEGORIES[@]}"; do
        if grep -q "### $category" "$changelog"; then
            count=$(grep -c "^- " "$changelog" | grep -A 20 "### $category" || echo 0)
            echo "✓ $category: found"
        fi
    done

    # Check for empty sections
    if grep -q "### .*\n\n###" "$changelog"; then
        echo "⚠️  WARNING: Empty sections detected"
    fi

    # Check for comparison links
    if grep -q "\[.*\]: http" "$changelog"; then
        echo "✓ Comparison links present"
    else
        echo "⚠️  INFO: No comparison links (add repository URLs)"
    fi

    echo ""
    echo "Validation complete"
}

validate_changelog "CHANGELOG.md"
```

## Phase 6: Integration with Release Process

I'll integrate changelog generation with releases:

```bash
#!/bin/bash
# Complete release workflow with changelog

release_workflow() {
    local version="$1"

    echo "=== Release Workflow: v$version ==="
    echo ""

    # 1. Generate changelog
    echo "Step 1: Generating changelog..."
    /changelog-auto "$version"

    # 2. Stage changelog
    echo "Step 2: Staging changelog..."
    git add CHANGELOG.md

    # 3. Update version files
    echo "Step 3: Updating version files..."
    if [ -f "package.json" ]; then
        npm version $version --no-git-tag-version
        git add package.json package-lock.json
    elif [ -f "setup.py" ]; then
        sed -i "s/version=['\"][^'\"]*['\"]/version='$version'/" setup.py
        git add setup.py
    fi

    # 4. Commit
    echo "Step 4: Creating release commit..."
    git commit -m "chore(release): $version

$(cat CHANGELOG.md | sed -n "/## \[$version\]/,/## \[/p" | head -n -1)"

    # 5. Create tag
    echo "Step 5: Creating git tag..."
    git tag -a "v$version" -m "Release v$version

$(cat CHANGELOG.md | sed -n "/## \[$version\]/,/## \[/p" | head -n -1)"

    # 6. Push
    echo "Step 6: Ready to push..."
    echo ""
    echo "Review the changes and run:"
    echo "  git push origin main"
    echo "  git push origin v$version"
}

release_workflow "$NEXT_VERSION"
```

## Practical Examples

**Auto-Generate:**
```bash
/changelog-auto              # Auto-detect version and generate
/changelog-auto 2.1.0        # Generate for specific version
/changelog-auto v1.0.0..HEAD # Generate for commit range
```

**Different Formats:**
```bash
/changelog-auto --format=github    # GitHub releases format
/changelog-auto --format=detailed  # With commit descriptions
/changelog-auto --format=simple    # Simple bullet list
```

**Release Integration:**
```bash
/changelog-auto --release          # Full release workflow
/changelog-auto --dry-run          # Preview without writing
```

## Conventional Commits Reference

I recognize these commit types:

- `feat:` → **Added** section (new features)
- `fix:` → **Fixed** section (bug fixes)
- `docs:` → **Documentation** section
- `style:` → **Changed** section (formatting)
- `refactor:` → **Changed** section (code restructure)
- `perf:` → **Performance** section (optimizations)
- `test:` → Usually omitted from user changelog
- `chore:` → Usually omitted from user changelog
- `!` or `BREAKING CHANGE:` → **Breaking Changes** section

## Best Practices

**Good Changelog Entries:**
- User-focused ("You can now..." instead of "Added method...")
- Clear and concise
- Links to issues/PRs
- Migration guides for breaking changes
- Security fixes prominently displayed

**Changelog Anti-Patterns:**
- Too technical ("Refactored BaseService class")
- Too vague ("Various improvements")
- Missing context
- Developer-focused language

## What I'll Actually Do

1. **Analyze history** - Parse git commits efficiently
2. **Detect version** - Semantic versioning based on changes
3. **Categorize changes** - Organize by type (features, fixes, etc.)
4. **Generate changelog** - Keep a Changelog format
5. **Validate quality** - Check for completeness
6. **Integrate release** - Optional full release workflow

**Important:** I will NEVER:
- Modify commit history
- Create changelogs without git validation
- Skip breaking change detection
- Add AI attribution

The changelog will be professional, user-focused, and ready for immediate release.

**Credits:** Based on [Keep a Changelog](https://keepachangelog.com) format and [Conventional Commits](https://conventionalcommits.org) specification.

---

## Token Optimization

**Expected range**: 400–1,000 tokens (initial), 50 tokens (no new commits)

**Caching**: Caches last-version info in `.claude/cache/changelog/last-version.json` for 7 days. Invalidated on new tags.

**Early exit**: Returns immediately if no new commits exist since the last changelog entry.

**Patterns used**: Grep-before-Read, early exit, git diff scope default, caching
