---
name: domain-context
description: Create and maintain a CONTEXT.md domain glossary and ADRs for the project — establishes shared vocabulary between developers, domain experts, and AI. Use when starting a new project, refining domain language, or resolving terminology ambiguities.
disable-model-invocation: false
risk: safe
---

# Domain Context

Create and maintain the project's domain glossary (`CONTEXT.md`) and architecture decision records (`docs/adr/`).

Arguments: `$ARGUMENTS` - `init` to create from scratch, `update <term>` to add/refine a term, `adr <decision>` to record a decision, or blank to review and improve existing docs

## Behavior

### 1. Detect Existing Structure

```bash
# Check what already exists
ls CONTEXT.md CONTEXT-MAP.md docs/adr/ 2>/dev/null
# Find any domain documentation
find . -name "CONTEXT.md" -not -path "*/node_modules/*" 2>/dev/null | head -5
```

### 2. CONTEXT.md Format

Create or update `CONTEXT.md` at the repo root (or within a bounded context directory for monorepos):

```markdown
# {Context Name}

{One or two sentences: what this context is and why it exists.}

## Language

**Order**:
A customer's request to purchase one or more products.
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account

## Relationships

- An **Order** produces one or more **Invoices**
- An **Invoice** belongs to exactly one **Customer**

## Example Dialogue

> **Dev:** "When a **Customer** places an **Order**, do we create the **Invoice** immediately?"
> **Domain expert:** "No — an **Invoice** is only generated once a **Fulfillment** is confirmed."

## Flagged Ambiguities

- "account" was used to mean both **Customer** and **User** — resolved: these are distinct concepts.
```

**Rules for entries:**
- One preferred term per concept — list others under `_Avoid_`
- One sentence max per definition — what it IS, not what it does
- Only terms specific to this domain — not general programming concepts
- Express relationships with cardinality where obvious
- Include an example dialogue showing terms interacting naturally

### 3. Multiple Bounded Contexts (Monorepos)

When the repo has multiple domains, create `CONTEXT-MAP.md` at root instead:

```markdown
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) — generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md) — manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched`; Billing generates invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

Infer which structure applies from the codebase layout.

### 4. Architecture Decision Records

ADRs live in `docs/adr/` with sequential numbering: `0001-slug.md`, `0002-slug.md`.

Create `docs/adr/` only when the first ADR is needed (lazy creation).

**ADR template** (keep minimal — one paragraph is fine):

```markdown
# {Short title of the decision}

{1–3 sentences: what's the context, what did we decide, and why.}
```

**Only create an ADR when ALL THREE are true:**
1. Hard to reverse — meaningful cost to changing course later
2. Surprising without context — a future reader would wonder "why on earth?"
3. Real trade-off — genuine alternatives existed and one was chosen for specific reasons

**ADR-worthy examples:** architectural shape, integration patterns between contexts, technology choices with lock-in, deliberate deviations from the obvious path, constraints not visible in the code.

**Not ADR-worthy:** obvious choices, easily reversible decisions, things the code already makes clear.

### 5. Updating Inline During Other Skills

When `/grill-me`, `/deepen-modules`, or `/to-prd` resolve terminology:
- Update `CONTEXT.md` immediately with the new term
- Offer an ADR if the decision meets all three criteria above
- Do not create documentation preemptively

### 6. Scan for Terminology Drift

```bash
# Find terms used inconsistently vs CONTEXT.md preferred vocabulary
# Example: if "Order" is preferred, look for usages of avoided aliases
grep -rn "purchase\|transaction" --include="*.md" --include="*.ts" \
  --include="*.py" . 2>/dev/null | grep -v node_modules | head -20
```

Report drift and offer to update CONTEXT.md or the code comments.

## Examples

```
/domain-context init
/domain-context update "Order vs Purchase — settle the terminology"
/domain-context adr "use event sourcing for the Orders aggregate"
/domain-context        ← review and improve existing CONTEXT.md
```

## Token Optimization

**Expected range**: 300–800 tokens (init/update), 100–200 tokens (adr), 200–500 tokens (review)

**Early exit**: If `CONTEXT.md` already exists and no arguments given, reads it and reports gaps — no full rewrite unless explicitly requested.

**Grep-before-Read**: Scans for terminology drift via grep before reading full source files.

**Patterns used**: Grep-before-Read, early exit, template-based generation, lazy file creation
