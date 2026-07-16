"""
threat_intelligence/campaigns/services/evidence_service.py

Evidence Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.campaigns.models import CampaignEvidence
from threat_intelligence.campaigns.repositories import CampaignEvidenceRepository


class EvidenceService:
    """Service for managing campaign evidence."""
    
    def __init__(self, repository: CampaignEvidenceRepository | None = None) -> None:
        self._repository = repository or CampaignEvidenceRepository()
    
    @property
    def repository(self) -> CampaignEvidenceRepository:
        return self._repository
    
    def create(
        self,
        campaign_id: str,
        evidence_type: str,
        title: str,
        description: str = "",
        author: str = "",
        **kwargs: Any,
    ) -> CampaignEvidence:
        """Create new evidence."""
        evidence = CampaignEvidence(
            id=str(uuid4()),
            campaign_id=campaign_id,
            evidence_type=evidence_type,
            title=title,
            description=description,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        return self._repository.create(evidence)
    
    def get(self, evidence_id: str) -> CampaignEvidence | None:
        """Get evidence by ID."""
        return self._repository.get(evidence_id)
    
    def update(self, evidence: CampaignEvidence) -> CampaignEvidence:
        """Update evidence."""
        updated = CampaignEvidence(
            id=evidence.id,
            campaign_id=evidence.campaign_id,
            evidence_type=evidence.evidence_type,
            title=evidence.title,
            description=evidence.description,
            content=evidence.content,
            content_type=evidence.content_type,
            source=evidence.source,
            source_url=evidence.source_url,
            collected_at=evidence.collected_at,
            collected_by=evidence.collected_by,
            assertion_ids=evidence.assertion_ids,
            indicator_ids=evidence.indicator_ids,
            malware_ids=evidence.malware_ids,
            infrastructure_ids=evidence.infrastructure_ids,
            chain_of_custody=evidence.chain_of_custody,
            confidence_level=evidence.confidence_level,
            confidence_score=evidence.confidence_score,
            confidence_explanation=evidence.confidence_explanation,
            created_at=evidence.created_at,
            modified_at=datetime.now(timezone.utc).isoformat(),
            created_by=evidence.created_by,
            modified_by=evidence.modified_by,
            version=evidence.version + 1,
            metadata=evidence.metadata,
            author=evidence.author,
            reason=evidence.reason,
        )
        return self._repository.update(updated)
    
    def delete(self, evidence_id: str) -> bool:
        """Delete evidence."""
        return self._repository.delete(evidence_id)
    
    def list_all(self) -> list[CampaignEvidence]:
        """List all evidence."""
        return self._repository.list_all()
    
    def search(self, query: dict[str, Any]) -> list[CampaignEvidence]:
        """Search evidence."""
        return self._repository.search(query)
    
    def find_by_campaign(self, campaign_id: str) -> list[CampaignEvidence]:
        """Find evidence by campaign."""
        return self._repository.search({"campaign_id": campaign_id})
    
    def find_by_type(self, evidence_type: str) -> list[CampaignEvidence]:
        """Find evidence by type."""
        return self._repository.search({"evidence_type": evidence_type})
