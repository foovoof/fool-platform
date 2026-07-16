# Cyber Knowledge Mapping Architecture

## Overview

Cyber Knowledge Mapping integrates the Cyber Domain Foundation with the existing Knowledge Graph Foundation. It creates semantic mappings between cyber domain concepts and canonical knowledge graph entities.

### Key Responsibilities

1. **Entity Mapping** - Map cyber entities to knowledge entities
2. **Relationship Mapping** - Map cyber relationships to knowledge relationships
3. **Ontology Binding** - Create semantic bindings between concepts
4. **Validation** - Validate mappings for consistency
5. **Registry** - Maintain mapping registry

### What Cyber Knowledge Mapping Does NOT Do

- ❌ Detection
- ❌ Correlation
- ❌ Threat Intelligence
- ❌ Threat Hunting
- ❌ Attribution
- ❌ IOC Correlation
- ❌ Graph Inference
- ❌ Risk Assessment
- ❌ AI/LLM
- ❌ ATT&CK Mapping Logic
- ❌ STIX Import
- ❌ Sigma Execution
- ❌ YARA Execution

## Architecture Position

```
┌─────────────────────────────────────────────────────────────┐
│                    FOOL Platform                            │
├─────────────────────────────────────────────────────────────┤
│  Standards                                                 │
│      ↓                                                     │
│  Contracts                                                 │
│      ↓                                                     │
│  Domain                                                    │
│      ↓                                                     │
│  Knowledge Graph                                           │
│      ↓                                                     │
│  Inference                                                 │
│      ↓                                                     │
│  Cyber Domain                                              │
│      ↓                                                     │
│  CYBER KNOWLEDGE MAPPING ← THIS LAYER                     │
│      ↓                                                     │
│  Detection & Correlation                                    │
│      ↓                                                     │
│  Threat Intelligence                                        │
│      ↓                                                     │
│  AI Augmentation                                           │
│      ↓                                                     │
│  Applications                                              │
└─────────────────────────────────────────────────────────────┘
```

## Dependency Rules

### Allowed Dependencies

Cyber Knowledge Mapping may depend on:

- ✅ `standards` - Standards definitions
- ✅ `contracts` - Domain contracts
- ✅ `domain` - Domain models
- ✅ `knowledge` - Knowledge graph
- ✅ `cyber/domain` - Cyber domain concepts
- ✅ `platform/events` - Event bus
- ✅ `python standard library` - Standard library only

### Forbidden Dependencies

Cyber Knowledge Mapping MUST NOT depend on:

- ❌ `intelligence` - Intelligence runtime
- ❌ `ai` - AI/ML components
- ❌ `applications` - Application layer
- ❌ `connectors` - Data connectors
- ❌ `processing` - Data processing
- ❌ `external feeds` - External data feeds
- ❌ `stix parsers` - STIX parsing
- ❌ `databases` - Database connections

## Mapping Models

### CyberKnowledgeMapping

Complete mapping of a cyber entity to knowledge graph.

```python
@dataclass(frozen=True)
class CyberKnowledgeMapping:
    mapping_id: str
    entity_mapping: EntityMapping | None
    relationship_mappings: tuple[RelationshipMapping, ...]
    ontology_bindings: tuple[OntologyBinding, ...]
    status: MappingStatus
    metadata: MappingMetadata
```

### EntityMapping

Mapping of a cyber entity to a knowledge entity.

```python
@dataclass(frozen=True)
class EntityMapping:
    mapping_id: str
    source_entity_type: str
    source_entity_id: str
    source_attributes: tuple[str, ...]
    target_knowledge: KnowledgeReference
    ontology_bindings: tuple[OntologyBinding, ...]
    status: MappingStatus
```

### RelationshipMapping

Mapping of cyber relationships to knowledge relationships.

```python
@dataclass(frozen=True)
class RelationshipMapping:
    mapping_id: str
    source_relationship_type: str
    source_entity_a_type: str
    source_entity_b_type: str
    target_relationship_type: str
    target_knowledge: KnowledgeReference
```

### OntologyBinding

Binding between cyber and knowledge ontology concepts.

```python
@dataclass(frozen=True)
class OntologyBinding:
    binding_id: str
    cyber_concept: str
    knowledge_concept: str
    cyber_namespace: str
    knowledge_namespace: str
    mapping_type: MappingType
```

## Entity Mappers

### Supported Entity Types

| Entity Type | Mapper | Knowledge Type |
|-------------|--------|----------------|
| `indicator` | IndicatorMapper | Indicator |
| `observable` | ObservableMapper | Observable |
| `threat_actor` | ThreatActorMapper | Actor |
| `malware` | MalwareMapper | Malware |
| `infrastructure` | InfrastructureMapper | Infrastructure |
| `technique` | TechniqueMapper | Technique |
| `vulnerability` | VulnerabilityMapper | Vulnerability |
| `tool` | ToolMapper | Tool |

### Example

```python
mapper = IndicatorMapper()
result = mapper.map("ind-1", {"type": "ipv4", "value": "1.2.3.4"})

assert result.entity_mapping.source_entity_type == "indicator"
assert result.entity_mapping.target_knowledge.entity_type == "Indicator"
```

## Relationship Mappers

### Supported Relationships

| Source | Target | Relationship |
|--------|--------|--------------|
| threat_actor | malware | uses_malware |
| threat_actor | infrastructure | uses_infrastructure |
| malware | technique | uses_technique |
| indicator | observable | based_on |

### Example

```python
mapper = ThreatActorMalwareMapper()
result = mapper.map("threat_actor", "malware", "uses")

assert result.relationship_mapping.target_relationship_type == "uses_malware"
```

## Ontology Mapper

Maps cyber concepts to knowledge ontology concepts.

```python
mapper = CyberOntologyMapper()
result = mapper.map_concept("indicator")

# Returns bindings:
# - indicator → Indicator
# - indicator → Observable
# - indicator → IOC
```

## Registry

Maintains mapping registry.

```python
registry = MappingRegistry()

# Register
registry.register(mapping)

# Lookup
retrieved = registry.get(mapping.mapping_id)

# Find by entity
results = registry.find_by_entity_id("ind-123")
```

## Validation

### Validators

| Validator | Purpose |
|-----------|---------|
| `OntologyConsistencyValidator` | Validates ontology bindings |
| `EntityConsistencyValidator` | Validates entity mappings |
| `RelationshipConsistencyValidator` | Validates relationships |
| `MappingCompletenessValidator` | Validates completeness |
| `DuplicateMappingValidator` | Detects duplicates |

### Example

```python
validator = MappingValidator()
result = validator.validate(mapping)

if not result.is_valid:
    for issue in result.issues:
        print(f"{issue.severity}: {issue.message}")
```

## Events

Emits optional events via platform/events.

| Event | Description |
|-------|-------------|
| `cyber.mapping.created` | Mapping created |
| `cyber.mapping.updated` | Mapping updated |
| `cyber.mapping.validated` | Mapping validated |
| `cyber.ontology.bound` | Ontology bound |

## Services

### CyberMappingService

```python
service = CyberMappingService()

result = service.map_entity(
    CyberEntityType.INDICATOR,
    "ind-123",
    {"type": "ipv4", "value": "1.2.3.4"},
)
```

### OntologyBindingService

```python
service = OntologyBindingService()
bindings = service.bind_concept("indicator")
```

### MappingValidationService

```python
service = MappingValidationService()
result = service.validate_mapping(mapping)
```

## Usage Example

```python
from cyber.mapping import CyberKnowledgeMapper, CyberEntityType

# Create mapper
mapper = CyberKnowledgeMapper()

# Map entity
result = mapper.map_entity(
    CyberEntityType.MALWARE,
    "mal-1",
    {"name": "Emotet"},
)

if result.success:
    # Bind to ontology
    bindings = mapper.bind_concept("malware")
    
    # Validate
    validation = mapper.validate_mapping(result.mapping)
    
    if validation.is_valid:
        print("Ready for detection layer")
```

## Mapping Lifecycle

```
┌─────────────┐
│ Cyber Entity│
└──────┬──────┘
       │ map_entity()
       ↓
┌─────────────┐
│Entity Mapping│
└──────┬──────┘
       │ bind_concept()
       ↓
┌─────────────┐
│ Ontology   │
│ Bindings   │
└──────┬──────┘
       │ validate()
       ↓
┌─────────────┐
│ Validation  │
│ Result      │
└──────┬──────┘
       │ register()
       ↓
┌─────────────┐
│ Registry    │
└─────────────┘
```

## Phase 6C Introduction

**Phase 6C — Detection & Correlation Foundation** will implement:

- Threat detection rules
- Event correlation
- Alert generation
- Basic threat hunting
- SIEM integration

## Guiding Principle

> Map cyber concepts to knowledge. Do not analyze them. Create semantic consistency. Do not create intelligence.
