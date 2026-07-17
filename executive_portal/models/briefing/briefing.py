"""
executive_portal/models/briefing/briefing.py

Strategic Briefing Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from executive_portal.models.base import PortalBase, ReferenceOnly


@dataclass(frozen=True)
class BriefingSection(PortalBase):
    """Briefing section."""
    briefing_id: str = ""
    title: str = ""
    content: str = ""
    order: int = 0
    publication_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "briefing_id": self.briefing_id,
            "title": self.title,
            "content": content,
            "order": self.order,
            "publication_refs": list(self.publication_refs),
            "evidence_refs": list(self.evidence_refs),
        })
        return base


@dataclass(frozen=True)
class BriefingApproval(PortalBase):
    """Briefing approval record."""
    briefing_id: str = ""
    approved_by: str = ""
    approved_at: str = ""
    notes: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "briefing_id": self.briefing_id,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "notes": self.notes,
        })
        return base


@dataclass(frozen=True)
class BriefingHistory(PortalBase):
    """Briefing version history."""
    briefing_id: str = ""
    version_number: int = 1
    changes_summary: str = ""
    changed_by: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "briefing_id": self.briefing_id,
            "version_number": self.version_number,
            "changes_summary": self.changes_summary,
            "changed_by": self.changed_by,
        })
        return base


@dataclass(frozen=True)
class BriefingMetadata(PortalBase):
    """Briefing metadata."""
    briefing_id: str = ""
    classification: str = "unclassified"
    tlp: str = "amber"
    audience: str = ""
    valid_until: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "briefing_id": self.briefing_id,
            "classification": self.classification,
            "tlp": self.tlp,
            "audience": self.audience,
            "valid_until": self.valid_until,
        })
        return base


@dataclass(frozen=True)
class BriefingVersion(PortalBase):
    """Briefing version."""
    briefing_id: str = ""
    version_number: int = 1
    sections: tuple[BriefingSection, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "briefing_id": self.briefing_id,
            "version_number": self.version_number,
            "sections": [s.to_dict() for s in self.sections],
        })
        return base


@dataclass(frozen=True)
class ExecutiveSummary(PortalBase):
    """Executive summary - REFERENCE ONLY."""
    briefing_id: str = ""
    title: str = ""
    summary: str = ""
    key_points: tuple[str, ...] = field(default_factory=tuple)
    publication_refs: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "briefing_id": self.briefing_id,
            "title": self.title,
            "summary": self.summary,
            "key_points": list(self.key_points),
            "publication_refs": list(self.publication_refs),
        })
        return base


@dataclass(frozen=True)
class StrategicBriefing(PortalBase):
    """
    Strategic Briefing - REFERENCE ONLY.
    
    IMPORTANT: This model consumes platform references.
    It NEVER generates or modifies intelligence.
    """
    title: str = ""
    description: str = ""
    owner: str = ""
    status: str = "draft"
    executive_summary: ExecutiveSummary = None
    sections: tuple[BriefingSection, ...] = field(default_factory=tuple)
    publication_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    report_refs: tuple[str, ...] = field(default_factory=tuple)
    metadata: BriefingMetadata = None
    approval: BriefingApproval = None
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "title": self.title,
            "description": self.description,
            "owner": self.owner,
            "status": self.status,
            "executive_summary": self.executive_summary.to_dict() if self.executive_summary else None,
            "sections": [s.to_dict() for s in self.sections],
            "publication_refs": list(self.publication_refs),
            "evidence_refs": list(self.evidence_refs),
            "report_refs": list(self.report_refs),
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "approval": self.approval.to_dict() if self.approval else None,
        })
        return base
