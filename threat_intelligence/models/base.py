"""
threat_intelligence/models/base.py

Base Models for Threat Intelligence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class ThreatBase:
    """Base class for threat intelligence entities."""
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    modified_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    created_by: str = ""
    modified_by: str = ""
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "created_by": self.created_by,
            "modified_by": self.modified_by,
            "version": self.version,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class Auditable:
    """Mixin for auditable entities."""
    author: str = ""
    reason: str = ""
    source: str = ""
    source_url: str = ""
    source_confidence: str = "unknown"
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
            "source_url": self.source_url,
            "source_confidence": self.source_confidence,
        }


@dataclass(frozen=True)
class Versionable:
    """Mixin for versionable entities."""
    revision_history: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "revision_history": list(self.revision_history),
        }


@dataclass(frozen=True)
class Explainable:
    """Mixin for explainable entities."""
    explanation: str = ""
    reasoning: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "explanation": self.explanation,
            "reasoning": self.reasoning,
        }


@dataclass(frozen=True)
class ConfidenceMixin:
    """Mixin for confidence-related entities."""
    confidence_level: str = "medium"
    confidence_score: float = 0.5
    confidence_explanation: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
        }
