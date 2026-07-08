---
name: database-connect
description: Database MCP server integration for PostgreSQL, MySQL, MongoDB
disable-model-invocation: true
---

# Database Connection & Management

I'll help you connect to and manage databases through MCP servers for data exploration, schema inspection, and queries.

Arguments: `$ARGUMENTS` - database type (postgres, mysql, mongodb), connection details, or query

## Database Capabilities

**Supported Databases:**
- PostgreSQL (via MCP or native psql)
- MySQL/MariaDB (via MCP or native mysql)
- MongoDB (via MCP or native mongo)
- SQLite (local database files)

**Operations:**
- Schema inspection and exploration
- Safe query execution
- Data exploration and analysis
- Migration support

## Token Optimization

**Expected range**: 1,500–2,500 tokens (initial), 400 tokens (cache hit)

**Caching**: Caches database connection config in `.claude/cache/database/` for 7 days. Invalidated when connection strings change.

**Early exit**: Returns immediately if MCP server for the target database is already connected.

**Patterns used**: Grep-before-Read, early exit, template-based generation, caching
