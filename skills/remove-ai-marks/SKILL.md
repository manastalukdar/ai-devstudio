---
name: remove-ai-marks
description: Strip multi-vendor AI provenance marks from files and text — invisible Unicode (Layer A), statistical text watermarks via rewrite (Layer B), and C2PA/EXIF/XMP/container metadata from PNG/JPEG/WebP/SVG/PDF/DOCX/ODT/HTML/MD. Requires the watermarks-remover local service (Docker). Use when the user asks to strip watermarks, remove C2PA/Content Credentials, clean AI metadata, remove invisible Unicode, or runs /remove-ai-marks.
disable-model-invocation: false
risk: safe
---

# Remove AI Marks

Strip AI provenance marks from text and files. Covers three layers:

| Layer | Target | Mechanism |
|---|---|---|
| A | Invisible Unicode, exotic spaces, bidi controls, tag chars | Deterministic service-side clean |
| B | Statistical token-sampling watermarks (SynthID-class, Kirchenbauer) | Agent-driven multi-pass prose rewrite |
| File | C2PA / EXIF / XMP / document properties | PNG, JPEG, WebP, SVG, PDF, DOCX, ODT, HTML, MD |

**Note**: This skill differs from `/remove-ai-tells`, which strips prose writing patterns (filler openers, AI vocabulary, hedging). Use both for thorough cleaning.

## Token Optimization

**Expected range**: 200–400 tokens (inspect only), 400–900 tokens (full clean with Layer B rewrite)

**Early exit**: If the service is unreachable, stop immediately with setup instructions — no further work.

**Patterns used**: Early exit, progressive disclosure (inspect → confirm → clean)

## Prerequisites

Requires the `watermarks-remover` service running locally (default: `http://127.0.0.1:8765`).

```bash
# Quick start via Docker
docker run -p 8765:8765 ghcr.io/guillaumemeyer/watermarks-remover:latest

# Or with Docker Compose (from the watermarks-remover repo)
docker compose up -d
```

Override the service URL via env var: `WATERMARKS_SERVICE_URL=http://...`

## Step 1 — Check Service

```bash
SERVICE_URL="${WATERMARKS_SERVICE_URL:-http://127.0.0.1:8765}"

if ! curl -sf "$SERVICE_URL/health" > /dev/null 2>&1; then
    echo "watermarks-remover service not reachable at $SERVICE_URL"
    echo ""
    echo "Start it with:"
    echo "  docker run -p 8765:8765 ghcr.io/guillaumemeyer/watermarks-remover:latest"
    echo ""
    echo "Or set WATERMARKS_SERVICE_URL to point to a running instance."
    exit 1
fi

# Check what optional backends are available
curl -sf "$SERVICE_URL/capabilities"
```

If the service is down, stop here and show the setup instructions above.

## Step 2 — Identify Target

Resolution order — use the first that yields a valid target:

1. **Explicit argument** — `/remove-ai-marks path/to/file.pdf`
2. **Pasted text** — if the user pasted text without a file path, treat it as inline text
3. **IDE active file** — `<ide_opened_file>` if it has a supported extension
4. **Staged files** — any staged files with a supported extension (`.md`, `.html`, `.pdf`, `.docx`, `.odt`, `.svg`, `.png`, `.jpg`, `.jpeg`, `.webp`)
5. **Ask** — prompt the user

Supported formats: plain text (inline), `.md`, `.html`, `.svg`, `.docx`, `.odt`, `.pdf`, `.png`, `.jpg`, `.jpeg`, `.webp`

## Step 3 — Inspect

For file targets, encode as base64 and POST to `/inspect`:

```bash
encoded=$(base64 -w0 "$TARGET_FILE")
filename=$(basename "$TARGET_FILE")

curl -sf "$SERVICE_URL/inspect" \
    -H "Content-Type: application/json" \
    -d "{\"content\": \"$encoded\", \"filename\": \"$filename\"}" \
    | python3 -m json.tool
```

For inline text:
```bash
encoded=$(printf '%s' "$TEXT" | base64 -w0)
curl -sf "$SERVICE_URL/inspect" \
    -H "Content-Type: application/json" \
    -d "{\"content\": \"$encoded\", \"filename\": \"input.txt\"}"
```

Report the inspection result:
```
Inspection — path/to/file.pdf
  Suspicious codepoints: 3 (U+200B ×2, U+FEFF ×1)
  C2PA metadata: present (Claude provenance, 2026-08-12)
  Format: PDF (auto-detected)
  Layer B: not applicable (not prose text)
```

## Step 4 — Confirm and Clean

Show the inspection report and ask:

```
Proceed with cleaning?
  y — run deterministic clean (Layer A + file metadata)
  b — run Layer B prose rewrite after Layer A (text/markdown targets only)
  n — exit without changes
```

Wait for user confirmation before making changes.

For `y` or `b`, POST to `/clean`:

```bash
curl -sf "$SERVICE_URL/clean" \
    -H "Content-Type: application/json" \
    -d "{\"content\": \"$encoded\", \"filename\": \"$filename\"}" \
    | python3 -c "
import sys, json, base64
r = json.load(sys.stdin)
if r.get('ok'):
    sys.stdout.buffer.write(base64.b64decode(r['cleaned']))
else:
    print('Clean failed:', r.get('report'))
    sys.exit(1)
" > "$TARGET_FILE.clean"
mv "$TARGET_FILE.clean" "$TARGET_FILE"
```

## Step 5 — Layer B Prose Rewrite (optional)

Only for text/markdown targets when the user chose `b`. Apply one rewrite pass to neutralize statistical sampling watermarks. Choose the strategy based on the content type:

- `paraphrase` — word-choice and syntax variation (default for most prose)
- `humanize` — rewrite for natural human voice
- `backtranslate` — pivot-language round-trip (strong signal disruption)
- `structural` — extract outline, regenerate prose (for heavily structured docs)
- `code` — rewording comments, docstrings, string literals; rename local identifiers only with explicit user approval

Apply the chosen strategy as a single rewrite pass. Preserve all facts, numbers, names, citations, and code logic.

## Step 6 — Report

```
remove-ai-marks complete — path/to/file.pdf

Layer A (deterministic):
  Removed: U+200B ×2, U+FEFF ×1
  C2PA metadata: stripped
  EXIF/XMP: stripped

Layer B: skipped (not requested)

File written: path/to/file.pdf
```

If the service reports that exiftool, qpdf, or c2patool are missing, note which metadata actions were skipped and how to add them (rebuild the Docker image with the full variant).

## Edge Cases

- **Binary files without supported extensions**: report "format not supported" and exit
- **C2PA soft binding**: survives metadata strip — note this in the report
- **Pixel/audio/video watermarks**: out of scope (optional CtrlRegen/MarkDiffusion backends require separate Docker images — report as out of scope unless `/capabilities` shows them available)
- **PDF without qpdf**: metadata strip is best-effort; note if qpdf is missing
- **Large files over 50 MB**: warn before encoding; the service may timeout

## Honest Limitations

Always include in the report:
- Layer A removes deterministic markers only; it cannot remove token-sampling watermarks
- Layer B is best-effort; no claim of undetectability without vendor detector access
- C2PA soft binding survives this tool
