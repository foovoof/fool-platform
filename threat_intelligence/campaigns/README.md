# Campaign Intelligence Core

## Phase 6E.4

This is the **Campaign Intelligence Foundation** - Phase 6E.4 of the FOOL Platform architecture.

## IMPORTANT: What This IS

This phase implements the **Campaign Intelligence Core**:

✅ Campaign management  
✅ Timeline tracking  
✅ Assertion management  
✅ Evidence management  
✅ Relationship tracking  
✅ Lifecycle management  
✅ Governance (approval, review, audit)  
✅ Versioning  
✅ Queries  

## IMPORTANT: What This Is NOT

This phase does **NOT** implement:

- ❌ Attribution
- ❌ Campaign Analysis
- ❌ Threat Hunting
- ❌ Detection
- ❌ Correlation
- ❌ ATT&CK Mapping
- ❌ Sigma
- ❌ YARA
- ❌ External Feeds
- ❌ Internet Access
- ❌ AI/LLM
- ❌ Autonomous Decisions

**Campaign is a governed intelligence entity. Campaign is NOT an analytical conclusion.**

## Architectural Principle

```
Campaign → Assertions → Evidence
               ↓
         Timeline Management
               ↓
         Lifecycle Management
               ↓
         Governance (Approval/Review/Audit)
               ↓
         Versioning & Audit Trail
```

**Campaign organizes intelligence around coordinated activities while remaining independent from attribution and operational analysis.**

## Module Structure

```
threat_intelligence/campaigns/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── enums.py
│   ├── base.py
│   ├── campaign.py
│   ├── timeline.py
│   ├── assertion.py
│   ├── evidence.py
│   ├── relationships.py
│   ├── lifecycle.py
│   ├── governance.py
│   └── versioning.py
├── repositories/
│   ├── __init__.py
│   ├── base.py
│   └── inmemory.py
├── services/
│   ├── __init__.py
│   ├── campaign_service.py
│   ├── assertion_service.py
│   ├── timeline_service.py
│   ├── evidence_service.py
│   ├── relationship_service.py
│   ├── lifecycle_service.py
│   ├── governance_service.py
│   └── version_service.py
├── validation.py
├── queries.py
├── events.py
├── registry.py
└── tests/
    ├── __init__.py
    └── test_campaigns.py
```

## Core Concepts

### Campaign

A Campaign is a governed intelligence entity that organizes intelligence around coordinated activities.

```python
from threat_intelligence.campaigns import Campaign, CampaignService

service = CampaignService()

campaign = service.create(
    name="Operation Aurora",
    description="Cyber espionage operation",
    author="analyst",
)
```

### Assertions

Assertions are governed, explainable claims about a campaign.

```python
from threat_intelligence.campaigns import AssertionService

service = AssertionService()

assertion = service.create(
    campaign_id=campaign.id,
    assertion_type="observation",
    assertion="Attacker used spear phishing",
    author="analyst",
)
```

### Timeline

Timeline tracks events and milestones for a campaign.

```python
from threat_intelligence.campaigns import TimelineService

service = TimelineService()

event = service.create_event(
    campaign_id=campaign.id,
    event_type="attack",
    timestamp="2024-01-15T10:00:00Z",
    description="Attack detected",
    author="analyst",
)

milestone = service.create_milestone(
    campaign_id=campaign.id,
    name="Initial Access",
    target_date="2024-01-15",
    author="analyst",
)
```

### Evidence

Evidence links supporting data to campaigns.

```python
from threat_intelligence.campaigns import EvidenceService

service = EvidenceService()

evidence = service.create(
    campaign_id=campaign.id,
    evidence_type="direct",
    title="Phishing Email",
    description="Email header analysis",
    author="analyst",
)
```

### Lifecycle

Campaign lifecycle manages status transitions.

```python
from threat_intelligence.campaigns import LifecycleService

service = LifecycleService()

success, msg = service.transition(
    "campaign-1",
    "active",
    reason="Starting campaign",
    transitioned_by="user",
)
```

Valid transitions:
- planned → proposed, active, cancelled, archived
- proposed → active, cancelled, archived
- active → on_hold, completed, cancelled
- on_hold → active, completed, cancelled
- completed → archived
- cancelled → archived

### Governance

Governance handles approvals, reviews, and audit trails.

```python
from threat_intelligence.campaigns import GovernanceService

service = GovernanceService()

approval = service.create_approval(
    campaign_id="campaign-1",
    approval_type="create",
    author="analyst",
)

service.approve(
    approval.id,
    approver="admin",
    comments="Approved",
)
```

### Versioning

Versioning tracks changes to campaigns.

```python
from threat_intelligence.campaigns import VersionService

service = VersionService()

version = service.create_version(
    campaign_id="campaign-1",
    changes="Initial version",
    changes_summary="Initial creation",
    changed_by="analyst",
    change_reason="Created campaign",
)
```

## Supported Entities

### Campaign

| Field | Description |
|-------|-------------|
| `id` | UUID identifier |
| `name` | Campaign name |
| `description` | Description |
| `status` | planned, proposed, active, on_hold, completed, cancelled, archived |
| `severity` | critical, high, medium, low, informational |
| `confidence_level` | high, medium, low |
| `confidence_score` | 0.0 - 1.0 |
| `start_date` | Start date |
| `end_date` | End date |
| `first_observed` | First observed |
| `last_observed` | Last observed |
| `aliases` | Alternative names |
| `objectives` | Campaign objectives |
| `motivations` | Attacker motivations |
| `sectors` | Targeted sectors |
| `geographies` | Targeted geographies |
| `associated_actors` | Related threat actors |
| `associated_malware` | Related malware |
| `associated_infrastructure` | Related infrastructure |
| `associated_indicators` | Related indicators |
| `associated_evidence` | Related evidence |
| `associated_assertions` | Related assertions |

### CampaignAssertion

| Field | Description |
|-------|-------------|
| `id` | UUID identifier |
| `campaign_id` | Parent campaign |
| `assertion_type` | observation, inference, attribution, relationship, timeline, capability, intent, impact |
| `assertion` | Assertion content |
| `status` | pending, confirmed, disputed, refuted, unverified |
| `evidence_ids` | Supporting evidence |
| `confidence_level` | Confidence level |
| `confidence_score` | 0.0 - 1.0 |

### TimelineEvent

| Field | Description |
|-------|-------------|
| `id` | UUID identifier |
| `campaign_id` | Parent campaign |
| `event_type` | Event type |
| `timestamp` | Event timestamp |
| `description` | Description |
| `evidence_ids` | Related evidence |
| `significance` | normal, significant, critical |

### CampaignEvidence

| Field | Description |
|-------|-------------|
| `id` | UUID identifier |
| `campaign_id` | Parent campaign |
| `evidence_type` | direct, circumstantial, corroborating, inconsistent |
| `title` | Evidence title |
| `description` | Description |
| `content` | Evidence content |
| `collected_at` | Collection timestamp |

### CampaignRelationship

| Field | Description |
|-------|-------------|
| `id` | UUID identifier |
| `campaign_id` | Parent campaign |
| `source_type` | Source entity type |
| `source_id` | Source entity ID |
| `target_type` | Target entity type |
| `target_id` | Target entity ID |
| `relationship_type` | Relationship type |

## Relationship Types

| Type | Description |
|------|-------------|
| `uses` | Campaign uses an entity |
| `targets` | Campaign targets an entity |
| `delivers` | Campaign delivers an entity |
| `exploits` | Campaign exploits an entity |
| `attributed_to` | Campaign attributed to entity |
| `associated_with` | Campaign associated with entity |
| `part_of` | Entity is part of campaign |
| `operates_in` | Campaign operates in sector/geography |
| `affects` | Campaign affects entity |
| `deploys` | Campaign deploys entity |
| `utilizes` | Campaign utilizes entity |
| `compromises` | Campaign compromises entity |

## Services

### CampaignService

```python
from threat_intelligence.campaigns import CampaignService

service = CampaignService()

campaign = service.create(
    name="Campaign Name",
    description="Description",
    author="analyst",
)

campaigns = service.list_all()
campaign = service.get(campaign.id)
campaigns = service.search({"status": "active"})
```

### AssertionService

```python
from threat_intelligence.campaigns import AssertionService

service = AssertionService()

assertion = service.create(
    campaign_id="campaign-1",
    assertion_type="observation",
    assertion="Assertion content",
    author="analyst",
)

assertions = service.find_by_campaign("campaign-1")
```

### TimelineService

```python
from threat_intelligence.campaigns import TimelineService

service = TimelineService()

event = service.create_event(
    campaign_id="campaign-1",
    event_type="attack",
    timestamp="2024-01-15T10:00:00Z",
    description="Event description",
    author="analyst",
)

events = service.find_events_by_campaign("campaign-1")
```

### EvidenceService

```python
from threat_intelligence.campaigns import EvidenceService

service = EvidenceService()

evidence = service.create(
    campaign_id="campaign-1",
    evidence_type="direct",
    title="Evidence Title",
    description="Evidence description",
    author="analyst",
)

evidence_list = service.find_by_campaign("campaign-1")
```

### LifecycleService

```python
from threat_intelligence.campaigns import LifecycleService

service = LifecycleService()

success, msg = service.transition(
    "campaign-1",
    "active",
    reason="Starting",
    transitioned_by="user",
)

status = service.get_status("campaign-1")
```

### GovernanceService

```python
from threat_intelligence.campaigns import GovernanceService

service = GovernanceService()

approval = service.create_approval(
    campaign_id="campaign-1",
    approval_type="create",
    author="analyst",
)

service.approve(approval.id, approver="admin")
service.reject(approval.id, approver="admin", rejection_reason="...")

audit_trail = service.get_audit_trail("campaign-1")
```

### VersionService

```python
from threat_intelligence.campaigns import VersionService

service = VersionService()

version = service.create_version(
    campaign_id="campaign-1",
    changes="Change description",
    changes_summary="Summary",
    changed_by="analyst",
    change_reason="Reason",
)

history = service.get_history("campaign-1")
```

## Query Service

```python
from threat_intelligence.campaigns import CampaignQueryService

service = CampaignQueryService()

campaigns = service.find_by_actor("actor-1")
campaigns = service.find_by_malware("malware-1")
campaigns = service.find_by_status("active")
campaigns = service.find_by_sector("finance")
campaigns = service.find_by_geography("US")
```

## Architecture Boundaries

### Allowed Dependencies

- ✅ `standards` - Standard definitions
- ✅ `contracts` - Domain contracts
- ✅ `domain` - Domain models
- ✅ `knowledge` - Knowledge graph
- ✅ `inference` - Inference engine
- ✅ `threat_intelligence` - Threat intelligence
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

1. **Campaign is governed** - All changes require approval/review
2. **Deterministic** - All logic is deterministic, no probability
3. **Explainable** - Every assertion has an explanation
4. **Auditable** - Complete audit trail
5. **Versioned** - All changes are versioned
6. **No AI** - No probabilistic AI or LLM
7. **No attribution** - Campaign does not imply attribution
8. **No analysis** - Campaign is not analytical output

## Next Phase

**Phase 6E.5 — Campaign Management Foundation**

This will implement:
- Campaign correlation
- Campaign reporting
- Campaign visualization
- Campaign metrics
