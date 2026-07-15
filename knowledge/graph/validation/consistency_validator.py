from __future__ import annotations

"""
knowledge/graph/validation/consistency_validator.py

Consistency validator for the Knowledge Layer.

Validates overall graph consistency.
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph


@dataclass
class ConsistencyValidationResult:
    """Result of consistency validation."""
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    orphan_nodes: list[str] = field(default_factory=list)
    orphan_edges: list[str] = field(default_factory=list)
    invalid_references: list[tuple[str, str]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def success(cls) -> "ConsistencyValidationResult":
        """Create a successful validation result."""
        return cls(is_valid=True)

    @classmethod
    def failure(cls, errors: list[str]) -> "ConsistencyValidationResult":
        """Create a failed validation result."""
        return cls(is_valid=False, errors=errors)


class ConsistencyValidator:
    """
    Validates overall graph consistency.
    
    Checks for:
    - Broken references
    - Orphan nodes/edges
    - Contract compliance
    - Data integrity
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize consistency validator.
        
        Args:
            graph: The graph to validate
        """
        self._graph = graph

    def validate(self) -> ConsistencyValidationResult:
        """
        Perform full consistency validation.
        
        Returns:
            ConsistencyValidationResult
        """
        result = ConsistencyValidationResult.success()
        
        self._check_node_references(result)
        self._check_edge_references(result)
        self._check_attribute_consistency(result)
        self._check_identity_consistency(result)
        
        result.is_valid = len(result.errors) == 0
        
        return result

    def _check_node_references(self, result: ConsistencyValidationResult) -> None:
        """Check that all node references are valid."""
        node_ids = {node.node_id for node in self._graph.list_nodes()}
        
        for node in self._graph.list_nodes():
            for entity_ref in node.entity_refs:
                if entity_ref not in node_ids:
                    result.invalid_references.append((node.node_id, entity_ref))
                    result.errors.append(
                        f"Node {node.node_id} references non-existent entity {entity_ref}"
                    )

    def _check_edge_references(self, result: ConsistencyValidationResult) -> None:
        """Check that all edge references are valid."""
        node_ids = {node.node_id for node in self._graph.list_nodes()}
        
        for edge in self._graph.list_edges():
            if edge.source_node_id not in node_ids:
                result.orphan_edges.append(edge.edge_id)
                result.errors.append(
                    f"Edge {edge.edge_id} references non-existent source {edge.source_node_id}"
                )
            
            if edge.target_node_id not in node_ids:
                result.orphan_edges.append(edge.edge_id)
                result.errors.append(
                    f"Edge {edge.edge_id} references non-existent target {edge.target_node_id}"
                )

    def _check_attribute_consistency(
        self,
        result: ConsistencyValidationResult,
    ) -> None:
        """Check attribute consistency."""
        for node in self._graph.list_nodes():
            if not isinstance(node.attributes, dict):
                result.errors.append(
                    f"Node {node.node_id} has invalid attributes type"
                )

    def _check_identity_consistency(
        self,
        result: ConsistencyValidationResult,
    ) -> None:
        """Check identity consistency."""
        identity_refs: dict[str, list[str]] = {}
        
        for node in self._graph.list_nodes():
            for ref in node.identity_refs:
                if ref not in identity_refs:
                    identity_refs[ref] = []
                identity_refs[ref].append(node.node_id)
        
        for ref, node_ids in identity_refs.items():
            if len(node_ids) > 1:
                result.warnings.append(
                    f"Identity reference '{ref}' shared by {len(node_ids)} nodes"
                )

    def validate_contract_compliance(self) -> ConsistencyValidationResult:
        """
        Validate contract compliance.
        
        Returns:
            ConsistencyValidationResult
        """
        result = ConsistencyValidationResult.success()
        
        for node in self._graph.list_nodes():
            if not node.identity_refs:
                result.warnings.append(
                    f"Node {node.node_id} has no identity references (contract violation)"
                )
        
        result.is_valid = len(result.errors) == 0
        return result
