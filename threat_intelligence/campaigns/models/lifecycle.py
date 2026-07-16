"""
threat_intelligence/campaigns/models/lifecycle.py

Campaign Lifecycle Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from threat_intelligence.campaigns.models.base import CampaignBase


@dataclass(frozen=True)
class LifecycleTransition(CampaignBase):
    """Lifecycle transition."""
    campaign_id: str = ""
    from_status: str = ""
    to_status: str = ""
    reason: str = ""
    transitioned_by: str = ""
    approval_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "from_status": self.from_status,
            "to_status": self.to_status,
            "reason": self.reason,
            "transitioned_by": self.transitioned_by,
            "approval_id": self.approval_id,
        })
        return base


@dataclass(frozen=True)
class LifecycleState(CampaignBase):
    """Current lifecycle state."""
    campaign_id: str = ""
    status: str = "planned"
    transitions: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    last_reviewed: str = ""
    next_review: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "status": self.status,
            "transitions": list(self.transitions),
            "last_reviewed": self.last_reviewed,
            "next_review": self.next_review,
        })
        return base


@dataclass(frozen=True)
class CampaignLifecycle(CampaignBase):
    """Campaign lifecycle."""
    campaign_id: str = ""
    current_status: str = "planned"
    transitions: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    approval_history: tuple[str, ...] = field(default_factory=tuple)
    review_history: tuple[str, ...] = field(default_factory=tuple)
    last_transition: str = ""
    next_review_date: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "current_status": self.current_status,
            "transitions": list(self.transitions),
            "approval_history": list(self.approval_history),
            "review_history": list(self.review_history),
            "last_transition": self.last_transition,
            "next_review_date": self.next_review_date,
        })
        return base
