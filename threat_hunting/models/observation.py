"""
threat_hunting/models/observation.py

Observation and Finding Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_hunting.models.base import (
    HuntBase,
    Auditable,
    ConfidenceMixin,
    ProvenanceMixin,
)


@dataclass(frozen=True)
class HuntObservation(HuntBase, Auditable, ConfidenceMixin, ProvenanceMixin):
    """Hunt observation."""
    hunt_id: str = ""
    session_id: str = ""
    hypothesis_id: str = ""
    source: str = ""
    description: str = ""
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    entity_refs: tuple[str, ...] = field(default_factory=tuple)
    relationships: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    significance: str = "normal"
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hunt_id": self.hunt_id,
            "session_id": self.session_id,
            "hypothesis_id": self.hypothesis_id,
            "source": self.source,
            "description": self.description,
            "evidence_ids": list(self.evidence_ids),
            "entity_refs": list(self.entity_refs),
            "relationships": list(self.relationships),
            "significance": self.significance,
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "metadata": self.metadata,
            "author": self.author,
            "reason": self.reason,
            "source_url": self.source_url,
        })
        return base


@dataclass(frozen=True)
class HuntFinding(HuntBase, Auditable, ConfidenceMixin):
    """Hunt finding."""
    hunt_id: str = ""
    session_id: str = ""
    hypothesis_id: str = ""
    title: str = ""
    description: str = ""
    severity: str = "informational"
    evidence_bundle_id: str = ""
    explanation: str = ""
    recommendation_ids: tuple[str, ...] = field(default_factory=tuple)
    related_observations: tuple[str, ...] = field(default_factory=tuple)
    related_entities: tuple[str, ...] = field(default_factory=tuple)
    cti_references: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hunt_id": self.hunt_id,
            "session_id": self.session_id,
            "hypothesis_id": self.hypothesis_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "evidence_bundle_id": self.evidence_bundle_id,
            "explanation": self.explanation,
            "recommendation_ids": list(self.recommendation_ids),
            "related_observations": list(self.related_observations),
            "related_entities": list(self.related_entities),
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "cti_references": list(self.cti_references),
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class HuntRecommendation(HuntBase, Auditable):
    """Hunt recommendation."""
    hunt_id: str = ""
    finding_id: str = ""
    recommendation_type: str = ""
    title: str = ""
    description: str = ""
    priority: int = 3
    target_entity_type: str = ""
    target_entity_id: str = ""
    action_required: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hunt_id": self.hunt_id,
            "finding_id": self.finding_id,
            "recommendation_type": self.recommendation_type,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "target_entity_type": self.target_entity_type,
            "target_entity_id": self.target_entity_id,
            "action_required": self.action_required,
            "author": self.author,
            "reason": self.reason,
        })
        return base
