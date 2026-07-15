from __future__ import annotations

"""
knowledge/graph/traversal/path_search.py

Path search algorithms for the Knowledge Layer.

Provides shortest path and path finding algorithms.
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.graph.models import Graph, Node


@dataclass
class PathResult:
    """Result of path search."""
    found: bool
    path: list[str]
    path_length: int
    edges_used: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


class PathSearch:
    """
    Path search algorithms.
    
    Deterministic, in-memory implementation.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize path search.
        
        Args:
            graph: The graph to search
        """
        self._graph = graph

    def find_shortest_path(
        self,
        source_id: str,
        target_id: str,
        direction: str = "both",
    ) -> PathResult:
        """
        Find the shortest path between two nodes.
        
        Uses BFS for unweighted shortest path.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            direction: Traversal direction
            
        Returns:
            PathResult with path information
        """
        if source_id == target_id:
            return PathResult(
                found=True,
                path=[source_id],
                path_length=0,
                edges_used=[],
            )

        adjacency = self._build_adjacency(direction)
        
        if source_id not in adjacency:
            return PathResult(
                found=False,
                path=[],
                path_length=-1,
                edges_used=[],
            )

        from collections import deque
        
        visited: set[str] = {source_id}
        queue: deque[tuple[str, list[str], list[str]]] = deque()
        queue.append((source_id, [source_id], []))

        while queue:
            current_id, path, edges = queue.popleft()
            
            neighbors = adjacency.get(current_id, [])
            
            for neighbor_id, edge_id in neighbors:
                if neighbor_id == target_id:
                    return PathResult(
                        found=True,
                        path=path + [neighbor_id],
                        path_length=len(path),
                        edges_used=edges + [edge_id],
                    )
                
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id], edges + [edge_id]))

        return PathResult(
            found=False,
            path=[],
            path_length=-1,
            edges_used=[],
        )

    def find_all_paths(
        self,
        source_id: str,
        target_id: str,
        max_length: int | None = None,
        direction: str = "both",
    ) -> list[PathResult]:
        """
        Find all paths between two nodes.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            max_length: Maximum path length (None for unlimited)
            direction: Traversal direction
            
        Returns:
            List of PathResult for each found path
        """
        if source_id == target_id:
            return [
                PathResult(
                    found=True,
                    path=[source_id],
                    path_length=0,
                    edges_used=[],
                )
            ]

        adjacency = self._build_adjacency(direction)
        all_paths: list[PathResult] = []
        
        self._find_all_paths_recursive(
            source_id,
            target_id,
            [source_id],
            [],
            adjacency,
            all_paths,
            max_length,
        )

        return all_paths

    def _find_all_paths_recursive(
        self,
        current_id: str,
        target_id: str,
        path: list[str],
        edges: list[str],
        adjacency: dict[str, list[tuple[str, str]]],
        all_paths: list[PathResult],
        max_length: int | None,
    ) -> None:
        """Recursively find all paths."""
        if max_length is not None and len(path) > max_length:
            return
        
        if current_id == target_id:
            all_paths.append(PathResult(
                found=True,
                path=path.copy(),
                path_length=len(path) - 1,
                edges_used=edges.copy(),
            ))
            return
        
        neighbors = adjacency.get(current_id, [])
        
        for neighbor_id, edge_id in neighbors:
            if neighbor_id not in path:
                self._find_all_paths_recursive(
                    neighbor_id,
                    target_id,
                    path + [neighbor_id],
                    edges + [edge_id],
                    adjacency,
                    all_paths,
                    max_length,
                )

    def find_shortest_paths_to_all(
        self,
        source_id: str,
        direction: str = "both",
    ) -> dict[str, PathResult]:
        """
        Find shortest paths from source to all reachable nodes.
        
        Args:
            source_id: Source node ID
            direction: Traversal direction
            
        Returns:
            Dictionary of target_id -> PathResult
        """
        adjacency = self._build_adjacency(direction)
        
        if source_id not in adjacency and source_id not in self._graph._nodes:  # noqa: SLF001
            return {}

        from collections import deque
        
        visited: set[str] = {source_id}
        distances: dict[str, int] = {source_id: 0}
        predecessors: dict[str, tuple[str, str]] = {}
        
        queue: deque[str] = deque()
        queue.append(source_id)

        while queue:
            current_id = queue.popleft()
            current_dist = distances.get(current_id, 0)
            
            neighbors = adjacency.get(current_id, [])
            
            for neighbor_id, edge_id in neighbors:
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    distances[neighbor_id] = current_dist + 1
                    predecessors[neighbor_id] = (current_id, edge_id)
                    queue.append(neighbor_id)

        results: dict[str, PathResult] = {}
        
        for target_id in visited:
            if target_id == source_id:
                continue
            
            path = self._reconstruct_path(source_id, target_id, predecessors)
            edges = [predecessors[n][1] for n in path[1:] if n in predecessors]
            
            results[target_id] = PathResult(
                found=True,
                path=path,
                path_length=distances.get(target_id, 0),
                edges_used=edges,
            )

        return results

    def _reconstruct_path(
        self,
        source_id: str,
        target_id: str,
        predecessors: dict[str, tuple[str, str]],
    ) -> list[str]:
        """Reconstruct path from predecessors."""
        path = [target_id]
        current = target_id
        
        while current != source_id:
            if current not in predecessors:
                break
            current, _ = predecessors[current]
            path.append(current)
        
        path.reverse()
        return path

    def _build_adjacency(
        self,
        direction: str,
    ) -> dict[str, list[tuple[str, str]]]:
        """Build adjacency list from graph."""
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
