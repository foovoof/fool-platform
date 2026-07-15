"""
knowledge/inference/explanation/explanation_model.py

Explanation Model for Inference Engine.

Defines explanation structure.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class Explanation:
    """
    Represents an explanation for an inference result.
    
    Every inference result must have an explanation.
    Explanations are always human-readable.
    """
    explanation_id: str = field(default_factory=lambda: str(uuid4()))
    rule_id: str = ""
    rule_name: str = ""
    evidence_ids: list[str] = field(default_factory=list)
    conclusion_ids: list[str] = field(default_factory=list)
    generated_text: str = ""
    steps: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def add_step(
        self,
        step_type: str,
        description: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Add an explanation step."""
        self.steps.append({
            "type": step_type,
            "description": description,
            "details": details or {},
        })
    
    def to_dict(self) -> dict[str, Any]:
        """Convert explanation to dictionary."""
        return {
            "explanation_id": self.explanation_id,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "evidence_ids": self.evidence_ids,
            "conclusion_ids": self.conclusion_ids,
            "generated_text": self.generated_text,
            "steps": self.steps,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Explanation:
        """Create explanation from dictionary."""
        return cls(**data)
