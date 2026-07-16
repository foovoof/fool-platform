"""
threat_intelligence/campaigns/services/campaign_service.py

Campaign Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.campaigns.models import Campaign
from threat_intelligence.campaigns.repositories import CampaignRepository


class CampaignService:
    """
    Service for managing campaigns.
    
    Provides CRUD operations and business logic.
    """
    
    def __init__(self, repository: CampaignRepository | None = None) -> None:
        self._repository = repository or CampaignRepository()
    
    @property
    def repository(self) -> CampaignRepository:
        """Get the repository."""
        return self._repository
    
    def create(
        self,
        name: str,
        description: str = "",
        author: str = "",
        **kwargs: Any,
    ) -> Campaign:
        """
        Create a new campaign.
        
        Args:
            name: Campaign name
            description: Description
            author: Author
            **kwargs: Additional fields
            
        Returns:
            Created campaign
        """
        campaign = Campaign(
            id=str(uuid4()),
            name=name,
            description=description,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        return self._repository.create(campaign)
    
    def get(self, campaign_id: str) -> Campaign | None:
        """Get campaign by ID."""
        return self._repository.get(campaign_id)
    
    def update(self, campaign: Campaign) -> Campaign:
        """Update a campaign."""
        updated = Campaign(
            id=campaign.id,
            name=campaign.name,
            description=campaign.description,
            status=campaign.status,
            severity=campaign.severity,
            confidence_level=campaign.confidence_level,
            confidence_score=campaign.confidence_score,
            confidence_explanation=campaign.confidence_explanation,
            start_date=campaign.start_date,
            end_date=campaign.end_date,
            first_observed=campaign.first_observed,
            last_observed=campaign.last_observed,
            aliases=campaign.aliases,
            objectives=campaign.objectives,
            motivations=campaign.motivations,
            sectors=campaign.sectors,
            geographies=campaign.geographies,
            associated_actors=campaign.associated_actors,
            associated_malware=campaign.associated_malware,
            associated_infrastructure=campaign.associated_infrastructure,
            associated_indicators=campaign.associated_indicators,
            associated_evidence=campaign.associated_evidence,
            associated_assertions=campaign.associated_assertions,
            victim_count=campaign.victim_count,
            intended_impact=campaign.intended_impact,
            observed_impact=campaign.observed_impact,
            tags=campaign.tags,
            governance_status=campaign.governance_status,
            review_status=campaign.review_status,
            approved_by=campaign.approved_by,
            approved_at=campaign.approved_at,
            explanation=campaign.explanation,
            reasoning=campaign.reasoning,
            created_at=campaign.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=campaign.created_by,
            modified_by=campaign.modified_by,
            version=campaign.version + 1,
            metadata=campaign.metadata,
            author=campaign.author,
            reason=campaign.reason,
            source=campaign.source,
            source_url=campaign.source_url,
            revision_history=campaign.revision_history,
        )
        return self._repository.update(updated)
    
    def delete(self, campaign_id: str) -> bool:
        """Delete a campaign."""
        return self._repository.delete(campaign_id)
    
    def list_all(self) -> list[Campaign]:
        """List all campaigns."""
        return self._repository.list_all()
    
    def search(self, query: dict[str, Any]) -> list[Campaign]:
        """Search campaigns."""
        return self._repository.search(query)
    
    def find_by_status(self, status: str) -> list[Campaign]:
        """Find campaigns by status."""
        return self._repository.search({"status": status})
    
    def find_by_actor(self, actor_id: str) -> list[Campaign]:
        """Find campaigns by associated actor."""
        return self._repository.search({"associated_actors": actor_id})
    
    def find_by_malware(self, malware_id: str) -> list[Campaign]:
        """Find campaigns by associated malware."""
        return self._repository.search({"associated_malware": malware_id})
    
    def find_by_infrastructure(self, infra_id: str) -> list[Campaign]:
        """Find campaigns by associated infrastructure."""
        return self._repository.search({"associated_infrastructure": infra_id})
    
    def find_by_indicator(self, indicator_id: str) -> list[Campaign]:
        """Find campaigns by associated indicator."""
        return self._repository.search({"associated_indicators": indicator_id})
    
    def count(self) -> int:
        """Count campaigns."""
        return self._repository.count()
    
    def exists(self, campaign_id: str) -> bool:
        """Check if campaign exists."""
        return self._repository.exists(campaign_id)
