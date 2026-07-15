from __future__ import annotations

"""
knowledge/graph/traversal/dfs.py

Depth-First Search traversal for the Knowledge Layer.

Deterministic DFS implementation.
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, Node, Edge


@dataclass
class DFSResult:
    """Result of DFS traversal."""
    visited_nodes: list[str]
    visited_edges: list[str]
    traversal_order: list[str]
    back_edges: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


class DFSTraversal:
    """
    Depth-First Search traversal.
    
    Deterministic, in-memory implementation.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize DFS traversal.
        
        Args:
            graph: The graph to traverse
        """
        self._graph = graph

    def traverse(
        self,
        start_node_id: str,
        max_depth: int | None = None,
        direction: str = "both",
    ) -> DFSResult:
        """
        Perform DFS traversal from a starting node.
        
        Args:
            start_node_id: The starting node ID
            max_depth: Maximum traversal depth (None for unlimited)
            direction: Traversal direction ("outgoing", "incoming", "both")
            
        Returns:
            DFSResult with traversal information
        """
        visited_nodes: set[str] = set()
        visited_edges: set[str] = set()
        traversal_order: list[str] = []
        back_edges: list[str] = []
        
        adjacency = self._build_adjacency(direction)
        
        self._dfs_recursive(
            start_node_id,
            0,
            max_depth,
            visited_nodes,
            visited_edges,
            traversal_order,
            back_edges,
            adjacency,
            set(),
        )

        return DFSResult(
            visited_nodes=list(visited_nodes),
            visited_edges=list(visited_edges),
            traversal_order=traversal_order,
            back_edges=back_edges,
        )

    def find_connected_component(
        self,
        start_node_id: str,
        direction: str = "both",
    ) -> list[Node]:
        """
        Find all nodes in the connected component.
        
        Args:
            start_node_id: The starting node ID
            direction: Traversal direction
            
        Returns:
            List of nodes in the connected component
        """
        result = self.traverse(start_node_id, direction=direction)
        
        return [
            self._graph.get_node(node_id)
            for node_id in result.visited_nodes
            for node in [self._graph.get_node(node_id)]
            if node is not None
        ]

    def has_cycle(self, start_node_id: str, direction: str = "both") -> bool:
        """
        Check if there is a cycle in the traversal.
        
        Args:
            start_node_id: The starting node ID
            direction: Traversal direction
            
        Returns:
            True if a cycle was found
        """
        result = self.traverse(start_node_id, direction=direction)
        return len(result.back_edges) > 0

    def find_all_cycles(self, direction: str = "both") -> list[list[str]]:
        """
        Find all cycles in the graph.
        
        Args:
            direction: Traversal direction
            
        Returns:
            List of cycles (each cycle is a list of node IDs)
        """
        all_nodes = [n.node_id for n in self._graph.list_nodes()]
        visited: set[str] = set()
        cycles: list[list[str]] = []
        
        for node_id in all_nodes:
            if node_id not in visited:
                self._find_cycles_from(
                    node_id,
                    direction,
                    visited,
                    cycles,
                    set(),
                    [],
                )

        return cycles

    def _find_cycles_from(
        self,
        start_node_id: str,
        direction: str,
        visited: set[str],
        cycles: list[list[str]],
        in_progress: set[str],
        path: list[str],
    ) -> None:
        """Recursively find cycles starting from a node."""
        visited.add(start_node_id)
        in_progress.add(start_node_id)
        path.append(start_node_id)
        
        adjacency = self._build_adjacency(direction)
        neighbors = adjacency.get(start_node_id, [])
        
        for neighbor_id, _ in neighbors:
            if neighbor_id in in_progress:
                cycle_start = path.index(neighbor_id)
                cycle = path[cycle_start:] + [neighbor_id]
                cycles.append(cycle)
            elif neighbor_id not in visited:
                self._find_cycles_from(
                    neighbor_id,
                    direction,
                    visited,
                    cycles,
                    in_progress,
                    path.copy(),
                )
        
        in_progress.remove(start_node_id)

    def _dfs_recursive(
        self,
        node_id: str,
        depth: int,
        max_depth: int | None,
        visited_nodes: set[str],
        visited_edges: set[str],
        traversal_order: list[str],
        back_edges: list[str],
        adjacency: dict[str, list[tuple[str, str]]],
        path: set[str],
    ) -> None:
        """Recursive DFS helper."""
        if node_id in visited_nodes:
            return
        
        if max_depth is not None and depth > max_depth:
            return
        
        visited_nodes.add(node_id)
        traversal_order.append(node_id)
        path.add(node_id)
        
        neighbors = adjacency.get(node_id, [])
        
        for neighbor_id, edge_id in neighbors:
            if edge_id not in visited_edges:
                visited_edges.add(edge_id)
            
            if neighbor_id in path:
                back_edges.append(edge_id)
            
            if neighbor_id not in visited_nodes:
                self._dfs_recursive(
                    neighbor_id,
                    depth + 1,
                    max_depth,
                    visited_nodes,
                    visited_edges,
                    traversal_order,
                    back_edges,
                    adjacency,
                    path.copy(),
                )

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
