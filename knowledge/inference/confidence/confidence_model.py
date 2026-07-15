"""
knowledge/inference/confidence/confidence_model.py

Confidence Model for Inference Engine.

Defines confidence records and levels.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ConfidenceLevel(Enum):
    """Confidence level categories."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


@dataclass
class ConfidenceRecord:
    """
    Represents a confidence record.
    
    Tracks the confidence value, source, and rationale.
    """
    confidence_id: str = field(default_factory=lambda: str(uuid4()))
    entity_id: str = ""
    entity_type: str = ""
    value: float = 0.0
    source_rule: str | None = None
    evidence_ids: list[str] = field(default_factory=list)
    rationale: str = ""
    calculation_method: str = "rule_based"
    metadata: dict[str, Any] = field(default_factory=dict)
    calculated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    @property
    def level(self) -> ConfidenceLevel:
        """Get the confidence level."""
        if self.value >= 0.8:
            return ConfidenceLevel.HIGH
        elif self.value >= 0.5:
            return ConfidenceLevel.MEDIUM
        elif self.value >= 0.0:
            return ConfidenceLevel.LOW
        return ConfidenceLevel.UNKNOWN
    
    def is_valid(self) -> bool:
        """Check if confidence value is valid."""
        return 0.0 <= self.value <= 1.0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert record to dictionary."""
        return {
            "confidence_id": self.confidence_id,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "value": self.value,
            "source_rule": self.source_rule,
            "evidence_ids": self.evidence_ids,
            "rationale": self.rationale,
            "calculation_method": self.calculation_method,
            "level": self.level.value,
            "metadata": self.metadata,
            "calculated_at": self.calculated_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConfidenceRecord:
        """Create record from dictionary."""
        return cls(**data)


@dataclass
class ConfidenceUpdate:
    """
    Represents an update to a confidence value.
    
    Tracks the change from old to new value.
    """
    update_id: str = field(default_factory=lambda: str(uuid4()))
    entity_id: str = ""
    old_value: float = 0.0
    new_value: float = 0.0
    change: float = 0.0
    source_rule: str | None = None
    evidence_ids: list[str] = field(default_factory=list)
    update_reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def __post_init__(self) -> None:
        """Calculate change after initialization."""
        self.change = self.new_value - self.old_value
    
    @property
    def is_increase(self) -> bool:
        """Check if confidence increased."""
        return self.change > 0
    
    @property
    def is_decrease(self) -> bool:
        """Check if confidence decreased."""
        return self.change < 0
    
    @property
    def is_significant(self) -> bool:
        """Check if change is significant (>= 0.1)."""
        return abs(self.change) >= 0.1
    
    def to_dict(self) -> dict[str, Any]:
        """Convert update to dictionary."""
        return {
            "update_id": self.update_id,
            "entity_id": self.entity_id,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "change": self.change,
            "source_rule": self.source_rule,
            "evidence_ids": self.evidence_ids,
            "update_reason": self.update_reason,
            "metadata": self.metadata,
            "updated_at": self.updated_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConfidenceUpdate:
        """Create update from dictionary."""
        return cls(**data)


@dataclass
class ConfidenceChain:
    """Represents a chain of confidence updates."""
    chain_id: str = field(default_factory=lambda: str(uuid4()))
    entity_id: str = ""
    updates: list[ConfidenceUpdate] = field(default_factory=list)
    final_value: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def add_update(self, update: ConfidenceUpdate) -> None:
        """Add an update to the chain."""
        self.updates.append(update)
        self.final_value = update.new_value
    
    def to_dict(self) -> dict[str, Any]:
        """Convert chain to dictionary."""
        return {
            "chain_id": self.chain_id,
            "entity_id": self.entity_id,
            "updates": [u.to_dict() for u in self.updates],
            "final_value": self.final_value,
            "metadata": self.metadata,
        }
