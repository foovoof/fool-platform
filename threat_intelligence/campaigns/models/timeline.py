"""
threat_intelligence/campaigns/models/timeline.py

Campaign Timeline Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.campaigns.models.base import CampaignBase, Auditable


@dataclass(frozen=True)
class TimelineEvent(CampaignBase, Auditable):
    """Timeline event."""
    campaign_id: str = ""
    event_type: str = ""
    timestamp: str = ""
    description: str = ""
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    assertion_ids: tuple[str, ...] = field(default_factory=tuple)
    actor_ids: tuple[str, ...] = field(default_factory=tuple)
    malware_ids: tuple[str, ...] = field(default_factory=tuple)
    infrastructure_ids: tuple[str, ...] = field(default_factory=tuple)
    indicator_ids: tuple[str, ...] = field(default_factory=tuple)
    location: str = ""
    significance: str = "normal"
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "description": self.description,
            "evidence_ids": list(self.evidence_ids),
            "assertion_ids": list(self.assertion_ids),
            "actor_ids": list(self.actor_ids),
            "malware_ids": list(self.malware_ids),
            "infrastructure_ids": list(self.infrastructure_ids),
            "indicator_ids": list(self.indicator_ids),
            "location": self.location,
            "significance": self.significance,
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base


@dataclass(frozen=True)
class Milestone(CampaignBase, Auditable):
    """Campaign milestone."""
    campaign_id: str = ""
    name: str = ""
    description: str = ""
    target_date: str = ""
    achieved_date: str = ""
    status: str = "proposed"
    significance: str = "normal"
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "name": self.name,
            "description": self.description,
            "target_date": self.target_date,
            "achieved_date": self.achieved_date,
            "status": self.status,
            "significance": self.significance,
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base


@dataclass(frozen=True)
class ObservedActivity(CampaignBase, Auditable):
    """Observed activity."""
    campaign_id: str = ""
    activity_type: str = ""
    timestamp: str = ""
    duration: int = 0
    description: str = ""
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    indicator_ids: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "activity_type": self.activity_type,
            "timestamp": self.timestamp,
            "duration": self.duration,
            "description": self.description,
            "evidence_ids": list(self.evidence_ids),
            "indicator_ids": list(self.indicator_ids),
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base


@dataclass(frozen=True)
class ActivityWindow(CampaignBase):
    """Activity window."""
    campaign_id: str = ""
    window_type: str = ""
    start_time: str = ""
    end_time: str = ""
    description: str = ""
    event_count: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "window_type": self.window_type,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "description": self.description,
            "event_count": self.event_count,
        })
        return base


@dataclass(frozen=True)
class CampaignTimeline(CampaignBase):
    """Campaign timeline."""
    campaign_id: str = ""
    first_observed: str = ""
    last_observed: str = ""
    active_start: str = ""
    active_end: str = ""
    events: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    milestones: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    activities: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    windows: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "campaign_id": self.campaign_id,
            "first_observed": self.first_observed,
            "last_observed": self.last_observed,
            "active_start": self.active_start,
            "active_end": self.active_end,
            "events": list(self.events),
            "milestones": list(self.milestones),
            "activities": list(self.activities),
            "windows": list(self.windows),
        })
        return base
