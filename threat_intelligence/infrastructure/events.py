"""
threat_intelligence/infrastructure/events.py

Infrastructure Events.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class InfrastructureEventType(Enum):
    """Infrastructure event types."""
    CREATED = "infrastructure.created"
    UPDATED = "infrastructure.updated"
    ARCHIVED = "infrastructure.archived"
    RELATIONSHIP_CREATED = "infrastructure.relationship.created"
    ASSERTION_CREATED = "infrastructure.assertion.created"
    VALIDATED = "infrastructure.validated"
    VERSION_CREATED = "infrastructure.version.created"
    EVIDENCE_ATTACHED = "infrastructure.evidence.attached"


@dataclass
class InfrastructureEvent:
    """Infrastructure event."""
    event_type: str
    infrastructure_id: str
    timestamp: str
    data: dict[str, Any]
    actor: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "infrastructure_id": self.infrastructure_id,
            "timestamp": self.timestamp,
            "data": self.data,
            "actor": self.actor,
        }


class InfrastructureEventEmitter:
    """Emitter for infrastructure events."""
    
    def __init__(self) -> None:
        self._events: list[InfrastructureEvent] = []
        self._enabled = True
    
    def enable(self) -> None:
        """Enable event emission."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable event emission."""
        self._enabled = False
    
    def emit(self, event: InfrastructureEvent) -> None:
        """Emit an event."""
        if self._enabled:
            self._events.append(event)
    
    def emit_created(self, infrastructure_id: str, data: dict[str, Any] = None) -> None:
        """Emit created event."""
        self.emit(InfrastructureEvent(
            event_type=InfrastructureEventType.CREATED.value,
            infrastructure_id=infrastructure_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data or {},
        ))
    
    def emit_updated(self, infrastructure_id: str, data: dict[str, Any] = None) -> None:
        """Emit updated event."""
        self.emit(InfrastructureEvent(
            event_type=InfrastructureEventType.UPDATED.value,
            infrastructure_id=infrastructure_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data or {},
        ))
    
    def emit_archived(self, infrastructure_id: str) -> None:
        """Emit archived event."""
        self.emit(InfrastructureEvent(
            event_type=InfrastructureEventType.ARCHIVED.value,
            infrastructure_id=infrastructure_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
        ))
    
    def emit_relationship_created(self, infrastructure_id: str, relationship_id: str) -> None:
        """Emit relationship created event."""
        self.emit(InfrastructureEvent(
            event_type=InfrastructureEventType.RELATIONSHIP_CREATED.value,
            infrastructure_id=infrastructure_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"relationship_id": relationship_id},
        ))
    
    def emit_assertion_created(self, infrastructure_id: str, assertion_id: str) -> None:
        """Emit assertion created event."""
        self.emit(InfrastructureEvent(
            event_type=InfrastructureEventType.ASSERTION_CREATED.value,
            infrastructure_id=infrastructure_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"assertion_id": assertion_id},
        ))
    
    def emit_validated(self, infrastructure_id: str) -> None:
        """Emit validated event."""
        self.emit(InfrastructureEvent(
            event_type=InfrastructureEventType.VALIDATED.value,
            infrastructure_id=infrastructure_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
        ))
    
    def emit_version_created(self, infrastructure_id: str, version_id: str) -> None:
        """Emit version created event."""
        self.emit(InfrastructureEvent(
            event_type=InfrastructureEventType.VERSION_CREATED.value,
            infrastructure_id=infrastructure_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"version_id": version_id},
        ))
    
    def emit_evidence_attached(self, infrastructure_id: str, evidence_id: str) -> None:
        """Emit evidence attached event."""
        self.emit(InfrastructureEvent(
            event_type=InfrastructureEventType.EVIDENCE_ATTACHED.value,
            infrastructure_id=infrastructure_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"evidence_id": evidence_id},
        ))
    
    def get_events(self) -> list[InfrastructureEvent]:
        """Get all events."""
        return list(self._events)
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
