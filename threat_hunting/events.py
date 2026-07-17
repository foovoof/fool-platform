"""
threat_hunting/events.py

Threat Hunting Events.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class HuntEventType(Enum):
    """Hunt event types."""
    STARTED = "hunt.started"
    COMPLETED = "hunt.completed"
    CANCELLED = "hunt.cancelled"
    HYPOTHESIS_CREATED = "hypothesis.created"
    HYPOTHESIS_APPROVED = "hypothesis.approved"
    HYPOTHESIS_VALIDATED = "hypothesis.validated"
    HYPOTHESIS_REJECTED = "hypothesis.rejected"
    OBSERVATION_RECORDED = "observation.recorded"
    FINDING_GENERATED = "finding.generated"
    EVIDENCE_AGGREGATED = "evidence.aggregated"
    REPORT_GENERATED = "report.generated"
    SESSION_STARTED = "session.started"
    SESSION_COMPLETED = "session.completed"


@dataclass
class HuntEvent:
    """Hunt event."""
    event_type: str
    hunt_id: str
    timestamp: str
    data: dict[str, Any]
    actor: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "hunt_id": self.hunt_id,
            "timestamp": self.timestamp,
            "data": self.data,
            "actor": self.actor,
        }


class HuntEventEmitter:
    """Emitter for hunt events."""
    
    def __init__(self) -> None:
        self._events: list[HuntEvent] = []
        self._enabled = True
    
    def enable(self) -> None:
        """Enable event emission."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable event emission."""
        self._enabled = False
    
    def emit(self, event: HuntEvent) -> None:
        """Emit an event."""
        if self._enabled:
            self._events.append(event)
    
    def emit_hunt_started(self, hunt_id: str, actor: str = "") -> None:
        """Emit hunt started event."""
        self.emit(HuntEvent(
            event_type=HuntEventType.STARTED.value,
            hunt_id=hunt_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_hunt_completed(self, hunt_id: str, actor: str = "") -> None:
        """Emit hunt completed event."""
        self.emit(HuntEvent(
            event_type=HuntEventType.COMPLETED.value,
            hunt_id=hunt_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_hypothesis_created(self, hunt_id: str, hypothesis_id: str) -> None:
        """Emit hypothesis created event."""
        self.emit(HuntEvent(
            event_type=HuntEventType.HYPOTHESIS_CREATED.value,
            hunt_id=hunt_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"hypothesis_id": hypothesis_id},
        ))
    
    def emit_observation_recorded(self, hunt_id: str, observation_id: str) -> None:
        """Emit observation recorded event."""
        self.emit(HuntEvent(
            event_type=HuntEventType.OBSERVATION_RECORDED.value,
            hunt_id=hunt_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"observation_id": observation_id},
        ))
    
    def emit_finding_generated(self, hunt_id: str, finding_id: str) -> None:
        """Emit finding generated event."""
        self.emit(HuntEvent(
            event_type=HuntEventType.FINDING_GENERATED.value,
            hunt_id=hunt_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"finding_id": finding_id},
        ))
    
    def emit_report_generated(self, hunt_id: str, report_id: str) -> None:
        """Emit report generated event."""
        self.emit(HuntEvent(
            event_type=HuntEventType.REPORT_GENERATED.value,
            hunt_id=hunt_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"report_id": report_id},
        ))
    
    def emit_session_started(self, hunt_id: str, session_id: str) -> None:
        """Emit session started event."""
        self.emit(HuntEvent(
            event_type=HuntEventType.SESSION_STARTED.value,
            hunt_id=hunt_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"session_id": session_id},
        ))
    
    def emit_session_completed(self, hunt_id: str, session_id: str) -> None:
        """Emit session completed event."""
        self.emit(HuntEvent(
            event_type=HuntEventType.SESSION_COMPLETED.value,
            hunt_id=hunt_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"session_id": session_id},
        ))
    
    def get_events(self) -> list[HuntEvent]:
        """Get all events."""
        return list(self._events)
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
