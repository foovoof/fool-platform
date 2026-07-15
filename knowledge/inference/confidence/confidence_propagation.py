"""
knowledge/inference/confidence/confidence_propagation.py

Confidence Propagation for Inference Engine.

Propagates confidence values through the knowledge graph.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, Node
from knowledge.inference.confidence.confidence_model import (
    ConfidenceRecord,
    ConfidenceUpdate,
    ConfidenceChain,
)
from knowledge.inference.confidence.confidence_calculator import ConfidenceCalculator


@dataclass
class PropagationResult:
    """Result of confidence propagation."""
    updated_entities: list[str] = field(default_factory=list)
    updates: list[ConfidenceUpdate] = field(default_factory=list)
    chains: list[ConfidenceChain] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class ConfidencePropagation:
    """
    Propagates confidence values through the knowledge graph.
    
    Propagation is deterministic and explainable.
    """
    
    def __init__(
        self,
        calculator: ConfidenceCalculator | None = None,
    ) -> None:
        """
        Initialize confidence propagation.
        
        Args:
            calculator: Optional confidence calculator
        """
        self._calculator = calculator or ConfidenceCalculator()
        self._confidence_records: dict[str, ConfidenceRecord] = {}
        self._confidence_chains: dict[str, ConfidenceChain] = {}
    
    def propagate_confidence(
        self,
        source_entity_id: str,
        graph: Graph,
        decay_factor: float = 0.9,
        max_depth: int = 3,
        initial_confidence: float = 1.0,
    ) -> PropagationResult:
        """
        Propagate confidence from a source entity.
        
        Args:
            source_entity_id: Source entity ID
            graph: The knowledge graph
            decay_factor: Confidence decay per hop
            max_depth: Maximum propagation depth
            initial_confidence: Initial confidence value
            
        Returns:
            Propagation result
        """
        result = PropagationResult()
        
        source_node = graph.get_node(source_entity_id)
        if not source_node:
            return result
        
        visited: set[str] = set()
        queue: list[tuple[str, float, int]] = [
            (source_entity_id, initial_confidence, 0)
        ]
        
        while queue:
            current_id, current_confidence, depth = queue.pop(0)
            
            if current_id in visited or depth > max_depth:
                continue
            
            visited.add(current_id)
            
            if current_id != source_entity_id:
                update = ConfidenceUpdate(
                    entity_id=current_id,
                    old_value=0.0,
                    new_value=current_confidence,
                    source_rule="propagation",
                    evidence_ids=[source_entity_id],
                    update_reason=f"Propagated from {source_entity_id}",
                )
                result.updates.append(update)
                result.updated_entities.append(current_id)
                
                self._update_chain(current_id, update)
            
            decayed_confidence = current_confidence * decay_factor
            
            if decayed_confidence < 0.1:
                continue
            
            edges = [e for e in graph.list_edges() if e.source_node_id == current_id]
            
            for edge in edges:
                neighbor_id = edge.target_node_id
                
                if neighbor_id not in visited:
                    queue.append((neighbor_id, decayed_confidence, depth + 1))
        
        return result
    
    def update_confidence_chain(
        self,
        entity_id: str,
        new_confidence: float,
        source_rule: str,
        evidence_ids: list[str],
        reason: str,
    ) -> ConfidenceUpdate:
        """
        Update confidence for an entity.
        
        Args:
            entity_id: Entity ID
            new_confidence: New confidence value
            source_rule: Source rule
            evidence_ids: Evidence IDs
            reason: Update reason
            
        Returns:
            Confidence update
        """
        old_record = self._confidence_records.get(entity_id)
        old_value = old_record.value if old_record else 0.0
        
        update = ConfidenceUpdate(
            entity_id=entity_id,
            old_value=old_value,
            new_value=new_confidence,
            source_rule=source_rule,
            evidence_ids=evidence_ids,
            update_reason=reason,
        )
        
        record = self._calculator.create_record(
            entity_id=entity_id,
            entity_type="inferred",
            value=new_confidence,
            source_rule=source_rule,
            evidence_ids=evidence_ids,
            rationale=reason,
        )
        self._confidence_records[entity_id] = record
        
        self._update_chain(entity_id, update)
        
        return update
    
    def get_confidence(self, entity_id: str) -> float:
        """
        Get confidence for an entity.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            Confidence value or 0.0
        """
        record = self._confidence_records.get(entity_id)
        return record.value if record else 0.0
    
    def get_record(self, entity_id: str) -> ConfidenceRecord | None:
        """
        Get confidence record for an entity.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            Confidence record or None
        """
        return self._confidence_records.get(entity_id)
    
    def get_chain(self, entity_id: str) -> ConfidenceChain | None:
        """
        Get confidence chain for an entity.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            Confidence chain or None
        """
        return self._confidence_chains.get(entity_id)
    
    def _update_chain(
        self,
        entity_id: str,
        update: ConfidenceUpdate,
    ) -> None:
        """Update the confidence chain for an entity."""
        if entity_id not in self._confidence_chains:
            self._confidence_chains[entity_id] = ConfidenceChain(
                entity_id=entity_id,
            )
        
        self._confidence_chains[entity_id].add_update(update)
    
    def merge_confidence_updates(
        self,
        updates: list[ConfidenceUpdate],
        method: str = "average",
    ) -> float:
        """
        Merge multiple confidence updates.
        
        Args:
            updates: List of updates
            method: Merge method
            
        Returns:
            Merged confidence value
        """
        values = [u.new_value for u in updates]
        return self._calculator.merge_confidences(values, method)
    
    def explain_propagation(
        self,
        result: PropagationResult,
    ) -> str:
        """
        Generate explanation for propagation.
        
        Args:
            result: Propagation result
            
        Returns:
            Text explanation
        """
        parts = [
            f"Confidence propagation completed:",
            f"- {len(result.updated_entities)} entity(ies) updated",
            f"- {len(result.updates)} confidence update(s)",
            f"- {len(result.chains)} confidence chain(s) maintained",
        ]
        
        if result.updates:
            avg_change = sum(u.change for u in result.updates) / len(result.updates)
            parts.append(f"- Average change: {avg_change:+.2f}")
        
        return "\n".join(parts)
