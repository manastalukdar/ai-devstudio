---
name: ai-governance
description: Audit an AI/ML system for governance controls — bias risk, explainability, model risk management, data lineage, fairness metrics, and regulatory alignment (EU AI Act, NIST AI RMF)
disable-model-invocation: false
risk: safe
---

# AI Governance Audit

Systematic trust and control assessment for AI/ML systems. Maps the AI system boundary, evaluates risk controls, and identifies gaps against governance frameworks (EU AI Act, NIST AI RMF, ISO 42001).

## Usage

```
/ai-governance                   # full audit of the current project
/ai-governance <path>            # audit a specific ML service or module
/ai-governance --framework eu    # focus on EU AI Act risk classification
/ai-governance --framework nist  # focus on NIST AI RMF (Govern/Map/Measure/Manage)
```

## Behavior

### Step 1 — Map the AI system boundary

```bash
# Identify model artifacts, training scripts, inference code
find . -name "*.pkl" -o -name "*.pt" -o -name "*.onnx" -o -name "model.*" 2>/dev/null | head -10
grep -rn "model.predict\|model.generate\|pipeline\|inference" --include="*.py" -l . | head -10

# Find dataset references
grep -rn "pd.read_csv\|load_dataset\|dataloader\|train_data" --include="*.py" -l . | head -10
```

Document:
- What decisions does the model make? (classification, ranking, generation, recommendation)
- Who is affected? (internal tooling vs customer-facing vs high-stakes)
- What data does it consume?

### Step 2 — Risk classification

Classify the system under the EU AI Act tiers:

| Risk tier | Criteria | Examples |
|---|---|---|
| **Unacceptable** | Social scoring, real-time biometric surveillance | Flag for legal review immediately |
| **High** | Employment, credit, health, safety, law enforcement | Full compliance controls required |
| **Limited** | Chatbots, emotion recognition disclosure | Transparency obligations only |
| **Minimal** | Spam filters, game AI, recommenders | Voluntary codes of practice |

Flag the applicable tier and list required controls.

### Step 3 — Evaluate bias and fairness controls

```bash
# Look for fairness tooling
grep -rn "fairlearn\|aif360\|what-if-tool\|demographic\|protected\|sensitive_attr\|equalized_odds" \
  --include="*.py" -l . 2>/dev/null

# Check if sensitive attributes are in training data
grep -rn "gender\|race\|ethnicity\|age\|religion\|nationality" \
  --include="*.py" --include="*.csv" --include="*.json" -l . 2>/dev/null | head -10
```

Check for:
- Fairness metric definition (demographic parity, equalized odds, calibration)
- Bias testing in CI pipeline
- Disparate impact analysis on test set
- Sensitive attribute handling (removed, proxied, or legitimately included)

### Step 4 — Evaluate explainability

```bash
grep -rn "shap\|lime\|captum\|eli5\|anchors\|explanation\|interpret" --include="*.py" -l . 2>/dev/null
```

Check:
- Is there a method to explain individual predictions?
- Are explanations surfaced to affected users or decision-makers?
- Is there a global feature importance report?
- For LLMs: are citations / sources provided for generated claims?

### Step 5 — Evaluate model risk management

Check for model risk controls:

| Control | What to look for | Gap indicator |
|---|---|---|
| Model card | `model_card.md`, `MODEL_CARD.md`, `README` with model description | No documentation of intended use, limitations, training data |
| Version tracking | Model version in filename, MLflow, DVC, W&B | Model artifact with no version |
| Performance monitoring | Drift detection, accuracy tracking in production | No monitoring post-deployment |
| Human-in-the-loop | Approval step for high-stakes decisions | Fully automated decisions in high-risk domain |
| Rollback plan | Previous model artifact retained | Only latest model available |
| Incident process | Runbook for model failure | No defined response to model misbehavior |

### Step 6 — Evaluate data governance

```bash
# Check for data lineage documentation
find . -name "data_catalog*" -o -name "lineage*" -o -name "data_dictionary*" 2>/dev/null
grep -rn "consent\|gdpr\|pii\|personally_identifiable\|anonymize\|pseudonymize" --include="*.py" -l . 2>/dev/null
```

Check:
- Is training data provenance documented?
- Is PII in training data identified and handled?
- Is there a data retention / deletion policy?
- Can a subject request their data be removed from training?

### Step 7 — Report findings

```
AI GOVERNANCE AUDIT — <system/path>

Risk Classification
  EU AI Act tier: LIMITED (chatbot with emotion recognition disclosure required)
  NIST AI RMF: Map phase incomplete — no impact assessment documented

Bias & Fairness (2 gaps)
  No fairness metrics defined — demographic parity not measured on test set
  gender column present in training features — document why or remove

Explainability (1 gap)
  No explanation method found — users cannot understand why they received a recommendation

Model Risk Management (3 gaps)
  No model card — intended use, limitations, and training data undocumented
  Model artifact (model.pkl) has no version tag — rollback impossible
  No drift monitoring configured — silent degradation in production undetected

Data Governance (1 gap)
  PII (email addresses) in training CSV with no anonymization documentation

Required actions for LIMITED tier compliance:
  [ ] Add disclosure that users are interacting with an AI system
  [ ] Document model limitations in model card
  [ ] Implement opt-out mechanism for data use in training
```

## Edge Cases

- **No ML code detected**: Check for third-party model API calls (OpenAI, Bedrock, etc.) and apply governance review to the integration layer.
- **Internal tooling only**: Note reduced risk tier; focus on model risk management and explainability rather than regulatory compliance.
- **Foundation model wrapper**: Most governance obligations shift to the foundation model provider; focus audit on the application layer (context, output validation, misuse prevention).

## Token Optimization

**Expected range**: 800–2,500 tokens (full audit); 300–600 tokens (single-framework focus)

**Patterns used**: Grep-before-Read, early exit (if no ML artifacts found, report and suggest scope), progressive disclosure (classification → gaps → required actions)

**Caching**: Caches system boundary map in `.claude/cache/ai-governance/boundary.json` (invalidated when model files or training scripts change).

**Early exit**: If no model artifacts, training scripts, or LLM client code found, report "No AI/ML system detected in this path" and exit.
