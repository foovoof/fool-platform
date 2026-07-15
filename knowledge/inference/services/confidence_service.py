from __future__ import annotations

"""
knowledge/inference/services/confidence_service.py

Confidence Service for the Knowledge Layer.

Orchestrates confidence operations.
"""
from typing import Any

from knowledge.graph.models import Graph
from knowledge.inference.confidence.confidence_model import ConfidenceRecord, ConfidenceUpdate
from knowledge.inference.confidence.confidence_calculator import ConfidenceCalculator, CalculationInput
from knowledge.inference.confidence.confidence_propagation import ConfidencePropagation


class ConfidenceService:
    """
    Service for confidence management.
    
    Orchestrates:
    - Confidence calculation
    - Confidence updates
    - Confidence propagation
    """
    
    def __init__(
        self,
        calculator: ConfidenceCalculator | None = None,
        propagation: ConfidencePropagation | None = None,
    ) -> None:
        """
        Initialize the service.
        
        Args:
            calculator: Optional confidence calculator
            propagation: Optional confidence propagation
        """
        self._calculator = calculator or ConfidenceCalculator()
        self._propagation = propagation or ConfidencePropagation()
    
    def calculate(
        self,
        base_confidence: float = 1.0,
        evidence_count: int = 0,
        supporting_evidence: int = 0,
        contradicting_evidence: int = 0,
        rule_confidence: float = 1.0,
    ) -> dict[str, Any]:
        """
        Calculate confidence.
        
        Args:
            base_confidence: Base confidence
            evidence_count: Evidence count
            supporting_evidence: Supporting evidence count
            contradicting_evidence: Contradicting evidence count
            rule_confidence: Rule confidence
            
        Returns:
            Calculation result
        """
        input_data = CalculationInput(
            base_confidence=base_confidence,
            evidence_count=evidence_count,
            supporting_evidence=supporting_evidence,
            contradicting_evidence=contradicting_evidence,
            rule_confidence=rule_confidence,
        )
        
        result = self._calculator.calculate_confidence(input_data)
        
        return {
            "value": result.value,
            "level": result.level.value,
            "rationale": result.rationale,
            "factors": result.factors,
        }
    
    def merge(
        self,
        confidences: list[float],
        method: str = "average",
    ) -> dict[str, Any]:
        """
        Merge multiple confidences.
        
        Args:
            confidences: List of confidence values
            method: Merge method
            
        Returns:
            Merged result
        """
        merged = self._calculator.merge_confidences(confidences, method)
        
        return {
            "value": merged,
            "method": method,
            "count": len(confidences),
        }
    
    def update(
        self,
        entity_id: str,
        new_confidence: float,
        source_rule: str,
        evidence_ids: list[str],
        reason: str,
    ) -> dict[str, Any]:
        """
        Update confidence for an entity.
        
        Args:
            entity_id: Entity ID
            new_confidence: New confidence value
            source_rule: Source rule ID
            evidence_ids: Evidence IDs
            reason: Update reason
            
        Returns:
            Update result
        """
        update = self._propagation.update_confidence_chain(
            entity_id,
            new_confidence,
            source_rule,
            evidence_ids,
            reason,
        )
        
        return {
            "success": True,
            "update": update.to_dict(),
        }
    
    def propagate(
        self,
        source_entity_id: str,
        graph: Graph,
        decay_factor: float = 0.9,
        max_depth: int = 3,
    ) -> dict[str, Any]:
        """
        Propagate confidence from a source entity.
        
        Args:
            source_entity_id: Source entity ID
            graph: Knowledge graph
            decay_factor: Decay factor
            max_depth: Maximum depth
            
        Returns:
            Propagation result
        """
        result = self._propagation.propagate_confidence(
            source_entity_id,
            graph,
            decay_factor,
            max_depth,
        )
        
        return {
            "success": True,
            "updated_entities": result.updated_entities,
            "updates": [u.to_dict() for u in result.updates],
        }
    
    def get_confidence(self, entity_id: str) -> dict[str, Any]:
        """Get confidence for an entity."""
        value = self._propagation.get_confidence(entity_id)
        record = self._propagation.get_record(entity_id)
        
        return {
            "entity_id": entity_id,
            "confidence": value,
            "record": record.to_dict() if record else None,
        }
    
    def get_chain(self, entity_id: str) -> dict[str, Any] | None:
        """Get confidence chain for an entity."""
        chain = self._propagation.get_chain(entity_id)
        if chain:
            return chain.to_dict()
        return None
