---
name: graphify
description: Build a queryable knowledge graph from the current codebase using the Graphify CLI — code, SQL schemas, docs, and more in one interactive graph
disable-model-invocation: false
risk: safe
---

# Graphify — Codebase Knowledge Graph

Turn the project into a queryable knowledge graph. Delegates to the [Graphify](https://github.com/safishamsi/graphify) CLI (`graphifyy` on PyPI).

## Usage

```
/graphify              # graph the current directory
/graphify <path>       # graph a specific subdirectory
/graphify --callflow   # also export a Mermaid call-flow HTML page
```

## Behavior

### Step 1 — Verify Graphify is installed

```bash
graphify --version 2>/dev/null || echo "NOT_INSTALLED"
```

If not installed, stop and print:

```
Graphify is not installed. Install it with:

    uv tool install graphifyy        # recommended (auto-adds to PATH)
    pipx install graphifyy           # alternative

Then re-run /graphify.
```

### Step 2 — Run the graph

Use the path from `$ARGUMENTS` if provided, otherwise `.`:

```bash
TARGET="${ARGUMENTS:-.}"
graphify "$TARGET"
```

### Step 3 — Report outputs

After the command succeeds, report the three output files:

```
graphify-out/
├── graph.html       Open in any browser — click nodes, filter, search
├── GRAPH_REPORT.md  Key concepts, surprising connections, suggested questions
└── graph.json       Full graph — query without re-reading files
```

If `--callflow` was passed, also run:

```bash
graphify export callflow-html
```

and report the additional output.

### Step 4 — Suggest next steps

Offer one follow-up based on what the graph found:

- If `GRAPH_REPORT.md` mentions orphaned modules → suggest `/understand --deep`
- If it highlights a complex service → suggest `/architecture-diagram`
- Otherwise → suggest opening `graph.html` and querying a key concept

## Edge Cases

- **No source files found**: Graphify will warn; relay the message and suggest running from the repo root.
- **Large monorepo**: Pass a subdirectory (e.g., `/graphify src/`) to limit scope.
- **Stale graph**: Delete `graphify-out/` and re-run to force a full rebuild.
- **PowerShell**: Remind Windows users to run `graphify .` not `/graphify .`.

## Token Optimization

**Expected range**: 200–400 tokens (the skill itself); Graphify runs out-of-process so no additional LLM tokens are consumed.

**Patterns used**: Bash for system queries (version check, CLI invocation); no file reads; no caching needed — Graphify manages its own output directory.

**Early exit**: Returns immediately with install instructions if the CLI is missing, saving all downstream tokens.
