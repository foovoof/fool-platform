"""
cyber/mapping/registry.py

Mapping Registry.

Registry for managing cyber knowledge mappings.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cyber.mapping.models import (
    CyberKnowledgeMapping,
    EntityMapping,
    RelationshipMapping,
    MappingStatus,
)


class MappingRegistry:
    """
    Registry for managing cyber knowledge mappings.
    
    Responsibilities:
    - Register mappings
    - Lookup mappings
    - Validate mappings
    - List mappings
    - Version mappings
    """
    
    def __init__(self) -> None:
        """Initialize registry."""
        self._mappings: dict[str, CyberKnowledgeMapping] = {}
        self._entity_mappings: dict[str, EntityMapping] = {}
        self._relationship_mappings: dict[str, RelationshipMapping] = {}
        self._versions: dict[str, list[str]] = {}
    
    def register(self, mapping: CyberKnowledgeMapping) -> bool:
        """
        Register a mapping.
        
        Args:
            mapping: Mapping to register
            
        Returns:
            True if registered
        """
        if mapping.mapping_id in self._mappings:
            return False
        
        self._mappings[mapping.mapping_id] = mapping
        
        if mapping.entity_mapping:
            self._entity_mappings[mapping.entity_mapping.mapping_id] = mapping.entity_mapping
        
        for rel_mapping in mapping.relationship_mappings:
            self._relationship_mappings[rel_mapping.mapping_id] = rel_mapping
        
        self._track_version(mapping.mapping_id)
        
        return True
    
    def get(self, mapping_id: str) -> CyberKnowledgeMapping | None:
        """Get mapping by ID."""
        return self._mappings.get(mapping_id)
    
    def get_entity_mapping(self, mapping_id: str) -> EntityMapping | None:
        """Get entity mapping by ID."""
        return self._entity_mappings.get(mapping_id)
    
    def get_relationship_mapping(self, mapping_id: str) -> RelationshipMapping | None:
        """Get relationship mapping by ID."""
        return self._relationship_mappings.get(mapping_id)
    
    def find_by_entity_id(self, entity_id: str) -> list[CyberKnowledgeMapping]:
        """Find mappings by entity ID."""
        results = []
        for mapping in self._mappings.values():
            if mapping.entity_mapping and mapping.entity_mapping.source_entity_id == entity_id:
                results.append(mapping)
        return results
    
    def find_by_status(self, status: MappingStatus) -> list[CyberKnowledgeMapping]:
        """Find mappings by status."""
        return [m for m in self._mappings.values() if m.status == status]
    
    def list_all(self) -> list[CyberKnowledgeMapping]:
        """List all mappings."""
        return list(self._mappings.values())
    
    def list_entity_mappings(self) -> list[EntityMapping]:
        """List all entity mappings."""
        return list(self._entity_mappings.values())
    
    def list_relationship_mappings(self) -> list[RelationshipMapping]:
        """List all relationship mappings."""
        return list(self._relationship_mappings.values())
    
    def count(self) -> int:
        """Count total mappings."""
        return len(self._mappings)
    
    def count_by_status(self, status: MappingStatus) -> int:
        """Count mappings by status."""
        return len(self.find_by_status(status))
    
    def get_versions(self, mapping_id: str) -> list[str]:
        """Get version history for a mapping."""
        return self._versions.get(mapping_id, []).copy()
    
    def _track_version(self, mapping_id: str) -> None:
        """Track version history."""
        if mapping_id not in self._versions:
            self._versions[mapping_id] = []
        self._versions[mapping_id].append(mapping_id)
    
    def clear(self) -> None:
        """Clear all mappings."""
        self._mappings.clear()
        self._entity_mappings.clear()
        self._relationship_mappings.clear()
        self._versions.clear()
    
    def validate_mapping(self, mapping: CyberKnowledgeMapping) -> tuple[bool, list[str]]:
        """
        Validate a mapping.
        
        Args:
            mapping: Mapping to validate
            
        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []
        
        if not mapping.mapping_id:
            errors.append("mapping_id is required")
        
        if not mapping.entity_mapping and not mapping.relationship_mappings:
            errors.append("Mapping must have either entity_mapping or relationship_mappings")
        
        if mapping.entity_mapping:
            if not mapping.entity_mapping.mapping_id:
                errors.append("entity_mapping.mapping_id is required")
            if not mapping.entity_mapping.source_entity_type:
                errors.append("entity_mapping.source_entity_type is required")
            if not mapping.entity_mapping.source_entity_id:
                errors.append("entity_mapping.source_entity_id is required")
        
        return len(errors) == 0, errors
