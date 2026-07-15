# Knowledge Layer

The Knowledge Layer is the foundation for knowledge representation and management in FOOL Platform.

## Purpose

The Knowledge Layer transforms FOOL from an execution platform into a knowledge platform.

**Important**: This is Phase 3A. Inference and reasoning belong to Phase 3B.

## Architecture Position

```
FOOL Platform Architecture:

Standards ──► Contracts ──► Domain ──► Knowledge ──► Intelligence
                                               ↓
                                         Platform
                                               ↓
                                         Applications
```

## What Knowledge Layer Does

- Knowledge graph structures
- Knowledge repositories
- Ontology integration
- Entity resolution
- Identity resolution
- Relationship resolution
- Knowledge validation
- Knowledge querying
- Knowledge traversal
- Knowledge services
- Knowledge events

## What Knowledge Layer Does NOT Do

- ❌ Inference
- ❌ Reasoning
- ❌ AI
- ❌ LLMs
- ❌ Embeddings
- ❌ Vector Search
- ❌ Graph Databases
- ❌ Threat Intelligence
- ❌ Cyber Intelligence

## Knowledge Principles

1. Domain objects become knowledge objects
2. Knowledge graph owns relationships
3. Resolution precedes inference
4. Ontology governs semantics
5. Validation is mandatory
6. Knowledge must be explainable
7. Knowledge must be deterministic
8. Knowledge emits events
9. Knowledge remains storage-agnostic
10. Inference is forbidden in Phase 3A

## Directory Structure

```
knowledge/
├── graph/
│   ├── models/          # Graph models (Node, Edge, Graph, etc.)
│   ├── repository/      # Repository implementations
│   ├── traversal/        # BFS, DFS, path search
│   ├── queries/          # Query operations
│   └── validation/       # Graph validation
├── ontology/           # Ontology loading, mapping, validation
├── resolution/          # Entity, identity, relationship resolution
├── events/             # Knowledge events
├── services/           # Knowledge services
└── tests/              # Tests
```

## Graph Models

```python
from knowledge.graph.models import Graph, Node, Edge

graph = Graph()
node = Node(node_type=NodeType.ENTITY)
edge = Edge(
    source_node_id=node1.node_id,
    target_node_id=node2.node_id,
    relationship_type=RelationshipType.LINKED_TO,
)
```

## Repository Pattern

```python
from knowledge.graph.repository import GraphRepository

repo = GraphRepository()
graph = Graph()
repo.create(graph)
repo.add_node(graph.graph_id, node)
repo.add_edge(graph.graph_id, edge)
```

## Resolution Engines

```python
from knowledge.resolution import EntityResolutionEngine

engine = EntityResolutionEngine()
result = engine.match(source_entity, target_entity)
```

## Traversal

```python
from knowledge.graph.traversal import BFSTraversal, PathSearch

bfs = BFSTraversal(graph)
result = bfs.traverse(start_node_id)

path_search = PathSearch(graph)
result = path_search.find_shortest_path(source_id, target_id)
```

## Validation

```python
from knowledge.graph.validation import GraphValidator

validator = GraphValidator(graph)
result = validator.validate()
```

## Events

```python
from knowledge.events import KnowledgeEventEmitter

emitter = KnowledgeEventEmitter()
emitter.emit_node_created(node_id, node_type)
```

## Services

```python
from knowledge.services import KnowledgeGraphService

service = KnowledgeGraphService()
service.create_graph(graph)
```

## Phase 3A Scope

### Implemented

- ✅ Graph models (Graph, Node, Edge, Subgraph, GraphSnapshot)
- ✅ Repository foundation (in-memory)
- ✅ Entity resolution (deterministic)
- ✅ Identity resolution (deterministic)
- ✅ Relationship resolution (deterministic)
- ✅ Deduplication engine
- ✅ Ontology loader, mapper, validator
- ✅ BFS, DFS traversal
- ✅ Path search
- ✅ Neighborhood search
- ✅ Query context and operations
- ✅ Graph, entity, relationship validation
- ✅ Consistency validation
- ✅ Knowledge events
- ✅ Knowledge services

### NOT Implemented

- ❌ Inference
- ❌ Reasoning
- ❌ AI/LLM integration
- ❌ Graph databases (Neo4j, etc.)
- ❌ Vector search
- ❌ Persistence

## Next Phase

**Phase 3B — INFERENCE & REASONING FOUNDATION**

Phase 3B will implement inference and reasoning capabilities.
