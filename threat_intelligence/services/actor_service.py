"""
threat_intelligence/services/actor_service.py

Threat Actor Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.models import ThreatActor
from threat_intelligence.repository import ThreatActorRepository


class ThreatActorService:
    """Service for managing threat actors."""
    
    def __init__(self, repository: ThreatActorRepository | None = None) -> None:
        self._repository = repository or ThreatActorRepository()
    
    @property
    def repository(self) -> ThreatActorRepository:
        return self._repository
    
    def create(
        self,
        name: str,
        actor_type: str,
        description: str = "",
        author: str = "",
        **kwargs: Any,
    ) -> ThreatActor:
        """Create a new threat actor."""
        actor = ThreatActor(
            id=str(uuid4()),
            name=name,
            actor_type=actor_type,
            description=description,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        return self._repository.create(actor)
    
    def get(self, actor_id: str) -> ThreatActor | None:
        """Get threat actor by ID."""
        return self._repository.get(actor_id)
    
    def update(self, actor: ThreatActor) -> ThreatActor:
        """Update a threat actor."""
        updated = ThreatActor(
            id=actor.id,
            name=actor.name,
            alias=actor.alias,
            description=actor.description,
            actor_type=actor.actor_type,
            sophistication=actor.sophistication,
            resource_level=actor.resource_level,
            motivation=actor.motivation,
            intent=actor.intent,
            target_sectors=actor.target_sectors,
            target_geographies=actor.target_geographies,
            associated_actors=actor.associated_actors,
            associated_malware=actor.associated_malware,
            associated_campaigns=actor.associated_campaigns,
            capabilities=actor.capabilities,
            tags=actor.tags,
            status=actor.status,
            created_at=actor.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=actor.created_by,
            modified_by=actor.modified_by,
            version=actor.version + 1,
            metadata=actor.metadata,
            author=actor.author,
            reason=actor.reason,
            source=actor.source,
            source_url=actor.source_url,
            source_confidence=actor.source_confidence,
            explanation=actor.explanation,
            reasoning=actor.reasoning,
        )
        return self._repository.update(updated)
    
    def delete(self, actor_id: str) -> bool:
        """Delete a threat actor."""
        return self._repository.delete(actor_id)
    
    def list_all(self) -> list[ThreatActor]:
        """List all threat actors."""
        return self._repository.list_all()
    
    def search(self, query: dict[str, Any]) -> list[ThreatActor]:
        """Search threat actors."""
        return self._repository.search(query)
    
    def find_by_name(self, name: str) -> list[ThreatActor]:
        """Find actors by name."""
        return self._repository.search({"name": name})
    
    def find_by_type(self, actor_type: str) -> list[ThreatActor]:
        """Find actors by type."""
        return self._repository.search({"actor_type": actor_type})
    
    def find_active(self) -> list[ThreatActor]:
        """Find active actors."""
        return self._repository.search({"status": "active"})
