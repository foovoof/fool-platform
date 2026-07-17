# Executive Intelligence Portal Foundation

## Phase 8E

This is the **Executive Intelligence Portal Foundation** - Phase 8E of the FOOL Platform architecture.

This is the **canonical executive consumption product** of the FOOL Reference Intelligence Platform.

## EXECUTIVE ARCHITECTURAL PRINCIPLE

```
Knowledge Platform
        │
owns intelligence
        │
Threat Intelligence Platform
        │
governs intelligence
        │
Publishing Platform
        │
publishes intelligence
        │
Executive Portal
        │
consumes intelligence
```

## BASE RULE

> **Consume, Never Mutate**

The Portal is strictly forbidden from creating, modifying, or redefining any internal knowledge.

## IMPORTANT: What This IS

This phase implements the **Executive Intelligence Portal**:

✅ Executive Workspaces  
✅ Dashboards (reference-only)  
✅ Strategic Briefings (reference-only)  
✅ Publication Feeds (reference-only)  
✅ Executive Collections (reference-only)  
✅ Bookmarks  
✅ Saved Searches  
✅ Navigation  
✅ Session Management  
✅ Audit Trail  
✅ Widget Framework  
✅ Personalization  
✅ Export (reference-only)  
✅ Event emission  

## IMPORTANT: What This Is NOT

This phase does **NOT** perform:

- ❌ Knowledge Creation
- ❌ Knowledge Modification
- ❌ Threat Analysis
- ❌ Correlation
- ❌ Detection
- ❌ Threat Hunting
- ❌ Investigation
- ❌ Evidence Storage
- ❌ Publishing
- ❌ Workflow Execution
- ❌ AI/LLM
- ❌ SOAR
- ❌ Automation
- ❌ External Connectors

## Module Structure

```
executive_portal/
├── __init__.py
├── runtime.py
├── events.py
└── models/
    ├── __init__.py
    ├── enums.py
    ├── base.py
    ├── core.py
    ├── session.py
    ├── dashboard/
    │   ├── __init__.py
    │   └── dashboard.py
    ├── briefing/
    │   ├── __init__.py
    │   └── briefing.py
    ├── collection/
    │   ├── __init__.py
    │   └── collection.py
    └── widget/
        ├── __init__.py
        └── widget.py
```

## Aggregate Roots

| Aggregate Root | Purpose |
|---------------|---------|
| `ExecutiveWorkspace` | Executive workspace |
| `ExecutiveDashboard` | Dashboard consumption |
| `StrategicBriefing` | Strategic briefing consumption |
| `ExecutiveCollection` | Collection management |
| `PublicationFeed` | Publication feed |
| `ExecutiveSession` | Session management |

## Reference Models (NEVER duplicated)

| Model | Platform Entity |
|-------|----------------|
| `PublicationReference` | Platform Publication |
| `ReportReference` | Platform Report |
| `EvidenceReference` | Platform Evidence |
| `MetricReference` | Platform Metric |
| `CollectionReference` | Platform Collection |

## Runtime Services

| Service | Purpose |
|---------|---------|
| `WorkspaceManager` | Workspace management |
| `DashboardManager` | Dashboard management |
| `BriefingManager` | Briefing management |
| `CollectionManager` | Collection management |
| `FeedManager` | Feed management |
| `BookmarkManager` | Bookmark management |
| `SearchManager` | Search management |
| `SessionManager` | Session management |
| `AuditManager` | Audit management |
| `WidgetRegistry` | Widget registration |

## Events

- `workspace.created`
- `workspace.opened`
- `workspace.updated`
- `dashboard.created`
- `dashboard.opened`
- `widget.added`
- `widget.removed`
- `briefing.created`
- `briefing.published`
- `collection.created`
- `bookmark.added`
- `search.executed`
- `session.started`
- `session.ended`
- `view.opened`

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
- ❌ `Detection engines` - Detection execution
- ❌ `SOAR` - SOAR
- ❌ **Knowledge Creation** - Creating/modifying intelligence

## Guiding Principle

> **Consume, Never Mutate**
>
> The Portal presents.
> The Platform owns.
>
> Portals are replaceable.
> The Platform is the foundation.

## Product Chain

```
Platform
        │
owns intelligence
        ▼
Analyst Workspace
        │
Analyze
        ▼
Investigation Workspace
        │
Investigate
        ▼
Threat Intelligence Workbench
        │
Govern
        ▼
Publishing & Dissemination
        │
Publish
        ▼
Executive Intelligence Portal
        │
Consume
```

## Ready for

- ✅ Web UI
- ✅ Desktop UI
- ✅ Mobile UI
- ✅ REST API
- ✅ Future AI copilots (consuming only)

## Next Phase

**Phase 8F — Product Suite Integration & Certification**
