"""
knowledge/inference/evidence/evidence_propagation.py

Evidence Propagation for Inference Engine.

Propagates evidence through the knowledge graph.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, Node, Edge
from knowledge.inference.evidence.evidence_tracker import EvidenceTracker, EvidenceType
from knowledge.inference.evidence.evidence_chain import EvidenceChain, EvidenceChainBuilder


@dataclass
class PropagationResult:
    """Result of evidence propagation."""
    propagated_evidence: list[str] = field(default_factory=list)
    affected_nodes: list[str] = field(default_factory=list)
    affected_edges: list[str] = field(default_factory=list)
    chains: list[EvidenceChain] = field(default_factory=list)


class EvidencePropagation:
    """
    Propagates evidence through the knowledge graph.
    
    Evidence can be propagated to:
    - Related nodes
    - Connected edges
    - Subgraphs
    """
    
    def __init__(
        self,
        evidence_tracker: EvidenceTracker | None = None,
        chain_builder: EvidenceChainBuilder | None = None,
    ) -> None:
        """
        Initialize evidence propagation.
        
        Args:
            evidence_tracker: Optional evidence tracker
            chain_builder: Optional chain builder
        """
        self._evidence_tracker = evidence_tracker or EvidenceTracker()
        self._chain_builder = chain_builder or EvidenceChainBuilder()
    
    def propagate_to_neighbors(
        self,
        evidence_id: str,
        graph: Graph,
        max_depth: int = 1,
    ) -> PropagationResult:
        """
        Propagate evidence to neighboring nodes.
        
        Args:
            evidence_id: The evidence ID
            graph: The knowledge graph
            max_depth: Maximum propagation depth
            
        Returns:
            Propagation result
        """
        result = PropagationResult()
        
        evidence = self._evidence_tracker.get_evidence(evidence_id)
        if not evidence:
            return result
        
        visited: set[str] = set()
        queue: list[tuple[str, int]] = [(evidence.source_id, 0)]
        
        while queue:
            current_id, depth = queue.pop(0)
            
            if current_id in visited or depth > max_depth:
                continue
            
            visited.add(current_id)
            result.affected_nodes.append(current_id)
            
            edges = [
                e for e in graph.list_edges()
                if e.source_node_id == current_id or e.target_node_id == current_id
            ]
            
            for edge in edges:
                if edge.edge_id not in result.affected_edges:
                    result.affected_edges.append(edge.edge_id)
                
                neighbor_id = (
                    edge.target_node_id
                    if edge.source_node_id == current_id
                    else edge.source_node_id
                )
                
                if neighbor_id not in visited:
                    queue.append((neighbor_id, depth + 1))
                    
                    self._evidence_tracker.register_node_evidence(
                        neighbor_id,
                        "inferred",
                        {"derived_from": evidence_id},
                        confidence=evidence.confidence * 0.9,
                    )
                    result.propagated_evidence.append(neighbor_id)
        
        return result
    
    def propagate_through_relationships(
        self,
        evidence_id: str,
        graph: Graph,
        relationship_types: list[str] | None = None,
    ) -> PropagationResult:
        """
        Propagate evidence through specific relationship types.
        
        Args:
            evidence_id: The evidence ID
            graph: The knowledge graph
            relationship_types: Optional relationship type filter
            
        Returns:
            Propagation result
        """
        result = PropagationResult()
        
        evidence = self._evidence_tracker.get_evidence(evidence_id)
        if not evidence:
            return result
        
        from knowledge.graph.models import RelationshipType
        
        edges = [
            e for e in graph.list_edges()
            if e.source_node_id == evidence.source_id
            or e.target_node_id == evidence.source_id
        ]
        
        for edge in edges:
            if relationship_types:
                if edge.relationship_type.value not in relationship_types:
                    continue
            
            if edge.edge_id not in result.affected_edges:
                result.affected_edges.append(edge.edge_id)
            
            neighbor_id = (
                edge.target_node_id
                if edge.source_node_id == evidence.source_id
                else edge.source_node_id
            )
            
            if neighbor_id not in result.affected_nodes:
                result.affected_nodes.append(neighbor_id)
                
                self._evidence_tracker.register_edge_evidence(
                    edge.edge_id,
                    evidence.source_id,
                    neighbor_id,
                    edge.relationship_type.value,
                    evidence.confidence * 0.95,
                )
                result.propagated_evidence.append(neighbor_id)
        
        return result
    
    def propagate_confidence(
        self,
        evidence_id: str,
        graph: Graph,
        decay_factor: float = 0.9,
        max_depth: int = 3,
    ) -> PropagationResult:
        """
        Propagate evidence with confidence decay.
        
        Args:
            evidence_id: The evidence ID
            graph: The knowledge graph
            decay_factor: Confidence decay per hop
            max_depth: Maximum propagation depth
            
        Returns:
            Propagation result
        """
        result = PropagationResult()
        
        evidence = self._evidence_tracker.get_evidence(evidence_id)
        if not evidence:
            return result
        
        visited: set[str] = set()
        queue: list[tuple[str, float, int]] = [
            (evidence.source_id, evidence.confidence, 0)
        ]
        
        while queue:
            current_id, current_confidence, depth = queue.pop(0)
            
            if current_id in visited or depth > max_depth:
                continue
            
            visited.add(current_id)
            result.affected_nodes.append(current_id)
            
            decayed_confidence = current_confidence * decay_factor
            
            if decayed_confidence < 0.1:
                continue
            
            edges = [
                e for e in graph.list_edges()
                if e.source_node_id == current_id
            ]
            
            for edge in edges:
                if edge.edge_id not in result.affected_edges:
                    result.affected_edges.append(edge.edge_id)
                
                neighbor_id = edge.target_node_id
                
                if neighbor_id not in visited:
                    queue.append((
                        neighbor_id,
                        decayed_confidence,
                        depth + 1,
                    ))
                    
                    self._evidence_tracker.register_node_evidence(
                        neighbor_id,
                        "propagated",
                        {
                            "derived_from": evidence_id,
                            "propagation_depth": depth + 1,
                            "confidence": decayed_confidence,
                        },
                        decayed_confidence,
                    )
                    result.propagated_evidence.append(neighbor_id)
        
        return result
    
    def build_chain_for_conclusion(
        self,
        conclusion_id: str,
        evidence_ids: list[str],
        rule_id: str,
        intermediate_conclusions: list[str] | None = None,
    ) -> EvidenceChain:
        """
        Build an evidence chain for a conclusion.
        
        Args:
            conclusion_id: The conclusion ID
            evidence_ids: Evidence IDs
            rule_id: The rule ID
            intermediate_conclusions: Optional intermediate conclusions
            
        Returns:
            The evidence chain
        """
        return self._chain_builder.build_chain(
            conclusion_id,
            evidence_ids,
            rule_id,
            intermediate_conclusions,
        )
    
    def explain_propagation(
        self,
        evidence_id: str,
        result: PropagationResult,
    ) -> str:
        """
        Generate explanation for propagation.
        
        Args:
            evidence_id: The evidence ID
            result: The propagation result
            
        Returns:
            Text explanation
        """
        evidence = self._evidence_tracker.get_evidence(evidence_id)
        if not evidence:
            return "Evidence not found"
        
        parts = [
            f"Evidence '{evidence_id}' was propagated to:",
            f"- {len(result.affected_nodes)} node(s)",
            f"- {len(result.affected_edges)} edge(s)",
            f"- {len(result.propagated_evidence)} new evidence record(s)",
        ]
        
        if result.chains:
            parts.append(
                f"- {len(result.chains)} evidence chain(s) built"
            )
        
        return "\n".join(parts)
