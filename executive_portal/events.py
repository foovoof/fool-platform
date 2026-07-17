"""
executive_portal/events.py

Executive Portal Events.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class PortalEventType(Enum):
    """Portal event types."""
    WORKSPACE_CREATED = "workspace.created"
    WORKSPACE_OPENED = "workspace.opened"
    WORKSPACE_UPDATED = "workspace.updated"
    DASHBOARD_CREATED = "dashboard.created"
    DASHBOARD_OPENED = "dashboard.opened"
    DASHBOARD_UPDATED = "dashboard.updated"
    WIDGET_ADDED = "widget.added"
    WIDGET_REMOVED = "widget.removed"
    BRIEFING_CREATED = "briefing.created"
    BRIEFING_PUBLISHED = "briefing.published"
    COLLECTION_CREATED = "collection.created"
    COLLECTION_UPDATED = "collection.updated"
    BOOKMARK_ADDED = "bookmark.added"
    BOOKMARK_REMOVED = "bookmark.removed"
    SEARCH_EXECUTED = "search.executed"
    FILTER_APPLIED = "filter.applied"
    LAYOUT_CHANGED = "layout.changed"
    EXPORT_REQUESTED = "export.requested"
    SESSION_STARTED = "session.started"
    SESSION_ENDED = "session.ended"
    VIEW_OPENED = "view.opened"
    PINNED = "pinned"
    SHARED = "shared"


@dataclass
class PortalEvent:
    """Portal event."""
    event_type: str
    entity_id: str
    entity_type: str
    timestamp: str
    data: dict[str, Any]
    actor: str = ""
    version: str = "1.0"
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "timestamp": self.timestamp,
            "data": self.data,
            "actor": self.actor,
            "version": self.version,
        }


class PortalEventEmitter:
    """Emitter for portal events."""
    
    def __init__(self) -> None:
        self._events: list[PortalEvent] = []
        self._enabled = True
    
    def enable(self) -> None:
        """Enable event emission."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable event emission."""
        self._enabled = False
    
    def emit(self, event: PortalEvent) -> None:
        """Emit an event."""
        if self._enabled:
            self._events.append(event)
    
    def emit_workspace_created(
        self,
        workspace_id: str,
        actor: str = "",
    ) -> None:
        """Emit workspace created event."""
        self.emit(PortalEvent(
            event_type=PortalEventType.WORKSPACE_CREATED.value,
            entity_id=workspace_id,
            entity_type="workspace",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_workspace_opened(
        self,
        workspace_id: str,
        actor: str = "",
    ) -> None:
        """Emit workspace opened event."""
        self.emit(PortalEvent(
            event_type=PortalEventType.WORKSPACE_OPENED.value,
            entity_id=workspace_id,
            entity_type="workspace",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_dashboard_created(
        self,
        dashboard_id: str,
        actor: str = "",
    ) -> None:
        """Emit dashboard created event."""
        self.emit(PortalEvent(
            event_type=PortalEventType.DASHBOARD_CREATED.value,
            entity_id=dashboard_id,
            entity_type="dashboard",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_dashboard_opened(
        self,
        dashboard_id: str,
        actor: str = "",
    ) -> None:
        """Emit dashboard opened event."""
        self.emit(PortalEvent(
            event_type=PortalEventType.DASHBOARD_OPENED.value,
            entity_id=dashboard_id,
            entity_type="dashboard",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_briefing_created(
        self,
        briefing_id: str,
        actor: str = "",
    ) -> None:
        """Emit briefing created event."""
        self.emit(PortalEvent(
            event_type=PortalEventType.BRIEFING_CREATED.value,
            entity_id=briefing_id,
            entity_type="briefing",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_collection_created(
        self,
        collection_id: str,
        actor: str = "",
    ) -> None:
        """Emit collection created event."""
        self.emit(PortalEvent(
            event_type=PortalEventType.COLLECTION_CREATED.value,
            entity_id=collection_id,
            entity_type="collection",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_bookmark_added(
        self,
        bookmark_id: str,
        actor: str = "",
    ) -> None:
        """Emit bookmark added event."""
        self.emit(PortalEvent(
            event_type=PortalEventType.BOOKMARK_ADDED.value,
            entity_id=bookmark_id,
            entity_type="bookmark",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_session_started(
        self,
        session_id: str,
        actor: str = "",
    ) -> None:
        """Emit session started event."""
        self.emit(PortalEvent(
            event_type=PortalEventType.SESSION_STARTED.value,
            entity_id=session_id,
            entity_type="session",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_view_opened(
        self,
        entity_id: str,
        entity_type: str,
        actor: str = "",
    ) -> None:
        """Emit view opened event."""
        self.emit(PortalEvent(
            event_type=PortalEventType.VIEW_OPENED.value,
            entity_id=entity_id,
            entity_type=entity_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def get_events(self) -> list[PortalEvent]:
        """Get all events."""
        return list(self._events)
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
