"""
threat_hunting/models/hypothesis.py

Hypothesis Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_hunting.models.base import (
    HuntBase,
    Auditable,
    Versionable,
    ConfidenceMixin,
)


@dataclass(frozen=True)
class HuntHypothesis(HuntBase, Auditable, ConfidenceMixin, Versionable):
    """Hunt hypothesis."""
    hunt_id: str = ""
    title: str = ""
    description: str = ""
    hypothesis_text: str = ""
    assumptions: tuple[str, ...] = field(default_factory=tuple)
    supporting_evidence: tuple[str, ...] = field(default_factory=tuple)
    contradicting_evidence: tuple[str, ...] = field(default_factory=tuple)
    status: str = "draft"
    validated: bool = False
    validated_by: str = ""
    validated_at: str = ""
    validation_notes: str = ""
    related_indicators: tuple[str, ...] = field(default_factory=tuple)
    related_actors: tuple[str, ...] = field(default_factory=tuple)
    related_malware: tuple[str, ...] = field(default_factory=tuple)
    related_campaigns: tuple[str, ...] = field(default_factory=tuple)
    related_infrastructure: tuple[str, ...] = field(default_factory=tuple)
    related_vulnerabilities: tuple[str, ...] = field(default_factory=tuple)
    related_ttps: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hunt_id": self.hunt_id,
            "title": self.title,
            "description": self.description,
            "hypothesis_text": self.hypothesis_text,
            "assumptions": list(self.assumptions),
            "supporting_evidence": list(self.supporting_evidence),
            "contradicting_evidence": list(self.contradicting_evidence),
            "status": self.status,
            "validated": self.validated,
            "validated_by": self.validated_by,
            "validated_at": self.validated_at,
            "validation_notes": self.validation_notes,
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "related_indicators": list(self.related_indicators),
            "related_actors": list(self.related_actors),
            "related_malware": list(self.related_malware),
            "related_campaigns": list(self.related_campaigns),
            "related_infrastructure": list(self.related_infrastructure),
            "related_vulnerabilities": list(self.related_vulnerabilities),
            "related_ttps": list(self.related_ttps),
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base


@dataclass(frozen=True)
class HypothesisHistory(HuntBase):
    """Hypothesis version history."""
    hypothesis_id: str = ""
    versions: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    total_revisions: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hypothesis_id": self.hypothesis_id,
            "versions": list(self.versions),
            "total_revisions": self.total_revisions,
        })
        return base


@dataclass(frozen=True)
class HypothesisVersion(HuntBase):
    """Hypothesis version."""
    hypothesis_id: str = ""
    version_number: int = 1
    changes: str = ""
    changes_summary: str = ""
    changed_by: str = ""
    change_reason: str = ""
    previous_version_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hypothesis_id": self.hypothesis_id,
            "version_number": self.version_number,
            "changes": self.changes,
            "changes_summary": self.changes_summary,
            "changed_by": self.changed_by,
            "change_reason": self.change_reason,
            "previous_version_id": self.previous_version_id,
        })
        return base
