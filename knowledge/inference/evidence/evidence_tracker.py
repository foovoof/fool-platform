"""
knowledge/inference/evidence/evidence_tracker.py

Evidence Tracker for Inference Engine.

Tracks evidence usage during inference.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class EvidenceType(Enum):
    """Types of evidence."""
    NODE = "node"
    EDGE = "edge"
    IDENTITY = "identity"
    ATTRIBUTE = "attribute"
    RELATIONSHIP = "relationship"
    DERIVED = "derived"
    EXTERNAL = "external"


@dataclass
class Evidence:
    """
    Represents a piece of evidence used in inference.
    
    Evidence is the basis for all conclusions.
    """
    evidence_id: str = field(default_factory=lambda: str(uuid4()))
    evidence_type: EvidenceType = EvidenceType.NODE
    source_id: str = ""
    source_type: str = ""
    value: Any = None
    confidence: float = 1.0
    used_by_conclusions: list[str] = field(default_factory=list)
    used_by_rules: list[str] = field(default_factory=list)
    derived_from: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert evidence to dictionary."""
        return {
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type.value,
            "source_id": self.source_id,
            "source_type": self.source_type,
            "value": self.value,
            "confidence": self.confidence,
            "used_by_conclusions": self.used_by_conclusions,
            "used_by_rules": self.used_by_rules,
            "derived_from": self.derived_from,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Evidence:
        """Create evidence from dictionary."""
        if isinstance(data.get("evidence_type"), str):
            data["evidence_type"] = EvidenceType(data["evidence_type"])
        return cls(**data)


class EvidenceTracker:
    """
    Tracks evidence usage during inference.
    
    Maintains a registry of all evidence and tracks
    which conclusions and rules use which evidence.
    """
    
    def __init__(self) -> None:
        """Initialize the evidence tracker."""
        self._evidence: dict[str, Evidence] = {}
        self._usage_by_conclusion: dict[str, list[str]] = {}
        self._usage_by_rule: dict[str, list[str]] = {}
    
    def register_evidence(self, evidence: Evidence) -> str:
        """
        Register a new piece of evidence.
        
        Args:
            evidence: The evidence to register
            
        Returns:
            The evidence ID
        """
        self._evidence[evidence.evidence_id] = evidence
        return evidence.evidence_id
    
    def register_node_evidence(
        self,
        node_id: str,
        node_type: str,
        value: dict[str, Any],
        confidence: float = 1.0,
    ) -> str:
        """
        Register evidence from a node.
        
        Args:
            node_id: The node ID
            node_type: The node type
            value: Node attributes
            confidence: Evidence confidence
            
        Returns:
            The evidence ID
        """
        evidence = Evidence(
            evidence_type=EvidenceType.NODE,
            source_id=node_id,
            source_type=node_type,
            value=value,
            confidence=confidence,
        )
        return self.register_evidence(evidence)
    
    def register_edge_evidence(
        self,
        edge_id: str,
        source_id: str,
        target_id: str,
        relationship_type: str,
        confidence: float = 1.0,
    ) -> str:
        """
        Register evidence from an edge.
        
        Args:
            edge_id: The edge ID
            source_id: Source node ID
            target_id: Target node ID
            relationship_type: Relationship type
            confidence: Evidence confidence
            
        Returns:
            The evidence ID
        """
        evidence = Evidence(
            evidence_type=EvidenceType.EDGE,
            source_id=edge_id,
            source_type=relationship_type,
            value={
                "source_id": source_id,
                "target_id": target_id,
                "relationship_type": relationship_type,
            },
            confidence=confidence,
        )
        return self.register_evidence(evidence)
    
    def track_usage(
        self,
        evidence_id: str,
        conclusion_id: str | None = None,
        rule_id: str | None = None,
    ) -> bool:
        """
        Track usage of evidence.
        
        Args:
            evidence_id: The evidence ID
            conclusion_id: Optional conclusion using the evidence
            rule_id: Optional rule using the evidence
            
        Returns:
            True if tracked successfully
        """
        if evidence_id not in self._evidence:
            return False
        
        evidence = self._evidence[evidence_id]
        
        if conclusion_id:
            if conclusion_id not in evidence.used_by_conclusions:
                evidence.used_by_conclusions.append(conclusion_id)
            if conclusion_id not in self._usage_by_conclusion:
                self._usage_by_conclusion[conclusion_id] = []
            if evidence_id not in self._usage_by_conclusion[conclusion_id]:
                self._usage_by_conclusion[conclusion_id].append(evidence_id)
        
        if rule_id:
            if rule_id not in evidence.used_by_rules:
                evidence.used_by_rules.append(rule_id)
            if rule_id not in self._usage_by_rule:
                self._usage_by_rule[rule_id] = []
            if evidence_id not in self._usage_by_rule[rule_id]:
                self._usage_by_rule[rule_id].append(evidence_id)
        
        return True
    
    def track_conclusion(
        self,
        conclusion_id: str,
        evidence_ids: list[str],
        rule_id: str,
    ) -> None:
        """
        Track a conclusion with its evidence.
        
        Args:
            conclusion_id: The conclusion ID
            evidence_ids: Evidence IDs used
            rule_id: The rule that generated the conclusion
        """
        for evidence_id in evidence_ids:
            self.track_usage(
                evidence_id,
                conclusion_id=conclusion_id,
                rule_id=rule_id,
            )
    
    def get_evidence(self, evidence_id: str) -> Evidence | None:
        """
        Get evidence by ID.
        
        Args:
            evidence_id: The evidence ID
            
        Returns:
            The evidence or None
        """
        return self._evidence.get(evidence_id)
    
    def get_evidence_for_conclusion(
        self,
        conclusion_id: str,
    ) -> list[Evidence]:
        """
        Get evidence used by a conclusion.
        
        Args:
            conclusion_id: The conclusion ID
            
        Returns:
            List of evidence
        """
        evidence_ids = self._usage_by_conclusion.get(conclusion_id, [])
        return [
            self._evidence[eid]
            for eid in evidence_ids
            if eid in self._evidence
        ]
    
    def get_evidence_for_rule(self, rule_id: str) -> list[Evidence]:
        """
        Get evidence used by a rule.
        
        Args:
            rule_id: The rule ID
            
        Returns:
            List of evidence
        """
        evidence_ids = self._usage_by_rule.get(rule_id, [])
        return [
            self._evidence[eid]
            for eid in evidence_ids
            if eid in self._evidence
        ]
    
    def list_evidence(
        self,
        evidence_type: EvidenceType | None = None,
    ) -> list[Evidence]:
        """
        List all evidence.
        
        Args:
            evidence_type: Optional filter by type
            
        Returns:
            List of evidence
        """
        evidence_list = list(self._evidence.values())
        if evidence_type:
            evidence_list = [
                e for e in evidence_list
                if e.evidence_type == evidence_type
            ]
        return evidence_list
    
    def count(self) -> int:
        """Get the number of registered evidence."""
        return len(self._evidence)
