from __future__ import annotations

"""
knowledge/services/ontology_service.py

Ontology Service for the Knowledge Layer.

Orchestrates ontology operations.
"""
from typing import Any

from knowledge.ontology import (
    OntologyLoader,
    OntologyMapper,
    OntologyValidator,
    ValidationResult,
)


class OntologyService:
    """
    Service for ontology operations.
    
    Orchestrates:
    - Ontology loading
    - Entity/relationship mapping
    - Ontology validation
    """

    def __init__(
        self,
        loader: OntologyLoader | None = None,
    ) -> None:
        """
        Initialize the service.
        
        Args:
            loader: Optional ontology loader
        """
        self._loader = loader or OntologyLoader()
        self._mapper = OntologyMapper(self._loader)
        self._validator = OntologyValidator(self._loader)

    def load_ontology(self) -> dict[str, Any]:
        """
        Load all ontology definitions.
        
        Returns:
            Dictionary with ontology definitions
        """
        return self._loader.load_all()

    def map_entity(
        self,
        entity: dict[str, Any],
        target_type: str,
    ) -> dict[str, Any]:
        """
        Map an entity to ontology.
        
        Args:
            entity: The entity to map
            target_type: Target entity type
            
        Returns:
            Mapping result
        """
        result = self._mapper.map_entity(entity, target_type)
        
        return {
            "is_mapped": result.is_mapped,
            "target_type": result.target_type,
            "mapped_data": result.mapped_data,
            "errors": result.errors,
        }

    def map_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
    ) -> dict[str, Any]:
        """
        Map a relationship to ontology.
        
        Args:
            source_id: Source entity ID
            target_id: Target entity ID
            relationship_type: Relationship type
            
        Returns:
            Mapping result
        """
        result = self._mapper.map_relationship(
            source_id,
            target_id,
            relationship_type,
        )
        
        return {
            "is_mapped": result.is_mapped,
            "source_type": result.source_type,
            "target_type": result.target_type,
            "mapped_data": result.mapped_data,
            "errors": result.errors,
        }

    def validate_entity(
        self,
        entity: dict[str, Any],
        entity_type: str,
    ) -> dict[str, Any]:
        """
        Validate an entity against ontology.
        
        Args:
            entity: The entity to validate
            entity_type: Expected entity type
            
        Returns:
            Validation result
        """
        result = self._mapper.validate_entity_mapping(entity, entity_type)
        
        return {
            "is_valid": result.is_valid,
            "entity_type": entity_type,
            "errors": result.errors,
        }

    def get_entity_definition(self, entity_type: str) -> dict[str, Any] | None:
        """
        Get entity definition from ontology.
        
        Args:
            entity_type: The entity type
            
        Returns:
            Entity definition or None
        """
        entity = self._loader.get_entity(entity_type)
        if entity:
            return {
                "entity_type": entity.entity_type,
                "name": entity.name,
                "description": entity.description,
                "identity_keys": entity.identity_keys,
                "required_attributes": entity.required_attributes,
            }
        return None

    def get_relationship_definition(
        self,
        relationship_type: str,
    ) -> dict[str, Any] | None:
        """
        Get relationship definition from ontology.
        
        Args:
            relationship_type: The relationship type
            
        Returns:
            Relationship definition or None
        """
        relationship = self._loader.get_relationship(relationship_type)
        if relationship:
            return {
                "relationship_type": relationship.relationship_type,
                "name": relationship.name,
                "description": relationship.description,
                "source_entity_types": relationship.source_entity_types,
                "target_entity_types": relationship.target_entity_types,
                "is_symmetric": relationship.is_symmetric,
            }
        return None

    def validate_ontology(self) -> dict[str, Any]:
        """
        Validate the ontology itself.
        
        Returns:
            Validation results
        """
        return self._validator.validate_ontology()

    def get_undefined_types(self) -> dict[str, list[str]]:
        """
        Get all undefined types (requires a graph).
        
        Note: This method requires a graph to be provided.
        Use validate_ontology() for standalone validation.
        
        Returns:
            Dictionary with undefined types
        """
        return {
            "nodes": [],
            "relationships": [],
        }
