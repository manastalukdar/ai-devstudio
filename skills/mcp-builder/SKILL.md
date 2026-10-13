---
name: mcp-builder
description: Guide for building new MCP servers from scratch — tool design, naming conventions, schema, error handling, and evaluation. Covers Python (FastMCP) and TypeScript.
disable-model-invocation: false
risk: none
---

# MCP Server Builder

Guide for building Model Context Protocol (MCP) servers that expose external services to LLMs through well-designed tools.

**Note**: For configuring existing MCP servers, use `/mcp-setup` instead.

## Usage

`/mcp-builder [service name or description]`

## Recommended Stack

- **TypeScript** — prefer for its SDK support and tooling
- **Python (FastMCP)** — when the team is Python-first or wrapping a Python library
- **Transport**: Streamable HTTP with stateless JSON for remote servers; stdio for local servers

## Four-Phase Workflow

---

### Phase 1 — Research and Planning

Before writing code:

1. **Survey the API**: What are the most useful operations? What's read-only vs. mutating?
2. **Balance coverage vs. workflow tools**: Lean toward broad coverage when unsure. Higher-level workflow tools (e.g., `create_and_publish_post`) are useful once common patterns emerge.
3. **Name tools consistently**:
   - `verb_noun` format: `list_repos`, `get_issue`, `create_pull_request`
   - Be specific: `search_issues` not `find_stuff`
   - Group related tools by noun prefix: all `repo_*` tools, all `issue_*` tools
4. **Plan outputs**: Focused, structured outputs — not raw API dumps. Decide what fields matter.
5. **Plan error messages**: Every error should suggest a next step.

---

### Phase 2 — Implementation

**Shared infrastructure first** (build once, use in every tool):

- Authenticated API client with retry logic
- Consistent error handling with actionable messages
- JSON/Markdown formatting helpers
- Pagination helpers where the API is paginated

**For each tool:**

1. Define input schema (Zod for TypeScript, Pydantic for Python) — all fields typed and described
2. Define output schema where possible
3. Write the tool description as if explaining it to someone who has never seen the API — be specific about what it returns and when to use it
4. Set tool annotations:
   - `readOnlyHint: true` — does not modify data
   - `destructiveHint: true` — deletes or overwrites data
   - `idempotentHint: true` — safe to retry
   - `openWorldHint: true` — interacts with external state

**TypeScript skeleton:**

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({ name: "my-service", version: "1.0.0" });

server.tool(
  "list_items",
  "Returns a paginated list of items. Use cursor for subsequent pages.",
  {
    cursor: z.string().optional().describe("Pagination cursor from previous response"),
    limit: z.number().min(1).max(100).default(20),
  },
  async ({ cursor, limit }) => {
    // implementation
  }
);
```

**Python (FastMCP) skeleton:**

```python
from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("my-service")

class ListItemsInput(BaseModel):
    cursor: str | None = None
    limit: int = 20

@mcp.tool()
def list_items(input: ListItemsInput) -> dict:
    """Returns a paginated list of items. Use cursor for subsequent pages."""
    # implementation
```

---

### Phase 3 — Review and Testing

**Code review checklist:**
- [ ] No duplicated error handling — shared helper used everywhere
- [ ] All tools have typed schemas
- [ ] Tool descriptions are specific and useful (not just the function name)
- [ ] Destructive tools have `destructiveHint: true`
- [ ] No credentials or secrets in schema defaults

**Testing:**
1. Build the project (`tsc --noEmit` / `python -m py_compile`)
2. Test with the MCP Inspector: `npx @modelcontextprotocol/inspector`
3. Verify each tool with a real call against the live service
4. Test pagination, empty results, and error conditions

---

### Phase 4 — Evaluations

Write 10 evaluation questions to verify the server works end-to-end:

- **Complex**: Require combining 2+ tool calls
- **Read-only**: No mutations — safe to run repeatedly
- **Independently answerable**: Each question stands alone
- **Verifiable**: Has a known correct string answer you can check

Save as XML:

```xml
<evals>
  <eval id="1">
    <question>How many open issues are in the anthropics/anthropic-sdk-python repo?</question>
    <answer>47</answer>
  </eval>
</evals>
```

Verify every answer yourself before saving. Evals rot — update them when the underlying data changes.

---

## Reference

- MCP specification: https://modelcontextprotocol.io/specification
- TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk
- Python SDK: https://github.com/modelcontextprotocol/python-sdk
- FastMCP: https://github.com/jlowin/fastmcp
- MCP Inspector: `npx @modelcontextprotocol/inspector`

## Token Optimization

**Expected range**: 500–2,000 tokens (initial), 200 tokens (cache hit)

**Early exit**: If the project already has an MCP server configured, confirm whether the goal is to extend it or build a new one before proceeding.

**Patterns used**: Progressive disclosure (one phase at a time), grep-before-read for existing server code
