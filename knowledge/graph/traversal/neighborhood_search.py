from __future__ import annotations

"""
knowledge/graph/traversal/neighborhood_search.py

Neighborhood search for the Knowledge Layer.

Provides neighborhood expansion algorithms.
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, Node, Edge, RelationshipType


@dataclass
class NeighborhoodResult:
    """Result of neighborhood search."""
    center_node_id: str
    nodes: list[Node]
    edges: list[Edge]
    levels: dict[str, int]
    relationship_types: dict[str, list[str]]
    metadata: dict[str, Any] = field(default_factory=dict)


class NeighborhoodSearch:
    """
    Neighborhood search algorithms.
    
    Deterministic, in-memory implementation.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize neighborhood search.
        
        Args:
            graph: The graph to search
        """
        self._graph = graph

    def expand(
        self,
        center_node_id: str,
        radius: int = 1,
        direction: str = "both",
        include_relationship_types: list[RelationshipType] | None = None,
    ) -> NeighborhoodResult:
        """
        Expand neighborhood from a center node.
        
        Args:
            center_node_id: The center node ID
            radius: Expansion radius (1 = direct neighbors)
            direction: Traversal direction
            include_relationship_types: Filter by relationship types
            
        Returns:
            NeighborhoodResult
        """
        center_node = self._graph.get_node(center_node_id)
        if not center_node:
            return NeighborhoodResult(
                center_node_id=center_node_id,
                nodes=[],
                edges=[],
                levels={},
                relationship_types={},
            )

        nodes: list[Node] = [center_node]
        edges: list[Edge] = []
        levels: dict[str, int] = {center_node_id: 0}
        relationship_types: dict[str, list[str]] = {}
        
        adjacency = self._build_adjacency(direction, include_relationship_types)
        
        current_level = {center_node_id}
        
        for level in range(1, radius + 1):
            next_level: set[str] = set()
            
            for node_id in current_level:
                neighbors = adjacency.get(node_id, [])
                
                for neighbor_id, edge_id, rel_type in neighbors:
                    if neighbor_id not in levels:
                        levels[neighbor_id] = level
                        next_level.add(neighbor_id)
                        
                        neighbor_node = self._graph.get_node(neighbor_id)
                        if neighbor_node:
                            nodes.append(neighbor_node)
                    
                    edge = self._graph.get_edge(edge_id)
                    if edge and edge not in edges:
                        edges.append(edge)
                        
                        rel_type_str = rel_type.value if isinstance(rel_type, RelationshipType) else rel_type
                        if rel_type_str not in relationship_types:
                            relationship_types[rel_type_str] = []
                        if edge_id not in relationship_types[rel_type_str]:
                            relationship_types[rel_type_str].append(edge_id)
            
            current_level = next_level
            if not current_level:
                break

        return NeighborhoodResult(
            center_node_id=center_node_id,
            nodes=nodes,
            edges=edges,
            levels=levels,
            relationship_types=relationship_types,
        )

    def get_direct_neighbors(
        self,
        node_id: str,
        direction: str = "both",
    ) -> list[Node]:
        """
        Get direct neighbors of a node.
        
        Args:
            node_id: The node ID
            direction: Traversal direction
            
        Returns:
            List of neighbor nodes
        """
        result = self.expand(node_id, radius=1, direction=direction)
        return [n for n in result.nodes if n.node_id != node_id]

    def get_neighbors_by_relationship(
        self,
        node_id: str,
        relationship_type: RelationshipType,
    ) -> list[Node]:
        """
        Get neighbors connected by specific relationship type.
        
        Args:
            node_id: The node ID
            relationship_type: The relationship type to filter by
            
        Returns:
            List of neighbor nodes
        """
        result = self.expand(
            node_id,
            radius=1,
            direction="both",
            include_relationship_types=[relationship_type],
        )
        return [n for n in result.nodes if n.node_id != node_id]

    def get_ego_network(
        self,
        node_id: str,
        radius: int = 1,
    ) -> NeighborhoodResult:
        """
        Get the ego network of a node.
        
        The ego network includes the center node and all nodes within radius.
        
        Args:
            node_id: The center node ID
            radius: Network radius
            
        Returns:
            NeighborhoodResult
        """
        return self.expand(node_id, radius=radius, direction="both")

    def find_common_neighbors(
        self,
        node_id_1: str,
        node_id_2: str,
    ) -> list[Node]:
        """
        Find common neighbors of two nodes.
        
        Args:
            node_id_1: First node ID
            node_id_2: Second node ID
            
        Returns:
            List of common neighbor nodes
        """
        neighbors_1 = set(n.node_id for n in self.get_direct_neighbors(node_id_1))
        neighbors_2 = set(n.node_id for n in self.get_direct_neighbors(node_id_2))
        
        common_ids = neighbors_1 & neighbors_2
        
        return [
            self._graph.get_node(nid)
            for nid in common_ids
            for node in [self._graph.get_node(nid)]
            if node is not None
        ]

    def _build_adjacency(
        self,
        direction: str,
        include_relationship_types: list[RelationshipType] | None = None,
    ) -> dict[str, list[tuple[str, str, RelationshipType]]]:
        """Build adjacency list from graph."""
        adjacency: dict[str, list[tuple[str, str, RelationshipType]]] = {}
        
        for edge in self._graph.list_edges():
            if include_relationship_types:
                if edge.relationship_type not in include_relationship_types:
                    continue
            
            if direction in ("outgoing", "both"):
                if edge.source_node_id not in adjacency:
                    adjacency[edge.source_node_id] = []
                adjacency[edge.source_node_id].append(
                    (edge.target_node_id, edge.edge_id, edge.relationship_type)
                )
            
            if direction in ("incoming", "both"):
                if edge.target_node_id not in adjacency:
                    adjacency[edge.target_node_id] = []
                adjacency[edge.target_node_id].append(
                    (edge.source_node_id, edge.edge_id, edge.relationship_type)
                )
        
        return adjacency
