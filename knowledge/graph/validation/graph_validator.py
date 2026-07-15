from __future__ import annotations

"""
knowledge/graph/validation/graph_validator.py

Graph validator for the Knowledge Layer.

Validates graph structure and integrity.
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, Node, Edge


@dataclass
class GraphValidationResult:
    """Result of graph validation."""
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    orphan_nodes: list[str] = field(default_factory=list)
    orphan_edges: list[str] = field(default_factory=list)
    dangling_edges: list[str] = field(default_factory=list)
    self_loops: list[str] = field(default_factory=list)
    duplicate_nodes: list[tuple[str, str]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def success(cls) -> "GraphValidationResult":
        """Create a successful validation result."""
        return cls(is_valid=True)

    @classmethod
    def failure(cls, errors: list[str]) -> "GraphValidationResult":
        """Create a failed validation result."""
        return cls(is_valid=False, errors=errors)


class GraphValidator:
    """
    Validates graph structure and integrity.
    
    Checks for:
    - Orphan nodes
    - Orphan edges
    - Dangling edges
    - Self-loops
    - Duplicate nodes
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize graph validator.
        
        Args:
            graph: The graph to validate
        """
        self._graph = graph

    def validate(self) -> GraphValidationResult:
        """
        Perform full graph validation.
        
        Returns:
            GraphValidationResult with all issues found
        """
        result = GraphValidationResult(is_valid=True)
        
        self._check_orphan_edges(result)
        self._check_dangling_edges(result)
        self._check_self_loops(result)
        self._check_node_consistency(result)
        
        result.is_valid = len(result.errors) == 0
        
        return result

    def _check_orphan_edges(self, result: GraphValidationResult) -> None:
        """Check for orphan edges (edges without connected nodes)."""
        node_ids = {node.node_id for node in self._graph.list_nodes()}
        
        for edge in self._graph.list_edges():
            if edge.source_node_id not in node_ids:
                result.orphan_edges.append(edge.edge_id)
                result.errors.append(
                    f"Edge {edge.edge_id} has orphan source node {edge.source_node_id}"
                )
            
            if edge.target_node_id not in node_ids:
                result.orphan_edges.append(edge.edge_id)
                result.errors.append(
                    f"Edge {edge.edge_id} has orphan target node {edge.target_node_id}"
                )

    def _check_dangling_edges(self, result: GraphValidationResult) -> None:
        """Check for dangling edges (edges referencing non-existent nodes)."""
        node_ids = {node.node_id for node in self._graph.list_nodes()}
        
        for edge in self._graph.list_edges():
            if edge.source_node_id not in node_ids or edge.target_node_id not in node_ids:
                result.dangling_edges.append(edge.edge_id)

    def _check_self_loops(self, result: GraphValidationResult) -> None:
        """Check for self-loop edges."""
        for edge in self._graph.list_edges():
            if edge.is_self_loop():
                result.self_loops.append(edge.edge_id)
                result.warnings.append(f"Edge {edge.edge_id} is a self-loop")

    def _check_node_consistency(self, result: GraphValidationResult) -> None:
        """Check for node consistency issues."""
        all_nodes = self._graph.list_nodes()
        
        node_ids = [node.node_id for node in all_nodes]
        seen_ids: set[str] = set()
        
        for node_id in node_ids:
            if node_id in seen_ids:
                result.duplicate_nodes.append((node_id, node_id))
                result.errors.append(f"Duplicate node ID: {node_id}")
            seen_ids.add(node_id)

    def validate_node_reference(self, node_id: str) -> bool:
        """
        Validate that a node reference exists.
        
        Args:
            node_id: The node ID to validate
            
        Returns:
            True if node exists
        """
        return self._graph.get_node(node_id) is not None

    def validate_edge_reference(self, edge_id: str) -> bool:
        """
        Validate that an edge reference exists.
        
        Args:
            edge_id: The edge ID to validate
            
        Returns:
            True if edge exists
        """
        return self._graph.get_edge(edge_id) is not None
