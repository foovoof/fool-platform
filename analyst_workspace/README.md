# Analyst Workspace Foundation

## Phase 8A

This is the **Analyst Workspace Foundation** - Phase 8A of the FOOL Platform architecture.

This is the **first official product built on top of the FOOL Reference Intelligence Platform.**

## IMPORTANT: What This IS

This phase implements the **Analyst Workspace Product Layer**:

✅ Workspace domain  
✅ Workspace models  
✅ Workspace runtime  
✅ Session management  
✅ Navigation  
✅ Views (consuming platform)  
✅ Panels (consuming platform)  
✅ Commands  
✅ Bookmarks/Favorites  
✅ Preferences  
✅ Event emission  
✅ Extensibility framework  

## IMPORTANT: What This Is NOT

This phase does **NOT** perform:

- ❌ Detection Logic
- ❌ Correlation Logic
- ❌ Threat Hunting Logic
- ❌ Investigation Logic
- ❌ Knowledge Modification
- ❌ Inference
- ❌ AI/LLM
- ❌ Copilot
- ❌ Chat Interface
- ❌ External Connectors
- ❌ Business Rules
- ❌ Persistence Engines
- ❌ SOC Dashboards
- ❌ SOAR
- ❌ Response Automation

## Architectural Principle

```
Reference Platform
        │
        ├── Knowledge
        ├── Intelligence
        ├── CTI
        ├── Exchange
        ├── Hunting
        ├── Incident
        └── Reporting
                │
                ▼
Analyst Workspace
```

**The workspace consumes platform capabilities. It never owns them.**

## Module Structure

```
analyst_workspace/
├── __init__.py
├── runtime.py
├── events.py
├── models/
│   ├── __init__.py
│   ├── enums.py
│   ├── base.py
│   ├── workspace.py
│   ├── session.py
│   ├── navigation.py
│   ├── bookmarks.py
│   ├── commands.py
│   └── notifications.py
└── tests/
    ├── __init__.py
    └── test_analyst_workspace.py
```

## Core Models

### Workspace
- Main workspace entity
- Layouts
- Preferences
- Context

### WorkspaceSession
- Session tracking
- Snapshots
- History
- Recovery

### Navigation
- Navigation tree
- Breadcrumbs
- Recently opened
- Back/forward

### Views
- Knowledge View
- Entity View
- Relationship View
- Evidence View
- Report View
- Investigation View
- Search View
- Timeline View
- Graph View
- Analytics View

### Panels
- Entity Details
- Relationship Details
- Evidence Panel
- Properties
- Metadata
- History
- Audit Trail
- Confidence
- Assertions
- References
- Notes

### Commands
- Open
- Close
- Compare
- Pin
- Bookmark
- Inspect
- Navigate
- Export
- Share
- Copy Reference

## Runtime Services

| Service | Purpose |
|---------|---------|
| `WorkspaceRuntime` | Main workspace management |
| `WorkspaceSessionManager` | Session lifecycle |
| `WorkspaceContextManager` | Context management |
| `WorkspaceNavigationManager` | Navigation management |
| `WorkspaceStateManager` | State management |
| `WorkspaceCommandDispatcher` | Command dispatch |
| `WorkspaceLifecycleManager` | Lifecycle management |
| `ViewRegistry` | View registration |
| `PanelRegistry` | Panel registration |

## Events

- `workspace.created`
- `workspace.loaded`
- `workspace.closed`
- `workspace.saved`
- `workspace.restored`
- `view.opened`
- `view.closed`
- `panel.opened`
- `selection.changed`
- `command.executed`

## Design Principles

The Analyst Workspace is:

1. **Platform-driven** - Consumes platform capabilities
2. **Modular** - Plugin-extensible
3. **Deterministic** - All logic is deterministic
4. **Explainable** - Every action is explainable
5. **Auditable** - Complete audit trail
6. **Replayable** - User actions can be replayed
7. **Replaceable** - Product layer is replaceable

## Extensibility

Every component supports:
- Plugin Registration
- View Registration
- Panel Registration
- Command Registration
- Layout Registration

No hard-coded components.

## Guiding Principle

> The Analyst Workspace provides a unified, governed, deterministic, explainable, and extensible working environment for intelligence analysts.
>
> It consumes the platform.
> It never owns it.
>
> The workspace is a product.
> The platform is the foundation.
>
> Products are replaceable.
> Platforms are not.

## Architecture Boundaries

### Allowed Dependencies

- ✅ `standards` - Standard definitions
- ✅ `contracts` - Domain contracts
- ✅ `domain` - Domain models
- ✅ `knowledge` - Knowledge graph
- ✅ `inference` - Inference engine
- ✅ `intelligence` - Intelligence runtime
- ✅ `cti_core` - CTI Core
- ✅ `threat_intelligence` - Threat Intelligence
- ✅ `threat_hunting` - Threat Hunting
- ✅ `reporting` - Reporting
- ✅ `Python standard library` - Standard library only

### Forbidden Dependencies

- ❌ `Applications` - Application layer
- ❌ `AI` - AI/ML components
- ❌ `Connectors` - Data connectors
- ❌ `Exchange` - Exchange adapters
- ❌ `Detection engines` - Detection execution
- ❌ `SOAR` - SOAR
- ❌ `Persistence` - Persistence engines
- ❌ `Business Logic` - Business rules

## Ready for

- Investigation Workspace
- Threat Intelligence Workbench
- Reporting Portal
- Management Console
- Web UI
- Desktop UI
- Mobile UI
- REST API
- Future AI copilots

## Next Phase

**Phase 8B — Investigation Workspace Foundation**
