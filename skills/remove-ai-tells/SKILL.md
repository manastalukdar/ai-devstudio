---
name: remove-ai-tells
description: Detect AI-generated writing patterns in documents — reports filler openers, AI closers, hedge phrases, cliché transitions, template phrasing, AI vocabulary, rhetorical question-answer pairs, and overused intensifiers with a per-document AI-written percentage, then asks before removing anything.
disable-model-invocation: false
---

# Remove AI Tells

I'll scan a document for patterns that signal AI-generated writing, report what was found and what percentage of the document reads as AI-written, then ask before making any changes.

## Token Optimization

**Expected range**: 400–900 tokens (detection + report), 50–100 tokens (early exit when file is clean), 600–1,500 tokens (detection + removal)

**Patterns used**: Grep-before-Read, early exit, progressive disclosure, git diff scope default

**Early exit**: If none of the grep patterns match, report "No AI tells found" and stop immediately.

**Two-phase design**: Detection (Steps 1–3) always runs cheaply. Removal (Steps 5–6) only runs after user confirms in Step 4.

## Step 1 — Identify Target File(s)

Resolution order — use the first that yields a valid file:

1. **Explicit argument** — `/remove-ai-tells docs/report.md`
2. **IDE active file** — if `<ide_opened_file>` has a doc extension (`.md`, `.txt`, `.rst`, `.adoc`) and no argument was given, use it.
3. **Staged doc files** — any staged files with a doc extension.
4. **Ask** — if none of the above yield a target, prompt the user.

```bash
declare -a TARGETS

if [[ -n "$ARGUMENTS" ]]; then
    read -r -a TARGETS <<< "$ARGUMENTS"
elif [[ -n "$IDE_ACTIVE_FILE" ]] && echo "$IDE_ACTIVE_FILE" | grep -qE '\.(md|txt|rst|adoc)$'; then
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

# Filler openers and padding openers
run_check "Openers" "^(Certainly|Absolutely|Of course|Sure,|Great!|Excellent!|Awesome|Wonderful|Totally!|Noted!|Perfect!|Interesting!|Fantastic!|Exactly!|Indeed,|Naturally,|Obviously,|Clearly,|In other words,|To put it simply,|Simply put,|In essence,|Essentially,|Basically,|Ultimately,|Overall,|Most importantly,|Above all,|The good news (is|here)|The bad news (is|here)|Having (established|covered|discussed) that|Now that we.?ve (established|covered|discussed|looked at)|Here are [0-9]+ (ways?|steps?|tips?|reasons?|things?|examples?|points?)|(Pro tip|Quick tip)[: ]|(You might be wondering|You may be (wondering|asking yourself)|You'?re probably wondering|As you (may|might|probably) (already )?know,|You may have noticed|Chances are,))[,!.]?"

# Great question, validation, AI closers, self-referential
run_check "Validation & closers" "(Great question[!.]?|That'?s (a )?(great|excellent|good) question|Thank(s| you) for (your question|asking)[.!]?|You'?re (absolutely |completely )?(right|correct)[.!,]|That'?s (absolutely |completely )?correct[.!,]|I hope (this (helps|clarifies|answers)|that (helps|answers)|you found this (helpful|useful))|Hope this helps|I trust this helps|Let me know if you (have any questions|need (anything|further|more))|Is there anything else (I can|you'?d like)|If you have any questions,? feel free to|Happy to (help|clarify|answer)|As an AI|As a language model|As your assistant|I('m| am) here to help|Feel free to (ask|reach out)|Don't hesitate to|I'?d be (happy|glad|delighted) to|[Ll]et me walk you through|I'?ll walk you through|I want to assure you|I'?m (excited|pleased|delighted) to (share|tell|show|present)|Allow me to (explain|walk|show|clarify|demonstrate)|Let me (clarify|explain|break (this|it) down)|Let'?s (explore|examine|break down|get started|dive in|begin)|I'?ll (begin|start) by|We'?ll (cover|explore|look at|discuss|examine)|I (encourage|invite|urge) you to)"

# Hedging phrases and transition clichés
run_check "Hedging & transitions" "(It('s| is) (worth|important) (noting|to note|mentioning|considering|emphasizing|pointing out)|Please note that|It should be noted|It is (important|essential|critical) to (note|mention|understand|remember)|needless to say|To be (fair|honest|clear|precise),|Just to (clarify|be clear),|[Aa]s (I |we )?(mentioned|noted|discussed) (earlier|above|before)|[Kk]eep in mind that|[Bb]ear in mind that|I should (note|mention)|[Ww]orth (mentioning|pointing out)|I'?d like to (point out|highlight|note|emphasize)|I want to (highlight|emphasize)|\b(Moreover,|Furthermore,|Additionally,|In addition,|In conclusion,|In summary,|That being said,|That said,|With that in mind,|With th(is|at) in mind,|With that said,|Having said that,|At the end of the day,|It goes without saying|First and foremost,|Last but not least,|To summarize,|To recap,|In a nutshell,|On that note,|To that end,|As such,|In light of (this|that),|Moving forward,|Going forward,|On a related note,|On the flip side,|Suffice it to say,|All things considered,|By the same token,|To put it another way,|In any case,|Nonetheless,|Nevertheless,|Not only that,|In other words,|Despite this)\b|It'?s not .+, it'?s|Not [A-Z][^.]+\. Not [A-Z])"

# Template phrasing and structural scaffolding
run_check "Template phrasing" "\b(In today'?s .{0,40} (world|landscape|environment|era)|in an era where|now more than ever|when it comes to|at its core|the reality is|the truth is|not just [^,.;]+, but|more than just|isn'?t just [^,.;]+, it'?s|whether you'?re (a )?[^,.;]+ or|from [^,.;]+ to [^,.;]+|there are several reasons why|let'?s take a closer look|ultimately, the choice depends on|the future of [^,.;]+ is|The key takeaway(s)?[: ]|if you.?re like most (people|developers?|users?|teams?|companies|organizations)|you.?ve probably (heard|seen|noticed|experienced|come across)|This is where .{1,40} comes in|That'?s where .{1,40} comes in|in (the )?(next|following|upcoming) section|as we.?ll see (below|later|above)|as (discussed|mentioned|noted|covered) (in )?(the )?(previous|next|following) section)\b"

# AI vocabulary — all overrepresented LLM terms in one pass
run_check "AI vocabulary" "\b(delve|dive into|unpack(ing)?|leverage[sd]?|utilize[sd]?|facilitate[sd]?|robust(ness)?|seamless(ly)?|holistic(ally)?|synergy|synergize|cutting.?edge|state.?of.?the.?art|groundbreaking|transformative|revolutionize|unlock(ing)?|foster(ing)?|empower(ing)?|best practices|pivotal|crucial|enhance[sd]?|underscore[sd]?|landscape|vibrant|testament|showcase[sd]?|intricate(ly)?|evolving|nuanced?|comprehensive|meticulous(ly)?|paramount|streamline[sd]?|actionable|harness(ing|ed)?|game-?changer|game-?changing|innovative|innovation|tailored|invaluable|endeavou?r(ing|ed)?|aforementioned|noteworthy|commendable|multifaceted|sophisticated|optimal(ly)?|optimize[sd]?|hallmark|cornerstone|bedrock|best-in-class|world-class|top-?tier|unprecedented|revolutionary|visionary|pioneering|propel(ling|led)?|catalyze[sd]?|catalyst|amplify|amplified|amplifying|bolster(ing|ed)?|spearhead(ing|ed)?|champion(ing|ed)?|synergistic|paradigm( shift)?|ecosystem|impactful|vital|scalable|scalability|elevate[sd]?|reimagine[sd]?|redefine[sd]?|disruptive|disrupt(ing|ed)?|pave the way|at the forefront|drive[sd]? (results?|innovation|growth|success|change|impact|value|adoption|engagement)|accelerate[sd]?|impact|legacy|significance|plays? a (pivotal|crucial|key|vital) role)\b"

# Vague authority, assertion intensifiers, hollow superlatives
run_check "Vague authority & intensifiers" "(experts? say|experts? (argue|suggest|agree|believe|note)|according to experts?|many experts? (say|believe|suggest)|industry reports?|as per (industry|expert) (standards?|guidelines?|consensus)|many believe|some argue that|it could be argued that|one could argue|studies show|research (shows|suggests|indicates)|data (shows|suggests|indicates)|it is (widely|generally|commonly) (believed|accepted|known|recognized|understood)|conventional wisdom|it has been shown that|it is (recommended|expected|suggested) that|general(ly accepted)? consensus|\b(without (question|a doubt)|there'?s no denying (that|this)|undeniably|unquestionably|it'?s no secret that|make no mistake|rest assured|highly (recommended|effective|relevant|valuable|efficient|useful|important|beneficial)|crystal clear|abundantly clear|perfectly clear|arguably (the |one of the )?(most|best)|perhaps the (most|best)|the best way to|the most important (thing|step|aspect|consideration)|the only way to|one of the most (important|effective|powerful|significant|compelling|critical))\b)"

# Wordiness — circumlocutions
run_check "Wordiness" "\b(in order to|due to the fact that|at this point in time|in the event that|with (regard|respect) to|the fact that|prior to|make use of|a (number|wide range|variety|great deal) of|is able to|has the ability to|it is possible to|as a result of|take into (consideration|account)|on a regular basis|in the case of|in spite of the fact that|in the near future|at a later (date|time)|subsequent to|for the purpose of|on the basis of|with the exception of|in the majority of cases|in terms of|in light of the fact that|owing to the fact that)\b"

# Rhetorical question-answer pairs
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
        printf '%s: %s bolded line(s) across %s non-blank lines (possible over-formatting)\n' \
            "$target" "$bold_lines" "$total_lines" | tee -a "$FINDINGS_FILE"
    fi
done

# Em dash overuse
for target in "${TARGETS[@]}"; do
    dash_count=$(grep -o "—" "$target" | wc -l | tr -d ' ')
    total_lines=$(grep -c . "$target" || echo 1)
    if (( dash_count > total_lines / 30 && dash_count > 1 )); then
        printf '%s: %s em dash(es) across %s non-blank lines\n' \
            "$target" "$dash_count" "$total_lines" | tee -a "$FINDINGS_FILE"
    fi
done
grep -HnE ".+—.+—" "${TARGETS[@]}" | tee -a "$FINDINGS_FILE" || true

# Right arrow overuse in prose
grep -Hn "→" "${TARGETS[@]}" | tee -a "$FINDINGS_FILE" || true

# Section separator overuse
grep -HnE "^---$" "${TARGETS[@]}" | tee -a "$FINDINGS_FILE" || true
```

If zero matches across all patterns, output:

```
No AI tells found in <file>. Document reads naturally.
```

and stop.

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
  ...

Total: 12 patterns across 1 file
```

### AI-Written Percentage

```bash
for target in "${TARGETS[@]}"; do
    total_lines=$(grep -c . "$target" || echo 1)
    hit_lines=$(
        awk -F: -v file="$target" '$1 == file && $2 ~ /^[0-9]+$/ { print $2 }' "$FINDINGS_FILE" |
        sort -u | wc -l | tr -d ' '
    )
    percentage=$(( (hit_lines * 100 + total_lines / 2) / total_lines ))
    printf '%s: %s%% (%s flagged lines out of %s non-blank lines)\n' \
        "$target" "$percentage" "$hit_lines" "$total_lines"
done
```

```
AI-written estimate: 17% (12 flagged lines out of 72 non-blank lines)
  Low (0–15%)    — occasional AI patterns; targeted fixes sufficient
  Medium (16–40%) — noticeable AI register; consider paragraph rewrites
  High (41%+)    — pervasive AI tone; consider full-section rewrites
```

## Step 4 — Ask Before Removing

```
Proceed with removal? Options:
  y   — apply all automatic fixes, then prompt for confirmation-required ones
  n   — exit without changes
  l   — list only (you already see the list above; this exits without changes)
  s   — selective: choose which categories to fix
```

Wait for the user's response. Do not apply any edits until the user confirms with `y` or `s`.

If the user chooses `s`, present each category in turn and proceed only with approved categories.

## Step 5 — Apply Fixes

### Automatic replacements

**Remove entirely** — the sentence is always better without these phrases. Delete the phrase and any punctuation or space it introduces:

- *Filler openers*: `Certainly,` `Absolutely,` `Of course,` `Sure,` `Great!` `Excellent!` `Awesome,` `Wonderful,` `Totally!` `Noted!` `Perfect!` `Interesting!` `Fantastic!` `Exactly!` `Indeed,` `Naturally,` `Obviously,` `Clearly,`
- *Validation openers*: `Great question!` `That's a great question` `Thank you for your question` `Thanks for asking` `You're right,` `You're absolutely right,` `That's correct,` — just answer directly.
- *AI closers*: `I hope this helps` `Hope this helps` `I trust this helps` `Let me know if you have any questions` `Let me know if you need anything` `Is there anything else I can help with` `Happy to help` `Happy to clarify` `I hope you found this helpful`
- *Transition openers*: `Moreover,` `Furthermore,` `That being said,` `That said,` `With that in mind,` `With that said,` `Having said that,` `On that note,` `To that end,` `In light of this/that,` `With this in mind,` `All things considered,` `By the same token,` `In any case,` `At the end of the day,` `Moving forward,` `Going forward,` `On a related note,` `Not only that,` `In conclusion,` `In summary,` `To summarize,` `To recap,` `In a nutshell,` `First and foremost,` `Last but not least,` — for `Nonetheless,` / `Nevertheless,` / `Despite this,` rewrite as two plain sentences or use `but`.
- *Hedging phrases*: `It's worth noting that` `It is worth/important noting/mentioning/considering` `It is important/essential to note/mention` `It should be noted that` `needless to say` `To be fair/honest/clear,` `As I mentioned earlier/above/before` `Keep in mind that` `Bear in mind that` `I should note/mention` `Worth mentioning/pointing out` `I'd like to point out/highlight` `I want to highlight/emphasize` — just state the thing directly.
- *Self-referential*: `Let me walk you through` `I'll walk you through` `Allow me to explain/clarify` `Let me clarify/explain/break this down` `Let's explore/examine/break down/dive in/get started` `I'll begin by` `I'll start by` `We'll cover/explore/look at` `I want to assure you` `I'm excited to share` `I'm pleased to present` `Feel free to ask` `Don't hesitate to` `I'd be happy to` `I encourage/invite/urge you to` — just start the explanation.
- *Anticipatory patterns*: `You might be wondering` `You may be asking yourself` `As you may know,` `As you probably know,` `You may have noticed` `Chances are,` `if you're like most people/developers` `you've probably heard/seen/noticed`
- *Template scaffolding*: `now more than ever` `At its core,` `The reality is` `The truth is` `Let's take a closer look` `Most importantly,` `Above all,` `The good news is` `The bad news is` `Having established that,` `Now that we've established/covered` `in the next/following section` `as we'll see below/later` `as discussed/mentioned in the previous section` `This is where [X] comes in`
- *Assertion intensifiers*: `without question` `without a doubt` `there's no denying that` `undeniably` `unquestionably` `it's no secret that` `make no mistake` `rest assured`
- *Hollow superlatives*: `the best way to` `the most important [thing/step/aspect]` `the only way to` `one of the most important/effective/powerful/significant` — state the approach directly.
- *Vague authority*: `some argue that` `it could be argued that` `one could argue` `it is widely/generally believed` `conventional wisdom` `it has been shown that` `according to experts` `many experts believe` — state the claim directly or attribute to a named source.
- *Padding openers*: `In other words,` `To put it simply,` `Simply put,` `In essence,` `Essentially,` `Basically,` `Ultimately,` `Overall,`
- *Labels*: `Pro tip:` `Quick tip:` — remove the label, keep the tip text.
- *Intensifiers*: `highly recommended` → `recommended`. `highly effective/relevant/valuable` → drop `highly`. `crystal clear/abundantly clear/perfectly clear` → `clear`.

**Shorten circumlocutions** — meaning is always identical:

| Wordy | Short |
|---|---|
| `in order to` | `to` |
| `due to the fact that` / `in light of the fact that` / `owing to the fact that` | `because` |
| `as a result of` | `because of` |
| `in the event that` | `if` |
| `in spite of the fact that` | `although` |
| `at this point in time` | `now` |
| `in the near future` | `soon` |
| `at a later date/time` | `later` |
| `subsequent to` | `after` |
| `prior to` | `before` |
| `for the purpose of` | `to` |
| `on the basis of` | `based on` |
| `with the exception of` | `except` |
| `in the majority of cases` | `usually` |
| `on a regular basis` | `regularly` |
| `in the case of` | `for` / `when` |
| `make use of` | `use` |
| `is able to` / `has the ability to` | `can` |
| `it is possible to` | `you can` |
| `take into consideration/account` | `consider` |
| `with regard/respect to` | `about` |
| `a number of` | `several` |
| `a wide range/variety of` | `many` |
| `Additionally,` / `In addition,` | `Also,` |
| `in terms of` | *(rewrite with a concrete verb)* |
| `the fact that` | *(restructure as a direct clause)* |

**Replace with simpler word**:

| Inflated | Replacement |
|---|---|
| `utilize` | `use` |
| `leverage` (verb) | `use` / `apply` |
| `facilitate` | `help` / `enable` |
| `delve` / `dive into` / `unpack` | `look at` / `examine` / `explore` |
| `spearhead` | `lead` / `run` |
| `champion` (verb) | `support` / `advocate for` |
| `endeavor` / `endeavour` | `try` / `work` / `aim` |
| `aforementioned` | `this` / `the` / *(repeat the noun)* |
| `showcase` | `show` / `demonstrate` |
| `underscore` (verb) | `show` / `confirm` |
| `please note that` | `Note:` |
| `holistic` | `end-to-end` / `full` |
| `paramount` | `critical` / `required` |
| `actionable` | *(remove — "actionable steps" → "steps")* |

**Vague praise — name the specific quality or remove**. Do not keep the word; either delete it or replace it with what is specifically true:

`robust` `seamless` `comprehensive` `meticulous` `sophisticated` `nuanced` `innovative/innovation` `cutting-edge` `state-of-the-art` `groundbreaking` `transformative` `streamline` `enhance` `elevate` `reimagine` `redefine` `disruptive` `game-changing` `harness (the power of)` `pivotal` `crucial` `vital` `impactful` `invaluable` `noteworthy` `commendable` `multifaceted` `vibrant` `intricate` `hallmark` `cornerstone` `bedrock` `best-in-class` `world-class` `top-tier` `unprecedented` `revolutionary` `visionary` `pioneering` `propel` `catalyze/catalyst` `amplify` `bolster` `synergistic` `paradigm shift` `ecosystem` `scalable/scalability` `optimal/optimize` `landscape` `testament` `evolving` `tailored` `best practices` `drive [vague object]` `pave the way` `at the forefront` `foster` `empower` `accelerate [vague]`

### Confirmation-required replacements

Show the current line and proposed rewrite; wait for user response before changing:

- **Filler and validation openers** — show the full sentence; removing the opener must not change meaning.
- **AI closers** — show the paragraph end; confirm removal doesn't cut real content.
- **Template phrasing** (`In today's…`, `from X to Y`, `the future of X`, `whether you're X or Y`) — show the sentence and offer a direct rewrite that names the actual subject.
- **Em dashes** — show each occurrence in context; replace with a comma, colon, or parentheses, or remove the clause if it is padding. Flag files where em dashes appear more than once per 30 lines as likely overused.
- **`→` arrows** — legitimate in code examples, tables, or CLI output; overused in prose as a connector. Remove from prose and rewrite as a complete sentence.
- **`---` section separators** — flag standalone horizontal rules; remove and rely on headings. Skip occurrences inside YAML front matter or code fences.
- **Wordiness patterns** — auto-replacements are always safe, but show the rewritten sentence so the user can verify no meaning was lost.
- **Bold overuse** — show a count of bolded phrases per page; ask which to remove.
- **Context-dependent AI vocabulary** (see Edge Cases below for which words) — show the sentence and ask.
- **Rhetorical question-answer pairs** — show the question and immediate answer; offer to merge into a single declarative sentence.
- **Contrast structures** (`It's not X, it's Y` / `Not A. Not B. But C.` / `Despite this,`) — show the sentence; rewrite as a plain positive statement.
- **Vague authority** — remove the attribution and state the claim directly, or cut the sentence if there is no specific source.
- **Importance sentences** — any sentence whose only purpose is to state impact, legacy, significance, or broader trends without a specific claim; delete it.
- **Sentences over 16 words** — show the sentence and a shorter rewrite.
- **Universal sentences** — any sentence that could apply to 1,000 other topics; delete it.
- **Motivational tone** — sentences written for an audience of many (TED Talk register); rewrite for one reader or delete.

Example prompt:
```
L3: "Certainly, the migration requires three steps."
     → "The migration requires three steps."
Apply? (y/n/edit)
```

## Step 6 — Report

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

- Output the clean version only — no explanation of what changed inline
- No formatting tricks: no bold to highlight fixes, no italics, no `~~strikethrough~~`
- No summary or commentary appended after the rewritten text
- Write for one reader, not an audience — direct address, not stage register
- If a general claim has no specific backing, delete the sentence rather than hedging it

## Edge Cases

Eight principles cover all context-dependent situations:

1. **Named specifics override the flag.** If a flagged term is followed in the same sentence by a specific metric, named comparison, or enumerated list — confirm before removing rather than auto-removing. Examples: `drive` with a cited percentage, `accelerate` with a deadline, `ecosystem` listing actual tools, `scalable` with a stated scale target, `disruptive` naming a specific incumbent, `arguably` with alternatives listed, `the best way to` with a cited benchmark in the next sentence.

2. **Technical/domain context is legitimate.** Skip and note the reason: `navigate` in UI/routing docs; `optimize` with a named performance target; `robust` in an RFC or protocol specification; `sophisticated` naming the specific technical components; `comprehensive` in a scope statement that explicitly lists what is covered.

3. **Quoted or cited text is never rewritten.** Do not change flagged words inside quotations, cited text, code blocks, or YAML front matter.

4. **Proper nouns and product names are skipped.** Do not flag words that are part of an official product, program, or organization name.

5. **Formal register warrants confirmation, not auto-removal.** `rest assured` in SLAs or warranty language; `hallmark`/`cornerstone` in brand standards or formal organizational writing; `I encourage you to` in a formal recommendation closing; `revolutionary`/`pioneering` with a cited first and date — confirm before removing.

6. **FAQ sections expect anticipatory patterns.** `You might be wondering` is the expected format in explicit FAQ sections — skip; flag only in prose paragraphs. `Here are N steps/tips` is appropriate in step-by-step tutorials — confirm rather than auto-remove.

7. **Logical connectors with explicit cause-effect are legitimate.** `As such,` is valid when a clear cause-effect chain is in the same sentence. `To put it another way` is valid when the second formulation adds a concrete example after an abstract statement. `The good news is` is valid in structured mixed-finding reports. Confirm before removing in these cases.

8. **Non-English content, large files, and multiple files.** For non-English content: report that patterns are English-only and skip. For files over 500 lines: process in sections and report progress per section. For multiple files: process each independently and report a combined summary at the end.
