from __future__ import annotations

"""
knowledge/graph/validation/ontology_validator.py

Ontology validator for the Knowledge Layer.

Validates entities and relationships against ontology definitions.
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, NodeType, RelationshipType
from knowledge.ontology.ontology_loader import OntologyLoader


@dataclass
class OntologyValidationResult:
    """Result of ontology validation."""
    is_valid: bool
    entity_type: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def success(cls, entity_type: str) -> "OntologyValidationResult":
        """Create a successful validation result."""
        return cls(is_valid=True, entity_type=entity_type)

    @classmethod
    def failure(
        cls,
        entity_type: str,
        errors: list[str],
    ) -> "OntologyValidationResult":
        """Create a failed validation result."""
        return cls(is_valid=False, entity_type=entity_type, errors=errors)


class OntologyValidator:
    """
    Validates entities and relationships against ontology definitions.
    """

    def __init__(
        self,
        graph: Graph,
        loader: OntologyLoader | None = None,
    ) -> None:
        """
        Initialize ontology validator.
        
        Args:
            graph: The graph to validate
            loader: Optional ontology loader
        """
        self._graph = graph
        self._loader = loader or OntologyLoader()

    def validate_node_type(self, node_type: NodeType) -> OntologyValidationResult:
        """
        Validate a node type against ontology.
        
        Args:
            node_type: The node type to validate
            
        Returns:
            OntologyValidationResult
        """
        if isinstance(node_type, str):
            node_type = NodeType(node_type)
        
        entity = self._loader.get_entity(node_type.value)
        if entity:
            return OntologyValidationResult.success(node_type.value)
        
        return OntologyValidationResult.failure(
            node_type.value,
            [f"Node type '{node_type.value}' not found in ontology"],
        )

    def validate_relationship_type(
        self,
        relationship_type: RelationshipType,
    ) -> OntologyValidationResult:
        """
        Validate a relationship type against ontology.
        
        Args:
            relationship_type: The relationship type to validate
            
        Returns:
            OntologyValidationResult
        """
        if isinstance(relationship_type, str):
            relationship_type = RelationshipType(relationship_type)
        
        relationship = self._loader.get_relationship(relationship_type.value)
        if relationship:
            return OntologyValidationResult.success(relationship_type.value)
        
        return OntologyValidationResult.failure(
            relationship_type.value,
            [f"Relationship type '{relationship_type.value}' not found in ontology"],
        )

    def validate_all_types(self) -> dict[str, OntologyValidationResult]:
        """
        Validate all node and relationship types in the graph.
        
        Returns:
            Dictionary of type -> validation result
        """
        results: dict[str, OntologyValidationResult] = {}
        
        for node in self._graph.list_nodes():
            type_str = node.node_type.value
            if type_str not in results:
                results[type_str] = self.validate_node_type(node.node_type)
        
        for edge in self._graph.list_edges():
            type_str = edge.relationship_type.value
            if type_str not in results:
                results[type_str] = self.validate_relationship_type(edge.relationship_type)
        
        return results

    def get_undefined_types(self) -> dict[str, list[str]]:
        """
        Get all types that are not defined in ontology.
        
        Returns:
            Dictionary with 'nodes' and 'relationships' lists
        """
        undefined_nodes: list[str] = []
        undefined_relationships: list[str] = []
        
        for node in self._graph.list_nodes():
            if not self._loader.get_entity(node.node_type.value):
                undefined_nodes.append(node.node_type.value)
        
        for edge in self._graph.list_edges():
            if not self._loader.get_relationship(edge.relationship_type.value):
                undefined_relationships.append(edge.relationship_type.value)
        
        return {
            "nodes": list(set(undefined_nodes)),
            "relationships": list(set(undefined_relationships)),
        }
