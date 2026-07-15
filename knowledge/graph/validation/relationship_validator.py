from __future__ import annotations

"""
knowledge/graph/validation/relationship_validator.py

Relationship validator for the Knowledge Layer.

Validates relationship (edge) structure and integrity.
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, Edge, RelationshipType


@dataclass
class RelationshipValidationResult:
    """Result of relationship validation."""
    is_valid: bool
    edge_id: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def success(cls, edge_id: str) -> "RelationshipValidationResult":
        """Create a successful validation result."""
        return cls(is_valid=True, edge_id=edge_id)

    @classmethod
    def failure(
        cls,
        edge_id: str,
        errors: list[str],
    ) -> "RelationshipValidationResult":
        """Create a failed validation result."""
        return cls(is_valid=False, edge_id=edge_id, errors=errors)


class RelationshipValidator:
    """
    Validates relationship (edge) structure and integrity.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize relationship validator.
        
        Args:
            graph: The graph containing the relationships
        """
        self._graph = graph

    def validate(self, edge_id: str) -> RelationshipValidationResult:
        """
        Validate a relationship.
        
        Args:
            edge_id: The edge ID to validate
            
        Returns:
            RelationshipValidationResult
        """
        edge = self._graph.get_edge(edge_id)
        if not edge:
            return RelationshipValidationResult.failure(
                edge_id,
                [f"Edge {edge_id} not found in graph"],
            )

        result = RelationshipValidationResult.success(edge_id)
        
        self._validate_edge_id(edge, result)
        self._validate_edge_references(edge, result)
        self._validate_relationship_type(edge, result)
        self._validate_confidence(edge, result)
        
        return result

    def _validate_edge_id(self, edge: Edge, result: RelationshipValidationResult) -> None:
        """Validate edge ID."""
        if not edge.edge_id:
            result.errors.append("Edge has no edge_id")
            result.is_valid = False

    def _validate_edge_references(
        self,
        edge: Edge,
        result: RelationshipValidationResult,
    ) -> None:
        """Validate edge source and target references."""
        if not edge.source_node_id:
            result.errors.append("Edge has no source_node_id")
            result.is_valid = False
        elif not self._graph.get_node(edge.source_node_id):
            result.errors.append(f"Source node {edge.source_node_id} not found")
            result.is_valid = False

        if not edge.target_node_id:
            result.errors.append("Edge has no target_node_id")
            result.is_valid = False
        elif not self._graph.get_node(edge.target_node_id):
            result.errors.append(f"Target node {edge.target_node_id} not found")
            result.is_valid = False

    def _validate_relationship_type(
        self,
        edge: Edge,
        result: RelationshipValidationResult,
    ) -> None:
        """Validate relationship type."""
        if edge.relationship_type == RelationshipType.UNKNOWN:
            result.warnings.append("Relationship type is UNKNOWN")

    def _validate_confidence(
        self,
        edge: Edge,
        result: RelationshipValidationResult,
    ) -> None:
        """Validate confidence value."""
        if not (0.0 <= edge.confidence <= 1.0):
            result.errors.append(
                f"Confidence value {edge.confidence} out of range [0.0, 1.0]"
            )
            result.is_valid = False

    def validate_all(self) -> list[RelationshipValidationResult]:
        """
        Validate all relationships in the graph.
        
        Returns:
            List of validation results
        """
        return [self.validate(edge.edge_id) for edge in self._graph.list_edges()]

    def find_invalid_relationships(self) -> list[RelationshipValidationResult]:
        """
        Find all invalid relationships.
        
        Returns:
            List of invalid relationship results
        """
        return [r for r in self.validate_all() if not r.is_valid]

    def find_relationships_without_confidence(self) -> list[str]:
        """
        Find relationships with default confidence.
        
        Returns:
            List of edge IDs
        """
        return [
            edge.edge_id
            for edge in self._graph.list_edges()
            if edge.confidence == 1.0
        ]
