from __future__ import annotations

"""
knowledge/services/knowledge_graph_service.py

Knowledge Graph Service for the Knowledge Layer.

Orchestrates graph operations.
"""
from typing import Any

from knowledge.graph.models import Graph, Node, Edge, NodeType, RelationshipType
from knowledge.graph.repository import GraphRepository
from knowledge.graph.validation import (
    GraphValidator,
    EntityValidator,
    RelationshipValidator,
    ConsistencyValidator,
)
from knowledge.events import KnowledgeEventEmitter


class KnowledgeGraphService:
    """
    Service for knowledge graph operations.
    
    Orchestrates:
    - Graph management
    - Validation
    - Event emission
    """

    def __init__(
        self,
        repository: GraphRepository | None = None,
        event_emitter: KnowledgeEventEmitter | None = None,
    ) -> None:
        """
        Initialize the service.
        
        Args:
            repository: Optional graph repository
            event_emitter: Optional event emitter
        """
        self._repository = repository or GraphRepository()
        self._event_emitter = event_emitter or KnowledgeEventEmitter()
        self._graph_validator = None
        self._entity_validator = None
        self._relationship_validator = None

    def create_graph(self, graph: Graph) -> Graph:
        """
        Create a new knowledge graph.
        
        Args:
            graph: The graph to create
            
        Returns:
            The created graph
        """
        return self._repository.create(graph)

    def get_graph(self, graph_id: str) -> Graph | None:
        """Get a graph by ID."""
        return self._repository.get_by_id(graph_id)

    def add_node(
        self,
        graph_id: str,
        node: Node,
    ) -> bool:
        """
        Add a node to a graph.
        
        Args:
            graph_id: The graph ID
            node: The node to add
            
        Returns:
            True if added
        """
        if self._repository.add_node(graph_id, node):
            self._event_emitter.emit_node_created(node.node_id, node.node_type.value)
            return True
        return False

    def add_edge(
        self,
        graph_id: str,
        edge: Edge,
    ) -> bool:
        """
        Add an edge to a graph.
        
        Args:
            graph_id: The graph ID
            edge: The edge to add
            
        Returns:
            True if added
        """
        if self._repository.add_edge(graph_id, edge):
            self._event_emitter.emit_edge_created(
                edge.edge_id,
                edge.source_node_id,
                edge.target_node_id,
                edge.relationship_type.value,
            )
            return True
        return False

    def validate_graph(self, graph_id: str) -> dict[str, Any]:
        """
        Validate a graph.
        
        Args:
            graph_id: The graph ID
            
        Returns:
            Validation results
        """
        graph = self._repository.get_by_id(graph_id)
        if not graph:
            return {"error": f"Graph {graph_id} not found"}

        self._graph_validator = GraphValidator(graph)
        self._entity_validator = EntityValidator(graph)
        self._relationship_validator = RelationshipValidator(graph)

        graph_result = self._graph_validator.validate()
        entity_results = self._entity_validator.validate_all()
        relationship_results = self._relationship_validator.validate_all()

        consistency_validator = ConsistencyValidator(graph)
        consistency_result = consistency_validator.validate()

        self._event_emitter.emit_graph_validated(
            graph_id,
            graph_result.is_valid,
            len(graph_result.errors),
        )

        return {
            "graph_id": graph_id,
            "is_valid": (
                graph_result.is_valid
                and all(r.is_valid for r in entity_results)
                and all(r.is_valid for r in relationship_results)
            ),
            "graph_validation": {
                "is_valid": graph_result.is_valid,
                "errors": graph_result.errors,
                "warnings": graph_result.warnings,
            },
            "entity_count": len(entity_results),
            "relationship_count": len(relationship_results),
            "consistency": {
                "is_valid": consistency_result.is_valid,
                "errors": consistency_result.errors,
            },
        }

    def get_graph_stats(self, graph_id: str) -> dict[str, Any]:
        """
        Get graph statistics.
        
        Args:
            graph_id: The graph ID
            
        Returns:
            Graph statistics
        """
        graph = self._repository.get_by_id(graph_id)
        if not graph:
            return {"error": f"Graph {graph_id} not found"}

        return {
            "graph_id": graph_id,
            "node_count": graph.get_node_count(),
            "edge_count": graph.get_edge_count(),
            "created_at": graph.created_at,
        }
