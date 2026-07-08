---
name: github-integration
description: Advanced GitHub automation via MCP GitHub server or gh CLI
disable-model-invocation: true
---

# GitHub Integration & Automation

I'll help you automate GitHub workflows including PR management, issue tracking, and GitHub Actions.

Arguments: `$ARGUMENTS` - operation (pr, issue, actions, release) and specific details

## GitHub Automation Capabilities

**Core Features:**
- Pull request creation, review, and management
- Issue tracking and automation
- GitHub Actions workflow management
- Release automation
- Repository insights and analytics


## Phase 1: GitHub Setup Detection

```bash
#!/bin/bash
# Detect GitHub CLI and MCP server setup

check_github_setup() {
    echo "=== GitHub Integration Setup ==="
    echo ""

    # Check gh CLI
    if command -v gh &> /dev/null; then
        echo "✓ GitHub CLI (gh) installed"
        gh --version

        # Check authentication
        if gh auth status &> /dev/null; then
            echo "✓ GitHub CLI authenticated"
            gh auth status 2>&1 | grep "Logged in"
        else
            echo "⚠️  GitHub CLI not authenticated"
            echo "Run: gh auth login"
        fi
    else
        echo "⚠️  GitHub CLI not installed"
        echo "Install: https://cli.github.com/"
    fi

    echo ""

    # Check for GitHub MCP server
    if [ -f "$HOME/.claude/config.json" ]; then
        if grep -q "github" "$HOME/.claude/config.json"; then
            echo "✓ GitHub MCP server configured"
        else
            echo "⚠️  GitHub MCP server not configured"
            echo "Run: /mcp-setup github"
        fi
    fi

    echo ""

    # Check if in a git repository
    if git rev-parse --git-dir &> /dev/null; then
        echo "✓ Git repository detected"

        # Check for GitHub remote
        if git remote -v | grep -q "github.com"; then
            echo "✓ GitHub remote configured"
            REMOTE_URL=$(git remote get-url origin)
            echo "  Remote: $REMOTE_URL"
        else
            echo "⚠️  No GitHub remote found"
        fi
    else
        echo "⚠️  Not in a git repository"
    fi

    echo ""
}

check_github_setup
```

## Phase 2: Pull Request Automation

### Create Pull Requests

```bash
#!/bin/bash
# Automated PR creation with intelligent defaults

create_pr() {
    local title="$1"
    local body="$2"
    local base="${3:-main}"
    local draft="${4:-false}"

    echo "=== Creating Pull Request ==="
    echo ""

    # Check if we're on a branch
    current_branch=$(git branch --show-current)

    if [ "$current_branch" = "main" ] || [ "$current_branch" = "master" ]; then
        echo "❌ Cannot create PR from main/master branch"
        echo "Create a feature branch first: git checkout -b feature/your-feature"
        exit 1
    fi

    echo "Current branch: $current_branch"
    echo "Target branch: $base"
    echo ""

    # Check for unpushed commits
    if ! git rev-parse --abbrev-ref --symbolic-full-name @{u} &> /dev/null; then
        echo "Pushing branch to remote..."
        git push -u origin "$current_branch"
    fi

    # Generate PR description if not provided
    if [ -z "$body" ]; then
        body=$(generate_pr_description)
    fi

    # Create PR
    if [ "$draft" = "true" ]; then
        gh pr create \
            --title "$title" \
            --body "$body" \
            --base "$base" \
            --draft
    else
        gh pr create \
            --title "$title" \
            --body "$body" \
            --base "$base"
    fi

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Pull request created successfully"
        pr_url=$(gh pr view --json url -q .url)
        echo "  URL: $pr_url"
    else
        echo "❌ Failed to create pull request"
        exit 1
    fi
}

generate_pr_description() {
    cat << EOF
## Summary

$(git log origin/main..HEAD --oneline | sed 's/^/- /')

## Changes

$(git diff origin/main..HEAD --stat)

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or breaking changes documented)
EOF
}

# Parse arguments
case "$1" in
    create)
        create_pr "$2" "$3" "$4" "$5"
        ;;
    *)
        echo "Usage: $0 create <title> [body] [base] [draft]"
        ;;
esac
```

### Review and Merge PRs

```bash
#!/bin/bash
# PR review and merge automation

review_pr() {
    local pr_number="$1"

    echo "=== Pull Request Review ==="
    echo ""

    # View PR details
    gh pr view "$pr_number"

    echo ""
    echo "=== PR Checks ==="

    # Check CI status
    gh pr checks "$pr_number"

    echo ""
    echo "=== Files Changed ==="

    # Show changed files
    gh pr diff "$pr_number" --name-only

    echo ""
    echo "=== Review Comments ==="

    # Show existing reviews
    gh pr review "$pr_number" --list
}

merge_pr() {
    local pr_number="$1"
    local merge_method="${2:-merge}"  # merge, squash, or rebase

    echo "=== Merging Pull Request #$pr_number ==="
    echo ""

    # Check if PR is ready
    pr_state=$(gh pr view "$pr_number" --json state -q .state)

    if [ "$pr_state" != "OPEN" ]; then
        echo "❌ PR is not open (state: $pr_state)"
        exit 1
    fi

    # Check if all checks passed
    checks_status=$(gh pr checks "$pr_number" --json state -q '.[] | select(.state != "SUCCESS") | .name')

    if [ -n "$checks_status" ]; then
        echo "⚠️  Some checks have not passed:"
        echo "$checks_status"
        echo ""
        read -p "Continue with merge? (yes/no): " confirm

        if [ "$confirm" != "yes" ]; then
            echo "Merge cancelled"
            exit 1
        fi
    fi

    # Perform merge
    case "$merge_method" in
        squash)
            gh pr merge "$pr_number" --squash --delete-branch
            ;;
        rebase)
            gh pr merge "$pr_number" --rebase --delete-branch
            ;;
        merge)
            gh pr merge "$pr_number" --merge --delete-branch
            ;;
        *)
            echo "Invalid merge method: $merge_method"
            echo "Use: merge, squash, or rebase"
            exit 1
            ;;
    esac

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Pull request merged successfully"
    else
        echo "❌ Failed to merge pull request"
        exit 1
    fi
}

# Execute
case "$1" in
    review)
        review_pr "$2"
        ;;
    merge)
        merge_pr "$2" "$3"
        ;;
    *)
        echo "Usage: $0 {review|merge} <pr-number> [merge-method]"
        ;;
esac
```

## Phase 3: Issue Management

### Create and Manage Issues

```bash
#!/bin/bash
# GitHub Issues automation

create_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    local assignees="$4"

    echo "=== Creating GitHub Issue ==="
    echo ""

    # Build command
    cmd="gh issue create --title \"$title\""

    if [ -n "$body" ]; then
        cmd="$cmd --body \"$body\""
    fi

    if [ -n "$labels" ]; then
        cmd="$cmd --label \"$labels\""
    fi

    if [ -n "$assignees" ]; then
        cmd="$cmd --assignee \"$assignees\""
    fi

    # Execute
    eval "$cmd"

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Issue created successfully"
        issue_url=$(gh issue list --limit 1 --json url -q '.[0].url')
        echo "  URL: $issue_url"
    else
        echo "❌ Failed to create issue"
        exit 1
    fi
}

list_issues() {
    local state="${1:-open}"
    local limit="${2:-20}"

    echo "=== GitHub Issues ($state) ==="
    echo ""

    gh issue list \
        --state "$state" \
        --limit "$limit" \
        --json number,title,labels,assignees,createdAt \
        --template '{{range .}}{{tablerow (printf "#%v" .number) .title (join ", " (pluck "name" .labels)) (join ", " (pluck "login" .assignees)) (timeago .createdAt)}}{{end}}'
}

update_issue() {
    local issue_number="$1"
    local action="$2"  # close, reopen, edit, add-label, remove-label

    case "$action" in
        close)
            gh issue close "$issue_number" --comment "Resolved"
            echo "✓ Issue #$issue_number closed"
            ;;
        reopen)
            gh issue reopen "$issue_number"
            echo "✓ Issue #$issue_number reopened"
            ;;
        edit)
            gh issue edit "$issue_number" --title "$3" --body "$4"
            echo "✓ Issue #$issue_number updated"
            ;;
        add-label)
            gh issue edit "$issue_number" --add-label "$3"
            echo "✓ Label added to issue #$issue_number"
            ;;
        remove-label)
            gh issue edit "$issue_number" --remove-label "$3"
            echo "✓ Label removed from issue #$issue_number"
            ;;
        *)
            echo "Invalid action: $action"
            exit 1
            ;;
    esac
}

# Execute
case "$1" in
    create)
        create_issue "$2" "$3" "$4" "$5"
        ;;
    list)
        list_issues "$2" "$3"
        ;;
    update)
        update_issue "$2" "$3" "$4" "$5"
        ;;
    *)
        echo "Usage: $0 {create|list|update} [args...]"
        ;;
esac
```

### Bulk Issue Operations

```bash
#!/bin/bash
# Bulk issue management

bulk_label_issues() {
    local label="$1"
    local search_query="$2"

    echo "=== Bulk Label Assignment ==="
    echo ""

    # Find matching issues
    issues=$(gh issue list --search "$search_query" --json number -q '.[].number')

    if [ -z "$issues" ]; then
        echo "No issues found matching: $search_query"
        exit 0
    fi

    issue_count=$(echo "$issues" | wc -l)
    echo "Found $issue_count issues matching search"
    echo ""

    read -p "Add label '$label' to all? (yes/no): " confirm

    if [ "$confirm" = "yes" ]; then
        for issue in $issues; do
            gh issue edit "$issue" --add-label "$label"
            echo "✓ Added label to issue #$issue"
        done
        echo ""
        echo "✓ Bulk label assignment complete"
    else
        echo "Operation cancelled"
    fi
}

close_stale_issues() {
    local days="${1:-30}"

    echo "=== Closing Stale Issues ==="
    echo ""

    # Find issues with no activity
    cutoff_date=$(date -d "$days days ago" +%Y-%m-%d)

    stale_issues=$(gh issue list \
        --search "updated:<$cutoff_date is:open" \
        --json number,title,updatedAt \
        --jq '.[] | "\(.number) \(.title) (last update: \(.updatedAt))"')

    if [ -z "$stale_issues" ]; then
        echo "No stale issues found"
        exit 0
    fi

    echo "Stale issues (no activity in $days days):"
    echo "$stale_issues"
    echo ""

    read -p "Close all stale issues? (yes/no): " confirm

    if [ "$confirm" = "yes" ]; then
        echo "$stale_issues" | while read issue_line; do
            issue_number=$(echo "$issue_line" | cut -d' ' -f1)
            gh issue close "$issue_number" --comment "Closing due to inactivity. Please reopen if still relevant."
            echo "✓ Closed issue #$issue_number"
        done
        echo ""
        echo "✓ Stale issues closed"
    else
        echo "Operation cancelled"
    fi
}

# Execute
case "$1" in
    bulk-label)
        bulk_label_issues "$2" "$3"
        ;;
    close-stale)
        close_stale_issues "$2"
        ;;
    *)
        echo "Usage: $0 {bulk-label|close-stale} [args...]"
        ;;
esac
```

## Phase 4: GitHub Actions Management

### Workflow Status and Management

```bash
#!/bin/bash
# GitHub Actions workflow management

list_workflows() {
    echo "=== GitHub Actions Workflows ==="
    echo ""

    gh workflow list
}

view_workflow_runs() {
    local workflow="$1"
    local limit="${2:-10}"

    echo "=== Workflow Runs: $workflow ==="
    echo ""

    gh run list \
        --workflow "$workflow" \
        --limit "$limit" \
        --json number,status,conclusion,createdAt,headBranch \
        --template '{{range .}}{{tablerow (printf "#%v" .number) .status .conclusion .headBranch (timeago .createdAt)}}{{end}}'
}

watch_workflow() {
    local run_id="$1"

    echo "=== Watching Workflow Run #$run_id ==="
    echo ""

    gh run watch "$run_id"

    # Get final status
    status=$(gh run view "$run_id" --json conclusion -q .conclusion)

    echo ""
    if [ "$status" = "success" ]; then
        echo "✓ Workflow completed successfully"
    else
        echo "❌ Workflow failed with status: $status"
        echo ""
        echo "View logs: gh run view $run_id --log"
    fi
}

rerun_failed_jobs() {
    local run_id="$1"

    echo "=== Rerunning Failed Jobs ==="
    echo ""

    gh run rerun "$run_id" --failed

    if [ $? -eq 0 ]; then
        echo "✓ Failed jobs rerunning"
        watch_workflow "$run_id"
    else
        echo "❌ Failed to rerun jobs"
        exit 1
    fi
}

# Execute
case "$1" in
    list)
        list_workflows
        ;;
    runs)
        view_workflow_runs "$2" "$3"
        ;;
    watch)
        watch_workflow "$2"
        ;;
    rerun)
        rerun_failed_jobs "$2"
        ;;
    *)
        echo "Usage: $0 {list|runs|watch|rerun} [args...]"
        ;;
esac
```

### Trigger Workflows

```bash
#!/bin/bash
# Manually trigger GitHub Actions workflows

trigger_workflow() {
    local workflow="$1"
    local ref="${2:-main}"

    echo "=== Triggering Workflow: $workflow ==="
    echo "Branch/Tag: $ref"
    echo ""

    # Check if workflow accepts workflow_dispatch
    workflow_file=".github/workflows/${workflow}.yml"

    if [ -f "$workflow_file" ]; then
        if grep -q "workflow_dispatch" "$workflow_file"; then
            gh workflow run "$workflow" --ref "$ref"

            if [ $? -eq 0 ]; then
                echo "✓ Workflow triggered"
                echo ""
                echo "Monitor with: gh run watch"
            else
                echo "❌ Failed to trigger workflow"
                exit 1
            fi
        else
            echo "❌ Workflow does not support manual triggering"
            echo "Add 'workflow_dispatch:' to the workflow file"
            exit 1
        fi
    else
        echo "❌ Workflow file not found: $workflow_file"
        exit 1
    fi
}

trigger_workflow "$1" "$2"
```

## Phase 5: Release Automation

```bash
#!/bin/bash
# GitHub Release automation

create_release() {
    local tag="$1"
    local title="$2"
    local notes="$3"
    local prerelease="${4:-false}"

    echo "=== Creating GitHub Release ==="
    echo "Tag: $tag"
    echo "Title: $title"
    echo ""

    # Generate release notes if not provided
    if [ -z "$notes" ]; then
        echo "Generating release notes..."
        notes=$(gh release view --json body -q .body 2>/dev/null || generate_release_notes "$tag")
    fi

    # Create release
    if [ "$prerelease" = "true" ]; then
        gh release create "$tag" \
            --title "$title" \
            --notes "$notes" \
            --prerelease
    else
        gh release create "$tag" \
            --title "$title" \
            --notes "$notes"
    fi

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Release created successfully"
        release_url=$(gh release view "$tag" --json url -q .url)
        echo "  URL: $release_url"
    else
        echo "❌ Failed to create release"
        exit 1
    fi
}

generate_release_notes() {
    local tag="$1"
    local prev_tag=$(git describe --tags --abbrev=0 "$tag^" 2>/dev/null)

    if [ -z "$prev_tag" ]; then
        prev_tag=$(git rev-list --max-parents=0 HEAD)
    fi

    cat << EOF
## What's Changed

$(git log "$prev_tag..$tag" --pretty=format:"- %s (%h)" --no-merges)

## Contributors

$(git log "$prev_tag..$tag" --format='%aN' --no-merges | sort -u | sed 's/^/- @/')

**Full Changelog**: https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)/compare/$prev_tag...$tag
EOF
}

list_releases() {
    local limit="${1:-10}"

    echo "=== GitHub Releases ==="
    echo ""

    gh release list --limit "$limit"
}

# Execute
case "$1" in
    create)
        create_release "$2" "$3" "$4" "$5"
        ;;
    list)
        list_releases "$2"
        ;;
    *)
        echo "Usage: $0 {create|list} [args...]"
        ;;
esac
```

## Phase 6: Repository Insights

```bash
#!/bin/bash
# Repository analytics and insights

repo_stats() {
    echo "=== Repository Statistics ==="
    echo ""

    # Basic info
    gh repo view --json name,description,stargazerCount,forkCount,openIssuesCount

    echo ""
    echo "=== Recent Activity ==="
    echo ""

    # Recent commits
    echo "Recent commits:"
    git log --oneline -5

    echo ""
    echo "Open PRs: $(gh pr list --state open --json number -q '. | length')"
    echo "Open Issues: $(gh issue list --state open --json number -q '. | length')"

    echo ""
    echo "=== Contributors ==="
    echo ""

    # Top contributors
    git shortlog -sn --all --no-merges | head -10
}

pr_stats() {
    echo "=== Pull Request Statistics ==="
    echo ""

    total_prs=$(gh pr list --state all --limit 1000 --json number -q '. | length')
    open_prs=$(gh pr list --state open --json number -q '. | length')
    merged_prs=$(gh pr list --state merged --limit 1000 --json number -q '. | length')

    echo "Total PRs: $total_prs"
    echo "Open PRs: $open_prs"
    echo "Merged PRs: $merged_prs"

    echo ""
    echo "=== Recent PRs ==="
    echo ""

    gh pr list --limit 10 --json number,title,state,createdAt
}

# Execute
case "$1" in
    repo)
        repo_stats
        ;;
    prs)
        pr_stats
        ;;
    *)
        repo_stats
        echo ""
        pr_stats
        ;;
esac
```

## Practical Examples

**Pull Requests:**
```bash
/github-integration pr create "Add feature X"
/github-integration pr review 123
/github-integration pr merge 123 squash
```

**Issues:**
```bash
/github-integration issue create "Bug: Login fails" --label bug
/github-integration issue list open
/github-integration issue close 456
```

**GitHub Actions:**
```bash
/github-integration actions list
/github-integration actions runs ci.yml
/github-integration actions watch 789
```

**Releases:**
```bash
/github-integration release create v1.0.0 "Release 1.0"
/github-integration release list
```

## Integration Points

- `/todos-to-issues` - Convert TODOs to GitHub issues
- `/ci-setup` - Configure GitHub Actions workflows
- `/commit` - Smart commits before creating PRs

## What I'll Actually Do

1. **Verify setup** - Check gh CLI and authentication
2. **Parse command** - Understand the requested operation
3. **Execute safely** - Run GitHub operations with validation
4. **Provide feedback** - Clear status and URLs
5. **Handle errors** - Graceful error messages

**Important:** I will NEVER:
- Expose sensitive tokens or credentials
- Force-merge PRs without approval
- Delete important branches or repositories
- Add AI attribution

All GitHub operations will be safe, validated, and transparent.

**Credits:** Based on GitHub CLI (gh) and MCP GitHub server integration patterns.

---

## Token Optimization

**Expected range**: 1,000–1,800 tokens (initial), 200 tokens (cache hit)

**Caching**: Caches GitHub connection state in `.cache/github-integration/` for 7 days. Invalidated when repo config changes.

**Early exit**: Returns immediately if the tool is already connected and authenticated.

**Patterns used**: Grep-before-Read, early exit, caching, Bash for system queries
