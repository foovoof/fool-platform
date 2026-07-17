"""
executive_portal/models/__init__.py

Executive Portal Models.
"""
from executive_portal.models.enums import (
    WidgetType,
    DashboardStatus,
    BriefingStatus,
    SessionStatus,
    AuditAction,
)

from executive_portal.models.base import (
    PortalBase,
    Auditable,
    ReferenceOnly,
)

from executive_portal.models.core import (
    ExecutiveWorkspace,
    ExecutiveBookmark,
    SavedSearch,
    Filter,
    NavigationItem,
    NavigationTree,
    PublicationFeed,
    ExecutivePreference,
    ExecutiveSnapshot,
)

from executive_portal.models.session import (
    ExecutiveSession,
    DashboardSession,
    SessionState,
    ViewHistory,
    AuditEntry,
    HistoryEntry,
)

from executive_portal.models.dashboard import (
    ExecutiveDashboard,
    DashboardLayout,
    DashboardSection,
    DashboardView,
    DashboardState,
    WidgetReference,
    WidgetConfiguration,
    WidgetMetadata,
)

from executive_portal.models.briefing import (
    StrategicBriefing,
    BriefingSection,
    BriefingVersion,
    BriefingHistory,
    BriefingMetadata,
    BriefingApproval,
    ExecutiveSummary,
)

from executive_portal.models.collection import (
    ExecutiveCollection,
    CollectionReference,
    CollectionHistory,
    CollectionMetadata,
)

from executive_portal.models.widget import (
    ExecutiveWidget,
    WidgetContext,
    WidgetProvider,
    PublicationReference,
    ReportReference,
    EvidenceReference,
    MetricReference,
)

__all__ = [
    # Enums
    "WidgetType",
    "DashboardStatus",
    "BriefingStatus",
    "SessionStatus",
    "AuditAction",
    # Base
    "PortalBase",
    "Auditable",
    "ReferenceOnly",
    # Core
    "ExecutiveWorkspace",
    "ExecutiveBookmark",
    "SavedSearch",
    "Filter",
    "NavigationItem",
    "NavigationTree",
    "PublicationFeed",
    "ExecutivePreference",
    "ExecutiveSnapshot",
    # Session
    "ExecutiveSession",
    "DashboardSession",
    "SessionState",
    "ViewHistory",
    "AuditEntry",
    "HistoryEntry",
    # Dashboard
    "ExecutiveDashboard",
    "DashboardLayout",
    "DashboardSection",
    "DashboardView",
    "DashboardState",
    "WidgetReference",
    "WidgetConfiguration",
    "WidgetMetadata",
    # Briefing
    "StrategicBriefing",
    "BriefingSection",
    "BriefingVersion",
    "BriefingHistory",
    "BriefingMetadata",
    "BriefingApproval",
    "ExecutiveSummary",
    # Collection
    "ExecutiveCollection",
    "CollectionReference",
    "CollectionHistory",
    "CollectionMetadata",
    # Widget
    "ExecutiveWidget",
    "WidgetContext",
    "WidgetProvider",
    "PublicationReference",
    "ReportReference",
    "EvidenceReference",
    "MetricReference",
]
