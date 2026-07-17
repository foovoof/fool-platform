"""
executive_portal/__init__.py

Executive Intelligence Portal Module.

Phase 8E - Executive Intelligence Portal Foundation.

IMPORTANT: The Portal consumes intelligence.
It NEVER creates, modifies, or duplicates it.

EXECUTIVE ARCHITECTURAL PRINCIPLE:
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

BASE RULE:
> Consume, Never Mutate

The Portal is strictly forbidden from creating, modifying,
or redefining any internal knowledge.
"""
from executive_portal.models import (
    # Enums
    WidgetType,
    DashboardStatus,
    BriefingStatus,
    SessionStatus,
    AuditAction,
    # Base
    PortalBase,
    Auditable,
    ReferenceOnly,
    # Core
    ExecutiveWorkspace,
    ExecutiveBookmark,
    SavedSearch,
    Filter,
    NavigationItem,
    NavigationTree,
    PublicationFeed,
    ExecutivePreference,
    ExecutiveSnapshot,
    # Session
    ExecutiveSession,
    DashboardSession,
    SessionState,
    ViewHistory,
    AuditEntry,
    HistoryEntry,
    # Dashboard
    ExecutiveDashboard,
    DashboardLayout,
    DashboardSection,
    DashboardView,
    DashboardState,
    WidgetReference,
    WidgetConfiguration,
    WidgetMetadata,
    # Briefing
    StrategicBriefing,
    BriefingSection,
    BriefingVersion,
    BriefingHistory,
    BriefingMetadata,
    BriefingApproval,
    ExecutiveSummary,
    # Collection
    ExecutiveCollection,
    CollectionReference,
    CollectionHistory,
    CollectionMetadata,
    # Widget
    ExecutiveWidget,
    WidgetContext,
    WidgetProvider,
    PublicationReference,
    ReportReference,
    EvidenceReference,
    MetricReference,
)

from executive_portal.runtime import (
    WorkspaceManager,
    DashboardManager,
    BriefingManager,
    CollectionManager,
    FeedManager,
    BookmarkManager,
    SearchManager,
    SessionManager,
    AuditManager,
    WidgetRegistry,
)

from executive_portal.events import (
    PortalEventEmitter,
    PortalEventType,
)

__all__ = [
    # Models
    "ExecutiveWorkspace",
    "ExecutiveDashboard",
    "StrategicBriefing",
    "ExecutiveCollection",
    "ExecutiveWidget",
    "ExecutiveBookmark",
    "PublicationFeed",
    "ExecutivePreference",
    "ExecutiveSnapshot",
    "ExecutiveSession",
    "DashboardSession",
    "SessionState",
    "ViewHistory",
    "AuditEntry",
    "HistoryEntry",
    "SavedSearch",
    "Filter",
    "NavigationItem",
    "NavigationTree",
    "WidgetReference",
    "WidgetConfiguration",
    "WidgetMetadata",
    "BriefingSection",
    "BriefingVersion",
    "BriefingHistory",
    "BriefingMetadata",
    "BriefingApproval",
    "ExecutiveSummary",
    "CollectionReference",
    "CollectionHistory",
    "CollectionMetadata",
    "WidgetContext",
    "WidgetProvider",
    "PublicationReference",
    "ReportReference",
    "EvidenceReference",
    "MetricReference",
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
    # Runtime
    "WorkspaceManager",
    "DashboardManager",
    "BriefingManager",
    "CollectionManager",
    "FeedManager",
    "BookmarkManager",
    "SearchManager",
    "SessionManager",
    "AuditManager",
    "WidgetRegistry",
    # Events
    "PortalEventEmitter",
    "PortalEventType",
]
