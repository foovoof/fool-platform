from __future__ import annotations

"""
knowledge/graph/repository/relationship_repository.py

Relationship repository implementation.

In-memory storage for knowledge relationships.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from knowledge.graph.models import Edge, RelationshipType


@dataclass
class RelationshipRecord:
    """Record of a relationship in the system."""
    relationship_id: str = field(default_factory=lambda: str(uuid4()))
    source_entity_ref: str = ""
    target_entity_ref: str = ""
    relationship_type: RelationshipType = RelationshipType.UNKNOWN
    edge_id: str | None = None
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    validated: bool = False
    validated_at: str | None = None


class RelationshipRepository:
    """
    In-memory repository for relationship records.
    
    Provides storage and retrieval of relationship information.
    """

    def __init__(self) -> None:
        """Initialize the repository."""
        self._relationships: dict[str, RelationshipRecord] = {}
        self._type_index: dict[str, list[str]] = {}
        self._source_index: dict[str, list[str]] = {}
        self._target_index: dict[str, list[str]] = {}

    def create(self, relationship: RelationshipRecord) -> RelationshipRecord:
        """
        Create a new relationship.
        
        Args:
            relationship: The relationship to create
            
        Returns:
            The created relationship
        """
        if relationship.relationship_id in self._relationships:
            raise ValueError(
                f"Relationship {relationship.relationship_id} already exists"
            )
        
        self._relationships[relationship.relationship_id] = relationship
        
        # Update type index
        rel_type = relationship.relationship_type.value
        if rel_type not in self._type_index:
            self._type_index[rel_type] = []
        self._type_index[rel_type].append(relationship.relationship_id)
        
        # Update source index
        if relationship.source_entity_ref:
            if relationship.source_entity_ref not in self._source_index:
                self._source_index[relationship.source_entity_ref] = []
            self._source_index[relationship.source_entity_ref].append(
                relationship.relationship_id
            )
        
        # Update target index
        if relationship.target_entity_ref:
            if relationship.target_entity_ref not in self._target_index:
                self._target_index[relationship.target_entity_ref] = []
            self._target_index[relationship.target_entity_ref].append(
                relationship.relationship_id
            )
        
        return relationship

    def update(self, relationship: RelationshipRecord) -> RelationshipRecord:
        """
        Update an existing relationship.
        
        Args:
            relationship: The relationship to update
            
        Returns:
            The updated relationship
        """
        if relationship.relationship_id not in self._relationships:
            raise ValueError(
                f"Relationship {relationship.relationship_id} not found"
            )
        self._relationships[relationship.relationship_id] = relationship
        return relationship

    def delete(self, relationship_id: str) -> bool:
        """
        Delete a relationship by ID.
        
        Args:
            relationship_id: The ID of the relationship to delete
            
        Returns:
            True if deleted
        """
        if relationship_id not in self._relationships:
            return False
        
        relationship = self._relationships[relationship_id]
        
        # Remove from type index
        rel_type = relationship.relationship_type.value
        if rel_type in self._type_index:
            self._type_index[rel_type] = [
                r for r in self._type_index[rel_type]
                if r != relationship_id
            ]
        
        # Remove from source index
        if relationship.source_entity_ref in self._source_index:
            self._source_index[relationship.source_entity_ref] = [
                r for r in self._source_index[relationship.source_entity_ref]
                if r != relationship_id
            ]
        
        # Remove from target index
        if relationship.target_entity_ref in self._target_index:
            self._target_index[relationship.target_entity_ref] = [
                r for r in self._target_index[relationship.target_entity_ref]
                if r != relationship_id
            ]
        
        del self._relationships[relationship_id]
        return True

    def get_by_id(self, relationship_id: str) -> RelationshipRecord | None:
        """Get a relationship by ID."""
        return self._relationships.get(relationship_id)

    def find_by_type(self, relationship_type: RelationshipType) -> list[RelationshipRecord]:
        """
        Find relationships by type.
        
        Args:
            relationship_type: The relationship type to filter by
            
        Returns:
            List of matching relationships
        """
        if isinstance(relationship_type, str):
            relationship_type = RelationshipType(relationship_type)
        rel_type = relationship_type.value
        rel_ids = self._type_index.get(rel_type, [])
        return [
            self._relationships[rid]
            for rid in rel_ids
            if rid in self._relationships
        ]

    def find_by_source(self, source_ref: str) -> list[RelationshipRecord]:
        """
        Find relationships by source entity.
        
        Args:
            source_ref: The source entity reference
            
        Returns:
            List of matching relationships
        """
        rel_ids = self._source_index.get(source_ref, [])
        return [
            self._relationships[rid]
            for rid in rel_ids
            if rid in self._relationships
        ]

    def find_by_target(self, target_ref: str) -> list[RelationshipRecord]:
        """
        Find relationships by target entity.
        
        Args:
            target_ref: The target entity reference
            
        Returns:
            List of matching relationships
        """
        rel_ids = self._target_index.get(target_ref, [])
        return [
            self._relationships[rid]
            for rid in rel_ids
            if rid in self._relationships
        ]

    def find_between(self, source_ref: str, target_ref: str) -> list[RelationshipRecord]:
        """
        Find relationships between two entities.
        
        Args:
            source_ref: The source entity reference
            target_ref: The target entity reference
            
        Returns:
            List of matching relationships
        """
        source_rels = set(r.relationship_id for r in self.find_by_source(source_ref))
        target_rels = set(r.relationship_id for r in self.find_by_target(target_ref))
        matching_ids = source_rels & target_rels
        return [self._relationships[rid] for rid in matching_ids]

    def mark_validated(self, relationship_id: str) -> bool:
        """
        Mark a relationship as validated.
        
        Args:
            relationship_id: The relationship ID
            
        Returns:
            True if marked
        """
        relationship = self._relationships.get(relationship_id)
        if not relationship:
            return False
        
        relationship.validated = True
        relationship.validated_at = datetime.now(timezone.utc).isoformat()
        return True

    def list(self, **kwargs: Any) -> list[RelationshipRecord]:
        """
        List relationships with optional filtering.
        
        Args:
            **kwargs: Optional filters:
                - validated: Filter by validation status
                - relationship_type: Filter by type
                - min_confidence: Minimum confidence threshold
                
        Returns:
            List of matching relationships
        """
        results = list(self._relationships.values())
        
        validated = kwargs.get("validated")
        if validated is not None:
            results = [r for r in results if r.validated == validated]
        
        rel_type = kwargs.get("relationship_type")
        if rel_type:
            if isinstance(rel_type, str):
                rel_type = RelationshipType(rel_type)
            results = [r for r in results if r.relationship_type == rel_type]
        
        min_confidence = kwargs.get("min_confidence")
        if min_confidence is not None:
            results = [r for r in results if r.confidence >= min_confidence]
        
        return results

    def exists(self, relationship_id: str) -> bool:
        """Check if a relationship exists."""
        return relationship_id in self._relationships

    def count(self, **kwargs: Any) -> int:
        """Count relationships matching criteria."""
        return len(self.list(**kwargs))

    def clear(self) -> None:
        """Clear all relationships."""
        self._relationships.clear()
        self._type_index.clear()
        self._source_index.clear()
        self._target_index.clear()
