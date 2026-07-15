"""
knowledge/inference/evidence/evidence_chain.py

Evidence Chain for Inference Engine.

Builds chains of evidence for conclusions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from knowledge.inference.evidence.evidence_tracker import Evidence


class ChainNodeType(Enum):
    """Types of nodes in an evidence chain."""
    EVIDENCE = "evidence"
    RULE = "rule"
    CONCLUSION = "conclusion"
    DERIVED_EVIDENCE = "derived_evidence"


@dataclass
class ChainNode:
    """A node in an evidence chain."""
    node_id: str
    node_type: ChainNodeType
    label: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChainEdge:
    """An edge in an evidence chain."""
    source_id: str
    target_id: str
    edge_type: str = "supports"
    rule_id: str | None = None


@dataclass
class EvidenceChain:
    """
    Represents a chain of evidence leading to a conclusion.
    
    Chains are directed graphs showing how evidence flows
    through rules to conclusions.
    """
    chain_id: str = field(default_factory=lambda: str(uuid4()))
    conclusion_id: str = ""
    evidence_ids: list[str] = field(default_factory=list)
    rule_ids: list[str] = field(default_factory=list)
    conclusion_ids: list[str] = field(default_factory=list)
    nodes: list[ChainNode] = field(default_factory=list)
    edges: list[ChainEdge] = field(default_factory=list)
    path: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def add_node(self, node: ChainNode) -> None:
        """Add a node to the chain."""
        if node.node_id not in [n.node_id for n in self.nodes]:
            self.nodes.append(node)
    
    def add_edge(self, edge: ChainEdge) -> None:
        """Add an edge to the chain."""
        self.edges.append(edge)
    
    def add_evidence(self, evidence_id: str) -> None:
        """Add evidence to the chain."""
        if evidence_id not in self.evidence_ids:
            self.evidence_ids.append(evidence_id)
    
    def add_rule(self, rule_id: str) -> None:
        """Add a rule to the chain."""
        if rule_id not in self.rule_ids:
            self.rule_ids.append(rule_id)
    
    def add_conclusion(self, conclusion_id: str) -> None:
        """Add a conclusion to the chain."""
        if conclusion_id not in self.conclusion_ids:
            self.conclusion_ids.append(conclusion_id)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert chain to dictionary."""
        return {
            "chain_id": self.chain_id,
            "conclusion_id": self.conclusion_id,
            "evidence_ids": self.evidence_ids,
            "rule_ids": self.rule_ids,
            "conclusion_ids": self.conclusion_ids,
            "nodes": [
                {
                    "node_id": n.node_id,
                    "node_type": n.node_type.value,
                    "label": n.label,
                    "metadata": n.metadata,
                }
                for n in self.nodes
            ],
            "edges": [
                {
                    "source_id": e.source_id,
                    "target_id": e.target_id,
                    "edge_type": e.edge_type,
                    "rule_id": e.rule_id,
                }
                for e in self.edges
            ],
            "path": self.path,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EvidenceChain:
        """Create chain from dictionary."""
        chain = cls(
            chain_id=data.get("chain_id", str(uuid4())),
            conclusion_id=data.get("conclusion_id", ""),
            evidence_ids=data.get("evidence_ids", []),
            rule_ids=data.get("rule_ids", []),
            conclusion_ids=data.get("conclusion_ids", []),
            path=data.get("path", []),
            metadata=data.get("metadata", {}),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
        )
        
        for node_data in data.get("nodes", []):
            chain.nodes.append(ChainNode(
                node_id=node_data["node_id"],
                node_type=ChainNodeType(node_data["node_type"]),
                label=node_data["label"],
                metadata=node_data.get("metadata", {}),
            ))
        
        for edge_data in data.get("edges", []):
            chain.edges.append(ChainEdge(
                source_id=edge_data["source_id"],
                target_id=edge_data["target_id"],
                edge_type=edge_data.get("edge_type", "supports"),
                rule_id=edge_data.get("rule_id"),
            ))
        
        return chain


class EvidenceChainBuilder:
    """
    Builds evidence chains from inference results.
    
    Constructs explainable chains showing how conclusions
    are derived from evidence through rules.
    """
    
    def __init__(self, evidence_tracker: Any = None) -> None:
        """
        Initialize the chain builder.
        
        Args:
            evidence_tracker: Optional evidence tracker
        """
        self._evidence_tracker = evidence_tracker
    
    def build_chain(
        self,
        conclusion_id: str,
        evidence_ids: list[str],
        rule_id: str,
        intermediate_conclusions: list[str] | None = None,
    ) -> EvidenceChain:
        """
        Build an evidence chain.
        
        Args:
            conclusion_id: The conclusion ID
            evidence_ids: Evidence IDs
            rule_id: The rule ID
            intermediate_conclusions: Optional intermediate conclusions
            
        Returns:
            The built evidence chain
        """
        chain = EvidenceChain(conclusion_id=conclusion_id)
        
        for evidence_id in evidence_ids:
            chain.add_evidence(evidence_id)
            
            evidence_node = ChainNode(
                node_id=evidence_id,
                node_type=ChainNodeType.EVIDENCE,
                label=f"Evidence: {evidence_id[:8]}",
            )
            chain.add_node(evidence_node)
        
        chain.add_rule(rule_id)
        
        rule_node = ChainNode(
            node_id=rule_id,
            node_type=ChainNodeType.RULE,
            label=f"Rule: {rule_id[:8]}",
        )
        chain.add_node(rule_node)
        
        chain.add_conclusion(conclusion_id)
        
        conclusion_node = ChainNode(
            node_id=conclusion_id,
            node_type=ChainNodeType.CONCLUSION,
            label=f"Conclusion: {conclusion_id[:8]}",
        )
        chain.add_node(conclusion_node)
        
        for evidence_id in evidence_ids:
            chain.add_edge(ChainEdge(
                source_id=evidence_id,
                target_id=rule_id,
                edge_type="supports",
            ))
        
        chain.add_edge(ChainEdge(
            source_id=rule_id,
            target_id=conclusion_id,
            edge_type="derives",
            rule_id=rule_id,
        ))
        
        if intermediate_conclusions:
            for i, inter_id in enumerate(intermediate_conclusions):
                chain.add_conclusion(inter_id)
                
                inter_node = ChainNode(
                    node_id=inter_id,
                    node_type=ChainNodeType.DERIVED_EVIDENCE,
                    label=f"Derived: {inter_id[:8]}",
                )
                chain.add_node(inter_node)
                
                chain.add_edge(ChainEdge(
                    source_id=rule_id,
                    target_id=inter_id,
                    edge_type="produces",
                    rule_id=rule_id,
                ))
                
                chain.add_edge(ChainEdge(
                    source_id=inter_id,
                    target_id=conclusion_id,
                    edge_type="supports",
                ))
        
        chain.path = self._build_path(chain)
        
        return chain
    
    def _build_path(self, chain: EvidenceChain) -> list[str]:
        """Build the path through the chain."""
        if not chain.nodes:
            return []
        
        evidence_nodes = [
            n.node_id for n in chain.nodes
            if n.node_type == ChainNodeType.EVIDENCE
        ]
        
        rule_nodes = [
            n.node_id for n in chain.nodes
            if n.node_type == ChainNodeType.RULE
        ]
        
        conclusion_nodes = [
            n.node_id for n in chain.nodes
            if n.node_type == ChainNodeType.CONCLUSION
        ]
        
        path: list[str] = []
        
        for e in evidence_nodes:
            path.append(e)
        
        if rule_nodes:
            path.extend(rule_nodes)
        
        for c in conclusion_nodes:
            path.append(c)
        
        return path
    
    def explain_chain(self, chain: EvidenceChain) -> str:
        """
        Generate a text explanation of the chain.
        
        Args:
            chain: The evidence chain
            
        Returns:
            Text explanation
        """
        parts: list[str] = []
        
        evidence_count = len(chain.evidence_ids)
        rule_count = len(chain.rule_ids)
        
        parts.append(
            f"This conclusion is supported by {evidence_count} piece(s) of evidence "
            f"through {rule_count} rule(s)."
        )
        
        if chain.path:
            parts.append("Evidence flow: " + " → ".join(chain.path[:5]))
            if len(chain.path) > 5:
                parts.append(f"... and {len(chain.path) - 5} more steps")
        
        return " ".join(parts)
