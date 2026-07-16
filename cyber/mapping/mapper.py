"""
cyber/mapping/mapper.py

Mapper.

Main mapper that coordinates all mapping operations.
"""
from __future__ import annotations

from typing import Any

from cyber.mapping.models import (
    CyberKnowledgeMapping,
    MappingMetadata,
    MappingResult,
    CyberEntityType,
)
from cyber.mapping.services import (
    CyberMappingService,
    OntologyBindingService,
    MappingValidationService,
)


class CyberKnowledgeMapper:
    """
    Main mapper for cyber knowledge mapping.
    
    Coordinates all mapping operations:
    - Entity mapping
    - Relationship mapping
    - Ontology binding
    - Validation
    
    NO intelligence logic.
    NO graph mutation.
    """
    
    def __init__(self) -> None:
        """Initialize mapper."""
        self._mapping_service = CyberMappingService()
        self._ontology_service = OntologyBindingService()
        self._validation_service = MappingValidationService()
    
    def map_entity(
        self,
        entity_type: CyberEntityType,
        entity_id: str,
        attributes: dict[str, Any],
        metadata: MappingMetadata | None = None,
    ) -> MappingResult:
        """
        Map a cyber entity to knowledge.
        
        Args:
            entity_type: Type of cyber entity
            entity_id: Entity ID
            attributes: Entity attributes
            metadata: Optional metadata
            
        Returns:
            Mapping result
        """
        return self._mapping_service.map_entity(
            entity_type,
            entity_id,
            attributes,
            metadata,
        )
    
    def map_relationship(
        self,
        source_type: str,
        target_type: str,
        relationship_type: str,
        metadata: MappingMetadata | None = None,
    ) -> MappingResult:
        """
        Map a cyber relationship to knowledge.
        
        Args:
            source_type: Source entity type
            target_type: Target entity type
            relationship_type: Type of relationship
            metadata: Optional metadata
            
        Returns:
            Mapping result
        """
        return self._mapping_service.map_relationship(
            source_type,
            target_type,
            relationship_type,
            metadata,
        )
    
    def get_mapping(self, mapping_id: str) -> CyberKnowledgeMapping | None:
        """Get mapping by ID."""
        return self._mapping_service.get_mapping(mapping_id)
    
    def list_mappings(self) -> list[CyberKnowledgeMapping]:
        """List all mappings."""
        return self._mapping_service.list_mappings()
    
    def count_mappings(self) -> int:
        """Count total mappings."""
        return self._mapping_service.count_mappings()
    
    def bind_concept(
        self,
        cyber_concept: str,
        metadata: MappingMetadata | None = None,
    ) -> list:
        """Bind a cyber concept to knowledge ontology."""
        return self._ontology_service.bind_concept(cyber_concept, metadata)
    
    def validate_mapping(self, mapping: CyberKnowledgeMapping):
        """Validate a mapping."""
        return self._validation_service.validate_mapping(mapping)
