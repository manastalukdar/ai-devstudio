---
name: remove-ai-tells
description: Detect AI-generated writing patterns in documents — reports filler openers, AI closers, hedge phrases, cliché transitions, template phrasing, AI vocabulary, rhetorical question-answer pairs, and overused intensifiers with a per-document AI-written percentage, then asks before removing anything.
disable-model-invocation: false
---

# Remove AI Tells

I'll scan a document for patterns that signal AI-generated writing, report what was found and what percentage of the document reads as AI-written, then ask before making any changes.

## Token Optimization

**Expected range**: 400–1,200 tokens (detection + report), 50–100 tokens (early exit when file is clean), 800–2,000 tokens (detection + removal)

**Patterns used**: Grep-before-Read, early exit, progressive disclosure, git diff scope default

**Early exit**: If none of the grep patterns match, report "No AI tells found" and stop immediately — no confirmation prompt needed.

**Two-phase design**: Detection (Steps 1–3) always runs and produces the findings report plus the AI-written percentage. Removal (Steps 5–6) only runs after the user explicitly confirms in Step 4, keeping read-only runs cheap.

## Step 1 — Identify Target File(s)

Resolution order — use the first that yields a valid file:

1. **Explicit argument** — `/remove-ai-tells docs/report.md`
2. **IDE active file** — when running inside the VSCode extension, Claude Code receives the currently opened file as `<ide_opened_file>` context. If that file has a doc extension (`.md`, `.txt`, `.rst`, `.adoc`) and no argument was given, use it automatically.
3. **Staged doc files** — any staged files with a doc extension.
4. **Ask** — if none of the above yield a target, prompt the user.

```bash
# Steps 1 and 3 are bash-resolvable; step 2 is resolved from IDE context.

declare -a TARGETS

if [[ -n "$ARGUMENTS" ]]; then
    # Split normal whitespace-separated arguments, then keep each resolved path quoted later.
    read -r -a TARGETS <<< "$ARGUMENTS"
elif [[ -n "$IDE_ACTIVE_FILE" ]] && echo "$IDE_ACTIVE_FILE" | grep -qE '\.(md|txt|rst|adoc)$'; then
    # IDE_ACTIVE_FILE is populated from <ide_opened_file> context when available
    TARGETS=("$IDE_ACTIVE_FILE")
    echo "Using IDE active file: $IDE_ACTIVE_FILE"
elif ! git diff --cached --quiet; then
    mapfile -t TARGETS < <(git diff --cached --name-only -- '*.md' '*.txt' '*.rst' '*.adoc')
else
    echo "No target file specified and no staged doc files found."
    echo "Usage: /remove-ai-tells <file>"
    exit 1
fi

if (( ${#TARGETS[@]} == 0 )); then
    echo "No doc files found."
    exit 1
fi

printf 'Targets:\n'
printf '  %s\n' "${TARGETS[@]}"
```

## Step 2 — Grep for AI-Tell Patterns (Early Exit)

Run all pattern checks before reading any file content. If nothing matches, stop immediately.

```bash
FINDINGS_FILE=$(mktemp)

run_check() {
    local _label="$1"
    local pattern="$2"
    local output
    output=$(grep -HniE "$pattern" "${TARGETS[@]}" || true)
    if [[ -n "$output" ]]; then
        printf '%s\n' "$output" | tee -a "$FINDINGS_FILE"
    fi
}

# Filler openers (sentence-start affirmations)
run_check "Filler openers" "^(Certainly|Absolutely|Of course|Sure,|Great!|Excellent!|Awesome|Wonderful|Totally!|Noted!|Perfect!|Interesting!|Fantastic!|Exactly!|Indeed,|Naturally,|Obviously,|Clearly,)[,!.]?"
# "Great question" variants — strong AI tell whether or not they open the line
run_check "Great question variants" "(Great question[!.]?|That'?s (a )?(great|excellent|good) question|Thank(s| you) for (your question|asking)[.!]?)"
# Validation openers — AI affirming the user before answering
run_check "Validation openers" "^(You'?re (absolutely |completely )?(right|correct)[.!,]|That'?s (absolutely |completely )?correct[.!,])"

# AI closers — sign-off phrases almost never written by humans
run_check "AI closers" "(I hope (this (helps|clarifies|answers)|that (helps|answers)|you found this (helpful|useful))|Hope this helps|I trust this helps|Let me know if you (have any questions|need (anything|further|more))|Is there anything else (I can|you'?d like)|If you have any questions,? feel free to|Happy to (help|clarify|answer)|Thank(s| you) for (your question|asking)[.!]?$)"

# Hedging phrases
run_check "Hedging phrases" "(It('s| is) (worth|important) (noting|to note|mentioning|considering|emphasizing|pointing out)|Please note that|It should be noted|Note that,|It is (important|essential|critical) to (note|mention|understand|remember)|needless to say|To be (fair|honest|clear|precise),|Just to (clarify|be clear),|To clarify,|[Aa]s (I |we )?(mentioned|noted|discussed) (earlier|above|before)|[Kk]eep in mind that|[Bb]ear in mind that|I should (note|mention)|[Ww]orth (mentioning|pointing out)|I'?d like to (point out|highlight|note|emphasize)|I want to (highlight|emphasize))"

# Transition clichés
run_check "Transition clichés" "\b(Moreover,|Furthermore,|Additionally,|In addition,|In conclusion,|In summary,|That being said,|That said,|With that in mind,|With th(is|at) in mind,|With that said,|Having said that,|At the end of the day,|It goes without saying|First and foremost,|Last but not least,|To summarize,|To recap,|In a nutshell,|On that note,|To that end,|As such,|In light of (this|that),|Moving forward,|Going forward,|On a related note,|On the flip side,|Suffice it to say,|All things considered,|By the same token,|To put it another way,|In any case,|Nonetheless,|Nevertheless,|Not only that,)"

# Template phrasing — generic article scaffolding common in AI output
run_check "Template phrasing" "\b(In today'?s .{0,40} (world|landscape|environment|era)|in an era where|now more than ever|when it comes to|at its core|the reality is|the truth is|not just [^,.;]+, but|more than just|isn'?t just [^,.;]+, it'?s|whether you'?re (a )?[^,.;]+ or|from [^,.;]+ to [^,.;]+|there are several reasons why|let'?s take a closer look|ultimately, the choice depends on|the future of [^,.;]+ is)\b"

# Structural AI patterns
run_check "Key takeaways" "(The key takeaway(s)?[: ]|Key takeaway(s)?:)"
# "Here are N ways/steps/tips/reasons" — AI list intro
run_check "List intros" "^Here are [0-9]+ (ways?|steps?|tips?|reasons?|things?|examples?|point)"
# "Pro tip" / "Quick tip" — AI filler label
run_check "Tip labels" "^(Pro tip|Quick tip)[: ]"
# Rhetorical question immediately answered — "What is X? X is …" (same or next line)
for target in "${TARGETS[@]}"; do
    awk '
        index($0, "?") { prev_line=NR; prev_text=$0; next }
        prev_line && $0 ~ /^[[:space:]]*[A-Z]/ {
            print FILENAME ":" prev_line ":" prev_text
            print FILENAME ":" NR ":" $0
            prev_line=0
        }
        /^[[:space:]]*$/ { prev_line=0 }
    ' "$target" | tee -a "$FINDINGS_FILE"
done
# Bold overuse — flag files where bolding appears on more than 1 in 10 non-blank lines
for target in "${TARGETS[@]}"; do
    total_lines=$(grep -c . "$target" || echo 1)
    bold_lines=$(grep -c "\*\*" "$target" || true)
    if (( bold_lines * 10 > total_lines )); then
        printf '%s: %s bolded line(s) across %s non-blank lines (possible over-formatting)\n' "$target" "$bold_lines" "$total_lines" | tee -a "$FINDINGS_FILE"
    fi
done

# AI vocabulary — words/phrases statistically overrepresented in LLM output
run_check "AI vocabulary" "\b(delve|dive into|unpack(ing)?|leverage[sd]?|utilize[sd]?|facilitate[sd]?|robust(ness)?|seamless(ly)?|holistic(ally)?|synergy|synergize|cutting.?edge|state.?of.?the.?art|groundbreaking|transformative|revolutionize|unlock(ing)? (the )?(full |true )?potential|foster(ing)?|empower(ing)?|best practices|pivotal|crucial|enhance[sd]?|underscore[sd]?|landscape|vibrant|testament|showcase[sd]?|intricate(ly)?|evolving)\b"
# Additional high-frequency LLM vocabulary
run_check "High-frequency LLM vocabulary" "\b(nuanced?|comprehensive|meticulous(ly)?|paramount|streamline[sd]?|actionable|harness(ing|ed)?|game-?changer|game-?changing|innovative|innovation|tailored|invaluable|endeavou?r(ing|ed)?|aforementioned|navigate[sd]? (the )?(complexities|challenges)|impactful|vital|scalability|scalable|elevate[sd]?|reimagine[sd]?|redefine[sd]?|disruptive|disrupt(ing|ed)?|pave the way|at the forefront)\b"
# Metaphorical "drive" — "drive results/innovation/growth/success/change"
run_check "Metaphorical drive" "\bdrive[sd]? (results?|innovation|growth|success|change|impact|value|adoption|engagement)\b"
# Additional aspirational/corporate LLM vocabulary
run_check "Aspirational corporate vocabulary" "\b(propel(ling|led)?|catalyze[sd]?|catalyst|amplify|amplified|amplifying|bolster(ing|ed)?|accelerate[sd]? (growth|adoption|change|innovation|progress)|spearhead(ing|ed)?|champion(ing|ed)? (innovation|diversity|change|growth)|synergistic(ally)?|paradigm( shift)?|ecosystem)\b"
# Elevated register / vague praise not yet covered
run_check "Elevated vague praise" "\b(noteworthy|commendable|multifaceted|sophisticated|optimal(ly)?|optimize[sd]?|hallmark|cornerstone|bedrock|best-in-class|world-class|top-?tier|unprecedented|revolutionary|visionary|pioneering)\b"

# Self-referential AI phrases
run_check "Self-referential AI phrases" "(As an AI|As a language model|As your assistant|I('m| am) here to help|Feel free to (ask|reach out)|Don't hesitate to|I'd be (happy|glad|delighted) to|[Ll]et me walk you through|I'?ll walk you through|I want to assure you|I'?m (excited|pleased|delighted) to (share|tell|show|present)|Allow me to (explain|walk|show|clarify|demonstrate)|Let me (clarify|explain|break (this|it) down)|Let'?s (explore|examine|break down|get started|dive in|begin)|I'?ll (begin|start) by|We'?ll (cover|explore|look at|discuss|examine))"

# Padding openers
run_check "Padding openers" "^(In other words,|To put it simply,|Simply put,|In essence,|Essentially,|Basically,|Ultimately,|Overall,)"

# Wordiness — circumlocutions always replaceable with a shorter form
run_check "Wordiness" "\b(in order to|due to the fact that|at this point in time|in the event that|with (regard|respect) to|the fact that|prior to|make use of|a (number|wide range|variety|great deal) of|is able to|has the ability to|it is possible to|as a result of|take into (consideration|account)|on a regular basis|in the case of|in spite of the fact that|in the near future|at a later (date|time)|subsequent to|for the purpose of|on the basis of|with the exception of|in the majority of cases)\b"
run_check "Vague connector" "\bin terms of\b"

# Contrast structures
run_check "Contrast structures" "(It'?s not .+, it'?s|Not [A-Z][^.]+\. Not [A-Z]|Despite this)"

# Vague authority
run_check "Vague authority" "(experts? say|experts? (argue|suggest|agree|believe|note)|according to experts?|many experts? (say|believe|suggest)|industry reports?|as per (industry|expert) (standards?|guidelines?|consensus)|many believe|some argue that|it could be argued that|one could argue|studies show|research (shows|suggests|indicates)|data (shows|suggests|indicates)|the data|it is (widely|generally|commonly) (believed|accepted|known|recognized|understood)|conventional wisdom (holds|suggests|says)|it has been shown that|it is (recommended|expected|suggested) that|general(ly accepted)? consensus)"

# Importance / significance sentences
run_check "Importance sentences" "\b(impact|legacy|significance|broader (trend|context|implications)|plays? a (pivotal|crucial|key|vital) role)\b"

# Hollow superlatives — claims of importance or optimality with no supporting evidence
run_check "Hollow superlative openers" "^(Most importantly,|Above all,)"
run_check "Hollow superlatives" "\b(the best way to|the most important (thing|step|aspect|consideration)|the only way to|one of the most (important|effective|powerful|significant|compelling|critical))\b"

# Assertion intensifiers — AI over-asserts certainty without evidence
run_check "Assertion intensifiers" "\b(without (question|a doubt)|there'?s no denying (that|this)|undeniably|unquestionably|it'?s no secret that|make no mistake|rest assured)\b"
run_check "Overused intensifiers" "\bhighly (recommended|effective|relevant|valuable|efficient|useful|important|beneficial)\b"

# Anticipatory patterns — AI preemptively answering questions the reader didn't ask
run_check "Anticipatory openers" "^(You might be wondering|You may be (wondering|asking yourself)|You'?re probably wondering|As you (may|might|probably) (already )?know,|You may have noticed|Chances are,)"
run_check "Anticipatory setup" "(This is where .{1,40} comes in|That'?s where .{1,40} comes in)"

# Excessive affirmative intensifiers
run_check "Excessive affirmative intensifiers" "\b(very very|really really|quite (quite|very))\b"

# Setup phrases — AI narrative scaffolding before the actual content
run_check "Setup phrases" "(Having (established|covered|discussed) that,?|Now that we.?ve (established|covered|discussed|looked at)|Now that we have (established|covered))"

# Hedged superlatives — AI softening an unsupported superlative claim
run_check "Hedged superlatives" "\b(arguably (the |one of the )?(most|best)|perhaps the (most|best))\b"

# AI certainty phrases — vague assertion of obvious clarity
run_check "AI certainty phrases" "\b(crystal clear|abundantly clear|perfectly clear)\b"

# AI framing phrases — good news / bad news setup before findings
run_check "Good news / bad news framing" "^(The good news (is|here)|The bad news (is|here))"

# Additional self-referential phrases
run_check "Additional self-referential phrases" "\b(I (encourage|invite|urge) you to)\b"

# Additional anticipatory patterns
run_check "Additional anticipatory patterns" "(if you.?re like most (people|developers?|users?|teams?|companies|organizations)|you.?ve probably (heard|seen|noticed|experienced|come across))"

# Additional wordiness — causal circumlocutions
run_check "Causal circumlocutions" "\b(in light of the fact that|owing to the fact that)\b"

# Internal cross-references — AI signposting that substitutes for clear structure
run_check "Internal cross-references" "\b(in (the )?(next|following|upcoming) section|as we.?ll see (below|later|above)|as (discussed|mentioned|noted|covered) (in )?(the )?(previous|next|following) section)\b"

# Em dash overuse — flag any line containing 2+ em dashes, or count total per file
for target in "${TARGETS[@]}"; do
    dash_count=$(grep -o "—" "$target" | wc -l | tr -d ' ')
    total_lines=$(grep -c . "$target" || echo 1)
    if (( dash_count > total_lines / 30 && dash_count > 1 )); then
        printf '%s: %s em dash(es) across %s non-blank lines\n' "$target" "$dash_count" "$total_lines" | tee -a "$FINDINGS_FILE"
    fi
done
# Also flag lines with multiple em dashes on one line
grep -HnE ".+—.+—" "${TARGETS[@]}" | tee -a "$FINDINGS_FILE" || true

# Right arrow overuse — "→" used as a prose connector or visual separator
grep -Hn "→" "${TARGETS[@]}" | tee -a "$FINDINGS_FILE" || true

# Section separator overuse — "---" on its own line (horizontal rule used as section divider)
grep -HnE "^---$" "${TARGETS[@]}" | tee -a "$FINDINGS_FILE" || true
```

If zero matches across all patterns, output:

```
No AI tells found in <file>. Document reads naturally.
```

and stop. If executing the shell snippet directly, this means `[[ ! -s "$FINDINGS_FILE" ]]`.

## Step 3 — Categorize, Score, and Report Findings

Group matches by category and report with line numbers. Do not make any changes yet.

Before reporting, discard obvious false positives:

- Matches inside fenced code blocks
- Matches inside YAML front matter
- Matches in blockquotes or quoted source text
- Matches in examples that intentionally demonstrate AI output
- Matches in generated-file notices, changelog boilerplate, or license text

```
AI tells found in docs/report.md:

Filler openers (2)
  L3:  "Certainly, here is the summary..."
  L47: "Absolutely! The next step is..."

AI vocabulary (5)
  L12: "leverage the existing infrastructure"
  L18: "seamless integration"
  L29: "robust solution"
  L34: "let's delve into the specifics"
  L61: "holistic approach"

Hedge phrases (1)
  L55: "It's worth noting that performance may vary"

Transition clichés (2)
  L40: "Furthermore, this approach..."
  L70: "In conclusion, we recommend..."

Template phrasing (2)
  L83: "In today's fast-paced development landscape..."
  L91: "This is not just a workflow, but a mindset..."

Total: 12 patterns across 1 file
```

### AI-Written Percentage

After collecting all matches, compute an estimate of how AI-written the document is:

```bash
for target in "${TARGETS[@]}"; do
    total_lines=$(grep -c . "$target" || echo 1)

    # Count distinct line numbers already reported for this file.
    # The findings file uses grep -Hn-style output: path:line:match.
    hit_lines=$(
        awk -F: -v file="$target" '$1 == file && $2 ~ /^[0-9]+$/ { print $2 }' "$FINDINGS_FILE" |
        sort -u |
        wc -l |
        tr -d ' '
    )

    percentage=$(( (hit_lines * 100 + total_lines / 2) / total_lines ))
    printf '%s: %s%% (%s flagged lines out of %s non-blank lines)\n' "$target" "$percentage" "$hit_lines" "$total_lines"
done
```

Report the score immediately after the findings block:

```
AI-written estimate: 17% (12 flagged lines out of 72 non-blank lines)
  Low (0–15%)    — occasional AI patterns; targeted fixes sufficient
  Medium (16–40%) — noticeable AI register; consider paragraph rewrites
  High (41%+)    — pervasive AI tone; consider full-section rewrites
```

Bracket interpretation is informational only. Always show the raw numbers so the user can judge.

## Step 4 — Ask Before Removing

After reporting the findings and score, always ask before making any changes:

```
Proceed with removal? Options:
  y   — apply all automatic fixes, then prompt for confirmation-required ones
  n   — exit without changes
  l   — list only (you already see the list above; this exits without changes)
  s   — selective: choose which categories to fix
```

Wait for the user's response. Do not apply any edits until the user confirms with `y` or `s`.

If the user chooses `s`, present each category in turn:

```
Fix "Filler openers" (2 instances)? (y/n)
Fix "AI vocabulary" (5 instances)? (y/n)
Fix "Hedge phrases" (1 instance)? (y/n)
Fix "Transition clichés" (2 instances)? (y/n)
Fix "Template phrasing" (2 instances)? (y/n)
```

Proceed only with the categories the user approves.

## Step 5 — Apply Fixes

### Automatic replacements (safe, no ambiguity)

Apply these without asking — the replacement is always better:

| Pattern | Replacement |
|---|---|
| `utilize` | `use` |
| `leverage` (verb) | `use` / `apply` |
| `facilitate` | `help` / `enable` |
| `delve` (any form) | `explore` / `examine` / `investigate` / `look at` |
| `dive into` (as prose filler) | `examine` / `look at` / *(remove)* |
| `unpack` (as prose filler) | `examine` / `explain` / *(remove)* |
| `In conclusion,` | *(remove — just end the section)* |
| `In summary,` | *(remove, or keep if it heads a genuine summary block)* |
| `To summarize,` | *(remove)* |
| `To recap,` | *(remove)* |
| `In a nutshell,` | *(remove)* |
| `First and foremost,` | *(remove — just state the first point)* |
| `Last but not least,` | *(remove — just state the final point)* |
| `It's worth noting that` | *(remove — just state the thing)* |
| `It is worth noting/mentioning/considering` | *(remove)* |
| `It is important/essential to note/mention` | *(remove)* |
| `Please note that` | `Note:` |
| `It should be noted that` | *(remove)* |
| `needless to say` | *(remove — if it's needless to say, don't say it)* |
| `To be fair,` / `To be honest,` / `To be clear,` | *(remove — just make the statement)* |
| `As I mentioned earlier/above/before` | *(remove — trust the reader to remember)* |
| `feel free to` | *(remove)* |
| `don't hesitate to` | *(remove)* |
| `I'd be happy to` | *(remove)* |
| `I hope this helps` / `Hope this helps` | *(remove)* |
| `Let me know if you have any questions` | *(remove)* |
| `Let me know if you need anything` | *(remove)* |
| `Is there anything else I can help with` | *(remove)* |
| `Happy to help` / `Happy to clarify` | *(remove)* |
| `Great question!` / `That's a great question` | *(remove — just answer the question)* |
| `Thank you for your question` / `Thanks for asking` | *(remove — just answer)* |
| `Perfect!` / `Interesting!` / `Fantastic!` / `Exactly!` as openers | *(remove)* |
| `You're right` / `You're absolutely right` / `That's correct` as openers | *(remove — just answer)* |
| `Indeed,` / `Naturally,` / `Obviously,` / `Clearly,` as sentence openers | *(remove — let the sentence stand alone)* |
| `I hope you found this helpful` / `I trust this helps` | *(remove)* |
| `Just to clarify,` / `Just to be clear,` / `To clarify,` | *(remove — just state the thing)* |
| `Keep in mind that` / `Bear in mind that` | *(remove — just state the thing)* |
| `I should note` / `I should mention` / `Worth mentioning` / `Worth pointing out` | *(remove — just state the thing)* |
| `I'd like to point out` / `I'd like to highlight` / `I want to highlight` | *(remove — just state the thing)* |
| `impactful` | *(remove or name what specifically changes)* |
| `vital` (vague) | *(remove or use "required" / "needed" if accurate)* |
| `scalable` / `scalability` (vague) | *(remove or describe the specific scale requirement)* |
| `elevate` (vague) | *(replace with what specifically improves: "speeds up", "reduces", "adds")* |
| `reimagine` / `redefine` | *(remove or describe what specifically changes)* |
| `disruptive` / `disrupt` (vague praise) | *(remove or name what it replaces)* |
| `pave the way` | *(remove — state what becomes possible directly)* |
| `at the forefront` | *(remove or name the specific position/advantage)* |
| `drive` + vague object ("drive results", "drive growth") | *(remove or replace: "increase", "reduce", "produce")* |
| `propel` (vague) | *(remove or replace with the specific mechanism)* |
| `catalyze` / `catalyst` (vague) | *(remove or name the specific trigger)* |
| `amplify` (vague) | *(remove or replace: "increase", "extend", "strengthen")* |
| `bolster` | *(remove or replace: "strengthen", "support", "increase")* |
| `accelerate` + vague object | *(remove or replace with a specific rate or mechanism)* |
| `spearhead` | `lead` / `run` / *(remove)* |
| `champion` (verb, vague) | `support` / `advocate for` / *(remove)* |
| `synergistic` | *(remove — describe the actual interaction)* |
| `paradigm shift` | *(remove or name what specifically changed)* |
| `ecosystem` (vague) | *(remove or name the specific set of tools/teams/systems)* |
| `Pro tip:` / `Quick tip:` | *(remove the label — just state the tip)* |
| `now more than ever` | *(remove — state the current condition directly)* |
| `At its core,` | *(remove — state the definition directly)* |
| `The reality is` / `The truth is` | *(remove — the statement should carry itself)* |
| `Let's take a closer look` | *(remove — just start the closer look)* |
| `Most importantly,` / `Above all,` as openers | *(remove — let the sentence stand on its own weight)* |
| `the best way to` | *(remove the superlative — state the approach directly)* |
| `the most important [thing/step/aspect]` | *(remove — state what matters and why instead)* |
| `the only way to` | *(remove unless literally true — rewrite as a recommendation)* |
| `one of the most (important|effective|powerful|significant)` | *(remove the superlative frame — state the specific quality directly)* |
| `some argue that` / `it could be argued that` / `one could argue` | *(remove — state the claim directly or attribute it to a named source)* |
| `a number of` | `several` / `many` |
| `a wide range of` / `a variety of` | `many` / `various` |
| `make use of` | `use` |
| `is able to` / `has the ability to` | `can` |
| `it is possible to` | `you can` |
| `prior to` | `before` |
| `it is (widely|generally) believed/accepted/known` | *(remove — state the claim directly or name a source)* |
| `conventional wisdom` | *(remove — state the claim directly or name a source)* |
| `it has been shown that` | *(remove — state the finding directly or cite a source)* |
| `it is recommended that` | *(rewrite as direct advice: "use X" not "it is recommended that X be used")* |
| `it is expected that` | *(rewrite as direct statement or remove)* |
| `generally accepted consensus` / `general consensus` | *(remove — state the claim directly)* |
| `Moving forward,` / `Going forward,` | *(remove — just continue)* |
| `On a related note,` | *(remove — let the connection be implicit, or start a new section)* |
| `On the flip side,` | *(remove — rewrite as "but" or "however" or two plain sentences)* |
| `Suffice it to say,` | *(remove — just say the thing)* |
| `noteworthy` | *(remove or state what specifically is worth noting)* |
| `commendable` | *(remove — state what specifically works well)* |
| `multifaceted` | *(remove or name the specific facets)* |
| `sophisticated` (vague) | *(remove or describe the specific complexity)* |
| `optimal` / `optimize` (vague) | *(replace with the specific criterion: "fastest", "smallest", "cheapest")* |
| `hallmark` | *(remove the phrase — state the trait directly)* |
| `cornerstone` / `bedrock` | *(remove — state the dependency directly)* |
| `best-in-class` / `world-class` / `top-tier` | *(remove — name the specific benchmark or comparison)* |
| `unprecedented` | *(remove or cite what it surpasses specifically)* |
| `revolutionary` (vague) | *(remove or describe what specifically changed)* |
| `visionary` | *(remove — state the specific insight or direction instead)* |
| `pioneering` (vague) | *(remove or name what was done first and why it mattered)* |
| `Let me walk you through` / `I'll walk you through` | *(remove — just start the explanation)* |
| `Allow me to (explain|clarify)` | *(remove — just explain or clarify)* |
| `Let me clarify` / `Let me explain` | *(remove — just state the clarification)* |
| `Let me break this down` | *(remove — just start the breakdown)* |
| `Let's explore` / `Let's examine` / `Let's break down` / `Let's dive in` / `Let's get started` | *(remove — just start)* |
| `I'll begin by` / `I'll start by` | *(remove — just begin)* |
| `We'll cover` / `We'll explore` / `We'll look at` | *(remove — just start; or replace "we'll" with "this section covers")* |
| `I want to assure you` | *(remove — just make the assertion)* |
| `I'm excited to share` / `I'm pleased to present` | *(remove — just share or present)* |
| `make no mistake` | *(remove — just state the claim)* |
| `rest assured` | *(remove — just state what is true)* |
| `You might be wondering` / `You may be asking yourself` | *(remove — just answer directly)* |
| `As you may know,` / `As you probably know,` | *(remove — state the fact without patronizing the reader)* |
| `You may have noticed` | *(remove — just state the observation)* |
| `Chances are,` | *(remove — just state the claim)* |
| `I encourage you to` / `I invite you to` / `I urge you to` | *(remove — just state the recommendation directly)* |
| `if you're like most people/developers/users` | *(remove — just state the claim; don't patronize the reader)* |
| `you've probably heard/seen/noticed` | *(remove — just state the observation)* |
| `Having established that,` / `Now that we've established` | *(remove — just continue; the content carries itself)* |
| `The good news is` / `The bad news is` | *(remove — just state the finding directly)* |
| `crystal clear` / `abundantly clear` / `perfectly clear` | `clear` |
| `arguably the most` / `arguably one of the best` | *(remove the hedge — state the claim directly or provide evidence)* |
| `perhaps the most` / `perhaps the best` | *(remove — state the claim or add supporting evidence)* |
| `in the next section` / `in the following section` | *(remove — let the section follow naturally via headings)* |
| `as we'll see below` / `as we'll see later` | *(remove — let the content speak when reached)* |
| `as discussed/mentioned/noted in the previous/next section` | *(remove — trust the reader to follow the document structure)* |
| `in the near future` | `soon` |
| `at a later date` / `at a later time` | `later` |
| `subsequent to` | `after` |
| `for the purpose of` | `to` |
| `on the basis of` | `based on` |
| `with the exception of` | `except` |
| `in the majority of cases` | `usually` / `mostly` |
| `according to experts` / `many experts believe` | *(remove — state the claim directly or cite a specific source)* |
| `as per (industry|expert) standards/guidelines` | *(remove — state the specific requirement)* |
| `without question` / `without a doubt` | *(remove — just make the claim)* |
| `there's no denying that` | *(remove — just state the claim)* |
| `undeniably` / `unquestionably` | *(remove — just state the claim)* |
| `it's no secret that` | *(remove — just state the claim)* |
| `highly recommended` | `recommended` *(or name the specific reason)* |
| `highly effective` / `highly relevant` | *(remove `highly` — the adjective stands alone)* |
| `You might be wondering` / `You may be asking yourself` | *(remove — just answer the question directly)* |
| `This is where [X] comes in` / `That's where [X] comes in` | *(rewrite as a direct statement about X)* |
| `as a result of` | `because of` |
| `take into consideration` / `take into account` | `consider` |
| `on a regular basis` | `regularly` |
| `in the case of` | `for` / `when` |
| `in spite of the fact that` | `although` |
| `in order to` | `to` |
| `due to the fact that` | `because` |
| `at this point in time` | `now` / `currently` |
| `in the event that` | `if` |
| `with regard to` / `with respect to` | `about` |
| `the fact that` (padding) | *(restructure — rewrite as a direct clause)* |
| `in terms of` (vague connector) | *(remove — rewrite with a concrete verb)* |
| `in light of the fact that` | `because` |
| `owing to the fact that` | `because` |
| `seamless` | *(remove or replace with specific adjective)* |
| `robust` | *(remove or replace with specific adjective)* |
| `holistic` | `end-to-end` / `full` / *(remove)* |
| `cutting-edge` | *(remove or name the specific technology)* |
| `state-of-the-art` | *(remove or name the specific capability)* |
| `groundbreaking` | *(remove)* |
| `streamline` | *(replace with what specifically changes: "cuts steps", "reduces time", "simplifies")* |
| `actionable` | *(remove — "actionable steps" → "steps", "actionable insights" → "findings")* |
| `comprehensive` | *(remove or replace with what it actually covers)* |
| `meticulous` / `meticulously` | *(remove — describe the specific care taken instead)* |
| `paramount` | `critical` / `required` / *(remove)* |
| `invaluable` | *(remove or state the specific value)* |
| `innovative` / `innovation` (vague praise) | *(remove or name the specific improvement)* |
| `game-changer` / `game-changing` | *(remove or describe what specifically changes)* |
| `harness` (as in "harnessing the power of") | `use` / `apply` / *(remove the whole phrase)* |
| `endeavor` / `endeavour` | `try` / `work` / `aim` |
| `aforementioned` | *(remove — use "this" / "the" or repeat the noun)* |
| `Furthermore,` | *(remove the opener — let the sentence stand alone)* |
| `Moreover,` | *(remove)* |
| `Additionally,` / `In addition,` | `Also,` *(or remove)* |
| `Nonetheless,` / `Nevertheless,` | *(remove — rewrite as two plain sentences or use "but")* |
| `Not only that,` | *(remove — just state the next point)* |
| `That being said,` / `That said,` | *(remove)* |
| `With that in mind,` / `With that said,` | *(remove)* |
| `On that note,` | *(remove)* |
| `To that end,` | *(remove)* |
| `As such,` | *(remove — rewrite with the actual logical connector: "so", "therefore", "because of this")* |
| `In light of this,` / `In light of that,` | *(remove)* |
| `With this in mind,` | *(remove)* |
| `All things considered,` | *(remove — just end the section)* |
| `By the same token,` | *(remove — rewrite with "similarly" or restructure)* |
| `To put it another way,` | *(remove — if the first version was clear, delete the repetition; if not, replace the first version)* |
| `In any case,` | *(remove)* |
| `At the end of the day,` | *(remove)* |
| `pivotal` | *(remove or replace with specific adjective)* |
| `crucial` | *(remove or use "required" / "needed" if accurate)* |
| `enhance` | *(replace with what specifically changes: "speeds up", "cuts", "adds")* |
| `underscore` (verb) | `show` / `confirm` / *(remove)* |
| `landscape` (abstract) | *(remove or name the specific domain)* |
| `vibrant` | *(remove)* |
| `testament` | *(remove the whole clause — state the fact directly)* |
| `showcase` | `show` / `demonstrate` |
| `intricate` | *(remove or describe the specific complexity)* |
| `evolving` | *(remove or name what is changing)* |
| `Despite this,` | *(remove — rewrite as two plain sentences)* |
| `Overall,` | *(remove — just end the section)* |

Apply all automatic replacements first using Edit, removing the minimal surrounding text.

### Confirmation-required replacements

For these, show the current line and the proposed rewrite, then ask before changing:

- Filler openers (`Certainly!`, `Absolutely!`, `Perfect!`, `Indeed,`, `Obviously,`, `Great question!`, etc.) — show the full sentence so the user can see if removing the opener changes meaning
- AI closers (`I hope this helps`, `I trust this helps`, `Let me know if you have any questions`, `Thank you for your question`, etc.) — show the paragraph end so the user can confirm removal doesn't cut real content
- Template phrasing (`In today's...`, `in an era where`, `not just X but Y`, `whether you're X or Y`, `from X to Y`, `when it comes to`, `the future of X is`) — show the sentence and offer a direct rewrite that names the actual subject
- Em dashes — show each occurrence in context; replace with a comma, colon, or parentheses depending on use, or remove the clause if it is padding. Flag files where em dashes appear more than once per 30 lines as likely overused.
- `→` arrows — show each occurrence in context; legitimate in code examples, tables, or CLI output, but overused in prose as a connector ("This leads to → better outcomes"). Remove from prose and rewrite as a complete sentence. Flag files where `→` appears more than once per 20 lines as likely overused.
- `---` section separators — flag standalone horizontal rules used between prose sections; remove and rely on headings for structure instead. Skip occurrences inside YAML front matter blocks or code fences.
- `leverage` when used as a noun ("leverage over competitors") — may be correct usage
- `nuanced` / `nuance` — sometimes accurate; show context and ask whether the specific distinction is named elsewhere in the sentence
- `tailored` — show context; legitimate when describing actual customization ("tailored to each team's workflow"), flagged when vague ("tailored solutions")
- `innovative` / `innovation` — confirm if referring to a named feature or product; remove if used as vague praise
- `navigate` — confirm if used literally (navigation UI, routing); flag if used as a metaphor ("navigate the complexities of")
- `comprehensive` — confirm if the document genuinely covers everything it claims; remove if used as a boast
- `vital` — confirm if the consequence of skipping is actually named; remove if used as vague emphasis
- `scalable` / `scalability` — confirm if a specific scale requirement or measurement is cited; remove if vague
- `disruptive` / `disrupt` — confirm if a specific incumbent or practice being replaced is named; remove if used as vague praise
- `drive` + object — confirm if a causal mechanism is described; remove if it is a vague action claim ("drives success")
- `elevate` — confirm if what specifically improves is named; remove if used as vague praise
- `reimagine` / `redefine` — confirm if what changes and how is specified; remove if used as aspiration language
- Wordiness patterns (`in order to`, `due to the fact that`, etc.) — auto-replacements are always safe, but show the rewritten sentence so the user can verify no meaning was lost
- Bold overuse — show a count of bolded phrases per page; ask the user which ones to remove rather than stripping all
- `accelerate` — confirm if a specific rate, timeline, or mechanism is cited; remove if used as vague praise
- `catalyst` / `catalyze` — confirm if the specific trigger and effect are named; remove if used as a metaphor for vague change
- `ecosystem` — confirm if a specific set of tools, services, or teams is named; remove if used as an abstract container word
- `paradigm shift` — confirm if what changed and what replaced it are both named; remove if used as aspiration language
- `As such,` — sometimes a legitimate logical connector ("the file was missing; as such, the build failed"); confirm before removing
- Hollow superlatives (`the best way to`, `the most important`) — show the sentence; if evidence is given in the same or next sentence, it may be justified; confirm before removing
- Validation openers (`You're right`, `That's correct`) — in genuine correction or confirmation contexts these may belong; show the full exchange and ask
- `sophisticated` — confirm if the document names the specific technical complexity; remove if used as vague praise
- `optimal` / `optimize` — confirm if a measurable criterion is stated; remove if used loosely ("the optimal approach")
- `hallmark` / `cornerstone` / `bedrock` — confirm if the document names what the trait enables or what breaks without it; remove if used as rhetorical elevation
- Assertion intensifiers (`without question`, `undeniably`) — confirm if supporting evidence appears in the same paragraph; remove if used as bluster
- Anticipatory patterns (`You might be wondering`) — flag only in prose; acceptable in FAQ sections where it introduces a listed question
- `best practices` — sometimes the appropriate term for the domain
- Self-referential phrases that may be intentional (e.g., a disclaimer section)
- Rhetorical question-answer pairs — show the question and immediate answer; offer to merge into a single declarative sentence
- Contrast structures (`It's not X, it's Y` / `Not A. Not B. But C.`) — show the sentence; rewrite as a plain positive statement
- Vague authority (`experts say`, `many believe`, `industry reports`) — remove the attribution entirely and state the claim directly, or cut the sentence if there is no specific source
- Importance sentences — any sentence whose only purpose is to state impact, legacy, significance, or broader trends without a specific claim; delete it
- Sentences over 16 words — show the sentence and a shorter rewrite; confirm before applying
- Universal sentences — any sentence that could apply to 1,000 other topics without modification; delete it
- Motivational tone — sentences written for an audience of many (TED Talk register, preaching, "you can do this" energy); rewrite for one reader or delete
- Any sentence where the replacement changes meaning or register

Example prompt:
```
L3: "Certainly, the migration requires three steps."
     → "The migration requires three steps."
Apply? (y/n/edit)
```

## Step 6 — Report

After all edits:

```
remove-ai-tells complete — docs/report.md

AI-written estimate: 14% → 0% (10 flagged lines resolved out of 72 non-blank lines)

Fixed automatically (8):
  utilize → use (×2)
  delve into → examine (×1)
  Furthermore, → [removed] (×2)
  It's worth noting that → [removed] (×1)
  seamless → [removed] (×1)
  robust → [removed] (×1)

Confirmed by user (2):
  L3  filler opener removed
  L47 filler opener removed

Skipped (0):
  none

Remaining AI tells: 0
```

## Rewrite Output Rules

These rules govern the text produced by the rewrite — not the skill's report.

- Output the clean version only — no explanation of what changed inline
- No formatting tricks: no bold to highlight fixes, no italics for emphasis, no `~~strikethrough~~`
- No summary or commentary appended after the rewritten text
- Write for one reader, not an audience — direct address, not stage register
- If a general claim has no specific backing, delete the sentence rather than hedging it

## Edge Cases

- **Non-doc files**: If the target is a code file, warn that this skill targets human-readable prose, not source code
- **Technical writing where "robust" is accurate**: If context clearly justifies the word (e.g., "RFC 9293 defines robust error recovery"), skip it and note why
- **"Comprehensive" in scope statements**: If the document explicitly lists everything it covers, `comprehensive` may be accurate — confirm before removing
- **"Tailored" describing real customization**: If the sentence names what was customized and for whom, it is not an AI tell — skip and note why
- **"Navigate" in UI/routing context**: Legitimate in technical docs describing navigation components or routing logic — skip
- **Rhetorical questions in FAQs**: Question-answer pairs are the expected format in FAQ sections — do not flag them
- **"Innovative" in product names or official titles**: Skip if part of a proper noun (e.g., "AWS Innovative Partner Program")
- **"Vital" with named consequence**: If the sentence names what breaks when the step is skipped, `vital` may be accurate — confirm before removing
- **"Scalable" with a cited measurement**: If the sentence names a specific scale target (e.g., "scalable to 10,000 concurrent users"), skip it
- **"Disruptive" naming a specific incumbent**: If the sentence names what is being replaced (e.g., "disruptive to legacy on-prem deployments"), it is not vague — confirm before removing
- **"Drive" with a measurable outcome**: If a metric or mechanism is named ("drive a 30% reduction in build time"), it is not a vague AI claim — skip
- **"Here are N ways/steps/tips" in tutorials**: This structure is appropriate in step-by-step guides; flag only in prose sections that could be written as paragraphs
- **Bold overuse in reference docs**: Tables and reference pages legitimately bold terms for quick scanning; flag only in prose paragraphs where bolding exceeds one in ten lines
- **"Accelerate" with a cited metric**: If a specific rate or deadline is named ("accelerate delivery from 6 to 3 weeks"), it is not vague — skip
- **"Ecosystem" naming specific members**: If the sentence lists the actual tools or teams ("the Node.js ecosystem: npm, Webpack, Jest"), it is not vague — skip
- **"As such" as a logical connector**: When a clear cause-effect chain is present in the same sentence, `as such` is legitimate — confirm before removing
- **"The best way to" backed by evidence**: If the next sentence provides a specific reason or benchmark, the superlative may be justified — confirm
- **"Pro tip" / "Quick tip" in genuine how-to guides**: These labels are idiomatic in tutorial writing; flag only when they precede generic advice that adds no specifics
- **"Optimize" in technical contexts**: Legitimate in engineering docs referring to specific performance work ("optimize the SQL query", "optimize bundle size") — skip when a concrete target is named
- **"Sophisticated" describing genuine technical complexity**: If the sentence lists the specific components or interactions that make something complex, it is not vague praise — skip
- **"Hallmark" / "cornerstone" in brand or standards documents**: These are idiomatic in formal organizational writing; confirm before removing rather than auto-removing
- **Anticipatory patterns in FAQ sections**: `You might be wondering` is the expected format when explicitly introducing a FAQ entry — skip; flag only in prose paragraphs
- **"Revolutionary" / "pioneering" with cited firsts**: If the sentence names what was done first and when, it is not vague — confirm before removing
- **"Unprecedented" with cited comparison**: If the sentence names the previous record or baseline being surpassed, it is not vague — confirm before removing
- **"Let me clarify" / "Allow me to" after a genuine misunderstanding**: In dialogue or correction contexts these are appropriate — confirm before removing
- **"As you may know" when knowledge cannot be assumed**: If the document is genuinely unsure whether the reader knows a prerequisite, this hedge is appropriate — confirm before removing
- **"Rest assured" in warranty or SLA language**: Standard in formal contractual writing — skip
- **"To put it another way" when the restatement adds genuine value**: If the second formulation is meaningfully different (e.g., a concrete example after an abstract statement), it may stay — confirm
- **Assertion intensifiers backed by data**: If `without question` or `undeniably` is followed in the same sentence by a cited fact or measurement, it may be intentional emphasis — confirm
- **"Crystal clear" / "abundantly clear" in instructional docs**: If the sentence contrasts a previously confusing step with a clarified one, `crystal clear` may convey a meaningful degree — confirm before removing
- **"The good news is" in genuinely mixed-finding reports**: When the document presents both positive and negative outcomes in a structured comparison, this framing may be deliberate — confirm before removing
- **"In the next section" in long reference documents**: Navigation aids are legitimate in technical reference docs with 10+ sections; flag only in prose articles where headings already serve that purpose
- **"I encourage you to" in call-to-action or closing sections**: In formal recommendation documents or closing remarks, this register may be appropriate — confirm before removing
- **"Arguably the most" backed by a comparison**: If the sentence names the alternatives being compared, the hedge is honest — confirm before removing rather than auto-removing
- **Template phrasing in marketing copy**: Phrases like `the future of X` or `from X to Y` may be intentional brand language; confirm before rewriting and prefer specificity over blanket deletion
- **"When it comes to" in contrastive writing**: If the phrase introduces a real comparison between domains, rewrite only when a direct subject would be clearer
- **Wordiness patterns in quotations**: Do not rewrite quoted speech or cited text, even if it contains flagged circumlocutions
- **Non-English content**: Detect via charset/content check; report that patterns are English-only and skip
- **Large files (>500 lines)**: Process in sections; report progress per section
- **Multiple files**: Process each file independently; report a combined summary at the end
- **Legitimate uses of flagged words**: When a flagged word appears in a quote, code block, or heading that is intentionally citing AI output, skip it
