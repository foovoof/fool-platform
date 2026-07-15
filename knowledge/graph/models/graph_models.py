from __future__ import annotations

"""
knowledge/graph/models/graph_models.py

Core graph models for the Knowledge Layer.

These models represent:
- Graph: The knowledge graph container
- Node: Individual knowledge nodes
- Edge: Relationships between nodes
- Subgraph: A subset of the graph
- GraphSnapshot: Point-in-time snapshot of the graph
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class NodeType(Enum):
    """Enumeration of valid node types."""
    ENTITY = "entity"
    IDENTITY = "identity"
    EVIDENCE = "evidence"
    RELATIONSHIP = "relationship"
    CONCEPT = "concept"
    CLASSIFICATION = "classification"
    SOURCE = "source"
    OBSERVATION = "observation"
    ANNOTATION = "annotation"
    UNKNOWN = "unknown"


class RelationshipType(Enum):
    """Enumeration of valid relationship types."""
    IDENTIFIED_BY = "identified_by"
    LINKED_TO = "linked_to"
    RELATED_TO = "related_to"
    EVIDENCES = "evidences"
    SUPERSEDED_BY = "superseded_by"
    CONTAINS = "contains"
    PART_OF = "part_of"
    SIMILAR_TO = "similar_to"
    CONTRADICTS = "contradicts"
    DERIVED_FROM = "derived_from"
    REFERENCES = "references"
    UNKNOWN = "unknown"


@dataclass
class Node:
    """
    Represents a node in the knowledge graph.
    
    A node is the fundamental unit of knowledge representation.
    """
    node_id: str = field(default_factory=lambda: str(uuid4()))
    node_type: NodeType = NodeType.UNKNOWN
    identity_refs: list[str] = field(default_factory=list)
    entity_refs: list[str] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def add_identity_ref(self, identity_ref: str) -> None:
        """Add an identity reference to this node."""
        if identity_ref not in self.identity_refs:
            self.identity_refs.append(identity_ref)

    def add_entity_ref(self, entity_ref: str) -> None:
        """Add an entity reference to this node."""
        if entity_ref not in self.entity_refs:
            self.entity_refs.append(entity_ref)

    def get_attribute(self, key: str, default: Any = None) -> Any:
        """Get an attribute value."""
        return self.attributes.get(key, default)

    def set_attribute(self, key: str, value: Any) -> None:
        """Set an attribute value."""
        self.attributes[key] = value

    def has_identity(self, identity_ref: str) -> bool:
        """Check if this node has a specific identity reference."""
        return identity_ref in self.identity_refs

    def is_entity_type(self, entity_type: str) -> bool:
        """Check if this node represents a specific entity type."""
        return self.node_type.value == entity_type


@dataclass
class Edge:
    """
    Represents an edge (relationship) in the knowledge graph.
    
    An edge connects two nodes with a typed relationship.
    """
    edge_id: str = field(default_factory=lambda: str(uuid4()))
    source_node_id: str = ""
    target_node_id: str = ""
    relationship_type: RelationshipType = RelationshipType.UNKNOWN
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def is_valid(self) -> bool:
        """Check if this edge has valid source and target."""
        return bool(self.source_node_id and self.target_node_id)

    def references_node(self, node_id: str) -> bool:
        """Check if this edge references a specific node."""
        return self.source_node_id == node_id or self.target_node_id == node_id

    def is_self_loop(self) -> bool:
        """Check if this edge is a self-loop."""
        return self.source_node_id == self.target_node_id


@dataclass
class Graph:
    """
    Represents the knowledge graph container.
    
    The graph holds all nodes and edges for a knowledge domain.
    """
    graph_id: str = field(default_factory=lambda: str(uuid4()))
    graph_version: str = "1.0.0"
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __post_init__(self) -> None:
        """Initialize internal storage."""
        self._nodes: dict[str, Node] = {}
        self._edges: dict[str, Edge] = {}
        self._node_index: dict[str, list[str]] = {}  # node_type -> node_ids
        self._identity_index: dict[str, list[str]] = {}  # identity_ref -> node_ids
        self._edge_index: dict[tuple[str, str], list[str]] = {}  # (source, target) -> edge_ids

    def add_node(self, node: Node) -> None:
        """
        Add a node to the graph.
        
        Args:
            node: The node to add
        """
        self._nodes[node.node_id] = node
        
        # Update type index
        node_type = node.node_type.value
        if node_type not in self._node_index:
            self._node_index[node_type] = []
        if node.node_id not in self._node_index[node_type]:
            self._node_index[node_type].append(node.node_id)
        
        # Update identity index
        for identity_ref in node.identity_refs:
            if identity_ref not in self._identity_index:
                self._identity_index[identity_ref] = []
            if node.node_id not in self._identity_index[identity_ref]:
                self._identity_index[identity_ref].append(node.node_id)

    def add_edge(self, edge: Edge) -> None:
        """
        Add an edge to the graph.
        
        Args:
            edge: The edge to add
        """
        if not edge.is_valid():
            raise ValueError("Edge must have valid source and target node IDs")
        
        self._edges[edge.edge_id] = edge
        
        # Update edge index
        key = (edge.source_node_id, edge.target_node_id)
        if key not in self._edge_index:
            self._edge_index[key] = []
        if edge.edge_id not in self._edge_index[key]:
            self._edge_index[key].append(edge.edge_id)

    def get_node(self, node_id: str) -> Node | None:
        """Get a node by ID."""
        return self._nodes.get(node_id)

    def get_edge(self, edge_id: str) -> Edge | None:
        """Get an edge by ID."""
        return self._edges.get(edge_id)

    def remove_node(self, node_id: str) -> bool:
        """
        Remove a node and its associated edges.
        
        Returns:
            True if node was removed
        """
        if node_id not in self._nodes:
            return False
        
        node = self._nodes[node_id]
        
        # Remove from type index
        node_type = node.node_type.value
        if node_type in self._node_index:
            self._node_index[node_type] = [
                n for n in self._node_index[node_type] if n != node_id
            ]
        
        # Remove from identity index
        for identity_ref in node.identity_refs:
            if identity_ref in self._identity_index:
                self._identity_index[identity_ref] = [
                    n for n in self._identity_index[identity_ref] if n != node_id
                ]
        
        # Remove associated edges
        edges_to_remove = [
            e.edge_id for e in self._edges.values()
            if e.references_node(node_id)
        ]
        for edge_id in edges_to_remove:
            self.remove_edge(edge_id)
        
        # Remove node
        del self._nodes[node_id]
        return True

    def remove_edge(self, edge_id: str) -> bool:
        """
        Remove an edge from the graph.
        
        Returns:
            True if edge was removed
        """
        if edge_id not in self._edges:
            return False
        
        edge = self._edges[edge_id]
        
        # Remove from index
        key = (edge.source_node_id, edge.target_node_id)
        if key in self._edge_index:
            self._edge_index[key] = [
                e for e in self._edge_index[key] if e != edge_id
            ]
        
        del self._edges[edge_id]
        return True

    def get_nodes_by_type(self, node_type: NodeType) -> list[Node]:
        """Get all nodes of a specific type."""
        node_ids = self._node_index.get(node_type.value, [])
        return [self._nodes[nid] for nid in node_ids if nid in self._nodes]

    def get_nodes_by_identity(self, identity_ref: str) -> list[Node]:
        """Get all nodes with a specific identity reference."""
        node_ids = self._identity_index.get(identity_ref, [])
        return [self._nodes[nid] for nid in node_ids if nid in self._nodes]

    def get_edges_between(self, source_id: str, target_id: str) -> list[Edge]:
        """Get all edges between two nodes."""
        key = (source_id, target_id)
        edge_ids = self._edge_index.get(key, [])
        return [self._edges[eid] for eid in edge_ids if eid in self._edges]

    def get_node_count(self) -> int:
        """Get the number of nodes in the graph."""
        return len(self._nodes)

    def get_edge_count(self) -> int:
        """Get the number of edges in the graph."""
        return len(self._edges)

    def list_nodes(self) -> list[Node]:
        """Get all nodes in the graph."""
        return list(self._nodes.values())

    def list_edges(self) -> list[Edge]:
        """Get all edges in the graph."""
        return list(self._edges.values())


@dataclass
class Subgraph:
    """
    Represents a subset of the knowledge graph.
    
    A subgraph contains selected nodes and edges.
    """
    subgraph_id: str = field(default_factory=lambda: str(uuid4()))
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_node(self, node: Node) -> None:
        """Add a node to the subgraph."""
        if node not in self.nodes:
            self.nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the subgraph."""
        if edge not in self.edges:
            self.edges.append(edge)

    def get_node_count(self) -> int:
        """Get the number of nodes."""
        return len(self.nodes)

    def get_edge_count(self) -> int:
        """Get the number of edges."""
        return len(self.edges)

    def contains_node(self, node_id: str) -> bool:
        """Check if subgraph contains a specific node."""
        return any(n.node_id == node_id for n in self.nodes)

    def contains_edge(self, edge_id: str) -> bool:
        """Check if subgraph contains a specific edge."""
        return any(e.edge_id == edge_id for e in self.edges)


@dataclass
class GraphSnapshot:
    """
    Represents a point-in-time snapshot of the knowledge graph.
    
    Used for versioning and audit purposes.
    """
    snapshot_id: str = field(default_factory=lambda: str(uuid4()))
    graph_id: str = ""
    graph_version: str = "1.0.0"
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    node_count: int = 0
    edge_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_graph(cls, graph: Graph) -> "GraphSnapshot":
        """
        Create a snapshot from a graph.
        
        Args:
            graph: The graph to snapshot
            
        Returns:
            A new GraphSnapshot
        """
        return cls(
            graph_id=graph.graph_id,
            graph_version=graph.graph_version,
            node_count=graph.get_node_count(),
            edge_count=graph.get_edge_count(),
            metadata=graph.metadata.copy(),
        )
