---
name: ddd-model
description: Apply Domain-Driven Design — identify bounded contexts, model aggregates and value objects, map context relationships, and generate implementation scaffolding
disable-model-invocation: false
risk: safe
---

# Domain-Driven Design Modeling

Map a domain into bounded contexts, aggregates, entities, value objects, and context relationships.

Arguments: `$ARGUMENTS` - domain name or description, or `audit` to assess DDD fitness of existing codebase

## Behavior

### 1. Assess DDD Fitness (when `audit` or no clear domain given)

```bash
# Check size and complexity signals
find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.java" \) \
  -not -path "*/node_modules/*" -not -path "*/.git/*" | wc -l

# Look for existing domain structure signals
find . -type d \( -name "domain" -o -name "entities" -o -name "aggregates" \
  -o -name "repositories" -o -name "services" \) 2>/dev/null | head -10

# Check for anemic domain model anti-patterns
grep -rn "class.*DTO\|class.*Model\b\|class.*Entity" . \
  --include="*.py" --include="*.ts" -l 2>/dev/null | head -10
```

DDD is a good fit when: domain logic is complex, multiple teams work on the same system, or the business rules change frequently. Skip it for CRUD-heavy apps with simple logic.

### 2. Bounded Context Discovery

Ask clarifying questions to identify contexts:
- What are the main business capabilities? (e.g., ordering, inventory, billing)
- Which teams own which parts of the system?
- Where do the same words mean different things? (e.g., "customer" in sales vs. support)
- What are the consistency requirements? (what must change together?)

Output a context map:

```
Domain: E-Commerce Platform
━━━━━━━━━━━━━━━━━━━━━━━━━━

Bounded Contexts:
┌─────────────┐  ACL  ┌─────────────┐  OHS  ┌─────────────┐
│   Catalog   │ ─────▶│   Orders    │ ─────▶│   Billing   │
│             │       │             │       │             │
│ Product     │       │ Order       │       │ Invoice     │
│ Category    │       │ LineItem    │       │ Payment     │
│ Pricing     │       │ Fulfillment │       │ Refund      │
└─────────────┘       └─────────────┘       └─────────────┘
        │                    │
        ▼ Shared Kernel       ▼ Customer Context (upstream)
   [ProductId, Money]    [CustomerId, Address]

Relationships:
- Catalog → Orders: Anti-Corruption Layer (Orders translates Catalog's ProductSnapshot)
- Orders → Billing: Open Host Service (Billing subscribes to OrderPlaced events)
- Customer: Shared upstream — both Catalog and Orders conform to Customer context
```

### 3. Aggregate Design

For each bounded context, define aggregates:

```
Aggregate: Order
├── Root: Order (enforces invariants)
│   - id: OrderId (value object)
│   - status: OrderStatus (enum)
│   - customerId: CustomerId (value object — reference to Customer context)
│   - lines: LineItem[] (child entities)
│   - totalAmount: Money (value object — computed)
│
├── Invariants:
│   - Total = sum of line amounts (always consistent)
│   - Cannot add lines to a shipped order
│   - Must have at least one line item
│
├── Commands (what changes state):
│   - PlaceOrder, AddLineItem, CancelOrder, ConfirmShipment
│
└── Domain Events (what happened):
    - OrderPlaced, OrderCancelled, OrderShipped
```

### 4. Generate Implementation Scaffolding

Detect language and generate appropriate structure:

```bash
# Detect primary language
if [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then LANG="python"
elif [ -f "package.json" ] && grep -q "typescript" package.json 2>/dev/null; then LANG="typescript"
elif find . -name "*.java" -not -path "*/node_modules/*" 2>/dev/null | grep -q .; then LANG="java"
fi
```

**Python scaffold:**
```python
# src/domain/<context>/aggregates/order.py
from dataclasses import dataclass, field
from typing import List
from ..value_objects import OrderId, Money, CustomerId
from ..events import OrderPlaced

@dataclass
class Order:
    id: OrderId
    customer_id: CustomerId
    lines: List["LineItem"] = field(default_factory=list)
    status: str = "draft"

    def place(self) -> "OrderPlaced":
        if not self.lines:
            raise ValueError("Order must have at least one line")
        self.status = "placed"
        return OrderPlaced(order_id=self.id, customer_id=self.customer_id)

    @property
    def total(self) -> Money:
        return sum((line.amount for line in self.lines), Money.zero())
```

**TypeScript scaffold:**
```typescript
// src/domain/<context>/aggregates/Order.ts
export class Order {
  private constructor(
    public readonly id: OrderId,
    public readonly customerId: CustomerId,
    private _lines: LineItem[] = [],
    private _status: OrderStatus = OrderStatus.Draft,
  ) {}

  static create(customerId: CustomerId): [Order, OrderCreated] {
    const order = new Order(OrderId.generate(), customerId);
    return [order, new OrderCreated(order.id)];
  }

  addLine(productId: ProductId, quantity: number, price: Money): void {
    if (this._status !== OrderStatus.Draft) throw new Error("Cannot modify placed order");
    this._lines.push(new LineItem(productId, quantity, price));
  }
}
```

### 5. Directory Structure

```
src/
└── domain/
    ├── catalog/
    │   ├── aggregates/      # Product, Category
    │   ├── value-objects/   # ProductId, Price, SKU
    │   ├── repositories/    # IProductRepository (interface only)
    │   ├── events/          # ProductPublished, PriceChanged
    │   └── services/        # domain services (no infra deps)
    ├── orders/
    │   ├── aggregates/      # Order
    │   ├── value-objects/   # OrderId, Money, LineItem
    │   ├── repositories/    # IOrderRepository
    │   └── events/          # OrderPlaced, OrderCancelled
    └── shared-kernel/
        └── value-objects/   # Money, Address (used across contexts)
```

### 6. Anti-Patterns to Flag

Scan existing code for common DDD violations:
```bash
# Anemic domain model — behavior in services, not entities
grep -rn "def update_\|def set_\|\.save()\|\.update(" . \
  --include="*.py" -l 2>/dev/null | head -5

# Cross-aggregate references by object (should be by ID)
grep -rn "order\.customer\." . --include="*.py" --include="*.ts" 2>/dev/null | head -5
```

## Examples

```
/ddd-model "e-commerce platform with catalog, orders, and billing"
/ddd-model "SaaS app with multi-tenancy, billing, and user management"
/ddd-model audit
```

## Token Optimization

**Expected range**: 800–3,000 tokens (full modeling), 400–800 tokens (audit only)

**Early exit**: Audit on a small CRUD app surfaces the DDD fitness warning and exits without generating full model.

**Grep-before-Read**: Detects language and existing structure via grep before reading source files.

**Patterns used**: Grep-before-Read, early exit, progressive disclosure (context map → aggregates → scaffolding on request)
