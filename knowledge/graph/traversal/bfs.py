from __future__ import annotations

"""
knowledge/graph/traversal/bfs.py

Breadth-First Search traversal for the Knowledge Layer.

Deterministic BFS implementation.
"""
from collections import deque
from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, Node, Edge


@dataclass
class BFSResult:
    """Result of BFS traversal."""
    visited_nodes: list[str]
    visited_edges: list[str]
    levels: dict[str, int]
    paths: dict[str, list[str]]
    metadata: dict[str, Any] = field(default_factory=dict)


class BFSTraversal:
    """
    Breadth-First Search traversal.
    
    Deterministic, in-memory implementation.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize BFS traversal.
        
        Args:
            graph: The graph to traverse
        """
        self._graph = graph

    def traverse(
        self,
        start_node_id: str,
        max_depth: int | None = None,
        direction: str = "both",
    ) -> BFSResult:
        """
        Perform BFS traversal from a starting node.
        
        Args:
            start_node_id: The starting node ID
            max_depth: Maximum traversal depth (None for unlimited)
            direction: Traversal direction ("outgoing", "incoming", "both")
            
        Returns:
            BFSResult with traversal information
        """
        visited_nodes: set[str] = set()
        visited_edges: set[str] = set()
        levels: dict[str, int] = {}
        paths: dict[str, list[str]] = {}
        
        queue: deque[tuple[str, int, list[str]]] = deque()
        
        start_node = self._graph.get_node(start_node_id)
        if not start_node:
            return BFSResult(
                visited_nodes=list(visited_nodes),
                visited_edges=list(visited_edges),
                levels=levels,
                paths=paths,
            )

        visited_nodes.add(start_node_id)
        levels[start_node_id] = 0
        paths[start_node_id] = [start_node_id]
        queue.append((start_node_id, 0, [start_node_id]))

        adjacency = self._build_adjacency(direction)

        while queue:
            current_id, depth, path = queue.popleft()
            
            if max_depth is not None and depth >= max_depth:
                continue
            
            neighbors = adjacency.get(current_id, [])
            
            for neighbor_id, edge_id in neighbors:
                if neighbor_id not in visited_nodes:
                    visited_nodes.add(neighbor_id)
                    levels[neighbor_id] = depth + 1
                    paths[neighbor_id] = path + [neighbor_id]
                    queue.append((neighbor_id, depth + 1, paths[neighbor_id]))
                
                if edge_id not in visited_edges:
                    visited_edges.add(edge_id)

        return BFSResult(
            visited_nodes=list(visited_nodes),
            visited_edges=list(visited_edges),
            levels=levels,
            paths=paths,
        )

    def find_nodes_at_level(
        self,
        start_node_id: str,
        level: int,
        direction: str = "both",
    ) -> list[Node]:
        """
        Find all nodes at a specific level from start.
        
        Args:
            start_node_id: The starting node ID
            level: The level to find
            direction: Traversal direction
            
        Returns:
            List of nodes at the specified level
        """
        result = self.traverse(start_node_id, max_depth=level, direction=direction)
        
        return [
            self._graph.get_node(node_id)
            for node_id, lvl in result.levels.items()
            if lvl == level
            for node in [self._graph.get_node(node_id)]
            if node is not None
        ]

    def find_reachable_nodes(
        self,
        start_node_id: str,
        direction: str = "both",
    ) -> list[Node]:
        """
        Find all reachable nodes from start.
        
        Args:
            start_node_id: The starting node ID
            direction: Traversal direction
            
        Returns:
            List of reachable nodes
        """
        result = self.traverse(start_node_id, direction=direction)
        
        return [
            self._graph.get_node(node_id)
            for node_id in result.visited_nodes
            for node in [self._graph.get_node(node_id)]
            if node is not None
        ]

    def _build_adjacency(
        self,
        direction: str,
    ) -> dict[str, list[tuple[str, str]]]:
        """
        Build adjacency list from graph.
        
        Args:
            direction: Traversal direction
            
        Returns:
            Adjacency dictionary
        """
        adjacency: dict[str, list[tuple[str, str]]] = {}
        
        for edge in self._graph.list_edges():
            if direction in ("outgoing", "both"):
                if edge.source_node_id not in adjacency:
                    adjacency[edge.source_node_id] = []
                adjacency[edge.source_node_id].append(
                    (edge.target_node_id, edge.edge_id)
                )
            
            if direction in ("incoming", "both"):
                if edge.target_node_id not in adjacency:
                    adjacency[edge.target_node_id] = []
                adjacency[edge.target_node_id].append(
                    (edge.source_node_id, edge.edge_id)
                )
        
        return adjacency
