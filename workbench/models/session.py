"""
workbench/models/session.py

Session Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from workbench.models.base import WorkbenchBase


@dataclass(frozen=True)
class WorkbenchSession(WorkbenchBase):
    """Workbench session."""
    user_id: str = ""
    session_type: str = ""
    started_at: str = ""
    ended_at: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "user_id": self.user_id,
            "session_type": self.session_type,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "context": self.context,
        })
        return base


@dataclass(frozen=True)
class WorkbenchContext(WorkbenchBase):
    """Workbench context."""
    session_id: str = ""
    entity_type: str = ""
    entity_id: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "session_id": self.session_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "parameters": self.parameters,
        })
        return base


@dataclass(frozen=True)
class WorkbenchHistory(WorkbenchBase):
    """Workbench action history."""
    session_id: str = ""
    action: str = ""
    entity_type: str = ""
    entity_id: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    actor: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "session_id": self.session_id,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "details": self.details,
            "actor": self.actor,
        })
        return base
