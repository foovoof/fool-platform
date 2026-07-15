"""
knowledge/inference/engine/inference_session.py

Inference Session Model.

Represents an inference execution context.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class InferenceSession:
    """
    Represents an inference execution session.
    
    Tracks the complete context of an inference run including:
    - Session metadata
    - Rules evaluated
    - Evidence used
    - Conclusions generated
    - Confidence updates
    """
    session_id: str = field(default_factory=lambda: str(uuid4()))
    graph_id: str = ""
    graph_version: str = ""
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: str | None = None
    rules_evaluated: list[str] = field(default_factory=list)
    rules_triggered: list[str] = field(default_factory=list)
    evidence_used: list[str] = field(default_factory=list)
    conclusions_generated: list[str] = field(default_factory=list)
    confidence_updates: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    status: str = "active"
    
    def mark_completed(self) -> None:
        """Mark the session as completed."""
        self.completed_at = datetime.now(timezone.utc).isoformat()
        self.status = "completed"
    
    def mark_failed(self, reason: str) -> None:
        """Mark the session as failed."""
        self.completed_at = datetime.now(timezone.utc).isoformat()
        self.status = "failed"
        self.metadata["failure_reason"] = reason
    
    def add_rule_evaluated(self, rule_id: str) -> None:
        """Add a rule that was evaluated."""
        if rule_id not in self.rules_evaluated:
            self.rules_evaluated.append(rule_id)
    
    def add_rule_triggered(self, rule_id: str) -> None:
        """Add a rule that was triggered."""
        if rule_id not in self.rules_triggered:
            self.rules_triggered.append(rule_id)
    
    def add_evidence(self, evidence_id: str) -> None:
        """Add evidence used."""
        if evidence_id not in self.evidence_used:
            self.evidence_used.append(evidence_id)
    
    def add_conclusion(self, conclusion_id: str) -> None:
        """Add a conclusion generated."""
        if conclusion_id not in self.conclusions_generated:
            self.conclusions_generated.append(conclusion_id)
    
    def add_confidence_update(self, update_id: str) -> None:
        """Add a confidence update."""
        if update_id not in self.confidence_updates:
            self.confidence_updates.append(update_id)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "session_id": self.session_id,
            "graph_id": self.graph_id,
            "graph_version": self.graph_version,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "rules_evaluated": self.rules_evaluated,
            "rules_triggered": self.rules_triggered,
            "evidence_used": self.evidence_used,
            "conclusions_generated": self.conclusions_generated,
            "confidence_updates": self.confidence_updates,
            "metadata": self.metadata,
            "status": self.status,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InferenceSession:
        """Create session from dictionary."""
        return cls(**data)
