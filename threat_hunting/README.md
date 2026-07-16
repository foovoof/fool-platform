# Threat Hunting Foundation

## Phase 6G

This is the **Threat Hunting Foundation** - Phase 6G of the FOOL Platform architecture.

## IMPORTANT: What This IS

This phase implements the **Threat Hunting Core**:

✅ Hunt entities  
✅ Hunt sessions  
✅ Hunt hypotheses  
✅ Hunt objectives  
✅ Hunt observations  
✅ Hunt findings  
✅ Evidence aggregation  
✅ Confidence propagation  
✅ Hunt reports  
✅ Descriptive recommendations  
✅ Event emission  
✅ Deterministic services  
✅ Explainable validation  

## IMPORTANT: What This Is NOT

This phase does **NOT** perform:

- ❌ AI/LLM
- ❌ Autonomous Hunting
- ❌ SOAR
- ❌ Incident Response
- ❌ Response Actions
- ❌ Containment
- ❌ Remediation
- ❌ Live Endpoint Collection
- ❌ Detection Rule Execution
- ❌ YARA Execution
- ❌ Threat Feed Polling
- ❌ External Lookups
- ❌ Risk Scoring
- ❌ Decision Engines
- ❌ Playbook Automation

**Threat Hunting is a consumer of intelligence. It does NOT produce canonical knowledge.**

## Architectural Principle

```
Standards → Contracts → Domain → Knowledge → Inference → Intelligence → Threat Intelligence → Threat Hunting → Applications
```

**Threat Hunting organizes and validates investigative knowledge. It does not automate investigations.**

## Module Structure

```
threat_hunting/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── enums.py
│   ├── base.py
│   ├── hunt.py
│   ├── hypothesis.py
│   ├── observation.py
│   ├── evidence.py
│   └── report.py
├── service.py
├── validation.py
├── events.py
└── tests/
    ├── __init__.py
    └── test_threat_hunting.py
```

## Hunt Lifecycle

```
draft → planned → approved → in_progress → completed/cancelled → archived
```

## Hypothesis Lifecycle

```
draft → approved → running → validated/rejected → archived
```

## Core Models

### Hunt
- Main hunt entity
- Scopes and objectives
- Session tracking
- Finding aggregation

### HuntSession
- Investigation session
- CTI snapshot
- Rules used
- Observations
- Findings

### HuntHypothesis
- Structured hypothesis
- Supporting/contradicting evidence
- Confidence assessment
- Validation status

### HuntObservation
- Descriptive observation
- Evidence references
- Confidence
- Source tracking

### HuntFinding
- Deterministic finding
- Severity assessment
- Evidence bundle
- Explanations

### HuntRecommendation
- **DESCRIPTIVE ONLY**
- Review recommendations
- NO action execution

## Evidence Aggregation

```python
EvidenceBundle
├── EvidenceReference
│   ├── entity_type
│   ├── entity_id
│   ├── relevance_score
│   └── supporting_findings
├── EvidenceChain
└── Confidence aggregation
```

## Confidence Propagation

Reuses the platform confidence framework.

## Guiding Principle

> **Threat Hunting organizes and validates investigative knowledge.**
> 
> It does not automate investigations.
> It does not make security decisions.
> It does not respond to incidents.
> It does not replace analysts.
> 
> It transforms intelligence into structured, explainable, deterministic hunting workflows.

## Architecture Boundaries

### Allowed Dependencies

- ✅ `standards` - Standard definitions
- ✅ `contracts` - Domain contracts
- ✅ `domain` - Domain models
- ✅ `knowledge` - Knowledge graph
- ✅ `inference` - Inference engine
- ✅ `intelligence` - Intelligence runtime
- ✅ `cti_core` - CTI Core
- ✅ `Python standard library` - Standard library only

### Forbidden Dependencies

- ❌ `Applications` - Application layer
- ❌ `AI` - AI/ML components
- ❌ `SOAR` - SOAR
- ❌ `Connectors` - Data connectors
- ❌ `Exchange` - Exchange adapters
- ❌ `Detection engines` - Detection rule execution
- ❌ `Endpoint agents` - Live endpoint collection

## Key Principles

1. **Consumer of intelligence** - Threat Hunting never produces canonical knowledge
2. **Deterministic** - All logic is deterministic, no probability
3. **Explainable** - Every result has an explanation
4. **Auditable** - Complete audit trail
5. **Replayable** - Hunting workflows can be replayed
6. **Versioned** - All changes are versioned
7. **Governed** - All entities are governed
8. **No AI** - No probabilistic AI or LLM
9. **Descriptive only** - Recommendations do not execute actions

## Design Principles

Every hunt must be:
- ✅ Deterministic
- ✅ Explainable
- ✅ Auditable
- ✅ Replayable
- ✅ Governed
- ✅ Versioned
- ✅ Provenanced
- ✅ Testable

## Next Phase

**Phase 6H — Incident Intelligence Foundation**
