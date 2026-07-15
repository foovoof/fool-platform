# Knowledge Layer Architecture

## Overview

The Knowledge Layer transforms FOOL Platform from an execution platform into a knowledge platform. This is Phase 3A implementation.

**Important**: Phase 3A does NOT implement intelligence. Intelligence belongs to Phase 3B.

## Architecture Position

```
FOOL Platform Architecture:

Standards ──► Contracts ──► Domain ──► Knowledge ──► Intelligence
                                               ↓
                                         Platform
                                               ↓
                                         Applications
```

## Dependency Rules

### Knowledge May Depend On

- ✅ standards/
- ✅ contracts/
- ✅ domain/
- ✅ platform/events interfaces
- ✅ Python standard library

### Knowledge Must NOT Depend On

- ❌ intelligence/
- ❌ ai/
- ❌ apps/
- ❌ connectors/
- ❌ infrastructure/
- ❌ graph databases
- ❌ external services
- ❌ external storage

### Domain Must NOT Import Knowledge

Domain objects become knowledge objects, but domain does not import knowledge.

## Graph Architecture

### Graph Belongs Entirely Inside Knowledge

Graph is NOT an architectural layer. Graph components exist under:

```
knowledge/graph/
├── models/
├── repository/
├── traversal/
├── queries/
├── validation/
└── services/
```

## Knowledge Components

### 1. Graph Models (knowledge/graph/models/)

| Model | Purpose |
|-------|---------|
| Graph | Knowledge graph container |
| Node | Knowledge entity |
| Edge | Knowledge relationship |
| Subgraph | Subset of graph |
| GraphSnapshot | Point-in-time snapshot |

### 2. Repository Layer (knowledge/graph/repository/)

| Repository | Purpose |
|------------|---------|
| GraphRepository | Graph storage |
| EntityRepository | Entity storage |
| IdentityRepository | Identity storage |
| RelationshipRepository | Relationship storage |
| EvidenceRepository | Evidence storage |

All repositories are in-memory only.

### 3. Resolution Layer (knowledge/resolution/)

| Engine | Purpose |
|--------|---------|
| EntityResolutionEngine | Deterministic entity matching |
| IdentityResolutionEngine | Deterministic identity matching |
| RelationshipResolutionEngine | Deterministic relationship matching |
| DeduplicationEngine | Duplicate detection |

### Resolution Rules

- Deterministic matching only
- No ML/AI similarity
- No embeddings
- No fuzzy matching
- No probabilistic scoring

### 4. Ontology Layer (knowledge/ontology/)

| Component | Purpose |
|-----------|---------|
| OntologyLoader | Load from standards/ |
| OntologyMapper | Map domain to ontology |
| OntologyValidator | Validate against ontology |

### 5. Traversal Layer (knowledge/graph/traversal/)

| Algorithm | Purpose |
|-----------|---------|
| BFSTraversal | Breadth-first search |
| DFSTraversal | Depth-first search |
| PathSearch | Shortest path, all paths |
| NeighborhoodSearch | Ego network, common neighbors |

### 6. Query Layer (knowledge/graph/queries/)

| Component | Purpose |
|-----------|---------|
| QueryContext | Query metadata |
| EntityQueries | Entity queries |
| IdentityQueries | Identity queries |
| RelationshipQueries | Relationship queries |
| GraphQueries | Graph statistics |

### 7. Validation Layer (knowledge/graph/validation/)

| Validator | Purpose |
|-----------|---------|
| GraphValidator | Graph structure |
| EntityValidator | Entity integrity |
| IdentityValidator | Identity consistency |
| RelationshipValidator | Relationship integrity |
| ConsistencyValidator | Overall consistency |

### 8. Events (knowledge/events/)

| Category | Events |
|----------|--------|
| Graph | node.created, node.updated, node.removed, edge.created, edge.updated, edge.removed, graph.validated |
| Resolution | entity.resolved, identity.merged, relationship.created, relationship.validated |

### 9. Services (knowledge/services/)

| Service | Purpose |
|---------|---------|
| KnowledgeGraphService | Graph orchestration |
| EntityResolutionService | Entity resolution orchestration |
| IdentityResolutionService | Identity resolution orchestration |
| RelationshipResolutionService | Relationship resolution orchestration |
| OntologyService | Ontology operations |

## State Machines

### Node Lifecycle

```
CREATED → INITIALIZED → VALIDATED → ACTIVE
                    ↓
                DELETED
```

### Relationship Lifecycle

```
CREATED → VALIDATED → ACTIVE
                  ↓
              DELETED
```

## Data Flow

```
Domain Object
    ↓
Ontology Mapping
    ↓
Entity Resolution (optional)
    ↓
Graph Storage
    ↓
Validation
    ↓
Query/Traversal
    ↓
Knowledge Service
    ↓
Event Emission
```

## Storage Rules

- In-memory only
- No databases
- No graph databases (Neo4j, ArangoDB, etc.)
- No persistence
- Repository abstraction hides storage

## Validation Rules

- Validation is mandatory
- Results are explainable
- No silent fixes
- All errors documented

## Event Rules

- Uses platform/events
- Event failures do not fail operations
- Event integration is optional

## Phase 3B Preview

Phase 3B will add:

- Inference engine
- Reasoning engine
- Rule-based reasoning
- Path-based reasoning
- ML-based inference (optional)
- Knowledge graph embeddings (optional)

Phase 3A remains foundational for Phase 3B.

## Testing

Run tests:

```bash
pytest knowledge/tests/
```

## Architecture Tests

See `testing/architecture/test_python_first_architecture.py` for:

- Knowledge layer existence
- Module structure
- Purity checks (no AI, connectors, infrastructure)
- Domain does not import knowledge
