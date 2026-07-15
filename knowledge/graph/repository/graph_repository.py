"""
knowledge/graph/repository/graph_repository.py

Graph repository implementation.

In-memory storage for knowledge graphs.
"""
from __future__ import annotations

from typing import Any

from knowledge.graph.models import Graph, Node, Edge, Subgraph, GraphSnapshot
from knowledge.graph.repository.base import KnowledgeRepository


class GraphRepository(KnowledgeRepository[Graph]):
    """
    In-memory repository for knowledge graphs.
    
    Provides storage for Graph objects.
    """

    def __init__(self) -> None:
        """Initialize the repository."""
        self._graphs: dict[str, Graph] = {}
        self._snapshots: dict[str, list[GraphSnapshot]] = {}

    def create(self, graph: Graph) -> Graph:
        """
        Create a new graph.
        
        Args:
            graph: The graph to create
            
        Returns:
            The created graph
        """
        if graph.graph_id in self._graphs:
            raise ValueError(f"Graph {graph.graph_id} already exists")
        self._graphs[graph.graph_id] = graph
        self._snapshots[graph.graph_id] = []
        return graph

    def update(self, graph: Graph) -> Graph:
        """
        Update an existing graph.
        
        Args:
            graph: The graph to update
            
        Returns:
            The updated graph
        """
        if graph.graph_id not in self._graphs:
            raise ValueError(f"Graph {graph.graph_id} not found")
        self._graphs[graph.graph_id] = graph
        return graph

    def delete(self, graph_id: str) -> bool:
        """
        Delete a graph by ID.
        
        Args:
            graph_id: The ID of the graph to delete
            
        Returns:
            True if deleted
        """
        if graph_id in self._graphs:
            del self._graphs[graph_id]
            if graph_id in self._snapshots:
                del self._snapshots[graph_id]
            return True
        return False

    def get_by_id(self, graph_id: str) -> Graph | None:
        """
        Get a graph by ID.
        
        Args:
            graph_id: The graph ID
            
        Returns:
            The graph or None
        """
        return self._graphs.get(graph_id)

    def list(self, **kwargs: Any) -> list[Graph]:
        """
        List all graphs.
        
        Args:
            **kwargs: Ignored for now
            
        Returns:
            List of all graphs
        """
        return list(self._graphs.values())

    def search(self, query: str, **kwargs: Any) -> list[Graph]:
        """
        Search graphs by metadata.
        
        Args:
            query: Search query (matches against graph_id)
            **kwargs: Ignored
            
        Returns:
            Matching graphs
        """
        return [
            g for g in self._graphs.values()
            if query.lower() in g.graph_id.lower()
        ]

    def exists(self, graph_id: str) -> bool:
        """Check if a graph exists."""
        return graph_id in self._graphs

    def count(self, **kwargs: Any) -> int:
        """Get the number of graphs."""
        return len(self._graphs)

    def clear(self) -> None:
        """Clear all graphs."""
        self._graphs.clear()
        self._snapshots.clear()

    def create_snapshot(self, graph_id: str) -> GraphSnapshot | None:
        """
        Create a snapshot of a graph.
        
        Args:
            graph_id: The graph ID
            
        Returns:
            The created snapshot or None if graph not found
        """
        graph = self._graphs.get(graph_id)
        if not graph:
            return None
        
        snapshot = GraphSnapshot.from_graph(graph)
        self._snapshots[graph_id].append(snapshot)
        return snapshot

    def get_snapshots(self, graph_id: str) -> list[GraphSnapshot]:
        """
        Get all snapshots for a graph.
        
        Args:
            graph_id: The graph ID
            
        Returns:
            List of snapshots
        """
        return self._snapshots.get(graph_id, []).copy()

    def add_node(self, graph_id: str, node: Node) -> bool:
        """
        Add a node to a graph.
        
        Args:
            graph_id: The graph ID
            node: The node to add
            
        Returns:
            True if added
        """
        graph = self._graphs.get(graph_id)
        if not graph:
            return False
        graph.add_node(node)
        return True

    def add_edge(self, graph_id: str, edge: Edge) -> bool:
        """
        Add an edge to a graph.
        
        Args:
            graph_id: The graph ID
            edge: The edge to add
            
        Returns:
            True if added
        """
        graph = self._graphs.get(graph_id)
        if not graph:
            return False
        try:
            graph.add_edge(edge)
            return True
        except ValueError:
            return False

    def get_node(self, graph_id: str, node_id: str) -> Node | None:
        """
        Get a node from a graph.
        
        Args:
            graph_id: The graph ID
            node_id: The node ID
            
        Returns:
            The node or None
        """
        graph = self._graphs.get(graph_id)
        if not graph:
            return None
        return graph.get_node(node_id)

    def get_edge(self, graph_id: str, edge_id: str) -> Edge | None:
        """
        Get an edge from a graph.
        
        Args:
            graph_id: The graph ID
            edge_id: The edge ID
            
        Returns:
            The edge or None
        """
        graph = self._graphs.get(graph_id)
        if not graph:
            return None
        return graph.get_edge(edge_id)

    def extract_subgraph(
        self,
        graph_id: str,
        node_ids: list[str],
    ) -> Subgraph | None:
        """
        Extract a subgraph containing specified nodes.
        
        Args:
            graph_id: The graph ID
            node_ids: IDs of nodes to include
            
        Returns:
            The subgraph or None if graph not found
        """
        graph = self._graphs.get(graph_id)
        if not graph:
            return None
        
        nodes = [graph.get_node(nid) for nid in node_ids]
        nodes = [n for n in nodes if n is not None]
        
        edges = []
        for node in nodes:
            for edge in graph.list_edges():
                if edge.source_node_id == node.node_id:
                    if edge.target_node_id in node_ids:
                        edges.append(edge)
                elif edge.target_node_id == node.node_id:
                    if edge.source_node_id in node_ids:
                        edges.append(edge)
        
        return Subgraph(nodes=nodes, edges=edges)
