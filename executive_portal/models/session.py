"""
executive_portal/models/session.py

Session and Audit Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from executive_portal.models.base import PortalBase


@dataclass(frozen=True)
class ViewHistory(PortalBase):
    """View history entry."""
    session_id: str = ""
    entity_type: str = ""
    entity_id: str = ""
    view_type: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "session_id": self.session_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "view_type": self.view_type,
        })
        return base


@dataclass(frozen=True)
class SessionState(PortalBase):
    """Session state snapshot."""
    session_id: str = ""
    dashboard_id: str = ""
    layout: dict[str, Any] = field(default_factory=dict)
    filters: dict[str, Any] = field(default_factory=dict)
    active_view: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "session_id": self.session_id,
            "dashboard_id": self.dashboard_id,
            "layout": self.layout,
            "filters": self.filters,
            "active_view": self.active_view,
        })
        return base


@dataclass(frozen=True)
class DashboardSession(PortalBase):
    """Dashboard session."""
    dashboard_id: str = ""
    user_id: str = ""
    status: str = "active"
    started_at: str = ""
    ended_at: str = ""
    state: SessionState = None
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "dashboard_id": self.dashboard_id,
            "user_id": self.user_id,
            "status": self.status,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "state": self.state.to_dict() if self.state else None,
        })
        return base


@dataclass(frozen=True)
class ExecutiveSession(PortalBase):
    """
    Executive session.
    
    IMPORTANT: Sessions track user activity only.
    They NEVER modify platform data.
    """
    user_id: str = ""
    workspace_id: str = ""
    status: str = "active"
    started_at: str = ""
    ended_at: str = ""
    view_history: tuple[ViewHistory, ...] = field(default_factory=tuple)
    dashboard_sessions: tuple[DashboardSession, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "user_id": self.user_id,
            "workspace_id": self.workspace_id,
            "status": self.status,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "view_history": [v.to_dict() for v in self.view_history],
            "dashboard_sessions": [d.to_dict() for d in self.dashboard_sessions],
        })
        return base


@dataclass(frozen=True)
class AuditEntry(PortalBase):
    """
    Audit entry.
    
    IMPORTANT: Audit records user actions only.
    They NEVER modify platform data.
    """
    session_id: str = ""
    user_id: str = ""
    action: str = ""
    entity_type: str = ""
    entity_id: str = ""
    entity_ref: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "session_id": self.session_id,
            "user_id": self.user_id,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "entity_ref": self.entity_ref,
            "details": self.details,
        })
        return base


@dataclass(frozen=True)
class HistoryEntry(PortalBase):
    """History entry."""
    user_id: str = ""
    action: str = ""
    entity_type: str = ""
    entity_id: str = ""
    url: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "user_id": self.user_id,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "url": self.url,
        })
        return base
