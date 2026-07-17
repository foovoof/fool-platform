"""
analyst_workspace/events.py

Analyst Workspace Events.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class WorkspaceEventType(Enum):
    """Workspace event types."""
    CREATED = "workspace.created"
    LOADED = "workspace.loaded"
    CLOSED = "workspace.closed"
    SAVED = "workspace.saved"
    RESTORED = "workspace.restored"
    SESSION_STARTED = "session.started"
    SESSION_ENDED = "session.ended"
    SESSION_RESTORED = "session.restored"
    VIEW_OPENED = "view.opened"
    VIEW_CLOSED = "view.closed"
    VIEW_CHANGED = "view.changed"
    PANEL_OPENED = "panel.opened"
    PANEL_CLOSED = "panel.closed"
    PANEL_CHANGED = "panel.changed"
    SELECTION_CHANGED = "selection.changed"
    COMMAND_EXECUTED = "command.executed"
    NAVIGATION_CHANGED = "navigation.changed"
    CONTEXT_CHANGED = "context.changed"
    BOOKMARK_ADDED = "bookmark.added"
    BOOKMARK_REMOVED = "bookmark.removed"
    FAVORITE_ADDED = "favorite.added"
    FAVORITE_REMOVED = "favorite.removed"
    NOTIFICATION_CREATED = "notification.created"
    NOTIFICATION_DISMISSED = "notification.dismissed"
    PREFERENCE_CHANGED = "preference.changed"


@dataclass
class WorkspaceEvent:
    """Workspace event."""
    event_type: str
    workspace_id: str
    timestamp: str
    data: dict[str, Any]
    actor: str = ""
    session_id: str = ""
    version: str = "1.0"
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "workspace_id": self.workspace_id,
            "timestamp": self.timestamp,
            "data": self.data,
            "actor": self.actor,
            "session_id": self.session_id,
            "version": self.version,
        }


class WorkspaceEventEmitter:
    """Emitter for workspace events."""
    
    def __init__(self) -> None:
        self._events: list[WorkspaceEvent] = []
        self._enabled = True
    
    def enable(self) -> None:
        """Enable event emission."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable event emission."""
        self._enabled = False
    
    def emit(self, event: WorkspaceEvent) -> None:
        """Emit an event."""
        if self._enabled:
            self._events.append(event)
    
    def emit_workspace_created(
        self,
        workspace_id: str,
        actor: str = "",
    ) -> None:
        """Emit workspace created event."""
        self.emit(WorkspaceEvent(
            event_type=WorkspaceEventType.CREATED.value,
            workspace_id=workspace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_workspace_loaded(
        self,
        workspace_id: str,
        actor: str = "",
    ) -> None:
        """Emit workspace loaded event."""
        self.emit(WorkspaceEvent(
            event_type=WorkspaceEventType.LOADED.value,
            workspace_id=workspace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_workspace_closed(
        self,
        workspace_id: str,
        actor: str = "",
    ) -> None:
        """Emit workspace closed event."""
        self.emit(WorkspaceEvent(
            event_type=WorkspaceEventType.CLOSED.value,
            workspace_id=workspace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_workspace_saved(
        self,
        workspace_id: str,
        actor: str = "",
    ) -> None:
        """Emit workspace saved event."""
        self.emit(WorkspaceEvent(
            event_type=WorkspaceEventType.SAVED.value,
            workspace_id=workspace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_workspace_restored(
        self,
        workspace_id: str,
        session_id: str,
        actor: str = "",
    ) -> None:
        """Emit workspace restored event."""
        self.emit(WorkspaceEvent(
            event_type=WorkspaceEventType.RESTORED.value,
            workspace_id=workspace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"session_id": session_id},
            actor=actor,
        ))
    
    def emit_view_opened(
        self,
        workspace_id: str,
        view_id: str,
        view_type: str,
    ) -> None:
        """Emit view opened event."""
        self.emit(WorkspaceEvent(
            event_type=WorkspaceEventType.VIEW_OPENED.value,
            workspace_id=workspace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"view_id": view_id, "view_type": view_type},
        ))
    
    def emit_view_closed(
        self,
        workspace_id: str,
        view_id: str,
    ) -> None:
        """Emit view closed event."""
        self.emit(WorkspaceEvent(
            event_type=WorkspaceEventType.VIEW_CLOSED.value,
            workspace_id=workspace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"view_id": view_id},
        ))
    
    def emit_panel_opened(
        self,
        workspace_id: str,
        panel_id: str,
        panel_type: str,
    ) -> None:
        """Emit panel opened event."""
        self.emit(WorkspaceEvent(
            event_type=WorkspaceEventType.PANEL_OPENED.value,
            workspace_id=workspace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"panel_id": panel_id, "panel_type": panel_type},
        ))
    
    def emit_selection_changed(
        self,
        workspace_id: str,
        selected_ids: list[str],
    ) -> None:
        """Emit selection changed event."""
        self.emit(WorkspaceEvent(
            event_type=WorkspaceEventType.SELECTION_CHANGED.value,
            workspace_id=workspace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"selected_ids": selected_ids},
        ))
    
    def emit_command_executed(
        self,
        workspace_id: str,
        session_id: str,
        command_name: str,
        success: bool,
    ) -> None:
        """Emit command executed event."""
        self.emit(WorkspaceEvent(
            event_type=WorkspaceEventType.COMMAND_EXECUTED.value,
            workspace_id=workspace_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"command_name": command_name, "success": success},
            session_id=session_id,
        ))
    
    def get_events(self) -> list[WorkspaceEvent]:
        """Get all events."""
        return list(self._events)
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
