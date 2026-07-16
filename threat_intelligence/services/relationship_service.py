"""
threat_intelligence/services/relationship_service.py

Relationship Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.models import Relationship
from threat_intelligence.repository import RelationshipRepository


class RelationshipService:
    """Service for managing relationships."""
    
    def __init__(self, repository: RelationshipRepository | None = None) -> None:
        self._repository = repository or RelationshipRepository()
    
    @property
    def repository(self) -> RelationshipRepository:
        return self._repository
    
    def create(
        self,
        source_type: str,
        source_id: str,
        target_type: str,
        target_id: str,
        relationship_type: str,
        description: str = "",
        author: str = "",
        **kwargs: Any,
    ) -> Relationship:
        """Create a new relationship."""
        relationship = Relationship(
            id=str(uuid4()),
            source_type=source_type,
            source_id=source_id,
            target_type=target_type,
            target_id=target_id,
            relationship_type=relationship_type,
            description=description,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        return self._repository.create(relationship)
    
    def get(self, relationship_id: str) -> Relationship | None:
        """Get relationship by ID."""
        return self._repository.get(relationship_id)
    
    def update(self, relationship: Relationship) -> Relationship:
        """Update a relationship."""
        updated = Relationship(
            id=relationship.id,
            source_type=relationship.source_type,
            source_id=relationship.source_id,
            target_type=relationship.target_type,
            target_id=relationship.target_id,
            relationship_type=relationship.relationship_type,
            description=relationship.description,
            first_seen=relationship.first_seen,
            last_seen=datetime.now(timezone.utc).isoformat(),
            tags=relationship.tags,
            created_at=relationship.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=relationship.created_by,
            modified_by=relationship.modified_by,
            version=relationship.version + 1,
            metadata=relationship.metadata,
            author=relationship.author,
            reason=relationship.reason,
            source=relationship.source,
            source_url=relationship.source_url,
            source_confidence=relationship.source_confidence,
            confidence_level=relationship.confidence_level,
            confidence_score=relationship.confidence_score,
            confidence_explanation=relationship.confidence_explanation,
        )
        return self._repository.update(updated)
    
    def delete(self, relationship_id: str) -> bool:
        """Delete a relationship."""
        return self._repository.delete(relationship_id)
    
    def list_all(self) -> list[Relationship]:
        """List all relationships."""
        return self._repository.list_all()
    
    def search(self, query: dict[str, Any]) -> list[Relationship]:
        """Search relationships."""
        return self._repository.search(query)
    
    def find_by_source(self, source_type: str, source_id: str) -> list[Relationship]:
        """Find relationships by source."""
        return self._repository.search({
            "source_type": source_type,
            "source_id": source_id,
        })
    
    def find_by_target(self, target_type: str, target_id: str) -> list[Relationship]:
        """Find relationships by target."""
        return self._repository.search({
            "target_type": target_type,
            "target_id": target_id,
        })
    
    def find_by_type(self, relationship_type: str) -> list[Relationship]:
        """Find relationships by type."""
        return self._repository.search({"relationship_type": relationship_type})
