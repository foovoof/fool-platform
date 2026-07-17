"""
analyst_workspace/models/__init__.py

Analyst Workspace Models.
"""
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

from analyst_workspace.models.base import (
    WorkspaceBase,
    Auditable,
    Versionable,
    TimestampMixin,
)

from analyst_workspace.models.workspace import (
    Workspace,
    WorkspaceLayout,
    WorkspaceState,
    WorkspacePreference,
    WorkspaceProfile,
    WorkspaceContext,
    WorkspaceSelection,
)

from analyst_workspace.models.session import (
    WorkspaceSession,
    SessionSnapshot,
    SessionHistory,
)

from analyst_workspace.models.navigation import (
    NavigationNode,
    Breadcrumb,
    NavigationState,
    RecentlyOpened,
)

from analyst_workspace.models.bookmarks import (
    WorkspaceBookmark,
    WorkspaceFavorite,
    CrossReference,
)

from analyst_workspace.models.commands import (
    CommandDefinition,
    CommandExecution,
    WorkspaceCommand,
)

from analyst_workspace.models.notifications import (
    WorkspaceNotification,
    ViewDefinition,
    PanelDefinition,
    OpenView,
    OpenPanel,
)

__all__ = [
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
    # Base
    "WorkspaceBase",
    "Auditable",
    "Versionable",
    "TimestampMixin",
    # Workspace
    "Workspace",
    "WorkspaceLayout",
    "WorkspaceState",
    "WorkspacePreference",
    "WorkspaceProfile",
    "WorkspaceContext",
    "WorkspaceSelection",
    # Session
    "WorkspaceSession",
    "SessionSnapshot",
    "SessionHistory",
    # Navigation
    "NavigationNode",
    "Breadcrumb",
    "NavigationState",
    "RecentlyOpened",
    # Bookmarks
    "WorkspaceBookmark",
    "WorkspaceFavorite",
    "CrossReference",
    # Commands
    "CommandDefinition",
    "CommandExecution",
    "WorkspaceCommand",
    # Notifications
    "WorkspaceNotification",
    "ViewDefinition",
    "PanelDefinition",
    "OpenView",
    "OpenPanel",
]
