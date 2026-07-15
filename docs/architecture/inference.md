# Inference Layer Architecture

## Overview

The Inference Layer provides deterministic rule-based inference for FOOL Platform. This is Phase 3B implementation.

**Important**: Phase 3B does NOT implement Intelligence Runtime. Intelligence belongs to Phase 4.

## Architecture Position

```
FOOL Platform Architecture:

Standards ──► Contracts ──► Domain ──► Knowledge ──► Intelligence
                                                       ↑
                                               Inference
```

## Dependency Rules

### Inference May Depend On

- ✅ standards/
- ✅ contracts/
- ✅ domain/
- ✅ knowledge/
- ✅ platform/events interfaces only
- ✅ Python standard library

### Inference Must NOT Depend On

- ❌ intelligence/
- ❌ ai/
- ❌ llm/
- ❌ embeddings
- ❌ connectors
- ❌ orchestration
- ❌ applications
- ❌ external services

## Critical Architectural Rule

### Forbidden Pattern

```
Inference Engine
        ↓
Graph Modified (FORBIDDEN)
```

### Required Pattern

```
Inference Engine
        ↓
Inference Result
        ↓
Inference Validation
        ↓
Knowledge Service
        ↓
Graph Update (via Service)
```

Inference MUST NOT directly modify the Knowledge Graph.

## Inference Components

### 1. Inference Engine (knowledge/inference/engine/)

| Component | Purpose |
|-----------|---------|
| InferenceEngine | Main inference orchestration |
| InferenceSession | Inference execution context |
| InferenceResult | Results of inference execution |
| InferenceConclusion | Single conclusion |

### 2. Rule System (knowledge/inference/rules/)

| Component | Purpose |
|-----------|---------|
| RuleRegistry | Rule storage and retrieval |
| RuleValidator | Rule validation |
| RuleEvaluator | Rule condition evaluation |
| RuleExecutor | Rule output execution |

### 3. Evidence (knowledge/inference/evidence/)

| Component | Purpose |
|-----------|---------|
| EvidenceTracker | Evidence registration and tracking |
| EvidenceChain | Evidence chain building |
| EvidencePropagation | Evidence propagation |

### 4. Confidence (knowledge/inference/confidence/)

| Component | Purpose |
|-----------|---------|
| ConfidenceRecord | Confidence value record |
| ConfidenceCalculator | Deterministic confidence calculation |
| ConfidencePropagation | Confidence propagation |

### 5. Explanation (knowledge/inference/explanation/)

| Component | Purpose |
|-----------|---------|
| Explanation | Explanation model |
| ExplanationGenerator | Human-readable explanation generation |

### 6. Validation (knowledge/inference/validation/)

| Component | Purpose |
|-----------|---------|
| InferenceValidator | Inference result validation |
| RuleConsistencyValidator | Rule consistency checking |

### 7. Events (knowledge/inference/events/)

| Event Type | Purpose |
|------------|---------|
| session.started | Session started |
| session.completed | Session completed |
| rule.evaluated | Rule evaluated |
| rule.triggered | Rule triggered |
| conclusion.generated | Conclusion generated |
| confidence.updated | Confidence updated |
| explanation.generated | Explanation generated |

### 8. Services (knowledge/inference/services/)

| Service | Purpose |
|---------|---------|
| InferenceService | Main inference orchestration |
| RuleService | Rule management |
| EvidenceService | Evidence operations |
| ConfidenceService | Confidence operations |
| ExplanationService | Explanation operations |

## Inference Flow

```
1. Create Session
        ↓
2. Select Rules (from Registry)
        ↓
3. Evaluate Rule Conditions (against Graph)
        ↓
4. Execute Rule Outputs (if triggered)
        ↓
5. Generate Conclusions
        ↓
6. Track Evidence
        ↓
7. Calculate Confidence
        ↓
8. Generate Explanations
        ↓
9. Produce Recommendations
        ↓
10. Validate Results
        ↓
11. Emit Events
        ↓
12. Return Inference Result
```

## Rule Architecture

### Rule Structure

```python
Rule:
  - rule_id: Unique identifier
  - name: Human-readable name
  - description: Rule description
  - version: Rule version
  - priority: Execution priority
  - enabled: Is rule enabled
  - conditions: List of conditions
  - outputs: List of outputs
  - source_ontology: Ontology reference
  - source_contract: Contract reference
```

### Condition Types

- ENTITY_EXISTS
- ATTRIBUTE_EQUALS
- ATTRIBUTE_NOT_EQUALS
- ATTRIBUTE_GREATER_THAN
- ATTRIBUTE_LESS_THAN
- ATTRIBUTE_IN
- ATTRIBUTE_CONTAINS
- RELATIONSHIP_EXISTS
- RELATIONSHIP_TYPE
- IDENTITY_EXISTS
- NODE_TYPE
- ALL_CONDITIONS (AND)
- ANY_CONDITIONS (OR)
- NOT_CONDITION

### Output Types

- ADD_ATTRIBUTE
- UPDATE_ATTRIBUTE
- ADD_IDENTITY
- ADD_RELATIONSHIP
- SET_CONFIDENCE
- CREATE_ENTITY
- CLASSIFY_ENTITY
- GENERATE_CONCLUSION
- PROPAGATE_CONFIDENCE

## Evidence Flow

```
Graph Fact
        ↓
Evidence Registration
        ↓
Evidence Tracking
        ↓
Evidence Chain Building
        ↓
Evidence Propagation
        ↓
Conclusion Support
```

## Confidence Flow

```
Evidence
        ↓
Confidence Calculation (Deterministic)
        ↓
Confidence Record
        ↓
Confidence Propagation
        ↓
Confidence Update
```

## Explainability

Every inference result must have an explanation.

```python
Explanation:
  - explanation_id: Unique identifier
  - rule_id: Source rule
  - evidence_ids: Supporting evidence
  - conclusion_ids: Conclusions explained
  - generated_text: Human-readable text
  - steps: Explanation steps
```

## Validation Model

### Rule Validation

- Structure validity
- Reference validity
- Ontology compliance
- Contract compliance

### Inference Validation

- Conclusion validity
- Evidence integrity
- Confidence integrity
- Explanation completeness

### Consistency Validation

- Circular references
- Conflicting rules
- Unreachable rules
- Orphan rules

## Event Integration

Uses platform/events. Event failures do not fail inference.

## Phase 4 Preview

Phase 4 will add:

- Intelligence Runtime
- Planning Engine
- Goal Selection
- Strategy Generation
- Autonomous Reasoning
- AI/LLM Integration

Phase 3B remains foundational for Phase 4.

## Testing

Run tests:

```bash
pytest knowledge/inference/tests/
```

## Architecture Tests

See `testing/architecture/test_python_first_architecture.py` for:

- Inference layer existence
- Module structure
- Purity checks (no AI, intelligence, connectors)
- Knowledge does not import inference
