"""
analyst_workspace/models/workspace.py

Workspace Core Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from analyst_workspace.models.base import (
    WorkspaceBase,
    Auditable,
    Versionable,
)


@dataclass(frozen=True)
class WorkspaceLayout:
    """Workspace layout configuration."""
    layout_id: str = ""
    name: str = ""
    description: str = ""
    panels: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    views: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    arrangement: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "layout_id": self.layout_id,
            "name": self.name,
            "description": self.description,
            "panels": list(self.panels),
            "views": list(self.views),
            "arrangement": self.arrangement,
        }


@dataclass(frozen=True)
class WorkspaceState:
    """Workspace state snapshot."""
    state_id: str = ""
    workspace_id: str = ""
    active_view: str = ""
    active_panel: str = ""
    selections: tuple[str, ...] = field(default_factory=tuple)
    context: dict[str, Any] = field(default_factory=dict)
    scroll_positions: dict[str, int] = field(default_factory=dict)
    expanded_nodes: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "state_id": self.state_id,
            "workspace_id": self.workspace_id,
            "active_view": self.active_view,
            "active_panel": self.active_panel,
            "selections": list(self.selections),
            "context": self.context,
            "scroll_positions": self.scroll_positions,
            "expanded_nodes": list(self.expanded_nodes),
        }


@dataclass(frozen=True)
class WorkspacePreference(WorkspaceBase, Auditable):
    """Workspace preference."""
    workspace_id: str = ""
    category: str = ""
    key: str = ""
    value: Any = None
    default_value: Any = None
    description: str = ""
    editable: bool = True
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "category": self.category,
            "key": self.key,
            "value": self.value,
            "default_value": self.default_value,
            "description": self.description,
            "editable": self.editable,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class WorkspaceProfile(WorkspaceBase, Auditable):
    """Workspace user profile."""
    user_id: str = ""
    name: str = ""
    email: str = ""
    role: str = ""
    default_workspace_id: str = ""
    preferences: dict[str, Any] = field(default_factory=dict)
    layouts: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "default_workspace_id": self.default_workspace_id,
            "preferences": self.preferences,
            "layouts": list(self.layouts),
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class WorkspaceContext(WorkspaceBase):
    """Workspace context information."""
    workspace_id: str = ""
    entity_id: str = ""
    entity_type: str = ""
    view_type: str = ""
    panel_ids: tuple[str, ...] = field(default_factory=tuple)
    parameters: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "view_type": self.view_type,
            "panel_ids": list(self.panel_ids),
            "parameters": self.parameters,
        })
        return base


@dataclass(frozen=True)
class WorkspaceSelection(WorkspaceBase):
    """Workspace selection state."""
    workspace_id: str = ""
    selection_type: str = ""
    selected_ids: tuple[str, ...] = field(default_factory=tuple)
    selection_mode: str = "single"
    selection_timestamp: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "selection_type": self.selection_type,
            "selected_ids": list(self.selected_ids),
            "selection_mode": self.selection_mode,
            "selection_timestamp": self.selection_timestamp,
        })
        return base


@dataclass(frozen=True)
class Workspace(WorkspaceBase, Auditable, Versionable):
    """Main workspace entity."""
    name: str = ""
    description: str = ""
    owner_id: str = ""
    status: str = "active"
    layouts: tuple[WorkspaceLayout, ...] = field(default_factory=tuple)
    current_layout_id: str = ""
    preferences: tuple[WorkspacePreference, ...] = field(default_factory=tuple)
    context: dict[str, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "status": self.status,
            "layouts": [l.to_dict() for l in self.layouts],
            "current_layout_id": self.current_layout_id,
            "preferences": [p.to_dict() for p in self.preferences],
            "context": self.context,
            "tags": list(self.tags),
            "author": self.author,
            "reason": self.reason,
        })
        return base
