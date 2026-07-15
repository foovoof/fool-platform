from __future__ import annotations

"""
knowledge/graph/queries/entity_queries.py

Entity queries for the Knowledge Layer.
"""
from typing import Any

from knowledge.graph.models import Graph, Node, NodeType
from knowledge.graph.queries.query_context import QueryContext


class EntityQueries:
    """
    Entity query operations.
    
    Provides query operations for entities (nodes) in the graph.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize entity queries.
        
        Args:
            graph: The graph to query
        """
        self._graph = graph

    def find_by_type(
        self,
        node_type: NodeType,
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find all entities of a specific type.
        
        Args:
            node_type: The node type to filter by
            context: Optional query context
            
        Returns:
            List of matching nodes
        """
        if isinstance(node_type, str):
            node_type = NodeType(node_type)
        
        results = self._graph.get_nodes_by_type(node_type)
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_by_attribute(
        self,
        key: str,
        value: Any | None = None,
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find entities by attribute.
        
        Args:
            key: Attribute key to filter by
            value: Optional attribute value to match
            context: Optional query context
            
        Returns:
            List of matching nodes
        """
        all_nodes = self._graph.list_nodes()
        
        if value is not None:
            results = [
                node for node in all_nodes
                if key in node.attributes and node.attributes[key] == value
            ]
        else:
            results = [
                node for node in all_nodes
                if key in node.attributes
            ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_by_identity(
        self,
        identity_ref: str,
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find entities by identity reference.
        
        Args:
            identity_ref: The identity reference to search for
            context: Optional query context
            
        Returns:
            List of matching nodes
        """
        results = self._graph.get_nodes_by_identity(identity_ref)
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_neighbors(
        self,
        node_id: str,
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find neighboring entities.
        
        Args:
            node_id: The node ID
            context: Optional query context
            
        Returns:
            List of neighboring nodes
        """
        node = self._graph.get_node(node_id)
        if not node:
            return []
        
        all_nodes = self._graph.list_nodes()
        connected_ids: set[str] = set()
        
        for edge in self._graph.list_edges():
            if edge.source_node_id == node_id:
                connected_ids.add(edge.target_node_id)
            elif edge.target_node_id == node_id:
                connected_ids.add(edge.source_node_id)
        
        results = [
            n for n in all_nodes
            if n.node_id in connected_ids
        ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_connected_entities(
        self,
        source_id: str,
        target_id: str,
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find all entities connected to both source and target.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            context: Optional query context
            
        Returns:
            List of nodes connected to both source and target
        """
        source_neighbors = {n.node_id for n in self.find_neighbors(source_id)}
        target_neighbors = {n.node_id for n in self.find_neighbors(target_id)}
        
        connected_ids = source_neighbors & target_neighbors
        
        results = [
            self._graph.get_node(nid)
            for nid in connected_ids
            for node in [self._graph.get_node(nid)]
            if node is not None
        ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_subgraph(
        self,
        node_ids: list[str],
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find all nodes in a subgraph.
        
        Args:
            node_ids: IDs of nodes in the subgraph
            context: Optional query context
            
        Returns:
            List of nodes in the subgraph
        """
        node_ids_set = set(node_ids)
        results = [
            self._graph.get_node(nid)
            for nid in node_ids
            for node in [self._graph.get_node(nid)]
            if node is not None
        ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results
