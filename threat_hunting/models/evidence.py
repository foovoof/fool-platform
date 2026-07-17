"""
threat_hunting/models/evidence.py

Evidence Models.
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
class EvidenceReference(HuntBase, Auditable, ProvenanceMixin):
    """Evidence reference."""
    bundle_id: str = ""
    evidence_type: str = ""
    entity_type: str = ""
    entity_id: str = ""
    description: str = ""
    relevance_score: float = 0.5
    supporting_findings: tuple[str, ...] = field(default_factory=tuple)
    contradicting_findings: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "bundle_id": self.bundle_id,
            "evidence_type": self.evidence_type,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "description": self.description,
            "relevance_score": self.relevance_score,
            "supporting_findings": list(self.supporting_findings),
            "contradicting_findings": list(self.contradicting_findings),
            "author": self.author,
            "reason": self.reason,
            "provenance_source": self.provenance_source,
            "provenance_url": self.provenance_url,
        })
        return base


@dataclass(frozen=True)
class EvidenceChain(HuntBase):
    """Evidence chain."""
    chain_id: str = ""
    bundle_id: str = ""
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    chain_type: str = ""
    description: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "chain_id": self.chain_id,
            "bundle_id": self.bundle_id,
            "evidence_ids": list(self.evidence_ids),
            "chain_type": self.chain_type,
            "description": self.description,
        })
        return base


@dataclass(frozen=True)
class EvidenceBundle(HuntBase, Auditable, ConfidenceMixin):
    """Evidence bundle."""
    hunt_id: str = ""
    session_id: str = ""
    finding_id: str = ""
    title: str = ""
    description: str = ""
    evidence_refs: tuple[EvidenceReference, ...] = field(default_factory=tuple)
    evidence_chains: tuple[EvidenceChain, ...] = field(default_factory=tuple)
    aggregate_confidence: float = 0.5
    aggregate_explanation: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hunt_id": self.hunt_id,
            "session_id": self.session_id,
            "finding_id": self.finding_id,
            "title": self.title,
            "description": self.description,
            "evidence_refs": [e.to_dict() for e in self.evidence_refs],
            "evidence_chains": [c.to_dict() for c in self.evidence_chains],
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "aggregate_confidence": self.aggregate_confidence,
            "aggregate_explanation": self.aggregate_explanation,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class ConfidenceHistory(HuntBase):
    """Confidence history entry."""
    entity_type: str = ""
    entity_id: str = ""
    previous_confidence: float = 0.0
    new_confidence: float = 0.0
    change_reason: str = ""
    supporting_evidence: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "previous_confidence": self.previous_confidence,
            "new_confidence": self.new_confidence,
            "change_reason": self.change_reason,
            "supporting_evidence": list(self.supporting_evidence),
        })
        return base
