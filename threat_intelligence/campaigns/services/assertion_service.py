"""
threat_intelligence/campaigns/services/assertion_service.py

Assertion Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.campaigns.models import CampaignAssertion
from threat_intelligence.campaigns.repositories import CampaignAssertionRepository


class AssertionService:
    """Service for managing campaign assertions."""
    
    def __init__(self, repository: CampaignAssertionRepository | None = None) -> None:
        self._repository = repository or CampaignAssertionRepository()
    
    @property
    def repository(self) -> CampaignAssertionRepository:
        return self._repository
    
    def create(
        self,
        campaign_id: str,
        assertion_type: str,
        assertion: str,
        author: str = "",
        **kwargs: Any,
    ) -> CampaignAssertion:
        """Create a new assertion."""
        assertion_obj = CampaignAssertion(
            id=str(uuid4()),
            campaign_id=campaign_id,
            assertion_type=assertion_type,
            assertion=assertion,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        return self._repository.create(assertion_obj)
    
    def get(self, assertion_id: str) -> CampaignAssertion | None:
        """Get assertion by ID."""
        return self._repository.get(assertion_id)
    
    def update(self, assertion: CampaignAssertion) -> CampaignAssertion:
        """Update an assertion."""
        updated = CampaignAssertion(
            id=assertion.id,
            campaign_id=assertion.campaign_id,
            assertion_type=assertion.assertion_type,
            assertion=assertion.assertion,
            status=assertion.status,
            evidence_ids=assertion.evidence_ids,
            supporting_assertions=assertion.supporting_assertions,
            contradicting_assertions=assertion.contradicting_assertions,
            confidence_level=assertion.confidence_level,
            confidence_score=assertion.confidence_score,
            confidence_explanation=assertion.confidence_explanation,
            source=assertion.source,
            source_url=assertion.source_url,
            validated=assertion.validated,
            validated_by=assertion.validated_by,
            validated_at=assertion.validated_at,
            explanation=assertion.explanation,
            reasoning=assertion.reasoning,
            created_at=assertion.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=assertion.created_by,
            modified_by=assertion.modified_by,
            version=assertion.version + 1,
            metadata=assertion.metadata,
            author=assertion.author,
            reason=assertion.reason,
            revision_history=assertion.revision_history,
        )
        return self._repository.update(updated)
    
    def delete(self, assertion_id: str) -> bool:
        """Delete an assertion."""
        return self._repository.delete(assertion_id)
    
    def list_all(self) -> list[CampaignAssertion]:
        """List all assertions."""
        return self._repository.list_all()
    
    def search(self, query: dict[str, Any]) -> list[CampaignAssertion]:
        """Search assertions."""
        return self._repository.search(query)
    
    def find_by_campaign(self, campaign_id: str) -> list[CampaignAssertion]:
        """Find assertions by campaign."""
        return self._repository.search({"campaign_id": campaign_id})
    
    def find_by_type(self, assertion_type: str) -> list[CampaignAssertion]:
        """Find assertions by type."""
        return self._repository.search({"assertion_type": assertion_type})
    
    def find_by_status(self, status: str) -> list[CampaignAssertion]:
        """Find assertions by status."""
        return self._repository.search({"status": status})
