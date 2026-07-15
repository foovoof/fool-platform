"""
connectors/base/events.py

Connector Events.

Optional platform events integration.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from connectors.base.models import ConnectorType


class ConnectorEventType(Enum):
    """Connector event types."""
    INITIALIZED = "connector.initialized"
    STARTED = "connector.started"
    COMPLETED = "connector.completed"
    FAILED = "connector.failed"
    VALIDATED = "connector.validated"
    STOPPED = "connector.stopped"


@dataclass
class ConnectorEvent:
    """Connector event."""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: ConnectorEventType = ConnectorEventType.INITIALIZED
    connector_id: str = ""
    connector_type: ConnectorType = ConnectorType.GENERIC
    request_id: str | None = None
    result_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "connector_id": self.connector_id,
            "connector_type": self.connector_type.value,
            "request_id": self.request_id,
            "result_id": self.result_id,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


class ConnectorEventEmitter:
    """
    Emits connector events.
    
    Integrates with platform/events if available.
    Works without Event Bus.
    """
    
    def __init__(self) -> None:
        """Initialize emitter."""
        self._event_bus = None
        self._events: list[ConnectorEvent] = []
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
        event_type: ConnectorEventType,
        connector_id: str,
        connector_type: ConnectorType,
        request_id: str | None = None,
        result_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Emit a connector event.
        
        Args:
            event_type: Event type
            connector_id: Connector ID
            connector_type: Connector type
            request_id: Optional request ID
            result_id: Optional result ID
            metadata: Optional metadata
            
        Returns:
            True if event was emitted
        """
        event = ConnectorEvent(
            event_type=event_type,
            connector_id=connector_id,
            connector_type=connector_type,
            request_id=request_id,
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
    
    def emit_initialized(
        self,
        connector_id: str,
        connector_type: ConnectorType,
    ) -> bool:
        """Emit connector initialized event."""
        return self.emit(
            ConnectorEventType.INITIALIZED,
            connector_id,
            connector_type,
        )
    
    def emit_started(
        self,
        connector_id: str,
        connector_type: ConnectorType,
        request_id: str,
    ) -> bool:
        """Emit connector started event."""
        return self.emit(
            ConnectorEventType.STARTED,
            connector_id,
            connector_type,
            request_id=request_id,
        )
    
    def emit_completed(
        self,
        connector_id: str,
        connector_type: ConnectorType,
        request_id: str,
        result_id: str,
    ) -> bool:
        """Emit connector completed event."""
        return self.emit(
            ConnectorEventType.COMPLETED,
            connector_id,
            connector_type,
            request_id=request_id,
            result_id=result_id,
        )
    
    def emit_failed(
        self,
        connector_id: str,
        connector_type: ConnectorType,
        request_id: str,
        error: str,
    ) -> bool:
        """Emit connector failed event."""
        return self.emit(
            ConnectorEventType.FAILED,
            connector_id,
            connector_type,
            request_id=request_id,
            metadata={"error": error},
        )
    
    def emit_validated(
        self,
        connector_id: str,
        connector_type: ConnectorType,
        request_id: str,
        valid: bool,
    ) -> bool:
        """Emit connector validated event."""
        return self.emit(
            ConnectorEventType.VALIDATED,
            connector_id,
            connector_type,
            request_id=request_id,
            metadata={"valid": valid},
        )
    
    def emit_stopped(
        self,
        connector_id: str,
        connector_type: ConnectorType,
    ) -> bool:
        """Emit connector stopped event."""
        return self.emit(
            ConnectorEventType.STOPPED,
            connector_id,
            connector_type,
        )
    
    def get_events(self) -> list[ConnectorEvent]:
        """Get all emitted events."""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
    
    def has_event_bus(self) -> bool:
        """Check if connected to event bus."""
        return self._has_event_bus
