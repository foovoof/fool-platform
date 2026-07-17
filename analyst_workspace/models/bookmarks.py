"""
analyst_workspace/models/bookmarks.py

Bookmarks and Favorites Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from analyst_workspace.models.base import (
    WorkspaceBase,
    TimestampMixin,
)


@dataclass(frozen=True)
class WorkspaceBookmark(WorkspaceBase):
    """Workspace bookmark."""
    workspace_id: str = ""
    user_id: str = ""
    name: str = ""
    description: str = ""
    entity_type: str = ""
    entity_id: str = ""
    url: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    category: str = ""
    pinned: bool = False
    access_count: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "url": self.url,
            "tags": list(self.tags),
            "category": self.category,
            "pinned": self.pinned,
            "access_count": self.access_count,
        })
        return base


@dataclass(frozen=True)
class WorkspaceFavorite(TimestampMixin):
    """Workspace favorite."""
    workspace_id: str = ""
    user_id: str = ""
    entity_type: str = ""
    entity_id: str = ""
    label: str = ""
    url: str = ""
    position: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "user_id": self.user_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "label": self.label,
            "url": self.url,
            "position": self.position,
        })
        return base


@dataclass(frozen=True)
class CrossReference:
    """Cross reference entry."""
    source_entity_type: str = ""
    source_entity_id: str = ""
    target_entity_type: str = ""
    target_entity_id: str = ""
    relationship_type: str = ""
    label: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "source_entity_type": self.source_entity_type,
            "source_entity_id": self.source_entity_id,
            "target_entity_type": self.target_entity_type,
            "target_entity_id": self.target_entity_id,
            "relationship_type": self.relationship_type,
            "label": self.label,
        }
