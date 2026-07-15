from __future__ import annotations

"""
knowledge/ontology/ontology_mapper.py

Ontology mapper for the Knowledge Layer.

Maps domain objects to ontology concepts.
"""
from dataclasses import dataclass, field
from typing import Any

from knowledge.ontology.ontology_loader import (
    OntologyLoader,
    OntologyEntity,
    OntologyRelationship,
)


@dataclass
class MappingResult:
    """Result of ontology mapping."""
    is_mapped: bool
    source_type: str
    target_type: str | None = None
    mapping_type: str = ""
    mapped_data: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Check if mapping is valid."""
        return self.is_mapped and len(self.errors) == 0


class OntologyMapper:
    """
    Maps domain objects to ontology definitions.
    
    Uses loaded ontology to validate and transform entities.
    """

    def __init__(self, loader: OntologyLoader | None = None) -> None:
        """
        Initialize the ontology mapper.
        
        Args:
            loader: Optional ontology loader
        """
        self._loader = loader or OntologyLoader()

    def map_domain_object(
        self,
        domain_object: dict[str, Any],
        target_entity_type: str,
    ) -> MappingResult:
        """
        Map a domain object to an ontology entity.
        
        Args:
            domain_object: The domain object to map
            target_entity_type: The target ontology entity type
            
        Returns:
            MappingResult
        """
        entity_def = self._loader.get_entity(target_entity_type)
        
        if not entity_def:
            return MappingResult(
                is_mapped=False,
                source_type=domain_object.get("type", "unknown"),
                target_type=target_entity_type,
                mapping_type="domain_to_entity",
                errors=[f"Entity type '{target_entity_type}' not found in ontology"],
            )

        errors: list[str] = []
        mapped_data: dict[str, Any] = {}
        
        mapped_data["entity_type"] = entity_def.entity_type
        mapped_data["name"] = domain_object.get("name", "")
        mapped_data["attributes"] = {}
        
        for attr in entity_def.required_attributes:
            if attr not in domain_object:
                errors.append(f"Required attribute '{attr}' missing")
            else:
                mapped_data["attributes"][attr] = domain_object[attr]

        for key, value in domain_object.items():
            if key not in ["type", "name"]:
                mapped_data["attributes"][key] = value

        identity_refs = []
        for key in entity_def.identity_keys:
            if key in domain_object:
                identity_refs.append(str(domain_object[key]))
        
        mapped_data["identity_refs"] = identity_refs

        return MappingResult(
            is_mapped=len(errors) == 0,
            source_type=domain_object.get("type", "unknown"),
            target_type=target_entity_type,
            mapping_type="domain_to_entity",
            mapped_data=mapped_data,
            errors=errors,
        )

    def map_entity(
        self,
        source_entity: dict[str, Any],
        target_entity_type: str,
    ) -> MappingResult:
        """
        Map an entity to a different entity type.
        
        Args:
            source_entity: The source entity
            target_entity_type: The target entity type
            
        Returns:
            MappingResult
        """
        entity_def = self._loader.get_entity(target_entity_type)
        
        if not entity_def:
            return MappingResult(
                is_mapped=False,
                source_type=source_entity.get("entity_type", "unknown"),
                target_type=target_entity_type,
                mapping_type="entity_to_entity",
                errors=[f"Entity type '{target_entity_type}' not found in ontology"],
            )

        errors: list[str] = []
        mapped_data: dict[str, Any] = {}
        
        mapped_data["entity_type"] = entity_def.entity_type
        mapped_data["attributes"] = source_entity.get("attributes", {}).copy()
        
        for attr in entity_def.required_attributes:
            if attr not in mapped_data["attributes"]:
                errors.append(f"Required attribute '{attr}' missing from source")

        mapped_data["identity_refs"] = source_entity.get("identity_refs", [])

        return MappingResult(
            is_mapped=len(errors) == 0,
            source_type=source_entity.get("entity_type", "unknown"),
            target_type=target_entity_type,
            mapping_type="entity_to_entity",
            mapped_data=mapped_data,
            errors=errors,
        )

    def map_relationship(
        self,
        source_entity_id: str,
        target_entity_id: str,
        relationship_type: str,
    ) -> MappingResult:
        """
        Map a relationship to ontology definition.
        
        Args:
            source_entity_id: Source entity ID
            target_entity_id: Target entity ID
            relationship_type: Relationship type
            
        Returns:
            MappingResult
        """
        relationship_def = self._loader.get_relationship(relationship_type)
        
        if not relationship_def:
            return MappingResult(
                is_mapped=False,
                source_type=source_entity_id,
                target_type=target_entity_id,
                mapping_type="relationship",
                errors=[f"Relationship type '{relationship_type}' not found in ontology"],
            )

        mapped_data: dict[str, Any] = {}
        mapped_data["relationship_type"] = relationship_def.relationship_type
        mapped_data["source_entity_id"] = source_entity_id
        mapped_data["target_entity_id"] = target_entity_id
        mapped_data["is_symmetric"] = relationship_def.is_symmetric

        return MappingResult(
            is_mapped=True,
            source_type=source_entity_id,
            target_type=target_entity_id,
            mapping_type="relationship",
            mapped_data=mapped_data,
        )

    def validate_entity_mapping(
        self,
        entity: dict[str, Any],
        entity_type: str,
    ) -> MappingResult:
        """
        Validate an entity against ontology.
        
        Args:
            entity: The entity to validate
            entity_type: The expected entity type
            
        Returns:
            MappingResult
        """
        entity_def = self._loader.get_entity(entity_type)
        
        if not entity_def:
            return MappingResult(
                is_mapped=False,
                source_type=entity_type,
                target_type=entity_type,
                mapping_type="validation",
                errors=[f"Entity type '{entity_type}' not found in ontology"],
            )

        errors: list[str] = []
        
        for attr in entity_def.required_attributes:
            if attr not in entity.get("attributes", {}):
                errors.append(f"Required attribute '{attr}' missing")

        identity_keys = entity_def.identity_keys
        if identity_keys:
            has_identity = any(
                key in entity.get("identity_refs", [])
                for key in identity_keys
            )
            if not has_identity:
                errors.append("No identity key found in identity_refs")

        return MappingResult(
            is_mapped=len(errors) == 0,
            source_type=entity_type,
            target_type=entity_type,
            mapping_type="validation",
            mapped_data=entity,
            errors=errors,
        )
