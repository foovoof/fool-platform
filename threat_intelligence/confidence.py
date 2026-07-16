"""
threat_intelligence/confidence.py

Confidence Module.

Provides confidence assessment for threat intelligence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class ConfidenceAssessment:
    """Confidence assessment."""
    confidence_level: str = "medium"
    confidence_score: float = 0.5
    source_reliability: str = "unknown"
    information_reliability: str = "unknown"
    rationale: str = ""
    assessed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    assessed_by: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "source_reliability": self.source_reliability,
            "information_reliability": self.information_reliability,
            "rationale": self.rationale,
            "assessed_at": self.assessed_at,
            "assessed_by": self.assessed_by,
        }


@dataclass(frozen=True)
class SourceAssessment:
    """Source reliability assessment."""
    source_name: str = ""
    source_type: str = ""
    reliability: str = "unknown"
    track_record: str = ""
    notes: str = ""
    assessed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "source_name": self.source_name,
            "source_type": self.source_type,
            "reliability": self.reliability,
            "track_record": self.track_record,
            "notes": self.notes,
            "assessed_at": self.assessed_at,
        }


@dataclass(frozen=True)
class ReliabilityAssessment:
    """Information reliability assessment."""
    reliability_level: str = "unknown"
    corroborating_sources: tuple[str, ...] = field(default_factory=tuple)
    conflicting_sources: tuple[str, ...] = field(default_factory=tuple)
    explanation: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "reliability_level": self.reliability_level,
            "corroborating_sources": list(self.corroborating_sources),
            "conflicting_sources": list(self.conflicting_sources),
            "explanation": self.explanation,
        }


class ConfidenceHistory:
    """
    History of confidence assessments.
    
    Tracks changes to confidence over time.
    """
    
    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id
        self._history: list[ConfidenceAssessment] = []
    
    def add_assessment(self, assessment: ConfidenceAssessment) -> None:
        """Add an assessment to history."""
        self._history.append(assessment)
    
    def get_latest(self) -> ConfidenceAssessment | None:
        """Get the latest assessment."""
        if self._history:
            return self._history[-1]
        return None
    
    def get_all(self) -> list[ConfidenceAssessment]:
        """Get all assessments."""
        return list(self._history)


class ConfidenceService:
    """
    Service for managing confidence assessments.
    
    Rule-based confidence calculation.
    No probabilistic AI.
    """
    
    def __init__(self) -> None:
        self._histories: dict[str, ConfidenceHistory] = {}
        self._source_assessments: dict[str, SourceAssessment] = {}
    
    def calculate_confidence(
        self,
        source_reliability: str,
        information_reliability: str,
    ) -> tuple[str, float]:
        """
        Calculate confidence based on source and information reliability.
        
        Rule-based calculation:
        - A + Confirmed = HIGH (0.9)
        - A + Likely = HIGH (0.8)
        - B + Confirmed = HIGH (0.75)
        - B + Likely = MEDIUM (0.6)
        - C + Likely = MEDIUM (0.5)
        - D + Possible = LOW (0.3)
        - E/F + any = LOW (0.2)
        
        Args:
            source_reliability: Source reliability rating
            information_reliability: Information reliability rating
            
        Returns:
            Tuple of (confidence_level, confidence_score)
        """
        score_map: dict[tuple[str, str], tuple[str, float]] = {
            ("a", "confirmed"):
                ("high", 0.9),
            ("a", "likely"):
                ("high", 0.8),
            ("a", "possible"):
                ("high", 0.7),
            ("b", "confirmed"):
                ("high", 0.75),
            ("b", "likely"):
                ("medium", 0.6),
            ("b", "possible"):
                ("medium", 0.5),
            ("c", "likely"):
                ("medium", 0.5),
            ("c", "possible"):
                ("low", 0.4),
            ("d", "possible"):
                ("low", 0.3),
            ("d", "doubtful"):
                ("low", 0.2),
            ("e", "unknown"):
                ("low", 0.2),
            ("f", "unknown"):
                ("low", 0.1),
        }
        
        result = score_map.get((source_reliability.lower(), information_reliability.lower()))
        if result:
            return result
        
        return ("medium", 0.5)
    
    def assess_source(
        self,
        source_name: str,
        source_type: str = "",
        reliability: str = "unknown",
        track_record: str = "",
        notes: str = "",
    ) -> SourceAssessment:
        """Assess a source's reliability."""
        assessment = SourceAssessment(
            source_name=source_name,
            source_type=source_type,
            reliability=reliability,
            track_record=track_record,
            notes=notes,
            assessed_at=datetime.now(timezone.utc).isoformat(),
        )
        self._source_assessments[source_name] = assessment
        return assessment
    
    def get_source_assessment(self, source_name: str) -> SourceAssessment | None:
        """Get source assessment."""
        return self._source_assessments.get(source_name)
    
    def record_confidence(
        self,
        entity_id: str,
        assessment: ConfidenceAssessment,
    ) -> None:
        """Record confidence assessment for an entity."""
        if entity_id not in self._histories:
            self._histories[entity_id] = ConfidenceHistory(entity_id)
        self._histories[entity_id].add_assessment(assessment)
    
    def get_confidence_history(self, entity_id: str) -> ConfidenceHistory | None:
        """Get confidence history for an entity."""
        return self._histories.get(entity_id)
    
    def get_latest_confidence(self, entity_id: str) -> ConfidenceAssessment | None:
        """Get latest confidence assessment for an entity."""
        history = self._histories.get(entity_id)
        if history:
            return history.get_latest()
        return None
