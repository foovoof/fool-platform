from __future__ import annotations

"""
knowledge/services/relationship_resolution_service.py

Relationship Resolution Service for the Knowledge Layer.

Orchestrates relationship resolution operations.
"""
from typing import Any

from knowledge.graph.models import RelationshipType
from knowledge.graph.repository import RelationshipRepository
from knowledge.resolution import (
    RelationshipResolutionEngine,
    RelationshipMatch,
)
from knowledge.events import KnowledgeEventEmitter


class RelationshipResolutionService:
    """
    Service for relationship resolution.
    
    Orchestrates:
    - Relationship matching
    - Relationship validation
    - Event emission
    """

    def __init__(
        self,
        relationship_repository: RelationshipRepository | None = None,
        resolution_engine: RelationshipResolutionEngine | None = None,
        event_emitter: KnowledgeEventEmitter | None = None,
    ) -> None:
        """
        Initialize the service.
        
        Args:
            relationship_repository: Optional relationship repository
            resolution_engine: Optional resolution engine
            event_emitter: Optional event emitter
        """
        self._repository = relationship_repository or RelationshipRepository()
        self._engine = resolution_engine or RelationshipResolutionEngine()
        self._event_emitter = event_emitter or KnowledgeEventEmitter()

    def match_relationships(
        self,
        source_ref: str,
        target_ref: str,
        rel_type: str,
        other_source: str,
        other_target: str,
        other_type: str,
        strict: bool = True,
    ) -> RelationshipMatch:
        """
        Match two relationships.
        
        Args:
            source_ref: Source entity reference
            target_ref: Target entity reference
            rel_type: Relationship type
            other_source: Other source reference
            other_target: Other target reference
            other_type: Other relationship type
            strict: Whether to use strict matching
            
        Returns:
            RelationshipMatch result
        """
        return self._engine.match(
            source_ref,
            target_ref,
            rel_type,
            other_source,
            other_target,
            other_type,
            strict,
        )

    def create_relationship(
        self,
        source_ref: str,
        target_ref: str,
        relationship_type: str,
        confidence: float = 1.0,
    ) -> dict[str, Any]:
        """
        Create a new relationship record.
        
        Args:
            source_ref: Source entity reference
            target_ref: Target entity reference
            relationship_type: Relationship type
            confidence: Confidence score
            
        Returns:
            Created relationship
        """
        from knowledge.graph.repository.relationship_repository import RelationshipRecord
        
        rel_type = RelationshipType(relationship_type)
        
        record = RelationshipRecord(
            source_entity_ref=source_ref,
            target_entity_ref=target_ref,
            relationship_type=rel_type,
            confidence=confidence,
        )
        
        self._repository.create(record)
        
        self._event_emitter.emit_relationship_created(
            record.relationship_id,
            source_ref,
            target_ref,
            relationship_type,
        )
        
        return {
            "relationship_id": record.relationship_id,
            "source_entity_ref": record.source_entity_ref,
            "target_entity_ref": record.target_entity_ref,
            "relationship_type": record.relationship_type.value,
            "confidence": record.confidence,
        }

    def get_relationship(self, relationship_id: str) -> dict[str, Any] | None:
        """Get a relationship by ID."""
        record = self._repository.get_by_id(relationship_id)
        if record:
            return {
                "relationship_id": record.relationship_id,
                "source_entity_ref": record.source_entity_ref,
                "target_entity_ref": record.target_entity_ref,
                "relationship_type": record.relationship_type.value,
                "confidence": record.confidence,
                "validated": record.validated,
            }
        return None
