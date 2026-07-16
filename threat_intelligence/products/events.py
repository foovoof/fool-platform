"""
threat_intelligence/products/events.py

Intelligence Products Events.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ProductEventType(Enum):
    """Product event types."""
    CREATED = "product.created"
    UPDATED = "product.updated"
    VERSIONED = "product.versioned"
    VALIDATED = "product.validated"
    PUBLISHED = "product.published"
    ARCHIVED = "product.archived"
    ASSERTION_ADDED = "product.assertion.added"
    LIFECYCLE_CHANGED = "product.lifecycle.changed"


@dataclass
class ProductEvent:
    """Product event."""
    event_type: str
    product_id: str
    timestamp: str
    data: dict[str, Any]
    actor: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "product_id": self.product_id,
            "timestamp": self.timestamp,
            "data": self.data,
            "actor": self.actor,
        }


class ProductEventEmitter:
    """Emitter for product events."""
    
    def __init__(self) -> None:
        self._events: list[ProductEvent] = []
        self._enabled = True
    
    def enable(self) -> None:
        """Enable event emission."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable event emission."""
        self._enabled = False
    
    def emit(self, event: ProductEvent) -> None:
        """Emit an event."""
        if self._enabled:
            self._events.append(event)
    
    def emit_created(self, product_id: str, data: dict[str, Any] = None) -> None:
        """Emit created event."""
        self.emit(ProductEvent(
            event_type=ProductEventType.CREATED.value,
            product_id=product_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data or {},
        ))
    
    def emit_updated(self, product_id: str, data: dict[str, Any] = None) -> None:
        """Emit updated event."""
        self.emit(ProductEvent(
            event_type=ProductEventType.UPDATED.value,
            product_id=product_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data or {},
        ))
    
    def emit_versioned(self, product_id: str, version_id: str, version: int) -> None:
        """Emit versioned event."""
        self.emit(ProductEvent(
            event_type=ProductEventType.VERSIONED.value,
            product_id=product_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"version_id": version_id, "version": version},
        ))
    
    def emit_validated(self, product_id: str, result: bool) -> None:
        """Emit validated event."""
        self.emit(ProductEvent(
            event_type=ProductEventType.VALIDATED.value,
            product_id=product_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"result": result},
        ))
    
    def emit_published(self, product_id: str) -> None:
        """Emit published event."""
        self.emit(ProductEvent(
            event_type=ProductEventType.PUBLISHED.value,
            product_id=product_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
        ))
    
    def emit_archived(self, product_id: str) -> None:
        """Emit archived event."""
        self.emit(ProductEvent(
            event_type=ProductEventType.ARCHIVED.value,
            product_id=product_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
        ))
    
    def emit_assertion_added(self, product_id: str, assertion_id: str) -> None:
        """Emit assertion added event."""
        self.emit(ProductEvent(
            event_type=ProductEventType.ASSERTION_ADDED.value,
            product_id=product_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"assertion_id": assertion_id},
        ))
    
    def emit_lifecycle_changed(self, product_id: str, from_status: str, to_status: str) -> None:
        """Emit lifecycle changed event."""
        self.emit(ProductEvent(
            event_type=ProductEventType.LIFECYCLE_CHANGED.value,
            product_id=product_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"from_status": from_status, "to_status": to_status},
        ))
    
    def get_events(self) -> list[ProductEvent]:
        """Get all events."""
        return list(self._events)
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
