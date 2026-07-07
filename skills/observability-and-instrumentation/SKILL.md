---
name: observability-and-instrumentation
description: Instrument code with structured logging, metrics, and OpenTelemetry tracing — define the on-call questions first, then work backward to the telemetry that answers them.
disable-model-invocation: false
risk: none
---

# Observability and Instrumentation

I'll instrument your code for production observability using the define-questions-first approach: start with what an on-call engineer needs to know, then work backward to the logs, metrics, and traces that answer those questions.

Arguments: `$ARGUMENTS` — service or feature to instrument

## Token Optimization

**Expected range**: 600–2,000 tokens (SLO questions + instrumentation plan + implementation)

**Early exit**: If the code already has OpenTelemetry spans, structured logging, and error rate metrics, report what is present and suggest only the gaps

**Patterns used**: Grep-before-Read (check existing telemetry before adding), progressive disclosure (plan first, code on confirmation)

## Step 1 — Define On-Call Questions

Before writing any code, answer: what does an on-call engineer need to know when this breaks at 3 AM?

Produce a minimum set of SLO questions:

```
On-call questions for [service/feature]:
1. Is it working? (availability / error rate)
   Threshold: [e.g., error rate < 1%]
2. Is it fast? (latency)
   Threshold: [e.g., p99 < 500ms]
3. Is it processing work? (throughput / queue depth)
   Threshold: [e.g., queue depth < 1000]
4. [domain-specific]: [e.g., "What fraction of payments succeed on first attempt?"]
   Threshold: [e.g., payment success rate > 99.5%]
```

Confirm the questions before proceeding. These become the acceptance criteria for the instrumentation.

## Step 2 — Audit Existing Telemetry

```bash
# Check for existing telemetry
grep -rn "console\.\(log\|error\|warn\)\|logger\.\|logging\." --include="*.ts" --include="*.js" --include="*.py" . | grep -v "node_modules\|dist" | wc -l

grep -rn "opentelemetry\|otel\|@opentelemetry" package.json requirements.txt 2>/dev/null | head -5

grep -rn "span\|trace\|metric\|histogram\|counter\|gauge" --include="*.ts" --include="*.js" --include="*.py" . | grep -v "node_modules" | wc -l
```

Report what exists and what is missing relative to the on-call questions.

## Step 3 — Instrumentation Plan

Map each on-call question to the telemetry type that answers it:

```
Question 1 (availability) → metric: error_rate counter + HTTP middleware span
Question 2 (latency)      → trace: span per request with duration histogram
Question 3 (throughput)   → metric: queue_depth gauge polled every 30s
Question 4 (domain SLO)   → structured log event: {event: "payment_attempt", success: bool}
```

## Step 4 — Implement Structured Logging

Use structured JSON logs (not printf-style). Every log event must include:
- `timestamp` (ISO 8601)
- `level` (error / warn / info / debug)
- `service` name
- `trace_id` and `span_id` (if in a traced context)
- Domain-specific fields relevant to the on-call question

```typescript
// Structured log example
logger.info({
  event: "payment_processed",
  payment_id: payment.id,
  success: true,
  duration_ms: elapsed,
  trace_id: span.spanContext().traceId,
})
```

## Step 5 — Add OpenTelemetry Spans

Wrap each meaningful unit of work in a span:

```typescript
const span = tracer.startSpan("payment.process", {
  attributes: {
    "payment.method": method,
    "payment.amount_cents": amount,
  },
})
try {
  const result = await processPayment(...)
  span.setStatus({ code: SpanStatusCode.OK })
  return result
} catch (err) {
  span.setStatus({ code: SpanStatusCode.ERROR, message: err.message })
  span.recordException(err)
  throw err
} finally {
  span.end()
}
```

## Step 6 — Add Metrics

For each on-call question, implement the corresponding metric:

```typescript
// Counter
const errorCounter = meter.createCounter("payment.errors", {
  description: "Number of payment processing errors",
})

// Histogram
const latencyHistogram = meter.createHistogram("payment.duration_ms", {
  description: "Payment processing latency",
  boundaries: [50, 100, 200, 500, 1000, 2000],
})

// Gauge
const queueDepthGauge = meter.createObservableGauge("queue.depth", {
  description: "Current queue depth",
})
```

## Step 7 — Verify Coverage

For each on-call question from Step 1, confirm it is now answerable:

```
On-call question coverage:
  [Q1] Is it working?     → answered by: error_rate counter ✓
  [Q2] Is it fast?        → answered by: duration_ms histogram ✓
  [Q3] Payment SLO?       → answered by: payment_processed log event ✓
```

## Edge Cases

- **No OpenTelemetry SDK installed**: add it as a dependency; provide the install command for the detected language
- **Existing printf-style logging**: do not remove it; wrap it with structured context and note the migration path
- **Serverless / edge functions**: note that OpenTelemetry export must be flushed before the function returns
- **High-cardinality label values** (e.g., user IDs as metric labels): warn that these will cause metric cardinality explosion; use histograms or log events instead
