"""
threat_intelligence/campaigns/models/versioning.py

Campaign Versioning Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.campaigns.models.base import CampaignBase, Auditable


@dataclass(frozen=True)
class CampaignVersion(CampaignBase):
    """Campaign version."""
    campaign_id: str = ""
    version_number: int = 1
    changes: str = ""
    changes_summary: str = ""
    changed_by: str = ""
    change_reason: str = ""
    previous_version_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "version_number": self.version_number,
            "changes": self.changes,
            "changes_summary": self.changes_summary,
            "changed_by": self.changed_by,
            "change_reason": self.change_reason,
            "previous_version_id": self.previous_version_id,
        })
        return base


@dataclass(frozen=True)
class CampaignHistory(CampaignBase):
    """Campaign version history."""
    campaign_id: str = ""
    versions: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    total_revisions: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "versions": list(self.versions),
            "total_revisions": self.total_revisions,
        })
        return base


@dataclass(frozen=True)
class RollbackMetadata(CampaignBase):
    """Rollback metadata."""
    campaign_id: str = ""
    target_version: int = 0
    rollback_reason: str = ""
    rolled_back_by: str = ""
    rollback_created_at: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "target_version": self.target_version,
            "rollback_reason": self.rollback_reason,
            "rolled_back_by": self.rolled_back_by,
            "rollback_created_at": self.rollback_created_at,
        })
        return base
