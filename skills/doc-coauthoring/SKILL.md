---
name: doc-coauthoring
description: Structured 3-stage co-authoring workflow for proposals, technical specs, decision docs, and RFCs — context gathering, section-by-section refinement, reader testing
disable-model-invocation: false
risk: none
---

# Document Co-Authoring

A structured workflow for writing documentation that survives a reader who wasn't in the room. Covers proposals, technical specs, decision docs, ADRs, and RFCs.

## Usage

`/doc-coauthoring [document type and topic]`

## Stages

The user can skip any stage by saying so. Ask which stages to run if the request is ambiguous.

---

### Stage 1 — Context Gathering

**Goal**: Understand what the document needs to accomplish before writing a word.

Ask:
1. What type of document is this? (proposal, spec, decision doc, RFC, report)
2. Who is the primary reader? What do they already know?
3. What should the reader do or decide after reading?
4. What's the deadline and distribution? (internal, public, narrow team)
5. What constraints exist? (length, format, confidentiality, prior decisions to respect)

Then ask the user to dump their background: notes, context, prior discussion. Ask 5–10 clarifying questions based on what they share. Do not start writing until the answers are clear.

If connected tools can pull in additional context (meeting notes, linked issues, prior docs), confirm with the user before fetching.

---

### Stage 2 — Refinement & Structure

**Goal**: Build the document one section at a time, with the user in control of structure.

**For each section:**

1. Propose 3–5 section titles based on the document type. Ask the user to keep, remove, rename, or add.
2. For each confirmed section, ask 2–4 targeted clarifying questions about that section's content.
3. Draft the section.
4. Refine through targeted edits — use `str_replace` style edits, not full reprints.

**Do not reprint the entire document** after each edit. Edit in place.

**Near the end**, re-read the full document and check for:
- Flow: does each section lead naturally to the next?
- Redundancy: is the same point made in multiple places?
- Filler: vague sentences that don't add information
- Tone consistency: does it read as one voice throughout?

---

### Stage 3 — Reader Testing

**Goal**: Verify the document answers the questions a reader would actually ask.

1. From the document, generate 5–10 questions a reader with no prior context would ask.
2. Answer each question using only the document text.
3. Where the answer is incomplete or wrong → identify the gap → offer a fix.

**If sub-agents are available**: Run the reader test using a fresh sub-agent with no conversation context. Hand it only the document. Ask it to answer the questions cold.

**If sub-agents are not available**: Give the user a prompt to run in a new conversation:
> "You are a first-time reader of this document. Answer the following questions using only the text I'm about to share. [paste document] [paste questions]"

The document passes when the fresh reader answers correctly and raises no new significant gaps.

---

## Final Checklist

Before calling the document done, confirm:

- [ ] Primary reader's question is answered directly
- [ ] Decision or action requested is stated explicitly
- [ ] No section assumes context not in the document
- [ ] All acronyms defined on first use
- [ ] Appendices contain supporting detail that would interrupt the main flow

## Tips

- Link this conversation in an appendix for readers who want the reasoning behind choices
- The user should do their own read-through and fact-check — Claude cannot verify external facts
- If a section stays contentious across multiple edits, flag it as "open question" and move on

## Token Optimization

**Expected range**: 800–3,000 tokens per stage (Stage 1 cheapest, Stage 3 most expensive with sub-agents)

**Early exit**: Skips stages the user explicitly opts out of.

**Patterns used**: Progressive disclosure (one section at a time), git diff scope equivalent (edit in place, not full reprints)
