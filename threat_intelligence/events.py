"""
threat_intelligence/events.py

Threat Intelligence Events.

Integrates with Platform Event Bus.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ThreatIntelligenceEventType(Enum):
    """Types of threat intelligence events."""
    INDICATOR_CREATED = "indicator.created"
    INDICATOR_UPDATED = "indicator.updated"
    INDICATOR_DELETED = "indicator.deleted"
    CAMPAIGN_CREATED = "campaign.created"
    CAMPAIGN_UPDATED = "campaign.updated"
    ACTOR_CREATED = "actor.created"
    ACTOR_UPDATED = "actor.updated"
    MALWARE_CREATED = "malware.created"
    MALWARE_UPDATED = "malware.updated"
    INFRASTRUCTURE_CREATED = "infrastructure.created"
    REPORT_CREATED = "report.created"
    REPORT_UPDATED = "report.updated"
    FINDING_CREATED = "finding.created"
    EVIDENCE_CREATED = "evidence.created"
    RELATIONSHIP_CREATED = "relationship.created"
    CONFIDENCE_UPDATED = "confidence.updated"


@dataclass(frozen=True)
class ThreatIntelligenceEvent:
    """Event for threat intelligence operations."""
    event_type: ThreatIntelligenceEventType
    entity_type: str = ""
    entity_id: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    data: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "timestamp": self.timestamp,
            "data": self.data,
        }


class ThreatIntelligenceEventEmitter:
    """
    Emits events for threat intelligence operations.
    
    Event integration is optional.
    Does not fail if event bus is unavailable.
    """
    
    def __init__(self) -> None:
        self._events: list[ThreatIntelligenceEvent] = []
        self._enabled = True
    
    def emit(self, event: ThreatIntelligenceEvent) -> None:
        """
        Emit an event.
        
        Silently ignores if event bus is unavailable.
        """
        if not self._enabled:
            return
        
        self._events.append(event)
        
        try:
            self._emit_to_bus(event)
        except Exception:
            pass
    
    def _emit_to_bus(self, event: ThreatIntelligenceEvent) -> None:
        """
        Emit event to platform event bus.
        
        This is a no-op by default.
        """
        pass
    
    def get_events(self) -> list[ThreatIntelligenceEvent]:
        """Get all emitted events."""
        return list(self._events)
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
    
    def enable(self) -> None:
        """Enable event emission."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable event emission."""
        self._enabled = False
    
    def emit_indicator_created(self, indicator_id: str, **data: Any) -> None:
        """Emit indicator created event."""
        event = ThreatIntelligenceEvent(
            event_type=ThreatIntelligenceEventType.INDICATOR_CREATED,
            entity_type="indicator",
            entity_id=indicator_id,
            data=data,
        )
        self.emit(event)
    
    def emit_indicator_updated(self, indicator_id: str, **data: Any) -> None:
        """Emit indicator updated event."""
        event = ThreatIntelligenceEvent(
            event_type=ThreatIntelligenceEventType.INDICATOR_UPDATED,
            entity_type="indicator",
            entity_id=indicator_id,
            data=data,
        )
        self.emit(event)
    
    def emit_indicator_deleted(self, indicator_id: str) -> None:
        """Emit indicator deleted event."""
        event = ThreatIntelligenceEvent(
            event_type=ThreatIntelligenceEventType.INDICATOR_DELETED,
            entity_type="indicator",
            entity_id=indicator_id,
        )
        self.emit(event)
    
    def emit_campaign_created(self, campaign_id: str, **data: Any) -> None:
        """Emit campaign created event."""
        event = ThreatIntelligenceEvent(
            event_type=ThreatIntelligenceEventType.CAMPAIGN_CREATED,
            entity_type="campaign",
            entity_id=campaign_id,
            data=data,
        )
        self.emit(event)
    
    def emit_actor_created(self, actor_id: str, **data: Any) -> None:
        """Emit actor created event."""
        event = ThreatIntelligenceEvent(
            event_type=ThreatIntelligenceEventType.ACTOR_CREATED,
            entity_type="threat_actor",
            entity_id=actor_id,
            data=data,
        )
        self.emit(event)
    
    def emit_malware_created(self, malware_id: str, **data: Any) -> None:
        """Emit malware created event."""
        event = ThreatIntelligenceEvent(
            event_type=ThreatIntelligenceEventType.MALWARE_CREATED,
            entity_type="malware",
            entity_id=malware_id,
            data=data,
        )
        self.emit(event)
    
    def emit_report_created(self, report_id: str, **data: Any) -> None:
        """Emit report created event."""
        event = ThreatIntelligenceEvent(
            event_type=ThreatIntelligenceEventType.REPORT_CREATED,
            entity_type="report",
            entity_id=report_id,
            data=data,
        )
        self.emit(event)
    
    def emit_finding_created(self, finding_id: str, **data: Any) -> None:
        """Emit finding created event."""
        event = ThreatIntelligenceEvent(
            event_type=ThreatIntelligenceEventType.FINDING_CREATED,
            entity_type="finding",
            entity_id=finding_id,
            data=data,
        )
        self.emit(event)
    
    def emit_evidence_created(self, evidence_id: str, **data: Any) -> None:
        """Emit evidence created event."""
        event = ThreatIntelligenceEvent(
            event_type=ThreatIntelligenceEventType.EVIDENCE_CREATED,
            entity_type="evidence",
            entity_id=evidence_id,
            data=data,
        )
        self.emit(event)
    
    def emit_relationship_created(self, relationship_id: str, **data: Any) -> None:
        """Emit relationship created event."""
        event = ThreatIntelligenceEvent(
            event_type=ThreatIntelligenceEventType.RELATIONSHIP_CREATED,
            entity_type="relationship",
            entity_id=relationship_id,
            data=data,
        )
        self.emit(event)
    
    def emit_confidence_updated(
        self, entity_type: str, entity_id: str, **data: Any
    ) -> None:
        """Emit confidence updated event."""
        event = ThreatIntelligenceEvent(
            event_type=ThreatIntelligenceEventType.CONFIDENCE_UPDATED,
            entity_type=entity_type,
            entity_id=entity_id,
            data=data,
        )
        self.emit(event)
