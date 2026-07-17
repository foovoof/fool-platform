"""
analyst_workspace/models/commands.py

Commands and Notifications Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from analyst_workspace.models.base import (
    WorkspaceBase,
    TimestampMixin,
)


@dataclass(frozen=True)
class CommandDefinition(WorkspaceBase):
    """Command definition."""
    name: str = ""
    description: str = ""
    scope: str = "global"
    shortcut: str = ""
    icon: str = ""
    category: str = ""
    parameters: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    enabled: bool = True
    visible: bool = True
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "scope": self.scope,
            "shortcut": self.shortcut,
            "icon": self.icon,
            "category": self.category,
            "parameters": list(self.parameters),
            "enabled": self.enabled,
            "visible": self.visible,
        })
        return base


@dataclass(frozen=True)
class CommandExecution(TimestampMixin):
    """Command execution record."""
    workspace_id: str = ""
    session_id: str = ""
    command_name: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    result: dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error: str = ""
    duration_ms: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "session_id": self.session_id,
            "command_name": self.command_name,
            "parameters": self.parameters,
            "result": self.result,
            "success": self.success,
            "error": self.error,
            "duration_ms": self.duration_ms,
        })
        return base


@dataclass(frozen=True)
class WorkspaceCommand(WorkspaceBase):
    """Workspace command."""
    workspace_id: str = ""
    name: str = ""
    command_type: str = ""
    scope: str = "global"
    parameters: dict[str, Any] = field(default_factory=dict)
    target_ids: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "name": self.name,
            "command_type": self.command_type,
            "scope": self.scope,
            "parameters": self.parameters,
            "target_ids": list(self.target_ids),
        })
        return base
