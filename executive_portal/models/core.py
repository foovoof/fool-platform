"""
executive_portal/models/core.py

Executive Portal Core Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from executive_portal.models.base import PortalBase, ReferenceOnly


@dataclass(frozen=True)
class ExecutiveBookmark(PortalBase):
    """Executive bookmark - REFERENCE ONLY."""
    user_id: str = ""
    name: str = ""
    ref_id: str = ""
    ref_type: str = ""
    ref_source: str = ""
    url: str = ""
    category: str = ""
    pinned: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "user_id": self.user_id,
            "name": self.name,
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "ref_source": self.ref_source,
            "url": self.url,
            "category": self.category,
            "pinned": self.pinned,
        })
        return base


@dataclass(frozen=True)
class SavedSearch(PortalBase):
    """Saved search."""
    user_id: str = ""
    name: str = ""
    query: str = ""
    filters: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "user_id": self.user_id,
            "name": self.name,
            "query": self.query,
            "filters": self.filters,
        })
        return base


@dataclass(frozen=True)
class Filter(PortalBase):
    """Filter definition."""
    name: str = ""
    field: str = ""
    operator: str = ""
    value: Any = None
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "field": self.field,
            "operator": self.operator,
            "value": self.value,
        })
        return base


@dataclass(frozen=True)
class NavigationItem(PortalBase):
    """Navigation item."""
    label: str = ""
    url: str = ""
    icon: str = ""
    order: int = 0
    parent_id: str = ""
    children: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "label": self.label,
            "url": self.url,
            "icon": self.icon,
            "order": self.order,
            "parent_id": self.parent_id,
            "children": list(self.children),
        })
        return base


@dataclass(frozen=True)
class NavigationTree(PortalBase):
    """Navigation tree."""
    name: str = ""
    items: tuple[NavigationItem, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "items": [i.to_dict() for i in self.items],
        })
        return base


@dataclass(frozen=True)
class PublicationFeed(PortalBase):
    """Publication feed - REFERENCE ONLY."""
    name: str = ""
    description: str = ""
    feed_type: str = "standard"
    publication_refs: tuple[str, ...] = field(default_factory=tuple)
    filters: tuple[Filter, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "feed_type": self.feed_type,
            "publication_refs": list(self.publication_refs),
            "filters": [f.to_dict() for f in self.filters],
        })
        return base


@dataclass(frozen=True)
class ExecutivePreference(PortalBase):
    """Executive preference."""
    user_id: str = ""
    category: str = ""
    key: str = ""
    value: Any = None
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "user_id": self.user_id,
            "category": self.category,
            "key": self.key,
            "value": self.value,
        })
        return base


@dataclass(frozen=True)
class ExecutiveWorkspace(PortalBase):
    """
    Executive Workspace - REFERENCE ONLY.
    
    IMPORTANT: This model consumes platform references.
    It NEVER owns or duplicates them.
    """
    name: str = ""
    description: str = ""
    owner: str = ""
    dashboard_ids: tuple[str, ...] = field(default_factory=tuple)
    feed_ids: tuple[str, ...] = field(default_factory=tuple)
    collection_ids: tuple[str, ...] = field(default_factory=tuple)
    briefing_ids: tuple[str, ...] = field(default_factory=tuple)
    layout: dict[str, Any] = field(default_factory=dict)
    preferences: tuple[ExecutivePreference, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "owner": self.owner,
            "dashboard_ids": list(self.dashboard_ids),
            "feed_ids": list(self.feed_ids),
            "collection_ids": list(self.collection_ids),
            "briefing_ids": list(self.briefing_ids),
            "layout": self.layout,
            "preferences": [p.to_dict() for p in self.preferences],
        })
        return base


@dataclass(frozen=True)
class ExecutiveSnapshot(PortalBase):
    """Executive snapshot export - REFERENCE ONLY."""
    workspace_id: str = ""
    snapshot_type: str = "workspace"
    ref_ids: tuple[str, ...] = field(default_factory=tuple)
    format: str = "json"
    exported_by: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "workspace_id": self.workspace_id,
            "snapshot_type": self.snapshot_type,
            "ref_ids": list(self.ref_ids),
            "format": self.format,
            "exported_by": self.exported_by,
        })
        return base
