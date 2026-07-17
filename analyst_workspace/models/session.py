"""
analyst_workspace/models/session.py

Session Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from analyst_workspace.models.base import (
    WorkspaceBase,
    Auditable,
    TimestampMixin,
)


@dataclass(frozen=True)
class SessionSnapshot(WorkspaceBase):
    """Session snapshot for save/restore."""
    session_id: str = ""
    state: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    open_views: tuple[str, ...] = field(default_factory=tuple)
    open_panels: tuple[str, ...] = field(default_factory=tuple)
    selections: tuple[str, ...] = field(default_factory=tuple)
    navigation_history: tuple[str, ...] = field(default_factory=tuple)
    scroll_positions: dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "session_id": self.session_id,
            "state": self.state,
            "context": self.context,
            "open_views": list(self.open_views),
            "open_panels": list(self.open_panels),
            "selections": list(self.selections),
            "navigation_history": list(self.navigation_history),
            "scroll_positions": self.scroll_positions,
        })
        return base


@dataclass(frozen=True)
class WorkspaceSession(WorkspaceBase, Auditable):
    """Workspace session."""
    workspace_id: str = ""
    user_id: str = ""
    status: str = "active"
    started_at: str = ""
    ended_at: str = ""
    last_activity: str = ""
    idle_time: int = 0
    snapshots: tuple[SessionSnapshot, ...] = field(default_factory=tuple)
    current_snapshot_id: str = ""
    is_recovery: bool = False
    parent_session_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "user_id": self.user_id,
            "status": self.status,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "last_activity": self.last_activity,
            "idle_time": self.idle_time,
            "snapshots": [s.to_dict() for s in self.snapshots],
            "current_snapshot_id": self.current_snapshot_id,
            "is_recovery": self.is_recovery,
            "parent_session_id": self.parent_session_id,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class SessionHistory(TimestampMixin, Auditable):
    """Session history entry."""
    session_id: str = ""
    action: str = ""
    entity_type: str = ""
    entity_id: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "session_id": self.session_id,
            "action": action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "details": self.details,
            "author": self.author,
            "reason": self.reason,
        })
        return base
