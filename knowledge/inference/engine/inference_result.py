"""
knowledge/inference/engine/inference_result.py

Inference Result and Conclusion Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ConclusionType(Enum):
    """Types of inference conclusions."""
    FACT = "fact"
    RELATIONSHIP = "relationship"
    ATTRIBUTE = "attribute"
    IDENTITY = "identity"
    CLASSIFICATION = "classification"
    ASSOCIATION = "association"
    DERIVATION = "derivation"


@dataclass
class InferenceConclusion:
    """
    Represents a single conclusion from inference.
    
    Conclusions are derived from rules and evidence.
    """
    conclusion_id: str = field(default_factory=lambda: str(uuid4()))
    conclusion_type: ConclusionType = ConclusionType.FACT
    conclusion_value: Any = None
    evidence_ids: list[str] = field(default_factory=list)
    confidence: float = 0.0
    explanation_id: str | None = None
    source_rule_id: str | None = None
    derived_from: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def is_valid(self) -> bool:
        """Check if conclusion is valid."""
        return (
            self.conclusion_value is not None
            and 0.0 <= self.confidence <= 1.0
            and len(self.evidence_ids) > 0
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert conclusion to dictionary."""
        return {
            "conclusion_id": self.conclusion_id,
            "conclusion_type": self.conclusion_type.value,
            "conclusion_value": self.conclusion_value,
            "evidence_ids": self.evidence_ids,
            "confidence": self.confidence,
            "explanation_id": self.explanation_id,
            "source_rule_id": self.source_rule_id,
            "derived_from": self.derived_from,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InferenceConclusion:
        """Create conclusion from dictionary."""
        if isinstance(data.get("conclusion_type"), str):
            data["conclusion_type"] = ConclusionType(data["conclusion_type"])
        return cls(**data)


@dataclass
class InferenceResult:
    """
    Represents the complete result of an inference session.
    
    Contains all conclusions, evidence references, confidence updates,
    and recommendations generated during inference.
    """
    result_id: str = field(default_factory=lambda: str(uuid4()))
    session_id: str = ""
    inferred_facts: list[dict[str, Any]] = field(default_factory=list)
    inferred_relationships: list[dict[str, Any]] = field(default_factory=list)
    evidence_references: list[str] = field(default_factory=list)
    confidence_updates: list[dict[str, Any]] = field(default_factory=list)
    explanations: list[dict[str, Any]] = field(default_factory=list)
    recommendations: list[dict[str, Any]] = field(default_factory=list)
    conclusions: list[InferenceConclusion] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def add_conclusion(self, conclusion: InferenceConclusion) -> None:
        """Add a conclusion."""
        self.conclusions.append(conclusion)
        
        fact = {
            "conclusion_id": conclusion.conclusion_id,
            "type": conclusion.conclusion_type.value,
            "value": conclusion.conclusion_value,
            "confidence": conclusion.confidence,
            "evidence": conclusion.evidence_ids,
        }
        self.inferred_facts.append(fact)
    
    def add_evidence_reference(self, evidence_id: str) -> None:
        """Add an evidence reference."""
        if evidence_id not in self.evidence_references:
            self.evidence_references.append(evidence_id)
    
    def add_confidence_update(
        self,
        entity_id: str,
        old_confidence: float,
        new_confidence: float,
        rule_id: str,
    ) -> None:
        """Add a confidence update."""
        update = {
            "entity_id": entity_id,
            "old_confidence": old_confidence,
            "new_confidence": new_confidence,
            "rule_id": rule_id,
        }
        self.confidence_updates.append(update)
    
    def add_explanation(self, explanation: dict[str, Any]) -> None:
        """Add an explanation."""
        self.explanations.append(explanation)
    
    def add_recommendation(
        self,
        recommendation_type: str,
        entity_id: str,
        action: str,
        rationale: str,
    ) -> None:
        """Add a recommendation."""
        recommendation = {
            "type": recommendation_type,
            "entity_id": entity_id,
            "action": action,
            "rationale": rationale,
        }
        self.recommendations.append(recommendation)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "result_id": self.result_id,
            "session_id": self.session_id,
            "inferred_facts": self.inferred_facts,
            "inferred_relationships": self.inferred_relationships,
            "evidence_references": self.evidence_references,
            "confidence_updates": self.confidence_updates,
            "explanations": self.explanations,
            "recommendations": self.recommendations,
            "conclusions": [c.to_dict() for c in self.conclusions],
            "created_at": self.created_at,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InferenceResult:
        """Create result from dictionary."""
        if "conclusions" in data:
            data["conclusions"] = [
                InferenceConclusion.from_dict(c)
                for c in data["conclusions"]
            ]
        return cls(**data)
