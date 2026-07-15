from __future__ import annotations

"""
knowledge/graph/validation/entity_validator.py

Entity validator for the Knowledge Layer.

Validates entity (node) structure and integrity.
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, Node, NodeType


@dataclass
class EntityValidationResult:
    """Result of entity validation."""
    is_valid: bool
    node_id: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def success(cls, node_id: str) -> "EntityValidationResult":
        """Create a successful validation result."""
        return cls(is_valid=True, node_id=node_id)

    @classmethod
    def failure(cls, node_id: str, errors: list[str]) -> "EntityValidationResult":
        """Create a failed validation result."""
        return cls(is_valid=False, node_id=node_id, errors=errors)


class EntityValidator:
    """
    Validates entity (node) structure and integrity.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize entity validator.
        
        Args:
            graph: The graph containing the entities
        """
        self._graph = graph

    def validate(self, node_id: str) -> EntityValidationResult:
        """
        Validate an entity.
        
        Args:
            node_id: The node ID to validate
            
        Returns:
            EntityValidationResult
        """
        node = self._graph.get_node(node_id)
        if not node:
            return EntityValidationResult.failure(
                node_id,
                [f"Node {node_id} not found in graph"],
            )

        result = EntityValidationResult.success(node_id)
        
        self._validate_node_id(node, result)
        self._validate_node_type(node, result)
        self._validate_attributes(node, result)
        
        return result

    def _validate_node_id(self, node: Node, result: EntityValidationResult) -> None:
        """Validate node ID."""
        if not node.node_id:
            result.errors.append("Node has no node_id")
            result.is_valid = False

    def _validate_node_type(self, node: Node, result: EntityValidationResult) -> None:
        """Validate node type."""
        if node.node_type == NodeType.UNKNOWN:
            result.warnings.append("Node type is UNKNOWN")

    def _validate_attributes(self, node: Node, result: EntityValidationResult) -> None:
        """Validate node attributes."""
        if not isinstance(node.attributes, dict):
            result.errors.append("Node attributes is not a dictionary")
            result.is_valid = False

    def validate_all(self) -> list[EntityValidationResult]:
        """
        Validate all entities in the graph.
        
        Returns:
            List of validation results
        """
        return [self.validate(node.node_id) for node in self._graph.list_nodes()]

    def find_invalid_entities(self) -> list[EntityValidationResult]:
        """
        Find all invalid entities.
        
        Returns:
            List of invalid entity results
        """
        return [r for r in self.validate_all() if not r.is_valid]
