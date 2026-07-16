"""
threat_intelligence/campaigns/services/relationship_service.py

Relationship Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.campaigns.models import CampaignRelationship
from threat_intelligence.campaigns.repositories import CampaignRelationshipRepository


class RelationshipService:
    """Service for managing campaign relationships."""
    
    def __init__(self, repository: CampaignRelationshipRepository | None = None) -> None:
        self._repository = repository or CampaignRelationshipRepository()
    
    @property
    def repository(self) -> CampaignRelationshipRepository:
        return self._repository
    
    def create(
        self,
        campaign_id: str,
        source_type: str,
        source_id: str,
        target_type: str,
        target_id: str,
        relationship_type: str,
        author: str = "",
        **kwargs: Any,
    ) -> CampaignRelationship:
        """Create a new relationship."""
        relationship = CampaignRelationship(
            id=str(uuid4()),
            campaign_id=campaign_id,
            source_type=source_type,
            source_id=source_id,
            target_type=target_type,
            target_id=target_id,
            relationship_type=relationship_type,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        return self._repository.create(relationship)
    
    def get(self, relationship_id: str) -> CampaignRelationship | None:
        """Get relationship by ID."""
        return self._repository.get(relationship_id)
    
    def delete(self, relationship_id: str) -> bool:
        """Delete relationship."""
        return self._repository.delete(relationship_id)
    
    def list_all(self) -> list[CampaignRelationship]:
        """List all relationships."""
        return self._repository.list_all()
    
    def search(self, query: dict[str, Any]) -> list[CampaignRelationship]:
        """Search relationships."""
        return self._repository.search(query)
    
    def find_by_campaign(self, campaign_id: str) -> list[CampaignRelationship]:
        """Find relationships by campaign."""
        return self._repository.search({"campaign_id": campaign_id})
    
    def find_by_type(self, relationship_type: str) -> list[CampaignRelationship]:
        """Find relationships by type."""
        return self._repository.search({"relationship_type": relationship_type})
    
    def find_by_source(self, source_type: str, source_id: str) -> list[CampaignRelationship]:
        """Find relationships by source."""
        return self._repository.search({
            "source_type": source_type,
            "source_id": source_id,
        })
    
    def find_by_target(self, target_type: str, target_id: str) -> list[CampaignRelationship]:
        """Find relationships by target."""
        return self._repository.search({
            "target_type": target_type,
            "target_id": target_id,
        })
