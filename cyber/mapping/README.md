# Cyber Knowledge Mapping

## Phase 6B

This is the **Cyber Knowledge Mapping** layer - Phase 6B of the FOOL Platform architecture.

## IMPORTANT: What This IS

This phase implements **semantic mappings** that:

✅ Maps cyber domain entities to knowledge graph entities  
✅ Creates ontology bindings between cyber and knowledge concepts  
✅ Maintains mapping registry  
✅ Provides validation  
✅ Emits events  

## IMPORTANT: What This Is NOT

This phase does **NOT** implement:

- ❌ Detection
- ❌ Correlation
- ❌ Threat Intelligence
- ❌ Threat Hunting
- ❌ Investigation
- ❌ AI/LLM
- ❌ Graph Inference
- ❌ Risk Scoring
- ❌ ATT&CK Mapping Logic
- ❌ STIX Import
- ❌ Sigma Execution
- ❌ YARA Execution
- ❌ Rule Evaluation

**Mappings only. Analysis begins in Phase 6C.**

## Architecture Position

```
Standards
    ↓
Contracts
    ↓
Domain
    ↓
Knowledge Graph
    ↓
Inference
    ↓
Cyber Domain
    ↓
Cyber Knowledge Mapping   ← THIS PHASE
    ↓
Detection & Correlation   ← Phase 6C
    ↓
Threat Intelligence
    ↓
AI Augmentation
    ↓
Applications
```

## Key Principles

1. **Mappings only** - Create semantic bindings, not intelligence
2. **No analysis** - Do not analyze cyber concepts
3. **Deterministic** - All mappings are deterministic
4. **Observable** - Events for all operations
5. **Reusable** - Mapping infrastructure is reusable

## Dependency Rules

Cyber Knowledge Mapping may depend on:

- ✅ standards
- ✅ contracts
- ✅ domain
- ✅ knowledge
- ✅ cyber/domain
- ✅ platform/events
- ✅ Python Standard Library

Cyber Knowledge Mapping MUST NOT depend on:

- ❌ intelligence runtime
- ❌ AI/LLM
- ❌ applications
- ❌ connectors
- ❌ processing
- ❌ external feeds
- ❌ STIX parsers
- ❌ databases

## Components

### Models (`cyber/mapping/models.py`)

| Model | Purpose |
|-------|---------|
| `CyberKnowledgeMapping` | Complete mapping |
| `EntityMapping` | Entity to entity mapping |
| `RelationshipMapping` | Relationship mapping |
| `OntologyBinding` | Ontology binding |
| `KnowledgeReference` | Knowledge graph reference |
| `MappingMetadata` | Mapping metadata |

### Mappers

| Mapper | Purpose |
|--------|---------|
| `BaseEntityMapper` | Base entity mapper |
| `IndicatorMapper` | Maps indicators |
| `ObservableMapper` | Maps observables |
| `ThreatActorMapper` | Maps threat actors |
| `MalwareMapper` | Maps malware |
| `InfrastructureMapper` | Maps infrastructure |
| `TechniqueMapper` | Maps techniques |
| `VulnerabilityMapper` | Maps vulnerabilities |
| `ToolMapper` | Maps tools |
| `RelationshipMapperRegistry` | Maps relationships |

### Ontology (`cyber/mapping/ontology_mapper.py`)

| Component | Purpose |
|-----------|---------|
| `CyberOntologyMapper` | Maps concepts to ontology |
| `OntologyBindingRegistry` | Maintains bindings |
| `OntologyBindingValidator` | Validates bindings |

### Registry (`cyber/mapping/registry.py`)

| Method | Purpose |
|--------|---------|
| `register()` | Register a mapping |
| `get()` | Get mapping by ID |
| `find_by_entity_id()` | Find by entity ID |
| `list_all()` | List all mappings |
| `count()` | Count mappings |

### Validation (`cyber/mapping/validation.py`)

| Validator | Purpose |
|-----------|---------|
| `OntologyConsistencyValidator` | Validates ontology |
| `EntityConsistencyValidator` | Validates entities |
| `RelationshipConsistencyValidator` | Validates relationships |
| `MappingCompletenessValidator` | Validates completeness |
| `DuplicateMappingValidator` | Detects duplicates |

### Events (`cyber/mapping/events.py`)

| Event | Description |
|-------|-------------|
| `cyber.mapping.created` | Mapping created |
| `cyber.mapping.updated` | Mapping updated |
| `cyber.mapping.validated` | Mapping validated |
| `cyber.ontology.bound` | Ontology bound |

### Services (`cyber/mapping/services.py`)

| Service | Purpose |
|---------|---------|
| `CyberMappingService` | Coordinates entity mapping |
| `OntologyBindingService` | Coordinates ontology binding |
| `MappingValidationService` | Coordinates validation |

## Usage

```python
from cyber.mapping import CyberKnowledgeMapper, CyberEntityType

# Create mapper
mapper = CyberKnowledgeMapper()

# Map an entity
result = mapper.map_entity(
    CyberEntityType.INDICATOR,
    "ind-123",
    {"type": "ipv4", "value": "1.2.3.4"},
)

if result.success:
    mapping = result.mapping
    print(f"Mapped: {mapping.mapping_id}")

# Map a relationship
result = mapper.map_relationship(
    "threat_actor",
    "malware",
    "uses",
)

# Bind concept to ontology
bindings = mapper.bind_concept("indicator")

# Validate mapping
validation = mapper.validate_mapping(mapping)
if validation.is_valid:
    print("Mapping is valid")
```

## Lifecycle

```
Cyber Entity → Mapper → Entity Mapping
                         ↓
                    Ontology Binding
                         ↓
                    Validation
                         ↓
                    Registry
```

## Next Phase

**Phase 6C — Detection & Correlation Foundation**

This will implement:
- Threat detection
- Event correlation
- Alert generation
- Basic threat hunting
