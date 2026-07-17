"""
executive_portal/models/dashboard/dashboard.py

Dashboard Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from executive_portal.models.base import PortalBase, ReferenceOnly


@dataclass(frozen=True)
class WidgetConfiguration(PortalBase):
    """Widget configuration."""
    widget_id: str = ""
    config: dict[str, Any] = field(default_factory=dict)
    refresh_interval: int = 300
    visibility: str = "visible"
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "widget_id": self.widget_id,
            "config": self.config,
            "refresh_interval": self.refresh_interval,
            "visibility": self.visibility,
        })
        return base


@dataclass(frozen=True)
class WidgetMetadata(PortalBase):
    """Widget metadata."""
    widget_type: str = ""
    name: str = ""
    description: str = ""
    icon: str = ""
    category: str = ""
    supported_ref_types: tuple[str, ...] = field(default_factory=tuple)
    plugin_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "widget_type": self.widget_type,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "category": self.category,
            "supported_ref_types": list(self.supported_ref_types),
            "plugin_id": self.plugin_id,
        })
        return base


@dataclass(frozen=True)
class WidgetReference(PortalBase, ReferenceOnly):
    """Reference to a widget - NEVER duplicated."""
    dashboard_id: str = ""
    widget_type: str = ""
    title: str = ""
    position: dict[str, int] = field(default_factory=dict)
    size: dict[str, int] = field(default_factory=dict)
    configuration: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "dashboard_id": self.dashboard_id,
            "widget_type": self.widget_type,
            "title": self.title,
            "position": self.position,
            "size": self.size,
            "configuration": self.configuration,
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "ref_source": self.ref_source,
        })
        return base


@dataclass(frozen=True)
class DashboardSection(PortalBase):
    """Dashboard section."""
    dashboard_id: str = ""
    name: str = ""
    order: int = 0
    collapsed: bool = False
    widgets: tuple[WidgetReference, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "dashboard_id": self.dashboard_id,
            "name": self.name,
            "order": self.order,
            "collapsed": self.collapsed,
            "widgets": [w.to_dict() for w in self.widgets],
        })
        return base


@dataclass(frozen=True)
class DashboardLayout(PortalBase):
    """Dashboard layout."""
    dashboard_id: str = ""
    layout_type: str = "grid"
    columns: int = 3
    rows: int = 2
    sections: tuple[DashboardSection, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "dashboard_id": self.dashboard_id,
            "layout_type": self.layout_type,
            "columns": self.columns,
            "rows": self.rows,
            "sections": [s.to_dict() for s in self.sections],
        })
        return base


@dataclass(frozen=True)
class DashboardState(PortalBase):
    """Dashboard state snapshot."""
    dashboard_id: str = ""
    active_view: str = ""
    filters: dict[str, Any] = field(default_factory=dict)
    scroll_position: int = 0
    expanded_sections: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "dashboard_id": self.dashboard_id,
            "active_view": self.active_view,
            "filters": self.filters,
            "scroll_position": self.scroll_position,
            "expanded_sections": list(self.expanded_sections),
        })
        return base


@dataclass(frozen=True)
class DashboardView(PortalBase):
    """Dashboard view configuration."""
    dashboard_id: str = ""
    name: str = ""
    description: str = ""
    layout_id: str = ""
    default: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "dashboard_id": self.dashboard_id,
            "name": self.name,
            "description": self.description,
            "layout_id": self.layout_id,
            "default": self.default,
        })
        return base


@dataclass(frozen=True)
class ExecutiveDashboard(PortalBase):
    """
    Executive Dashboard - REFERENCE ONLY.
    
    IMPORTANT: This model consumes platform references.
    It NEVER owns or duplicates them.
    """
    name: str = ""
    description: str = ""
    owner: str = ""
    status: str = "active"
    widgets: tuple[WidgetReference, ...] = field(default_factory=tuple)
    layouts: tuple[DashboardLayout, ...] = field(default_factory=tuple)
    views: tuple[DashboardView, ...] = field(default_factory=tuple)
    publication_refs: tuple[str, ...] = field(default_factory=tuple)
    report_refs: tuple[str, ...] = field(default_factory=tuple)
    collection_refs: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "owner": self.owner,
            "status": self.status,
            "widgets": [w.to_dict() for w in self.widgets],
            "layouts": [l.to_dict() for l in self.layouts],
            "views": [v.to_dict() for v in self.views],
            "publication_refs": list(self.publication_refs),
            "report_refs": list(self.report_refs),
            "collection_refs": list(self.collection_refs),
            "tags": list(self.tags),
        })
        return base
