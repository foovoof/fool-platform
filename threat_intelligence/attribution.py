"""
threat_intelligence/attribution.py

Attribution Support Module.

Provides attribution support without implementing attribution engine.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AttributionEvidence:
    """Evidence supporting attribution."""
    evidence_id: str = ""
    evidence_type: str = ""
    description: str = ""
    weight: float = 0.0


@dataclass(frozen=True)
class AttributionIndicator:
    """Indicator supporting attribution."""
    indicator_id: str = ""
    indicator_type: str = ""
    value: str = ""
    weight: float = 0.0


@dataclass(frozen=True)
class AttributionRelationship:
    """Relationship supporting attribution."""
    relationship_id: str = ""
    source_entity: str = ""
    target_entity: str = ""
    relationship_type: str = ""
    weight: float = 0.0


@dataclass(frozen=True)
class AttributionConfidence:
    """Confidence reference for attribution."""
    confidence_level: str = "medium"
    confidence_score: float = 0.5
    explanation: str = ""


@dataclass(frozen=True)
class AttributionSupport:
    """
    Attribution support data.
    
    This is a data structure only.
    No attribution logic is implemented.
    """
    target_type: str = ""
    target_id: str = ""
    evidence: tuple[AttributionEvidence, ...] = field(default_factory=tuple)
    indicators: tuple[AttributionIndicator, ...] = field(default_factory=tuple)
    relationships: tuple[AttributionRelationship, ...] = field(default_factory=tuple)
    confidence: AttributionConfidence | None = None
    explanation: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "target_type": self.target_type,
            "target_id": self.target_id,
            "evidence": [
                {"evidence_id": e.evidence_id, "evidence_type": e.evidence_type,
                 "description": e.description, "weight": e.weight}
                for e in self.evidence
            ],
            "indicators": [
                {"indicator_id": i.indicator_id, "indicator_type": i.indicator_type,
                 "value": i.value, "weight": i.weight}
                for i in self.indicators
            ],
            "relationships": [
                {"relationship_id": r.relationship_id, "source_entity": r.source_entity,
                 "target_entity": r.target_entity, "relationship_type": r.relationship_type,
                 "weight": r.weight}
                for r in self.relationships
            ],
            "confidence": self.confidence.__dict__ if self.confidence else None,
            "explanation": self.explanation,
        }


class AttributionBuilder:
    """
    Builder for attribution support.
    
    Only builds attribution data structures.
    No attribution logic.
    """
    
    def __init__(self, target_type: str, target_id: str) -> None:
        self._target_type = target_type
        self._target_id = target_id
        self._evidence: list[AttributionEvidence] = []
        self._indicators: list[AttributionIndicator] = []
        self._relationships: list[AttributionRelationship] = []
        self._confidence: AttributionConfidence | None = None
        self._explanation: str = ""
    
    def add_evidence(
        self,
        evidence_id: str,
        evidence_type: str,
        description: str = "",
        weight: float = 1.0,
    ) -> AttributionBuilder:
        """Add supporting evidence."""
        self._evidence.append(AttributionEvidence(
            evidence_id=evidence_id,
            evidence_type=evidence_type,
            description=description,
            weight=weight,
        ))
        return self
    
    def add_indicator(
        self,
        indicator_id: str,
        indicator_type: str,
        value: str = "",
        weight: float = 1.0,
    ) -> AttributionBuilder:
        """Add supporting indicator."""
        self._indicators.append(AttributionIndicator(
            indicator_id=indicator_id,
            indicator_type=indicator_type,
            value=value,
            weight=weight,
        ))
        return self
    
    def add_relationship(
        self,
        relationship_id: str,
        source_entity: str,
        target_entity: str,
        relationship_type: str,
        weight: float = 1.0,
    ) -> AttributionBuilder:
        """Add supporting relationship."""
        self._relationships.append(AttributionRelationship(
            relationship_id=relationship_id,
            source_entity=source_entity,
            target_entity=target_entity,
            relationship_type=relationship_type,
            weight=weight,
        ))
        return self
    
    def set_confidence(
        self,
        confidence_level: str,
        confidence_score: float,
        explanation: str = "",
    ) -> AttributionBuilder:
        """Set confidence reference."""
        self._confidence = AttributionConfidence(
            confidence_level=confidence_level,
            confidence_score=confidence_score,
            explanation=explanation,
        )
        return self
    
    def set_explanation(self, explanation: str) -> AttributionBuilder:
        """Set explanation."""
        self._explanation = explanation
        return self
    
    def build(self) -> AttributionSupport:
        """Build attribution support."""
        return AttributionSupport(
            target_type=self._target_type,
            target_id=self._target_id,
            evidence=tuple(self._evidence),
            indicators=tuple(self._indicators),
            relationships=tuple(self._relationships),
            confidence=self._confidence,
            explanation=self._explanation,
        )
