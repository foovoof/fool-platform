"""
analyst_workspace/__init__.py

Analyst Workspace Module.

Phase 8A - Analyst Workspace Foundation.

IMPORTANT: This module does NOT perform:
- Detection Logic
- Correlation Logic
- Threat Hunting Logic
- Investigation Logic
- Knowledge Modification
- Inference
- AI/LLM
- Copilot
- Chat Interface
- External Connectors
- Business Rules
- Persistence Engines
- SOC Dashboards
- SOAR
- Response Automation

The Analyst Workspace is a Product Layer that consumes platform capabilities.
It never owns them.
"""
from analyst_workspace.models import (
    Workspace,
    WorkspaceSession,
    WorkspaceLayout,
    WorkspaceState,
    WorkspacePreference,
    WorkspaceProfile,
    WorkspaceContext,
    WorkspaceSelection,
    NavigationNode,
    Breadcrumb,
    NavigationState,
    RecentlyOpened,
    WorkspaceBookmark,
    WorkspaceFavorite,
    CrossReference,
    CommandDefinition,
    CommandExecution,
    WorkspaceCommand,
    WorkspaceNotification,
    ViewDefinition,
    PanelDefinition,
    OpenView,
    OpenPanel,
    SessionSnapshot,
    SessionHistory,
)

from analyst_workspace.models.enums import (
    WorkspaceStatus,
    SessionStatus,
    ViewType,
    PanelType,
    CommandScope,
    NotificationLevel,
    Theme,
    Language,
    TimeFormat,
)

from analyst_workspace.runtime import (
    WorkspaceRuntime,
    WorkspaceSessionManager,
    WorkspaceContextManager,
    WorkspaceNavigationManager,
    WorkspaceStateManager,
    WorkspaceCommandDispatcher,
    WorkspaceLifecycleManager,
    ViewRegistry,
    PanelRegistry,
)

from analyst_workspace.events import (
    WorkspaceEventEmitter,
    WorkspaceEventType,
)

__all__ = [
    # Models
    "Workspace",
    "WorkspaceSession",
    "WorkspaceLayout",
    "WorkspaceState",
    "WorkspacePreference",
    "WorkspaceProfile",
    "WorkspaceContext",
    "WorkspaceSelection",
    "NavigationNode",
    "Breadcrumb",
    "NavigationState",
    "RecentlyOpened",
    "WorkspaceBookmark",
    "WorkspaceFavorite",
    "CrossReference",
    "CommandDefinition",
    "CommandExecution",
    "WorkspaceCommand",
    "WorkspaceNotification",
    "ViewDefinition",
    "PanelDefinition",
    "OpenView",
    "OpenPanel",
    "SessionSnapshot",
    "SessionHistory",
    # Enums
    "WorkspaceStatus",
    "SessionStatus",
    "ViewType",
    "PanelType",
    "CommandScope",
    "NotificationLevel",
    "Theme",
    "Language",
    "TimeFormat",
    # Runtime
    "WorkspaceRuntime",
    "WorkspaceSessionManager",
    "WorkspaceContextManager",
    "WorkspaceNavigationManager",
    "WorkspaceStateManager",
    "WorkspaceCommandDispatcher",
    "WorkspaceLifecycleManager",
    "ViewRegistry",
    "PanelRegistry",
    # Events
    "WorkspaceEventEmitter",
    "WorkspaceEventType",
]
