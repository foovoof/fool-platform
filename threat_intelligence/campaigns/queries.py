"""
threat_intelligence/campaigns/queries.py

Campaign Queries.
"""
from __future__ import annotations

from typing import Any

from threat_intelligence.campaigns.services import (
    CampaignService,
    AssertionService,
    TimelineService,
    EvidenceService,
    RelationshipService,
    LifecycleService,
    GovernanceService,
    VersionService,
)


class CampaignQueryService:
    """
    Service for querying campaigns.
    
    Provides pure Python APIs for finding campaigns by various criteria.
    """
    
    def __init__(
        self,
        campaign_service: CampaignService | None = None,
        assertion_service: AssertionService | None = None,
        timeline_service: TimelineService | None = None,
        evidence_service: EvidenceService | None = None,
        relationship_service: RelationshipService | None = None,
        lifecycle_service: LifecycleService | None = None,
        governance_service: GovernanceService | None = None,
        version_service: VersionService | None = None,
    ) -> None:
        self._campaign_service = campaign_service or CampaignService()
        self._assertion_service = assertion_service or AssertionService()
        self._timeline_service = timeline_service or TimelineService()
        self._evidence_service = evidence_service or EvidenceService()
        self._relationship_service = relationship_service or RelationshipService()
        self._lifecycle_service = lifecycle_service or LifecycleService()
        self._governance_service = governance_service or GovernanceService()
        self._version_service = version_service or VersionService()
    
    def find_by_actor(self, actor_id: str) -> list[dict[str, Any]]:
        """Find campaigns by associated actor."""
        campaigns = self._campaign_service.find_by_actor(actor_id)
        return [c.to_dict() for c in campaigns]
    
    def find_by_malware(self, malware_id: str) -> list[dict[str, Any]]:
        """Find campaigns by associated malware."""
        campaigns = self._campaign_service.find_by_malware(malware_id)
        return [c.to_dict() for c in campaigns]
    
    def find_by_infrastructure(self, infra_id: str) -> list[dict[str, Any]]:
        """Find campaigns by associated infrastructure."""
        campaigns = self._campaign_service.find_by_infrastructure(infra_id)
        return [c.to_dict() for c in campaigns]
    
    def find_by_indicator(self, indicator_id: str) -> list[dict[str, Any]]:
        """Find campaigns by associated indicator."""
        campaigns = self._campaign_service.find_by_indicator(indicator_id)
        return [c.to_dict() for c in campaigns]
    
    def find_by_status(self, status: str) -> list[dict[str, Any]]:
        """Find campaigns by status."""
        campaigns = self._campaign_service.find_by_status(status)
        return [c.to_dict() for c in campaigns]
    
    def find_by_severity(self, severity: str) -> list[dict[str, Any]]:
        """Find campaigns by severity."""
        campaigns = self._campaign_service.search({"severity": severity})
        return [c.to_dict() for c in campaigns]
    
    def find_by_confidence(self, confidence_level: str) -> list[dict[str, Any]]:
        """Find campaigns by confidence level."""
        campaigns = self._campaign_service.search({"confidence_level": confidence_level})
        return [c.to_dict() for c in campaigns]
    
    def find_by_sector(self, sector: str) -> list[dict[str, Any]]:
        """Find campaigns targeting a sector."""
        campaigns = self._campaign_service.search({"sectors": sector})
        return [c.to_dict() for c in campaigns]
    
    def find_by_geography(self, geography: str) -> list[dict[str, Any]]:
        """Find campaigns targeting a geography."""
        campaigns = self._campaign_service.search({"geographies": geography})
        return [c.to_dict() for c in campaigns]
    
    def find_assertions_by_campaign(self, campaign_id: str) -> list[dict[str, Any]]:
        """Find assertions for a campaign."""
        assertions = self._assertion_service.find_by_campaign(campaign_id)
        return [a.to_dict() for a in assertions]
    
    def find_evidence_by_campaign(self, campaign_id: str) -> list[dict[str, Any]]:
        """Find evidence for a campaign."""
        evidence = self._evidence_service.find_by_campaign(campaign_id)
        return [e.to_dict() for e in evidence]
    
    def find_timeline_events(self, campaign_id: str) -> list[dict[str, Any]]:
        """Find timeline events for a campaign."""
        events = self._timeline_service.find_events_by_campaign(campaign_id)
        return [e.to_dict() for e in events]
    
    def find_milestones(self, campaign_id: str) -> list[dict[str, Any]]:
        """Find milestones for a campaign."""
        milestones = self._timeline_service.find_milestones_by_campaign(campaign_id)
        return [m.to_dict() for m in milestones]
    
    def find_relationships(self, campaign_id: str) -> list[dict[str, Any]]:
        """Find relationships for a campaign."""
        relationships = self._relationship_service.find_by_campaign(campaign_id)
        return [r.to_dict() for r in relationships]
    
    def get_lifecycle_status(self, campaign_id: str) -> str | None:
        """Get lifecycle status for a campaign."""
        return self._lifecycle_service.get_status(campaign_id)
    
    def get_audit_trail(self, campaign_id: str) -> dict[str, Any] | None:
        """Get audit trail for a campaign."""
        trail = self._governance_service.get_audit_trail(campaign_id)
        return trail.to_dict() if trail else None
    
    def get_version_history(self, campaign_id: str) -> dict[str, Any] | None:
        """Get version history for a campaign."""
        history = self._version_service.get_history(campaign_id)
        return history.to_dict() if history else None
