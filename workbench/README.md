# Threat Intelligence Workbench Foundation

## Phase 8C

This is the **Threat Intelligence Workbench Foundation** - Phase 8C of the FOOL Platform architecture.

This is the **canonical intelligence governance product** of the FOOL Reference Intelligence Platform.

## FUNDAMENTAL PRINCIPLES

```
Platform owns Intelligence Assets
         ↓
Workbench governs Intelligence Assets
         ↓
Workspaces consume Intelligence Assets
```

**The Workbench SHALL never become another CTI Core.**

- It orchestrates.
- It governs.
- It certifies.
- It **NEVER** owns platform knowledge.

## REFERENCE NOT REPLICA

Every intelligence asset used inside the Workbench **SHALL be represented by references**.

- **NEVER** copies
- **NEVER** duplicated models
- **ONLY** references

## GOVERN, NOT OWN

This is the governing architectural rule:

The Workbench **manages**:
- Lifecycle
- Approvals
- Reviews
- Publication
- Governance

The Workbench **never owns**:
- Indicators
- Observables
- Threat Actors
- Campaigns
- Malware
- Infrastructure
- Vulnerabilities
- TTPs
- Evidence
- Reports

## IMPORTANT: What This IS

This phase implements the **Threat Intelligence Workbench**:

✅ Product governance  
✅ Collection governance  
✅ Review cycles  
✅ Approval workflows  
✅ Publication governance  
✅ Source assessment (human only)  
✅ Confidence review (human only)  
✅ Governance decisions  
✅ Reference management  
✅ Audit trail  
✅ Event emission  

## IMPORTANT: What This Is NOT

This phase does **NOT** perform:

- ❌ Detection Logic
- ❌ Correlation Logic
- ❌ Knowledge Inference
- ❌ Knowledge Modification
- ❌ Indicator Ownership
- ❌ Evidence Storage
- ❌ Report Generation
- ❌ External Publishing
- ❌ PDF Rendering
- ❌ AI/LLM
- ❌ Autonomous Reviews
- ❌ Automatic Approvals
- ❌ Confidence Prediction
- ❌ SOAR

## Module Structure

```
workbench/
├── __init__.py
├── runtime.py
├── events.py
├── models/
│   ├── __init__.py
│   ├── enums.py
│   ├── base.py
│   ├── product.py
│   ├── governance.py
│   └── session.py
└── tests/
    ├── __init__.py
    └── test_workbench.py
```

## Product Lifecycle

```
DRAFT → IN_REVIEW → APPROVED → PUBLISHED → SUPERSEDED → ARCHIVED
```

Every transition supports:
- reviewer
- timestamp
- reason
- audit
- version
- approval record

**No automatic transitions.**

## Aggregate Roots

| Aggregate Root | Purpose |
|---------------|---------|
| `IntelligenceProduct` | Main product governance |
| `IntelligenceCollection` | Collection governance |
| `Publication` | Publication governance |
| `ReviewCycle` | Review cycle governance |

## Core Models

### Reference Models (NEVER duplicated)

| Model | Purpose |
|-------|---------|
| `AssertionReference` | Reference to platform assertion |
| `EvidencePackageReference` | Reference to platform evidence |
| `KnowledgeReference` | Reference to platform knowledge |

### Governance Models

| Model | Purpose |
|-------|---------|
| `Reviewer` | Reviewer information |
| `ReviewCycle` | Review cycle management |
| `ApprovalRecord` | Approval workflow record |
| `ApprovalWorkflow` | Approval workflow definition |
| `Publication` | Publication governance |
| `SourceAssessment` | Source reliability (human only) |
| `ConfidenceReview` | Confidence review (human only) |
| `GovernanceDecision` | Governance decision record |
| `PublicationPolicy` | Publication policy definition |

## Runtime Services

| Service | Purpose |
|---------|---------|
| `ProductManager` | Product governance |
| `CollectionManager` | Collection governance |
| `ReviewManager` | Review cycle management |
| `ApprovalManager` | Approval workflow |
| `PublicationManager` | Publication governance |
| `GovernanceManager` | Governance decisions |
| `SourceAssessmentManager` | Source assessments |
| `ConfidenceReviewManager` | Confidence reviews |

## Events

- `product.created`
- `product.updated`
- `product.review.started`
- `product.review.completed`
- `product.approved`
- `product.rejected`
- `product.published`
- `product.archived`
- `collection.created`
- `publication.created`
- `approval.completed`
- `confidence.reviewed`
- `source.assessed`
- `governance.decision`

## Architecture Boundaries

### Allowed Dependencies

- ✅ `standards` - Standard definitions
- ✅ `contracts` - Domain contracts
- ✅ `domain` - Domain models
- ✅ `knowledge` - Knowledge graph
- ✅ `cti_core` - CTI Core
- ✅ `threat_intelligence` - Threat Intelligence
- ✅ `reporting` - Reporting
- ✅ `Python standard library` - Standard library only

### Forbidden Dependencies

- ❌ `Applications` - Application layer
- ❌ `AI` - AI/ML components
- ❌ `Connectors` - Data connectors
- ❌ `Exchange` - Exchange adapters
- ❌ `Detection engines` - Detection execution
- ❌ `SOAR` - SOAR
- ❌ **Platform ownership of CTI entities**

## Guiding Principle

> **The Workbench governs. The Platform owns.**
>
> Reference, not replica.
> Govern, not own.
>
> Products are replaceable.
> The Platform is the foundation.

## Ready for

- ✅ Investigation Workspace integration
- ✅ Analyst Workspace integration
- ✅ Reporting Portal integration
- ✅ Management Console integration
- ✅ Web UI integration
- ✅ Desktop UI integration
- ✅ REST API integration
- ✅ Future AI copilots (consuming only)

## Next Phase

**Phase 8D — Investigation Workspace Foundation**
