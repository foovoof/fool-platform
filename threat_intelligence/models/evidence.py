"""
threat_intelligence/models/evidence.py

Evidence Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.models.base import ThreatBase, Auditable, Explainable
from threat_intelligence.models.enums import EvidenceType


@dataclass(frozen=True)
class EvidenceReference(ThreatBase, Auditable, Explainable):
    """Evidence reference."""
    evidence_type: str = EvidenceType.DIRECT.value
    content: str = ""
    content_type: str = ""
    source_system: str = ""
    source_id: str = ""
    collected_at: str = ""
    collected_by: str = ""
    chain_of_custody: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "evidence_type": self.evidence_type,
            "content": self.content,
            "content_type": self.content_type,
            "source_system": self.source_system,
            "source_id": self.source_id,
            "collected_at": self.collected_at,
            "collected_by": self.collected_by,
            "chain_of_custody": list(self.chain_of_custody),
            "tags": list(self.tags),
            "explanation": self.explanation,
            "reasoning": self.reasoning,
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base


@dataclass(frozen=True)
class EvidenceBundle(ThreatBase, Auditable, Explainable):
    """Evidence bundle containing multiple evidence items."""
    title: str = ""
    description: str = ""
    evidence_items: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    related_entities: tuple[str, ...] = field(default_factory=tuple)
    threat_actor: str = ""
    malware: str = ""
    campaign: str = ""
    confidence_level: str = "medium"
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "title": self.title,
            "description": self.description,
            "evidence_items": list(self.evidence_items),
            "related_entities": list(self.related_entities),
            "threat_actor": self.threat_actor,
            "malware": self.malware,
            "campaign": self.campaign,
            "confidence_level": self.confidence_level,
            "tags": list(self.tags),
            "explanation": self.explanation,
            "reasoning": self.reasoning,
        })
        return base


@dataclass(frozen=True)
class EvidenceTimeline(ThreatBase):
    """Evidence timeline."""
    timeline_entries: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    related_entities: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "timeline_entries": list(self.timeline_entries),
            "related_entities": list(self.related_entities),
        })
        return base


@dataclass(frozen=True)
class EvidenceLineage(ThreatBase, Auditable):
    """Evidence lineage for chain of custody."""
    parent_evidence: str = ""
    child_evidence: tuple[str, ...] = field(default_factory=tuple)
    transformation_history: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "parent_evidence": self.parent_evidence,
            "child_evidence": list(self.child_evidence),
            "transformation_history": list(self.transformation_history),
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base
