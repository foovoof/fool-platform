from __future__ import annotations

"""
knowledge/graph/validation/identity_validator.py

Identity validator for the Knowledge Layer.

Validates identity references in the graph.
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, Node


@dataclass
class IdentityValidationResult:
    """Result of identity validation."""
    is_valid: bool
    node_id: str
    identity_refs: list[str]
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def success(
        cls,
        node_id: str,
        identity_refs: list[str],
    ) -> "IdentityValidationResult":
        """Create a successful validation result."""
        return cls(
            is_valid=True,
            node_id=node_id,
            identity_refs=identity_refs,
        )

    @classmethod
    def failure(
        cls,
        node_id: str,
        identity_refs: list[str],
        errors: list[str],
    ) -> "IdentityValidationResult":
        """Create a failed validation result."""
        return cls(
            is_valid=False,
            node_id=node_id,
            identity_refs=identity_refs,
            errors=errors,
        )


class IdentityValidator:
    """
    Validates identity references in the graph.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize identity validator.
        
        Args:
            graph: The graph containing the entities
        """
        self._graph = graph

    def validate(self, node_id: str) -> IdentityValidationResult:
        """
        Validate identity references for a node.
        
        Args:
            node_id: The node ID to validate
            
        Returns:
            IdentityValidationResult
        """
        node = self._graph.get_node(node_id)
        if not node:
            return IdentityValidationResult.failure(
                node_id,
                [],
                [f"Node {node_id} not found in graph"],
            )

        result = IdentityValidationResult.success(node_id, node.identity_refs)
        
        self._validate_identity_refs(node, result)
        self._check_duplicate_identities(result)
        
        return result

    def _validate_identity_refs(
        self,
        node: Node,
        result: IdentityValidationResult,
    ) -> None:
        """Validate identity references format."""
        for ref in node.identity_refs:
            if not ref:
                result.errors.append("Empty identity reference found")
                result.is_valid = False
            elif not isinstance(ref, str):
                result.errors.append(f"Identity reference is not a string: {type(ref)}")
                result.is_valid = False

    def _check_duplicate_identities(
        self,
        result: IdentityValidationResult,
    ) -> None:
        """Check for duplicate identity references."""
        seen: set[str] = set()
        for ref in result.identity_refs:
            if ref in seen:
                result.warnings.append(f"Duplicate identity reference: {ref}")
            seen.add(ref)

    def find_duplicate_identities(self) -> dict[str, list[str]]:
        """
        Find nodes that share identity references.
        
        Returns:
            Dictionary mapping identity_ref to list of node_ids
        """
        identity_map: dict[str, list[str]] = {}
        
        for node in self._graph.list_nodes():
            for ref in node.identity_refs:
                if ref not in identity_map:
                    identity_map[ref] = []
                identity_map[ref].append(node.node_id)
        
        return {
            ref: nodes
            for ref, nodes in identity_map.items()
            if len(nodes) > 1
        }

    def find_nodes_without_identities(self) -> list[str]:
        """
        Find nodes without identity references.
        
        Returns:
            List of node IDs without identities
        """
        return [
            node.node_id
            for node in self._graph.list_nodes()
            if not node.identity_refs
        ]
