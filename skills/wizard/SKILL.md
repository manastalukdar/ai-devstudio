---
name: wizard
description: Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover.
disable-model-invocation: false
risk: safe
---

# Wizard

A **wizard** is a bash script that walks a human, step by step, through a manual procedure that's tedious to do by hand and tedious to re-explain to an AI every time. It opens each URL, says exactly what to click and copy, captures the values, writes them where they belong (`.env`, GitHub secrets), confirms at every stage, and shows how many stages are left.

A wizard is ephemeral by default: built for one run, saved to a scratch or `scripts/` path, deleted when the job's done. Commit it only when the user wants a repeatable setup path that should live in the repo.

**Don't invoke this for steps the agent can perform itself.** This skill is for where a human is genuinely in the loop.

## Process

### 1. Scope the procedure

Work out every manual step the human must take and every value captured along the way. Read the repo first, don't ask cold:

- For **setup**: `.env`, `.env.example`, `.env.*`, `README`, `docker-compose*`, framework config, and `.github/workflows/*` (every `secrets.*` / `vars.*` reference is a value the wizard must produce).
- For **migration or transition**: the current state, the target state, and the irreversible actions between them.

Show the user the ordered list of stages and the values each produces. Confirm: they may add, drop, or reorder.

**Done when:** every stage is named in order, and for each captured value you know (a) where the human gets it, (b) where it's written (`.env`, GitHub secret, both, or nowhere), and (c) whether it's secret (hidden entry) or public.

### 2. Map each stage's journey

For each stage, write the precise path a human follows: which URL to open, what to do there, where a value is shown, which variable it fills. Where you don't know the current UI or exact command, say so and ask the user or check the docs — **never invent steps that may not exist**.

**Done when:** every stage traces to concrete instructions a stranger could follow.

### 3. Author the wizard

Write a bash script to the target path. Use this structure for each stage:

```bash
#!/usr/bin/env bash
set -euo pipefail

TOTAL_STAGES=<N>
CURRENT_STAGE=0

# Helper functions
stage() {
  CURRENT_STAGE=$((CURRENT_STAGE + 1))
  clear
  echo "━━━ Stage $CURRENT_STAGE / $TOTAL_STAGES: $1 ━━━"
  echo
}

open_url() {
  local url="$1"
  echo "Opening: $url"
  if grep -qi microsoft /proc/version 2>/dev/null; then
    powershell.exe /c start "$url"
  elif command -v xdg-open &>/dev/null; then
    xdg-open "$url"
  elif command -v open &>/dev/null; then
    open "$url"
  fi
}

ask() {
  local prompt="$1" var="$2"
  read -rp "$prompt: " "$var"
}

ask_secret() {
  local prompt="$1" var="$2"
  read -rsp "$prompt: " "$var"
  echo
}

write_env() {
  local key="$1" val="$2" file="${3:-.env}"
  if grep -q "^$key=" "$file" 2>/dev/null; then
    sed -i "s|^$key=.*|$key=$val|" "$file"
  else
    echo "$key=$val" >> "$file"
  fi
}

confirm() {
  read -rp "$1 [y/N]: " ans
  [[ "$ans" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 1; }
}

# ── STAGES ──────────────────────────────────────────────

stage "Stage name here"
# say what to do
# open_url "https://..."
# ask_secret "Paste the API key" API_KEY
# write_env "API_KEY" "$API_KEY"

echo
echo "✅ Done! All $TOTAL_STAGES stages complete."
```

Hold the bar: open the URL before asking for its value, use `ask_secret` for anything secret, `write_env` every persisted value, and `confirm` before any irreversible action. Each `stage` clears the screen — keep a stage to one focused task.

### 4. Verify and hand off

- `bash -n <script>` to check syntax; run `shellcheck` if available.
- `chmod +x <script>`.
- **Don't run it end-to-end yourself** — it opens browsers and blocks on human input. Trace it statically: every value from step 1 is captured and lands where step 1 said, and every CI secret name exactly matches a `secrets.*` reference in `.github/workflows/`.
- Tell the user how to run it. If it's a repeatable setup path, commit it and link from the README.

## Token Optimization

**Expected range**: 400–1,500 tokens (reads `.env.example`, `README`, CI workflows, then generates script)

**Patterns used**: Grep-before-Read (only reads relevant config files), early exit (scoping conversation before writing script)

*Ported from [mattpocock/skills](https://github.com/mattpocock/skills) with attribution.*
