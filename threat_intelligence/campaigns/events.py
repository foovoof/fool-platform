"""
threat_intelligence/campaigns/events.py

Campaign Events.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class CampaignEventType(Enum):
    """Campaign event types."""
    CREATED = "campaign.created"
    UPDATED = "campaign.updated"
    VALIDATED = "campaign.validated"
    REVIEWED = "campaign.reviewed"
    PUBLISHED = "campaign.published"
    ARCHIVED = "campaign.archived"
    ASSERTION_CREATED = "campaign.assertion.created"
    TIMELINE_UPDATED = "campaign.timeline.updated"
    VERSION_CREATED = "campaign.version.created"
    EVIDENCE_LINKED = "campaign.evidence.linked"
    STATUS_CHANGED = "campaign.status.changed"


@dataclass
class CampaignEvent:
    """Campaign event."""
    event_type: str
    campaign_id: str
    timestamp: str
    data: dict[str, Any]
    actor: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "campaign_id": self.campaign_id,
            "timestamp": self.timestamp,
            "data": self.data,
            "actor": self.actor,
        }


class CampaignEventEmitter:
    """
    Emitter for campaign events.
    
    Optional integration with platform events.
    """
    
    def __init__(self) -> None:
        self._events: list[CampaignEvent] = []
        self._enabled = True
    
    def enable(self) -> None:
        """Enable event emission."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable event emission."""
        self._enabled = False
    
    def emit(self, event: CampaignEvent) -> None:
        """Emit an event."""
        if self._enabled:
            self._events.append(event)
    
    def emit_campaign_created(self, campaign_id: str, data: dict[str, Any] = None) -> None:
        """Emit campaign created event."""
        self.emit(CampaignEvent(
            event_type=CampaignEventType.CREATED.value,
            campaign_id=campaign_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data or {},
        ))
    
    def emit_campaign_updated(self, campaign_id: str, data: dict[str, Any] = None) -> None:
        """Emit campaign updated event."""
        self.emit(CampaignEvent(
            event_type=CampaignEventType.UPDATED.value,
            campaign_id=campaign_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data or {},
        ))
    
    def emit_campaign_validated(self, campaign_id: str, data: dict[str, Any] = None) -> None:
        """Emit campaign validated event."""
        self.emit(CampaignEvent(
            event_type=CampaignEventType.VALIDATED.value,
            campaign_id=campaign_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data or {},
        ))
    
    def emit_campaign_reviewed(self, campaign_id: str, data: dict[str, Any] = None) -> None:
        """Emit campaign reviewed event."""
        self.emit(CampaignEvent(
            event_type=CampaignEventType.REVIEWED.value,
            campaign_id=campaign_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data or {},
        ))
    
    def emit_campaign_published(self, campaign_id: str, data: dict[str, Any] = None) -> None:
        """Emit campaign published event."""
        self.emit(CampaignEvent(
            event_type=CampaignEventType.PUBLISHED.value,
            campaign_id=campaign_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data or {},
        ))
    
    def emit_campaign_archived(self, campaign_id: str, data: dict[str, Any] = None) -> None:
        """Emit campaign archived event."""
        self.emit(CampaignEvent(
            event_type=CampaignEventType.ARCHIVED.value,
            campaign_id=campaign_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data or {},
        ))
    
    def emit_assertion_created(self, campaign_id: str, assertion_id: str) -> None:
        """Emit assertion created event."""
        self.emit(CampaignEvent(
            event_type=CampaignEventType.ASSERTION_CREATED.value,
            campaign_id=campaign_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"assertion_id": assertion_id},
        ))
    
    def emit_timeline_updated(self, campaign_id: str, data: dict[str, Any] = None) -> None:
        """Emit timeline updated event."""
        self.emit(CampaignEvent(
            event_type=CampaignEventType.TIMELINE_UPDATED.value,
            campaign_id=campaign_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data or {},
        ))
    
    def emit_version_created(self, campaign_id: str, version_id: str) -> None:
        """Emit version created event."""
        self.emit(CampaignEvent(
            event_type=CampaignEventType.VERSION_CREATED.value,
            campaign_id=campaign_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"version_id": version_id},
        ))
    
    def emit_evidence_linked(self, campaign_id: str, evidence_id: str) -> None:
        """Emit evidence linked event."""
        self.emit(CampaignEvent(
            event_type=CampaignEventType.EVIDENCE_LINKED.value,
            campaign_id=campaign_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"evidence_id": evidence_id},
        ))
    
    def get_events(self) -> list[CampaignEvent]:
        """Get all events."""
        return list(self._events)
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
