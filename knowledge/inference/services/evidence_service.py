from __future__ import annotations

"""
knowledge/inference/services/evidence_service.py

Evidence Service for the Knowledge Layer.

Orchestrates evidence operations.
"""
from typing import Any

from knowledge.graph.models import Graph
from knowledge.inference.evidence.evidence_tracker import EvidenceTracker, Evidence, EvidenceType
from knowledge.inference.evidence.evidence_chain import EvidenceChainBuilder
from knowledge.inference.evidence.evidence_propagation import EvidencePropagation


class EvidenceService:
    """
    Service for evidence management.
    
    Orchestrates:
    - Evidence registration
    - Evidence tracking
    - Evidence chain building
    - Evidence propagation
    """
    
    def __init__(
        self,
        evidence_tracker: EvidenceTracker | None = None,
    ) -> None:
        """
        Initialize the service.
        
        Args:
            evidence_tracker: Optional evidence tracker
        """
        self._tracker = evidence_tracker or EvidenceTracker()
        self._chain_builder = EvidenceChainBuilder()
        self._propagation = EvidencePropagation(self._tracker)
    
    def register_evidence(
        self,
        evidence_type: str,
        source_id: str,
        value: Any,
        confidence: float = 1.0,
    ) -> dict[str, Any]:
        """
        Register new evidence.
        
        Args:
            evidence_type: Type of evidence
            source_id: Source ID
            value: Evidence value
            confidence: Confidence value
            
        Returns:
            Registration result
        """
        evidence = Evidence(
            evidence_type=EvidenceType(evidence_type),
            source_id=source_id,
            value=value,
            confidence=confidence,
        )
        
        evidence_id = self._tracker.register_evidence(evidence)
        
        return {
            "success": True,
            "evidence_id": evidence_id,
        }
    
    def track_usage(
        self,
        evidence_id: str,
        conclusion_id: str | None = None,
        rule_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Track evidence usage.
        
        Args:
            evidence_id: Evidence ID
            conclusion_id: Optional conclusion ID
            rule_id: Optional rule ID
            
        Returns:
            Tracking result
        """
        success = self._tracker.track_usage(
            evidence_id,
            conclusion_id,
            rule_id,
        )
        
        return {
            "success": success,
            "evidence_id": evidence_id,
        }
    
    def build_chain(
        self,
        conclusion_id: str,
        evidence_ids: list[str],
        rule_id: str,
    ) -> dict[str, Any]:
        """
        Build an evidence chain.
        
        Args:
            conclusion_id: Conclusion ID
            evidence_ids: Evidence IDs
            rule_id: Rule ID
            
        Returns:
            Chain data
        """
        chain = self._chain_builder.build_chain(
            conclusion_id,
            evidence_ids,
            rule_id,
        )
        
        return {
            "success": True,
            "chain": chain.to_dict(),
        }
    
    def propagate(
        self,
        evidence_id: str,
        graph: Graph,
        mode: str = "neighbors",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Propagate evidence.
        
        Args:
            evidence_id: Evidence ID
            graph: Knowledge graph
            mode: Propagation mode
            **kwargs: Additional parameters
            
        Returns:
            Propagation result
        """
        if mode == "neighbors":
            result = self._propagation.propagate_to_neighbors(
                evidence_id,
                graph,
                kwargs.get("max_depth", 1),
            )
        elif mode == "relationships":
            result = self._propagation.propagate_through_relationships(
                evidence_id,
                graph,
                kwargs.get("relationship_types"),
            )
        elif mode == "confidence":
            result = self._propagation.propagate_confidence(
                evidence_id,
                graph,
                kwargs.get("decay_factor", 0.9),
                kwargs.get("max_depth", 3),
            )
        else:
            return {
                "success": False,
                "error": f"Unknown propagation mode: {mode}",
            }
        
        return {
            "success": True,
            "propagated_evidence": result.propagated_evidence,
            "affected_nodes": result.affected_nodes,
            "affected_edges": result.affected_edges,
        }
    
    def get_evidence(self, evidence_id: str) -> dict[str, Any] | None:
        """Get evidence by ID."""
        evidence = self._tracker.get_evidence(evidence_id)
        if evidence:
            return evidence.to_dict()
        return None
    
    def list_evidence(
        self,
        evidence_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """List all evidence."""
        et = EvidenceType(evidence_type) if evidence_type else None
        evidence_list = self._tracker.list_evidence(et)
        return [e.to_dict() for e in evidence_list]
