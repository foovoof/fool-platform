"""
cyber/standards/events.py

Cyber Standards Events.

Event integration with platform event bus.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class CyberStandardEventType(Enum):
    """Types of cyber standard events."""
    LOADED = "cyber.standard.loaded"
    VALIDATED = "cyber.standard.validated"
    MAPPING_CREATED = "cyber.mapping.created"
    MAPPING_FAILED = "cyber.mapping.failed"


@dataclass(frozen=True)
class CyberStandardEvent:
    """Event for cyber standard operations."""
    event_type: CyberStandardEventType
    standard_type: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    data: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "standard_type": self.standard_type,
            "timestamp": self.timestamp,
            "data": self.data,
        }


class CyberStandardEventEmitter:
    """
    Emits events for cyber standard operations.
    
    Event integration is optional.
    Does not fail if event bus is unavailable.
    """
    
    def __init__(self) -> None:
        self._events: list[CyberStandardEvent] = []
        self._enabled = True
    
    def emit(self, event: CyberStandardEvent) -> None:
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
    
    def _emit_to_bus(self, event: CyberStandardEvent) -> None:
        """
        Emit event to platform event bus.
        
        This is a no-op by default.
        Subclasses can override to integrate with actual event bus.
        """
        pass
    
    def get_events(self) -> list[CyberStandardEvent]:
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
    
    def emit_loaded(
        self, standard_type: str, version: str = ""
    ) -> None:
        """Emit standard loaded event."""
        event = CyberStandardEvent(
            event_type=CyberStandardEventType.LOADED,
            standard_type=standard_type,
            data={"version": version},
        )
        self.emit(event)
    
    def emit_validated(
        self, standard_type: str, is_valid: bool, errors: list[str] | None = None
    ) -> None:
        """Emit standard validated event."""
        event = CyberStandardEvent(
            event_type=CyberStandardEventType.VALIDATED,
            standard_type=standard_type,
            data={
                "is_valid": is_valid,
                "errors": errors or [],
            },
        )
        self.emit(event)
    
    def emit_mapping_created(
        self, standard_type: str, source_id: str, target_id: str
    ) -> None:
        """Emit mapping created event."""
        event = CyberStandardEvent(
            event_type=CyberStandardEventType.MAPPING_CREATED,
            standard_type=standard_type,
            data={
                "source_id": source_id,
                "target_id": target_id,
            },
        )
        self.emit(event)
    
    def emit_mapping_failed(
        self, standard_type: str, source_id: str, error: str
    ) -> None:
        """Emit mapping failed event."""
        event = CyberStandardEvent(
            event_type=CyberStandardEventType.MAPPING_FAILED,
            standard_type=standard_type,
            data={
                "source_id": source_id,
                "error": error,
            },
        )
        self.emit(event)
