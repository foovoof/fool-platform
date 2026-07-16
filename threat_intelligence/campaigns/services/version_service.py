"""
threat_intelligence/campaigns/services/version_service.py

Version Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.campaigns.models import CampaignVersion, CampaignHistory, RollbackMetadata
from threat_intelligence.campaigns.repositories import CampaignVersionRepository


class VersionService:
    """Service for campaign versioning."""
    
    def __init__(self, repository: CampaignVersionRepository | None = None) -> None:
        self._repository = repository or CampaignVersionRepository()
        self._histories: dict[str, CampaignHistory] = {}
        self._rollback_metadata: dict[str, RollbackMetadata] = {}
    
    @property
    def repository(self) -> CampaignVersionRepository:
        return self._repository
    
    def create_version(
        self,
        campaign_id: str,
        changes: str,
        changes_summary: str,
        changed_by: str,
        change_reason: str = "",
        previous_version_id: str = "",
    ) -> CampaignVersion:
        """Create a new version."""
        history = self._histories.get(campaign_id)
        version_number = 1 if not history else history.total_revisions + 1
        
        version = CampaignVersion(
            id=str(uuid4()),
            campaign_id=campaign_id,
            version_number=version_number,
            changes=changes,
            changes_summary=changes_summary,
            changed_by=changed_by,
            change_reason=change_reason,
            previous_version_id=previous_version_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
        )
        
        self._repository.create(version)
        self._update_history(campaign_id, version)
        
        return version
    
    def _update_history(self, campaign_id: str, version: CampaignVersion) -> None:
        """Update campaign history."""
        if campaign_id not in self._histories:
            self._histories[campaign_id] = CampaignHistory(
                campaign_id=campaign_id,
            )
        
        history = self._histories[campaign_id]
        self._histories[campaign_id] = CampaignHistory(
            campaign_id=campaign_id,
            versions=history.versions + (version.to_dict(),),
            total_revisions=history.total_revisions + 1,
        )
    
    def get_version(self, version_id: str) -> CampaignVersion | None:
        """Get version by ID."""
        return self._repository.get(version_id)
    
    def get_history(self, campaign_id: str) -> CampaignHistory | None:
        """Get version history for campaign."""
        return self._histories.get(campaign_id)
    
    def get_versions(self, campaign_id: str) -> list[CampaignVersion]:
        """Get all versions for campaign."""
        return self._repository.search({"campaign_id": campaign_id})
    
    def rollback(
        self,
        campaign_id: str,
        target_version: int,
        rolled_back_by: str,
        rollback_reason: str = "",
    ) -> RollbackMetadata | None:
        """Create rollback metadata."""
        history = self._histories.get(campaign_id)
        if not history:
            return None
        
        version_exists = any(
            v.get("version_number") == target_version
            for v in history.versions
        )
        
        if not version_exists:
            return None
        
        metadata = RollbackMetadata(
            id=str(uuid4()),
            campaign_id=campaign_id,
            target_version=target_version,
            rollback_reason=rollback_reason,
            rolled_back_by=rolled_back_by,
            rollback_created_at=datetime.now(timezone.utc).isoformat(),
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
        )
        
        self._rollback_metadata[f"{campaign_id}:{target_version}"] = metadata
        
        return metadata
    
    def get_rollback_metadata(
        self,
        campaign_id: str,
        target_version: int,
    ) -> RollbackMetadata | None:
        """Get rollback metadata."""
        return self._rollback_metadata.get(f"{campaign_id}:{target_version}")
