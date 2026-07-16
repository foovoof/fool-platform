"""
cyber/mapping/events.py

Mapping Events.

Optional platform events for cyber knowledge mapping.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class MappingEventType(Enum):
    """Mapping event types."""
    CREATED = "cyber.mapping.created"
    UPDATED = "cyber.mapping.updated"
    VALIDATED = "cyber.mapping.validated"
    ONTOLOGY_BOUND = "cyber.ontology.bound"


@dataclass
class MappingEvent:
    """Mapping event."""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: MappingEventType = MappingEventType.CREATED
    mapping_id: str = ""
    entity_type: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "mapping_id": self.mapping_id,
            "entity_type": self.entity_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


class MappingEventEmitter:
    """
    Emits mapping events.
    
    Integrates with platform/events if available.
    Works without Event Bus.
    """
    
    def __init__(self) -> None:
        """Initialize emitter."""
        self._event_bus = None
        self._events: list[MappingEvent] = []
        self._has_event_bus = False
        self._try_connect_event_bus()
    
    def _try_connect_event_bus(self) -> None:
        """Try to connect to platform event bus."""
        try:
            from fool_platform.events import EventBus
            self._event_bus = EventBus()
            self._has_event_bus = True
        except ImportError:
            self._has_event_bus = False
    
    def emit(
        self,
        event_type: MappingEventType,
        mapping_id: str,
        entity_type: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Emit a mapping event.
        
        Args:
            event_type: Event type
            mapping_id: Mapping ID
            entity_type: Entity type
            metadata: Optional metadata
            
        Returns:
            True if event was emitted
        """
        event = MappingEvent(
            event_type=event_type,
            mapping_id=mapping_id,
            entity_type=entity_type,
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
    
    def emit_created(
        self,
        mapping_id: str,
        entity_type: str = "",
    ) -> bool:
        """Emit mapping created event."""
        return self.emit(
            MappingEventType.CREATED,
            mapping_id,
            entity_type,
        )
    
    def emit_updated(
        self,
        mapping_id: str,
        entity_type: str = "",
    ) -> bool:
        """Emit mapping updated event."""
        return self.emit(
            MappingEventType.UPDATED,
            mapping_id,
            entity_type,
        )
    
    def emit_validated(
        self,
        mapping_id: str,
        entity_type: str = "",
        valid: bool = True,
    ) -> bool:
        """Emit mapping validated event."""
        return self.emit(
            MappingEventType.VALIDATED,
            mapping_id,
            entity_type,
            {"valid": valid},
        )
    
    def emit_ontology_bound(
        self,
        mapping_id: str,
        entity_type: str = "",
        bindings_count: int = 0,
    ) -> bool:
        """Emit ontology bound event."""
        return self.emit(
            MappingEventType.ONTOLOGY_BOUND,
            mapping_id,
            entity_type,
            {"bindings_count": bindings_count},
        )
    
    def get_events(self) -> list[MappingEvent]:
        """Get all emitted events."""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
    
    def has_event_bus(self) -> bool:
        """Check if connected to event bus."""
        return self._has_event_bus
