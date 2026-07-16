# Threat Intelligence Core

## Phase 6E.1

This is the **Threat Intelligence Core Foundation** - Phase 6E.1 of the FOOL Platform architecture.

## IMPORTANT: What This IS

This phase implements the **canonical CTI (Cyber Threat Intelligence) Core**:

✅ Indicator management  
✅ Threat actor profiles  
✅ Campaign tracking  
✅ Malware tracking  
✅ Infrastructure tracking  
✅ Vulnerability tracking  
✅ Evidence management  
✅ Confidence assessment  
✅ Reporting  
✅ Query capabilities  
✅ Versioning  
✅ Lifecycle management  
✅ Attribution support  

## IMPORTANT: What This Is NOT

This phase does **NOT** implement:

- ❌ STIX/TAXII
- ❌ MISP
- ❌ External feeds
- ❌ Threat Hunting
- ❌ Incident Response
- ❌ Digital Forensics
- ❌ AI/LLM
- ❌ Sigma execution
- ❌ YARA execution
- ❌ SOAR
- ❌ SIEM integrations

**Core only. No external integrations.**

## Architectural Principle

```
Threat Models → Services → Repositories
                    ↓
              Lifecycle Manager
                    ↓
              Confidence Framework
                    ↓
              Evidence Management
                    ↓
              Query & Reporting
                    ↓
              Versioning & Audit
```

**FOOL owns the threat intelligence domain. No external standard becomes the canonical model.**

## Module Structure

```
threat_intelligence/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── enums.py
│   ├── base.py
│   ├── entities.py
│   ├── relationships.py
│   ├── evidence.py
│   ├── findings.py
│   ├── reports.py
│   └── collections.py
├── services/
│   ├── __init__.py
│   ├── indicator_service.py
│   ├── actor_service.py
│   ├── malware_service.py
│   └── relationship_service.py
├── repository/
│   ├── __init__.py
│   ├── base.py
│   └── inmemory.py
├── registry.py
├── events.py
├── validation.py
├── query.py
├── versioning.py
├── confidence.py
├── lifecycle.py
├── reporting.py
├── evidence.py
├── attribution.py
└── tests/
    ├── __init__.py
    └── test_threat_intelligence.py
```

## Supported Entities

### Indicators

| Field | Description |
|-------|-------------|
| `id` | UUID identifier |
| `name` | Indicator name |
| `value` | Indicator value |
| `indicator_type` | Type (IP, domain, hash, etc.) |
| `pattern` | STIX pattern (optional) |
| `status` | Observed, deployed, revoked, expired |
| `threat_level` | Critical, high, medium, low |
| `confidence_level` | High, medium, low |
| `confidence_score` | 0.0 - 1.0 |

### Threat Actors

| Field | Description |
|-------|-------------|
| `id` | UUID identifier |
| `name` | Actor name |
| `alias` | Alias names |
| `actor_type` | Nation state, criminal, hacktivist |
| `sophistication` | Sophistication level |
| `resource_level` | Available resources |
| `motivation` | Motivation |
| `target_sectors` | Targeted industry sectors |
| `target_geographies` | Targeted regions |

### Campaigns

| Field | Description |
|-------|-------------|
| `id` | UUID identifier |
| `name` | Campaign name |
| `status` | Planned, active, completed, cancelled |
| `threat_actor` | Associated threat actor |
| `start_date` | Campaign start |
| `end_date` | Campaign end |
| `objective` | Campaign objective |

### Malware

| Field | Description |
|-------|-------------|
| `id` | UUID identifier |
| `name` | Malware name |
| `malware_type` | Type (trojan, ransomware, etc.) |
| `malware_family` | Family name |
| `capabilities` | Malware capabilities |
| `command_and_control` | C2 infrastructure |

## Services

### IndicatorService

```python
from threat_intelligence import IndicatorService, IndicatorType

service = IndicatorService()

# Create indicator
indicator = service.create(
    name="Malicious Domain",
    value="evil.com",
    indicator_type=IndicatorType.DOMAIN_NAME.value,
    author="analyst",
)

# Search indicators
results = service.find_by_type(IndicatorType.DOMAIN_NAME.value)
```

### ThreatActorService

```python
from threat_intelligence import ThreatActorService, ThreatActorType

service = ThreatActorService()

# Create threat actor
actor = service.create(
    name="APT29",
    actor_type=ThreatActorType.NATION_STATE.value,
    author="analyst",
)
```

### MalwareService

```python
from threat_intelligence import MalwareService, MalwareType

service = MalwareService()

# Create malware entry
malware = service.create(
    name="Emotet",
    malware_type=MalwareType.TROJAN.value,
    author="analyst",
)
```

## Confidence Framework

### Confidence Levels

| Level | Score Range |
|-------|-------------|
| HIGH | 0.7 - 1.0 |
| MEDIUM | 0.4 - 0.7 |
| LOW | 0.0 - 0.4 |

### Confidence Calculation

Rule-based calculation based on:
- Source reliability (A-F)
- Information reliability (Confirmed-Likely-Possible-Doubtful-Unlikely-Unknown)

```python
from threat_intelligence import ConfidenceService

service = ConfidenceService()

level, score = service.calculate_confidence(
    source_reliability="A",
    information_reliability="confirmed",
)

print(f"Confidence: {level} ({score})")  # HIGH (0.9)
```

## Lifecycle Management

### Indicator Lifecycle

```
new → in_progress → stable → archived
                    ↓
                degraded → deprecated → archived
```

### Campaign Lifecycle

```
new → in_progress → stable → archived
                    ↓
                deprecated → archived
```

### Report Lifecycle

```
draft → review → published → archived
         ↓
       draft
```

## Evidence Management

### Evidence Types

| Type | Description |
|------|-------------|
| DIRECT | Direct evidence of activity |
| CIRCUMSTANTIAL | Circumstantial evidence |
| CORROBORATING | Corroborating evidence |
| INCONSISTENT | Inconsistent evidence |

### Evidence Chain

```python
from threat_intelligence import EvidenceChainBuilder

builder = EvidenceChainBuilder()
bundle = builder.add_evidence("e1", "direct", "Evidence 1") \
    .add_evidence("e2", "circumstantial", "Evidence 2") \
    .build()
```

## Versioning

Every entity supports:
- Version tracking
- Revision history
- Author attribution
- Change reasons

```python
from threat_intelligence import VersioningService

service = VersioningService()
service.record_version(
    entity_id="indicator-1",
    version=2,
    author="analyst",
    reason="Updated confidence score",
)

history = service.get_history("indicator-1")
```

## Architecture Boundaries

### Allowed Dependencies

- ✅ `standards` - Standard definitions
- ✅ `contracts` - Domain contracts
- ✅ `domain` - Domain models
- ✅ `knowledge` - Knowledge graph
- ✅ `inference` - Inference engine
- ✅ `intelligence runtime` - Intelligence runtime
- ✅ `platform events` - Event bus
- ✅ `Python standard library` - Standard library only

### Forbidden Dependencies

- ❌ `AI` - AI/ML components
- ❌ `LLM` - LLM components
- ❌ `connectors` - Data connectors
- ❌ `applications` - Application layer
- ❌ `databases` - Database integrations
- ❌ `external APIs` - External services
- ❌ `web frameworks` - Web frameworks

## Key Principles

1. **FOOL is authoritative** - Internal model is the source of truth
2. **Deterministic** - All logic is deterministic, no probability
3. **Explainable** - Every assessment has an explanation
4. **Auditable** - Complete audit trail
5. **Versioned** - All changes are versioned
6. **No AI** - No probabilistic AI or LLM
7. **No external feeds** - No network access, no external services

## Next Phase

**Phase 6E.2 — IOC Management Foundation**

This will implement:
- IOC collection management
- IOC enrichment
- IOC sharing
- IOC correlation
