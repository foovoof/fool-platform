"""
threat_intelligence/campaigns/models/governance.py

Campaign Governance Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.campaigns.models.base import CampaignBase, Auditable


@dataclass(frozen=True)
class Approval(CampaignBase, Auditable):
    """Campaign approval."""
    campaign_id: str = ""
    approval_type: str = ""
    status: str = "pending"
    approver: str = ""
    approved_at: str = ""
    rejection_reason: str = ""
    comments: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "approval_type": self.approval_type,
            "status": self.status,
            "approver": self.approver,
            "approved_at": self.approved_at,
            "rejection_reason": self.rejection_reason,
            "comments": self.comments,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class Review(CampaignBase, Auditable):
    """Campaign review."""
    campaign_id: str = ""
    review_type: str = ""
    status: str = "pending"
    reviewer: str = ""
    reviewed_at: str = ""
    findings: str = ""
    recommendations: str = ""
    next_review_date: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "review_type": self.review_type,
            "status": self.status,
            "reviewer": self.reviewer,
            "reviewed_at": self.reviewed_at,
            "findings": self.findings,
            "recommendations": self.recommendations,
            "next_review_date": self.next_review_date,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class AuditEntry(CampaignBase, Auditable):
    """Audit entry."""
    campaign_id: str = ""
    action: str = ""
    entity_type: str = ""
    entity_id: str = ""
    changes: dict[str, Any] = field(default_factory=dict)
    previous_state: dict[str, Any] = field(default_factory=dict)
    new_state: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "changes": self.changes,
            "previous_state": self.previous_state,
            "new_state": self.new_state,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class AuditTrail(CampaignBase):
    """Audit trail."""
    campaign_id: str = ""
    entries: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "entries": list(self.entries),
        })
        return base
