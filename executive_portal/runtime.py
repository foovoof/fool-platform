"""
executive_portal/runtime.py

Executive Portal Runtime.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from executive_portal.models import (
    ExecutiveWorkspace,
    ExecutiveDashboard,
    StrategicBriefing,
    ExecutiveCollection,
    ExecutiveWidget,
    ExecutiveBookmark,
    PublicationFeed,
    ExecutivePreference,
    ExecutiveSession,
    AuditEntry,
    SavedSearch,
    NavigationTree,
    Filter,
    WidgetMetadata,
    WidgetReference,
    ViewHistory,
    DashboardSession,
)


class InMemoryStorage:
    """Simple in-memory storage."""
    
    def __init__(self) -> None:
        self._workspaces: dict[str, ExecutiveWorkspace] = {}
        self._dashboards: dict[str, ExecutiveDashboard] = {}
        self._briefings: dict[str, StrategicBriefing] = {}
        self._collections: dict[str, ExecutiveCollection] = {}
        self._widgets: dict[str, ExecutiveWidget] = {}
        self._bookmarks: dict[str, ExecutiveBookmark] = {}
        self._feeds: dict[str, PublicationFeed] = {}
        self._preferences: dict[str, ExecutivePreference] = {}
        self._sessions: dict[str, ExecutiveSession] = {}
        self._audit: dict[str, AuditEntry] = {}
        self._searches: dict[str, SavedSearch] = {}
        self._navigation: dict[str, NavigationTree] = {}
        self._widget_metadata: dict[str, WidgetMetadata] = {}


_storage = InMemoryStorage()


class WorkspaceManager:
    """Manages executive workspaces - REFERENCE ONLY."""
    
    def create(
        self,
        name: str,
        owner: str,
        description: str = "",
    ) -> ExecutiveWorkspace:
        """Create workspace."""
        workspace = ExecutiveWorkspace(
            id=str(uuid4()),
            name=name,
            description=description,
            owner=owner,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._workspaces[workspace.id] = workspace
        return workspace
    
    def get(self, workspace_id: str) -> ExecutiveWorkspace | None:
        """Get workspace."""
        return _storage._workspaces.get(workspace_id)
    
    def list_all(self) -> list[ExecutiveWorkspace]:
        """List all workspaces."""
        return list(_storage._workspaces.values())


class DashboardManager:
    """Manages dashboards - REFERENCE ONLY."""
    
    def create(
        self,
        name: str,
        owner: str,
        description: str = "",
    ) -> ExecutiveDashboard:
        """Create dashboard."""
        dashboard = ExecutiveDashboard(
            id=str(uuid4()),
            name=name,
            description=description,
            owner=owner,
            status="active",
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._dashboards[dashboard.id] = dashboard
        return dashboard
    
    def get(self, dashboard_id: str) -> ExecutiveDashboard | None:
        """Get dashboard."""
        return _storage._dashboards.get(dashboard_id)
    
    def add_widget(
        self,
        dashboard_id: str,
        widget: WidgetReference,
    ) -> ExecutiveDashboard | None:
        """Add widget reference to dashboard."""
        dashboard = self.get(dashboard_id)
        if not dashboard:
            return None
        
        updated = ExecutiveDashboard(
            id=dashboard.id,
            name=dashboard.name,
            description=dashboard.description,
            owner=dashboard.owner,
            status=dashboard.status,
            widgets=dashboard.widgets + (widget,),
            layouts=dashboard.layouts,
            views=dashboard.views,
            publication_refs=dashboard.publication_refs,
            report_refs=dashboard.report_refs,
            collection_refs=dashboard.collection_refs,
            tags=dashboard.tags,
            created_at=dashboard.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=dashboard.version + 1,
            metadata=dashboard.metadata,
        )
        _storage._dashboards[updated.id] = updated
        return updated


class BriefingManager:
    """Manages strategic briefings - REFERENCE ONLY."""
    
    def create(
        self,
        title: str,
        owner: str,
        description: str = "",
    ) -> StrategicBriefing:
        """Create briefing."""
        briefing = StrategicBriefing(
            id=str(uuid4()),
            title=title,
            description=description,
            owner=owner,
            status="draft",
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._briefings[briefing.id] = briefing
        return briefing
    
    def get(self, briefing_id: str) -> StrategicBriefing | None:
        """Get briefing."""
        return _storage._briefings.get(briefing_id)


class CollectionManager:
    """Manages executive collections - REFERENCE ONLY."""
    
    def create(
        self,
        name: str,
        owner: str,
        description: str = "",
    ) -> ExecutiveCollection:
        """Create collection."""
        collection = ExecutiveCollection(
            id=str(uuid4()),
            name=name,
            description=description,
            owner=owner,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._collections[collection.id] = collection
        return collection
    
    def get(self, collection_id: str) -> ExecutiveCollection | None:
        """Get collection."""
        return _storage._collections.get(collection_id)


class FeedManager:
    """Manages publication feeds - REFERENCE ONLY."""
    
    def create(
        self,
        name: str,
        description: str = "",
    ) -> PublicationFeed:
        """Create feed."""
        feed = PublicationFeed(
            id=str(uuid4()),
            name=name,
            description=description,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._feeds[feed.id] = feed
        return feed
    
    def get(self, feed_id: str) -> PublicationFeed | None:
        """Get feed."""
        return _storage._feeds.get(feed_id)


class BookmarkManager:
    """Manages bookmarks - REFERENCE ONLY."""
    
    def create(
        self,
        user_id: str,
        name: str,
        ref_id: str,
        ref_type: str,
        ref_source: str,
    ) -> ExecutiveBookmark:
        """Create bookmark."""
        bookmark = ExecutiveBookmark(
            id=str(uuid4()),
            user_id=user_id,
            name=name,
            ref_id=ref_id,
            ref_type=ref_type,
            ref_source=ref_source,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._bookmarks[bookmark.id] = bookmark
        return bookmark


class SearchManager:
    """Manages saved searches."""
    
    def create(
        self,
        user_id: str,
        name: str,
        query: str,
        filters: dict[str, Any] = None,
    ) -> SavedSearch:
        """Create saved search."""
        search = SavedSearch(
            id=str(uuid4()),
            user_id=user_id,
            name=name,
            query=query,
            filters=filters or {},
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._searches[search.id] = search
        return search


class SessionManager:
    """Manages executive sessions."""
    
    def create(
        self,
        user_id: str,
        workspace_id: str,
    ) -> ExecutiveSession:
        """Create session."""
        session = ExecutiveSession(
            id=str(uuid4()),
            user_id=user_id,
            workspace_id=workspace_id,
            status="active",
            started_at=datetime.now(timezone.utc).isoformat(),
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._sessions[session.id] = session
        return session
    
    def get(self, session_id: str) -> ExecutiveSession | None:
        """Get session."""
        return _storage._sessions.get(session_id)
    
    def add_view_history(
        self,
        session_id: str,
        entity_type: str,
        entity_id: str,
        view_type: str,
    ) -> ExecutiveSession | None:
        """Add view history."""
        session = self.get(session_id)
        if not session:
            return None
        
        entry = ViewHistory(
            entity_type=entity_type,
            entity_id=entity_id,
            view_type=view_type,
        )
        
        updated = ExecutiveSession(
            id=session.id,
            user_id=session.user_id,
            workspace_id=session.workspace_id,
            status=session.status,
            started_at=session.started_at,
            ended_at=session.ended_at,
            view_history=session.view_history + (entry,),
            dashboard_sessions=session.dashboard_sessions,
            created_at=session.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=session.version + 1,
            metadata=session.metadata,
        )
        _storage._sessions[updated.id] = updated
        return updated


class AuditManager:
    """Manages audit records."""
    
    def record(
        self,
        session_id: str,
        user_id: str,
        action: str,
        entity_type: str,
        entity_id: str,
        entity_ref: str = "",
        details: dict[str, Any] = None,
    ) -> AuditEntry:
        """Record audit entry."""
        entry = AuditEntry(
            id=str(uuid4()),
            session_id=session_id,
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_ref=entity_ref,
            details=details or {},
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
        )
        _storage._audit[entry.id] = entry
        return entry
    
    def list_by_session(self, session_id: str) -> list[AuditEntry]:
        """List audit entries by session."""
        return [
            e for e in _storage._audit.values()
            if e.session_id == session_id
        ]


class WidgetRegistry:
    """Registry for widget types."""
    
    def register(self, widget: WidgetMetadata) -> None:
        """Register widget type."""
        _storage._widget_metadata[widget.id] = widget
    
    def get(self, widget_id: str) -> WidgetMetadata | None:
        """Get widget type."""
        return _storage._widget_metadata.get(widget_id)
    
    def list_all(self) -> list[WidgetMetadata]:
        """List all widget types."""
        return list(_storage._widget_metadata.values())
