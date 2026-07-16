"""
threat_intelligence/models/findings.py

Finding Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.models.base import ThreatBase, Auditable, Explainable, ConfidenceMixin
from threat_intelligence.models.enums import FindingType, ThreatLevel


@dataclass(frozen=True)
class IntelligenceFinding(ThreatBase, Auditable, Explainable, ConfidenceMixin):
    """Intelligence finding."""
    title: str = ""
    description: str = ""
    finding_type: str = FindingType.THREAT_ACTOR.value
    threat_level: str = ThreatLevel.MEDIUM.value
    entities: tuple[str, ...] = field(default_factory=tuple)
    entity_types: tuple[str, ...] = field(default_factory=tuple)
    related_findings: tuple[str, ...] = field(default_factory=tuple)
    supporting_evidence: tuple[str, ...] = field(default_factory=tuple)
    recommended_actions: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    status: str = "new"
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "title": self.title,
            "description": self.description,
            "finding_type": self.finding_type,
            "threat_level": self.threat_level,
            "entities": list(self.entities),
            "entity_types": list(self.entity_types),
            "related_findings": list(self.related_findings),
            "supporting_evidence": list(self.supporting_evidence),
            "recommended_actions": list(self.recommended_actions),
            "tags": list(self.tags),
            "status": self.status,
            "explanation": self.explanation,
            "reasoning": self.reasoning,
        })
        return base


@dataclass(frozen=True)
class Sighting(ThreatBase, Auditable, ConfidenceMixin):
    """Sighting of a threat entity."""
    entity_type: str = ""
    entity_id: str = ""
    entity_value: str = ""
    sighting_count: int = 1
    first_sighted: str = ""
    last_sighted: str = ""
    sighting_locations: tuple[str, ...] = field(default_factory=tuple)
    sighting_context: str = ""
    related_indicators: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "entity_value": self.entity_value,
            "sighting_count": self.sighting_count,
            "first_sighted": self.first_sighted,
            "last_sighted": self.last_sighted,
            "sighting_locations": list(self.sighting_locations),
            "sighting_context": self.sighting_context,
            "related_indicators": list(self.related_indicators),
            "tags": list(self.tags),
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base


@dataclass(frozen=True)
class Observation(ThreatBase, Auditable):
    """Raw observation."""
    observation_type: str = ""
    content: dict[str, Any] = field(default_factory=dict)
    source: str = ""
    collected_at: str = ""
    location: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "observation_type": self.observation_type,
            "content": self.content,
            "source": self.source,
            "collected_at": self.collected_at,
            "location": self.location,
            "tags": list(self.tags),
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base
