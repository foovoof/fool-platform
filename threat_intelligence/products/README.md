# Intelligence Products Foundation

## Phase 6E.9

This is the **Intelligence Reports & Products Foundation** - Phase 6E.9 of the FOOL Platform architecture.

## IMPORTANT: What This IS

This phase implements the **Intelligence Products Core**:

✅ Intelligence Product entities  
✅ Product lifecycle  
✅ Versioning  
✅ Assertions  
✅ Evidence linking  
✅ Confidence binding  
✅ Provenance tracking  
✅ Registry-driven taxonomy  
✅ Deterministic services  
✅ Explainable validation  

## IMPORTANT: What This Is NOT

This phase does **NOT** perform:

- ❌ PDF Generation
- ❌ HTML Reports
- ❌ Markdown Rendering
- ❌ Dashboards
- ❌ Visualizations
- ❌ AI Summary
- ❌ Natural Language Generation
- ❌ Templates Engine
- ❌ Email Distribution
- ❌ TAXII Export
- ❌ STIX Export
- ❌ MISP Export
- ❌ IOC Feeds
- ❌ External APIs

**Products reference canonical intelligence entities. Products never duplicate knowledge.**

## Architectural Principle

```
Knowledge → Intelligence → Products
                        ↓
              Canonical Entity References
                        ↓
                Product Lifecycle
                        ↓
              Version Management
                        ↓
              Registry-Driven Taxonomy
```

**Products transform governed intelligence entities into governed intelligence products.**

## Module Structure

```
threat_intelligence/products/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── enums.py
│   ├── base.py
│   ├── product.py
│   └── assertion.py
├── registries.py
├── service.py
├── validation.py
├── events.py
├── queries.py
└── tests/
    ├── __init__.py
    └── test_products.py
```

## Product Types

| Type | Description |
|------|-------------|
| `threat_report` | Threat Report |
| `technical_report` | Technical Report |
| `strategic_report` | Strategic Report |
| `operational_report` | Operational Report |
| `tactical_report` | Tactical Report |
| `executive_summary` | Executive Summary |
| `indicator_list` | Indicator List |
| `ioc_bulletin` | IOC Bulletin |
| `ttp_analysis` | TTP Analysis |
| `campaign_report` | Campaign Report |
| `threat_actor_profile` | Threat Actor Profile |
| `malware_analysis` | Malware Analysis |
| `vulnerability_advisory` | Vulnerability Advisory |
| `infrastructure_report` | Infrastructure Report |

## Lifecycle States

```
draft → under_review → validated → approved → published → superseded/deprecated → archived
```

Valid transitions:
- draft → under_review, archived
- under_review → validated, draft, archived
- validated → approved, under_review, archived
- approved → published, archived
- published → superseded, deprecated, archived

## Classification Levels

| Level | Description |
|-------|-------------|
| `unclassified` | Unclassified |
| `internal` | Internal |
| `confidential` | Confidential |
| `secret` | Secret |
| `top_secret` | Top Secret |

## Canonical Entity References

Products can reference:

- Indicators (`indicator_refs`)
- Observables (`observable_refs`)
- Threat Actors (`actor_refs`)
- Campaigns (`campaign_refs`)
- Malware (`malware_refs`)
- Infrastructure (`infrastructure_refs`)
- Vulnerabilities (`vulnerability_refs`)
- TTPs (`ttp_refs`)
- Evidence (`evidence_refs`)
- Assertions (`assertion_refs`)
- Knowledge (`knowledge_refs`)
- Inference (`inference_refs`)

**Products NEVER duplicate intelligence. They only reference canonical entities.**

## Services

### ProductService

```python
from threat_intelligence.products import ProductService

service = ProductService()

product = service.create(
    name="Q1 Threat Report",
    product_type="threat_report",
    title="Q1 2024 Threat Landscape",
    description="Quarterly threat analysis",
    author="analyst",
    classification="internal",
)

retrieved = service.get(product.id)
results = service.find_by_type("threat_report")
results = service.find_by_status("published")
```

### LifecycleService

```python
from threat_intelligence.products import LifecycleService

service = LifecycleService()

success, msg = service.transition(
    "prod-1",
    "under_review",
    reason="Ready for review",
    transitioned_by="user",
)
```

### ProductQueryService

```python
from threat_intelligence.products import ProductQueryService

service = ProductQueryService()

results = service.find_by_type("threat_report")
results = service.find_by_status("published")
results = service.find_by_actor("actor-1")
results = service.find_by_malware("malware-1")
results = service.find_by_indicator("ioc-1")
results = service.find_by_campaign("campaign-1")
```

## Taxonomy Registries

```python
from threat_intelligence.products import (
    ProductTypeRegistry,
    ClassificationRegistry,
    LifecycleRegistry,
    RelationshipRegistry,
)

# Get all product types
types = ProductTypeRegistry.get_types()

# Get classification levels
levels = ClassificationRegistry.get_levels()

# Get lifecycle states
states = LifecycleRegistry.get_states()
```

## Assertions

Product assertions are governed claims:

```python
from threat_intelligence.products import ProductAssertion

assertion = ProductAssertion(
    product_id="prod-1",
    assertion_type="finding",
    assertion="APT29 targets financial institutions",
    status="confirmed",
    evidence_refs=("evidence-1",),
)
```

## Confidence Binding

```python
from threat_intelligence.products import ProductConfidence

confidence = ProductConfidence(
    product_id="prod-1",
    confidence_level="high",
    confidence_score=0.85,
    confidence_explanation="Based on multiple sources",
    evidence_refs=("evidence-1", "evidence-2"),
)
```

## Provenance

```python
from threat_intelligence.products import ProductProvenance

provenance = ProductProvenance(
    product_id="prod-1",
    source_type="intelligence_feed",
    source_id="feed-1",
    source_description="Internal threat intel feed",
    collection_method="automated",
    collected_by="system",
)
```

## Architecture Boundaries

### Allowed Dependencies

- ✅ `standards` - Standard definitions
- ✅ `contracts` - Domain contracts
- ✅ `knowledge` - Knowledge graph
- ✅ `inference` - Inference engine
- ✅ `intelligence` - Intelligence runtime
- ✅ `Python standard library` - Standard library only

### Forbidden Dependencies

- ❌ `Internet` - Internet access
- ❌ `Connectors` - Data connectors
- ❌ `Exchange` - Exchange integrations
- ❌ `TAXII` - TAXII
- ❌ `STIX` - STIX
- ❌ `MISP` - MISP
- ❌ `AI` - AI/ML components
- ❌ `Rendering` - PDF, HTML, Markdown
- ❌ `UI` - User interfaces
- ❌ `Dashboards` - Dashboards

## Key Principles

1. **Products reference** - Products never duplicate knowledge
2. **Deterministic** - All logic is deterministic, no probability
3. **Explainable** - Every assessment has an explanation
4. **Auditable** - Complete audit trail
5. **Versioned** - All changes are versioned
6. **No AI** - No probabilistic AI or LLM
7. **Registry-driven** - Taxonomy comes from registries

## Guiding Principle

> Knowledge becomes Intelligence.  
> Intelligence becomes Products.  
> Products never own knowledge.  
> Products reference canonical intelligence.  
> Everything is explainable.  
> Everything is versioned.  
> Everything is governed.  
> Nothing is duplicated.

## Next Phase

**Phase 6E.10 — Intelligence Query & Analytics Foundation**
