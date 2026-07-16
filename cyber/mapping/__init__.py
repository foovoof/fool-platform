"""
cyber/mapping/__init__.py

FOOL Platform Cyber Knowledge Mapping.

IMPORTANT: This module creates semantic mappings only.
It does NOT implement:
- Detection
- Correlation
- Threat Intelligence
- Investigation
- AI/LLM
- Graph Inference
- Risk Scoring
"""
from cyber.mapping.models import (
    MappingType,
    MappingStatus,
    MappingMetadata,
    KnowledgeReference,
    OntologyBinding,
    EntityMapping,
    RelationshipMapping,
    CyberKnowledgeMapping,
    MappingResult,
    ValidationIssue,
    ValidationResult,
    CyberEntityType,
)
from cyber.mapping.mapper import CyberKnowledgeMapper
from cyber.mapping.entity_mapper import (
    BaseEntityMapper,
    EntityMapperRegistry,
)
from cyber.mapping.relationship_mapper import (
    BaseRelationshipMapper,
    RelationshipMapperRegistry,
)
from cyber.mapping.ontology_mapper import (
    CyberOntologyMapper,
    OntologyBindingRegistry,
    OntologyBindingValidator,
)
from cyber.mapping.registry import MappingRegistry
from cyber.mapping.validation import MappingValidator
from cyber.mapping.events import (
    MappingEventEmitter,
    MappingEventType,
    MappingEvent,
)
from cyber.mapping.services import (
    CyberMappingService,
    OntologyBindingService,
    MappingValidationService,
)


__all__ = [
    # Models
    "MappingType",
    "MappingStatus",
    "MappingMetadata",
    "KnowledgeReference",
    "OntologyBinding",
    "EntityMapping",
    "RelationshipMapping",
    "CyberKnowledgeMapping",
    "MappingResult",
    "ValidationIssue",
    "ValidationResult",
    "CyberEntityType",
    # Mapper
    "CyberKnowledgeMapper",
    # Entity Mapper
    "BaseEntityMapper",
    "EntityMapperRegistry",
    # Relationship Mapper
    "BaseRelationshipMapper",
    "RelationshipMapperRegistry",
    # Ontology Mapper
    "CyberOntologyMapper",
    "OntologyBindingRegistry",
    "OntologyBindingValidator",
    # Registry
    "MappingRegistry",
    # Validation
    "MappingValidator",
    # Events
    "MappingEventEmitter",
    "MappingEventType",
    "MappingEvent",
    # Services
    "CyberMappingService",
    "OntologyBindingService",
    "MappingValidationService",
]
