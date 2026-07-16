# Infrastructure Intelligence Core

## Phase 6E.6

This is the **Infrastructure Intelligence Foundation** - Phase 6E.6 of the FOOL Platform architecture.

## IMPORTANT: What This IS

This phase implements the **Infrastructure Intelligence Core**:

✅ Infrastructure entities  
✅ Infrastructure lifecycle  
✅ Assertions  
✅ Relationships  
✅ Evidence linkage  
✅ Confidence tracking  
✅ Version history  
✅ Registry-driven taxonomy  
✅ Deterministic services  
✅ Explainable validation  

## IMPORTANT: What This Is NOT

This phase does **NOT** perform:

- ❌ DNS Resolution
- ❌ Passive DNS
- ❌ WHOIS
- ❌ External Enrichment
- ❌ Internet Access
- ❌ Threat Hunting
- ❌ Detection Logic
- ❌ AI/LLM

**Infrastructure is a managed intelligence entity. It is NOT a scanner. It is NOT an external data source.**

## Architectural Principle

```
Infrastructure → Assertions → Evidence
                    ↓
            Lifecycle Management
                    ↓
            Relationship Tracking
                    ↓
            Version History
                    ↓
            Registry-Driven Taxonomy
```

**Infrastructure represents intelligence knowledge about assets, hosting, network presence, communication endpoints, certificates, autonomous systems, cloud resources, and related operational objects.**

## Module Structure

```
threat_intelligence/infrastructure/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── enums.py
│   ├── base.py
│   ├── infrastructure.py
│   └── assertion.py
│   └── lifecycle.py
├── taxonomy/
│   ├── __init__.py
│   └── registries.py
├── service.py
├── lifecycle.py
├── validation.py
├── events.py
├── queries.py
└── tests/
    ├── __init__.py
    └── test_infrastructure.py
```

## Infrastructure Types

| Type | Description |
|------|-------------|
| `ip_address` | IP Address |
| `domain` | Domain |
| `subdomain` | Subdomain |
| `fqdn` | Fully Qualified Domain Name |
| `hostname` | Hostname |
| `url_endpoint` | URL Endpoint |
| `cloud_asset` | Cloud Asset |
| `server` | Server |
| `vps` | Virtual Private Server |
| `dedicated_host` | Dedicated Host |
| `cdn` | Content Delivery Network |
| `proxy` | Proxy Server |
| `vpn` | VPN Server |
| `tor_node` | Tor Node |
| `gateway` | Gateway |
| `load_balancer` | Load Balancer |
| `asn` | Autonomous System Number |
| `cidr` | CIDR Block |
| `certificate` | SSL/TLS Certificate |
| `name_server` | Name Server |
| `mail_server` | Mail Server |
| `container_endpoint` | Container Endpoint |
| `kubernetes_endpoint` | Kubernetes Endpoint |
| `custom` | Custom Infrastructure |

## Infrastructure Roles

| Role | Description |
|------|-------------|
| `command_control` | Command and Control |
| `delivery` | Delivery Infrastructure |
| `exfiltration` | Data Exfiltration |
| `hosting` | Hosting Infrastructure |
| `scanning` | Scanning Infrastructure |
| `attack` | Attack Infrastructure |
| `phishing` | Phishing Infrastructure |
| `staging` | Staging Infrastructure |
| `support` | Support Infrastructure |

## Lifecycle States

```
draft → observed → validated → published → active → deprecated → archived
                                                    ↓
                                               revoked
```

Valid transitions:
- draft → observed, archived
- observed → validated, archived
- validated → published, archived
- published → active, deprecated, archived
- active → deprecated, archived
- deprecated → active, archived
- revoked → archived

## Services

### InfrastructureService

```python
from threat_intelligence.infrastructure import InfrastructureService

service = InfrastructureService()

infra = service.create(
    name="C2 Server",
    infrastructure_type="ip_address",
    value="1.2.3.4",
    role="command_control",
    author="analyst",
)

infrastructure = service.get(infra.id)
results = service.find_by_type("ip_address")
results = service.find_by_status("active")
```

### InfrastructureLifecycleService

```python
from threat_intelligence.infrastructure import InfrastructureLifecycleService

service = InfrastructureLifecycleService()

success, msg = service.transition(
    "infra-1",
    "observed",
    reason="Starting observation",
    transitioned_by="user",
)
```

### InfrastructureQueryService

```python
from threat_intelligence.infrastructure import InfrastructureQueryService

service = InfrastructureQueryService()

results = service.find_by_type("ip_address")
results = service.find_by_actor("actor-1")
results = service.find_by_malware("malware-1")
results = service.find_by_campaign("campaign-1")
```

## Taxonomy Registries

```python
from threat_intelligence.infrastructure.taxonomy import (
    InfrastructureTypeRegistry,
    InfrastructureRoleRegistry,
    RelationshipRegistry,
)

# Get all types
types = InfrastructureTypeRegistry.get_types()

# Get description
desc = InfrastructureTypeRegistry.get_description("ip_address")

# Check validity
is_valid = InfrastructureTypeRegistry.is_valid("ip_address")
```

## Assertions

Infrastructure assertions are governed claims about infrastructure:

```python
assertion = InfrastructureAssertion(
    infrastructure_id="infra-1",
    assertion_type="hosting",
    assertion="Infrastructure hosts malware",
    status="pending",
    evidence_ids=("evidence-1",),
)
```

## Relationships

Infrastructure can be related to:

- Threat Actors
- Campaigns
- Malware
- Indicators
- Other Infrastructure
- Certificates
- Services
- Cloud Resources

```python
relationship = InfrastructureRelationship(
    infrastructure_id="infra-1",
    source_type="infrastructure",
    source_id="infra-1",
    target_type="malware",
    target_id="malware-1",
    relationship_type="hosts",
)
```

## Architecture Boundaries

### Allowed Dependencies

- ✅ `standards` - Standard definitions
- ✅ `contracts` - Domain contracts
- ✅ `domain` - Domain models
- ✅ `knowledge` - Knowledge graph
- ✅ `inference` - Inference engine
- ✅ `intelligence` - Intelligence runtime
- ✅ `cyber domain` - Cyber domain
- ✅ `Python standard library` - Standard library only

### Forbidden Dependencies

- ❌ `AI` - AI/ML components
- ❌ `LLM` - LLM components
- ❌ `connectors` - Data connectors
- ❌ `exchange` - Exchange integrations
- ❌ `TAXII` - TAXII
- ❌ `STIX Import` - STIX import
- ❌ `DNS Resolution` - DNS resolution
- ❌ `WHOIS` - WHOIS lookup
- ❌ `Passive DNS` - Passive DNS
- ❌ `Internet` - Internet access
- ❌ `APIs` - External APIs
- ❌ `databases` - Database integrations

## Key Principles

1. **Infrastructure is managed** - All changes are tracked
2. **Deterministic** - All logic is deterministic, no probability
3. **Explainable** - Every assessment has an explanation
4. **Auditable** - Complete audit trail
5. **Versioned** - All changes are versioned
6. **No AI** - No probabilistic AI or LLM
7. **No external data** - No internet access, no external services
8. **Registry-driven** - Taxonomy comes from registries

## Next Phase

**Phase 6E.7 — Infrastructure Management Foundation**

This will implement:
- Infrastructure correlation
- Infrastructure reporting
- Infrastructure metrics
