from __future__ import annotations

"""
knowledge/tests/test_knowledge.py

Tests for Knowledge Layer.

Covers:
1. Graph creation
2. Node creation
3. Edge creation
4. Repository operations
5. Entity resolution
6. Identity resolution
7. Relationship resolution
8. Ontology loading
9. Traversal (BFS, DFS)
10. Path search
11. Neighborhood search
12. Query context
13. Graph queries
14. Validation
15. Knowledge events
16. Knowledge services
17. No AI imports
18. Architecture boundary validation
"""
import pytest
from datetime import datetime, timezone
from uuid import uuid4

from knowledge.graph.models import (
    Graph, Node, Edge, Subgraph, GraphSnapshot,
    NodeType, RelationshipType,
)
from knowledge.graph.repository import (
    GraphRepository, EntityRepository,
    IdentityRepository, RelationshipRepository, EvidenceRepository,
)
from knowledge.resolution import (
    EntityResolutionEngine, EntityMatchType,
    IdentityResolutionEngine, IdentityMatchType,
    RelationshipResolutionEngine, RelationshipMatchType,
    DeduplicationEngine,
)
from knowledge.ontology import OntologyLoader, OntologyMapper, OntologyValidator
from knowledge.graph.traversal import (
    BFSTraversal, DFSTraversal, PathSearch, NeighborhoodSearch,
)
from knowledge.graph.queries import QueryContext, Pagination, Filters
from knowledge.graph.queries import EntityQueries, GraphQueries
from knowledge.graph.validation import (
    GraphValidator, EntityValidator, ConsistencyValidator,
)
from knowledge.events import (
    KnowledgeEventEmitter, KnowledgeEvent,
    GraphEventType, ResolutionEventType,
)
from knowledge.services import (
    KnowledgeGraphService, EntityResolutionService,
    IdentityResolutionService, RelationshipResolutionService,
    OntologyService,
)


class TestGraphModels:
    """Test graph models."""

    def test_graph_creation(self):
        """Test Graph creation."""
        graph = Graph()
        assert graph.graph_id is not None
        assert graph.graph_version == "1.0.0"
        assert graph.get_node_count() == 0
        assert graph.get_edge_count() == 0

    def test_node_creation(self):
        """Test Node creation."""
        node = Node(
            node_type=NodeType.ENTITY,
            identity_refs=["id-123"],
            attributes={"name": "Test"},
        )
        assert node.node_id is not None
        assert node.node_type == NodeType.ENTITY
        assert "id-123" in node.identity_refs

    def test_edge_creation(self):
        """Test Edge creation."""
        edge = Edge(
            source_node_id="node-1",
            target_node_id="node-2",
            relationship_type=RelationshipType.LINKED_TO,
        )
        assert edge.edge_id is not None
        assert edge.source_node_id == "node-1"
        assert edge.target_node_id == "node-2"
        assert edge.is_valid()

    def test_subgraph_creation(self):
        """Test Subgraph creation."""
        node = Node(node_type=NodeType.ENTITY)
        subgraph = Subgraph(nodes=[node])
        assert subgraph.get_node_count() == 1

    def test_graph_snapshot(self):
        """Test GraphSnapshot creation."""
        graph = Graph()
        node = Node(node_type=NodeType.ENTITY)
        graph.add_node(node)
        
        snapshot = GraphSnapshot.from_graph(graph)
        assert snapshot.graph_id == graph.graph_id
        assert snapshot.node_count == 1


class TestGraphRepository:
    """Test graph repository."""

    def test_create_and_get_graph(self):
        """Test graph creation and retrieval."""
        repo = GraphRepository()
        graph = Graph()
        repo.create(graph)
        
        retrieved = repo.get_by_id(graph.graph_id)
        assert retrieved is not None
        assert retrieved.graph_id == graph.graph_id

    def test_add_node_to_graph(self):
        """Test adding node to graph."""
        repo = GraphRepository()
        graph = Graph()
        repo.create(graph)
        
        node = Node(node_type=NodeType.ENTITY)
        repo.add_node(graph.graph_id, node)
        
        retrieved = repo.get_by_id(graph.graph_id)
        assert retrieved.get_node_count() == 1

    def test_add_edge_to_graph(self):
        """Test adding edge to graph."""
        repo = GraphRepository()
        graph = Graph()
        repo.create(graph)
        
        node1 = Node(node_type=NodeType.ENTITY)
        node2 = Node(node_type=NodeType.ENTITY)
        repo.add_node(graph.graph_id, node1)
        repo.add_node(graph.graph_id, node2)
        
        edge = Edge(
            source_node_id=node1.node_id,
            target_node_id=node2.node_id,
            relationship_type=RelationshipType.LINKED_TO,
        )
        repo.add_edge(graph.graph_id, edge)
        
        retrieved = repo.get_by_id(graph.graph_id)
        assert retrieved.get_edge_count() == 1


class TestEntityResolution:
    """Test entity resolution."""

    def test_exact_match(self):
        """Test exact identifier matching."""
        engine = EntityResolutionEngine()
        
        result = engine.match_identifiers(
            ["id-123"],
            ["id-123"],
        )
        
        assert result.is_match
        assert result.match_type == EntityMatchType.EXACT

    def test_normalized_match(self):
        """Test normalized matching."""
        engine = EntityResolutionEngine(case_sensitive=False)
        
        result = engine.match_normalized("Test Value", "test value")
        
        assert result.is_match
        assert result.match_type == EntityMatchType.NORMALIZED

    def test_attribute_match(self):
        """Test attribute matching."""
        engine = EntityResolutionEngine()
        
        result = engine.match_attributes(
            {"name": "Test", "type": "A"},
            {"name": "Test", "type": "A"},
        )
        
        assert result.is_match

    def test_no_match(self):
        """Test non-matching entities."""
        engine = EntityResolutionEngine()
        
        result = engine.match_identifiers(
            ["id-123"],
            ["id-456"],
        )
        
        assert not result.is_match


class TestIdentityResolution:
    """Test identity resolution."""

    def test_exact_identity_match(self):
        """Test exact identity matching."""
        engine = IdentityResolutionEngine()
        
        result = engine.match_exact("value-123", "value-123")
        
        assert result.is_match
        assert result.match_type == IdentityMatchType.EXACT

    def test_normalized_identity_match(self):
        """Test normalized identity matching."""
        engine = IdentityResolutionEngine(case_sensitive=False)
        
        result = engine.match_normalized("Test", "test")
        
        assert result.is_match


class TestRelationshipResolution:
    """Test relationship resolution."""

    def test_exact_relationship_match(self):
        """Test exact relationship matching."""
        engine = RelationshipResolutionEngine()
        
        result = engine.match_exact(
            "entity-1", "entity-2", "related_to",
            "entity-1", "entity-2", "related_to",
        )
        
        assert result.is_match
        assert result.match_type == RelationshipMatchType.EXACT

    def test_symmetric_relationship(self):
        """Test symmetric relationship matching."""
        engine = RelationshipResolutionEngine(
            symmetric_relationships={"related_to"},
        )
        
        result = engine.match_symmetric(
            "entity-1", "entity-2", "related_to",
            "entity-2", "entity-1", "related_to",
        )
        
        assert result.is_match


class TestTraversal:
    """Test graph traversal."""

    def test_bfs_traversal(self):
        """Test BFS traversal."""
        graph = Graph()
        node1 = Node(node_type=NodeType.ENTITY)
        node2 = Node(node_type=NodeType.ENTITY)
        node3 = Node(node_type=NodeType.ENTITY)
        
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_node(node3)
        
        edge1 = Edge(
            source_node_id=node1.node_id,
            target_node_id=node2.node_id,
            relationship_type=RelationshipType.LINKED_TO,
        )
        edge2 = Edge(
            source_node_id=node2.node_id,
            target_node_id=node3.node_id,
            relationship_type=RelationshipType.LINKED_TO,
        )
        
        graph.add_edge(edge1)
        graph.add_edge(edge2)
        
        traversal = BFSTraversal(graph)
        result = traversal.traverse(node1.node_id)
        
        assert node1.node_id in result.visited_nodes
        assert node2.node_id in result.visited_nodes
        assert node3.node_id in result.visited_nodes

    def test_dfs_traversal(self):
        """Test DFS traversal."""
        graph = Graph()
        node1 = Node(node_type=NodeType.ENTITY)
        node2 = Node(node_type=NodeType.ENTITY)
        
        graph.add_node(node1)
        graph.add_node(node2)
        
        edge = Edge(
            source_node_id=node1.node_id,
            target_node_id=node2.node_id,
            relationship_type=RelationshipType.LINKED_TO,
        )
        graph.add_edge(edge)
        
        traversal = DFSTraversal(graph)
        result = traversal.traverse(node1.node_id)
        
        assert node1.node_id in result.visited_nodes
        assert node2.node_id in result.visited_nodes

    def test_shortest_path(self):
        """Test shortest path search."""
        graph = Graph()
        node1 = Node(node_type=NodeType.ENTITY)
        node2 = Node(node_type=NodeType.ENTITY)
        node3 = Node(node_type=NodeType.ENTITY)
        
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_node(node3)
        
        edge1 = Edge(
            source_node_id=node1.node_id,
            target_node_id=node2.node_id,
            relationship_type=RelationshipType.LINKED_TO,
        )
        edge2 = Edge(
            source_node_id=node2.node_id,
            target_node_id=node3.node_id,
            relationship_type=RelationshipType.LINKED_TO,
        )
        
        graph.add_edge(edge1)
        graph.add_edge(edge2)
        
        search = PathSearch(graph)
        result = search.find_shortest_path(node1.node_id, node3.node_id)
        
        assert result.found
        assert len(result.path) == 3


class TestQueries:
    """Test query operations."""

    def test_query_context(self):
        """Test QueryContext creation."""
        context = QueryContext.create(
            trace_id="trace-123",
            correlation_id="corr-456",
        )
        
        assert context.trace_id == "trace-123"
        assert context.correlation_id == "corr-456"

    def test_pagination(self):
        """Test Pagination."""
        pagination = Pagination(offset=0, limit=10)
        items = list(range(20))
        
        result = pagination.apply(items)
        
        assert len(result) == 10
        assert result[0] == 0

    def test_graph_stats(self):
        """Test graph statistics."""
        graph = Graph()
        node = Node(node_type=NodeType.ENTITY)
        graph.add_node(node)
        
        queries = GraphQueries(graph)
        stats = queries.get_stats()
        
        assert stats["node_count"] == 1
        assert stats["edge_count"] == 0


class TestValidation:
    """Test validation operations."""

    def test_graph_validator(self):
        """Test graph validation."""
        graph = Graph()
        node = Node(node_type=NodeType.ENTITY)
        graph.add_node(node)
        
        validator = GraphValidator(graph)
        result = validator.validate()
        
        assert result.is_valid

    def test_entity_validator(self):
        """Test entity validation."""
        graph = Graph()
        node = Node(node_type=NodeType.ENTITY)
        graph.add_node(node)
        
        validator = EntityValidator(graph)
        result = validator.validate(node.node_id)
        
        assert result.is_valid

    def test_consistency_validator(self):
        """Test consistency validation."""
        graph = Graph()
        node = Node(node_type=NodeType.ENTITY)
        graph.add_node(node)
        
        validator = ConsistencyValidator(graph)
        result = validator.validate()
        
        assert result.is_valid


class TestEvents:
    """Test knowledge events."""

    def test_event_emitter_without_bus(self):
        """Test event emitter without Event Bus."""
        emitter = KnowledgeEventEmitter()
        
        result = emitter.emit_node_created("node-123", "entity")
        
        assert result is False
        assert emitter.get_event_count() == 1

    def test_event_types(self):
        """Test event type definitions."""
        assert GraphEventType.NODE_CREATED.value == "knowledge.node.created"
        assert ResolutionEventType.ENTITY_RESOLVED.value == "knowledge.entity.resolved"


class TestServices:
    """Test knowledge services."""

    def test_knowledge_graph_service(self):
        """Test Knowledge Graph Service."""
        service = KnowledgeGraphService()
        
        graph = Graph()
        service.create_graph(graph)
        
        retrieved = service.get_graph(graph.graph_id)
        assert retrieved is not None

    def test_entity_resolution_service(self):
        """Test Entity Resolution Service."""
        service = EntityResolutionService()
        
        result = service.match_entities(
            {"identifiers": ["1"], "name": "Test"},
            {"identifiers": ["1"], "name": "Test"},
        )
        
        assert result.is_match

    def test_identity_resolution_service(self):
        """Test Identity Resolution Service."""
        service = IdentityResolutionService()
        
        result = service.match_identities(
            {"type": "email", "value": "test@example.com"},
            {"type": "email", "value": "test@example.com"},
        )
        
        assert result.is_match

    def test_relationship_resolution_service(self):
        """Test Relationship Resolution Service."""
        service = RelationshipResolutionService()
        
        result = service.match_relationships(
            "entity-1", "entity-2", "related_to",
            "entity-1", "entity-2", "related_to",
        )
        
        assert result.is_match

    def test_ontology_service(self):
        """Test Ontology Service."""
        service = OntologyService()
        
        ontology = service.load_ontology()
        
        assert "entities" in ontology
        assert "relationships" in ontology


class TestArchitectureConstraints:
    """Test architecture constraints."""

    def test_no_ai_imports(self):
        """Verify no AI imports."""
        from pathlib import Path
        
        knowledge_dir = Path(__file__).parent.parent
        for py_file in knowledge_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            lower_content = content.lower()
            assert "openai" not in lower_content
            assert "anthropic" not in lower_content
            assert "llm" not in lower_content

    def test_no_connector_imports(self):
        """Verify no connector imports."""
        from pathlib import Path
        
        knowledge_dir = Path(__file__).parent.parent
        for py_file in knowledge_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from connectors" not in content
            assert "import connectors" not in content

    def test_no_infrastructure_imports(self):
        """Verify no infrastructure imports."""
        from pathlib import Path
        
        knowledge_dir = Path(__file__).parent.parent
        for py_file in knowledge_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            content = py_file.read_text()
            assert "from infrastructure" not in content
            assert "import infrastructure" not in content
