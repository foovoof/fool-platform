"""
executive_portal/models/widget/widget.py

Widget Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from executive_portal.models.base import PortalBase, ReferenceOnly


@dataclass(frozen=True)
class WidgetContext(PortalBase):
    """Widget context."""
    dashboard_id: str = ""
    workspace_id: str = ""
    filters: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "dashboard_id": self.dashboard_id,
            "workspace_id": self.workspace_id,
            "filters": self.filters,
            "parameters": self.parameters,
        })
        return base


@dataclass(frozen=True)
class WidgetProvider:
    """Widget data provider contract."""
    provider_id: str = ""
    provider_type: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "provider_type": self.provider_type,
        }


@dataclass(frozen=True)
class PublicationReference(PortalBase, ReferenceOnly):
    """Reference to a publication - NEVER duplicated."""
    widget_id: str = ""
    title: str = ""
    publication_date: str = ""
    source: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "widget_id": self.widget_id,
            "title": self.title,
            "publication_date": self.publication_date,
            "source": self.source,
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "ref_source": self.ref_source,
        })
        return base


@dataclass(frozen=True)
class ReportReference(PortalBase, ReferenceOnly):
    """Reference to a report - NEVER duplicated."""
    widget_id: str = ""
    title: str = ""
    report_date: str = ""
    author: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "widget_id": self.widget_id,
            "title": self.title,
            "report_date": self.report_date,
            "author": self.author,
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "ref_source": self.ref_source,
        })
        return base


@dataclass(frozen=True)
class EvidenceReference(PortalBase, ReferenceOnly):
    """Reference to evidence - NEVER duplicated."""
    widget_id: str = ""
    evidence_type: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "widget_id": self.widget_id,
            "evidence_type": self.evidence_type,
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "ref_source": self.ref_source,
        })
        return base


@dataclass(frozen=True)
class MetricReference(PortalBase, ReferenceOnly):
    """Reference to a metric - NEVER duplicated."""
    widget_id: str = ""
    metric_name: str = ""
    metric_source: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "widget_id": self.widget_id,
            "metric_name": self.metric_name,
            "metric_source": self.metric_source,
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "ref_source": self.ref_source,
        })
        return base


@dataclass(frozen=True)
class ExecutiveWidget(PortalBase):
    """
    Executive Widget - REFERENCE ONLY.
    
    IMPORTANT: Widgets consume platform references.
    They NEVER own or duplicate data.
    """
    widget_type: str = ""
    name: str = ""
    description: str = ""
    title: str = ""
    position: dict[str, int] = field(default_factory=dict)
    size: dict[str, int] = field(default_factory=dict)
    configuration: dict[str, Any] = field(default_factory=dict)
    publication_refs: tuple[PublicationReference, ...] = field(default_factory=tuple)
    report_refs: tuple[ReportReference, ...] = field(default_factory=tuple)
    evidence_refs: tuple[EvidenceReference, ...] = field(default_factory=tuple)
    metric_refs: tuple[MetricReference, ...] = field(default_factory=tuple)
    plugin_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "widget_type": self.widget_type,
            "name": self.name,
            "description": self.description,
            "title": self.title,
            "position": self.position,
            "size": self.size,
            "configuration": self.configuration,
            "publication_refs": [r.to_dict() for r in self.publication_refs],
            "report_refs": [r.to_dict() for r in self.report_refs],
            "evidence_refs": [r.to_dict() for r in self.evidence_refs],
            "metric_refs": [r.to_dict() for r in self.metric_refs],
            "plugin_id": self.plugin_id,
        })
        return base
