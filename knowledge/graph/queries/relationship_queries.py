from __future__ import annotations

"""
knowledge/graph/queries/relationship_queries.py

Relationship queries for the Knowledge Layer.
"""
from typing import Any

from knowledge.graph.models import Graph, Edge, RelationshipType
from knowledge.graph.queries.query_context import QueryContext


class RelationshipQueries:
    """
    Relationship query operations.
    
    Provides query operations for relationships (edges) in the graph.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize relationship queries.
        
        Args:
            graph: The graph to query
        """
        self._graph = graph

    def find_by_type(
        self,
        relationship_type: RelationshipType,
        context: QueryContext | None = None,
    ) -> list[Edge]:
        """
        Find all relationships of a specific type.
        
        Args:
            relationship_type: The relationship type
            context: Optional query context
            
        Returns:
            List of matching edges
        """
        if isinstance(relationship_type, str):
            relationship_type = RelationshipType(relationship_type)
        
        results = [
            edge for edge in self._graph.list_edges()
            if edge.relationship_type == relationship_type
        ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_by_node(
        self,
        node_id: str,
        context: QueryContext | None = None,
    ) -> list[Edge]:
        """
        Find all relationships involving a node.
        
        Args:
            node_id: The node ID
            context: Optional query context
            
        Returns:
            List of matching edges
        """
        results = [
            edge for edge in self._graph.list_edges()
            if edge.references_node(node_id)
        ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_between(
        self,
        source_id: str,
        target_id: str,
        context: QueryContext | None = None,
    ) -> list[Edge]:
        """
        Find relationships between two nodes.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            context: Optional query context
            
        Returns:
            List of matching edges
        """
        results = self._graph.get_edges_between(source_id, target_id)
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_outgoing(
        self,
        node_id: str,
        relationship_type: RelationshipType | None = None,
        context: QueryContext | None = None,
    ) -> list[Edge]:
        """
        Find outgoing relationships from a node.
        
        Args:
            node_id: The node ID
            relationship_type: Optional relationship type filter
            context: Optional query context
            
        Returns:
            List of outgoing edges
        """
        results = [
            edge for edge in self._graph.list_edges()
            if edge.source_node_id == node_id
        ]
        
        if relationship_type:
            if isinstance(relationship_type, str):
                relationship_type = RelationshipType(relationship_type)
            results = [
                edge for edge in results
                if edge.relationship_type == relationship_type
            ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_incoming(
        self,
        node_id: str,
        relationship_type: RelationshipType | None = None,
        context: QueryContext | None = None,
    ) -> list[Edge]:
        """
        Find incoming relationships to a node.
        
        Args:
            node_id: The node ID
            relationship_type: Optional relationship type filter
            context: Optional query context
            
        Returns:
            List of incoming edges
        """
        results = [
            edge for edge in self._graph.list_edges()
            if edge.target_node_id == node_id
        ]
        
        if relationship_type:
            if isinstance(relationship_type, str):
                relationship_type = RelationshipType(relationship_type)
            results = [
                edge for edge in results
                if edge.relationship_type == relationship_type
            ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def get_relationship_summary(
        self,
        node_id: str,
    ) -> dict[str, Any]:
        """
        Get summary of all relationships for a node.
        
        Args:
            node_id: The node ID
            
        Returns:
            Dictionary with relationship summary
        """
        outgoing = self.find_outgoing(node_id)
        incoming = self.find_incoming(node_id)
        
        type_counts: dict[str, int] = {}
        for edge in outgoing + incoming:
            rel_type = edge.relationship_type.value
            type_counts[rel_type] = type_counts.get(rel_type, 0) + 1
        
        return {
            "node_id": node_id,
            "outgoing_count": len(outgoing),
            "incoming_count": len(incoming),
            "total_count": len(outgoing) + len(incoming),
            "type_counts": type_counts,
        }
