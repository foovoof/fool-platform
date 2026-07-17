"""
analyst_workspace/models/navigation.py

Navigation Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from analyst_workspace.models.base import (
    WorkspaceBase,
    TimestampMixin,
)


@dataclass(frozen=True)
class NavigationNode(WorkspaceBase):
    """Navigation tree node."""
    workspace_id: str = ""
    parent_id: str = ""
    label: str = ""
    node_type: str = ""
    entity_type: str = ""
    entity_id: str = ""
    icon: str = ""
    children: tuple[str, ...] = field(default_factory=tuple)
    expanded: bool = False
    visible: bool = True
    order: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "parent_id": self.parent_id,
            "label": self.label,
            "node_type": self.node_type,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "icon": self.icon,
            "children": list(self.children),
            "expanded": self.expanded,
            "visible": self.visible,
            "order": self.order,
        })
        return base


@dataclass(frozen=True)
class Breadcrumb(TimestampMixin):
    """Breadcrumb trail entry."""
    workspace_id: str = ""
    label: str = ""
    entity_type: str = ""
    entity_id: str = ""
    url: str = ""
    position: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "label": self.label,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "url": self.url,
            "position": self.position,
        })
        return base


@dataclass(frozen=True)
class NavigationState(WorkspaceBase):
    """Navigation state."""
    workspace_id: str = ""
    current_node_id: str = ""
    breadcrumbs: tuple[Breadcrumb, ...] = field(default_factory=tuple)
    expanded_nodes: tuple[str, ...] = field(default_factory=tuple)
    selected_nodes: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "current_node_id": self.current_node_id,
            "breadcrumbs": [b.to_dict() for b in self.breadcrumbs],
            "expanded_nodes": list(self.expanded_nodes),
            "selected_nodes": list(self.selected_nodes),
        })
        return base


@dataclass(frozen=True)
class RecentlyOpened(TimestampMixin):
    """Recently opened entity."""
    workspace_id: str = ""
    entity_type: str = ""
    entity_id: str = ""
    label: str = ""
    url: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "label": self.label,
            "url": self.url,
        })
        return base
