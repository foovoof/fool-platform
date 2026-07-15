from __future__ import annotations

"""
knowledge/graph/queries/graph_queries.py

Graph queries for the Knowledge Layer.
"""
from typing import Any

from knowledge.graph.models import Graph, Node, Edge, NodeType
from knowledge.graph.queries.query_context import QueryContext


class GraphQueries:
    """
    Graph query operations.
    
    Provides overall graph query operations.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize graph queries.
        
        Args:
            graph: The graph to query
        """
        self._graph = graph

    def get_stats(self) -> dict[str, Any]:
        """
        Get graph statistics.
        
        Returns:
            Dictionary with graph statistics
        """
        all_nodes = self._graph.list_nodes()
        all_edges = self._graph.list_edges()
        
        type_counts: dict[str, int] = {}
        for node in all_nodes:
            node_type = node.node_type.value
            type_counts[node_type] = type_counts.get(node_type, 0) + 1
        
        rel_type_counts: dict[str, int] = {}
        for edge in all_edges:
            rel_type = edge.relationship_type.value
            rel_type_counts[rel_type] = rel_type_counts.get(rel_type, 0) + 1
        
        return {
            "graph_id": self._graph.graph_id,
            "graph_version": self._graph.graph_version,
            "node_count": len(all_nodes),
            "edge_count": len(all_edges),
            "node_types": type_counts,
            "relationship_types": rel_type_counts,
            "created_at": self._graph.created_at,
        }

    def find_isolated_nodes(
        self,
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find nodes with no connections.
        
        Args:
            context: Optional query context
            
        Returns:
            List of isolated nodes
        """
        connected_nodes: set[str] = set()
        
        for edge in self._graph.list_edges():
            connected_nodes.add(edge.source_node_id)
            connected_nodes.add(edge.target_node_id)
        
        all_nodes = self._graph.list_nodes()
        results = [
            node for node in all_nodes
            if node.node_id not in connected_nodes
        ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_nodes_without_type(
        self,
        node_type: NodeType,
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find nodes that are not of a specific type.
        
        Args:
            node_type: The node type to exclude
            context: Optional query context
            
        Returns:
            List of nodes not of the specified type
        """
        if isinstance(node_type, str):
            node_type = NodeType(node_type)
        
        all_nodes = self._graph.list_nodes()
        results = [
            node for node in all_nodes
            if node.node_type != node_type
        ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_dangling_edges(
        self,
        context: QueryContext | None = None,
    ) -> list[Edge]:
        """
        Find edges that reference non-existent nodes.
        
        Args:
            context: Optional query context
            
        Returns:
            List of dangling edges
        """
        node_ids = {node.node_id for node in self._graph.list_nodes()}
        
        results = [
            edge for edge in self._graph.list_edges()
            if edge.source_node_id not in node_ids
            or edge.target_node_id not in node_ids
        ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def find_self_loops(
        self,
        context: QueryContext | None = None,
    ) -> list[Edge]:
        """
        Find self-loop edges.
        
        Args:
            context: Optional query context
            
        Returns:
            List of self-loop edges
        """
        results = [
            edge for edge in self._graph.list_edges()
            if edge.is_self_loop()
        ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results

    def get_connected_components(self) -> list[list[str]]:
        """
        Get all connected components.
        
        Returns:
            List of connected components (each is a list of node IDs)
        """
        visited: set[str] = set()
        all_nodes = self._graph.list_nodes()
        components: list[list[str]] = []
        
        adjacency: dict[str, set[str]] = {}
        for edge in self._graph.list_edges():
            if edge.source_node_id not in adjacency:
                adjacency[edge.source_node_id] = set()
            if edge.target_node_id not in adjacency:
                adjacency[edge.target_node_id] = set()
            adjacency[edge.source_node_id].add(edge.target_node_id)
            adjacency[edge.target_node_id].add(edge.source_node_id)
        
        for node in all_nodes:
            if node.node_id in visited:
                continue
            
            component: list[str] = []
            stack = [node.node_id]
            
            while stack:
                node_id = stack.pop()
                if node_id in visited:
                    continue
                
                visited.add(node_id)
                component.append(node_id)
                
                for neighbor in adjacency.get(node_id, set()):
                    if neighbor not in visited:
                        stack.append(neighbor)
            
            if component:
                components.append(component)
        
        return components

    def find_nodes_with_attributes(
        self,
        attributes: dict[str, Any],
        match_all: bool = True,
        context: QueryContext | None = None,
    ) -> list[Node]:
        """
        Find nodes with specific attributes.
        
        Args:
            attributes: Dictionary of attributes to match
            match_all: If True, all attributes must match
            context: Optional query context
            
        Returns:
            List of matching nodes
        """
        all_nodes = self._graph.list_nodes()
        
        if match_all:
            results = [
                node for node in all_nodes
                if all(
                    node.attributes.get(k) == v
                    for k, v in attributes.items()
                )
            ]
        else:
            results = [
                node for node in all_nodes
                if any(
                    node.attributes.get(k) == v
                    for k, v in attributes.items()
                )
            ]
        
        if context:
            results = context.pagination.apply(results)
        
        return results
