---
name: mcp-setup
description: Set up and configure MCP servers
disable-model-invocation: true
---

# MCP Server Setup

I'll help you set up and configure Model Context Protocol (MCP) servers for enhanced Claude Code capabilities.

Arguments: `$ARGUMENTS` - server name, provider, or configuration type

## MCP Overview

**Model Context Protocol (MCP)** enables Claude Code to connect to external tools and data sources:
- Database access
- API integrations
- File system operations
- Custom tools and services

## Token Optimization

**Expected range**: 400–1,000 tokens (initial), 100 tokens (cache hit)

**Caching**: Caches MCP server registry in `.claude/cache/mcp/servers.json` for 7 days.

**Early exit**: Returns immediately if the requested MCP server is already configured and connected.

**Patterns used**: Grep-before-Read, early exit, caching
