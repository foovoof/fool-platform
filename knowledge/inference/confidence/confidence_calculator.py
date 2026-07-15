"""
knowledge/inference/confidence/confidence_calculator.py

Confidence Calculator for Inference Engine.

Provides deterministic confidence calculations.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from knowledge.inference.confidence.confidence_model import (
    ConfidenceRecord,
    ConfidenceLevel,
)


@dataclass
class CalculationInput:
    """Input for confidence calculation."""
    base_confidence: float = 1.0
    evidence_count: int = 0
    supporting_evidence: int = 0
    contradicting_evidence: int = 0
    rule_confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CalculationResult:
    """Result of confidence calculation."""
    value: float
    level: ConfidenceLevel
    rationale: str
    factors: list[dict[str, Any]] = field(default_factory=list)


class ConfidenceCalculator:
    """
    Calculates confidence values deterministically.
    
    All calculations are explainable.
    No ML or probabilistic models.
    """
    
    def calculate_confidence(
        self,
        input_data: CalculationInput,
    ) -> CalculationResult:
        """
        Calculate confidence from input data.
        
        Args:
            input_data: Calculation input
            
        Returns:
            Calculation result
        """
        factors: list[dict[str, Any]] = []
        value = input_data.base_confidence
        
        if input_data.rule_confidence < 1.0:
            rule_factor = input_data.rule_confidence
            factors.append({
                "factor": "rule_confidence",
                "value": rule_factor,
                "description": f"Rule confidence: {rule_factor}",
            })
            value *= rule_factor
        
        if input_data.evidence_count > 0:
            evidence_factor = min(input_data.evidence_count * 0.05, 0.2)
            factors.append({
                "factor": "evidence_count",
                "value": evidence_factor,
                "description": f"Evidence count bonus: +{evidence_factor}",
            })
            value = min(value + evidence_factor, 1.0)
        
        if input_data.supporting_evidence > 0:
            supporting_factor = min(input_data.supporting_evidence * 0.1, 0.3)
            factors.append({
                "factor": "supporting_evidence",
                "value": supporting_factor,
                "description": f"Supporting evidence bonus: +{supporting_factor}",
            })
            value = min(value + supporting_factor, 1.0)
        
        if input_data.contradicting_evidence > 0:
            contradiction_factor = min(
                input_data.contradicting_evidence * 0.15,
                0.5,
            )
            factors.append({
                "factor": "contradicting_evidence",
                "value": -contradiction_factor,
                "description": f"Contradiction penalty: -{contradiction_factor}",
            })
            value = max(value - contradiction_factor, 0.0)
        
        value = max(0.0, min(1.0, value))
        
        if value >= 0.8:
            level = ConfidenceLevel.HIGH
        elif value >= 0.5:
            level = ConfidenceLevel.MEDIUM
        elif value > 0.0:
            level = ConfidenceLevel.LOW
        else:
            level = ConfidenceLevel.UNKNOWN
        
        rationale = self._generate_rationale(input_data, value, factors)
        
        return CalculationResult(
            value=value,
            level=level,
            rationale=rationale,
            factors=factors,
        )
    
    def merge_confidences(
        self,
        confidences: list[float],
        method: str = "average",
    ) -> float:
        """
        Merge multiple confidence values.
        
        Args:
            confidences: List of confidence values
            method: Merge method ('average', 'min', 'max', 'weighted')
            
        Returns:
            Merged confidence value
        """
        if not confidences:
            return 0.0
        
        valid_confidences = [c for c in confidences if 0.0 <= c <= 1.0]
        if not valid_confidences:
            return 0.0
        
        if method == "average":
            return sum(valid_confidences) / len(valid_confidences)
        
        if method == "min":
            return min(valid_confidences)
        
        if method == "max":
            return max(valid_confidences)
        
        if method == "weighted":
            weights = [1.0 / len(valid_confidences)] * len(valid_confidences)
            return sum(c * w for c, w in zip(valid_confidences, weights))
        
        return sum(valid_confidences) / len(valid_confidences)
    
    def propagate_confidence(
        self,
        source_confidence: float,
        propagation_factor: float = 0.9,
        hops: int = 1,
    ) -> list[float]:
        """
        Propagate confidence with decay.
        
        Args:
            source_confidence: Source confidence value
            propagation_factor: Decay factor per hop
            hops: Number of hops
            
        Returns:
            List of confidence values per hop
        """
        result: list[float] = [source_confidence]
        current = source_confidence
        
        for _ in range(hops):
            current *= propagation_factor
            result.append(current)
        
        return result
    
    def validate_confidence(self, value: float) -> bool:
        """
        Validate a confidence value.
        
        Args:
            value: The value to validate
            
        Returns:
            True if valid
        """
        return 0.0 <= value <= 1.0
    
    def create_record(
        self,
        entity_id: str,
        entity_type: str,
        value: float,
        source_rule: str | None = None,
        evidence_ids: list[str] | None = None,
        rationale: str = "",
    ) -> ConfidenceRecord:
        """
        Create a confidence record.
        
        Args:
            entity_id: Entity ID
            entity_type: Entity type
            value: Confidence value
            source_rule: Source rule ID
            evidence_ids: Evidence IDs
            rationale: Rationale for the value
            
        Returns:
            Confidence record
        """
        if not self.validate_confidence(value):
            value = max(0.0, min(1.0, value))
        
        return ConfidenceRecord(
            entity_id=entity_id,
            entity_type=entity_type,
            value=value,
            source_rule=source_rule,
            evidence_ids=evidence_ids or [],
            rationale=rationale,
        )
    
    def _generate_rationale(
        self,
        input_data: CalculationInput,
        value: float,
        factors: list[dict[str, Any]],
    ) -> str:
        """Generate rationale for calculation."""
        parts = [
            f"Base confidence: {input_data.base_confidence}",
        ]
        
        if input_data.evidence_count > 0:
            parts.append(
                f"Evidence count: {input_data.evidence_count} pieces"
            )
        
        if input_data.supporting_evidence > 0:
            parts.append(
                f"Supporting evidence: {input_data.supporting_evidence}"
            )
        
        if input_data.contradicting_evidence > 0:
            parts.append(
                f"Contradicting evidence: {input_data.contradicting_evidence}"
            )
        
        parts.append(f"Final confidence: {value:.2f}")
        
        return "; ".join(parts)
