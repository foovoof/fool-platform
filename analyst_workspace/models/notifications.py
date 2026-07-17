"""
analyst_workspace/models/notifications.py

Notifications and Views/Panels Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from analyst_workspace.models.base import (
    WorkspaceBase,
    TimestampMixin,
)


@dataclass(frozen=True)
class WorkspaceNotification(TimestampMixin):
    """Workspace notification."""
    workspace_id: str = ""
    title: str = ""
    message: str = ""
    level: str = "info"
    source: str = ""
    entity_type: str = ""
    entity_id: str = ""
    action_url: str = ""
    dismissed: bool = False
    read: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "title": self.title,
            "message": self.message,
            "level": self.level,
            "source": self.source,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "action_url": self.action_url,
            "dismissed": self.dismissed,
            "read": self.read,
        })
        return base


@dataclass(frozen=True)
class ViewDefinition(WorkspaceBase):
    """View definition."""
    name: str = ""
    view_type: str = ""
    description: str = ""
    icon: str = ""
    category: str = ""
    supported_entity_types: tuple[str, ...] = field(default_factory=tuple)
    panels: tuple[str, ...] = field(default_factory=tuple)
    configuration: dict[str, Any] = field(default_factory=dict)
    plugin_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "view_type": self.view_type,
            "description": self.description,
            "icon": self.icon,
            "category": self.category,
            "supported_entity_types": list(self.supported_entity_types),
            "panels": list(self.panels),
            "configuration": self.configuration,
            "plugin_id": self.plugin_id,
        })
        return base


@dataclass(frozen=True)
class PanelDefinition(WorkspaceBase):
    """Panel definition."""
    name: str = ""
    panel_type: str = ""
    description: str = ""
    icon: str = ""
    default_width: int = 300
    default_height: int = 200
    min_width: int = 100
    min_height: int = 100
    resizable: bool = True
    collapsible: bool = True
    plugin_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "panel_type": self.panel_type,
            "description": self.description,
            "icon": self.icon,
            "default_width": self.default_width,
            "default_height": self.default_height,
            "min_width": self.min_width,
            "min_height": self.min_height,
            "resizable": self.resizable,
            "collapsible": self.collapsible,
            "plugin_id": self.plugin_id,
        })
        return base


@dataclass(frozen=True)
class OpenView(WorkspaceBase):
    """Open view instance."""
    workspace_id: str = ""
    view_id: str = ""
    view_type: str = ""
    title: str = ""
    entity_id: str = ""
    entity_type: str = ""
    configuration: dict[str, Any] = field(default_factory=dict)
    position: dict[str, int] = field(default_factory=dict)
    panel_id: str = ""
    is_active: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "view_id": self.view_id,
            "view_type": self.view_type,
            "title": self.title,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "configuration": self.configuration,
            "position": self.position,
            "panel_id": self.panel_id,
            "is_active": self.is_active,
        })
        return base


@dataclass(frozen=True)
class OpenPanel(WorkspaceBase):
    """Open panel instance."""
    workspace_id: str = ""
    panel_id: str = ""
    panel_type: str = ""
    title: str = ""
    configuration: dict[str, Any] = field(default_factory=dict)
    position: dict[str, int] = field(default_factory=dict)
    size: dict[str, int] = field(default_factory=dict)
    collapsed: bool = False
    visible: bool = True
    order: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "panel_id": self.panel_id,
            "panel_type": self.panel_type,
            "title": self.title,
            "configuration": self.configuration,
            "position": self.position,
            "size": self.size,
            "collapsed": self.collapsed,
            "visible": self.visible,
            "order": self.order,
        })
        return base
