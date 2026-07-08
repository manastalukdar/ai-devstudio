---
name: understand
description: Project architecture analysis to understand structure, patterns, and dependencies
disable-model-invocation: false
---

# Understand Project

I'll analyze your entire application to understand its architecture, patterns, and how everything works together.


```bash
# Check for cached project analysis
CACHE_FILE=".claude/cache/project/architecture.json"
PACKAGE_JSON="package.json"  # Or pyproject.toml, go.mod, etc.

if [ -f "$CACHE_FILE" ] && [ -f "$PACKAGE_JSON" ]; then
    # Verify cache is still valid (package.json hasn't changed)
    CURRENT_CHECKSUM=$(md5sum "$PACKAGE_JSON" 2>/dev/null | cut -d' ' -f1)
    CACHED_CHECKSUM=$(jq -r '.package_checksum' "$CACHE_FILE" 2>/dev/null)

    if [ "$CURRENT_CHECKSUM" = "$CACHED_CHECKSUM" ] && [ "$1" != "--no-cache" ]; then
        echo "✓ Using cached project analysis (saves 99% tokens)"
        jq '.' "$CACHE_FILE"
        exit 0  # Early exit with cached results
    fi
fi

echo "Analyzing project structure (will cache for future runs)..."
```

**Phase 1: Project Discovery (Optimized with Glob and minimal Read)**
Using native tools for efficient analysis:
- **Glob** to map entire project structure (100 tokens vs 10,000+ reading all files)
- **Read** only key files (README, package.json) - 500 tokens
- **Grep** to identify technology patterns (100 tokens)
- **Read** entry points only after Grep identifies them (200 tokens)

**Progressive Depth Levels (saves 80% on shallow runs):**

```bash
DEPTH="shallow"  # Default

case "$1" in
    --medium) DEPTH="medium" ;;
    --deep) DEPTH="deep" ;;
    --frontend|--backend|--database) DEPTH="focused" ;;
esac
```

**Shallow Analysis (500-2,000 tokens)** - Default:
- Project type and main technologies (from package.json)
- Architecture pattern (from directory structure via Glob)
- High-level organization
- Tech stack summary

**Medium Analysis (2,000-4,000 tokens)** - With --medium flag:
- + Detailed directory structure
- + Core module identification
- + Dependency relationships
- + Key integration points

**Deep Analysis (8,000-15,000 tokens)** - With --deep flag:
- + Complete code pattern analysis
- + All component relationships
- + Detailed dependency mapping
- + Comprehensive documentation

I'll discover (based on depth level):
- Project type and main technologies (Glob + Read package.json)
- Architecture patterns (MVC, microservices, etc.) - from Glob structure
- Directory structure and organization (Glob only, no file reads)
- Dependencies and external integrations (from package.json)
- Build and deployment setup (Grep for build configs)

**Phase 2: Code Architecture Analysis**
- **Entry points**: Main files, index files, app initializers
- **Core modules**: Business logic organization
- **Data layer**: Database, models, repositories
- **API layer**: Routes, controllers, endpoints
- **Frontend**: Components, views, templates
- **Configuration**: Environment setup, constants
- **Testing**: Test structure and coverage

**Phase 3: Pattern Recognition**
I'll identify established patterns:
- Naming conventions for files and functions
- Code style and formatting rules
- Error handling approaches
- Authentication/authorization flow
- State management strategy
- Communication patterns between modules

**Phase 4: Dependency Mapping**
- Internal dependencies between modules
- External library usage patterns
- Service integrations
- API dependencies
- Database relationships
- Asset and resource management

**Phase 5: Documentation Synthesis**
After analysis, I'll provide:
- **Architecture diagram** (in text/markdown)
- **Key components** and their responsibilities
- **Data flow** through the application
- **Important patterns** to follow
- **Tech stack summary**
- **Development workflow**

**Integration Points:**
I'll identify how components interact:
- API endpoints and their consumers
- Database queries and their callers
- Event systems and listeners
- Shared utilities and helpers
- Cross-cutting concerns (logging, auth)

**Output Format:**
```
PROJECT OVERVIEW
├── Architecture: [Type]
├── Main Technologies: [List]
├── Key Patterns: [List]
└── Entry Point: [File]

COMPONENT MAP
├── Frontend
│   └── [Structure]
├── Backend
│   └── [Structure]
├── Database
│   └── [Schema approach]
└── Tests
    └── [Test strategy]

KEY INSIGHTS
- [Important finding 1]
- [Important finding 2]
- [Unique patterns]
```

**Save Analysis to Cache (99% savings on next run)**

```bash
# Cache the complete project analysis with checksum
mkdir -p .claude/cache/project
PACKAGE_CHECKSUM=$(md5sum "$PACKAGE_JSON" 2>/dev/null | cut -d' ' -f1)

cat > .claude/cache/project/architecture.json <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "package_checksum": "$PACKAGE_CHECKSUM",
  "project_type": "detected_type",
  "main_technologies": ["tech1", "tech2"],
  "architecture_pattern": "detected_pattern",
  "directory_structure": {
    "frontend": "path/to/frontend",
    "backend": "path/to/backend",
    "tests": "path/to/tests"
  },
  "dependencies": {
    "production": 20,
    "development": 15
  },
  "entry_points": ["src/index.ts", "src/main.ts"],
  "key_patterns": ["pattern1", "pattern2"],
  "integration_points": ["api", "database", "external_services"]
}
EOF

echo "✓ Project analysis cached - next run will use cache (99% token savings)"
```

**Optimization Summary:**
- First run: 2,000-15,000 tokens (depending on depth)
- Cached runs: 500 tokens (99% savings)
- Average across 10 runs: ~1,500 tokens (85% savings)

When the analysis is large, I'll create a todo list to explore specific areas in detail.

This gives you a complete mental model of how your application works, optimized for token efficiency through aggressive caching and progressive depth levels.

## Token Optimization

**Expected range**: 500–6,000 tokens (initial), 50 tokens (cache hit)

**Caching**: Caches project architecture in `.claude/cache/project/architecture.json` for 7 days. Invalidated when project structure changes.

**Early exit**: Returns cached analysis immediately if project structure has not changed.

**Patterns used**: Grep-before-Read, early exit, caching, progressive disclosure
