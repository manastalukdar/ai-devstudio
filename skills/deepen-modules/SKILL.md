---
name: deepen-modules
description: Surface architectural deepening opportunities — find shallow modules and refactor them into deep ones using precise vocabulary (module, seam, adapter, depth, leverage, locality). Use when refactoring architecture, reducing coupling, or improving testability.
disable-model-invocation: false
risk: safe
---

# Deepen Modules

Find shallow modules and refactor them into deep ones that concentrate complexity behind simple, stable interfaces.

Arguments: `$ARGUMENTS` - path or component to analyze, or blank to scan the whole codebase

## Vocabulary (use consistently)

| Term | Definition |
|---|---|
| **Module** | Anything with an interface and implementation — function, class, package, or slice (scale-agnostic) |
| **Interface** | Everything callers must know: types, invariants, error modes, ordering, config, performance facts |
| **Depth** | Leverage at the interface — deep = high leverage (small interface, large hidden implementation) |
| **Seam** | Where an interface lives; a place where behavior can be altered without editing in place |
| **Adapter** | A concrete thing satisfying an interface at a seam |
| **Leverage** | What callers gain from depth |
| **Locality** | What maintainers gain from depth — change, bugs, and knowledge concentrated in one place |

**Deletion test**: Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.

**Seam rule**: One adapter = hypothetical seam. Two adapters = real seam. Don't introduce a port unless at least two adapters are justified.

## Behavior

### Phase 1: Explore

```bash
# Check for existing domain docs to respect
ls CONTEXT.md docs/adr/ 2>/dev/null

# Find shallow module signals
grep -rn "^export function\|^export const\|^class " . \
  --include="*.ts" --include="*.py" --include="*.js" \
  -l 2>/dev/null | grep -v node_modules | head -20

# Find pass-through patterns (thin wrappers)
grep -rn "return.*\." . --include="*.ts" --include="*.py" \
  2>/dev/null | grep -v node_modules | head -10
```

Walk the codebase organically. Note friction: places where understanding requires bouncing between multiple files, where callers duplicate logic, where modules expose their internals.

### Phase 2: Present Candidates

Deliver a numbered list. For each opportunity:

```
## Candidate 1: [Module Name]

**Files**: src/auth/tokenValidator.ts, src/middleware/auth.ts
**Problem**: TokenValidator exposes 4 internal methods callers combine in different orders — shallow interface, no invariants enforced
**Solution**: Single `validate(token): Result<Claims, AuthError>` that encapsulates the combination logic
**Benefits**: Callers can't mis-sequence; error handling centralized; testable via one seam
**Depth gain**: 4-method interface → 1-method interface; same capability
```

Use domain vocabulary from `CONTEXT.md` if it exists. Do not propose interface designs yet — just present candidates.

### Phase 3: Classify Dependencies for Each Candidate

For each candidate, classify its dependencies to determine the safe deepening path:

**1. In-process** — pure computation, in-memory state, no I/O
→ Merge modules and test through the new interface directly. No adapter needed.

**2. Local-substitutable** — dependencies with local test stand-ins (PGLite for Postgres, in-memory filesystem)
→ Deepenable. Test with the stand-in running in the test suite. Seam is internal.

**3. Remote but owned** (Ports & Adapters) — your own services across a network boundary
→ Define a port (interface) at the seam. Deep module owns the logic; transport is injected as an adapter. Tests use in-memory adapter. Production uses HTTP/gRPC adapter.

**4. True external** — third-party services (Stripe, Twilio, etc.)
→ Deepened module takes the external dependency as an injected port. Tests provide a mock adapter.

### Phase 4: Design Loop

For the chosen candidate:
- Propose the new interface
- Discuss trade-offs
- Update `CONTEXT.md` with any new terms that emerge
- Offer an ADR if the decision is hard to reverse and non-obvious
- Write the new tests at the module's interface — tests describe behavior through the public API, not internal state

**Test discipline during deepening:**
- Old unit tests on shallow modules become waste once the deepened interface is tested — delete them
- New tests assert observable outcomes through the new interface
- Tests survive internal refactors — they describe behavior, not implementation

## Examples

```
/deepen-modules src/payments/
/deepen-modules          ← scan whole codebase
/deepen-modules "the auth middleware feels wrong"
```

## Sample Output

```
Found 3 deepening opportunities:

1. PaymentProcessor (HIGH) — 6-method interface wrapping Stripe; collapse to process(intent) + refund(id)
2. UserRepository (MED) — duplicated query logic across 4 callers; extract into findBy(criteria) deep module
3. EmailService (LOW) — thin wrapper, but only one adapter exists → hypothetical seam, defer

Recommend starting with #1. Dependency: true external (Stripe) → ports & adapters pattern.
Proceed?
```

## Token Optimization

**Expected range**: 500–2,500 tokens (full scan), 300–800 tokens (targeted path)

**Grep-before-Read**: Finds module boundaries and shallow patterns via grep before reading full files.

**Early exit**: If a targeted path is given, scopes analysis to that path only — avoids whole-codebase walk.

**Patterns used**: Grep-before-Read, early exit, progressive disclosure (candidates list → design loop on selection)
