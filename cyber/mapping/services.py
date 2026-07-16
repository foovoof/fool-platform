"""
cyber/mapping/services.py

Mapping Services.

Services for coordinating cyber knowledge mapping operations.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from cyber.mapping.models import (
    CyberKnowledgeMapping,
    EntityMapping,
    RelationshipMapping,
    MappingMetadata,
    MappingStatus,
    MappingResult,
    CyberEntityType,
)
from cyber.mapping.entity_mapper import EntityMapperRegistry, BaseEntityMapper
from cyber.mapping.relationship_mapper import RelationshipMapperRegistry
from cyber.mapping.ontology_mapper import CyberOntologyMapper, OntologyBindingRegistry
from cyber.mapping.registry import MappingRegistry
from cyber.mapping.validation import MappingValidator, MappingValidationResult
from cyber.mapping.events import MappingEventEmitter


class CyberMappingService:
    """
    Main service for cyber knowledge mapping.
    
    Responsibilities:
    - Coordinate entity mapping
    - Coordinate relationship mapping
    - Coordinate ontology binding
    - Coordinate registry
    - Coordinate event emission
    
    NO intelligence logic.
    NO graph mutation.
    """
    
    def __init__(self) -> None:
        """Initialize service."""
        self._registry = MappingRegistry()
        self._ontology_mapper = CyberOntologyMapper()
        self._ontology_registry = OntologyBindingRegistry()
        self._validator = MappingValidator()
        self._event_emitter = MappingEventEmitter()
    
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
        start_time = time.time()
        errors = []
        warnings = []
        
        mapper = EntityMapperRegistry.get_mapper(entity_type)
        if not mapper:
            errors.append(f"No mapper found for entity type: {entity_type.value}")
            return MappingResult(
                success=False,
                errors=tuple(errors),
                execution_time_ms=(time.time() - start_time) * 1000,
            )
        
        result = mapper.map(entity_id, attributes, metadata)
        
        if result.entity_mapping:
            mapping = CyberKnowledgeMapping(
                entity_mapping=result.entity_mapping,
                ontology_bindings=result.bindings,
                status=MappingStatus.MAPPED,
                metadata=metadata or MappingMetadata(),
            )
            
            is_valid, validation_errors = self._registry.validate_mapping(mapping)
            if not is_valid:
                errors.extend(validation_errors)
            
            if is_valid:
                self._registry.register(mapping)
                self._event_emitter.emit_created(mapping.mapping_id, entity_type.value)
                
                for binding in result.bindings:
                    self._ontology_registry.register(binding)
                self._event_emitter.emit_ontology_bound(
                    mapping.mapping_id,
                    entity_type.value,
                    len(result.bindings),
                )
            
            return MappingResult(
                success=is_valid,
                mapping=mapping if is_valid else None,
                errors=tuple(errors),
                warnings=tuple(warnings),
                execution_time_ms=(time.time() - start_time) * 1000,
            )
        
        errors.extend(result.errors)
        return MappingResult(
            success=False,
            errors=tuple(errors),
            execution_time_ms=(time.time() - start_time) * 1000,
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
        start_time = time.time()
        errors = []
        
        mapper = RelationshipMapperRegistry.get_mapper(source_type, target_type)
        result = mapper.map(source_type, target_type, relationship_type, metadata)
        
        if result.relationship_mapping:
            mapping = CyberKnowledgeMapping(
                relationship_mappings=(result.relationship_mapping,),
                status=MappingStatus.MAPPED,
                metadata=metadata or MappingMetadata(),
            )
            
            self._registry.register(mapping)
            self._event_emitter.emit_created(
                mapping.mapping_id,
                f"{source_type}->{target_type}",
            )
            
            return MappingResult(
                success=True,
                mapping=mapping,
                execution_time_ms=(time.time() - start_time) * 1000,
            )
        
        errors.extend(result.errors)
        return MappingResult(
            success=False,
            errors=tuple(errors),
            execution_time_ms=(time.time() - start_time) * 1000,
        )
    
    def get_mapping(self, mapping_id: str) -> CyberKnowledgeMapping | None:
        """Get mapping by ID."""
        return self._registry.get(mapping_id)
    
    def list_mappings(self) -> list[CyberKnowledgeMapping]:
        """List all mappings."""
        return self._registry.list_all()
    
    def count_mappings(self) -> int:
        """Count total mappings."""
        return self._registry.count()


class OntologyBindingService:
    """
    Service for ontology binding operations.
    
    Responsibilities:
    - Coordinate ontology binding
    - Validate bindings
    - Manage binding registry
    """
    
    def __init__(self) -> None:
        """Initialize service."""
        self._mapper = CyberOntologyMapper()
        self._registry = OntologyBindingRegistry()
        self._event_emitter = MappingEventEmitter()
    
    def bind_concept(
        self,
        cyber_concept: str,
        metadata: MappingMetadata | None = None,
    ) -> list:
        """
        Bind a cyber concept to knowledge ontology.
        
        Args:
            cyber_concept: Cyber concept to bind
            metadata: Optional metadata
            
        Returns:
            List of ontology bindings
        """
        result = self._mapper.map_concept(cyber_concept, metadata)
        
        for binding in result.bindings:
            self._registry.register(binding)
        
        return list(result.bindings)
    
    def get_bindings(self, cyber_concept: str) -> list:
        """Get bindings for a concept."""
        return self._registry.get(cyber_concept)
    
    def list_concepts(self) -> list[str]:
        """List all bound concepts."""
        return self._registry.list_concepts()


class MappingValidationService:
    """
    Service for mapping validation.
    
    Responsibilities:
    - Coordinate validation
    - Return structured results
    """
    
    def __init__(self) -> None:
        """Initialize service."""
        self._validator = MappingValidator()
        self._event_emitter = MappingEventEmitter()
    
    def validate_mapping(
        self,
        mapping: CyberKnowledgeMapping,
    ) -> MappingValidationResult:
        """
        Validate a complete mapping.
        
        Args:
            mapping: Mapping to validate
            
        Returns:
            Validation result
        """
        result = self._validator.validate(mapping)
        
        self._event_emitter.emit_validated(
            mapping.mapping_id,
            mapping.entity_mapping.source_entity_type if mapping.entity_mapping else "",
            result.is_valid,
        )
        
        return result
    
    def validate_entity(
        self,
        entity_mapping: EntityMapping,
    ) -> MappingValidationResult:
        """Validate an entity mapping."""
        return self._validator.validate_entity(entity_mapping)
    
    def validate_relationship(
        self,
        rel_mapping: RelationshipMapping,
    ) -> MappingValidationResult:
        """Validate a relationship mapping."""
        return self._validator.validate_relationship(rel_mapping)
