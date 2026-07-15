"""
intelligence/capabilities/events/__init__.py

Capability Events.

Event types and emitter for capability execution.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from intelligence.capabilities.models import (
    CapabilityType,
    CapabilityStatus,
)


class CapabilityEventType(Enum):
    """Capability event types."""
    STARTED = "intelligence.capability.started"
    COMPLETED = "intelligence.capability.completed"
    FAILED = "intelligence.capability.failed"
    FINDING_CREATED = "intelligence.finding.created"
    ARTIFACT_CREATED = "intelligence.artifact.created"


@dataclass
class CapabilityEvent:
    """Represents a capability event."""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: CapabilityEventType = CapabilityEventType.STARTED
    capability_id: str = ""
    capability_type: CapabilityType = CapabilityType.RESEARCH
    task_id: str | None = None
    result_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "capability_id": self.capability_id,
            "capability_type": self.capability_type.value,
            "task_id": self.task_id,
            "result_id": self.result_id,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


class CapabilityEventEmitter:
    """
    Emits capability events.
    
    Integrates with platform/events if available.
    Event Bus integration remains optional.
    """
    
    def __init__(self) -> None:
        """Initialize emitter."""
        self._event_bus = None
        self._events: list[CapabilityEvent] = []
        self._has_event_bus = False
        self._try_connect_event_bus()
    
    def _try_connect_event_bus(self) -> None:
        """Try to connect to the platform event bus."""
        try:
            from fool_platform.events import EventBus
            self._event_bus = EventBus()
            self._has_event_bus = True
        except ImportError:
            self._has_event_bus = False
    
    def emit(
        self,
        event_type: CapabilityEventType,
        capability_id: str,
        capability_type: CapabilityType,
        task_id: str | None = None,
        result_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Emit a capability event.
        
        Args:
            event_type: Type of event
            capability_id: Capability ID
            capability_type: Capability type
            task_id: Optional task ID
            result_id: Optional result ID
            metadata: Optional metadata
            
        Returns:
            True if event was emitted
        """
        event = CapabilityEvent(
            event_type=event_type,
            capability_id=capability_id,
            capability_type=capability_type,
            task_id=task_id,
            result_id=result_id,
            metadata=metadata or {},
        )
        
        self._events.append(event)
        
        if self._event_bus and self._has_event_bus:
            try:
                self._event_bus.publish(
                    topic=event_type.value,
                    payload=event.to_dict(),
                )
            except Exception:
                pass
        
        return True
    
    def emit_started(
        self,
        capability_id: str,
        capability_type: CapabilityType,
        task_id: str,
    ) -> bool:
        """Emit capability started event."""
        return self.emit(
            CapabilityEventType.STARTED,
            capability_id,
            capability_type,
            task_id=task_id,
        )
    
    def emit_completed(
        self,
        capability_id: str,
        capability_type: CapabilityType,
        task_id: str,
        result_id: str,
    ) -> bool:
        """Emit capability completed event."""
        return self.emit(
            CapabilityEventType.COMPLETED,
            capability_id,
            capability_type,
            task_id=task_id,
            result_id=result_id,
        )
    
    def emit_failed(
        self,
        capability_id: str,
        capability_type: CapabilityType,
        task_id: str,
        error: str,
    ) -> bool:
        """Emit capability failed event."""
        return self.emit(
            CapabilityEventType.FAILED,
            capability_id,
            capability_type,
            task_id=task_id,
            metadata={"error": error},
        )
    
    def emit_finding_created(
        self,
        capability_id: str,
        capability_type: CapabilityType,
        task_id: str,
        finding_id: str,
    ) -> bool:
        """Emit finding created event."""
        return self.emit(
            CapabilityEventType.FINDING_CREATED,
            capability_id,
            capability_type,
            task_id=task_id,
            metadata={"finding_id": finding_id},
        )
    
    def emit_artifact_created(
        self,
        capability_id: str,
        capability_type: CapabilityType,
        task_id: str,
        artifact_id: str,
    ) -> bool:
        """Emit artifact created event."""
        return self.emit(
            CapabilityEventType.ARTIFACT_CREATED,
            capability_id,
            capability_type,
            task_id=task_id,
            metadata={"artifact_id": artifact_id},
        )
    
    def get_events(self) -> list[CapabilityEvent]:
        """Get all emitted events."""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
    
    def has_event_bus(self) -> bool:
        """Check if connected to event bus."""
        return self._has_event_bus
