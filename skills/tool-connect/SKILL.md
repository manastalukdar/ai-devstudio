---
name: tool-connect
description: Connect to external tools via MCP (GitHub, databases, APIs)
disable-model-invocation: true
---

# External Tool Connection via MCP

I'll help you connect to external tools and services through Model Context Protocol (MCP), enabling direct integration with GitHub, databases, APIs, and more.

Arguments: `$ARGUMENTS` - tool/service name, connection details, or integration type

## Tool Connection Overview

Connect Claude Code to:
- **GitHub** - Repositories, issues, PRs
- **Databases** - PostgreSQL, MySQL, MongoDB, Redis
- **APIs** - REST, GraphQL, gRPC
- **Cloud Services** - AWS, GCP, Azure
- **Project Tools** - Jira, Linear, Slack

## Token Optimization

**Expected range**: 300–800 tokens (initial), 50 tokens (already connected)

**Caching**: Caches tool connection state in `.claude/cache/tools/connections.json` for 7 days.

**Early exit**: Returns immediately if the requested tool is already connected.

**Patterns used**: Grep-before-Read, early exit, caching
